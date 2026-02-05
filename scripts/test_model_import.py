"""
测试模型导入和加载
"""

import os
import sys

# 设置UTF-8编码输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'core'))

print("=" * 60)
print("Kronos UI 模型测试")
print("=" * 60)
print()

# Test 1: 检查文件是否存在
print("[测试 1] 检查模型文件...")
model_files = [
    'core/model/__init__.py',
    'core/model/kronos.py',
    'core/model/module.py'
]

for file in model_files:
    path = os.path.join(project_root, file)
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    status = "OK" if exists else "FAIL"
    print(f"  {status}: {file} ({size} bytes)")

print()

# Test 2: 导入模块
print("[测试 2] 导入模型模块...")
try:
    from core.model import Kronos, KronosTokenizer, KronosPredictor
    print("  OK: 模型导入成功")
except ImportError as e:
    print(f"  FAIL: 模型导入失败 - {e}")
    sys.exit(1)

print()

# Test 3: 测试 from_pretrained 方法
print("[测试 3] 测试 from_pretrained 方法...")
print("  注意: 这需要从网络下载模型，可能需要几分钟")
print()

try:
    # 加载最小的模型进行测试
    print("  加载 KronosTokenizer (从缓存或下载)...")
    tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
    print(f"  OK: Tokenizer 类型 = {type(tokenizer)}")
    print(f"  OK: Tokenizer = {tokenizer}")

    print()
    print("  加载 Kronos-mini 模型 (从缓存或下载)...")
    model = Kronos.from_pretrained("NeoQuasar/Kronos-mini")
    print(f"  OK: 模型类型 = {type(model)}")
    print(f"  OK: 模型 = {model}")

    print()
    print("=" * 60)
    print("所有测试通过!")
    print("=" * 60)

except Exception as e:
    print(f"  FAIL: {e}")
    print()
    print("详细错误信息:")
    import traceback
    traceback.print_exc()
    print()
    print("=" * 60)
    print("测试失败!")
    print("=" * 60)
