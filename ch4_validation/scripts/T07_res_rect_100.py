"""
T07_res_rect_100.py — Table 7（tab:res-rect-100）核验
=====================================================
对象：100 Hz 单频、方形域矩形波导 R4–R6 (Cases 6–8)，6 列：
      No. / Dataset / Fig. / Lx×Ly / Sol / TL。

单频表的特点（与 T06 的差别）
  · xlsx 里 25/50/75Hz 三块为 `—`，只有 Overall 与 100Hz 两块有值且**应当同值**；
    这本身是一条可核的自洽条件（D 段）。
  · 表内多一列几何尺寸 Lx×Ly，须与 xlsx 的 Lx/Ly 列一致（E 段）。
  · `\\bottomrule` 之后有一行 `\\multicolumn{6}` 脚注重复声明单位，与 caption 重复（G 段）。

核验链
  A. 源可追溯   B. best epoch   C. 双渠道交叉   D. 单频自洽(Overall==100Hz)
  E. 印刷值比对(含几何尺寸)      F. Fig. 列引用   G. caption/脚注冗余
  H. 位数一致   I. 正文引用 + 派生倍数 8.676
"""
import os
import re

import _boot  # noqa: F401
from common import metrics as M
from common import paths, registry, report, texparse as T

SLUG = "T07_res_rect_100"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]

# Case -> (Dataset, Lx, Ly, (主图 label, 子图 label))
CASES = {
    6: ("R4", 128, 128, ("fig:res-rect-100", "fig:res-rect-100-4")),
    7: ("R5", 256, 256, ("fig:res-rect-100", "fig:res-rect-100-5")),
    8: ("R6", 512, 512, ("fig:res-rect-100", "fig:res-rect-100-6")),
}

