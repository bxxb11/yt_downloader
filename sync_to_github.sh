#!/bin/bash
echo "========================================"
echo "GitHub同步脚本"
echo "========================================"
echo ""

# 检查git配置
if ! git config user.name > /dev/null 2>&1; then
    echo "[警告] 未配置Git用户信息"
    echo ""
    echo "请先运行以下命令配置Git:"
    echo "  git config --global user.name \"Your Name\""
    echo "  git config --global user.email \"your.email@example.com\""
    echo ""
    exit 1
fi

echo "[1/4] 检查Git状态..."
git status --short
echo ""

echo "[2/4] 添加所有更改..."
git add .
echo ""

echo "[3/4] 提交更改..."
read -p "请输入提交信息 (直接回车使用默认): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update: YouTube视频下载工具"
fi
git commit -m "$commit_msg"
echo ""

echo "[4/4] 检查远程仓库..."
if ! git remote -v > /dev/null 2>&1; then
    echo "[提示] 尚未配置远程仓库"
    echo ""
    echo "请先运行以下命令添加远程仓库:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
    echo ""
    echo "然后运行此脚本再次同步"
    exit 1
fi

echo ""
echo "准备推送到GitHub..."
echo "分支: $(git branch --show-current)"
echo ""
read -p "确认推送到GitHub? (Y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

git push -u origin main
echo ""
echo "========================================"
if [ $? -eq 0 ]; then
    echo "[成功] 已成功同步到GitHub!"
else
    echo "[错误] 推送失败，请检查:"
    echo "  1. 远程仓库地址是否正确"
    echo "  2. 是否有推送权限"
    echo "  3. 网络连接是否正常"
fi
echo "========================================"

