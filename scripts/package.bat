@echo off
REM Kronos Web UI - 可移动版本打包脚本
REM 创建一个可以拷贝到其他电脑使用的压缩包

chcp 65001 >nul 2>&1

echo ========================================
echo   Kronos Web UI - 可移动版本打包
echo ========================================
echo.

REM 设置版本号
set VERSION=2.0.0
set PACKAGE_NAME=kronos-web-ui-portable-%VERSION%

REM 创建临时目录
echo [1/6] 创建临时目录...
if exist "build\package" rmdir /s /q "build\package"
mkdir "build\package"

REM 复制核心文件
echo [2/6] 复制核心文件...
xcopy /E /I /Y core "build\package\core" >nul
xcopy /E /I /Y config "build\package\config" >nul
xcopy /E /I /Y templates "build\package\templates" >nul
xcopy /E /I /Y scripts "build\package\scripts" >nul
xcopy /E /I /Y docs "build\package\docs" >nul

REM 创建必要的空目录
echo [3/6] 创建目录结构...
mkdir "build\package\cache\models" 2>nul
mkdir "build\package\logs" 2>nul
mkdir "build\package\static\exports" 2>nul

REM 复制配置和文档文件
echo [4/6] 复制配置文件...
copy /Y README.md "build\package\" >nul
copy /Y LICENSE "build\package\" >nul
copy /Y requirements.txt "build\package\" >nul
copy /Y CONTRIBUTING.md "build\package\" >nul

REM 创建启动说明
echo [5/6] 创建启动说明...
(
echo Kronos Web UI v%VERSION% - 可移动版本
echo.
echo ========================================
echo.
echo 快速启动：
echo.
echo Windows 用户：
echo   1. 双击运行：scripts\start.bat
echo   2. 等待浏览器自动打开
echo   3. 开始使用！
echo.
echo 首次使用需要：
echo   1. 安装 Python 3.10-3.13
echo   2. 运行：pip install -r requirements.txt
echo.
echo 详细说明请查看：README.md
echo.
echo ========================================
) > "build\package\启动说明.txt"

