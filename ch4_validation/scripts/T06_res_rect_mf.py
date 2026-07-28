"""
T06_res_rect_mf.py — Table 6（tab:res-rect-mf）核验
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

SLUG = "T06_res_rect_mf"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]

# Case No. -> (Dataset 名, 该行 Fig. 列应引用的 (主图 label, 子图 label))
CASES = {
    3: ("R1", ("fig:res-128", "fig:res-128-r")),
    4: ("R2", ("fig:res-256", "fig:res-256-r")),
    5: ("R3", ("fig:res-512", "fig:res-512-r")),
    9: ("W1", ("fig:res-128", "fig:res-128-w")),
    10: ("W2", ("fig:res-256", "fig:res-256-w")),
    11: ("W3", ("fig:res-512", "fig:res-512-w")),
}
RECT, WEDGE = [3, 4, 5], [9, 10, 11]

# 正文直接引用：(说明, 正文字面量, (case, 组, 量))
PROSE = [
    ("Case 3 频均 Sol", "1.688", (3, "Overall", "sol")),
    ("Case 9 频均 Sol", "2.121", (9, "Overall", "sol")),
    ("Case 3 频均 TL", "0.951", (3, "Overall", "tl")),
    ("Case 9 频均 TL", "0.899", (9, "Overall", "tl")),
    ("Case 4 频均 Sol", "3.773", (4, "Overall", "sol")),
    ("Case 5 频均 Sol", "13.164", (5, "Overall", "sol")),
    ("Case 4 频均 TL", "1.369", (4, "Overall", "tl")),
    ("Case 5 频均 TL", "2.157", (5, "Overall", "tl")),
    ("Case 11 频均 Sol", "10.797", (11, "Overall", "sol")),
    ("Case 11 频均 TL", "1.852", (11, "Overall", "tl")),
    ("Case 3 @50Hz TL", "0.516", (3, 50, "tl")),
    ("Case 3 @75Hz TL", "1.094", (3, 75, "tl")),
    ("Case 3 @100Hz TL", "1.490", (3, 100, "tl")),
    ("Case 9 @100Hz TL", "1.265", (9, 100, "tl")),
]


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, T.number_of(LABEL))

    xl = paths.xlsx_path("4.3")
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
    rows = T.data_rows(env, ncol=13)
    raws = T.data_rows_raw(env, ncol=13)
    c.check(len(rows) == 6, "tex 数据行数 = 6", f"实得 {len(rows)}")
    printed = {int(r[0]): r for r in rows}
    printed_raw = {int(r[0].strip()): r for r in raws}
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 3-5 与 9-11",
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
    c.note("列序：No., Dataset, Fig., 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。"
           "Avg. 对应 xlsx/日志的 Overall 组。")
    order = [(25, 0), (50, 1), (75, 2), (100, 3), ("Overall", 4)]
    for no in CASES:
        c.check(printed[no][1].strip() == CASES[no][0], f"Case {no} Dataset 名",
                f"tex `{printed[no][1].strip()}`")
        for g, blk in order:
            for k, q in enumerate(("sol", "tl")):
                cell = printed[no][3 + blk * 2 + k]
                gname = "Avg." if g == "Overall" else f"{g}Hz"
                c.eq(f"Case {no} {gname} {q.upper()} (xlsx)", xd[no][g][q], cell)
                c.eq(f"Case {no} {gname} {q.upper()} (log)", ld[no][g][q], cell)

    # ── E ────────────────────────────────────────────────────────
    c.section("6. Fig. 列引用正确性")
    c.note("每行的图号必须指向该案例自己的图与子图；"
           "同一尺度下矩形取 `-r` 子图、楔形取 `-w`，错配读者会看错图。"
           "同时确认被引 label 在 aux 里存在（否则排出 `??`）。")
    aux = T.labels()
    for no, (_, (main, sub)) in CASES.items():
        got = T.refs_in(printed_raw[no][2])
        c.check(got == [main, sub], f"Case {no} Fig. 列引用",
                f"tex `{printed_raw[no][2]}` → {got}，应为 `[{main}, {sub}]`")
        for lb in (main, sub):
            c.check(lb in aux, f"label `{lb}` 已在 aux 注册",
                    f"编号 `{aux.get(lb, {}).get('num', '缺失')}`")

    # ── F ────────────────────────────────────────────────────────
    c.section("7. 几何分组小标题行")
    c.note("表内用两行 `\\multicolumn{13}` 小标题分隔矩形/楔形；"
           "它们不是数据行（会被 ncol 过滤掉），但缺失会让 6 行混为一体。")
    body = T.tabular_body(env) or ""
    for name, kw, cases in (("Rectangular waveguide", "Rectangular", RECT),
                            ("Wedge waveguide", "Wedge", WEDGE)):
        c.check(f"\\textit{{{name}}}" in body, f"小标题行 `{name}` 存在", "")
        # 该小标题之后、下一个小标题之前，出现的行号应正好是这一组
        seg = body.split(f"\\textit{{{name}}}")[-1]
        seg = re.split(r"\\textit\{", seg)[0]
        nums = [int(m.group(1)) for m in re.finditer(r"^\s*(\d+)\s*&", seg, re.M)]
        c.check(nums == cases, f"`{name}` 组下辖案例", f"实得 {nums}，应为 {cases}")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. Avg. 列与四频均值自洽")
    c.note("caption 声明 Avg. 为四频均值；四频样本数相等，故等权均值应等于 Overall 组。")
    for no in CASES:
        for q in ("sol", "tl"):
            mean = sum(xd[no][f][q] for f in M.FREQS) / 4.0
            ov = xd[no]["Overall"][q]
            c.check(abs(mean - ov) <= max(1e-9, abs(ov) * 1e-5),
                    f"Case {no} Avg. {q.upper()} = 四频均值",
                    f"均值 `{mean:.6g}` / Overall `{ov:.6g}`")

    # ── H ────────────────────────────────────────────────────────
    c.section("9. 同表小数位一致性")
    bad = []
    for no in CASES:
        for j in range(3, 13):
            v = printed[no][j]
            if not re.fullmatch(r"\d+\.\d{3}", v):
                bad.append(f"Case {no} 第{j + 1}列 `{v}`")
    c.check(not bad, "全部 60 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))

    # ── I ────────────────────────────────────────────────────────
    c.section("10. 正文引用精确性（4.3 节）")
    c.note("每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。"
           "只查①会漏掉正文与表格一起错的情形。")
    for name, lit, (no, g, q) in PROSE:
        blk = 4 if g == "Overall" else [25, 50, 75, 100].index(g)
        cell = printed[no][3 + blk * 2 + (0 if q == "sol" else 1)]
        c.check(lit == cell, f"正文 {name}", f"正文 `{lit}` / 表格 `{cell}`")
        c.eq(f"正文 {name} ← xlsx 源", xd[no][g][q], lit)

    c.section("11. 正文派生倍数（印刷值口径）")
    c.note("派生倍数一律用**表格印刷值**相除，读者才能直接复算。"
           "用全精度源值回算会得到另一个数（如 2.268 变 2.267），"
           "此前 8.676/8.670 就是这么错的。")
    tl3, tl5 = float(printed[3][12]), float(printed[5][12])
    ratio = tl5 / tl3
    c.check(f"{ratio:.3f}" == "2.268",
            "矩形多频 512m/128m TL 倍数 = 2.268",
            f"`{tl5}`/`{tl3}` = `{ratio:.6f}` → `{ratio:.3f}`")
    hits = T.sentences_with(r"factor of only \$2\.268\$", T.tex_text())
    c.check(bool(hits), "正文该倍数可定位",
            f"tex 行 {T.line_of(hits[0][0])}" if hits else "未找到")

    c.section("12. 正文趋势断言")
    c.note("正文断言“楔形在最大range反而略优”，须由表值支持。")
    s11, s5 = xd[11]["Overall"]["sol"], xd[5]["Overall"]["sol"]
    c.check(s11 < s5, "512m 处楔形 Sol < 矩形 Sol",
            f"W3 `{s11:.3f}` < R3 `{s5:.3f}`")
    for lit, no in (("10.797", 11), ("13.164", 5)):
        cell = printed[no][11]
        c.check(lit == cell, f"正文对比值 {lit} (Case {no})", f"表格 `{cell}`")


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
