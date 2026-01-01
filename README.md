# YouTube视频下载器

一个简单易用的YouTube视频下载工具，使用Python和yt-dlp实现。

## 🌐 Web应用版本（推荐）

**现在支持网页界面！** 无需命令行，通过浏览器即可使用。

👉 [查看Web应用使用说明](WEB_APP_README.md)

**快速启动:**
```bash
# Windows
start_server.bat

# macOS/Linux  
./start_server.sh

# 或直接运行
python app.py
```

然后访问: http://localhost:5000

---

## 💻 命令行版本

## 安装

1. 确保已安装Python 3.7或更高版本

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. **（推荐）安装ffmpeg** - 用于修复视频播放问题：
   - **Windows**: 
     - 使用winget: `winget install ffmpeg`
     - 或从 https://ffmpeg.org/download.html 下载，解压后将bin目录添加到系统PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) 或 `sudo yum install ffmpeg` (CentOS/RHEL)

   > **注意**: 如果下载的视频无法播放（显示"MPEG-TS in MP4 container"警告），需要安装ffmpeg来修复。

## 使用方法

### 基本用法

```bash
python download_youtube.py <视频链接>
```

### 指定输出目录

```bash
python download_youtube.py <视频链接> --output my_videos
```

### 指定视频质量

```bash
python download_youtube.py <视频链接> --quality 720p
```

可用的质量选项：
- `best` - 最佳质量（默认）
- `1080p` - 1080p质量
- `720p` - 720p质量
- `worst` - 最低质量

## 示例

```bash
# 下载视频到默认的downloads文件夹
python download_youtube.py https://www.youtube.com/watch?v=MdxYAGwaysQ

# 下载到指定文件夹
python download_youtube.py https://www.youtube.com/watch?v=MdxYAGwaysQ --output my_videos

# 下载720p质量
python download_youtube.py https://www.youtube.com/watch?v=MdxYAGwaysQ --quality 720p
```

## 功能特点

- ✅ 自动下载最佳质量的视频和音频并合并
- ✅ 支持自定义输出目录
- ✅ 支持选择视频质量
- ✅ 显示下载进度和视频信息
- ✅ 自动处理视频标题作为文件名

## 修复无法播放的视频

如果下载的视频无法播放（出现"MPEG-TS in MP4 container"警告），可以使用修复工具：

```bash
# 修复downloads目录中的所有视频
python fix_videos.py

# 修复指定视频文件
python fix_videos.py video.mp4

# 修复后替换原文件（不保留原文件）
python fix_videos.py --replace
```

**注意**: 修复功能需要安装ffmpeg（见上方安装说明）

## 故障排除

### 视频无法播放
- **问题**: 下载的视频文件无法在播放器中打开
- **原因**: 视频可能是MPEG-TS格式被错误封装在MP4容器中
- **解决**: 
  1. 安装ffmpeg（见上方安装说明）
  2. 运行 `python fix_videos.py` 修复视频

### 下载失败
- 检查网络连接
- 确认视频链接有效
- 某些视频可能因版权限制无法下载

## 注意事项

- 下载的视频仅供个人学习使用，请遵守YouTube的使用条款
- 某些视频可能因版权限制无法下载
- 下载速度取决于网络连接

