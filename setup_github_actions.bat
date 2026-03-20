@echo off
chcp 65001 >nul
cls
echo ========================================
echo GitHub Actions 自动打包助手
echo ========================================
echo.
echo 这个脚本会帮你准备 Git 仓库
echo.
echo 前提条件：
echo 1. 已安装 Git（如果没有，请先安装）
echo    下载地址：https://git-scm.com/download/win
echo 2. 有 GitHub 账号
echo ========================================
echo.
pause

REM 检查 git 是否安装
where git >nul 2>nul
if errorlevel 1 (
    echo.
    echo [错误] 未检测到 Git！
    echo.
    echo 请先安装 Git:
    echo 1. 访问：https://git-scm.com/download/win
    echo 2. 下载并安装 Windows 版 Git
    echo 3. 安装完成后重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo.
echo [1/4] Git 已安装，继续...
git --version
echo.

REM 检查是否已有 git 仓库
if exist .git (
    echo [2/4] Git 仓库已存在
) else (
    echo [2/4] 初始化 Git 仓库...
    git init
)
echo.

REM 添加文件
echo [3/4] 添加文件到 Git...
git add .
echo.

REM 提交
echo [4/4] 提交文件...
git commit -m "Initial commit"
if errorlevel 1 (
    echo [提示] 没有需要提交的文件
)
echo.

echo ========================================
echo 准备完成！
echo ========================================
echo.
echo 接下来请手动执行以下步骤：
echo.
echo 步骤 1: 在 GitHub 创建仓库
echo   1. 访问：https://github.com/new
echo   2. 仓库名：class-schedule-app
echo   3. 选择 Public
echo   4. 点击 Create repository
echo.
echo 步骤 2: 复制仓库地址
echo   格式：https://github.com/你的用户名/仓库名.git
echo.
echo 步骤 3: 在命令行中运行（替换为你的地址）
echo.
echo   git remote add origin https://github.com/你的用户名/仓库名.git
echo   git branch -M main
echo   git push -u origin main
echo.
echo ========================================
echo.
echo 提示：
echo - 配置文件已在 .github/workflows/android.yml
echo - 推送到 GitHub 后会自动触发构建
echo.
pause
