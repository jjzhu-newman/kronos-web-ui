@echo off
REM Kronos UI - 启动脚本
REM 自动检测Python环境并启动应用

REM 设置控制台编码为UTF-8
chcp 65001 >nul 2>&1

echo ========================================
echo   Kronos Web UI v2.0
echo   AI Financial Prediction Platform
echo ========================================
echo.

REM 检查Python 3.13（CUDA版本）
set "PYTHON_CMD=D:\Program Files\Python313\python.exe"
if not exist "%PYTHON_CMD%" (
    echo Python 3.13 未找到，尝试使用默认Python...
    set "PYTHON_CMD=python"
)

"%PYTHON_CMD%" --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python！
    echo 请先安装Python 3.10或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/4] 检测到Python版本:
"%PYTHON_CMD%" --version
echo.

REM 获取项目根目录
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
cd /d "%PROJECT_ROOT%"

REM 检查并创建必要目录
if not exist "logs" mkdir logs
if not exist "cache\models" mkdir cache\models
if not exist "static\exports" mkdir static\exports

echo [2/4] 检查依赖包...
"%PYTHON_CMD%" -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 首次运行，正在安装依赖包...
    echo 这可能需要几分钟，请耐心等待...
    echo.
    "%PYTHON_CMD%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [错误] 依赖安装失败！
        echo 请检查网络连接或手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo.
) else (
    echo 依赖包已安装
)
echo.

echo [3/4] 检查配置文件...
if not exist "config\config.json" (
    echo [警告] 配置文件不存在！
    pause
    exit /b 1
)
echo 配置文件检查完成
echo.

echo [4/4] 启动Kronos Web服务器...
echo.
echo ========================================
echo 服务器将在以下地址启动:
echo   http://localhost:7070
echo ========================================
echo.
echo 浏览器将自动打开，如未打开请手动访问上述地址
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

REM 启动应用
"%PYTHON_CMD%" core\app.py

pause
