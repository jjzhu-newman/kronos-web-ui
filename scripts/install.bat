@echo off
REM Kronos UI - 环境安装脚本
REM 一键安装所有Python依赖

echo ========================================
echo   Kronos UI - 环境安装
echo ========================================
echo.

echo [1/2] 检查Python环境...
python --version
if errorlevel 1 (
    echo.
    echo [错误] Python未安装或不在PATH中！
    echo 请先安装Python 3.10+
    echo 下载: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo Python环境检查通过
echo.

echo [2/2] 安装Python依赖包...
echo 这可能需要几分钟，请耐心等待...
echo.

REM 升级pip
python -m pip install --upgrade pip

REM 安装项目依赖
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败！
    echo 请检查网络连接后重试
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 现在可以运行 scripts\start.bat 启动应用
echo.
pause
