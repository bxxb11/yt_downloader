# 🚀 快速启动指南

## Web应用版本（推荐）

### 1️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

### 2️⃣ 启动服务器

**Windows:**
```bash
start_server.bat
```

**macOS/Linux:**
```bash
chmod +x start_server.sh
./start_server.sh
```

**或直接运行:**
```bash
python app.py
```

### 3️⃣ 打开浏览器
访问: **http://localhost:5000**

---

## 命令行版本

### 基本下载
```bash
python download_youtube.py "视频链接"
```

### 指定质量
```bash
python download_youtube.py "视频链接" --quality 720p
```

---

## 📁 项目结构

```
yt_downloader/
├── app.py                 # Web应用主程序
├── download_youtube.py    # 命令行下载脚本
├── redownload_fixed.py    # Plan B重新下载脚本
├── fix_videos.py          # 视频修复脚本
├── templates/
│   └── index.html         # Web界面
├── static/                # 静态文件目录
├── downloads/             # 下载文件目录
├── requirements.txt       # Python依赖
├── README.md              # 项目说明
├── WEB_APP_README.md      # Web应用说明
├── agent.md               # 操作手册
└── QUICK_START.md         # 本文件
```

---

## 💡 使用建议

1. **首次使用**: 推荐使用Web应用版本，界面更友好
2. **批量下载**: 使用命令行版本，可以编写脚本批量处理
3. **视频播放**: 如果视频无法播放，使用VLC播放器
4. **网络问题**: 如果下载失败，检查网络连接或使用VPN

---

## 🆘 需要帮助？

- 查看 [agent.md](agent.md) - 详细操作手册
- 查看 [WEB_APP_README.md](WEB_APP_README.md) - Web应用说明
- 查看 [README.md](README.md) - 项目总览

