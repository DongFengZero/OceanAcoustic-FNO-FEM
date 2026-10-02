"""_acctable.py — 精度表的通用打印器。

第四章大多数表是同一形状：若干案例 × (Avg. + 25/50/75/100 Hz) × (Sol, TL)。
Sol 单位 1e-6，TL 单位 dB，印刷 3 位小数。这里只写一遍，各 table*.py 传入
案例清单即可，省得每张表重抄一遍格式。

取数一律走 common/metrics.py 的 xlsx_case()——与 verify.py 同一个函数。
"""
import _tblcommon as K


def print_acc(label, title, sec, cases, note_lines=()):
    """cases: {case_no: 行标签}，按给定顺序打印。"""
    K.head(label, title)
    xl = K.paths.xlsx_path(sec)
    K.note(f"xlsx: {K.paths.rel(xl)}")
    K.note("取数：common/metrics.py 的 xlsx_case()（与 verify.py 同源）")
    for ln in note_lines:
        K.note(ln)

    w = [22, 6] + [9] * 10
    hdr = ["Case / label", "best"]
    for g in ("Avg.",) + tuple(f"{f}Hz" for f in K.FREQS):
        hdr += [f"{g} Sol", f"{g} TL"]
    K.row(hdr, w)
    K.rule(w)
    for no, lab in cases.items():
        d = K.M.xlsx_case(xl, no)
        cells = [f"{no}  {lab}", str(d.get("best_epoch") or "—")]
        for g in ("Overall",) + tuple(K.FREQS):
            b = d.get(g) or {}
            cells += [K.f3(b.get("sol")), K.f3(b.get("tl"))]
        K.row(cells, w)
    K.rule(w)
    K.note("Sol 单位 1e-6（已乘）；TL 单位 dB；论文印刷 3 位小数")

    if K.want_tex():
        print("\n  tex 数据行（逐字符对照）：")
        for r in K.tex_rows(label):
            print("   ", " | ".join(r))
