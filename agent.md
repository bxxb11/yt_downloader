# YouTube视频下载工具 - 操作手册

## 📋 目录

1. [功能概述](#功能概述)
2. [环境要求](#环境要求)
3. [安装步骤](#安装步骤)
4. [使用方法](#使用方法)
5. [常见问题解决](#常见问题解决)
6. [故障排除](#故障排除)
7. [最佳实践](#最佳实践)

---

## 功能概述

这是一个基于Python和yt-dlp的YouTube视频下载工具，支持：

- ✅ 下载YouTube视频到本地
- ✅ 支持自定义输出目录
- ✅ 支持选择视频质量（best/720p/1080p/worst）
- ✅ 自动处理视频标题作为文件名
- ✅ 显示下载进度和视频信息
- ✅ Plan B方案：无需ffmpeg也能处理大部分视频

---

## 环境要求

- **Python**: 3.7 或更高版本
- **操作系统**: Windows / macOS / Linux
- **网络**: 需要能够访问YouTube

---

## 安装步骤

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. （可选）安装ffmpeg

如果需要修复视频播放问题，建议安装ffmpeg：

**Windows:**
```bash
winget install ffmpeg
```
或从 https://ffmpeg.org/download.html 下载并添加到PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
```

---

## 使用方法

### 基本下载

```bash
python download_youtube.py "视频链接"
```

**示例:**
```bash
python download_youtube.py "https://www.youtube.com/watch?v=MdxYAGwaysQ"
```

### 指定输出目录

```bash
python download_youtube.py "视频链接" --output my_videos
```

### 指定视频质量

```bash
python download_youtube.py "视频链接" --quality 720p
```

**可用质量选项:**
- `best` - 最佳质量（默认）
- `1080p` - 1080p质量
- `720p` - 720p质量
- `worst` - 最低质量

### 完整示例

```bash
# 下载到默认的downloads文件夹
python download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 下载到指定文件夹
python download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID" --output my_videos

# 下载720p质量
python download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID" --quality 720p

# 下载1080p质量到指定文件夹
python download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID" --output hd_videos --quality 1080p
```

---

## 常见问题解决

### 问题1: 视频无法播放

**症状**: 下载的视频文件无法在播放器中打开，出现"MPEG-TS in MP4 container"警告

**解决方案（按优先级）:**

#### 方案A: 使用VLC播放器（推荐，最简单）

1. 下载VLC播放器: https://www.videolan.org/vlc/
2. 用VLC打开无法播放的视频文件
3. VLC通常能处理MPEG-TS格式的视频

#### 方案B: 重新下载（使用Plan B脚本）

```bash
python redownload_fixed.py "视频链接"
```

这个脚本会：
- 完全排除HLS流格式
- 只选择兼容的mp4/webm格式
- 下载的文件会添加 `_fixed` 后缀

#### 方案C: 使用ffmpeg修复（需要安装ffmpeg）

```bash
# 修复downloads目录中的所有视频
python fix_videos.py

# 修复指定视频文件
python fix_videos.py video.mp4

# 修复后替换原文件
python fix_videos.py --replace
```

### 问题2: 下载失败

**可能原因和解决方案:**

1. **网络连接问题**
   - 检查网络连接
   - 确认能够访问YouTube
   - 如果使用VPN，尝试切换节点

2. **视频链接无效**
   - 确认视频链接正确
   - 确认视频未被删除或设为私有

3. **版权限制**
   - 某些视频可能因版权限制无法下载
   - 尝试下载其他视频测试

4. **格式选择失败**
   - 尝试使用不同的质量选项（720p/1080p）
   - 使用Plan B脚本重新下载

### 问题3: 下载速度慢

**优化建议:**

1. 检查网络连接速度
2. 尝试使用较低质量（720p）下载
3. 避免同时下载多个视频

---

## 故障排除

### 错误: "ffmpeg未找到"

**说明**: 修复功能需要ffmpeg，但下载功能不需要

**解决**: 
- 如果只是下载视频，可以忽略此错误
- 如果需要修复视频，请安装ffmpeg（见安装步骤）

### 错误: "No supported JavaScript runtime"

**说明**: YouTube提取可能需要JavaScript运行时，但不影响基本下载

**解决**: 
- 可以忽略此警告
- 如需完整功能，可安装deno: https://deno.land/

### 错误: "Connection failed"

**说明**: 网络连接问题

**解决**:
1. 检查网络连接
2. 检查VPN设置（如使用）
3. 等待后重试
4. 使用Plan B脚本（`redownload_fixed.py`）

### 错误: "Video unavailable"

**说明**: 视频不可用

**解决**:
- 确认视频链接正确
- 确认视频未被删除或设为私有
- 确认视频在您所在地区可访问

---

## 最佳实践

### 1. 下载前检查

- 确认视频链接有效
- 确认网络连接正常
- 确认有足够的磁盘空间

### 2. 质量选择建议

- **best**: 适合保存重要视频，文件较大
- **1080p**: 适合高清观看，平衡质量和文件大小
- **720p**: 适合一般观看，文件较小
- **worst**: 适合快速预览，文件最小

### 3. 文件管理

- 使用 `--output` 参数指定输出目录，便于管理
- 定期清理不需要的视频文件
- 为不同类型的视频创建不同的文件夹

### 4. 批量下载

虽然脚本不支持批量下载，但可以：

1. 创建批处理脚本（Windows）:
```bash
@echo off
python download_youtube.py "链接1"
python download_youtube.py "链接2"
python download_youtube.py "链接3"
```

2. 或使用Shell脚本（macOS/Linux）:
```bash
#!/bin/bash
python download_youtube.py "链接1"
python download_youtube.py "链接2"
python download_youtube.py "链接3"
```

### 5. 视频播放建议

- **首选**: VLC播放器（兼容性最好）
- **备选**: Windows Media Player, QuickTime, 其他播放器
- 如果视频无法播放，优先使用VLC

### 6. 性能优化

- 使用SSD存储下载的视频（更快）
- 避免同时运行多个下载任务
- 定期更新yt-dlp: `pip install --upgrade yt-dlp`

---

## 脚本文件说明

### 主要脚本

- **`download_youtube.py`** - 主下载脚本，支持自定义质量和输出目录
- **`redownload_fixed.py`** - Plan B重新下载脚本，避免MPEG-TS问题
- **`fix_videos.py`** - 视频修复脚本（需要ffmpeg）

### 配置文件

- **`requirements.txt`** - Python依赖列表
- **`README.md`** - 项目说明文档
- **`PLAN_B_README.md`** - Plan B方案详细说明
- **`agent.md`** - 本操作手册

---

## 快速参考

### 常用命令

```bash
# 基本下载
python download_youtube.py "视频链接"

# 下载到指定目录
python download_youtube.py "视频链接" --output my_videos

# 下载720p质量
python download_youtube.py "视频链接" --quality 720p

# Plan B重新下载（避免播放问题）
python redownload_fixed.py "视频链接"

# 修复视频（需要ffmpeg）
python fix_videos.py
```

### 输出位置

- 默认输出目录: `downloads/`
- 文件命名: `视频标题.扩展名`
- Plan B文件: `视频标题_fixed.扩展名`

---

## 技术支持

### 常见问题

1. **Q: 为什么下载的视频无法播放？**
   - A: 可能是MPEG-TS格式问题，使用VLC播放器或Plan B脚本重新下载

2. **Q: 必须安装ffmpeg吗？**
   - A: 不是必须的。下载功能不需要ffmpeg，只有修复功能需要

3. **Q: 可以下载播放列表吗？**
   - A: 当前版本只支持单个视频下载，播放列表功能未实现

4. **Q: 下载速度很慢怎么办？**
   - A: 检查网络连接，尝试使用较低质量，或检查是否有其他程序占用带宽

5. **Q: 如何批量下载？**
   - A: 可以创建批处理脚本，依次调用下载命令

### 更新和维护

- 定期更新yt-dlp: `pip install --upgrade yt-dlp`
- 检查Python版本兼容性
- 关注YouTube API变化

---

## 注意事项

⚠️ **重要提示**:

1. **版权**: 下载的视频仅供个人学习使用，请遵守YouTube的使用条款和版权法律
2. **隐私**: 不要下载和分享他人的私有视频
3. **网络**: 确保您的网络连接稳定，避免下载中断
4. **存储**: 注意磁盘空间，高清视频文件可能很大
5. **合规**: 遵守当地法律法规，不要下载受版权保护的内容用于商业用途

---

## 版本信息

- **工具版本**: 1.0
- **yt-dlp版本**: 最新稳定版
- **Python要求**: 3.7+
- **最后更新**: 2026年1月

---

## 附录

### 支持的视频格式

- MP4 (H.264)
- WebM (VP9)
- 其他yt-dlp支持的格式

### 不支持的格式

- 需要特殊权限的视频
- 受地区限制的视频（取决于网络）
- 已删除或私有的视频

### 推荐工具

- **VLC播放器**: https://www.videolan.org/vlc/ （视频播放）
- **ffmpeg**: https://ffmpeg.org/ （视频处理）

---

**祝您使用愉快！如有问题，请参考故障排除部分或查看相关文档。**

