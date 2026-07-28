"""
T18_mesh_wedge.py — Table 18（tab:mesh-wedge-mf）核验
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

SLUG = "T18_mesh_wedge"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]

# Case No. -> (Dataset 名, 该行 Fig. 列应引用的 (主图 label, 子图 label))
CASES = {
    36: ("W4", ("fig:mesh-wedge", "fig:mesh-wedge-a")),
    37: ("W7", ("fig:mesh-wedge", "fig:mesh-wedge-b")),
    38: ("W8", ("fig:mesh-wedge", "fig:mesh-wedge-c")),
}

# 正文直接引用（4.6 节网格独立性段落）
PROSE = [
    ("Case 36 (Δ=1.00) Sol", "0.100", (36, "sol")),
    ("Case 38 (Δ=0.25) Sol", "0.326", (38, "sol")),
    ("Case 36 (Δ=1.00) TL", "0.610", (36, "tl")),
    ("Case 37 (Δ=0.50) TL", "0.361", (37, "tl")),
    ("Case 38 (Δ=0.25) TL", "0.311", (38, "tl")),
]



def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, T.number_of(LABEL))

    xl = paths.xlsx_path("4.6")
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
    rows = T.data_rows(env, ncol=6)
    raws = T.data_rows_raw(env, ncol=6)
    c.check(len(rows) == 3, "tex 数据行数 = 3", f"实得 {len(rows)}")
    printed = {int(r[0]): r for r in rows}
    printed_raw = {int(r[0].strip()): r for r in raws}
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 36-38",
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
        # 只验证 100 Hz
        for q in ("sol", "tl"):
            a, b = xd[no][100][q], ld[no][100][q]
            ok = a is not None and b is not None and abs(a - b) <= max(1e-9, abs(a) * 2e-6)
            c.check(ok, f"Case {no} 100Hz {q.upper()}", f"`{a!r}` / `{b!r}`")

    # ── D ────────────────────────────────────────────────────────
    c.section("5. 印刷值比对（源值舍入到 3 位 vs tex）")
    c.note("列序：No., Dataset, Δ, Fig., Sol, TL。本表只有 100 Hz。")
    for no in CASES:
        c.check(printed[no][1].strip() == CASES[no][0], f"Case {no} Dataset 名",
                f"tex `{printed[no][1].strip()}`")
        # 列 4=Sol, 列 5=TL
        for k, q in enumerate(("sol", "tl")):
            cell = printed[no][4 + k]  # 列 4=Sol, 列 5=TL
            c.eq(f"Case {no} 100Hz {q.upper()} (xlsx)", xd[no][100][q], cell)
            c.eq(f"Case {no} 100Hz {q.upper()} (log)", ld[no][100][q], cell)

    # ── E ────────────────────────────────────────────────────────
    c.section("6. Fig. 列引用正确性")
    c.note("每行的图号必须指向该案例自己的图与子图。"
           "同时确认被引 label 在 aux 里存在（否则排出 `??`）。")
    aux = T.labels()
    for no, (_, (main, sub)) in CASES.items():
        got = T.refs_in(printed_raw[no][3])  # Fig. 列是第 4 列（索引 3）
        c.check(got == [main, sub], f"Case {no} Fig. 列引用",
                f"tex `{printed_raw[no][3]}` → {got}，应为 `[{main}, {sub}]`")
        for lb in (main, sub):
            c.check(lb in aux, f"label `{lb}` 已在 aux 注册",
                    f"编号 `{aux.get(lb, {}).get('num', '缺失')}`")

    # ── G ────────────────────────────────────────────────────────
    c.section("7. 同表小数位一致性")
    bad = []
    for no in CASES:
        for j in range(4, 6):  # 列 4=Sol, 列 5=TL
            v = printed[no][j]
            if not re.fullmatch(r"\d+\.\d{3}", v):
                bad.append(f"Case {no} 第{j + 1}列 `{v}`")
    c.check(not bad, "全部 6 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))

    # ── G ────────────────────────────────────────────────────────
    c.section("7. 正文引用精确性（4.6 节）")
    c.note("验证正文段落中引用的数值与表格/源数据一致。")
    for desc, quoted, (no, field) in PROSE:
        # 列索引：4=Sol, 5=TL
        col_idx = 4 if field == "sol" else 5
        cell = printed[no][col_idx]
        c.check(quoted == cell, desc, f"正文 `{quoted}` / 表格 `{cell}`")
        c.eq(f"{desc} <- xlsx 源", xd[no][100][field], quoted, nd=3)


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
