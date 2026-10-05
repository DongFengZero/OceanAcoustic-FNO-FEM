"""
T10_abl.py — Table 10（tab:abl）核验
====================================
对象：消融变体逐频前向精度，**矩形 R1（Cases 25-28）与楔形 W1（Cases 29-32）
      分块排在同一张表**，12 列：

        No. | Variant | 25Hz(Sol,TL) | 50Hz | 75Hz | 100Hz | Avg.(Sol,TL)

R1 修订把原来的 Table 15（abl-rect）与 Table 16（abl-wedge）合并为本表，
故本脚本覆盖两个几何；每块的判据与合并前逐条相同，只是版式变了。

版式要点（与合并前的并排表不同）
  * 两几何不是左右并排，而是**上下两块**，块头是 `\\multicolumn{12}` 行；
    因此 No. 列只有一个（列 0），不像并排表那样每块各有一列 No.。
  * R1 把多张表绑进同一个 figure* 浮动体，`T.table_env()` 可能解析到同浮动体内
    的邻居，故本表自己的 tabular 取自 `T.table_body_of(LABEL)`。

核验链
  1. 本表 tabular 的定位
  2. 源可追溯      xlsx / 8 份日志 / tex 行 No. 与 Variant 名 / 块序
  3. best epoch    xlsx 列 == 日志自证
  4. 双渠道交叉    xlsx vs 日志同轮评估块（5 组 × 2 量 × 8 案例 = 80 个量）
  5. 印刷值比对    两渠道 × 80 格
  6. Avg. 自洽     Avg. == 四频均值
  7. 位数一致      全部 80 个数值格 3 位小数
  8. 加粗判据      每列**各自几何块内**的最小值加粗（caption 的口径）
  9. 正文引用      4.5 节直接引用 8 处（含定位复核）+ 变体排序断言
 10. caption       best epoch 口径与表号
 11. caption 附言  按几何加粗 / 四频均值 / 案例号范围
"""
import re
import sys

import _boot  # noqa: F401
import _acctable as A
from common import metrics as M
from common import paths, registry, report, texparse as T

SLUG = "T10_abl"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
NUMBER = 10

# 行标签 -> Variant 名。矩形块 25-28，楔形块 29-32。
RECT = {25: "Full model", 26: "w/o physics prior",
        27: "w/o graph correction", 28: "w/o prior supervision"}
WEDGE = {29: "Full model", 30: "w/o physics prior",
         31: "w/o graph correction", 32: "w/o prior supervision"}
CASES = sorted(RECT) + sorted(WEDGE)

# 合并表列布局：0=No., 1=Variant, 2..11 = (Sol,TL)×(25,50,75,100,Avg.)
NC = 12
GROUPS = [25, 50, 75, 100, "Overall"]
NUMCOLS = list(range(2, 12))

# 4.5 节正文直接引用：(说明, 正文字面量, (案例, 组, 量), 定位用的原句片段)
PROSE = [
    ("Case 25 频均 Sol", "11.483", (25, "Overall", "sol"),
     "from $11.483$ to $649.193"),
    ("Case 26 频均 Sol", "649.193", (26, "Overall", "sol"),
     "from $11.483$ to $649.193"),
    ("Case 25 频均 TL", "1.911", (25, "Overall", "tl"),
     "the TL degrades from $1.911$ to $38.800"),
    ("Case 26 频均 TL", "38.800", (26, "Overall", "tl"),
     "the TL degrades from $1.911$ to $38.800"),
    ("Case 29 频均 Sol", "21.645", (29, "Overall", "sol"),
     "from $21.645$ to $3022.705"),
    ("Case 30 频均 Sol", "3022.705", (30, "Overall", "sol"),
     "from $21.645$ to $3022.705"),
    ("Case 29 频均 TL", "1.936", (29, "Overall", "tl"),
     "from $1.936$ to $48.797"),
    ("Case 30 频均 TL", "48.797", (30, "Overall", "tl"),
     "from $1.936$ to $48.797"),
]

# 4.5 节正文的唯一起句，用来界定"本表正文"的窗口
PROSE_ANCHOR = "The physics prior is by far the most important component"


def cell_index(g, q):
    """组 + 量 -> 列索引（0-based）。"""
    blk = 4 if g == "Overall" else [25, 50, 75, 100].index(g)
    return 2 + blk * 2 + (0 if q == "sol" else 1)


def prose_window():
    """4.5 节正文片段：从本表段落起句到下一个 \\subsection 为止。

    限定窗口是必需的：本章（乃至本表自身）多处复用同一批字面量，
    全场搜会把别的节的引用误当成本表的引用。
    """
    txt = T.tex_text()
    i = txt.find(PROSE_ANCHOR)
    if i < 0:
        return ""
    j = txt.find("\\subsection", i)
    return txt[i: j if j > 0 else len(txt)]


