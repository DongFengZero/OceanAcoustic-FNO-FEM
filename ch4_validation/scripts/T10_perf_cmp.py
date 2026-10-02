"""
T10_perf_cmp.py — Table 10（tab:perf-cmp）核验
==============================================
对象：五方法逐频前向精度，**矩形 R1（Cases 15-19）与楔形 W1（Cases 20-24）
      分块排在同一张表**，12 列：

        No. | Method | 25Hz(Sol,TL) | 50Hz | 75Hz | 100Hz | Avg.(Sol,TL)

R1 修订把原来的 Table 13（perf-rect）与 Table 14（perf-wedge）合并为本表，
故本脚本覆盖两个几何；每块的判据与合并前逐条相同，只是版式变了。

版式要点（与合并前的并排表不同）
  * 两几何不是左右并排，而是**上下两块**，块头是 `\\multicolumn{12}` 行；
    因此 No. 列只有一个（列 0），不像并排表那样每块各有一列 No.。
  * R1 把多张表绑进同一个 figure* 浮动体，`T.table_env()` 可能解析到同浮动体内
    的邻居，故本表自己的 tabular 取自 `T.table_body_of(LABEL)`。

核验链
  1. 表格版式      本表自己的 tabular / 行数 / 两个块头
  2. 源可追溯      xlsx / 10 份日志 / tex 行 No. 与 Method 名 / 块序
  3. best epoch    xlsx 列 == 日志自证
  4. 双渠道交叉    xlsx vs 日志同轮评估块（5 组 × 2 量 × 10 案例 = 100 个量）
  5. 印刷值比对    两渠道 × 100 格
  6. Avg. 自洽     Avg. == 四频均值
  7. 位数一致      全部 100 个数值格 3 位小数
  8. 加粗判据      每列**各自几何块内**的最小值加粗（caption 的口径）
  9. 正文引用      4.4 节直接引用 10 处（含定位复核）
 10. caption       best epoch 口径与表号
 11. caption 附言  按几何加粗 / 四频均值 / 案例号范围 / 图引用
"""
import re
import sys

import _boot  # noqa: F401
import _acctable as A
from common import metrics as M
from common import paths, registry, report, texparse as T

SLUG = "T10_perf_cmp"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
NUMBER = 10

# 行标签 -> Method 名。矩形块 15-19，楔形块 20-24。
RECT = {15: "Proposed", 16: "DeepONet", 17: "FNO", 18: "KNO", 19: "CNO"}
WEDGE = {20: "Proposed", 21: "DeepONet", 22: "FNO", 23: "KNO", 24: "CNO"}
CASES = sorted(RECT) + sorted(WEDGE)

# 合并表列布局：0=No., 1=Method, 2..11 = (Sol,TL)×(25,50,75,100,Avg.)
NC = 12
BLOCKS = [("矩形", sorted(RECT), 0), ("楔形", sorted(WEDGE), 0)]
GROUPS = [25, 50, 75, 100, "Overall"]
NUMCOLS = list(range(2, 12))

# 4.4 节正文直接引用：(说明, 正文字面量, (案例, 组, 量), 定位用的原句片段)
#
# 第四项是必需的：本表的数值与 4.3 / 4.5 节正文共用同一批字面量
# （1.688 / 0.951 / 2.121 / 0.899 在 4.3 节讲 Table 6 的 128m 案例时也出现），
# 只按裸数值定位会命中别的节。原句片段取自 4.4 节那段实际文字。
PROSE = [
    ("Case 15 频均 Sol", "1.688", (15, "Overall", "sol"),
     "reaches an average solution error of $1.688"),
    ("Case 15 频均 TL", "0.951", (15, "Overall", "tl"),
     "and a TL of $0.951$"),
    ("Case 17 频均 Sol", "3.730", (17, "Overall", "sol"),
     "FNO, trails at $3.730"),
    ("Case 17 频均 TL", "1.305", (17, "Overall", "tl"),
     "and $1.305$\\,dB"),
    ("Case 20 频均 Sol", "2.121", (20, "Overall", "sol"),
     "the proposed solver attains $2.121"),
    ("Case 20 频均 TL", "0.899", (20, "Overall", "tl"),
     "and $0.899$\\,dB"),
    ("Case 22 频均 Sol", "3.179", (22, "Overall", "sol"),
     "against $3.179"),
    ("Case 22 频均 TL", "1.090", (22, "Overall", "tl"),
     "and $1.090$\\,dB"),
    ("Case 20 @100Hz TL", "1.265", (20, 100, "tl"),
     "holds the TL to $1.265"),
    ("Case 21 @100Hz TL", "5.512", (21, 100, "tl"),
     "DeepONet degrades to $5.512"),
]

# 4.4 节正文的唯一起句，用来界定"本表正文"的窗口
PROSE_ANCHOR = "The proposed solver attains the lowest solution error"


def cell_index(g, q):
    """组 + 量 -> 列索引（0-based）。"""
    blk = 4 if g == "Overall" else [25, 50, 75, 100].index(g)
    return 2 + blk * 2 + (0 if q == "sol" else 1)


