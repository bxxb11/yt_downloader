@echo off
chcp 65001 >nul
echo ========================================
echo GitHub同步脚本
echo ========================================
echo.

REM 检查git配置
git config user.name >nul 2>&1
if errorlevel 1 (
    echo [警告] 未配置Git用户信息
    echo.
    echo 请先运行以下命令配置Git:
    echo   git config --global user.name "Your Name"
    echo   git config --global user.email "your.email@example.com"
    echo.
    pause
    exit /b 1
)

echo [1/4] 检查Git状态...
git status --short
echo.

echo [2/4] 添加所有更改...
git add .
echo.

echo [3/4] 提交更改...
set /p commit_msg="请输入提交信息 (直接回车使用默认): "
if "%commit_msg%"=="" set commit_msg=Update: YouTube视频下载工具
git commit -m "%commit_msg%"
echo.

echo [4/4] 检查远程仓库...
git remote -v >nul 2>&1
if errorlevel 1 (
    echo [提示] 尚未配置远程仓库
    echo.
    echo 请先运行以下命令添加远程仓库:
    echo   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    echo.
    echo 然后运行此脚本再次同步
    pause
    exit /b 1
)

echo.
echo 准备推送到GitHub...
echo 分支: main
git branch --show-current
echo.
set /p confirm="确认推送到GitHub? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo 已取消
    pause
    exit /b 0
)

git push -u origin main
echo.
echo ========================================
if errorlevel 1 (
    echo [错误] 推送失败，请检查:
    echo   1. 远程仓库地址是否正确
    echo   2. 是否有推送权限
    echo   3. 网络连接是否正常
) else (
    echo [成功] 已成功同步到GitHub!
)
echo ========================================
pause

