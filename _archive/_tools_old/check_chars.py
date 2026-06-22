import re

with open(r'D:\Claude code_workspace\2026-06-16-youtube-content-pipeline\_runtime\downloads\test_2min.en_seg_zh_split.ass', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    if 'Dialogue:' not in line:
        continue
    # Extract between last ASS tag } and the literal \N
    # Format: ...{\fnSimHei\fs42}CHINESE TEXT\N{\fnSegoe UI...
    m = re.search(r'\\fs42\}(.+?)\\N', line)
    if not m:
        continue
    zh = m.group(1)
    n = len(zh)
    if n > 28:
        print(f'OVER {n:2d}: {zh}')
    else:
        print(f'OK   {n:2d}: {zh}')
