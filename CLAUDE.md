# 猫波信号站

YouTube → B站 管线 SDK：下载、断句、翻译、字幕渲染、封面、元数据。这里是管线代码的开发和迭代仓库，不存放各期视频的制作过程文件。

## 项目定位

**管线 SDK** — 只管工具链（pipeline.py、脚本、参考、生产参数）的迭代。每期视频的制作全周期在产出目录进行。

产出目录：`D:\workspace\_output\猫波信号站\`（唯一真相源，详见该目录 CLAUDE.md）

## 文件管理规则

### 目录职责

| 目录 | 职责 | 谁看 | 规则 |
|------|------|------|------|
| `CLAUDE.md` | 项目硬约束+坑+流程 | Agent | 只放规则和硬约束，不放软知识 |
| `生产方法论.html` | 统一方法论入口（真相源） | Agent+人类 | 选题/封面/标题/字幕/发布/选题库/技能迭代全流程，可复制粘贴参数 |
| `_tools/` | 辅助脚本 | Agent | 封面/头像生成、转录处理、测试。每个脚本只做一件事 |
| `_ref/` | 参考素材 + 生产参数 | Agent+人类 | `生产参数.md`=封面/标题/字幕唯一真相源，`pitfalls.md`=踩坑日志（唯一真相源，生产前必读），格式见 §踩坑日志 |
| `_archive/` | 过程归档 | — | 已废弃/被替代的文件，不读只存 |

**`_runtime/` 仅用于管线开发测试**，不存放各期视频实际制作文件。各期制作全周期统一在 `D:\workspace\_output\猫波信号站\视频\<YYYYMMDD_slug>\` 下。

### 每期视频文件夹约定

见 `D:\workspace\_output\猫波信号站\视频\CLAUDE.md` §目录规范。各期制作全周期在产出目录下进行。

管线脚本通过 `--slug` 参数指定目标视频目录 slug，自动在产出目录下找到或创建对应文件夹。

### 文件命名红线

- **禁止全角冒号（：U+FF1A）** 在文件名中，shell 编码必然炸
- 视频成品 = B站标题（≤80字），上传时自动识别
- 字幕中间产物文件名固定（`01_raw.srt` ~ `05.ass`），路径见产出目录视频/CLAUDE.md
- 封面固定为 `cover.jpg`，不保留多版本
- 不使用 `_final` `_v2` `_old` 后缀——旧版直接删，git 能找回

### 新增视频 checklist

1. 在 `D:\workspace\_output\猫波信号站\视频\` 下建 `YYYYMMDD_slug/` + 子目录 `成片/` `_runtime/素材/` `_runtime/字幕/` `_runtime/frames/`
2. yt-dlp 下载原视频到 `_runtime/素材/source.mp4`，ffmpeg 提取音频到 `_runtime/素材/audio.wav`
3. whisper ASR → `_runtime/字幕/01_raw.srt` → 断句 → 翻译 → 字符限制 → ASS，中间产物逐一写入 `_runtime/字幕/`（01_raw.srt ~ 05.ass）按 pipeline.py 步骤跑
4. `_runtime/字幕/transcript.txt` 提取（从 03_zh.srt 去时间戳去序号）
5. 截图至少 5 个时间点到 `_runtime/frames/`，选主讲人正脸最清晰的一张，其余删除
6. 封面 `_tools/gen_cover.py` 生成 → `cover.jpg`
7. `发布面板.html` 全部字段填完
8. 渲染视频落 `成片/<B站标题>.mp4`

## 管线流程

### 1. 下载
```bash
yt-dlp --write-auto-subs --sub-langs en --convert-subs srt \
  -f "bestvideo[height<=1080][vcodec^=avc1]+bestaudio[ext=m4a]/..." <url>
