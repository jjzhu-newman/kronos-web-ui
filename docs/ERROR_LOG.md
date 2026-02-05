# Kronos UI 错误记录与解决方案

> 项目: Kronos UI v2.0
> 开始时间: 2025-02-04
> 维护者: 开发团队

---

## 说明

本文档记录项目开发和使用过程中遇到的所有错误及其解决方案，便于快速排查问题。

---

## 开发阶段错误

### 错误 #001: Bash 命令路径问题

**时间**: 2025-02-04
**错误**: 使用 `dir /b` 命令在 Git Bash 中执行失败

```
dir: cannot access '/b': No such file or directory
```

**原因**: Git Bash 环境下不支持 Windows 的 `dir` 命令

**解决方案**: 使用 `ls` 命令代替
```bash
# 错误写法
dir /b "D:\ClaudeCode\Kronos_UI"

# 正确写法
ls -la "D:\ClaudeCode\Kronos_UI"
```

**预防**: 在跨平台脚本中使用 POSIX 兼容命令

---

### 错误 #002: 文件复制引号问题

**时间**: 2025-02-04
**错误**: Bash 复制命令中的引号未正确转义

```
/usr/bin/bash: eval: line 1: unexpected EOF while looking for matching `"'
```

**原因**: Windows 路径中的引号在 Bash 中需要特殊处理

**解决方案**: 使用正斜杠路径
```bash
# 错误写法
cp "D:\ClaudeCode\Kronos\..." "..."

