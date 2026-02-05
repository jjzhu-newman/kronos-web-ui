# 贡献指南

感谢您对 Kronos Web UI 项目的关注！我们欢迎任何形式的贡献。

## 🤝 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议：

1. 检查 [Issues](https://github.com/jjzhu-newman/kronos-web-ui/issues) 是否已存在相同问题
2. 如果没有，创建新的 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 系统环境信息（OS、Python 版本等）
   - 相关日志或截图

### 提交代码

#### 开发环境设置

1. **Fork 仓库**
   ```bash
   # 在 GitHub 上点击 Fork 按钮
   ```

2. **克隆到本地**
   ```bash
   git clone https://github.com/YOUR_USERNAME/kronos-web-ui.git
   cd kronos-web-ui
   ```

3. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

4. **安装开发依赖**
   ```bash
   pip install -r requirements.txt
   pip install flake8 black pytest  # 开发工具
   ```

5. **添加上游仓库**
   ```bash
   git remote add upstream https://github.com/jjzhu-newman/kronos-web-ui.git
   ```

#### 开发流程

1. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

2. **编写代码**
   - 遵循现有代码风格
   - 添加必要的注释
   - 更新相关文档

3. **测试您的更改**
   ```bash
   # 运行应用
   python core/app.py

   # 测试核心功能
   python -c "from core.config_loader import get_config"
   python -c "from core.logger import setup_logger"
   ```

4. **代码格式化**（可选但推荐）
   ```bash
   # 使用 Black 格式化代码
   black .

   # 使用 Flake8 检查代码质量
   flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   提交信息格式：
   - `feat:` 新功能
   - `fix:` 修复 bug
   - `docs:` 文档更新
   - `style:` 代码格式调整
   - `refactor:` 代码重构
   - `test:` 测试相关
   - `chore:` 构建/工具相关

6. **推送到您的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**
   - 访问原仓库
   - 点击 "New Pull Request"
   - 选择您的分支
   - 填写 PR 描述：
     - 简短描述更改内容
     - 关联相关 Issue（如 `Fixes #123`）
     - 说明测试情况
     - 添加截图（如果适用）

#### Pull Request 检查清单

在提交 PR 前，请确保：

- [ ] 代码遵循项目风格指南
- [ ] 已添加必要的文档和注释
- [ ] 已测试所有更改
- [ ] 没有引入新的警告
- [ ] 提交信息清晰明确
- [ ] PR 描述详细完整

## 📋 代码规范

### Python 代码风格

- 遵循 PEP 8 规范
- 使用有意义的变量和函数名
- 函数添加 docstring
- 复杂逻辑添加注释

**示例**：
```python
def fetch_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    获取股票历史数据

    Args:
        symbol: 股票代码
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)

    Returns:
        包含股票数据的 DataFrame

    Raises:
        ValueError: 日期格式错误
        ConnectionError: 网络连接失败
    """
    # 实现代码...
    pass
```

### 前端代码风格

- 使用 2 空格缩进
- 使用单引号优先
- 函数添加 JSDoc 注释
- 事件处理函数命名以 `handle` 开头

**示例**：
```javascript
/**
 * 处理模型加载按钮点击事件
 * @param {string} modelKey - 模型标识符
 * @param {string} device - 设备类型 (cpu/cuda/mps)
 */
async function handleLoadModel(modelKey, device) {
    try {
        // 实现代码...
    } catch (error) {
        console.error('模型加载失败:', error);
    }
}
```

### Git 提交信息格式

使用 Conventional Commits 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型**：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**：
```
feat(data-fetcher): add support for crypto data from Binance API

- Implement Binance API integration
- Add error handling for rate limiting
- Update documentation

Closes #42
```

## 🎨 项目结构

```
kronos-web-ui/
├── core/                   # 核心模块
│   ├── model/             # Kronos 模型实现
│   ├── app.py             # Flask 主应用
│   ├── config_loader.py   # 配置加载
│   ├── data_fetcher.py    # 数据获取
│   ├── logger.py          # 日志系统
│   └── model_cache.py     # 模型缓存
├── templates/             # 前端模板
│   └── index.html        # 主界面
├── config/               # 配置文件
├── docs/                 # 文档
├── scripts/              # 工具脚本
└── tests/                # 测试文件（待添加）
```

## 🐛 调试技巧

### 启用调试日志

```python
# 在 core/app.py 中设置
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 常见开发问题

1. **模块导入错误**
   ```bash
   # 确保项目根目录在 PYTHONPATH
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **端口占用**
   ```bash
   # 修改 config/config.json 中的端口
   "port": 7071
   ```

3. **模型缓存问题**
   ```bash
   # 清除缓存
   rm -rf cache/models/*
   ```

## 📖 相关资源

- [Flask 文档](https://flask.palletsprojects.com/)
- [PyTorch 文档](https://pytorch.org/docs/)
- [Lightweight Charts](https://www.tradingview.com/lightweight-charts/)
- [项目开发日志](docs/DEVELOPMENT_LOG.md)

## 💬 讨论和交流

- 💬 [Discussions](https://github.com/jjzhu-newman/kronos-web-ui/discussions) - 技术讨论
- 🐛 [Issues](https://github.com/jjzhu-newman/kronos-web-ui/issues) - Bug 报告
- 📧 Email: your-email@example.com

## 📄 许可证

通过贡献代码，您同意您的贡献将在 [MIT 许可证](LICENSE) 下发布。

## 🙏 致谢

感谢所有贡献者！您的贡献让这个项目变得更好。

---

**有问题？** 查看 [FAQ](docs/USER_GUIDE.md) 或创建 [Discussion](https://github.com/jjzhu-newman/kronos-web-ui/discussions)
