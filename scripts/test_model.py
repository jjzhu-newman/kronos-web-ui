"""
测试模型加载
"""

import os
import sys

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'core'))

from core.model import Kronos, KronosTokenizer

print("Testing model loading...")
print()

try:
    # Test loading tokenizer
    print("[1/2] Loading KronosTokenizer...")
    tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
    print(f"  SUCCESS: Tokenizer loaded")
    print(f"  Type: {type(tokenizer)}")
    print()

    # Test loading model (smallest model)
    print("[2/2] Loading Kronos-mini...")
    model = Kronos.from_pretrained("NeoQuasar/Kronos-mini")
    print(f"  SUCCESS: Model loaded")
    print(f"  Type: {type(model)}")
    print()

    print("=" * 50)
    print("All tests passed!")
    print("=" * 50)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
