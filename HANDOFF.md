# HANDOFF · 猫波信号站

> 打开新会话时读此文件，了解当前状态和下一步。

## 当前状态

**架构重构完成（2026-06-22）**：pipeline.py 已拆分为 7 个独立阶段脚本，合并入 catwave skill。旧 Cursor Team 字幕需要按新逻辑重跑。

## 架构

```
D:\workspace\lab\2026-06-16-猫波信号站\                   ← Lab 根目录
│
├── .claude/skills/catwave/              ← 唯一真相源
│   ├── SKILL.md                         ← 全流程定义 + 门禁标准 + 调用方式
│   └── tools/
│       ├── _lib.py                      ← 共享：SubEntry / SRT读写 / 时间工具 / 路径
│       ├── stage_02_download.py         ← ② yt-dlp 下载
│       ├── stage_03_segment.py          ← ③ 去重叠 + LLM补标点（短句模式）
│       ├── stage_04_sponsor.py          ← ④ 赞助检测 → cuts.json
│       ├── stage_05_translate.py        ← ⑤ DeepSeek 翻译 + 专名修复
│       ├── stage_06_split.py            ← ⑥ 标点优先拆分 + PIL 像素宽度
│       ├── stage_07_ass.py              ← ⑦ ASS + transcript
│       ├── stage_08_render.py           ← ⑧ ffmpeg + 赞助裁剪
│       └── gen_cover.py                 ← ⑩ 封面合成
│
├── _runtime/<slug>_process/             ← 下载缓存（source.mp4 + 01_raw.srt）
├── 生产方法论.html                       ← 完整方法论
└── HANDOFF.md                           ← 本文档

D:\workspace\_output\猫波信号站\视频\<YYYYMMDD_slug>\
│   _runtime/字幕/  ← 01_raw → 02_seg → 02_seg_clean → 03_zh → 04_split → 05.ass
│   _runtime/_sponsor_cuts.json  ← 赞助时间戳（⑧消费）
│   成片/           ← <标题>.mp4
│   cover.jpg / 发布面板.html / draft.md
```

**核心原则：** SKILL.md 是唯一真相源；每个阶段一个独立脚本，阶段间通过文件通信。

## 待做

- [ ] ③ 重跑：新断句逻辑（去重叠 + LLM短句标点）替代旧 pipeline.py 的"合并为长句"
- [ ] ⑤⑥⑦⑧ 重跑：翻译→字宽→ASS→渲染
- [ ] 发布到 B站

## 旧架构（已删除）

- `pipeline.py` → 已拆为 `tools/stage_02_*.py` ~ `stage_08_*.py`
- `.claude/skills/猫波信号站/` → 已重命名为 `catwave`
- `_tools/gen_cover.py` → 已移入 `catwave/tools/`

## 关键约束

- yt-dlp 必须 H.264+AAC
- YouTube 需代理 VORTEX_PROXY 127.0.0.1:7897
- DEEPSEEK_API_KEY 用于 ③④⑤
- ffmpeg 渲染 ASS：必须 chdir 到字幕目录用相对路径
- 文件名禁止全角冒号 U+FF1A
- 封面：msyhbd.ttc 纯色无描边，亮度 0.80，#FFC82D，≤4.8MB
- 视频文件名 = B站标题，标题 ≤80 字
