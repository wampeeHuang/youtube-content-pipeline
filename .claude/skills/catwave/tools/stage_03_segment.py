"""Stage ③: Merge time-overlapping YouTube fragments, then LLM adds punctuation.

Usage: python stage_03_segment.py --slug <slug>
Input:  <lab>/_runtime/<slug>_process/01_raw.srt
Output: <output>/_runtime/字幕/02_seg.srt

Logic:
  1. Scan 01_raw.srt fragments. Consecutive fragments whose time ranges overlap
     are merged into one segment (mechanical, no LLM).
  2. Non-overlapping fragments stay independent — each is already a natural subtitle unit.
  3. Segments are sent to DeepSeek in batches (20/batch). LLM adds punctuation and
     splits at EVERY major punctuation mark (comma, period, semicolon, etc.) with <S>.
  4. Each <S> clause inherits a proportional slice of the segment's time range.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import (
    PROCESS_ROOT, SubEntry, ms_to_time, read_srt, srt_path, time_to_ms, write_srt,
)


def run(slug: str, *, api_key: str | None = None):
    api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")

    # Read raw YouTube fragments
    lab_srt = PROCESS_ROOT / slug / "_process" / "01_raw.srt"
    if not lab_srt.exists():
        # Try date-prefix match
        hits = sorted(PROCESS_ROOT.glob(f"*_{slug}"))
        lab_srt = hits[0] / "_process" / "01_raw.srt" if hits else lab_srt
    if not lab_srt.exists():
        print(f"ERROR: {lab_srt} not found. Run stage_02_download first.")
        sys.exit(1)

    raw = read_srt(lab_srt)
    print(f"[③] {len(raw)} raw fragments → merging overlapping...")

    # Step 1: Mechanical de-overlap
    merged = _merge_overlapping(raw)
    print(f"  {len(merged)} segments after time-overlap merge")

    if not api_key:
        print("  WARNING: No DEEPSEEK_API_KEY, writing merged text as-is")
        out = srt_path(slug, "02_seg.srt")
        write_srt(merged, out)
        print(f"  → {out}")
        return

    # Step 2: LLM punctuation on short clauses
    print(f"  Adding punctuation via DeepSeek...")
    segmented = _llm_add_punctuation(merged, api_key)
    print(f"  {len(segmented)} clauses after punctuation split")

    out = srt_path(slug, "02_seg.srt")
    write_srt(segmented, out)
    print(f"  → {out}")


# ── Mechanical de-overlap ────────────────────────────────────────────────────


def _merge_overlapping(entries: list[SubEntry]) -> list[SubEntry]:
    """Merge consecutive fragments whose time ranges overlap.

    YouTube auto-captions produce fragments like:
      A: 00:00 → 00:04  "the following is"
      B: 00:02 → 00:08  "a conversation with"
    These overlap at 00:02-00:04 → merge into one segment.

    Non-overlapping fragments stay independent.
    """
    if not entries:
        return []
    result = []
    buf, buf_start, buf_end = [], None, None
    for e in entries:
        if buf_start is None:
            buf_start = e.start
        buf.append(e.text)
        buf_end = e.end
        # Check if NEXT fragment overlaps with current buffer's end
        # Overlap: next.start < current.end + 200ms (allow small gap)
        next_idx = entries.index(e) + 1 if hasattr(entries, 'index') else 0
    # Re-implement with explicit loop
    result = []
    i = 0
    while i < len(entries):
        buf = [entries[i].text]
        buf_start = entries[i].start
        buf_end = entries[i].end
        j = i + 1
        while j < len(entries):
            next_start_ms = time_to_ms(entries[j].start)
            buf_end_ms = time_to_ms(buf_end)
            # Overlap if next fragment starts before current buffer ends + 200ms gap
            if next_start_ms <= buf_end_ms + 200:
                buf.append(entries[j].text)
                buf_end = entries[j].end  # Extend to latest end
                j += 1
            else:
                break
        text = " ".join(buf)
        result.append(SubEntry(len(result) + 1, buf_start, buf_end, text.strip()))
        i = j

    return result


# ── LLM punctuation (short-clause mode) ──────────────────────────────────────


def _llm_add_punctuation(segments: list[SubEntry], api_key: str) -> list[SubEntry]:
    """Send segments to DeepSeek. Returns clauses split at every punctuation mark.

    Prompt instructs LLM to:
    - Add punctuation to ASR text (never change words)
    - Split at EVERY major punctuation: . , ; : ! ?
    - Use <S> as split marker
    - Keep clauses short — one breath-length each
    """
    if len(segments) < 3:
        return segments

    batch_size = 20
    batches = [segments[i:i + batch_size] for i in range(0, len(segments), batch_size)]

    all_clauses = []  # list of (text, segment_start_ms, segment_end_ms, batch_index)
    seg_offset = 0

    for bi, batch in enumerate(batches):
        batch_start_ms = time_to_ms(segments[seg_offset].start)
        batch_end_ms = time_to_ms(segments[seg_offset + len(batch) - 1].end)

        # Build prompt
        lines = [f"{li+1}. {e.text.strip()}" for li, e in enumerate(batch)]
        prompt_lines = "\n".join(lines)

        prompt = (
            "Add punctuation (periods, commas, question marks, semicolons, colons) "
            "to these English transcript fragments. CRITICAL: do NOT change ANY words. Only add punctuation.\n\n"
            "Split at EVERY punctuation mark with <S>. Do NOT merge fragments together.\n"
            "Goal: each <S> clause should be short — one breath, ~5-15 words.\n"
            "Output the punctuated text with <S> markers only, no line numbers, no explanations.\n\n"
            f"{prompt_lines}"
        )

        result = None
        for attempt in range(2):
            try:
                req = urllib.request.Request(
                    "https://api.deepseek.com/v1/chat/completions",
                    data=json.dumps({
                        "model": "deepseek-chat",
                        "messages": [
                            {"role": "system", "content": (
                                "You restore punctuation to ASR transcripts. "
                                "Split at EVERY punctuation mark (. , ; : ! ?) with <S>. "
                                "Never change any word. Keep clauses short."
                            )},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.1,
                        "max_tokens": 8192,
                    }).encode(),
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                )
                with urllib.request.urlopen(req, timeout=180) as resp:
                    body = json.loads(resp.read())
                    result = body["choices"][0]["message"]["content"].strip()
                    break
            except Exception as e:
                if attempt == 1:
                    print(f"    Batch {bi} failed: {e}")
                time.sleep(2)

        if result:
            clauses = [s.strip() for s in result.split("<S>") if s.strip()]
            for clause in clauses:
                all_clauses.append((clause, batch_start_ms, batch_end_ms, bi))

        seg_offset += len(batch)

    if not all_clauses:
        return segments  # Fallback: return merged segments as-is

    # Distribute clauses into time ranges
    return _distribute_time(all_clauses)


def _distribute_time(clauses: list[tuple[str, int, int, int]]) -> list[SubEntry]:
    """Assign time ranges to clauses. Within each batch, even distribution."""
    groups = defaultdict(list)
    for text, start_ms, end_ms, bi in clauses:
        groups[bi].append((text, start_ms, end_ms))

    result = []
    seq = 1
    for bi in sorted(groups.keys()):
        group = groups[bi]
        _, batch_start_ms, batch_end_ms = group[0]
        n = len(group)
        segment_ms = max((batch_end_ms - batch_start_ms) // n, 800)

        for j, (text, _, _) in enumerate(group):
            start_ms = batch_start_ms + j * segment_ms
            end_ms = min(start_ms + segment_ms, batch_end_ms)
            result.append(SubEntry(seq, ms_to_time(start_ms), ms_to_time(end_ms), text))
            seq += 1

    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="③ De-overlap + LLM punctuation")
    p.add_argument("--slug", required=True)
    args = p.parse_args()
    run(args.slug)
