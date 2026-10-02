"""_tblcommon.py — 表数据打印脚本的共享引导与格式化。

设计要点
--------
这些 table*.py 脚本不自己解析 xlsx，而是直接复用 ch4_validation/common/ 里的
加载器（metrics.xlsx_case 等）。核验套件用的是同一批函数，所以打印出来的数值
与 verify.py 的取数口径**必然一致**，不会各写一套而慢慢漂移。

用法
----
    python table04_05_ideal.py            # 打印 Table 4 与 Table 5
    python table04_05_ideal.py --tex      # 顺便打印 tex 行，便于逐字符对照

需要先设好环境变量（与 verify.py 相同）：
    CH4_RAWROOT   Raw_Experimental_Data 的父目录
    CH4_TEXDIR    编译好的论文目录（含 .aux，仅 --tex 需要）
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_PKG = os.path.join(_REPO, "ch4_validation")
if _PKG not in sys.path:
    sys.path.insert(0, _PKG)

_SCR = os.path.join(_PKG, "scripts")
if _SCR not in sys.path:
    sys.path.insert(0, _SCR)

from common import metrics as M          # noqa: E402
from common import paths, registry       # noqa: E402

FREQS = M.FREQS


def checker_module(slug):
    """导入核验脚本模块（如 "T20_runtime"），复用它的 loader。

    这样打印脚本与 verify.py 走的是同一个取数函数，两边不会各写一套解析而
    慢慢漂移——这是这些脚本可信的前提。
    """
    import importlib
    return importlib.import_module(slug)


def want_tex():
    return "--tex" in sys.argv


def head(label, title):
    """表头：论文里的表号 + label + 一句话对象说明。"""
    try:
        from common import texparse as T
        num = T.number_of(label)
    except Exception:
        num = None
    tag = f"Table {num}" if num else "Table ?"
    print()
    print("=" * 78)
    print(f"{tag}  [{label}]  {title}")
    print("=" * 78)


def row(cells, widths):
    print("  ".join(str(c).ljust(w) for c, w in zip(cells, widths)))


def rule(widths, ch="-"):
    print("  ".join(ch * w for w in widths))


def f3(v):
    """3 位小数，与多数表的印刷位数一致；None 显示为 —。"""
    return "—" if v is None else f"{v:.3f}"


def f2(v):
    return "—" if v is None else f"{v:.2f}"


def tex_rows(label):
    """从 tex 里抓该表环境的数据行（已清洗单元格），用于逐字符对照。"""
    from common import texparse as T
    env = T.table_env(label)
    if not env:
        return []
    return T.data_rows(env)


def note(msg):
    print(f"  · {msg}")
