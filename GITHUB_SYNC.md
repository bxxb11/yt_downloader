# GitHub同步指南

## 📋 前置步骤

### 1. 配置Git用户信息（如果尚未配置）

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

或者仅为当前仓库配置：

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 2. 在GitHub上创建新仓库

1. 登录GitHub
2. 点击右上角的 "+" → "New repository"
3. 填写仓库信息：
   - Repository name: `yt_downloader` (或您喜欢的名称)
   - Description: `YouTube视频下载工具 - Web应用版本`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

## 🚀 同步到GitHub

### 方法1: 使用HTTPS（推荐）

```bash
# 1. 添加远程仓库（替换YOUR_USERNAME和YOUR_REPO_NAME）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 2. 查看远程仓库
git remote -v

# 3. 推送到GitHub
git branch -M main
git push -u origin main
```

### 方法2: 使用SSH

```bash
# 1. 添加远程仓库（替换YOUR_USERNAME和YOUR_REPO_NAME）
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# 2. 推送到GitHub
git branch -M main
git push -u origin main
```

## 📝 后续更新

当您修改代码后，使用以下命令同步：

```bash
# 1. 查看更改
git status

# 2. 添加更改
git add .

# 3. 提交更改
git commit -m "描述您的更改"

# 4. 推送到GitHub
git push
```

## 🔧 常用Git命令

```bash
# 查看状态
git status

# 查看提交历史
git log

# 查看远程仓库
git remote -v

# 拉取最新更改
git pull

# 创建新分支
git checkout -b feature-name

# 切换分支
git checkout main
```

## ⚠️ 注意事项

1. **不要提交敏感信息**
   - API密钥
   - 密码
   - 个人配置

2. **.gitignore已配置**
   - 已排除 `downloads/` 目录中的视频文件
   - 已排除Python缓存文件
   - 已排除IDE配置文件

3. **首次推送可能需要身份验证**
   - HTTPS: 使用Personal Access Token
   - SSH: 需要配置SSH密钥

## 🔐 GitHub身份验证

### 使用Personal Access Token (HTTPS)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 生成新token，选择 `repo` 权限
3. 推送时使用token作为密码

### 使用SSH密钥

```bash
# 1. 生成SSH密钥（如果还没有）
ssh-keygen -t ed25519 -C "your.email@example.com"

# 2. 复制公钥
cat ~/.ssh/id_ed25519.pub

# 3. 添加到GitHub: Settings → SSH and GPG keys → New SSH key
```

## 📦 项目文件说明

已包含的文件：
- ✅ 源代码文件（.py）
- ✅ 配置文件（requirements.txt）
- ✅ 文档文件（.md）
- ✅ 模板文件（templates/）
- ✅ 启动脚本

已排除的文件：
- ❌ 下载的视频文件（downloads/*.mp4等）
- ❌ Python缓存（__pycache__/）
- ❌ 虚拟环境（venv/）
- ❌ IDE配置（.vscode/等）

---

**提示**: 如果遇到问题，请查看GitHub的帮助文档或联系支持。

