"""
T07_sq100.py — Table 7（tab:sq100）核验
=======================================
对象：$f=100$ Hz 方形域精度，矩形 R4-R6（Cases 6-8）与楔形 W4-W6（Cases 12-14）
      **并排**排在同一张表里，9 列：

        Lx×Ly | No. R | Dataset | Sol | TL || No. W | Dataset | Sol | TL

R1 修订把原来的 Table 7（矩形）与 Table 8（楔形）合并为本表，故本脚本
覆盖两个几何；每半的判据与合并前逐条相同，只是列偏移不同。

核验链
  A. 源可追溯      xlsx / 6 份日志 / tex 环境
  B. best epoch    xlsx 列 == 日志自证
  C. 双渠道交叉    xlsx vs 日志同轮评估块
  D. 单频自洽      Overall == 100Hz，且 25/50/75Hz 为空
  E. 印刷值比对    两渠道 × 每格，几何尺寸另与 xlsx 的 Lx/Ly 比对
  F. 分组行        两个 Lx×Ly 标签与案例归属正确
  G. 位数一致      全部数值格 3 位小数
  H. 正文引用      4.3 节直接引用 + 派生倍数 8.676
  I. caption       best epoch 口径；caption 已把行与子图对应关系写明
"""
import os
import sys

import _boot  # noqa: F401
import _acctable as A
from common import metrics as M
from common import paths, registry, report, texparse as T

SLUG = "T07_sq100"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
NUMBER = 7

# 行标签 -> (几何, 案例, Dataset, Lx=Ly)
RECT = [(6, "R4", 128), (7, "R5", 256), (8, "R6", 512)]
WEDGE = [(12, "W4", 128), (13, "W5", 256), (14, "W6", 512)]
CASES = [c for c, _, _ in RECT] + [c for c, _, _ in WEDGE]

# 合并表列布局：0=Lx×Ly, 1=No.R, 2=Dataset, 3=Sol, 4=TL,
#                5=No.W, 6=Dataset, 7=Sol, 8=TL
NC = 9
BLOCKS = [("矩形", [c for c, _, _ in RECT], 1),
          ("楔形", [c for c, _, _ in WEDGE], 5)]

