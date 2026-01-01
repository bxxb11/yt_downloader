# 安装和使用指南

## 📋 系统要求

- Python 3.7 或更高版本
- 网络连接（用于访问YouTube）
- 足够的磁盘空间（用于存储下载的视频）

## 🔧 安装步骤

### Windows

1. **安装Python**
   - 从 https://www.python.org/downloads/ 下载并安装Python
   - 安装时勾选 "Add Python to PATH"

2. **克隆仓库**
   ```bash
   git clone https://github.com/bxxb11/yt_downloader.git
   cd yt_downloader
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **启动应用**
   ```bash
   start_server.bat
   ```
   或
   ```bash
   python app.py
   ```

5. **打开浏览器**
   - 访问: http://localhost:5000

### macOS

1. **安装Python**
   ```bash
   # 使用Homebrew
   brew install python3
   
   # 或从官网下载
   # https://www.python.org/downloads/
   ```

2. **克隆仓库**
   ```bash
   git clone https://github.com/bxxb11/yt_downloader.git
   cd yt_downloader
   ```

3. **安装依赖**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **启动应用**
   ```bash
   chmod +x start_server.sh
   ./start_server.sh
   ```
   或
   ```bash
   python3 app.py
   ```

5. **打开浏览器**
   - 访问: http://localhost:5000

### Linux

1. **安装Python**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip
   
   # CentOS/RHEL
   sudo yum install python3 python3-pip
   ```

2. **克隆仓库**
   ```bash
   git clone https://github.com/bxxb11/yt_downloader.git
   cd yt_downloader
   ```

3. **安装依赖**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **启动应用**
   ```bash
   chmod +x start_server.sh
   ./start_server.sh
   ```
   或
   ```bash
   python3 app.py
   ```

5. **打开浏览器**
   - 访问: http://localhost:5000

## 🎯 使用方法

### 基本使用

1. **启动服务器**
   - 运行 `python app.py` 或使用启动脚本
   - 保持终端窗口打开

2. **打开网页**
   - 在浏览器中访问 http://localhost:5000

3. **下载视频**
   - 粘贴YouTube视频链接
   - 选择视频质量
   - （可选）设置自定义下载目录
   - 点击"获取视频信息"
   - 点击"开始下载"
   - 查看下载进度

### 自定义下载目录

- 在"下载目录"输入框中输入路径
- **Windows**: `D:\Videos` 或 `C:\Users\YourName\Downloads`
- **macOS/Linux**: `/home/user/videos` 或 `~/Downloads`
- **留空**: 使用默认的 `downloads/` 目录

## 📁 文件位置

- **默认下载目录**: 项目目录下的 `downloads/` 文件夹
- **自定义目录**: 您指定的任意目录

## ❓ 常见问题

### Q: 无法访问 http://localhost:5000

**A**: 检查：
1. 服务器是否正在运行（查看终端窗口）
2. 端口5000是否被其他程序占用
3. 防火墙是否阻止了连接

### Q: 安装依赖失败

**A**: 尝试：
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像（如果网络慢）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 视频无法播放

**A**: 
1. 使用VLC播放器打开视频（推荐）
2. 或使用Plan B脚本重新下载：`python redownload_fixed.py "视频链接"`

### Q: 下载速度慢

**A**: 
1. 检查网络连接
2. 尝试使用较低质量（720p）
3. 检查是否有其他程序占用带宽

## 🔒 隐私和安全

- ✅ 所有操作在本地完成
- ✅ 视频文件存储在本地
- ✅ 不会上传任何数据到云端
- ✅ 完全私密，只有您能访问

## 📚 更多文档

- [Web应用使用说明](WEB_APP_README.md)
- [自定义下载目录](CUSTOM_DOWNLOAD_DIR.md)
- [本地使用指南](LOCAL_USAGE.md)
- [操作手册](agent.md)
- [快速开始](QUICK_START.md)

## 🆘 需要帮助？

- 查看 [操作手册](agent.md) 了解详细功能
- 查看 [常见问题](README.md#故障排除)
- 提交 Issue: https://github.com/bxxb11/yt_downloader/issues

---

**享受下载视频的乐趣！** 🎬

