# HANDOFF · 猫波信号站

> 打开新会话时读此文件，了解当前状态和下一步。

## 当前状态

Kevin Weil 期已完成制作。架构调整：管线 SDK 在 lab，制作全周期在 output/视频/YYYYMMDD_slug/。

## 已做 (2026-06-20)

- [x] Kevin Weil 期完成：下载 → 断句(245条) → 翻译 → ASS → 渲染 → 封面 → 发布面板
- [x] 架构调整：lab = 管线 SDK，output/视频/ = 制作全周期
- [x] lab CLAUDE.md 重写：明确 SDK 定位，`_runtime/` 仅开发测试用
- [x] output CLAUDE.md 修正：视频目录 YYYYMMDD_slug/（纯英文），`_runtime/` 归视频目录
- [x] Kevin Weil 文件搬家：从 lab `_runtime/` → output `20260620_kevin-weil-lenny/`
- [x] 飞书表格 Kevin Weil 状态→已发布，B站标题已写入
- [x] 飞书 API 踩坑：更新记录用**字段名**不是字段 ID（PUT records 用中文名，fields API 用 ID）

## Kevin Weil 交付物

```
D:\workspace\_output\猫波信号站\视频\20260620_kevin-weil-lenny\
├── 成片/OpenAI CPO Kevin Weil：你现在用的AI是你余生最差的——AI每两个月就颠覆一次.mp4
├── cover.jpg
├── 发布面板.html
└── _runtime/
    ├── draft.md (专栏文章草稿)
    ├── frames/frame_2700s.jpg
    └── 字幕/ (01_raw~05.ass + transcript.txt)
```

## 飞书选题库

| 项目 | 值 |
|------|-----|
| URL | https://fcn7dgp1xcm8.feishu.cn/base/F7E8bJie5aX3BvsZz1Xc9KiznNb?table=tblIs359fHfIapwd |
| App Token | F7E8bJie5aX3BvsZz1Xc9KiznNb |
| Table ID | tblIs359fHfIapwd |
| Token 刷新 | `echo '{"ids":["app-cli_aa992600d0215cb2"]}' \| lark-channel-bridge secrets get` |

## 未做 / 下一步

### 剩余选题

飞书表格 2 个候选 (2026-06-19 入库)：

| # | 候选 | 评分 | 来源 |
|---|------|------|------|
| 1 | Cursor Team：AI 编程的未来 | 29 | Lex Fridman |
| 2 | Dan Shipper：AI 原生创业 | 26 | Lenny's Podcast |

### 管线改进

- Kevin Weil 翻译有 50+ 条"未翻译"（赞助商口播 + 语速过快段落），后续可改进 prompt 或加 fallback
- pipeline.py 需要 `--work-dir` 参数支持目标目录
- 字幕同步未做全局偏移修正

## 关键文件指针

```
D:\workspace\lab\2026-06-16-猫波信号站\         ← 管线 SDK
D:\workspace\_output\猫波信号站\                 ← 产出根
D:\workspace\_output\猫波信号站\CLAUDE.md        ← 产出宪法
D:\workspace\_output\猫波信号站\视频\CLAUDE.md    ← 视频目录规范 + 生命周期
D:\workspace\_output\猫波信号站\视频\20260620_kevin-weil-lenny\  ← Kevin Weil 期
D:\workspace\_output\猫波信号站\选题库\飞书选题库.md  ← API 参数 + 字段速查
```

## 关键约束

- 文件名禁止全角冒号 U+FF1A
- Python 文件 I/O 显式 `encoding='utf-8'`
- yt-dlp 必须指定 H.264+AAC
- ASS 用单事件 `\N` 双语
- 封面亮度 0.80，SimHei，#FFC82D 暖黄
- 视频文件名 = B站标题，标题 ≤80 字
- 飞书 API：更新记录用字段名（中文），不用 field_id
- 视频目录命名：YYYYMMDD_slug/（纯英文）
- ffmpeg Windows 路径有 `:` 时用相对路径绕开 filter parser
