@echo off
chcp 65001 >nul
cls
echo ========================================
echo 推送代码到 GitHub
echo ========================================
echo.
echo 正在推送代码到：yi-gua-ji/class-schedule-app
echo.

REM 检查 git 是否安装
where git >nul 2>nul
if errorlevel 1 (
    echo [错误] 未安装 Git！
    echo 请先安装：https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Git 已安装
git --version
echo.

echo [2/5] 初始化仓库...
if not exist .git (
    git init
) else (
    echo 仓库已存在
)
echo.

echo [3/5] 添加文件...
git add .
echo.

echo [4/5] 提交文件...
git commit -m "Initial commit"
echo.

echo [5/5] 推送到 GitHub...
echo.
echo 请运行以下命令（需要你的 GitHub 账号密码）：
echo.
echo git remote add origin https://github.com/yi-gua-ji/class-schedule-app.git
echo git branch -M main
echo git push -u origin main
echo.
echo ========================================
echo 或者手动运行上面的命令
echo ========================================
pause
