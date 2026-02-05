#!/bin/bash
# Kronos UI - 启动脚本 (Linux/Mac)

echo "========================================"
echo "  Kronos Web UI v2.0"
echo "  AI Financial Prediction Platform"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3！"
    echo "请先安装Python 3.10或更高版本"
    exit 1
fi

echo "[1/4] 检测到Python版本:"
python3 --version
echo

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# 检查并创建必要目录
mkdir -p logs cache/models static/exports

echo "[2/4] 检查依赖包..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "首次运行，正在安装依赖包..."
    echo "这可能需要几分钟，请耐心等待..."
    echo
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo
        echo "[错误] 依赖安装失败！"
        echo "请检查网络连接或手动运行: pip install -r requirements.txt"
        exit 1
    fi
    echo
else
    echo "依赖包已安装"
fi
echo

echo "[3/4] 检查配置文件..."
if [ ! -f "config/config.json" ]; then
    echo "[警告] 配置文件不存在！"
    exit 1
fi
echo "配置文件检查完成"
echo

echo "[4/4] 启动Kronos Web服务器..."
echo
echo "========================================"
echo "服务器将在以下地址启动:"
echo "  http://localhost:7070"
echo "========================================"
echo
echo "浏览器将自动打开，如未打开请手动访问上述地址"
echo "按 Ctrl+C 停止服务器"
echo "========================================"
echo

# 启动应用
python3 core/app.py