# 正文直接引用：(说明, 字面量, (case, 量))
PROSE = [
    ("Case 6 Sol", "0.058", (6, "sol")),
    ("Case 6 TL", "0.444", (6, "tl")),
    ("Case 7 TL", "1.217", (7, "tl")),
    ("Case 8 TL", "3.852", (8, "tl")),
]


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, T.number_of(LABEL))

    xl = paths.xlsx_path("4.3")
    c.source("印刷面 tex", paths.TEX, f"`\\label{{{LABEL}}}` 所在 minipage")
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
            "tex 表格环境可定位且确实包住 label", f"长度 {len(env or '')}")
    rows = T.data_rows(env, ncol=6)
    raws = T.data_rows_raw(env, ncol=6)
    c.check(len(rows) == 3, "tex 数据行数 = 3", f"实得 {len(rows)}")
    printed = {int(r[0]): r for r in rows}
    printed_raw = {int(r[0].strip()): r for r in raws}
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 Case 6-8", str(sorted(printed)))

    # ── B ────────────────────────────────────────────────────────
    c.section("3. best epoch 一致性", ("案例", "xlsx / 日志自证", "结论"))
    c.note("三例 best epoch 各不相同（192/196/200），"
           "正说明取值是逐案例按各自最佳轮读的，不是一律取 ep200。")
    xd, ld = {}, {}
    for no in CASES:
        xd[no] = M.xlsx_case(xl, no)
        be_x = xd[no]["best_epoch"]
        be_l = M.log_best_epoch(logs[no])
        c.check(be_x == be_l, f"Case {no} best epoch", f"xlsx `{be_x}` / log `{be_l}`")
        ld[no] = M.log_epoch(logs[no], be_x)
        c.check(ld[no] is not None, f"Case {no} 日志含『评估 Epoch {be_x}』块", f"轮次 {be_x}")

    # ── C ────────────────────────────────────────────────────────
    c.section("4. 双渠道交叉验证（xlsx vs log）", ("量", "xlsx / log", "结论"))
    for no in CASES:
        for g in ("Overall", 100):
            for q in ("sol", "tl"):
                a, b = xd[no][g][q], ld[no][g][q]
                ok = a is not None and b is not None and abs(a - b) <= max(1e-9, abs(a) * 2e-6)
                c.check(ok, f"Case {no} {g} {q.upper()}", f"`{a!r}` / `{b!r}`")

    # ── D ────────────────────────────────────────────────────────
    c.section("5. 单频自洽性")
    c.note("单频案例只在 100 Hz 上训练与评估，故 Overall 组必须等于 100Hz 组；"
           "25/50/75Hz 三块应为空（xlsx 记 `—`）。两者任一不成立，"
           "说明该行被误当多频案例填了数。")
    for no in CASES:
        for q in ("sol", "tl"):
            a, b = xd[no]["Overall"][q], xd[no][100][q]
            c.check(a is not None and b is not None and abs(a - b) <= max(1e-12, abs(a) * 1e-9),
                    f"Case {no} Overall {q.upper()} == 100Hz {q.upper()}",
                    f"`{a!r}` == `{b!r}`")
        empty = [f for f in (25, 50, 75)
                 if xd[no][f]["sol"] is None and xd[no][f]["tl"] is None]
        c.check(empty == [25, 50, 75], f"Case {no} 25/50/75Hz 均为空",
                f"空的频率 {empty}")

    # ── E ────────────────────────────────────────────────────────
    c.section("6. 印刷值比对（源值舍入到 3 位 vs tex）")
    c.note("列序：No., Dataset, Fig., Lx×Ly, Sol, TL。"
           "几何尺寸另与 xlsx 的 Lx/Ly 列比对——尺寸写错会让整行读者对错案例。")
    rows_x = M.load_sheet(xl)
    for no, (dsname, lx, ly, _) in CASES.items():
        c.check(printed[no][1].strip() == dsname, f"Case {no} Dataset 名",
                f"tex `{printed[no][1].strip()}`")
        # 几何尺寸：tex 写 $128\times128$，clean 后成 128x128
        geo = printed[no][3].replace("$", "").strip()
        c.check(geo == f"{lx}x{ly}", f"Case {no} Lx×Ly 印刷值",
                f"tex `{geo}` / 期望 `{lx}x{ly}`")
        xr = M.case_row(rows_x, no)
        c.check(int(xr[3]) == lx and int(xr[4]) == ly,
                f"Case {no} Lx/Ly 与 xlsx 一致",
                f"xlsx `{int(xr[3])}×{int(xr[4])}`")
        for k, q in enumerate(("sol", "tl")):
            cell = printed[no][4 + k]
            c.eq(f"Case {no} {q.upper()} (xlsx)", xd[no][100][q], cell)
            c.eq(f"Case {no} {q.upper()} (log)", ld[no][100][q], cell)

    # ── F ────────────────────────────────────────────────────────
    c.section("7. Fig. 列引用正确性")
    aux = T.labels()
    for no, (_, _, _, (main, sub)) in CASES.items():
        got = T.refs_in(printed_raw[no][2])
        c.check(got == [main, sub], f"Case {no} Fig. 列引用",
                f"tex `{printed_raw[no][2]}` → {got}")
        for lb in (main, sub):
            c.check(lb in aux, f"label `{lb}` 已在 aux 注册",
                    f"编号 `{aux.get(lb, {}).get('num', '缺失')}`")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. caption 与表内脚注")
    cap = T.caption_of(LABEL) or ""
    c.check("best epoch" in cap, "caption 声明 best epoch", "本表取各案例最佳轮")
    c.check("100" in cap and "f=100" in cap.replace("$", "").replace("\\,", ""),
            "caption 标明单频 f=100 Hz", "")
    foot = re.search(r"\\multicolumn\{6\}[^\\]*\\footnotesize([^\\]*)", env or "")
    has_foot = foot is not None
    dup = has_foot and ("10^{-6}" in cap or "10" in cap) and "10" in (foot.group(1) if foot else "")
    c.check(not dup,
            "单位声明未在 caption 与表内脚注重复",
            f"caption 已写单位；表内另有脚注 `{(foot.group(1).strip() if foot else '')}`"
            + ("——两处重复，建议删表内脚注" if dup else ""),
            warn_only=True)

    # ── H ────────────────────────────────────────────────────────
    c.section("9. 同表小数位一致性")
    bad = []
    for no in CASES:
        for j in (4, 5):
            v = printed[no][j]
            if not re.fullmatch(r"\d+\.\d{3}", v):
                bad.append(f"Case {no} 第{j + 1}列 `{v}`")
    c.check(not bad, "全部 6 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))

    # ── I ────────────────────────────────────────────────────────
    c.section("10. 正文引用精确性（4.3 节）")
    for name, lit, (no, q) in PROSE:
        cell = printed[no][4 if q == "sol" else 5]
        c.check(lit == cell, f"正文 {name}", f"正文 `{lit}` / 表格 `{cell}`")
        c.eq(f"正文 {name} ← xlsx 源", xd[no][100][q], lit)

    c.section("11. 正文派生倍数（印刷值口径）")
    c.note("倍数用表格印刷值相除。此处 3.852/0.444 = 8.6756… → 8.676；"
           "若改用全精度源值 3.852302/0.4443021 会得 8.670，与正文不符——"
           "这正是先前 8.676/8.670 之争的由来，口径必须固定为印刷值。")
    tl6, tl8 = float(printed[6][5]), float(printed[8][5])
    r_print = tl8 / tl6
    r_full = xd[8][100]["tl"] / xd[6][100]["tl"]
    c.check(f"{r_print:.3f}" == "8.676", "100Hz 矩形 512m/128m TL 倍数 = 8.676",
            f"印刷值口径 `{tl8}`/`{tl6}` = `{r_print:.6f}` → `{r_print:.3f}`")
    c.note(f"对照：全精度口径为 `{r_full:.6f}` → `{r_full:.3f}`，"
           "与正文的 8.676 不同；正文采用印刷值口径，故以印刷值为准。")
    hits = T.sentences_with(r"factor of \$8\.676\$", T.tex_text())
    c.check(bool(hits), "正文该倍数可定位",
            f"tex 行 {T.line_of(hits[0][0])}" if hits else "未找到")

    c.section("12. 正文趋势断言")
    c.note("正文称单频方形域“最准的是 128×128”，且 TL 随域增大单调上升。")
    tls = [xd[no][100]["tl"] for no in (6, 7, 8)]
    sols = [xd[no][100]["sol"] for no in (6, 7, 8)]
    c.check(tls == sorted(tls), "TL 随域尺度单调上升",
            " < ".join(f"{v:.3f}" for v in tls))
    c.check(sols == sorted(sols), "Sol 随域尺度单调上升",
            " < ".join(f"{v:.3f}" for v in sols))

    return c


if __name__ == "__main__":
    import sys
    sys.exit(run().finish())
