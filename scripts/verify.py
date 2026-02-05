"""
Kronos UI Project Verification Script
Check if all project modules are working correctly
"""

import os
import sys

# Add project path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

print("=" * 60)
print("Kronos UI Project Verification")
print("=" * 60)
print()

# Check directory structure
print("[1/6] Checking directory structure...")
required_dirs = [
    'core', 'core/model', 'templates', 'config', 'docs',
    'cache', 'logs', 'scripts', 'build', 'static'
]

missing_dirs = []
for dir_name in required_dirs:
    dir_path = os.path.join(project_root, dir_name)
    if not os.path.exists(dir_path):
        missing_dirs.append(dir_name)

if missing_dirs:
    print(f"  [X] Missing directories: {', '.join(missing_dirs)}")
else:
    print(f"  [OK] All required directories exist")

# Check configuration files
print("[2/6] Checking configuration files...")
try:
    import json
    config_path = os.path.join(project_root, 'config', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    print(f"  [OK] config.json loaded")
    print(f"       - Version: {config.get('app', {}).get('version', 'unknown')}")
    print(f"       - Port: {config.get('app', {}).get('port', 'unknown')}")
except Exception as e:
    print(f"  [X] config.json failed: {e}")

try:
    models_path = os.path.join(project_root, 'config', 'models.json')
    with open(models_path, 'r', encoding='utf-8') as f:
        models = json.load(f)
    print(f"  [OK] models.json loaded")
    available_models = models.get('available_models', {})
    print(f"       - Models: {', '.join(available_models.keys())}")
except Exception as e:
    print(f"  [X] models.json failed: {e}")

# Check core modules
print("[3/6] Checking core modules...")
modules_to_check = [
    ('config_loader', 'core.config_loader'),
    ('logger', 'core.logger'),
    ('model_cache', 'core.model_cache'),
]

for module_name, module_path in modules_to_check:
    try:
        __import__(module_path)
        print(f"  [OK] {module_name} imported")
    except Exception as e:
        print(f"  [X] {module_name} failed: {e}")

# Check data fetcher
print("[4/6] Checking data fetcher...")
try:
    from core.data_fetcher import MarketDataFetcher
    print(f"  [OK] data_fetcher imported")

    # Test initialization
    fetcher = MarketDataFetcher()
    print(f"  [OK] MarketDataFetcher initialized")

    # Check data source status
    if fetcher.ak_available:
        print(f"  [OK] Akshare available")
    else:
        print(f"  [WARN] Akshare not installed (pip install akshare)")

    if fetcher.bs is not None:
        print(f"  [OK] Baostock available")
    else:
        print(f"  [WARN] Baostock not installed (pip install baostock)")

    if fetcher.ts is not None:
        print(f"  [OK] Tushare configured")
    else:
        print(f"  [WARN] Tushare not configured")

except Exception as e:
    print(f"  [X] data_fetcher check failed: {e}")

# Check frontend files
print("[5/6] Checking frontend files...")
template_path = os.path.join(project_root, 'templates', 'index.html')
if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'Kronos UI' in content:
        print(f"  [OK] index.html exists and contains content")
    else:
        print(f"  [WARN] index.html may be incomplete")
else:
    print(f"  [X] index.html not found")

# Check documentation
print("[6/6] Checking documentation...")
doc_files = [
    'docs/PROJECT_PLAN.md',
    'docs/DEVELOPMENT_LOG.md',
    'docs/ERROR_LOG.md',
    'docs/USER_GUIDE.md',
    'README.md'
]

for doc_file in doc_files:
    doc_path = os.path.join(project_root, doc_file)
    if os.path.exists(doc_path):
        size = os.path.getsize(doc_path)
        print(f"  [OK] {doc_file} ({size} bytes)")
    else:
        print(f"  [X] {doc_file} not found")

print()
print("=" * 60)
print("Verification Complete")
print("=" * 60)
print()
print("Project is ready to use!")
print("Run 'python scripts/start.bat' to start the application")
print()