REM 创建部署说明
(
echo # Kronos Web UI - 部署说明
echo.
echo ## 版本信息
echo - 版本: v%VERSION%
echo - 类型: 可移动版本
echo - 日期: %date% %time%
echo.
echo ## 系统要求
echo.
echo ### 最低配置
echo - **操作系统**: Windows 10/11, Linux, macOS
echo - **Python**: 3.10 - 3.13（推荐 3.13）
echo - **内存**: 4GB+
echo - **硬盘**: 2GB 可用空间（不含模型）
echo.
echo ### GPU 加速（可选）
echo - **NVIDIA**: GTX 1060 或更新（4GB+ 显存）
echo - **Python**: 需要 3.13 以支持 CUDA
echo.
echo ## 安装步骤
echo.
echo ### 步骤 1: 解压文件
echo ```bash
echo # 将压缩包解压到任意目录
echo # 例如：D:\Kronos_UI 或 /home/user/Kronos_UI
echo ```
echo.
echo ### 步骤 2: 安装 Python（如果还没有）
echo.
echo #### Windows
echo 1. 访问：https://www.python.org/downloads/
echo 2. 下载 Python 3.13
echo 3. 安装时勾选 "Add Python to PATH"
echo.
echo #### Linux
echo ```bash
echo sudo apt update
echo sudo apt install python3.13 python3-pip
echo ```
echo.
echo #### macOS
echo ```bash
echo brew install python@3.13
echo ```
echo.
echo ### 步骤 3: 安装依赖
echo ```bash
echo # Windows
echo pip install -r requirements.txt
echo.
echo # Linux/Mac
echo pip3 install -r requirements.txt
echo ```
echo.
echo ### 步骤 4: 启动应用
echo.
echo #### Windows
echo ```bash
echo # 双击运行
echo scripts\start.bat
echo.
echo # 或命令行
echo cd scripts
echo start.bat
echo ```
echo.
echo #### Linux/Mac
echo ```bash
echo cd scripts
echo bash start.sh
echo ```
echo.
echo ### 步骤 5: 打开浏览器
echo.
echo 应用启动后，浏览器会自动打开：
echo.
echo **http://localhost:7070**
echo.
echo 如果没有自动打开，请手动访问上述地址。
echo.
echo ## 首次使用
echo.
echo 1. **选择模型** - 推荐使用 Kronos-small（平衡速度和精度）
echo 2. **选择设备** - 有 NVIDIA 显卡选择 CUDA，否则选择 CPU
echo 3. **加载模型** - 首次需要下载模型（约 100-500MB）
echo 4. **输入股票代码** - 如 A 股：601212
echo 5. **开始预测** - 点击预测按钮
echo.
echo ## 目录结构
echo.
echo ```
echo kronos-web-ui-portable/
echo ├── core/              # 核心代码
echo ├── config/            # 配置文件
echo ├── templates/         # Web 界面
echo ├── scripts/           # 启动脚本
echo ├── docs/              # 文档
echo ├── cache/             # 缓存目录（自动创建）
echo ├── logs/              # 日志目录（自动创建）
echo ├── requirements.txt   # Python 依赖
echo ├── README.md          # 项目说明
echo ├── LICENSE            # 许可证
echo └── 启动说明.txt       # 快速启动指南
echo ```
echo.
echo ## 可选配置
echo.
echo ### GPU 加速（Windows + Python 3.13）
echo.
echo 如果您有 NVIDIA 显卡，可以启用 GPU 加速：
echo.
echo ```bash
echo # 运行 CUDA 安装脚本
echo cd scripts
echo install_cuda_pytorch.bat
echo ```
echo.
echo ### Tushare Token（可选）
echo.
echo 如果需要使用 Tushare 作为备用数据源：
echo.
echo **Windows**:
echo ```cmd
echo set TUSHARE_TOKEN=your_token_here
echo ```
echo.
echo **Linux/Mac**:
echo ```bash
echo export TUSHARE_TOKEN=your_token_here
echo ```
echo.
echo ## 故障排除
echo.
echo ### 问题 1: 端口被占用
echo.
echo **错误**: 端口 7070 已被使用
echo.
echo **解决**:
echo - 修改 `config/config.json` 中的端口号
echo - 或关闭占用端口的程序
echo.
echo ### 问题 2: Python 版本过低
echo.
echo **错误**: Python 版本不兼容
echo.
echo **解决**:
echo - 安装 Python 3.10-3.13
echo - 推荐使用 Python 3.13
echo.
echo ### 问题 3: 依赖安装失败
echo.
echo **错误**: pip install 失败
echo.
echo **解决**:
echo ```bash
echo # 升级 pip
echo python -m pip install --upgrade pip
echo.
echo # 使用国内镜像
echo pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo ```
echo.
echo ### 问题 4: CUDA 不可用
echo.
echo **错误**: CUDA available: False
echo.
echo **解决**:
echo - 确认使用 Python 3.13
echo - 运行 `scripts\install_cuda_pytorch.bat`
echo - 或继续使用 CPU 模式
echo.
echo ## 技术支持
echo.
echo - **文档**: 查看 `docs/` 目录
echo - **GitHub**: https://github.com/jjzhu-newman/kronos-web-ui
echo - **Issues**: https://github.com/jjzhu-newman/kronos-web-ui/issues
echo.
echo ## 更新日志
echo.
echo ### v2.0.0 (当前版本)
echo - 🚀 完全重构的 UI/UX
echo - ⚡ GPU 加速支持
echo - 💾 本地模型缓存
echo - 🔄 多数据源自动降级
echo - 📊 交互式图表
echo.
echo ## 许可证
echo.
echo MIT License - 详见 LICENSE 文件
echo.
echo ---
echo.
echo **祝您使用愉快！** 🚀
echo.
echo _生成时间: %date% %time%_
) > "build\package\部署说明.md"

echo [6/6] 创建压缩包...
echo.
echo 正在压缩，请稍候...
echo.

REM 使用 PowerShell 创建 ZIP 文件
powershell -Command "Compress-Archive -Path 'build\package\*' -DestinationPath 'build\%PACKAGE_NAME%.zip' -Force"

if errorlevel 1 (
    echo.
    echo [错误] 压缩失败！
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 压缩包位置:
echo   build\%PACKAGE_NAME%.zip
echo.
echo 文件大小:
for %%A in ("build\%PACKAGE_NAME%.zip") do echo   %%~zA 字节
echo.
echo 解压后可直接在其他电脑上使用！
echo.
echo ========================================
echo.
echo 按任意键退出...
pause >nul
