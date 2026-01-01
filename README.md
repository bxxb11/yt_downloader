# YouTube视频下载器

一个简单易用的YouTube视频下载工具，使用Python和yt-dlp实现。

**本地网页应用** - 在您的电脑上运行，通过浏览器访问和下载视频。

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/bxxb11/yt_downloader.git
cd yt_downloader
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动应用

```bash
# Windows
start_server.bat

# macOS/Linux
chmod +x start_server.sh
./start_server.sh

# 或直接运行
python app.py
```

### 4. 打开浏览器

访问: **http://localhost:5000**

## ✨ 功能特点

- ✅ **网页界面** - 美观的Apple风格界面，无需命令行
- ✅ **实时进度** - 显示下载进度、速度和剩余时间
- ✅ **视频预览** - 下载前查看视频信息、缩略图
- ✅ **文件管理** - 查看、下载、删除已下载的文件
- ✅ **多质量选择** - 支持best/1080p/720p/worst
- ✅ **自定义目录** - 可以指定下载到任意目录
- ✅ **完全本地化** - 所有数据存储在本地，不会上传到云端

## 🌐 Web应用版本（推荐）

**本地网页界面！** 无需命令行，通过浏览器即可使用。

👉 [查看Web应用使用说明](WEB_APP_README.md)

**快速启动:**
```bash
# Windows
start_server.bat

# macOS/Linux  
chmod +x start_server.sh
./start_server.sh

# 或直接运行
python app.py
```

然后访问: **http://localhost:5000**

**注意**: 这是本地应用，只在您的电脑上运行，不会部署到云端。

---

## 💻 命令行版本

## 📦 安装

### 快速安装

```bash
# 1. 克隆仓库
git clone https://github.com/bxxb11/yt_downloader.git
cd yt_downloader

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动应用
python app.py

# 4. 打开浏览器访问 http://localhost:5000
```

**详细安装说明**: 查看 [INSTALL.md](INSTALL.md)

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

