"""
T08_res_wedge_100.py — Table 8（tab:res-wedge-100）核验
=======================================================
对象：100 Hz 单频、方形域楔形波导 W4–W6 (Cases 12–14)，6 列：
      No. / Dataset / Fig. / Lx×Ly / Sol / TL。

与 T07 同构，另加三项本表特有的核验：
  J. 跨表版式一致    Table 7/8 并列于同一浮动体，列定义与表头须逐字符相同，
                     否则两表不等宽、读者无法左右对读（★）
  K. 跨节复用关系    4.6 的基线行复用本节单频案例：Case 33≡6、Case 36≡12。
                     用 best epoch + 全精度值双重确认是同一次运行，
                     而不是碰巧印成同样的三位小数（★）
  L. best epoch 离群  Case 14 的最佳轮为 129，显著早于同组的 195/193。
                     不是错误，但须在报告里留痕，避免后人误以为漏取（★）
"""
import os
import re

import _boot  # noqa: F401
from common import metrics as M
from common import paths, registry, report, texparse as T

SLUG = "T08_res_wedge_100"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
SIB = "tab:res-rect-100"          # 并列的 Table 7

CASES = {
    12: ("W4", 128, 128, ("fig:res-wedge-100", "fig:res-wedge-100-10")),
    13: ("W5", 256, 256, ("fig:res-wedge-100", "fig:res-wedge-100-11")),
    14: ("W6", 512, 512, ("fig:res-wedge-100", "fig:res-wedge-100-12")),
}

PROSE = [
    ("Case 12 Sol", "0.100", (12, "sol")),
    ("Case 12 TL", "0.610", (12, "tl")),
    ("Case 13 TL", "0.930", (13, "tl")),
    ("Case 14 TL", "3.407", (14, "tl")),
]