# 正确写法
cp D:/ClaudeCode/Kronos/model/__init__.py D:/ClaudeCode/Kronos_UI/core/model/
```

---

### 错误 #003: app.py 语法错误

**时间**: 2025-02-04
**错误**: 运行 start.bat 时报语法错误

```
File "D:\ClaudeCode\Kronos_UI\core\app.py", line 319
    return jsonify({'error': str(e)}'), 500
                                    ^
SyntaxError: unterminated string literal
```

**原因**: app.py 第319行有多余的引号

**错误代码**:
```python
return jsonify({'error': str(e)}'), 500
```

**正确代码**:
```python
return jsonify({'error': str(e)}), 500
```

**解决方案**: 删除 `str(e)}` 后的额外引号

**预防**: 代码审查时注意字符串引号配对

---

### 错误 #004: 模型导入路径错误

**时间**: 2025-02-04
**错误**: 模型加载失败，提示 `KronosTokenizer.__init__() missing 8 required positional arguments`

**错误信息**:
```
[ERROR] 模型下载失败: KronosTokenizer.__init__() missing 8 required positional arguments: 'd_in', 'n_enc_layers', 'n_dec_layers', 'beta', 'gamma0', 'gamma', 'zeta', and 'group_size'
```

**原因**:
1. `core/model/kronos.py` 中的导入路径错误
2. `app.py` 中的模块导入路径不正确

**错误代码**:
```python
# core/model/kronos.py
sys.path.append("../")
from model.module import *  # 错误：使用了绝对导入

# core/app.py
from model import Kronos, KronosTokenizer  # 错误：找不到 model 模块
```

**正确代码**:
```python
# core/model/kronos.py
from .module import *  # 正确：使用相对导入

# core/app.py
from core.model import Kronos, KronosTokenizer  # 正确：完整路径
```

**解决方案**:
1. 修改 `kronos.py` 使用相对导入: `from .module import *`
2. 修改 `app.py` 使用完整导入路径: `from core.model import ...`

---

### 错误 #005: Windows 控制台中文乱码

**时间**: 2025-02-04
**错误**: Windows 控制台显示中文为乱码

**原因**: Windows 控制台默认使用 GBK 编码，而日志输出为 UTF-8

**解决方案**:

方法1: 在 `start.bat` 开头添加:
```cmd
chcp 65001 >nul 2>&1
```

方法2: 在 `app.py` 中设置编码:
```python
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

**注意**: 日志文件仍使用 UTF-8 编码，只是控制台显示需要设置

---

### 错误 #006: Tokenizer 和 Model ID 混淆

**时间**: 2025-02-04
**错误**: 模型加载时提示 `KronosTokenizer.__init__() missing 8 required positional arguments`

**错误信息**:
```
[ERROR] 模型下载失败: KronosTokenizer.__init__() missing 8 required positional arguments: 'd_in', 'n_enc_layers', 'n_dec_layers', 'beta', 'gamma0', 'gamma', 'zeta', and 'group_size'
```

**原因**: tokenizer 和 model 使用不同的 ID，需要分别加载：
- Kronos-mini 模型使用 `NeoQuasar/Kronos-mini`
- 但它的 tokenizer 使用 `NeoQuasar/Kronos-Tokenizer-2k`

**错误代码**:
```python
# 错误：使用同一个 model_id 加载两者
result = model_cache.get_or_download_model(
    model_id=model_cfg['model_id'],  # 如 "NeoQuasar/Kronos-mini"
    model_class=Kronos,
    tokenizer_class=KronosTokenizer,  # 但 tokenizer 需要不同的 ID
)
```

**正确代码**:
```python
# 正确：分别使用各自的 ID 加载
tokenizer = KronosTokenizer.from_pretrained(model_cfg['tokenizer_id'])  # "NeoQuasar/Kronos-Tokenizer-2k"
model = Kronos.from_pretrained(model_cfg['model_id'])  # "NeoQuasar/Kronos-mini"
```

**解决方案**:
在 `app.py` 中分别加载 tokenizer 和 model，使用各自的 ID

---

### 错误 #007: CUDA 不可用但仍可选择

**时间**: 2025-02-04
**错误**: 选择 GPU 设备时报错 "Torch not compiled with CUDA enabled"

**原因**: PyTorch CPU 版本不支持 CUDA，但前端未禁用 GPU 选项

**解决方案**:

1. 后端添加 CUDA 检测 (`/api/models` 和 `/api/status`)
2. 前端根据 CUDA 可用性启用/禁用 GPU 选项

**实现**:
```python
# 后端：检测 CUDA
import torch
cuda_available = torch.cuda.is_available()

# 前端：根据可用性控制选项
if (!cuda_available) {
    cudaOption.disabled = true;
    cudaOption.text = 'CUDA (不可用 - PyTorch CPU版本)';
    // 自动切换到 CPU
    deviceSelect.value = 'cpu';
}
```

---

### 错误 #008: 模型缓存状态显示不准确

**时间**: 2025-02-04
**症状**: 页面显示"模型未缓存需下载"，但实际已缓存

**原因**: 只检查了 model 缓存，未检查 tokenizer 缓存

**解决方案**:
```python
# 检查 model 和 tokenizer 的缓存状态
model_cached = model_cache.is_model_cached(model['model_id'])
tokenizer_cached = model_cache.is_model_cached(model['tokenizer_id'])

# 只有两者都缓存才标记为已缓存
model_info['cached'] = model_cached and tokenizer_cached
```

---

### 错误 #009: GPU 设备未经验证直接使用

**时间**: 2025-02-04
**错误**: 用户选择 GPU 设备时报错 `Torch not compiled with CUDA enabled`

**原因**: 前端未正确禁用 GPU 选项，或用户使用了缓存的旧页面

**解决方案**: 后端添加设备验证，自动降级到 CPU

**实现**:
```python
# 检查 CUDA 可用性
import torch
cuda_available = torch.cuda.is_available()

# 如果请求使用 CUDA 但不可用，自动降级
if device.startswith('cuda') and not cuda_available:
    logger.warning(f"CUDA requested but not available, downgrading to CPU")
    device = 'cpu'  # 自动降级
```

**结果**: 即使用户选择了 GPU，如果没有 CUDA 也会自动切换到 CPU，不会报错

---

### 错误 #010: PyTorch CPU 版本导致 CUDA 不可用

**时间**: 2025-02-04
**错误**: 用户有 NVIDIA 显卡，但选择 GPU 时报错 "Torch not compiled with CUDA enabled"

**实际检测**:
```
PyTorch version: 2.10.0+cpu
CUDA available: False
```

**根本原因**: 安装了 PyTorch **CPU 版本**而不是 CUDA 版本

**为什么之前的项目能用？**
- 之前的项目可能使用不同的 Python 环境
- 或者之前安装了 CUDA 版本的 PyTorch

**解决方案**:

**方案1: 重新安装 CUDA 版 PyTorch** (推荐)
```cmd
# 运行安装脚本
cd D:\ClaudeCode\Kronos_UI\scripts
install_cuda_pytorch.bat
```

**方案2: 手动安装**
```cmd
# 卸载 CPU 版本
pip uninstall torch torchvision -y

# 安装 CUDA 12.4 版本
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

**方案3: 安装其他 CUDA 版本**
```cmd
# CUDA 11.8 (兼容性更好)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

**验证安装**:
```cmd
python -c "import torch; print(f'CUDA可用: {torch.cuda.is_available()}')"
# 应该输出: True
```

**相关文档**: `docs/CUDA_GUIDE.md`

**预防**:
- 创建独立的环境变量或虚拟环境
- 在虚拟环境中安装特定版本的 PyTorch
- 明确标注环境用途（如 "Kronos GPU 环境"）

---

### 错误 #011: Python 3.14 不支持 CUDA PyTorch

**时间**: 2025-02-05
**错误**: 运行 install_cuda_pytorch.bat 后，PyTorch 仍然是 CPU 版本

**实际检测**:
```
Python版本: 3.14.2
PyTorch version: 2.10.0+cpu
CUDA available: False
```

**根本原因**: **Python 3.14 太新，PyTorch 尚未发布 Python 3.14 的 CUDA wheel**

**详细分析**:
检查 PyTorch 官方 wheel 源发现：
- Python 3.14 (cp314): ❌ 无 CUDA wheel
- Python 3.13 (cp313): ✅ 有 CUDA wheel (torch 2.6.0+cu124)
- Python 3.12 (cp312): ✅ 有 CUDA wheel (torch 2.4.0-2.6.0+cu124)

**解决方案**:

**方案1: 降级到 Python 3.13** (强烈推荐)
```cmd
# 1. 下载 Python 3.13
# https://www.python.org/downloads/release/python-1313/

# 2. 安装 Python 3.13 到新目录（如 C:\Python313）

# 3. 使用 Python 3.13 安装 CUDA PyTorch
C:\Python313\python.exe -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

# 4. 验证
C:\Python313\python.exe -c "import torch; print('CUDA可用:', torch.cuda.is_available())"
```

**方案2: 使用 Python 3.12** (备选)
```cmd
# Python 3.12 同样支持 CUDA
# 下载: https://www.python.org/downloads/release/python-3128/
```

**方案3: 继续使用 Python 3.14 + CPU** (当前方案)
- ✅ 完全支持所有功能
- ✅ 预测结果完全相同
- ⏱️ 预测速度: 30-60秒 (vs GPU: 5-10秒)
- ✅ 无需任何修改

**方案4: 等待 PyTorch 发布 Python 3.14 CUDA wheel**
- PyTorch 将在未来版本中支持 Python 3.14
- 可以关注 PyTorch 发布说明: https://github.com/pytorch/pytorch/releases

**推荐方案**: 方案1 (Python 3.13)

**原因**:
1. Python 3.13 是最新稳定版
2. PyTorch 2.6.0+cu124 完全支持 Python 3.13
3. 一行命令即可安装 CUDA 版本
4. GPU 加速可提升 5-10倍性能

**相关文档**: `docs/CUDA_GUIDE.md`

---

## 潜在运行时错误

### 错误 #101: 模型未加载

**症状**: 点击预测按钮提示 "Model not loaded"

**可能原因**:
1. 模型加载失败
2. 页面刷新后模型丢失
3. 模型加载超时

**解决方案**:
```python
# 检查模型是否已加载
if predictor is None:
    return jsonify({'error': 'Model not loaded'}), 400

# 前端检查
const status = await checkStatus();
if (!status.model_loaded) {
    alert('请先加载模型');
    return;
}
```

**预防**:
- 在前端显示模型加载状态
- 自动重新加载模型

---

### 错误 #102: 数据获取失败

**症状**: "所有数据源均无法获取数据"

**可能原因**:
1. 网络连接问题
2. 交易代码格式错误
3. API 限流
4. 数据源服务不可用

**解决方案**:
1. 检查网络连接
2. 验证交易代码格式
3. 等待几分钟后重试
4. 切换到其他数据源

**日志示例**:
```
[WARNING] Akshare 获取 601212 失败: Connection timeout
[WARNING] Baostock 获取 601212 失败: API error
[INFO] Tushare 获取 601212 成功: 500 条数据
```

---

### 错误 #103: 模型下载失败

**症状**: 模型加载一直显示"下载中"

**可能原因**:
1. HuggingFace 连接超时
2. 网络限速
3. 磁盘空间不足
4. 防火墙阻止

**解决方案**:
1. 检查网络连接
2. 使用 VPN 或镜像源
3. 清理磁盘空间
4. 检查防火墙设置

**手动下载**:
```python
# 设置 HF 镜像源
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

---

### 错误 #104: 数据量不足

**症状**: "Insufficient data: got 200 points, need 400"

**原因**: 历史数据点数少于 lookback 参数

**解决方案**:
1. 减少 lookback 参数
2. 选择时间跨度更长的交易代码
3. 使用更大的 interval（如日线代替小时线）

```javascript
// 调整参数
lookback = 200  // 从 400 减少到 200
```

---

### 错误 #105: 端口被占用

**症状**: 启动失败，提示端口 7070 已被使用

**解决方案**:

**Windows**:
```cmd
netstat -ano | findstr :7070
taskkill /PID <PID> /F
```

**Linux/Mac**:
```bash
lsof -ti:7070 | xargs kill -9
```

**或修改配置**:
```json
{
  "app": {
    "port": 7071  // 改用其他端口
  }
}
```

---

### 错误 #106: 依赖包冲突

**症状**: ImportError 或版本冲突

**示例**:
```
ImportError: cannot import name 'url_quote' from 'werkzeug.urls'
```

**原因**: Flask 和 Werkzeug 版本不兼容

**解决方案**:
```bash
pip install --upgrade flask werkzeug
```

或指定兼容版本:
```
flask>=3.0.0
werkzeug>=3.0.0
```

---

### 错误 #107: Baostock 登录失败

**症状**: "Baostock 登录失败"

**原因**: Baostock 服务问题或网络问题

**解决方案**:
1. 检查 Baostock 服务状态
2. 系统会自动降级到其他数据源
3. 可以禁用 Baostock 使用其他数据源

---

### 错误 #108: CUDA 不可用

**症状**: 选择 CUDA 后报错

**错误信息**:
```
RuntimeError: CUDA available: False
```

**原因**:
1. 未安装 NVIDIA 驱动
2. PyTorch CPU 版本
3. CUDA 版本不匹配

**解决方案**:
1. 使用 CPU 模式
2. 或安装 CUDA 版本的 PyTorch:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

---

## 配置错误

### 错误 #201: 配置文件不存在

**症状**: "配置文件不存在: config/config.json"

**解决方案**:
1. 检查项目目录结构
2. 确保 `config/config.json` 存在
3. 检查文件权限

---

### 错误 #202: 日志目录无法创建

**症状**: "Permission denied: logs/"

**解决方案**:
1. 检查目录权限
2. 手动创建 logs 目录:
```bash
mkdir logs
```

---

## 数据源特定错误

### Akshare 错误

#### 错误 #301: Akshare 限流

**症状**: "Akshare API 限流"

**解决方案**:
- 系统自动降级到 Baostock
- 等待几分钟后重试
- 使用其他数据源

#### 错误 #302: 股票代码格式错误

**症状**: "无法识别的股票代码"

**解决方案**:
- A股代码不需要交易所后缀
- 使用纯数字: `601212` 而不是 `601212.SH`

---

### Baostock 错误

#### 错误 #311: Baostock 未安装

**症状**: "Baostock 未安装"

**解决方案**:
```bash
pip install baostock
```

---

### Tushare 错误

#### 错误 #321: Tushare Token 未设置

**症状**: "Tushare 未配置"

**解决方案**:
1. 注册 Tushare: https://tushare.pro/register
2. 获取 token
3. 设置环境变量:
```cmd
set TUSHARE_TOKEN=your_token_here
```

#### 错误 #322: 积分不足

**症状**: "Tushare API 积分不足"

**原因**: 免费用户每日 1000 积分限制

**解决方案**:
- 等待第二天积分重置
- 或升级到专业版
- 或使用其他数据源

---

## 前端错误

### 错误 #401: 图表不显示

**症状**: 点击预测后图表区域空白

**可能原因**:
1. Lightweight Charts 未加载
2. 数据格式错误
3. 浏览器兼容性

**解决方案**:
1. 检查浏览器控制台错误
2. 刷新页面重试
3. 使用 Chrome/Edge 浏览器

---

### 错误 #402: 预测结果为空

**症状**: 显示 "No data to export"

**原因**: 预测失败或未执行

**解决方案**:
1. 检查是否已加载模型
2. 查看预测错误提示
3. 检查数据源连接

---

## 性能问题

### 问题 #501: 首次启动慢

**症状**: 首次运行需要很长时间

**原因**:
1. 安装 Python 依赖（约1-2分钟）
2. 下载模型文件（约1-10分钟）

**优化**:
- 预先安装依赖
- 使用本地缓存模型

---

### 问题 #502: 预测速度慢

**症状**: 预测需要很长时间

**优化方案**:
1. 使用更小的模型（Kronos-mini）
2. 减少 lookback 参数
3. 减少 pred_len 参数
4. 使用 GPU 加速

---

## 调试技巧

### 1. 查看日志

```bash
# 应用日志
cat logs/app.log

# 错误日志
cat logs/error.log

# 实时查看
tail -f logs/app.log
```

### 2. 测试数据源

```python
from core.data_fetcher import MarketDataFetcher

fetcher = MarketDataFetcher()

# 测试 Akshare
df = fetcher.fetch_akshare('601212')

# 测试 Baostock
df = fetcher.fetch_baostock('601212')
```

### 3. 测试模型加载

```python
from model import Kronos, KronosTokenizer

model = Kronos.from_pretrained('NeoQuasar/Kronos-small')
tokenizer = KronosTokenizer.from_pretrained('NeoQuasar/Kronos-Tokenizer-base')
```

---

## 错误预防

### 开发阶段

1. 使用类型提示
2. 编写单元测试
3. 代码审查
4. 文档完善

### 部署阶段

1. 环境测试
2. 依赖版本锁定
3. 错误监控
4. 日志记录

---

## 联系支持

如果遇到未记录的错误，请：

1. 记录错误信息和堆栈跟踪
2. 查看 `logs/error.log`
3. 提交 GitHub Issue
4. 附带复现步骤

---

**最后更新**: 2025-02-04
**文档版本**: 1.0.0