# 正文直接引用（4.3 节）
PROSE = [
    ("Case 6 Sol", "0.058", (6, "sol")),
    ("Case 6 TL", "0.444", (6, "tl")),
    ("Case 7 TL", "1.217", (7, "tl")),
    ("Case 8 TL", "3.852", (8, "tl")),
    ("Case 12 Sol", "0.100", (12, "sol")),
    ("Case 12 TL", "0.610", (12, "tl")),
    ("Case 13 TL", "0.930", (13, "tl")),
    ("Case 14 TL", "3.407", (14, "tl")),
]


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, str(NUMBER))
    xl = paths.xlsx_path("4.3")
    env, logs = A.check_sources(c, LABEL, xl, CASES,
                                "工作表1，best epoch 全测试集")

    printed, owner, rows = A.acc_blocks(env, NC, BLOCKS)
    c.section("2. 源可追溯性")
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 6-8 与 12-14",
            str(sorted(printed)))
    for no in CASES:
        want = "矩形" if no in [x for x, _, _ in RECT] else "楔形"
        c.check(owner.get(no) == want, f"Case {no} 落在{want}块",
                f"实得 {owner.get(no)}")

    xd, ld = A.check_epoch(c, xl, logs, CASES)

    c.section("4. 双渠道交叉验证（xlsx vs log）", ("量", "xlsx / log", "结论"))
    c.note("单频案例只在 100 Hz 上训练与评估，故只核 100Hz 与 Overall 两组。")
    for no in CASES:
        for g in ("Overall", 100):
            for q in ("sol", "tl"):
                a, b = xd[no][g][q], ld[no][g][q]
                ok = (a is not None and b is not None
                      and abs(a - b) <= max(1e-9, abs(a) * 2e-6))
                c.check(ok, f"Case {no} {'Avg.' if g == 'Overall' else '100Hz'} "
                            f"{q.upper()}", f"`{a!r}` / `{b!r}`")

    c.section("5. 单频自洽性")
    c.note("单频案例的 Overall 组必须等于 100Hz 组，且 25/50/75Hz 为空；"
           "两者任一不成立，说明该行被误当多频案例填了数。")
    for no in CASES:
        for q in ("sol", "tl"):
            a, b = xd[no]["Overall"][q], xd[no][100][q]
            c.check(a is not None and b is not None
                    and abs(a - b) <= max(1e-12, abs(a) * 1e-9),
                    f"Case {no} Avg. {q.upper()} == 100Hz {q.upper()}",
                    f"`{a!r}` == `{b!r}`")
        empty = [f for f in (25, 50, 75)
                 if xd[no][f]["sol"] is None and xd[no][f]["tl"] is None]
        c.check(empty == [25, 50, 75], f"Case {no} 25/50/75Hz 均为空",
                f"空的频率 {empty}")

    c.section("6. 印刷值比对（源值舍入到 3 位 vs tex）")
    c.note("列序：Lx×Ly, No., Dataset, Sol, TL（矩形块）| No., Dataset, Sol, TL"
           "（楔形块）。几何尺寸另与 xlsx 的 Lx/Ly 列比对——尺寸写错会让读者"
           "整行对错案例。")
    rows_x = M.load_sheet(xl)
    for name, spec, c0 in (("矩形", RECT, 2), ("楔形", WEDGE, 6)):
        for no, ds, lx in spec:
            c.check(printed[no][c0].strip() == ds, f"Case {no} Dataset 名",
                    f"tex `{printed[no][c0].strip()}`")
            xr = M.case_row(rows_x, no)
            c.check(int(xr[3]) == lx and int(xr[4]) == lx,
                    f"Case {no} Lx/Ly 与 xlsx 一致", f"xlsx `{lx}×{lx}`")
            for k, q in enumerate(("sol", "tl")):
                cell = printed[no][c0 + 1 + k]
                c.eq(f"Case {no} {q.upper()} (xlsx)", xd[no][100][q], cell)
                c.eq(f"Case {no} {q.upper()} (log)", ld[no][100][q], cell)

    c.section("7. 分组的 Lx×Ly 标签")
    c.note("行首的尺寸标签同时被两个几何块共用；写错会让楔形行被读成矩形尺寸。")
    geo = {}
    for r in rows:
        v = r[0].replace("$", "").replace("\\times", "x").strip()
        if r[1].strip().isdigit():
            geo[int(r[1])] = v
            geo[int(r[5].strip())] = v
    for no, _, lx in RECT + WEDGE:
        c.check(geo.get(no) == f"{lx}x{lx}", f"Case {no} 尺寸标签",
                f"tex `{geo.get(no)}` / 期望 `{lx}x{lx}`")

    A.check_decimals(c, printed, CASES, [3, 4, 7, 8])

    c.section("9. 正文引用精确性（4.3 节）")
    for desc, lit, (no, q) in PROSE:
        c0 = 3 if no in [x for x, _, _ in RECT] else 7
        cell = printed[no][c0 + (0 if q == "sol" else 1)]
        c.check(lit == cell, f"正文 {desc}", f"正文 `{lit}` / 表格 `{cell}`")
        c.eq(f"正文 {desc} ← xlsx 源", xd[no][100][q], lit)

    c.section("10. 正文派生倍数（印刷值口径）")
    c.note("倍数用表格印刷值相除：3.852/0.444 = 8.6756… → 正文写 8.676。"
           "若改用全精度源值会得 8.670，与正文不符；口径必须固定为印刷值。")
    tl6 = float(printed[6][4])
    tl8 = float(printed[8][4])
    r_print = tl8 / tl6
    c.check(f"{r_print:.3f}" == "8.676", "100Hz 矩形 512m/128m TL 倍数 = 8.676",
            f"印刷值口径 `{tl8}`/`{tl6}` = `{r_print:.6f}` → `{r_print:.3f}`")
    hits = T.sentences_with(r"factor of \$8\.676\$", T.tex_text())
    c.check(bool(hits), "正文该倍数可定位",
            f"tex 行 {T.line_of(hits[0][0])}" if hits else "未找到")

    c.section("11. 正文趋势断言")
    c.note("正文称单频方形域最准的是 128×128，且 TL 随域增大单调上升。")
    for name, spec in (("矩形", RECT), ("楔形", WEDGE)):
        nos = [n for n, _, _ in spec]
        tls = [xd[n][100]["tl"] for n in nos]
        sols = [xd[n][100]["sol"] for n in nos]
        c.check(tls == sorted(tls), f"{name} TL 随域尺度单调上升",
                " < ".join(f"{v:.3f}" for v in tls))
        c.check(sols == sorted(sols), f"{name} Sol 随域尺度单调上升",
                " < ".join(f"{v:.3f}" for v in sols))

    A.check_caption(c, LABEL, NUMBER, want_epoch="best epoch")

    c.section("13. caption 已写明行与子图的对应关系")
    c.note("两几何并排后，行序与 Fig. 的 (a)-(c)/(d)-(f) 必须由 caption 交代，"
           "否则读者无法把某一行对到某个子图。")
    cap = T.caption_of(LABEL) or ""
    c.check("panels (a)--(c) and (d)--(f)" in cap.replace("~", " "),
            "caption 写明行对应 (a)-(c)/(d)-(f)",
            "caption 含 `panels (a)--(c) and (d)--(f)`")
    c.check("fig:sq100" in cap, "caption 交叉引用 Fig.\\ref{fig:sq100}", "")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
