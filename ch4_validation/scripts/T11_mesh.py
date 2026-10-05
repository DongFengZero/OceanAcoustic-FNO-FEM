"""
T11_mesh.py — Table 11（tab:mesh）核验
======================================
对象：网格无关性，$f=100$ Hz，矩形 R4/R7/R8（$\Delta=1.00/0.50/0.25$ m，Cases 33-35）
      与楔形 W4/W7/W8（Cases 36-38）**并排**在同一张表里，9 列：

        Δ (m) | No. R | Dataset | Sol | TL || No. W | Dataset | Sol | TL

R1 修订把原来的 mesh-rect 与 mesh-wedge 两张表合并为本表，故本脚本覆盖两个
几何；每半的判据与合并前逐条相同，只是列偏移不同。

核验链
  A. 源可追溯      xlsx / 6 份日志 / tex 表体
  B. best epoch    xlsx 列 == 日志自证
  C. 双渠道交叉    xlsx vs 日志同轮评估块（只核 100Hz）
  D. 印刷值比对    两渠道 × 每格；Dataset 名与 Δ 标签另核
  E. Δ 列与案例归属 三档分辨率与两个几何块的对应
  F. 位数一致      全部数值格 3 位小数
  G. 复用关系      4.6 最粗一档即 4.3 的单频案例（33≡6、36≡12）
  H. 正文引用      4.6 节直接引用 + TL 随细化不升的断言
  I. caption       best epoch 口径；行与子图 (a)-(c)/(d)-(f) 的对应
"""
import os
import sys

import _boot  # noqa: F401
import _acctable as A
from common import metrics as M
from common import paths, registry, report, texparse as T

SLUG = "T11_mesh"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
NUMBER = 11

# 行标签 -> (几何, 案例, Dataset, Δ)
RECT = [(33, "R4", "1.00"), (34, "R7", "0.50"), (35, "R8", "0.25")]
WEDGE = [(36, "W4", "1.00"), (37, "W7", "0.50"), (38, "W8", "0.25")]
CASES = [c for c, _, _ in RECT] + [c for c, _, _ in WEDGE]

# 合并表列布局：0=Δ, 1=No.R, 2=Dataset, 3=Sol, 4=TL, 5=No.W, 6=Dataset, 7=Sol, 8=TL
NC = 9
BLOCKS = [("矩形", [c for c, _, _ in RECT], 1),
          ("楔形", [c for c, _, _ in WEDGE], 5)]

PROSE = [
    ("Case 33 (Δ=1.00) Sol", "0.058", (33, "sol")),
    ("Case 35 (Δ=0.25) Sol", "0.287", (35, "sol")),
    ("Case 36 (Δ=1.00) Sol", "0.100", (36, "sol")),
    ("Case 38 (Δ=0.25) Sol", "0.326", (38, "sol")),
    ("Case 33 (Δ=1.00) TL", "0.444", (33, "tl")),
    ("Case 34 (Δ=0.50) TL", "0.384", (34, "tl")),
    ("Case 35 (Δ=0.25) TL", "0.393", (35, "tl")),
    ("Case 36 (Δ=1.00) TL", "0.610", (36, "tl")),
    ("Case 37 (Δ=0.50) TL", "0.361", (37, "tl")),
    ("Case 38 (Δ=0.25) TL", "0.311", (38, "tl")),
]

