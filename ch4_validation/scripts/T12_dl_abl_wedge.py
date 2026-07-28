"""
T12_dl_abl_wedge.py — Table 12（tab:dl-abl-wedge）核验
====================================================
对象：W1 楔形域、y=33.4 m 深度线上四种消融变体的逐频 TL-MAE (dB)，
      6 列：No. / Method / 25Hz / 50Hz / 75Hz / 100Hz，表头带各频源坐标。

这张表**不在 xlsx 里**，源是成图脚本 `advantage_depth_line.py` 从 ep200 npz
的现场提取（组 `ablation_W1_module_advantage`），故 caption 标 last epoch。
核验链与 Table 4/6/7/8 完全不同：

  A. 脚本同源      权威副本 D:\\Data 与 repo 副本 md5 比对
  B. 口径防漂移    从脚本对象读 GRID/METHOD/FREQS/force_y，断言未被改动
  C. 全精度重算    复用脚本自身函数重算，**不复制算法**（★核心）
  D. json 一致     脚本导出的 _mae_tables.json 与重算值一致
  E. 补 0 判别     json 只存 round(er,3)，`1.440`/`2.210` 真伪必须靠全精度裁定（★）
  F. 印刷值        16 格逐字符比对
  G. 表头源坐标    4 个 (x,y) 与所选样本的 source_pos 一致（★）
  H. 图表同源      论文 Fig.13 的 PDF 与 MAE 表出自同一次运行，md5 比对（★）
  I. 加粗正确性    Best in bold 须真的落在每列最小值上——本表 Full 四频全胜
                   （与 Table 11 的 R1 不同），加粗必须跟着数走而非跟着结论走
  J. 跨表版式      与 Table 11 列定义/表头一致（并列 minipage，须等宽）
  K. 正文引用      4.5 节以全测试集误差（Tables 15/16）论述，本表无直接引用；
                   改为反向核验『正文未以 2 位小数复述本表数值』
  L. 结论方向性    去掉物理先验后误差应显著变差（>5×），验证消融的物理意义
"""
import os
import re

import _boot  # noqa: F401
from common import depthline as DL
from common import paths, registry, report, texparse as T

SLUG = "T12_dl_abl_wedge"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
GROUP = "ablation_W1_module_advantage"
SIB = "tab:dl-abl-rect"
FIG_LABEL = "fig:dl-abl-wedge"
FIG_FILE = "ablation_W1_module_advantage.pdf"

