# Kronos Web UI - 快速使用指南

## 📦 可移动版本说明

这是一个完整的可移动版本，可以拷贝到任何电脑上使用。

---

## 🚀 快速开始（3 步）

### 步骤 1: 解压文件

将压缩包解压到任意目录，例如：
- Windows: `D:\Kronos_UI`
- Linux/Mac: `/home/user/Kronos_UI`

### 步骤 2: 安装依赖（仅首次）

**Windows**:
```cmd
# 双击运行
scripts\install_all.bat

# 或命令行
pip install -r requirements.txt
```

**Linux/Mac**:
```bash
pip3 install -r requirements.txt
```

### 步骤 3: 启动应用

**Windows**:
- 双击运行：`scripts\start.bat`

**Linux/Mac**:
```bash
bash scripts/start.sh
```

浏览器会自动打开：**http://localhost:7070**

---

## ⚙️ 系统要求

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 10/11, Linux, macOS |
| **Python** | 3.10 - 3.13（推荐 3.13） |
| **内存** | 4GB+ |
| **硬盘** | 2GB+ （不含模型） |

**GPU 加速**（可选）:
- NVIDIA 显卡：GTX 1060 或更新
- 需要 Python 3.13

---

## 📖 首次使用

1. **打开浏览器** → http://localhost:7070

2. **选择模型**
   - 推荐使用 **Kronos-small**（平衡速度和精度）

3. **选择设备**
   - 有 NVIDIA 显卡：选择 **CUDA**
   - 其他情况：选择 **CPU**

4. **点击"加载模型"**
   - 首次需要下载模型（约 100MB）
   - 以后会自动使用缓存

5. **输入股票代码**
   - A 股：`601212`（白银有色）
   - 美股：`AAPL`
   - 加密货币：`BTCUSDT`

6. **点击"预测"** → 等待结果

---

## 🎯 快速提示

### 常用操作

| 操作 | 说明 |
|------|------|
| **加载模型** | 每次启动应用只需加载一次 |
| **切换股票** | 输入新代码，直接预测 |
| **调整参数** | Temperature: 0.8-1.2, Top-P: 0.9 |
| **导出数据** | 点击"导出"按钮 |

### 推荐设置

**稳健投资**:
- Temperature: 0.8
- Top-P: 0.9
- Lookback: 400

**趋势判断**:
- Temperature: 1.2
- Top-P: 0.95
- Lookback: 400

---

## 🐛 常见问题

### Q1: 启动失败

**错误**: `ModuleNotFoundError`

**解决**:
```bash
# 重新安装依赖
pip install -r requirements.txt
```

### Q2: 端口被占用

**错误**: 端口 7070 已被使用

**解决**:
修改 `config/config.json`:
```json
{
  "app": {
    "port": 7071  // 改成其他端口
  }
}
```

### Q3: CUDA 不可用

**错误**: `CUDA available: False`

**解决**:
- 继续使用 CPU 模式（完全可用）
- 或安装 CUDA 版本（需要 Python 3.13）

### Q4: 预测失败

**错误**: `所有数据源均无法获取数据`

**解决**:
- 检查股票代码格式（A 股用纯数字）
- 检查网络连接
- 等待几分钟后重试

---

## 📚 更多文档

- **完整指南**: [README.md](README.md)
- **用户手册**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **CUDA 设置**: [docs/CUDA_GUIDE.md](docs/CUDA_GUIDE.md)
- **错误解决**: [docs/ERROR_LOG.md](docs/ERROR_LOG.md)

---

## 💡 使用技巧

### 1. 模型选择

| 模型 | 参数量 | 速度 | 适用场景 |
|------|--------|------|----------|
| **Kronos-mini** | 4.1M | 最快 | 快速测试 |
| **Kronos-small** | 24.7M | 平衡 | **日常使用** |
| **Kronos-base** | 102.3M | 最精准 | 深度分析 |

### 2. 设备选择

- **CPU**: 完全可用，预测 30-60 秒
- **CUDA**: 推荐，预测 5-10 秒（5-10x 加速）

### 3. 参数调整

**Temperature** (温度):
- `0.6-0.8`: 保守，适合稳定市场
- `1.0`: 默认，平衡
- `1.2-1.5`: 激进，适合波动行情

**Top-P** (核采样):
- `0.8-0.9`: 集中，确定性高
- `0.9-0.95`: 平衡
- `1.0`: 分散，不确定性高

---

## 🔄 更新和升级

### 检查版本

查看 `config/config.json` 中的版本号。

### 获取更新

访问 GitHub:
```
https://github.com/jjzhu-newman/kronos-web-ui
```

下载最新版本并替换文件。

---

## 📞 技术支持

- **GitHub**: https://github.com/jjzhu-newman/kronos-web-ui
- **问题反馈**: https://github.com/jjzhu-newman/kronos-web-ui/issues
- **使用讨论**: https://github.com/jjzhu-newman/kronos-web-ui/discussions

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

**开始使用吧！祝您投资顺利！** 🚀📈
