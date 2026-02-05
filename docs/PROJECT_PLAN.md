# Kronos UI 项目重构规划

> 项目创建时间: 2025-02-04
> 最后更新时间: 2025-02-04
> 当前状态: 规划中

---

## 一、项目概述

### 1.1 项目目标
创建一个**开箱即用、自给自足、可迁移**的 Kronos 金融预测 Web UI 项目。

### 1.2 核心要求
- ✅ **开箱即用**：双击启动，无需安装Python或任何依赖
- ✅ **自给自足**：不依赖外部文件夹，所有代码内置
- ✅ **可迁移**：复制到任何Windows电脑即可运行
- ✅ **模型缓存**：本地缓存，启动即用
- ✅ **多数据源**：Baostock(备用1) → Akshare(主) → Tushare(备用2)
- ✅ **完整文档**：开发日志、错误日志、使用指南

---

## 二、项目架构设计

### 2.1 目录结构

```
D:\ClaudeCode\Kronos_UI/
├── docs/                           # 项目文档
│   ├── PROJECT_PLAN.md             # 项目规划文件（本文件）
│   ├── DEVELOPMENT_LOG.md          # 开发对话日志
│   ├── ERROR_LOG.md                # 错误记录与解决方案
│   └── USER_GUIDE.md               # 用户使用指南
├── core/                           # 核心代码
│   ├── model/                      # Kronos模型代码
│   │   ├── __init__.py
│   │   ├── kronos.py
│   │   ├── module.py
│   │   └── predictor.py
│   ├── app.py                      # Flask主应用
│   └── data_fetcher.py             # 数据获取器（支持多数据源）
├── templates/                      # 前端模板
│   └── index.html                  # Web界面
├── static/                         # 静态资源
│   └── exports/                    # 导出文件目录
├── config/                         # 配置文件
│   ├── config.json                 # 主配置文件
│   └── models.json                 # 模型配置
├── cache/                          # 缓存目录
│   └── models/                     # 模型缓存
├── logs/                           # 日志目录
│   ├── app.log                     # 应用日志
│   └── error.log                   # 错误日志
├── scripts/                        # 启动脚本
│   ├── Kronos_UI.exe               # 打包后的可执行文件
│   ├── start.bat                   # 开发环境启动脚本
│   └── start.sh                    # Linux/Mac启动脚本
├── build/                          # 打包配置
│   ├── build.spec                  # PyInstaller配置
│   └── requirements.txt            # 打包依赖
├── runtime/                        # 运行时（可选，便携Python）
├── README.md                       # 项目说明
└── .gitignore                      # Git忽略文件
```

### 2.2 核心改进点

| 改进项 | 原实现 | 新实现 |
|--------|--------|--------|
| **启动方式** | 需要Python环境 | 双击exe直接运行 |
| **依赖管理** | 手动pip安装 | 内嵌于exe |
| **模型加载** | 每次从HF下载 | 本地缓存优先 |
| **路径管理** | 相对路径 `../Kronos` | 内置 `core/` 目录 |
| **A股数据源** | Akshare/Tushare | Baostock(备1)→Akshare(主)→Tushare(备2) |
| **配置管理** | 硬编码 | JSON配置文件 |
| **错误处理** | 控制台输出 | 文件日志记录 |
| **项目文档** | 无 | 完整文档体系 |

---

## 三、A股数据源架构

### 3.1 数据源优先级

```
Akshare（主数据源，免费，无需注册）
    ↓ 失败
Baostock（第一备用，免费，需简单注册）
    ↓ 失败
Tushare（第二备用，需token，积分限制）
```

### 3.2 各数据源特性

| 数据源 | 优先级 | 免费额度 | 注册要求 | 优势 | 劣势 |
|--------|--------|----------|----------|------|------|
| **Akshare** | 主 | 完全免费 | 无需注册 | 数据全、更新快 | 偶尔限流 |
| **Baostock** | 备用1 | 完全免费 | 简单注册 | 稳定可靠 | 数据量少 |
| **Tushare** | 备用2 | 1000积分/天 | 需要注册 | 数据质量高 | 需要token |

### 3.3 自动降级机制

```python
class MarketDataFetcher:
    def fetch_a_stock(self, symbol: str):
        """
        A股数据获取 - 自动降级策略
        """
        # 1. 尝试 Akshare（主数据源）
        try:
            return self.fetch_akshare(symbol)
        except Exception as e:
            logger.warning(f"Akshare失败: {e}")

        # 2. 尝试 Baostock（第一备用）
        try:
            return self.fetch_baostock(symbol)
        except Exception as e:
            logger.warning(f"Baostock失败: {e}")

        # 3. 尝试 Tushare（第二备用）
        try:
            return self.fetch_tushare(symbol)
        except Exception as e:
            logger.error(f"所有数据源均失败: {e}")
            raise
```

---

## 四、开箱即用实现方案

### 4.1 方案对比

| 方案 | 优点 | 缺点 | 选择 |
|------|------|------|------|
| PyInstaller打包 | 单文件exe，跨平台 | 体积大(~200MB)，首次启动慢 | ✅ 推荐 |
| Conda便携环境 | 体积小，更新快 | 需要启动脚本 | 备选 |
| Docker容器 | 完全隔离 | 需要安装Docker | 不推荐 |