# 4.6 复用关系：(4.6 案例, 4.3 案例)
REUSE = [(33, 6), (36, 12)]


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, str(NUMBER))
    xl = paths.xlsx_path("4.6")
    env, logs = A.check_sources(c, LABEL, xl, CASES,
                                "工作表1，best epoch 全测试集")
    c.source("复用比对 xlsx", paths.xlsx_path("4.3"),
             "4.3 节汇总，用于确认 Case 33≡6、36≡12")

    printed, owner, rows = A.acc_blocks(env, NC, BLOCKS)
    c.section("2. 源可追溯性")
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 33-35 与 36-38",
            str(sorted(printed)))
    for no in CASES:
        want = "矩形" if no in [x for x, _, _ in RECT] else "楔形"
        c.check(owner.get(no) == want, f"Case {no} 落在{want}块",
                f"实得 {owner.get(no)}")

    xd, ld = A.check_epoch(c, xl, logs, CASES)

    c.section("4. 双渠道交叉验证（xlsx vs log）", ("量", "xlsx / log", "结论"))
    c.note("本表只有 100 Hz 一档，故只核 100Hz 组。")
    for no in CASES:
        for q in ("sol", "tl"):
            a, b = xd[no][100][q], ld[no][100][q]
            ok = (a is not None and b is not None
                  and abs(a - b) <= max(1e-9, abs(a) * 2e-6))
            c.check(ok, f"Case {no} 100Hz {q.upper()}", f"`{a!r}` / `{b!r}`")

    c.section("5. 印刷值比对（源值舍入到 3 位 vs tex）")
    c.note("列序：Δ, No., Dataset, Sol, TL（矩形块）| No., Dataset, Sol, TL"
           "（楔形块）。")
    for name, spec, c0 in (("矩形", RECT, 2), ("楔形", WEDGE, 6)):
        for no, ds, _ in spec:
            c.check(printed[no][c0].strip() == ds, f"Case {no} Dataset 名",
                    f"tex `{printed[no][c0].strip()}`")
            for k, q in enumerate(("sol", "tl")):
                cell = printed[no][c0 + 1 + k]
                c.eq(f"Case {no} {q.upper()} (xlsx)", xd[no][100][q], cell)
                c.eq(f"Case {no} {q.upper()} (log)", ld[no][100][q], cell)

    c.section("6. Δ 列与案例归属")
    c.note("行首的 Δ 标签同时被两个几何块共用；写错会让楔形行被读成矩形分辨率。")
    delta = {}
    for r in rows:
        v = r[0].replace("$", "").strip()
        if r[1].strip().isdigit():
            delta[int(r[1])] = v
            delta[int(r[5].strip())] = v
    for no, _, d in RECT + WEDGE:
        c.check(delta.get(no) == d, f"Case {no} Δ 标签",
                f"tex `{delta.get(no)}` / 期望 `{d}`")

    A.check_decimals(c, printed, CASES, [3, 4, 7, 8])

    c.section("8. 与 4.3 节的复用关系")
    c.note("4.6 网格研究的最粗一档就是 4.3 的单频案例：Case 33 复用 Case 6、"
           "Case 36 复用 Case 12。判定不看三位小数（那可能是巧合），"
           "而要求 best epoch 与全精度值都一致，才算同一次运行。")
    xl3 = paths.xlsx_path("4.3")
    for a6, a3 in REUSE:
        d6, d3 = M.xlsx_case(xl, a6), M.xlsx_case(xl3, a3)
        c.check(d6["best_epoch"] == d3["best_epoch"],
                f"Case {a6} 与 Case {a3} best epoch 相同",
                f"`{d6['best_epoch']}` == `{d3['best_epoch']}`")
        for q in ("sol", "tl"):
            va, vb = d6[100][q], d3[100][q]
            c.check(va is not None and vb is not None and va == vb,
                    f"Case {a6} 与 Case {a3} {q.upper()} 全精度相同",
                    f"`{va!r}` == `{vb!r}`")

    c.section("9. 正文引用精确性（4.6 节）")
    for desc, lit, (no, q) in PROSE:
        c0 = 3 if no in [x for x, _, _ in RECT] else 7
        cell = printed[no][c0 + (0 if q == "sol" else 1)]
        c.check(lit == cell, f"正文 {desc}", f"正文 `{lit}` / 表格 `{cell}`")
        c.eq(f"正文 {desc} ← xlsx 源", xd[no][100][q], lit)

    c.section("10. 正文趋势断言")
    c.note("正文称解误差随细化温和上升，而 TL（物理相关量）不随细化变差。")
    for name, spec in (("矩形", RECT), ("楔形", WEDGE)):
        nos = [n for n, _, _ in spec]
        sols = [xd[n][100]["sol"] for n in nos]
        tls = [xd[n][100]["tl"] for n in nos]
        c.check(sols == sorted(sols), f"{name} Sol 随细化上升",
                " < ".join(f"{v:.3f}" for v in sols))
        c.check(max(tls) < 0.65, f"{name} TL 全部低于 0.65 dB",
                " / ".join(f"{v:.3f}" for v in tls))
        c.check(tls[-1] <= tls[0], f"{name} 最细网格 TL 不劣于最粗",
                f"`{tls[0]:.3f}` → `{tls[-1]:.3f}`")

    A.check_caption(c, LABEL, NUMBER, want_epoch="best epoch")

    c.section("12. caption 已写明行与子图的对应关系")
    cap = T.caption_of(LABEL) or ""
    c.check("panels (a)--(c) and (d)--(f)" in cap.replace("~", " "),
            "caption 写明行对应 (a)-(c)/(d)-(f)",
            "caption 含 `panels (a)--(c) and (d)--(f)`")
    c.check("fig:mesh" in cap, "caption 交叉引用 Fig.\\ref{fig:mesh}", "")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
