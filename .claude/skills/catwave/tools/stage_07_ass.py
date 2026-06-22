"""Stage ⑦: Generate ASS subtitle file + transcript.

Usage: python stage_07_ass.py --slug <slug>
Input:  <output>/_runtime/字幕/04_split.srt
Output: <output>/_runtime/字幕/05.ass + transcript.txt
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import (
    SubEntry, extract_transcript, ms_to_time, read_srt, srt_path, time_to_ms, write_srt,
)


def run(slug: str):
    src = srt_path(slug, "04_split.srt")
    if not src.exists():
        print(f"ERROR: {src} not found. Run stage_06 first.")
        sys.exit(1)

    entries = read_srt(src)

    # Fix overlapping segments
    fixed = _clip_overlaps(entries)

    # Generate ASS
    ass = _generate_ass(fixed)
    ass_path = srt_path(slug, "05.ass")
    ass_path.write_text(ass, encoding="utf-8")
    print(f"[⑦] ASS: {len(fixed)} events → {ass_path.name}")

    # Generate transcript (Chinese-only plain text)
    cn_entries = [_cn_only(e) for e in fixed]
    transcript = extract_transcript(cn_entries)
    tx_path = srt_path(slug, "transcript.txt")
    tx_path.write_text(transcript, encoding="utf-8")
    print(f"  Transcript → {tx_path.name}")


def _clip_overlaps(entries: list[SubEntry]) -> list[SubEntry]:
    fixed = []
    for i, e in enumerate(entries):
        end_ms = time_to_ms(e.end)
        if i + 1 < len(entries):
            next_start_ms = time_to_ms(entries[i + 1].start)
            if end_ms > next_start_ms:
                end_ms = max(next_start_ms - 20, time_to_ms(e.start) + 500)
        fixed.append(SubEntry(e.index, e.start, ms_to_time(end_ms), e.text))
    return fixed


def _cn_only(e: SubEntry) -> SubEntry:
    parts = e.text.split("\\N", 1)
    return SubEntry(e.index, e.start, e.end, parts[0])


def _generate_ass(entries: list[SubEntry]) -> str:
    header = """[Script Info]
Title: Bilingual Subtitles
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Style: Default,SimHei,42,&H00FFFFFF&,&H00000000&,&H00FFFFFF&,&H00000000&,0,0,0,0,100,100,0,0,1,0,0,2,200,200,45,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for e in entries:
        start = _ass_time(e.start)
        end = _ass_time(e.end)
        text = e.text.replace("\\N", "\\N{\\fnMicrosoft YaHei}")
        lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,45,,{text}")
    return "\n".join(lines)


def _ass_time(srt_time: str) -> str:
    h, m, rest = srt_time.split(":")
    s, ms = rest.split(",")
    return f"{int(h)}:{m}:{s}.{ms[:2]}"


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="⑦ Generate ASS + transcript")
    p.add_argument("--slug", required=True)
    args = p.parse_args()
    run(args.slug)