# tex 行序 → (No., Method 印刷名, 脚本内方法标签)
ROWS = [
    (29, "Full model", "Full (Ours)"),
    (30, "w/o physics prior", "w/o prior"),
    (31, "w/o graph correction", "w/o graph"),
    (32, "w/o prior supervision", "w/o prior-sup."),
]
FREQS = (25, 50, 75, 100)


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, T.number_of(LABEL))

    c.source("印刷面 tex", paths.TEX, f"`\\label{{{LABEL}}}` 所在 minipage")
    c.source("成图/取数脚本（权威）", DL.AUTH, "组 `ablation_W1_module_advantage`")
    c.source("同一脚本 repo 副本", DL.COPY, "md5 应与权威副本相同")
    c.source("脚本导出 MAE 表", DL.MAE_JSON, "round 到 3 位，供正文取用")
    c.source("论文图件", os.path.join(paths.FIGDIR, FIG_FILE),
             f"Fig.~\\ref{{{FIG_LABEL}}}，应与脚本产物逐字节相同")

    # ── A ────────────────────────────────────────────────────────
    c.section("2. 源可追溯性与脚本同源")
    c.note("脚本用 `ROOT = dirname(__file__)` 定位数据与产物，只有位于 "
           "`D:\\Data` 下才能同时命中 `ROOT/Case25-32` 与 `ROOT/重绘结果`；"
           "repo 内 `Validation_Scripts/` 那份是副本，md5 相同但路径不通。")
    ma, mc = DL.md5(DL.AUTH), DL.md5(DL.COPY)
    c.check(ma is not None, "权威脚本存在", paths.rel(DL.AUTH))
    c.check(ma == mc, "repo 副本与权威副本 md5 相同", f"`{ma}`")
    c.check(os.path.exists(DL.MAE_JSON), "MAE json 存在", paths.rel(DL.MAE_JSON))

    m = DL.script()
    for case, p in DL.recompute(GROUP)["npz"].items():
        c.check(os.path.exists(p), f"{case} 的 ep200 npz 存在", paths.rel(p))

    # ── B ────────────────────────────────────────────────────────
    c.section("3. 提取口径防漂移")
    c.note("口径直接从脚本对象读出再断言，脚本改了这里立刻失败，"
           "不会出现『核验脚本按旧口径算、论文按新口径印』的错位。")
    cfg = m.GROUPS[GROUP]
    for name, got, want in (("插值网格 GRID", m.GRID, 300),
                            ("插值方式 METHOD", m.METHOD, "cubic"),
                            ("频率集 FREQS", tuple(m.FREQS), FREQS),
                            ("指定深度线 force_y", cfg.get("force_y"), 33.4),
                            ("数据目录 grpdir", cfg["grpdir"], "Case25-32"),
                            ("域类型", cfg["domain"], "Wedge")):
        c.check(got == want, f"{name} = {want!r}", f"脚本内 `{got!r}`")
    c.check([lb for _, lb in cfg["members"]] == [r[2] for r in ROWS],
            "脚本方法顺序与 tex 行序一致",
            " / ".join(lb for _, lb in cfg["members"]))

    # ── C ────────────────────────────────────────────────────────
    c.section("4. 全精度重算（复用脚本自身函数）")
    R = DL.recompute(GROUP)
    c.note(f"重算落在第 {R['row']} 行，实际深度 y={R['y_line']:.6f} m；"
           f"force_y={cfg['force_y']} 取最近行，caption 写 33.4 m 是其一位小数。")
    c.check(abs(round(R["y_line"], 1) - 33.4) < 1e-9,
            "选中行深度舍入到 1 位 = 33.4 m", f"实际 `{R['y_line']:.6f}`")
    cap = T.caption_of(LABEL) or ""
    c.check("y=33.4" in cap.replace("$", "").replace("\\,", "").replace(" ", ""),
            "caption 深度值与重算一致", "caption 含 `y=33.4\\,m`")
    c.check("last epoch" in cap, "caption 声明 last epoch",
            "深度线由 ep200 npz 现场提取，非 best epoch 汇总")

    # ── D / E ────────────────────────────────────────────────────
    c.section("5. json 与全精度重算一致")
    jg = DL.mae_json()[GROUP]
    c.check(abs(jg["y_line"] - round(R["y_line"], 2)) < 1e-9,
            "json y_line 与重算一致", f"json `{jg['y_line']}` / 重算 `{round(R['y_line'], 2)}`")
    for f in FREQS:
        for k, (_, _, lab) in enumerate(ROWS):
            a, b = jg["mae_table"][str(f)][lab], R["er"][f][k]
            c.check(abs(a - round(b, 3)) < 1e-12, f"{f}Hz {lab} json vs 重算",
                    f"json `{a}` / 重算 `{b:.9f}`")

    # ── F ────────────────────────────────────────────────────────
    c.section("6. 印刷值比对（全精度舍入到 3 位 vs tex）")
    c.note("判定用全精度值，不用 json —— json 已是 round(...,3)，"
           "拿它比对等于自证，无法识别补 0（如 w/o graph@25Hz 印 `1.440`，"
           "全精度须确认第 3 位真是 0）。")
    env = T.table_env(LABEL)
    c.check(env is not None and f"\\label{{{LABEL}}}" in env,
            "tex 表格环境可定位", f"长度 {len(env or '')}")
    rows = T.data_rows(env, ncol=6)
    c.check(len(rows) == 4, "tex 数据行数 = 4", f"实得 {len(rows)}")
    printed = {int(r[0]): r for r in rows}
    c.check(set(printed) == {r[0] for r in ROWS}, "行 No. 覆盖 Case 29-32",
            str(sorted(printed)))
    for k, (no, meth, lab) in enumerate(ROWS):
        c.check(printed[no][1].strip() == meth, f"Case {no} Method 名",
                f"tex `{printed[no][1].strip()}`")
        for j, f in enumerate(FREQS):
            c.eq(f"Case {no} {f}Hz", R["er"][f][k], printed[no][2 + j])

    # 补 0 判别：报告里显式列出末位为 0 的格子及其全精度来源
    zeros = []
    for k, (no, _, _) in enumerate(ROWS):
        for j, f in enumerate(FREQS):
            cell = printed[no][2 + j]
            if cell.endswith("0"):
                zeros.append((no, f, cell, R["er"][f][k]))
    c.section("7. 末位为 0 的单元格：真值还是补 0")
    c.note("凡印刷值末位为 0 的格，单看数字无法排除『2 位补 1 个 0』，"
           "逐个回溯全精度源值确认第 3 位确实是 0 或由进位得到。")
    if not zeros:
        c.check(True, "无末位为 0 的单元格", "不适用")
    for no, f, cell, full in zeros:
        c.check(f"{full:.3f}" == cell, f"Case {no} {f}Hz 末位 0 可由全精度复现",
                f"全精度 {full:.9f} → `{cell}`")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 表头源坐标与所选样本一致")
    c.note("表头每频率标 $(x,y)$，须等于该频率**实际选中样本**的 source_pos；"
           "选线算法逐频独立挑样本，四个坐标互不相同，写错不会报编译错。")
    hdr = T.header_row(env) or ""
    # 坐标为 1 位小数（全章统一口径），正则须容纳小数点
    got = [tuple(float(v) for v in mm)
           for mm in re.findall(r"\$\(([\d.]+),([\d.]+)\)\$", hdr)]
    c.check(len(got) == 4, "表头解析到 4 组源坐标", str(got))
    for j, f in enumerate(FREQS):
        sx, sy = R["src"][f]
        want = (round(sx, 1), round(sy, 1))
        c.check(j < len(got) and got[j] == want, f"{f}Hz 源坐标",
                f"tex `{got[j] if j < len(got) else '缺'}` / "
                f"样本 {R['sample'][f]} 实际 ({sx:.5f}, {sy:.5f}) → `{want}`")

    # ── H ────────────────────────────────────────────────────────
    c.section("9. 表与图同源（Table 12 ↔ Fig. 13）")
    c.note("MAE 表和深度线图是同一次 build_group 的两个产物。"
           "比对论文图件与脚本输出目录下同名 PDF 的 md5：相同则"
           "『表里的数』与『图里的线』必定来自同一次计算，不可能各自漂移。")
    src_pdf = DL.figure_pdf(GROUP)
    dst_pdf = os.path.join(paths.FIGDIR, FIG_FILE)
    m1, m2 = DL.md5(src_pdf), DL.md5(dst_pdf)
    c.check(m1 is not None, "脚本产出 PDF 存在", paths.rel(src_pdf))
    c.check(m2 is not None, "论文图件存在", paths.rel(dst_pdf))
    c.check(m1 == m2, "两者逐字节相同", f"md5 `{m1}`")
    aux = T.labels()
    c.check(FIG_LABEL in aux, f"`{FIG_LABEL}` 已在 aux 注册",
            f"编号 `{aux.get(FIG_LABEL, {}).get('num', '缺失')}`")
    figcap = T.caption_of(FIG_LABEL) or ""
    c.check("33.4" in figcap, "图注深度与表一致", "图注含 `y=33.4\\,m`")
    c.check("last epoch" in figcap, "图注声明 last epoch", "")

    # ── I ────────────────────────────────────────────────────────
    c.section("10. 加粗正确性（Best in bold）")
    mask = T.bold_mask(env, ncol=6)
    bm = {int(T.clean_cell(rows[i][0])): mask[i] for i in range(len(rows))}
    for j, f in enumerate(FREQS):
        col = [R["er"][f][k] for k in range(len(ROWS))]
        kbest = min(range(len(col)), key=lambda t: col[t])
        want_no = ROWS[kbest][0]
        got_no = [no for no in bm if bm[no][2 + j]]
        c.check(got_no == [want_no], f"{f}Hz 加粗落在最小值行",
                f"加粗 {got_no} / 最小值 Case {want_no} (`{col[kbest]:.3f}`)")

    # ── H2 ───────────────────────────────────────────────────────
    c.section("11. 同表小数位一致性")
    bad = [f"Case {no} {f}Hz `{printed[no][2 + j]}`"
           for no, _, _ in ROWS for j, f in enumerate(FREQS)
           if not re.fullmatch(r"\d+\.\d{3}", printed[no][2 + j])]
    c.check(not bad, "全部 16 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))

    # ── J ────────────────────────────────────────────────────────
    c.section("12. 与 Table 11 的版式一致性")
    sib = T.table_env(SIB) or ""
    a, b = T.tabular_preamble(env), T.tabular_preamble(sib)
    c.check(a is not None and a == b, "列定义与 Table 11 相同",
            f"Table 12 `{a}` / Table 11 `{b}`")
    c.check(a == "@{}QA EEEE@{}", "列定义为消融深度线族专用 `@{}QA EEEE@{}`", f"`{a}`")
    c.check("\\TABstyle" in (env or "") and "\\TABstyle" in sib,
            "两表同用 \\TABstyle", "")

    # ── K ────────────────────────────────────────────────────────
    c.section("13. 正文引用精确性（4.5 节）")
    c.note("4.5 节正文以 Tables 15/16 的全测试集误差为论述依据，未直接引用本表的"
           "单点深度线数值；故本节只核验『表内值未被正文以低位数复述』。")
    txt = T.tex_text()
    body = T.body_text("\\subsection{Ablation Study}",
                       "\\subsection{Mesh Independence}", txt)
    leaked = []
    for no, _, _ in ROWS:
        for j, f in enumerate(FREQS):
            cell = printed[no][2 + j]
            two = f"{float(cell):.2f}"
            if two != cell and re.search(rf"(?<![\d.]){re.escape(two)}(?![\d])", body):
                leaked.append(f"Case {no} {f}Hz 印 `{cell}` 正文疑似 `{two}`")
    c.check(not leaked, "正文未以 2 位小数复述本表数值",
            "无低位数复述" if not leaked else "；".join(leaked))
    hits = T.sentences_with(r"y=33\.4", txt)
    c.check(bool(hits), "深度线深度 y=33.4 m 在 caption 中声明且与脚本 force_y 一致",
            f"tex 行 {T.line_of(hits[0][0])}" if hits else "未找到")

    # ── L ────────────────────────────────────────────────────────
    c.section("14. 消融结论方向性（去掉模块应变差）")
    c.note("与 Table 11（R1）不同，本表 Full model 四个频率全部最小，故加粗全部"
           "落在 Case 29 行；此处断言物理先验是主导项，且 Full 的逐频占优是真实的。")
    for f in FREQS:
        col = R["er"][f]
        c.check(col[1] > col[0] * 5, f"{f}Hz 去掉物理先验后误差 >5× Full",
                f"w/o prior `{col[1]:.3f}` vs Full `{col[0]:.3f}` "
                f"({col[1] / col[0]:.1f}×)")
    wins = sum(1 for f in FREQS if R["er"][f][0] == min(R["er"][f]))
    c.check(wins == 4, "Full 在 4 个频率中全部占优（与 R1 表不同）",
            f"占优频率数 {wins}")

    return c


if __name__ == "__main__":
    import sys
    sys.exit(run().finish())