### 4.2 PyInstaller打包方案

**优点：**
- 用户双击exe即可运行
- 无需安装Python
- 所有依赖内置

**打包命令：**
```bash
pyinstaller --clean --onefile ^
    --name "Kronos_UI" ^
    --icon=assets/icon.ico ^
    --add-data "templates;templates" ^
    --add-data "config;config" ^
    --hidden-import "torch" ^
    --hidden-import "transformers" ^
    --hidden-import "huggingface_hub" ^
    core/app.py
```

**生成的文件：**
- `Kronos_UI.exe` - 单文件可执行程序
- 首次运行自动解压到临时目录
- 模型缓存到 `%APPDATA%/Kronos_UI/cache`

---

## 五、开发任务清单

### 阶段1：基础架构搭建 ⏳
- [ ] 创建项目目录结构
- [ ] 移动并整合核心模型代码
- [ ] 创建配置文件系统
- [ ] 实现日志记录系统

### 阶段2：数据源扩展 ⏳
- [ ] 集成 Baostock 数据源
- [ ] 实现自动降级逻辑
- [ ] 添加数据源状态显示
- [ ] 更新前端数据源选择器

### 阶段3：模型缓存优化 ⏳
- [ ] 实现模型本地缓存
- [ ] 添加缓存管理功能
- [ ] 优化模型加载速度
- [ ] 添加下载进度显示

### 阶段4：打包与部署 ⏳
- [ ] 配置 PyInstaller
- [ ] 测试exe运行
- [ ] 优化启动速度
- [ ] 制作安装程序

### 阶段5：文档与测试 ⏳
- [ ] 编写用户使用指南
- [ ] 记录开发日志
- [ ] 记录错误与解决方案
- [ ] 全面测试项目功能

---

## 六、技术规范

### 6.1 配置文件

**config/config.json**
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
      "fallback_2": "tushare",
      "auto_fallback": true
    }
  },
  "models": {
    "cache_dir": "cache/models",
    "use_cache": true,
    "auto_download": true
  },
  "logging": {
    "level": "INFO",
    "console": true,
    "file": true
  }
}
```

### 6.2 依赖管理

**requirements.txt**（完整版）
```
# Core ML
torch>=2.0.0
numpy>=1.24.0
pandas>=2.0.0
einops==0.8.1
safetensors>=0.4.0
huggingface_hub>=0.23.0

# Web Framework
flask>=3.0.0
flask-cors>=4.0.0

# Data Sources
requests>=2.31.0
yfinance>=0.2.0
baostock>=0.8.8
akshare>=1.12.0
tushare>=1.4.0

# Utilities
tqdm>=4.67.0
matplotlib>=3.7.0
```

---

## 七、验收标准

### 7.1 开箱即用验收 ✅
- [ ] 双击 `Kronos_UI.exe` 直接启动
- [ ] 无需安装Python
- [ ] 无需安装任何依赖
- [ ] 首次运行自动下载模型（带进度条）

### 7.2 功能验收
- [ ] 浏览器自动打开 http://localhost:7070
- [ ] 可成功加载Kronos模型
- [ ] A股数据获取支持自动降级
- [ ] 可进行加密货币/美股预测
- [ ] 预测结果可导出

### 7.3 可迁移性验收
- [ ] 复制整个文件夹到新电脑
- [ ] 双击exe即可运行
- [ ] 所有功能正常

### 7.4 文档验收
- [ ] DEVELOPMENT_LOG.md 完整
- [ ] ERROR_LOG.md 详尽
- [ ] USER_GUIDE.md 清晰
- [ ] README.md 完善

---

## 八、开发日志

### 2025-02-04
- ✅ 完成项目审核
- ✅ 创建项目规划文档
- ✅ 确定开箱即用方案（PyInstaller）
- ✅ 确定A股数据源策略（Akshare→Baostock→Tushare）
- ⏳ 等待用户审核规划
- ⏳ 开始项目实施

---

## 九、风险与注意事项

### 9.1 打包相关
- PyInstaller打包后体积较大（~200-500MB）
- 首次启动可能较慢（解压临时文件）
- 杀毒软件可能误报（需数字签名）

### 9.2 数据源相关
- Baostock需要注册获取token
- Tushare积分限制（免费用户1000/天）
- Akshare可能限流

### 9.3 模型相关
- 首次运行需要从HuggingFace下载模型
- 模型较大（mini: ~20MB, small: ~100MB, base: ~400MB）
- 需要网络连接下载模型

---

## 十、后续优化方向

- [ ] 添加离线模式（本地模型）
- [ ] 支持自定义模型路径
- [ ] 添加数据源测试功能
- [ ] 支持批量预测
- [ ] 添加预测结果对比功能

---

**备注：** 本规划是项目开发的指导文件，任何修改需经用户同意。开发过程中的所有对话将记录在 `DEVELOPMENT_LOG.md`，遇到的错误将记录在 `ERROR_LOG.md`。
