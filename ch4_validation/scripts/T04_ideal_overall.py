"""
T04_ideal_overall.py — Table 4（tab:ideal-overall）核验
=======================================================
对象：解析解场精度，R0 (Case 1) / W0 (Case 2)，逐频 Sol/TL + Avg.

核验链
  A. 源可追溯      xlsx / log / tex 三方路径均存在且落到本案例
  B. best epoch    xlsx 的 Best Epoch 列 == 日志自证的最佳轮
  C. 双渠道交叉     同一 best epoch 下 xlsx 与 log 的 Sol/TL 互相印证
  D. 印刷值比对     两渠道值按 3 位舍入后与 tex 印刷值逐字符相等
  E. Avg. 自洽      Avg. 列 == 四频均值（caption 的声明）
  F. 小数位一致     同表内 Sol/TL 全部 3 位
  G. 文段引用       4.2 正文 4 处引用与表格印刷值同值同位数

口径：Sol = MSE×1e6；TL = TL vs COMSOL。详见 common/metrics.py 顶部说明。
"""
import os
import re

import _boot  # noqa: F401
from common import metrics as M
from common import paths, registry, report, texparse as T

SLUG = "T04_ideal_overall"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
CASES = {1: "R0 (rect.)", 2: "W0 (wedge)"}

# 正文引用（正文与脚本两份独立记录，才能抓出单侧笔误；有意改数须成对更新）
PROSE = [
    ("R0 频均 Sol", r"\$2\.090\\times10\^\{-6\}\$", "2.090", (1, "Overall", "sol")),
    ("W0 频均 Sol", r"\$3\.383\\times10\^\{-6\}\$", "3.383", (2, "Overall", "sol")),
    ("R0 场 TL", r"\$0\.509\$\\,dB", "0.509", (1, "Overall", "tl")),
    ("W0 场 TL", r"\$0\.514\$\\,dB", "0.514", (2, "Overall", "tl")),
]


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, T.number_of(LABEL))

    xl = paths.xlsx_path("4.2")
    c.source("印刷面 tex", paths.TEX, f"`\\label{{{LABEL}}}` 所在 minipage")
    c.source("渠道1 xlsx", xl, "工作表1『Case1-2 汇总』，best epoch 全测试集")
    for no in CASES:
        c.source(f"渠道2 log (Case {no})", paths.log_path(no), "训练日志 best epoch 原始块")

    # ── A. 源可追溯 ──────────────────────────────────────────────
    c.section("2. 源可追溯性")
    c.check(os.path.exists(paths.TEX), "tex 存在", paths.rel(paths.TEX))
    c.check(os.path.exists(xl), "xlsx 存在", paths.rel(xl))
    logs = {}
    for no in CASES:
        lp = paths.log_path(no)
        logs[no] = lp
        c.check(lp is not None and os.path.exists(lp), f"Case {no} 日志存在", paths.rel(lp))

    env = T.table_env(LABEL)
    c.check(env is not None, "tex 表格环境可定位", f"`{LABEL}`")
    rows = T.data_rows(env, ncol=12)
    c.check(len(rows) == 2, "tex 数据行数 = 2", f"实得 {len(rows)}")

    printed = {}      # no -> [12 cells]
    for r in rows:
        printed[int(r[0])] = r
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 Case 1-2", str(sorted(printed)))

    # ── B. best epoch 双方自证 ───────────────────────────────────
    c.section("3. best epoch 一致性", ("案例", "xlsx Best Epoch / 日志自证", "结论"))
    c.note("xlsx 的 Best Epoch 列与日志里最后一次“保存最佳模型 (Epoch N)”必须同值；"
           "两者不一致则后续所有取值都在比不同轮次。")
    xd, ld = {}, {}
    for no in CASES:
        xd[no] = M.xlsx_case(xl, no)
        be_x = xd[no]["best_epoch"]
        be_l = M.log_best_epoch(logs[no])
        c.check(be_x == be_l, f"Case {no} best epoch", f"xlsx `{be_x}` / log `{be_l}`")
        ld[no] = M.log_epoch(logs[no], be_x)
        c.check(ld[no] is not None, f"Case {no} 日志含 Epoch {be_x} 统计块",
                f"轮次 {be_x}")

    # ── C. 双渠道交叉 ────────────────────────────────────────────
    c.section("4. 双渠道交叉验证（xlsx vs log，同一 best epoch）",
              ("量", "xlsx / log", "结论"))
    c.note("日志侧 Sol 由 `(总损失 − w_prior×prior)/w_rel` 现场计算，"
           "权重从该轮 `Loss Weights:` 行解析，不假定为常数。")
    for no in CASES:
        w = ld[no].get("weights")
        c.note(f"Case {no} 解析到的损失权重：rel_mse={w[0]:.2e}, prior={w[1]:.2e}")
        for g in ("Overall",) + M.FREQS:
            for q in ("sol", "tl"):
                a, b = xd[no][g][q], ld[no][g][q]
                ok = a is not None and b is not None and abs(a - b) <= max(
                    1e-9, abs(a) * 2e-6)
                c.check(ok, f"Case {no} {g} {q.upper()}",
                        f"`{a!r}` / `{b!r}`")

    # ── D. 印刷值比对 ────────────────────────────────────────────
    c.section("5. 印刷值比对（源值舍入到 3 位 vs tex）")
    c.note("列序：No., Dataset, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。"
           "Avg. 对应 xlsx/日志的 Overall 组。")
    order = [(25, 0), (50, 1), (75, 2), (100, 3), ("Overall", 4)]
    for no in CASES:
        c.check(printed[no][1].strip() == CASES[no], f"Case {no} Dataset 名",
                f"tex `{printed[no][1].strip()}`")
        for g, blk in order:
            for k, q in enumerate(("sol", "tl")):
                cell = printed[no][2 + blk * 2 + k]
                gname = "Avg." if g == "Overall" else f"{g}Hz"
                c.eq(f"Case {no} {gname} {q.upper()} (xlsx)", xd[no][g][q], cell)
                c.eq(f"Case {no} {gname} {q.upper()} (log)", ld[no][g][q], cell)

    # ── E. Avg. 自洽 ─────────────────────────────────────────────
    c.section("6. Avg. 列与四频均值自洽")
    c.note("caption 声明 “Avg. is the mean over the four frequencies”，"
           "四频样本数相等（各 1800），故等权均值应与 Overall 组一致。")
    for no in CASES:
        for q in ("sol", "tl"):
            mean = sum(xd[no][f][q] for f in M.FREQS) / 4.0
            ov = xd[no]["Overall"][q]
            c.check(abs(mean - ov) <= max(1e-9, abs(ov) * 1e-5),
                    f"Case {no} Avg. {q.upper()} = 四频均值",
                    f"均值 `{mean:.6g}` / Overall `{ov:.6g}`")

    # ── F. 小数位一致 ────────────────────────────────────────────
    c.section("7. 同表小数位一致性")
    c.note("要求：同一表格内 Sol 与 TL 一律 3 位小数，不因数值大小变位数。")
    bad = []
    for no in CASES:
        for j in range(2, 12):
            v = printed[no][j]
            if not re.fullmatch(r"\d+\.\d{3}", v):
                bad.append(f"Case {no} 第{j + 1}列 `{v}`")
    c.check(not bad, "全部 20 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))

    # ── G. 文段引用 ──────────────────────────────────────────────
    c.section("8. 正文引用精确性（4.2 节）")
    c.note("判定不设容差：正文字面量须与表格印刷值逐字符相同，"
           "位数不足（如 `0.51` 之于 `0.509`）即判失败。")
    tex = T.tex_text()
    for name, pat, expect, (no, g, q) in PROSE:
        hits = T.sentences_with(pat, tex)
        blk = 4 if g == "Overall" else [25, 50, 75, 100].index(g)
        cell = printed[no][2 + blk * 2 + (0 if q == "sol" else 1)]
        ok = bool(hits) and expect == cell
        loc = f"tex 行 {T.line_of(hits[0][0], tex)}" if hits else "未找到"
        c.check(ok, f"正文 {name}",
                f"正文 `{expect}` / 表格 `{cell}` — {loc}")
        # 同时确认该字面量确实由源数据支持，而非与表格一起错
        c.eq(f"正文 {name} ← xlsx 源", xd[no][g][q], expect)

    # ── H ────────────────────────────────────────────────────────
    c.section("8. Caption epoch 声明核验")
    c.note("本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。")
    cap = T.caption_of(LABEL)
    c.check("best epoch" in cap, "caption 声明 best epoch",
            "本表源自 log 的 best epoch，非 last epoch")

    return c


if __name__ == "__main__":
    import sys
    sys.exit(run().finish())
