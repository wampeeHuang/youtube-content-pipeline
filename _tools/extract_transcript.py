import re
from pathlib import Path

src = Path(r'D:\Claude code_workspace\2026-06-16-youtube-content-pipeline\_runtime\downloads\boris_sequoia.en_seg.srt')
out = Path(r'D:\Claude code_workspace\2026-06-16-youtube-content-pipeline\_runtime\boris_sequoia_transcript.txt')

with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

blocks = re.split(r'\n\s*\n', content.strip())
lines_out = []
for block in blocks:
    lines = block.strip().split('\n')
    if len(lines) >= 3:
        lines_out.append(lines[2])

with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_out))

print(f'Done: {len(lines_out)} lines, {sum(len(l) for l in lines_out)} chars')
