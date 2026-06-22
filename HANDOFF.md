# HANDOFF · 猫波信号站

> 打开新会话时读此文件，了解当前状态和下一步。

## 当前状态

**基础版测试片已完成（2026-06-22）**：无背景框，纯白双语字幕，95s。
背景框功能代码在 stage_07_ass.py 中但**默认关闭**（--bg-opacity 0），因色块与文字相对位置不对，暂时搁置。

## 管道进度

| # | 阶段 | 状态 | 产出 |
|---|------|------|------|
| ② | 下载 | ✅ | source.mp4 + 01_raw.srt |
| ③ | 去重叠+标点 | ✅ | 3917碎片→287段→2014短句 |
| ④ | 赞助检测 | ✅ | 2条赞助 cut（49.6-54.1s + 2:28:39-2:28:42） |
| ⑤ | 翻译 | ✅ | 2012条双语字幕 |
| ⑥ | 字宽拆分 | ✅ | 2012→2318行，6条超1520px |
| ⑦ | ASS | ✅ | SimHei 42px + YaHei，Outline=0，MarginL/R=200 |
| ⑧ | 测试片 | ✅ | test_95s.mp4 (95s, 无背景框, 赞助段未裁) |
| ⑧ | 全片 | ✅ 旧版 | Cursor创始人团队：AI编程的未来.mp4 (1.28GB, 旧ASS) |

## 已知问题

1. **背景框位置偏差**：色块与文字相对位置不对，用户反馈"对不上"。代码保留在 stage_07_ass.py（`--bg-opacity` 参数），默认关闭。
2. **测试片赞助段未裁**：95s 测试片包含 49.6-54.1s 赞助内容，该段无翻译字幕。
3. **全片 concat 方案字幕同步**：`_render_with_cuts` 用 concat 拼接视频段后烧录 ASS，时间轴改变后字幕偏移。赞助剪切点之后可能偏移约 4.5s。未验证。

## 待做

- [ ] 修复背景框位置（用户说色块跟字幕对不上）
- [ ] 修复全片渲染 concat 字幕同步
- [ ] 重新渲染全片（修复后）
- [ ] 测试片赞助段处理（裁剪或翻译）
- [ ] ⑨-⑭ AI 决策段
- [ ] 发布到 B站

## 架构

```
D:\workspace\lab\2026-06-16-猫波信号站\                   ← Lab 根目录
│
├── .claude/skills/video-catwave/              ← 唯一真相源
│   ├── SKILL.md                         ← 全流程定义 + 门禁标准 + 调用方式
│   └── tools/
│       ├── _lib.py                      ← 共享：SubEntry / SRT读写 / 时间工具 / 路径
│       ├── stage_02_download.py         ← ② yt-dlp 下载
│       ├── stage_03_segment.py          ← ③ 去重叠（30s cap）+ LLM补标点（per-segment）
│       ├── stage_04_sponsor.py          ← ④ 赞助检测 → cuts.json
│       ├── stage_05_translate.py        ← ⑤ DeepSeek 翻译 + 专名修复
│       ├── stage_06_split.py            ← ⑥ 标点优先拆分 + PIL 像素宽度
│       ├── stage_07_ass.py              ← ⑦ ASS + transcript（背景框默认关闭）
│       ├── stage_08_render.py           ← ⑧ ffmpeg（测试片简单烧录/全片concat裁赞助）
│       └── gen_cover.py                 ← ⑩ 封面合成
│
├── _archive/_tools_old/                 ← 旧 _tools/ 归档
└── HANDOFF.md                           ← 本文档

D:\workspace\_output\猫波信号站\视频\20260620_cursor-team-lex-fridman\
│   _runtime/字幕/  ← 01_raw → 02_seg → 02_seg_clean → 03_zh → 04_split → 05.ass
│   _runtime/_sponsor_cuts.json  ← 赞助时间戳
│   _runtime/测试片/  ← test_95s.mp4（当前最新）
│   成片/           ← Cursor创始人团队：AI编程的未来.mp4（旧版）
│   cover.jpg / 发布面板.html / draft.md
```

## 关键约束

- yt-dlp 必须 H.264+AAC
- YouTube 需代理 VORTEX_PROXY 127.0.0.1:7897
- DEEPSEEK_API_KEY 用于 ③④⑤
- ffmpeg 渲染 ASS：必须 chdir 到字幕目录用相对路径
- 文件名禁止全角冒号 U+FF1A
- 封面：msyhbd.ttc 纯色无描边，亮度 0.80，#FFC82D，≤4.8MB
- 视频文件名 = B站标题，标题 ≤80 字
- 成片只保留最终交付物，测试片放 _runtime/测试片/
