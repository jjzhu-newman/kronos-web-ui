@echo off
REM Kronos Web UI - 一键安装脚本
REM 在新电脑上首次运行此脚本

chcp 65001 >nul 2>&1

echo ========================================
echo   Kronos Web UI - 一键安装
echo ========================================
echo.

REM 检查 Python
echo [1/5] 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [错误] 未找到 Python！
    echo.
    echo 请先安装 Python 3.10-3.13：
    echo https://www.python.org/downloads/
    echo.
    echo 安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo Python 版本: %PYTHON_VER%
echo.

REM 检查 Python 版本
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
    echo [警告] Python 版本过低，需要 3.10 或更高
    echo 请安装 Python 3.10-3.13
    echo.
    pause
    exit /b 1
)

REM 检查 pip
echo [2/5] 检查 pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [错误] pip 未安装！
    echo.
    pause
    exit /b 1
)

python -m pip --version
echo.

REM 升级 pip
echo [3/5] 升级 pip...
echo 这可能需要几分钟...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [警告] pip 升级失败，继续使用当前版本
)
echo.

REM 安装依赖
echo [4/5] 安装依赖包...
echo 这需要下载约 500MB-1GB，请耐心等待...
echo.

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败！
    echo.
    echo 可能的原因：
    echo 1. 网络连接问题
    echo 2. pip 源访问受限
    echo.
    echo 解决方法：
    echo 使用国内镜像源安装：
    echo   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] 验证安装...
python -c "import flask; import torch; import pandas; print('核心依赖安装成功！')"
if errorlevel 1 (
    echo.
    echo [警告] 部分依赖验证失败
    echo 但这可能不影响使用
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 现在可以运行启动脚本了：
echo.
echo   Windows: scripts\start.bat
echo   Linux/Mac: bash scripts/start.sh
echo.
echo 或者直接运行：
echo.
echo   python core\app.py
echo.
echo ========================================
echo.
echo 按任意键退出...
pause >nul
