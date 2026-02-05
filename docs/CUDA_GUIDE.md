# CUDA 支持指南

## 检测当前状态

运行 `scripts\check_cuda.bat` 检测您的 CUDA 环境。

---

## 问题诊断

### 当前状态

```
PyTorch version: 2.10.0+cpu
CUDA available: False
```

**说明**: 您安装的是 **PyTorch CPU 版本**，不支持 CUDA。

---

## 安装 CUDA 版 PyTorch

### 方法1: 使用安装脚本（推荐）

```cmd
cd D:\ClaudeCode\Kronos_UI\scripts
install_cuda_pytorch.bat
```

### 方法2: 手动安装

```cmd
# 1. 卸载 CPU 版本
pip uninstall torch torchvision -y

# 2. 安装 CUDA 版本 (CUDA 12.4)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

### 方法3: 其他 CUDA 版本

**CUDA 11.8** (较旧，兼容性好):
```cmd
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**CUDA 12.1**:
```cmd
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

---

## 系统要求

### 最低要求
- NVIDIA 显卡：GTX 1060 或更新
- 显存：4GB+
- 驱动：最新 NVIDIA 驱动
- 操作系统：Windows 10/11
- **Python 版本：3.12 或 3.13** ⚠️ **不支持 Python 3.14**

### 推荐配置
- NVIDIA 显卡：RTX 3060 或更新
- 显存：8GB+
- CUDA：12.4
- **Python：3.13** (最新稳定版，完全支持)

### ⚠️ 重要：Python 版本兼容性

| Python 版本 | PyTorch CUDA 支持 | 推荐使用 |
|-------------|------------------|---------|
| 3.14 | ❌ 无 CUDA wheel | 不推荐 |
| 3.13 | ✅ 完全支持 | **强烈推荐** |
| 3.12 | ✅ 完全支持 | 推荐 |
| 3.11 | ✅ 完全支持 | 可用 |
| 3.10 | ✅ 完全支持 | 可用 |

**当前检测**: Python 3.14.2
**状态**: ❌ PyTorch 仅支持 CPU 版本
**解决方案**: 降级到 Python 3.13 或 3.12

---

## Python 3.14 用户：如何启用 CUDA

如果您当前使用 Python 3.14，请按以下步骤操作：

### 步骤1: 下载 Python 3.13

1. 访问 Python 官网: https://www.python.org/downloads/
2. 下载 **Python 3.13.x** (最新稳定版)
3. 安装时选择自定义路径，如 `C:\Python313`
4. 勾选 "Add Python to PATH" (可选)

### 步骤2: 使用 Python 3.13 安装 CUDA PyTorch

打开命令提示符，执行：

```cmd
REM 使用 Python 3.13 直接安装 CUDA 版本
C:\Python313\python.exe -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

REM 验证安装
C:\Python313\python.exe -c "import torch; print('CUDA可用:', torch.cuda.is_available())"
```

应该输出: `CUDA可用: True`

### 步骤3: 使用 Python 3.13 运行 Kronos UI

**方法A: 修改启动脚本**
```cmd
REM 编辑 start.bat，将 python 改为:
C:\Python313\python.exe core\app.py
```

**方法B: 直接运行**
```cmd
C:\Python313\python.exe D:\ClaudeCode\Kronos_UI\core\app.py
```

**方法C: 创建虚拟环境** (推荐)
```cmd
REM 创建 Python 3.13 虚拟环境
C:\Python313\python.exe -m venv D:\ClaudeCode\Kronos_UI\venv_gpu

REM 激活虚拟环境
D:\ClaudeCode\Kronos_UI\venv_gpu\Scripts\activate.bat

REM 安装 CUDA PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

REM 安装其他依赖
pip install -r requirements.txt

REM 运行应用
python core\app.py
```

---

## 验证安装

安装完成后，验证：

```cmd
python -c "import torch; print(f'CUDA可用: {torch.cuda.is_available()}')"
```

如果输出 `True`，说明安装成功！

---

## 常见问题

### Q1: 安装后仍然报错 "Torch not compiled with CUDA enabled"

**原因**: 可能是 NVIDIA 驱动版本过旧

**解决**:
1. 更新 NVIDIA 驱动: https://www.nvidia.com/Download/index.aspx
2. 重新安装 PyTorch

---

### Q2: 安装时提示 "Could not find a version that satisfies the requirement"

**原因**: 网络问题或 PyTorch 源不可用

**解决**:
1. 使用国内镜像源:
```cmd
pip install torch torchvision -i https://pypi.tuna.tsinghua.edu.cn/simple
```

2. 或临时启用全局代理

---

### Q3: 安装成功但 `torch.cuda.is_available()` 返回 False

**原因**: NVIDIA 驱动版本不兼容

**解决**:
1. 检查驱动版本: `nvidia-smi`
2. 更新到最新驱动
3. 重新安装匹配的 PyTorch 版本

---

## 性能对比

| 设备 | 预测速度 (120点) | 内存占用 |
|------|-----------------|----------|
| CPU | ~30-60秒 | ~500MB |
| GPU (RTX 3060) | ~5-10秒 | ~1GB |
| GPU (RTX 4090) | ~2-5秒 | ~2GB |

---

## 如果没有 NVIDIA 显卡

不用担心！CPU 模式仍然可以正常使用：

- ✅ 完全支持所有功能
- ✅ 预测结果完全相同
- ⏱️ 只是速度慢一些（30-60秒 vs 5-10秒）

---

**更新时间**: 2025-02-04
