@echo off
echo ========================================
echo 课表应用 APK 打包工具
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [1/5] 检查 Python 安装... 完成
echo.

REM 创建虚拟环境
echo [2/5] 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo [错误] 创建虚拟环境失败
    pause
    exit /b 1
)

echo [3/5] 安装打包依赖...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install buildozer

echo.
echo ========================================
echo 重要提示！
echo ========================================
echo.
echo Buildozer 需要在 Linux 环境下运行。你有以下选择：
echo.
echo 选项 1: 使用 WSL2 (推荐)
echo   1. 以管理员身份打开 PowerShell
echo   2. 运行：wsl --install -d Ubuntu
echo   3. 重启电脑
echo   4. 在 Ubuntu 中运行此脚本
echo.
echo 选项 2: 使用 Google Colab 云端打包
echo   访问：https://colab.research.google.com/
echo   参考 BUILD_APK_GUIDE.md 中的详细说明
echo.
echo 选项 3: 使用 Docker
echo   1. 安装 Docker Desktop
echo   2. 运行：docker run --rm -v %cd%:/home/user/hostcwd kivy/buildozer android debug
echo.
echo ========================================
echo.

pause
