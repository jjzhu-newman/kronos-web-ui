@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   安装 CUDA 版 PyTorch
echo ========================================
echo.

echo [1/4] 检查 Python 版本...
for /f "tokens=*" %%i in ('python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"') do set PYTHON_VERSION=%%i
echo 当前 Python 版本: %PYTHON_VERSION%

python -c "import sys; exit(0 if sys.version_info >= (3, 14) else 1)"
if errorlevel 1 (
    echo ✓ Python 版本支持 CUDA
) else (
    echo.
    echo ========================================
    echo   ⚠️  警告：Python 3.14 不支持 CUDA
    echo ========================================
    echo.
    echo 您的 Python 版本是 3.14 或更高，PyTorch 尚未发布
    echo Python 3.14 的 CUDA 版本。
    echo.
    echo 解决方案：
    echo   1. 安装 Python 3.13（推荐）
    echo      下载地址：https://www.python.org/downloads/
    echo.
    echo   2. 或继续使用当前 CPU 版本（速度较慢）
    echo.
    echo 详细说明请查看：docs\CUDA_GUIDE.md
    echo.
    pause
    exit /b 1
)

echo.
echo [2/4] 检查当前 PyTorch...
python -c "import torch; print('当前PyTorch:', torch.__version__)" 2>nul
if errorlevel 1 (
    echo 当前未安装PyTorch
) else (
    echo 检测到PyTorch，将先卸载
)

echo.
echo [3/4] 安装CUDA版本PyTorch...
echo 这需要下载约2-3GB，请耐心等待...
echo.

pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

echo.
echo [4/4] 验证安装...
python -c "import torch; print('PyTorch版本:', torch.__version__); print('CUDA可用:', torch.cuda.is_available())"

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 请重启 Kronos UI 应用，然后选择CUDA设备
echo.
pause
