# HANDOFF · YouTube Content Pipeline

> 打开新会话时读此文件，了解当前状态和下一步。

## 当前状态

项目已从纯规范文档落地为可运行代码。上一次会话的核心产出：

- `pipeline.py` — 完整 CLI，6 步管线（下载→断句→翻译→字数控制→ASS→渲染），已通过单元测试
- `_tools/gen_cover.py` — PIL 封面生成器，SimHei 暖黄主题，命令行独立运行
- `_ref/pitfalls.md` — 8 条详细踩坑记录
- `SKILL.md` — Claude Code 技能定义（`~/.claude/skills/youtube-content-pipeline/`）
- GitHub: https://github.com/wampeeHuang/youtube-content-pipeline
- GitHub: https://github.com/wampeeHuang/screenshot-vision

已处理的视频：Boris Cherny Sequoia AI Ascent 2026（上次会话完成，产物不在此工作区）

## 已做

- [x] 管线 6 步全部实现并可独立运行
- [x] SRT 解析/序列化（零依赖）
- [x] DeepSeek API 批量翻译（并行 5 并发，行数对齐，3 次重试）
- [x] 中文字数控制（≤28 字，标点拆分 + 无标点硬切 fallback）
- [x] ASS 双语字幕生成（单事件 \N 模式，SimHei + Segoe UI）
- [x] FFmpeg 渲染
- [x] 封面生成脚本（独立 CLI）
- [x] 项目规范文档（CLAUDE.md）
- [x] 踩坑日志（`_ref/pitfalls.md` + 工具架 `tips/windows-gbk-python-io.md`）
- [x] GitHub 仓库创建并推送

## 未做 / 下一步

### 高优先级：补全封面生成能力

当前 `_tools/gen_cover.py` **可以独立运行**（`python _tools/gen_cover.py <frame> <output> --title "..." --sub "..."`），但有两处缺口：

1. **未集成到 pipeline.py 主流程**：`pipeline.py all` 跑完后不自动生成封面，需要手动调用 gen_cover.py
2. **封面文字需人工提供**：gen_cover.py 需要 `--title` 和 `--sub` 参数。缺少"从 transcript 自动提取封面标题"的能力

建议做法：
- pipeline.py 增加 `--cover-title` 和 `--cover-sub` 参数（可选）
- 如果提供了封面文字，渲染完成后自动调用 gen_cover.py
- 如果没提供，提示用户手动生成

### 转译新视频

1. 获取 YouTube URL
2. `python pipeline.py all <url> --slug <name>`
3. 截图 5+ 张到 `frames/`，选正脸最清晰的保留
4. `python _tools/gen_cover.py frames/best_frame.jpg output/cover.jpg --title "..." --sub "..."`
5. 填写 `output/B站上传信息.txt` 和 `output/B站专栏文章.md`
6. 清理原始 mp4

### 待扩展（不改代码，先记着）

- 掐头去尾自动化（检测低密度段）
- 术语表/上下文翻译
- 多 API 翻译后端切换
- 字幕全局时间偏移修正

## 项目结构

```
D:\Claude code_workspace\2026-06-16-youtube-content-pipeline\
  pipeline.py          ← 核心 CLI，唯一真相源
  SKILL.md             ← Claude Code 技能定义（副本，原件在 ~/.claude/skills/）
  CLAUDE.md            ← 项目规范
  HANDOFF.md           ← 本文件
  _tools/
    gen_cover.py       ← 封面生成
  _ref/
    pitfalls.md        ← 踩坑日志
  _runtime/            ← 运行时产出（按视频分子文件夹）
    <video_slug>/
      _process/        ← 管线中间产物（01_raw.srt ~ 05.ass + transcript.txt）
      frames/          ← 截图
      output/          ← 最终交付物（mp4 + cover.jpg + B站上传信息.txt + B站专栏文章.md）
```

## 关键约束

- 文件名禁止全角冒号 U+FF1A
- Python 文件 I/O 必须显式 `encoding='utf-8'`
- yt-dlp 必须指定 H.264+AAC
- ASS 用单事件 `\N` 双语，不用双 Dialogue
- 封面亮度 0.80，SimHei 字体，#FFC82D 暖黄，无频道水印
- 视频文件名 = B站标题（B站自动识别）
- 完整已知坑清单见 `_ref/pitfalls.md`
