"""_boot.py — 让 scripts/ 下的脚本无论 cwd 在哪都能 import common。

每个核验脚本第一行 `import _boot`，之后 `from common import ...` 即可。
不用相对 import，是为了让每个脚本都能被单独 `python scripts/Txx.py` 直接跑。
"""
import os
import sys

_PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # ch4_validation/
if _PKG not in sys.path:
    sys.path.insert(0, _PKG)

# Windows 控制台默认 GBK，报告里的中文/箭头会炸；统一改 UTF-8。
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass
