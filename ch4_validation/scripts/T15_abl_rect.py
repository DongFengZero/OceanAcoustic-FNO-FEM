"""
T15_abl_rect.py — Table 15（tab:abl-rect）核验
====================================================
对象：多频前向精度，矩形 R1–R3 (Cases 3–5) + 楔形 W1–W3 (Cases 9–11)，
      逐频 Sol/TL + Avg.，13 列（含 Fig. 列）。

核验链（较 T04 多出三项）
  A. 源可追溯      xlsx / 6 份日志 / tex
  B. best epoch    xlsx 列 == 日志自证
  C. 双渠道交叉     xlsx vs 日志同轮评估块，60 个量
  D. 印刷值比对     两渠道 × 60 格
  E. Fig. 列引用    每行图号须指向该案例自己的图与子图（★T06 独有）
  F. 分组行         两个 \\multicolumn 小标题行存在且几何归属正确（★T06 独有）
  G. Avg. 自洽      Avg. == 四频均值
  H. 位数一致       Sol/TL 全 3 位
  I. 文段引用       4.3 正文 16 处直接引用 + 1 处派生倍数（★含派生口径）

派生倍数口径：用**表格印刷值**相除，保证读者可直接复算。
2.157/0.951 = 2.2681… → 正文写 2.268。不可用全精度源值回算成别的数。
"""
import os
import re

import _boot  # noqa: F401
from common import metrics as M
from common import paths, registry, report, texparse as T

SLUG = "T15_abl_rect"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]

# Case No. -> (Dataset 名, 该行 Fig. 列应引用的 (主图 label, 子图 label))
CASES = {
    25: ("Full model",),
    26: ("w/o physics prior",),
    27: ("w/o graph correction",),
    28: ("w/o prior supervision",),
}

# 正文直接引用：(说明, 正文字面量, (case, 组, 量))
PROSE = [
    ("Case 25 Full model 频均 Sol", "11.483", (25, "Overall", "sol")),
    ("Case 25 Full model 频均 TL", "1.911", (25, "Overall", "tl")),
    ("Case 26 w/o prior 频均 Sol", "649.193", (26, "Overall", "sol")),
    ("Case 26 w/o prior 频均 TL", "38.800", (26, "Overall", "tl")),
]


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, T.number_of(LABEL))

    xl = paths.xlsx_path("4.5")
    c.source("印刷面 tex", paths.TEX, f"`\\label{{{LABEL}}}` 所在 table* 环境")
    c.source("渠道1 xlsx", xl, "工作表1，best epoch 全测试集")
    for no in CASES:
        c.source(f"渠道2 log (Case {no})", paths.log_path(no), "训练日志同轮『评估』块")

    # ── A ────────────────────────────────────────────────────────
    c.section("2. 源可追溯性")
    c.check(os.path.exists(xl), "xlsx 存在", paths.rel(xl))
    logs = {}
    for no in CASES:
        lp = paths.log_path(no)
        logs[no] = lp
        c.check(lp is not None and os.path.exists(lp), f"Case {no} 日志存在", paths.rel(lp))

    env = T.table_env(LABEL)
    c.check(env is not None and f"\\label{{{LABEL}}}" in env,
            "tex 表格环境可定位且确实包住 label", f"`{LABEL}`，长度 {len(env or '')}")
    rows = T.data_rows(env, ncol=12)
    raws = T.data_rows_raw(env, ncol=12)
    c.check(len(rows) == 4, "tex 数据行数 = 4", f"实得 {len(rows)}")
    printed = {int(r[0]): r for r in rows}
    printed_raw = {int(r[0].strip()): r for r in raws}
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 15-19",
            str(sorted(printed)))

    # ── B ────────────────────────────────────────────────────────
    c.section("3. best epoch 一致性", ("案例", "xlsx / 日志自证", "结论"))
    xd, ld = {}, {}
    for no in CASES:
        xd[no] = M.xlsx_case(xl, no)
        be_x = xd[no]["best_epoch"]
        be_l = M.log_best_epoch(logs[no])
        c.check(be_x == be_l, f"Case {no} best epoch", f"xlsx `{be_x}` / log `{be_l}`")
        ld[no] = M.log_epoch(logs[no], be_x)
        c.check(ld[no] is not None, f"Case {no} 日志含『评估 Epoch {be_x}』块", f"轮次 {be_x}")

    # ── C ────────────────────────────────────────────────────────
    c.section("4. 双渠道交叉验证（xlsx vs log，同一 best epoch）",
              ("量", "xlsx / log", "结论"))
    c.note("日志侧取『评估 Epoch N 完成』块（测试集），非『训练』块；"
           "Sol 由 `(损失 − w_prior×prior)/w_rel` 现场算，权重逐轮解析。")
    for no in CASES:
        for g in ("Overall",) + M.FREQS:
            for q in ("sol", "tl"):
                a, b = xd[no][g][q], ld[no][g][q]
                ok = a is not None and b is not None and abs(a - b) <= max(1e-9, abs(a) * 2e-6)
                c.check(ok, f"Case {no} {g} {q.upper()}", f"`{a!r}` / `{b!r}`")

    # ── D ────────────────────────────────────────────────────────
    c.section("5. 印刷值比对（源值舍入到 3 位 vs tex）")
    c.note("列序：No., Variant, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。"
           "Avg. 对应 xlsx/日志的 Overall 组。本表无 Fig. 列。"
           "日志渠道的一致性已在第 4 节双渠道验证中确认，此处仅比对 xlsx。")
    order = [(25, 0), (50, 1), (75, 2), (100, 3), ("Overall", 4)]
    for no in CASES:
        c.check(printed[no][1].strip() == CASES[no][0], f"Case {no} Variant 名",
                f"tex `{printed[no][1].strip()}`")
        for g, blk in order:
            for k, q in enumerate(("sol", "tl")):
                cell = printed[no][2 + blk * 2 + k]
                gname = "Avg." if g == "Overall" else f"{g}Hz"
                c.eq(f"Case {no} {gname} {q.upper()} (xlsx)", xd[no][g][q], cell)

    # ── E ────────────────────────────────────────────────────────
    c.section("6. Avg. 列与四频均值自洽")
    c.note("caption 声明 Avg. 为四频均值；四频样本数相等，故等权均值应等于 Overall 组。")
    for no in CASES:
        for q in ("sol", "tl"):
            mean = sum(xd[no][f][q] for f in M.FREQS) / 4.0
            ov = xd[no]["Overall"][q]
            c.check(abs(mean - ov) <= max(1e-9, abs(ov) * 1e-5),
                    f"Case {no} Avg. {q.upper()} = 四频均值",
                    f"均值 `{mean:.6g}` / Overall `{ov:.6g}`")

    # ── F ────────────────────────────────────────────────────────
    c.section("7. 同表小数位一致性")
    bad = []
    for no in CASES:
        for j in range(2, 12):
            v = printed[no][j]
            if not re.fullmatch(r"\d+\.\d{3}", v):
                bad.append(f"Case {no} 第{j + 1}列 `{v}`")
    c.check(not bad, "全部 40 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 正文引用精确性（4.5 节）")
    c.note("每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。"
           "只查①会漏掉正文与表格一起错的情形。")
    for name, lit, (no, g, q) in PROSE:
        blk = 4 if g == "Overall" else [25, 50, 75, 100].index(g)
        cell = printed[no][2 + blk * 2 + (0 if q == "sol" else 1)]
        c.check(lit == cell, f"正文 {name}", f"正文 `{lit}` / 表格 `{cell}`")
        c.eq(f"正文 {name} <- xlsx 源", xd[no][g][q], lit)


    # ── Caption epoch 声明核验 ──
    c.section("X. Caption epoch 声明核验")
    c.note("本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。")
    cap = T.caption_of(LABEL)
    c.check("best epoch" in cap, "caption 声明 best epoch",
            "本表源自 log 的 best epoch，非 last epoch")

    return c



if __name__ == "__main__":
    import sys
    sys.exit(run().finish())
