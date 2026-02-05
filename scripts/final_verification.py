"""
Kronos UI 最终验证报告
"""

import os
import sys

print("=" * 70)
print(" Kronos UI v2.0 - 最终验证报告")
print("=" * 70)
print()

# 设置UTF-8输出
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except:
        pass

# 添加路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'core'))
sys.path.insert(0, project_root)

print("[检查 1] 项目文件结构")
required_files = [
    'core/app.py',
    'core/config_loader.py',
    'core/logger.py',
    'core/data_fetcher.py',
    'core/model_cache.py',
    'core/model/__init__.py',
    'core/model/kronos.py',
    'core/model/module.py',
    'config/config.json',
    'config/models.json',
    'templates/index.html',
    'requirements.txt'
]

all_ok = True
for file in required_files:
    path = os.path.join(project_root, file)
    if os.path.exists(path):
        print(f"  [OK] {file}")
    else:
        print(f"  [MISSING] {file}")
        all_ok = False

print()

if all_ok:
    print("[检查 2] 模块导入")
    try:
        from core.model import Kronos, KronosTokenizer, KronosPredictor
        from core.config_loader import get_config
        from core.logger import setup_logger
        from core.data_fetcher import MarketDataFetcher
        from core.model_cache import get_model_cache
        print("  [OK] 所有核心模块导入成功")
    except ImportError as e:
        print(f"  [FAIL] 模块导入失败: {e}")
        all_ok = False

    print()

    print("[检查 3] 模型加载测试")
    try:
        # 测试 from_pretrained 方法
        tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
        model = Kronos.from_pretrained("NeoQuasar/Kronos-mini")
        print("  [OK] 模型 from_pretrained 方法正常工作")
    except Exception as e:
        print(f"  [FAIL] 模型加载失败: {e}")
        all_ok = False

    print()

    print("[检查 4] 配置文件")
    try:
        config = get_config()
        version = config.get('app.version')
        print(f"  [OK] 配置文件正常 (版本: {version})")
    except Exception as e:
        print(f"  [FAIL] 配置文件错误: {e}")
        all_ok = False

    print()

    print("[检查 5] 数据源")
    try:
        fetcher = MarketDataFetcher()
        if fetcher.ak_available:
            print("  [OK] Akshare 可用")
        if fetcher.bs is not None:
            print("  [OK] Baostock 可用")
        if fetcher.ts is not None:
            print("  [OK] Tushare 可用")
    except Exception as e:
        print(f"  [WARN] 数据源检查跳过: {e}")

    print()

print("=" * 70)
if all_ok:
    print(" 状态: 所有检查通过! 项目已就绪。")
    print()
    print("启动方式:")
    print("  1. Windows: 双击 scripts\\start.bat")
    print("  2. Linux/Mac: 运行 bash scripts/start.sh")
    print()
    print("浏览器访问: http://localhost:7070")
else:
    print("状态: 存在问题，请检查上述错误。")
print("=" * 70)
