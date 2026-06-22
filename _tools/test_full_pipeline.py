"""End-to-end test: segment -> translate -> enforce_chars -> ASS -> render"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import segment_srt, translate_srt, enforce_max_chars, srt_to_ass, render_subtitles

DOWNLOADS = Path(__file__).parent.parent / "_runtime" / "downloads"

srt_en = DOWNLOADS / "test_2min.en.srt"
video = DOWNLOADS / "test_2min_h264.mp4"

# Step 1: Segment
print("=" * 60)
print("STEP 1: Sentence Segmentation")
print("=" * 60)
srt_seg = segment_srt(srt_en)

# Step 2: Translate
print()
print("=" * 60)
print("STEP 2: Translate EN -> ZH")
print("=" * 60)
srt_zh = translate_srt(srt_seg)

# Step 2.5: Enforce max chars
print()
print("=" * 60)
print("STEP 2.5: Enforce Max Chinese Chars")
print("=" * 60)
srt_split = enforce_max_chars(srt_zh)

# Step 3: Generate ASS
print()
print("=" * 60)
print("STEP 3: Generate ASS")
print("=" * 60)
ass = srt_to_ass(srt_split)

# Step 4: Render
print()
print("=" * 60)
print("STEP 4: Render")
print("=" * 60)
output = render_subtitles(video, ass)

print()
print("=" * 60)
print(f"DONE: {output}")
print("=" * 60)
