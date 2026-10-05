"""_tblcommon.py — 表数据打印脚本的共享引导与格式化。

设计要点
--------
这些 table*.py 脚本不自己解析 xlsx，而是直接复用 ch4_validation/common/ 里的
加载器（metrics.xlsx_case 等）。核验套件用的是同一批函数，所以打印出来的数值
与 verify.py 的取数口径**必然一致**，不会各写一套而慢慢漂移。

用法
----
    python table04_ideal.py               # 打印 Table 4
    python table04_ideal.py --tex         # 顺便打印 tex 行，便于逐字符对照

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
    """导入核验脚本模块（如 "T13_runtime"），复用它的 loader。

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


# 浮动体里一张表可能用 tabular 或 tabular*（论文两者都有），统一成一种切法。
_TAB_BEGIN = r"\\begin\{tabular\*?\}"
_TAB_END = r"\\end\{tabular\*?\}"


def tex_rows_of(i, label):
    """该浮动体里第 i 张（0 起）tabular 的数据行。

    R1 把若干对表并进同一浮动体：一个 \\label 下挂两张 tabular，而
    texparse.tabular_body() 只切到第一个 \\end{tabular}，所以第二张取不到。
    本函数按 \\begin{tabular[*]} 出现顺序切开，调用方按索引取自己那半。
    """
    import re
    from common import texparse as T
    env = T.table_env(label)
    if not env:
        return []
    parts = re.split(_TAB_BEGIN, env)[1:]
    if i >= len(parts):
        return []
    seg = re.split(_TAB_END, parts[i])[0]
    # tabular* 的宽度参数与列格式在同一行，data_rows 会把它们当第一行，故去掉
    seg = re.sub(r"^[^\n]*\n", "", seg, count=1)
    return T.data_rows(seg)


def n_tabulars(label):
    """该 label 所在浮动体里有几张 tabular（打印脚本据此选择取哪张）。"""
    import re
    from common import texparse as T
    env = T.table_env(label)
    return len(re.findall(_TAB_BEGIN, env)) if env else 0


def tex_rows(label):
    """该 label 的浮动体里**第一张** tabular 的数据行。

    多数表一个 label 只有一张 tabular（R1 的"合并"是把矩形/楔形并成一张表的
    左右两个列组，不是两张表），此时本函数即整表。确实是两张的（tab:runtime
    的 (a)/(b)）用 tex_rows_of(i, label) 指明第 i 张。
    """
    return tex_rows_of(0, label)


def note(msg):
    print(f"  · {msg}")
