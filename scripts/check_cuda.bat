@echo off
REM Kronos UI - CUDA 环境检测脚本

echo ========================================
echo   CUDA 环境检测
echo ========================================
echo.

echo [检查 1] NVIDIA 驱动
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo [结果] 未检测到 NVIDIA 驱动或 nvidia-smi 工具
    echo.
    echo 请先安装 NVIDIA 显卡驱动:
    echo https://www.nvidia.com/Download/index.aspx
    echo.
) else (
    echo [结果] NVIDIA 驱动已安装
    echo.
    echo 显卡信息:
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
    echo.
)

echo [检查 2] PyTorch 版本
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}')" 2>nul
if errorlevel 1 (
    echo [结果] PyTorch 未安装
) else (
    echo [结果] PyTorch 已安装
    echo.
    python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'"
    echo.
)

echo [检查 3] CUDA 工具包
where nvcc >nul 2>&1
if errorlevel 1 (
    echo [结果] CUDA toolkit 未在 PATH 中
) else (
    echo [结果] CUDA toolkit 已安装
    nvcc --version
    echo.
)

echo ========================================
echo   检测完成
echo ========================================
echo.

echo 安装 CUDA 版 PyTorch:
echo   运行: scripts\install_cuda_pytorch.bat
echo.

echo 或手动安装:
echo   pip uninstall torch torchvision -y
echo   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
echo.

pause
