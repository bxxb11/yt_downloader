# 🚀 GitHub同步 - 快速开始

## 第一步：配置Git（首次使用）

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 第二步：在GitHub创建仓库

1. 访问 https://github.com/new
2. 填写仓库名称（如：`yt_downloader`）
3. 选择 Public 或 Private
4. **不要**勾选 "Initialize with README"
5. 点击 "Create repository"

## 第三步：同步到GitHub

### 方法A: 使用同步脚本（推荐）

**Windows:**
```bash
sync_to_github.bat
```

**macOS/Linux:**
```bash
chmod +x sync_to_github.sh
./sync_to_github.sh
```

### 方法B: 手动同步

```bash
# 1. 添加远程仓库（替换YOUR_USERNAME和YOUR_REPO_NAME）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 2. 提交更改
git add .
git commit -m "Initial commit: YouTube视频下载工具"

# 3. 推送到GitHub
git branch -M main
git push -u origin main
```

## ✅ 完成！

现在您的代码已经同步到GitHub了！

访问 `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME` 查看您的仓库。

---

**详细说明**: 查看 [GITHUB_SYNC.md](GITHUB_SYNC.md)