# 4.6 复用关系：(4.6 案例, 本节案例)
REUSE = [(36, 12)]
REUSE_SIB = [(33, 6)]             # 对照：矩形侧同样成立，一并记录


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, T.number_of(LABEL))

    xl = paths.xlsx_path("4.3")
    c.source("印刷面 tex", paths.TEX, f"`\\label{{{LABEL}}}` 所在 minipage")
    c.source("渠道1 xlsx", xl, "工作表1，best epoch 全测试集")
    for no in CASES:
        c.source(f"渠道2 log (Case {no})", paths.log_path(no), "训练日志同轮『评估』块")
    c.source("复用比对 xlsx", paths.xlsx_path("4.6"), "4.6 节汇总，用于确认 Case 36≡12")

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
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 Case 12-14", str(sorted(printed)))

    # ── B / L ────────────────────────────────────────────────────
    c.section("3. best epoch 一致性", ("案例", "xlsx / 日志自证", "结论"))
    xd, ld = {}, {}
    for no in CASES:
        xd[no] = M.xlsx_case(xl, no)
        be_x = xd[no]["best_epoch"]
        be_l = M.log_best_epoch(logs[no])
        c.check(be_x == be_l, f"Case {no} best epoch", f"xlsx `{be_x}` / log `{be_l}`")
        ld[no] = M.log_epoch(logs[no], be_x)
        c.check(ld[no] is not None, f"Case {no} 日志含『评估 Epoch {be_x}』块", f"轮次 {be_x}")
    bes = {no: xd[no]["best_epoch"] for no in CASES}
    c.note(f"本组 best epoch 为 {bes}。Case 14 的 129 明显早于另两例，"
           "是该次训练的验证损失确实在 129 轮触底（日志自证一致），"
           "不是漏取或截断；记此一笔以免后人误判。")
    c.check(all(1 <= v <= 200 for v in bes.values()),
            "三例 best epoch 均落在 1–200 合法区间", str(sorted(bes.values())))

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
    c.note("单频案例 Overall 组须等于 100Hz 组，且 25/50/75Hz 为空。")
    for no in CASES:
        for q in ("sol", "tl"):
            a, b = xd[no]["Overall"][q], xd[no][100][q]
            c.check(a is not None and b is not None and abs(a - b) <= max(1e-12, abs(a) * 1e-9),
                    f"Case {no} Overall {q.upper()} == 100Hz {q.upper()}",
                    f"`{a!r}` == `{b!r}`")
        empty = [f for f in (25, 50, 75)
                 if xd[no][f]["sol"] is None and xd[no][f]["tl"] is None]
        c.check(empty == [25, 50, 75], f"Case {no} 25/50/75Hz 均为空", f"空的频率 {empty}")

    # ── E ────────────────────────────────────────────────────────
    c.section("6. 印刷值比对（源值舍入到 3 位 vs tex）")
    rows_x = M.load_sheet(xl)
    for no, (dsname, lx, ly, _) in CASES.items():
        c.check(printed[no][1].strip() == dsname, f"Case {no} Dataset 名",
                f"tex `{printed[no][1].strip()}`")
        geo = printed[no][3].replace("$", "").strip()
        c.check(geo == f"{lx}x{ly}", f"Case {no} Lx×Ly 印刷值",
                f"tex `{geo}` / 期望 `{lx}x{ly}`")
        xr = M.case_row(rows_x, no)
        c.check(int(xr[3]) == lx and int(xr[4]) == ly,
                f"Case {no} Lx/Ly 与 xlsx 一致", f"xlsx `{int(xr[3])}×{int(xr[4])}`")
        for k, q in enumerate(("sol", "tl")):
            cell = printed[no][4 + k]
            c.eq(f"Case {no} {q.upper()} (xlsx)", xd[no][100][q], cell)
            c.eq(f"Case {no} {q.upper()} (log)", ld[no][100][q], cell)

    # ── F ────────────────────────────────────────────────────────
    c.section("7. Fig. 列引用正确性")
    c.note("楔形三行须各自指向 `fig:res-wedge-100` 的 -10/-11/-12 子图；"
           "子图后缀沿用案例序号而非 1/2/3，错配不会报编译错，只能靠比对发现。")
    aux = T.labels()
    for no, (_, _, _, (main, sub)) in CASES.items():
        got = T.refs_in(printed_raw[no][2])
        c.check(got == [main, sub], f"Case {no} Fig. 列引用",
                f"tex `{printed_raw[no][2]}` → {got}")
        for lb in (main, sub):
            c.check(lb in aux, f"label `{lb}` 已在 aux 注册",
                    f"编号 `{aux.get(lb, {}).get('num', '缺失')}`")

    # ── J ────────────────────────────────────────────────────────
    c.section("8. 与 Table 7 的版式一致性")
    c.note("Table 7/8 并列在同一 `table*` 的左右 minipage 内，"
           "列定义与表头必须逐字符相同，否则两表不等宽、无法左右对读。")
    sib = T.table_env(SIB) or ""
    for what, fn in (("列定义 (tabular preamble)", T.tabular_preamble),
                     ("表头行", T.header_row)):
        a, b = fn(env), fn(sib)
        c.check(a is not None and a == b, f"{what}与 Table 7 相同",
                f"Table 8 `{a}` / Table 7 `{b}`")
    c.check("\\TABstyle" in (env or "") and "\\TABstyle" in sib,
            "两表同用 \\TABstyle", "")
    for name, e in (("Table 8", env), ("Table 7", sib)):
        c.check("Sol in units of" not in (e or ""),
                f"{name} 表内无与 caption 重复的单位脚注",
                "已于 2026-07-28 删除")

    # ── K ────────────────────────────────────────────────────────
    c.section("9. 与 4.6 节的复用关系")
    c.note("4.6 网格研究的最粗一档就是本节的单频案例：Case 36 复用 Case 12、"
           "Case 33 复用 Case 6。判定不看三位小数是否相同（那可能是巧合），"
           "而要求 best epoch 与全精度值都一致，才算同一次运行。")
    xl6 = paths.xlsx_path("4.6")
    for a6, a3 in REUSE + REUSE_SIB:
        d6, d3 = M.xlsx_case(xl6, a6), M.xlsx_case(xl, a3)
        c.check(d6["best_epoch"] == d3["best_epoch"],
                f"Case {a6} 与 Case {a3} best epoch 相同",
                f"`{d6['best_epoch']}` == `{d3['best_epoch']}`")
        for q in ("sol", "tl"):
            va, vb = d6[100][q], d3[100][q]
            c.check(va is not None and vb is not None and va == vb,
                    f"Case {a6} 与 Case {a3} {q.upper()} 全精度相同",
                    f"`{va!r}` == `{vb!r}`")

    # ── H ────────────────────────────────────────────────────────
    c.section("10. 同表小数位一致性")
    bad = []
    for no in CASES:
        for j in (4, 5):
            v = printed[no][j]
            if not re.fullmatch(r"\d+\.\d{3}", v):
                bad.append(f"Case {no} 第{j + 1}列 `{v}`")
    c.check(not bad, "全部 6 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))

    # ── I ────────────────────────────────────────────────────────
    c.section("11. 正文引用精确性（4.3 节）")
    for name, lit, (no, q) in PROSE:
        cell = printed[no][4 if q == "sol" else 5]
        c.check(lit == cell, f"正文 {name}", f"正文 `{lit}` / 表格 `{cell}`")
        c.eq(f"正文 {name} ← xlsx 源", xd[no][100][q], lit)

    c.section("12. 正文趋势断言")
    c.note("正文列出楔形单频 TL 递增序列 0.610 → 0.930 → 3.407，"
           "并称 128m 单频两例是全体中最准的。")
    tls = [xd[no][100]["tl"] for no in (12, 13, 14)]
    sols = [xd[no][100]["sol"] for no in (12, 13, 14)]
    c.check(tls == sorted(tls), "TL 随域尺度单调上升",
            " < ".join(f"{v:.3f}" for v in tls))
    c.check(sols == sorted(sols), "Sol 随域尺度单调上升",
            " < ".join(f"{v:.3f}" for v in sols))
    seq = T.sentences_with(r"\$0\.610\$ to \$0\.930\$ to \$3\.407\$", T.tex_text())
    c.check(bool(seq), "正文递增序列可定位",
            f"tex 行 {T.line_of(seq[0][0])}" if seq else "未找到")
    # “128m 单频最准”须在全部 12 个前向案例里成立
    c.note("『单频 128m 最准』是跨表断言：需在 4.3 全部 12 例中比较，"
           "而不只是本表 3 例。")
    allc = list(range(3, 15))
    tl_all = {no: M.xlsx_case(xl, no)["Overall"]["tl"] for no in allc}
    best = min(tl_all, key=tl_all.get)
    c.check(best == 6 and sorted(tl_all.values())[:2] == sorted(
        [tl_all[6], tl_all[12]]),
        "Cases 6/12 的 TL 是 12 例中最小的两个",
        f"最小 Case {best} (`{tl_all[6]:.3f}`)、次小 Case 12 (`{tl_all[12]:.3f}`)")


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