def prose_window():
    """4.4 节正文片段：从本表段落起句到下一个 \\subsection 为止。

    限定窗口是必需的：本表的数值与 Table 6 的 4.3 节正文、Table 11 的
    4.5 节正文共用同一批字面量（如 1.688 / 0.951 在 4.3 节也出现），
    全场搜会把别的节的引用误当成本表的引用。
    """
    txt = T.tex_text()
    i = txt.find(PROSE_ANCHOR)
    if i < 0:
        return ""
    j = txt.find("\\subsection", i)
    return txt[i: j if j > 0 else len(txt)]


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, str(NUMBER))
    xl = paths.xlsx_path("4.4")
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
    c.check(len(rows) == 10, "数据行数 = 10（两几何各 5 行）", f"实得 {len(rows)}")
    c.check(len(mask) == len(rows), "加粗掩码与数据行同形", f"{len(mask)} / {len(rows)}")
    n_head = body.count("\\multicolumn{12}")
    c.check(n_head == 2, "两个 \\multicolumn{12} 块头行（矩形 / 楔形）",
            f"实得 {n_head}")

    # ── 2. 源可追溯性 ─────────────────────────────────────────────
    c.section("2. 源可追溯性")
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 15-19 与 20-24",
            str(sorted(printed)))
    for no in CASES:
        want = "矩形" if no in RECT else "楔形"
        owner = RECT if no in RECT else WEDGE
        c.check(owner.get(no) == printed[no][1].strip(),
                f"Case {no} 落在{want}块且 Method 名相符",
                f"tex `{printed[no][1].strip()}` / 期望 `{owner.get(no)}`")
    # 块序：矩形行必须在楔形行之前。data_rows 保序，故按出现顺序判断。
    order = [int(r[0]) for r in rows]
    c.check(order == CASES, "行序为矩形块 15-19 后接楔形块 20-24", str(order))

    # ── 3-4. best epoch 与双渠道 ─────────────────────────────────
    xd, ld = A.check_epoch(c, xl, logs, CASES)
    A.check_dual(c, xd, ld, CASES, GROUPS)

    # ── 5. 印刷值比对 ────────────────────────────────────────────
    spec = {no: [("", 2, GROUPS)] for no in CASES}
    A.check_printed(c, xd, ld, printed, spec,
                    title="5. 印刷值比对（源值舍入到 3 位 vs tex）")
    c.note("列序：No., Method, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)；"
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
           "若误按全表取，楔形块会出现 5 行全不加粗而隐形漏检。")
    bad = []
    for blk, nos in (("矩形", sorted(RECT)), ("楔形", sorted(WEDGE))):
        for j in NUMCOLS:
            vals = [(float(printed[no][j]), no) for no in nos]
            mn = min(v[0] for v in vals)
            bold = [no for no in nos
                    if mask[order.index(no)][j]]
            expect = sorted(no for v, no in vals if abs(v - mn) < 1e-9)
            if sorted(bold) != expect:
                bad.append(f"{blk} 第{j + 1}列 最小在 {expect}，加粗在 {bold}")
    c.check(not bad, "两几何块 × 10 列 = 20 处加粗均指向块内最小值",
            "全部合规" if not bad else "；".join(bad))

    # ── 9. 正文引用 ──────────────────────────────────────────────
    c.section("9. 正文引用精确性（4.4 节）")
    c.note("每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。"
           "只查①会漏掉正文与表格一起错的情形。")
    win = prose_window()
    c.check(bool(win), "4.4 节正文窗口可定位", f"起句 `{PROSE_ANCHOR[:40]}…`")
    for name, lit, (no, g, q), anchor in PROSE:
        cell = printed[no][cell_index(g, q)]
        c.check(lit == cell, f"正文 {name}", f"正文 `{lit}` / 表格 `{cell}`")
        c.eq(f"正文 {name} <- xlsx 源", xd[no][g][q], lit)
        pat = re.escape(anchor)
        hits = T.sentences_with(pat, win)
        c.check(bool(hits), f"正文 {name} 可定位",
                f"窗口内行 {T.line_of(hits[0][0])}" if hits else "窗口内未找到")

    A.check_caption(c, LABEL, NUMBER, want_epoch="best epoch",
                    title="10. caption 声明核验")

    # ── 11. caption 附言 ─────────────────────────────────────────
    c.section("11. caption 其余声明（按几何加粗 / 四频均值 / 案例号 / 图引用）")
    cap = T.caption_of(LABEL) or ""
    c.check("within each geometry" in cap, "caption 写明加粗按几何分别判定", "")
    c.check("mean over the four frequencies" in cap.replace("\\ ", " "),
            "caption 声明 Avg. 为四频均值", "")
    c.check("Cases~15--19" in cap and "Cases~20--24" in cap,
            "caption 写明两块的案例号范围", "")
    c.check("fig:perf-cmp-r" in cap and "fig:perf-cmp-w" in cap,
            "caption 交叉引用 Fig.\\ref{fig:perf-cmp-r}/{-w}", "")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
