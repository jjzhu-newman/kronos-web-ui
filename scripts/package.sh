#!/bin/bash
# Kronos Web UI - 可移动版本打包脚本 (Linux/Mac)

VERSION="2.0.0"
PACKAGE_NAME="kronos-web-ui-portable-${VERSION}"

echo "========================================"
echo "  Kronos Web UI - 可移动版本打包"
echo "========================================"
echo ""

# 创建临时目录
echo "[1/6] 创建临时目录..."
rm -rf build/package
mkdir -p build/package

# 复制核心文件
echo "[2/6] 复制核心文件..."
cp -r core build/package/
cp -r config build/package/
cp -r templates build/package/
cp -r scripts build/package/
cp -r docs build/package/

# 创建必要的空目录
echo "[3/6] 创建目录结构..."
mkdir -p build/package/cache/models
mkdir -p build/package/logs
mkdir -p build/package/static/exports

# 复制配置和文档文件
echo "[4/6] 复制配置文件..."
cp README.md build/package/
cp LICENSE build/package/
cp requirements.txt build/package/
cp CONTRIBUTING.md build/package/

# 创建启动说明
echo "[5/6] 创建启动说明..."
cat > build/package/启动说明.txt << 'EOF'
Kronos Web UI - 可移动版本

========================================

快速启动：

Linux/Mac 用户：
  1. 打开终端，进入项目目录
  2. 运行：bash scripts/start.sh
  3. 等待浏览器自动打开
  4. 开始使用！

Windows 用户：
  1. 双击运行：scripts\start.bat
  2. 等待浏览器自动打开
  3. 开始使用！

首次使用需要：
  1. 安装 Python 3.10-3.13
  2. 运行：pip install -r requirements.txt

详细说明请查看：README.md

========================================
EOF

# 创建部署说明（同 Windows 版本）
cat > build/package/部署说明.md << EOF
# Kronos Web UI - 部署说明

## 版本信息
- 版本: v${VERSION}
- 类型: 可移动版本
- 日期: $(date)

## 系统要求

### 最低配置
- **操作系统**: Windows 10/11, Linux, macOS
- **Python**: 3.10 - 3.13（推荐 3.13）
- **内存**: 4GB+
- **硬盘**: 2GB 可用空间（不含模型）

### GPU 加速（可选）
- **NVIDIA**: GTX 1060 或更新（4GB+ 显存）
- **Python**: 需要 3.13 以支持 CUDA

## 安装步骤

### 步骤 1: 解压文件
\`\`\`bash
# 将压缩包解压到任意目录
# 例如：/home/user/Kronos_UI
\`\`\`

### 步骤 2: 安装 Python（如果还没有）

#### Linux
\`\`\`bash
sudo apt update
sudo apt install python3.13 python3-pip
\`\`\`

#### macOS
\`\`\`bash
brew install python@3.13
\`\`\`

### 步骤 3: 安装依赖
\`\`\`bash
pip3 install -r requirements.txt
\`\`\`

### 步骤 4: 启动应用
\`\`\`bash
cd scripts
bash start.sh
\`\`\`

### 步骤 5: 打开浏览器
应用启动后，浏览器会自动打开：
**http://localhost:7070**

## 首次使用

1. **选择模型** - 推荐使用 Kronos-small
2. **选择设备** - 有 NVIDIA 显卡选择 CUDA，否则选择 CPU
3. **加载模型** - 首次需要下载模型（约 100-500MB）
4. **输入股票代码** - 如 A 股：601212
5. **开始预测** - 点击预测按钮

## 技术支持

- **文档**: 查看 \`docs/\` 目录
- **GitHub**: https://github.com/jjzhu-newman/kronos-web-ui
- **Issues**: https://github.com/jjzhu-newman/kronos-web-ui/issues

---

**祝您使用愉快！** 🚀
EOF

# 创建压缩包
echo "[6/6] 创建压缩包..."
echo ""

cd build
if command -v tar &> /dev/null; then
    tar -czf "${PACKAGE_NAME}.tar.gz" package/
    echo "✓ 压缩包创建成功："
    echo "  build/${PACKAGE_NAME}.tar.gz"
    echo ""
    echo "文件大小："
    ls -lh "${PACKAGE_NAME}.tar.gz" | awk '{print "  " $5}'
else
    echo "错误: 未找到 tar 命令"
    exit 1
fi

cd ..

echo ""
echo "========================================"
echo "  打包完成！"
echo "========================================"
echo ""
echo "压缩包位置:"
echo "  build/${PACKAGE_NAME}.tar.gz"
echo ""
echo "解压后可直接在其他电脑上使用！"
echo ""
echo "========================================"
