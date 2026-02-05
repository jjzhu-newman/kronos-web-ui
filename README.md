# Kronos Web UI

<div align="center">

![Kronos Web UI](https://img.shields.io/badge/Kronos-Web%20UI-blue)
![Version](https://img.shields.io/badge/version-2.0.0-green)
![Python](https://img.shields.io/badge/python-3.13+-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

**AI 驱动的金融时间序列预测平台**

基于 Kronos 深度学习模型的 Web 界面，支持股票、期货、加密货币等多种金融产品的价格预测。

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用指南](#使用指南) • [配置说明](#配置说明)

</div>

---

## 📖 简介

Kronos Web UI 是一个**开箱即用**的金融预测平台，基于先进的 Kronos 时间序列预测模型。通过简洁的 Web 界面，用户可以轻松：

- 📈 实时获取 A 股、美股、加密货币等市场数据
- 🤖 使用深度学习模型进行价格预测
- 📊 可视化预测结果和历史趋势
- ⚡ 支持 GPU 加速，预测速度提升 5-10 倍

### 主要特点

✨ **开箱即用** - 一键启动，无需复杂配置  
🔄 **多数据源** - Akshare、Baostock、Tushare 自动降级  
💾 **本地缓存** - 模型本地缓存，无需重复下载  
🚀 **GPU 加速** - 支持 CUDA/MPS 加速  
📊 **实时可视化** - 基于 Lightweight Charts 的交互式图表  
🌐 **Web 界面** - 现代化响应式设计，支持移动端

---

## 🚀 功能特性

### 数据源支持

| 市场 | 数据源 | 状态 |
|------|--------|------|
| **A 股** | Akshare / Baostock / Tushare | ✅ 三级自动降级 |
| **美股** | Yfinance | ✅ |
| **加密货币** | Binance API | ✅ |
| **港股** | Yfinance | ✅ |

### 模型支持

| 模型 | 参数量 | 速度 | 推荐场景 |
|------|--------|------|----------|
| **Kronos-mini** | 4.1M | ⚡⚡⚡ 最快 | 快速测试 |
| **Kronos-small** | 24.7M | ⚡⚡ 平衡 | 日常使用（推荐） |
| **Kronos-base** | 102.3M | ⚡ 最精准 | 深度分析 |

### 设备支持

- 🖥️ **CPU** - 完全支持，速度约 30-60 秒
- 🎮 **CUDA (NVIDIA)** - 支持 RTX 1060+，速度约 5-10 秒
- 🍎 **MPS (Apple Silicon)** - 支持 M1/M2/M3 芯片

---

## 📦 快速开始

### 系统要求

#### 最低配置
- **Python**: 3.10 - 3.13（推荐 3.13）
- **内存**: 4GB+
- **硬盘**: 2GB 可用空间

#### GPU 加速（可选）
- **NVIDIA**: GTX 1060 或更新（4GB+ 显存）
- **驱动**: 最新 NVIDIA 驱动
- **CUDA**: 12.4（Python 3.13 自动支持）

### 安装步骤

#### 方式 1: 直接下载（推荐）

1. **下载项目**
   ```bash
   git clone https://github.com/jjzhu-newman/kronos-web-ui.git
   cd kronos-web-ui
   ```

2. **运行启动脚本**
   ```bash
   # Windows
   scripts\start.bat

   # Linux/Mac
   bash scripts/start.sh
   ```

3. **打开浏览器**
   ```
   http://localhost:7070
   ```

#### 方式 2: 手动安装

1. **安装 Python 依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **启动应用**
   ```bash
   python core/app.py
   ```

### 首次使用

1. **选择模型** - 推荐使用 `Kronos-small`（平衡速度和精度）
2. **选择设备** - 有 NVIDIA 显卡选择 `CUDA`，否则选择 `CPU`
3. **点击"加载模型"** - 首次需要下载模型（约 100-500MB，已自动缓存）
4. **输入股票代码** - 如 A 股：`601212`（白银有色）
5. **点击"预测"** - 等待 5-60 秒查看预测结果

---

## 📖 使用指南

### 基础操作

#### 1. 加载模型

![模型选择界面](docs/images/model-selection.png)

- **模型选择**: 根据需求选择模型大小
- **设备选择**: 自动检测可用设备
- **高级设置**: 
  - `Lookback`: 历史数据点数（默认 400）
  - `预测长度`: 预测未来数据点数（默认 120）

#### 2. 数据获取

系统采用**三级自动降级**策略：

```
Akshare（主数据源）
    ↓ 失败自动切换
Baostock（第一备用）
    ↓ 失败自动切换
Tushare（第二备用）
```

#### 3. 参数调整

**Temperature（温度）** - 控制预测保守程度

| 值 | 效果 | 场景 |
|----|------|------|
| 0.6 - 0.8 | 保守 | 稳定市场 |
| 1.0 | 默认 | 日常使用 |
| 1.2 - 1.5 | 激进 | 波动行情 |

**Top-P（核采样）** - 控制预测多样性

| 值 | 效果 | 场景 |
|----|------|------|
| 0.8 - 0.9 | 集中 | 确定性高 |
| 0.9 - 0.95 | 平衡 | 默认推荐 |
| 1.0 | 分散 | 不确定性高 |

### 数据导出

支持导出格式：
- 📊 **CSV** - Excel 友好
- 📈 **图片** - PNG 高清图表
- 📋 **JSON** - 程序化处理

---

## ⚙️ 配置说明

### 配置文件

主配置文件: `config/config.json`

```json
{
  "app": {
    "name": "Kronos Web UI",
    "version": "2.0.0",
    "port": 7070,
    "auto_open_browser": true
  },
  "data_sources": {
    "a_stocks": {
      "primary": "akshare",
      "fallback_1": "baostock",
      "fallback_2": "tushare"
    }
  }
}
```

### Tushare 配置（可选）

如需使用 Tushare 作为备用数据源：

1. 注册账号: https://tushare.pro/register
2. 获取 Token
3. 设置环境变量:
   ```bash
   # Windows
   set TUSHARE_TOKEN=your_token_here

   # Linux/Mac
   export TUSHARE_TOKEN=your_token_here
   ```

---

## 📂 项目结构

```
kronos-web-ui/
├── core/                   # 核心模块
│   ├── model/             # Kronos 模型
│   ├── app.py             # Flask 主应用
│   ├── config_loader.py   # 配置加载器
│   ├── data_fetcher.py    # 数据获取器
│   ├── logger.py          # 日志系统
│   └── model_cache.py     # 模型缓存管理
├── templates/             # 前端模板
│   └── index.html        # 主界面
├── config/               # 配置文件
│   ├── config.json      # 主配置
│   └── models.json      # 模型配置
├── cache/               # 缓存目录
│   └── models/          # 模型缓存
├── logs/                # 日志文件
├── scripts/             # 启动脚本
│   ├── start.bat       # Windows 启动脚本
│   └── start.sh        # Linux/Mac 启动脚本
├── docs/                # 文档
│   ├── USER_GUIDE.md   # 用户指南
│   ├── CUDA_GUIDE.md   # CUDA 安装指南
│   ├── ERROR_LOG.md    # 错误日志
│   └── DEVELOPMENT_LOG.md # 开发日志
├── requirements.txt     # Python 依赖
└── README.md           # 项目说明
```

---

## 🔧 高级功能

### GPU 加速设置

如需启用 GPU 加速（推荐）：

#### Windows

1. **检查 Python 版本**
   ```bash
   python --version
   # 推荐 Python 3.13
   ```

2. **安装 CUDA 版 PyTorch**（Python 3.13）
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
   ```

3. **验证 CUDA**
   ```bash
   python -c "import torch; print(torch.cuda.is_available())"
   # 输出: True
   ```

详细指南: [docs/CUDA_GUIDE.md](docs/CUDA_GUIDE.md)

### 模型缓存管理

模型自动缓存到 `cache/models/` 目录：

- **Kronos-mini**: 约 16MB
- **Kronos-small**: 约 95MB
- **Kronos-base**: 约 391MB
- **Tokenizers**: 约 16MB 每个

首次下载后，下次启动无需重新下载。

---

## 🐛 故障排除

### 常见问题

#### 1. 模型加载失败

**错误**: `Failed to load model`

**解决**:
- 检查网络连接
- 查看日志文件 `logs/app.log`
- 尝试手动下载模型

#### 2. CUDA 不可用

**错误**: `CUDA available: False`

**解决**:
- 检查 Python 版本（需要 3.10-3.13）
- 安装 CUDA 版 PyTorch
- 更新 NVIDIA 驱动

详细错误解决: [docs/ERROR_LOG.md](docs/ERROR_LOG.md)

#### 3. 数据获取失败

**错误**: `所有数据源均无法获取数据`

**解决**:
- 检查股票代码格式（A 股使用纯数字，如 `601212`）
- 检查网络连接
- 等待几分钟后重试（可能 API 限流）

---

## 📚 文档

- [用户指南](docs/USER_GUIDE.md) - 详细使用说明
- [CUDA 指南](docs/CUDA_GUIDE.md) - GPU 加速设置
- [错误日志](docs/ERROR_LOG.md) - 常见问题解决
- [开发日志](docs/DEVELOPMENT_LOG.md) - 开发历程

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [Kronos Model](https://github.com/NeoQuasar/Kronos) - 时间序列预测基础模型
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [Lightweight Charts](https://www.tradingview.com/lightweight-charts/) - 图表库
- [Akshare](https://akshare.akfamily.xyz/) - A 股数据接口
- [PyTorch](https://pytorch.org/) - 深度学习框架

---

## 📮 联系方式

- **作者**: jjzhu-newman
- **GitHub**: [@jjzhu-newman](https://github.com/jjzhu-newman)
- **问题反馈**: [Issues](https://github.com/jjzhu-newman/kronos-web-ui/issues)

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐ Star！**

Made with ❤️ by [jjzhu-newman](https://github.com/jjzhu-newman)

</div>