```
H.264+AAC（B站兼容），最高 1080p。

### 2. 断句（pipeline.py §1.5）
切句子级片段（目标 ~18 英文词/句），携带词裁剪。输出 `*_seg.srt`。

### 3. 翻译（pipeline.py §2）
DeepSeek API EN→ZH 双语，并行每批 10 条。输出 `*_zh.srt`。

### 4. 中文字符限制（pipeline.py §3）
`enforce_max_chars(srt_path, max_chars=28)` — 中文超 28 字拆为两条。

### 5. ASS 生成（pipeline.py §4）
`srt_to_ass(srt_path)` — 中文 SimHei 42px 中上，英文 Segoe UI 32px 中下。

### 6. 渲染（pipeline.py §5）
```bash
ffmpeg -i video.mp4 -vf "ass=subs.ass" -c:v libx264 -crf 20 -c:a copy output.mp4
```

### 7. B站元数据
- **标题**：≤80 字。从 transcript 提取最独特/反直觉的论断。不啰嗦，不堆砌关键词
- **标签**：≤10 个，每个 ≤12 字
- **简介**：≤2000 字。核心论点 + 嘉宾 + 出处
- **合集**：猫波译站
- **分区**：知识 > 科技 > 人工智能

### 8. 封面（_tools/gen_cover.py）
- 底图：视频截图，亮度 0.80（黑色透明度 80%），微微压暗
- 字体：SimHei（系统最粗中文），四周 2px 填充模拟超粗
- 主色：暖黄 #FFC82D，辅色：暖白 #FCFAF5
- 布局：全部居中，最多 3 行 + 1 条装饰线 + 底部信息条
- 不加频道水印

### 9. 专栏文章
从翻译 transcript 提取：引言 → 核心论点分节 → 结尾。B站专栏 markdown。

## B站 频道资产

| 项目 | 值 |
|------|-----|
| 昵称 | 猫波信号站 |
| UID | `bili51931896575` |
| 签名 | 猫波雷达滴滴响——又有好信号来了！ |
| 合集 | 猫波译站 |
| 头像 | avatar_catwave_v3.png（1024×1024，浅暖白底，脉冲雷达图形） |

## 踩坑日志

**位置**：`_ref/pitfalls.md`（唯一真相源）。本文件「已知坑」为摘要索引，完整诊断/根因/修复/预防见该文件。

### 写入标准

踩坑后必须写入 `_ref/pitfalls.md`，格式参照 `~/.agentboard/tips/`：

```markdown
## N. 一句话标题（洞察，不是主题）
type: diagnosis | method | fact
date: YYYY-MM-DD
source: 触发写入的事件/任务简述

### 现象
### 根因
### 修复
### 预防
```

**准入五问**（全过才写）：可复用？非显然？学习成本高（>30min 定位）？跨会话有价值？可操作？

### 已知坑索引

| # | 坑 | 位置 |
|---|-----|------|
| 1 | 全角冒号 U+FF1A → Windows 文件名编码错误 | pitfalls.md #1 |
| 2 | yt-dlp 默认拿 webm/vp9 → B站不兼容 | pitfalls.md #2 |
| 3 | "透明度 80%" = 亮度 0.80，不是 0.20 | pitfalls.md #3 |
| 4 | ASS 双 Dialogue 被 libass 碰撞检测吞掉 | pitfalls.md #4 |
| 5 | Windows PIL 中文字体只有 SimHei 够粗 | pitfalls.md #5 |
| 6 | DeepSeek 批量翻译行数对齐和并行稳定性 | pitfalls.md #6 |
| 7 | enforce_max_chars 无标点长文本永不拆分 | pitfalls.md #7 |
| 8 | B站 API 直接调用返回 HTML 错误页 | pitfalls.md #8 |
| 9 | B站章节上限 10 段 + 格式必须 HH:MM:SS | pitfalls.md #9 |
| 10 | B站标签只能逐个输入，不能批量粘贴 | pitfalls.md #10 |
| 11 | B站封面首页推荐 4:3 裁剪 | pitfalls.md #11 |