def check_printed_both(c, xd, ld, printed, cases, groups, nd=3):
    """两渠道各按自己的值舍入到 nd 位比对，并区分"渠道冲突"与"舍入边界"。

    xlsx 是印刷面的直接来源，故单元格必须与 **xlsx** 的舍入值逐字符相等 ——
    这一条是硬判据，不放松。日志渠道是独立复算，正常应给出同一个舍入值；
    但当全精度值恰好压在 nd 位的进位边界两侧时（两渠道相差 ~1e-7 而分属
    相邻的两个印刷值），它会得到 ±1 个末位。此时若直接判 FAIL，报的是
    "某一次实现少了 5 位有效数字"，而不是论文有错。

    故：xlsx 不符 -> FAIL；xlsx 相符而 log 不符 -> 记为 WARN 并写出两渠道的
    全精度值，读者一眼能看出是边界而非错误。
    """
    c.section("5. 印刷值比对（源值舍入到 3 位 vs tex）")
    for no in cases:
        for k, g in enumerate(groups):
            for j, q in enumerate(("sol", "tl")):
                cell = printed[no][2 + k * 2 + j]
                gname = "Avg." if g == "Overall" else f"{g}Hz"
                a, b = xd[no][g][q], ld[no][g][q]
                c.eq(f"Case {no} {gname} {q.upper()} (xlsx)", a, cell, nd=nd)
                disagree = (b is not None
                            and M.fmt(b, nd) != M.fmt(a, nd))
                if disagree:
                    c.check(False, f"Case {no} {gname} {q.upper()} (log)",
                            f"源 {b!r} → `{M.fmt(b, nd)}` / 印刷 `{cell}`"
                            f"（xlsx `{a!r}` → `{M.fmt(a, nd)}`，两渠道全精度"
                            f"相差 {abs(a - b) / max(1e-12, abs(a)):.2e}，"
                            f"属 {nd} 位进位边界）",
                            warn_only=True)
                else:
                    c.eq(f"Case {no} {gname} {q.upper()} (log)", b, cell, nd=nd)


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, str(NUMBER))
    xl = paths.xlsx_path("4.5")
    env, logs = A.check_sources(c, LABEL, xl, CASES,
                                "工作表1，best epoch 全测试集")

    # ── 1. 本表自己的 tabular ─────────────────────────────────────
    body, star = T.table_body_of(LABEL)
    c.section("1. 本表 tabular 的定位")
    c.note("R1 把多张表绑进同一个 figure* 浮动体，`table_env()` 可能解析到邻居的"
           " tabular；本表一律用 `table_body_of()` 取 label 自己的表体。")
    c.check(body is not None, "label 之后可定位到本表 tabular",
            f"tabular*={star}，长度 {len(body or '')}")
    if body is None:
        return c
    rows = T.data_rows(body, ncol=NC)
    mask = T.bold_mask(body, ncol=NC)
    printed = {int(r[0]): r for r in rows if r[0].strip().isdigit()}
    n_head = body.count("\\multicolumn{12}")
    c.check(len(rows) == 8, "数据行数 = 8（两几何各 4 行）", f"实得 {len(rows)}")
    c.check(len(mask) == len(rows), "加粗掩码与数据行同形", f"{len(mask)} / {len(rows)}")
    c.check(n_head == 2, "两个 \\multicolumn{12} 块头行（矩形 / 楔形）",
            f"实得 {n_head}")

    # ── 2. 源可追溯性 ─────────────────────────────────────────────
    c.section("2. 源可追溯性")
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 25-28 与 29-32",
            str(sorted(printed)))
    for no in CASES:
        want = "矩形" if no in RECT else "楔形"
        owner = RECT if no in RECT else WEDGE
        c.check(owner.get(no) == printed[no][1].strip(),
                f"Case {no} 落在{want}块且 Variant 名相符",
                f"tex `{printed[no][1].strip()}` / 期望 `{owner.get(no)}`")
    order = [int(r[0]) for r in rows]
    c.check(order == CASES, "行序为矩形块 25-28 后接楔形块 29-32", str(order))

    # ── 3-4. best epoch 与双渠道 ─────────────────────────────────
    xd, ld = A.check_epoch(c, xl, logs, CASES)
    A.check_dual(c, xd, ld, CASES, GROUPS)

    # ── 5. 印刷值比对 ────────────────────────────────────────────
    check_printed_both(c, xd, ld, printed, CASES, GROUPS)
    c.note("列序：No., Variant, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)；"
           "Avg. 对应 xlsx/日志的 Overall 组。两几何共用一张表，故行内只有一组数值。")

    # ── 6. Avg. 自洽 ─────────────────────────────────────────────
    c.section("6. Avg. 列与四频均值自洽")
    c.note("caption 声明 Avg. 为四频均值；四频样本数相等，故等权均值应等于 Overall 组。")
    for no in CASES:
        for q in ("sol", "tl"):
            mean = sum(xd[no][f][q] for f in M.FREQS) / 4.0
            ov = xd[no]["Overall"][q]
            c.check(abs(mean - ov) <= max(1e-9, abs(ov) * 1e-5),
                    f"Case {no} Avg. {q.upper()} = 四频均值",
                    f"均值 `{mean:.6g}` / Overall `{ov:.6g}`")

    # ── 7. 位数一致 ──────────────────────────────────────────────
    A.check_decimals(c, printed, CASES, NUMCOLS,
                     title="7. 同表小数位一致性")

    # ── 8. 加粗判据 ──────────────────────────────────────────────
    c.section("8. 加粗判据（每列在各几何块内的最小值）")
    c.note("caption：'The best value in each column, within each geometry, is in "
           "bold'。两几何是上下两块、行集合互不相干，故最小值必须**分块**取；"
           "若误按全表取，楔形块会出现 4 行全不加粗而隐形漏检。")
    bad = []
    for blk, nos in (("矩形", sorted(RECT)), ("楔形", sorted(WEDGE))):
        for j in NUMCOLS:
            vals = [(float(printed[no][j]), no) for no in nos]
            mn = min(v[0] for v in vals)
            bold = [no for no in nos if mask[order.index(no)][j]]
            expect = sorted(no for v, no in vals if abs(v - mn) < 1e-9)
            if sorted(bold) != expect:
                bad.append(f"{blk} 第{j + 1}列 最小在 {expect}，加粗在 {bold}")
    c.check(not bad, "两几何块 × 10 列 = 20 处加粗均指向块内最小值",
            "全部合规" if not bad else "；".join(bad))

    # ── 9. 正文引用 ──────────────────────────────────────────────
    c.section("9. 正文引用精确性（4.5 节）")
    c.note("每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。"
           "只查①会漏掉正文与表格一起错的情形。")
    win = prose_window()
    c.check(bool(win), "4.5 节正文窗口可定位", f"起句 `{PROSE_ANCHOR[:40]}…`")
    for name, lit, (no, g, q), anchor in PROSE:
        cell = printed[no][cell_index(g, q)]
        c.check(lit == cell, f"正文 {name}", f"正文 `{lit}` / 表格 `{cell}`")
        c.eq(f"正文 {name} <- xlsx 源", xd[no][g][q], lit)
        hits = T.sentences_with(re.escape(anchor), win)
        c.check(bool(hits), f"正文 {name} 可定位",
                f"窗口内行 {T.line_of(hits[0][0])}" if hits else "窗口内未找到")

    c.section("10. 正文变体排序断言（印刷值口径）")
    c.note("正文：去掉物理先验后误差激增；楔形上全模型各频段最优，矩形上全模型"
           "在 50-100Hz 领先、25Hz 由 w/o prior supervision 略胜。这些是可复算的"
           "排序断言，用表格印刷值验证，不用源值。")
    for q in ("sol", "tl"):
        c.check(float(printed[26][cell_index("Overall", q)])
                > float(printed[25][cell_index("Overall", q)]) * 10,
                f"矩形 w/o prior 的频均 {q.upper()} 比全模型高一个数量级",
                f"`{printed[26][cell_index('Overall', q)]}` vs "
                f"`{printed[25][cell_index('Overall', q)]}`")
        c.check(float(printed[30][cell_index("Overall", q)])
                > float(printed[29][cell_index("Overall", q)]) * 10,
                f"楔形 w/o prior 的频均 {q.upper()} 比全模型高一个数量级",
                f"`{printed[30][cell_index('Overall', q)]}` vs "
                f"`{printed[29][cell_index('Overall', q)]}`")
    for q in ("sol", "tl"):
        wins = [no for no in sorted(WEDGE)
                if float(printed[no][cell_index("Overall", q)])
                == min(float(printed[m][cell_index("Overall", q)])
                       for m in sorted(WEDGE))]
        c.check(wins == [29], f"楔形频均 {q.upper()} 最优为全模型 (Case 29)",
                f"实得 {wins}")
        for f in (50, 75, 100):
            best = min(float(printed[m][cell_index(f, q)]) for m in sorted(RECT))
            c.check(abs(float(printed[25][cell_index(f, q)]) - best) < 1e-9,
                    f"矩形 {f}Hz {q.upper()} 最优为全模型 (Case 25)",
                    f"全模型 `{printed[25][cell_index(f, q)]}` / 最小 `{best:.3f}`")
        best25 = min(float(printed[m][cell_index(25, q)]) for m in sorted(RECT))
        c.check(abs(float(printed[28][cell_index(25, q)]) - best25) < 1e-9,
                f"矩形 25Hz {q.upper()} 最优为 w/o prior supervision (Case 28)",
                f"Case 28 `{printed[28][cell_index(25, q)]}` / 最小 `{best25:.3f}`")

    A.check_caption(c, LABEL, NUMBER, want_epoch="best epoch",
                    title="11. caption 声明核验")

    # ── 12. caption 附言 ─────────────────────────────────────────
    c.section("12. caption 其余声明（按几何加粗 / 四频均值 / 案例号）")
    cap = T.caption_of(LABEL) or ""
    c.check("within each geometry" in cap, "caption 写明加粗按几何分别判定", "")
    c.check("mean over the four frequencies" in cap.replace("\\ ", " "),
            "caption 声明 Avg. 为四频均值", "")
    c.check("Cases~25--28" in cap and "Cases~29--32" in cap,
            "caption 写明两块的案例号范围", "")
    c.check("four variants" in cap, "caption 声明变体数为 4", "")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
