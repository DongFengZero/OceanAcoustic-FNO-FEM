"""
T08_dl_abl.py — Table 8（tab:dl-abl）核验
=========================================
对象：R1 矩形域（Cases 25-28，y=71.9 m）与 W1 楔形域（Cases 29-32，y=33.4 m）
      深度线上四种消融变体的逐频 TL-MAE (dB)。R1 把原来分开的两张表（旧
      tab:dl-abl-rect / tab:dl-abl-wedge）并成一张：9 列
      `Variant | 25 50 75 100 (rect) | 25 50 75 100 (wedge)`，
      No. 列取消，行以**变体名**为键，矩形块在前（列 1-4）、楔形块在后（5-8）。

这张表**不在 xlsx 里**，源是成图脚本 `fig06_07_dl.py` 从 ep200 npz 的现场提取
（组 `ablation_R1_module_advantage` 与 `ablation_W1_module_advantage`），
故 caption 标 last epoch（承 Table 7 的 epoch convention）。核验链：

  A. 脚本同源      权威副本与 repo 副本比对
  B. 口径防漂移    从脚本对象读 GRID/METHOD/FREQS/force_y，断言未被改动（两组分别）
  C. 全精度重算    复用脚本自身函数重算，**不复制算法**（★核心）
  D. json 一致     脚本导出的 _mae_tables.json 与重算值一致
  E. 补 0 判别     `1.440`/`2.210` 之类的末位 0 必须由全精度裁定（★）
  F. 印刷值        32 格逐字符比对（两几何分别对块）
  G. 表头源坐标    8 个 (x,y) 与两组各自所选样本的 source_pos 一致（★）
  H. 图表同源      论文图件与成图脚本 out/ 产物同源（★）
  I. 加粗正确性    每列最小加粗，**两块各自取最小**；本表矩形 25 Hz 的最小值
                   落在 w/o prior supervision 上（不是 Full），加粗须跟着数走
  J. 跨表版式      与 Table 7 同用 \\TABstyleDL、同一 tabular* 总宽
  K. 正文引用      1.356 dB @75Hz / 1.834 dB @100Hz（矩形块），y=71.9 / y=33.4
  L. 消融方向性    去掉物理先验后误差显著变差；Full 在楔形四频全胜、矩形 3/4
"""
import hashlib
import os
import re

import _boot  # noqa: F401
from common import depthline as DL
from common import paths, registry, report, texparse as T

SLUG = "T08_dl_abl"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
SIB = "tab:dl-cmp"

BLOCKS = [
    dict(key="rect", title="矩形 R1", group="ablation_R1_module_advantage",
         fig="ablation_R1_module_advantage.pdf", y=71.9, domain="Rectangle",
         grpdir="Case25-32", col0=1, cases="Cases~25--28"),
    dict(key="wedge", title="楔形 W1", group="ablation_W1_module_advantage",
         fig="ablation_W1_module_advantage.pdf", y=33.4, domain="Wedge",
         grpdir="Case25-32", col0=5, cases="Cases~29--32"),
]

# tex 行序 → (No., Variant 印刷名, 脚本内变体标签)，两块共用同一组变体
ROWS = [
    (25, "Full model", "Full (Ours)"),
    (26, "w/o physics prior", "w/o prior"),
    (27, "w/o graph correction", "w/o graph"),
    (28, "w/o prior supervision", "w/o prior-sup."),
]
NO_WEDGE = [29, 30, 31, 32]
FREQS = (25, 50, 75, 100)
NCOL = 9

# 见 T08 同名说明：DL.figure_pdf() 指向 core 的 cache/（旧版大画布图），
# R1 论文用的纸面尺寸图由成图脚本写到它同级的 out/。
FIG_OUT = os.path.join(os.path.dirname(DL.AUTH), "out")


def fig_pdf(group):
    return os.path.join(FIG_OUT, f"{group}.pdf")


def pdf_md5_no_ts(p):
    """PDF 的 md5，先抹掉嵌入式创建/修改时间戳（matplotlib 每次运行都写）。"""
    if not p or not os.path.exists(p):
        return None
    b = open(p, "rb").read()
    b = re.sub(rb"/(?:CreationDate|ModDate)\s*\([^)]*\)", b"/DT(X)", b)
    return hashlib.md5(b).hexdigest()


def main_table(label):
    """该 label 自己的 tabular 源码（同浮动体内有多张表，须认 label 就近的）。"""
    return T.table_body_of(label)


def caption_before(label):
    li = T.tex_text().find(f"\\label{{{label}}}")
    if li < 0:
        return ""
    m = None
    for mm in re.finditer(r"\\captionof\{table\}\s*\{", T.tex_text()[:li]):
        m = mm
    if m is None:
        return ""
    close = T._brace_span(T.tex_text(), m.end() - 1)
    return T.tex_text()[m.end():close]


def style_span(lb):
    li = T.tex_text().find(f"\\label{{{lb}}}")
    return T.tex_text()[li:li + 200] if li >= 0 else ""


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, T.number_of(LABEL))

    c.source("印刷面 tex", paths.TEX, f"`\\label{{{LABEL}}}` 所在 tabular*")
    c.source("成图/取数脚本（权威）", DL.AUTH,
             "组 `ablation_R1_module_advantage` / `ablation_W1_module_advantage`")
    c.source("同一脚本 repo 副本", DL.COPY, "口径与权威副本同源")
    c.source("脚本导出 MAE 表", DL.MAE_JSON, "round 到 3 位，供正文取用")
    for b in BLOCKS:
        c.source(f"论文图件（{b['title']}）", os.path.join(paths.FIGDIR, b["fig"]),
                 "成图脚本 out/ 下的纸面尺寸 PDF")

    # ── A ────────────────────────────────────────────────────────
    c.section("2. 源可追溯性与脚本同源")
    c.note("深度线的口径由 `Validation_Scripts/fig06_07_dl/_depthline_core.py` 承载，"
           "成图脚本 `fig06_07_dl.py` 直接加载它、不复制算法；"
           "`common/depthline.py` 又直接 import 同一份 core，故三者口径不可能各自漂移。")
    ma, mc = DL.md5(DL.AUTH), DL.md5(DL.COPY)
    c.check(ma is not None, "权威脚本存在", paths.rel(DL.AUTH))
    c.check(os.path.exists(DL.COPY), "repo 副本存在", paths.rel(DL.COPY))
    c.check(os.path.exists(DL.MAE_JSON), "MAE json 存在", paths.rel(DL.MAE_JSON))

    m = DL.script()
    for b in BLOCKS:
        for case, p in DL.recompute(b["group"])["npz"].items():
            c.check(os.path.exists(p), f"{case} 的 ep200 npz 存在", paths.rel(p))

    # ── B ────────────────────────────────────────────────────────
    c.section("3. 提取口径防漂移")
    for name, got, want in (("插值网格 GRID", m.GRID, 300),
                            ("插值方式 METHOD", m.METHOD, "cubic"),
                            ("频率集 FREQS", tuple(m.FREQS), FREQS)):
        c.check(got == want, f"{name} = {want!r}", f"脚本内 `{got!r}`")
    for b in BLOCKS:
        cfg = m.GROUPS[b["group"]]
        for name, got, want in (("指定深度线 force_y", cfg.get("force_y"), b["y"]),
                                ("数据目录 grpdir", cfg["grpdir"], b["grpdir"]),
                                ("域类型", cfg["domain"], b["domain"])):
            c.check(got == want, f"[{b['key']}] {name} = {want!r}", f"脚本内 `{got!r}`")
        c.check([lb for _, lb in cfg["members"]] == [r[2] for r in ROWS],
                f"[{b['key']}] 脚本变体顺序与 tex 行序一致",
                " / ".join(lb for _, lb in cfg["members"]))

    # ── C ────────────────────────────────────────────────────────
    c.section("4. 全精度重算（复用脚本自身函数）")
    RR = {}
    for b in BLOCKS:
        R = DL.recompute(b["group"])
        RR[b["key"]] = R
        cfg = m.GROUPS[b["group"]]
        c.note(f"[{b['key']}] 重算落在第 {R['row']} 行，实际深度 y={R['y_line']:.6f} m；"
               f"force_y={cfg['force_y']} 取最近行，caption 写 {b['y']} m 是其一位小数。")
        c.check(abs(round(R["y_line"], 1) - b["y"]) < 1e-9,
                f"[{b['key']}] 选中行深度舍入到 1 位 = {b['y']} m",
                f"实际 `{R['y_line']:.6f}`")

    env, star = main_table(LABEL)
    c.check(env is not None, "tex 表体可定位", f"长度 {len(env or '')}")
    c.check(star, "表体为 tabular*（固定总宽）", f"is_star={star}")
    cap = caption_before(LABEL) or ""
    flat = cap.replace("$", "").replace("\\,", "").replace(" ", "")
    for b in BLOCKS:
        c.check(f"y={b['y']}" in flat,
                f"caption 声明 {b['key']} 深度 y={b['y']} m（与重算一致）",
                "caption 含该值")
        c.check(b["cases"] in flat, f"caption 声明 {b['key']} 的 {b['cases']}", "")
    c.check("\\ref{tab:dl-cmp}" in cap,
            "caption 以 Table 7 交代 header/emphasis/epoch 约定（含 epoch）",
            "故本表不再重复 last epoch 字样")

    # ── D / E ────────────────────────────────────────────────────
    c.section("5. json 与全精度重算一致")
    for b in BLOCKS:
        R = RR[b["key"]]
        jg = DL.mae_json()[b["group"]]
        c.check(abs(jg["y_line"] - round(R["y_line"], 2)) < 1e-9,
                f"[{b['key']}] json y_line 与重算一致",
                f"json `{jg['y_line']}` / 重算 `{round(R['y_line'], 2)}`")
        for f in FREQS:
            for k, (_, _, lab) in enumerate(ROWS):
                a, bb = jg["mae_table"][str(f)][lab], R["er"][f][k]
                c.check(abs(a - round(bb, 3)) < 1e-12,
                        f"[{b['key']}] {f}Hz {lab} json vs 重算",
                        f"json `{a}` / 重算 `{bb:.9f}`")

    # ── F ────────────────────────────────────────────────────────
    c.section("6. 印刷值比对（全精度舍入到 3 位 vs tex）")
    c.note("判定用全精度值，不用 json —— json 已是 round(...,3)。本表含大量"
           "两位整数级 MAE（去先验后 26-40 dB），末位 0 的格子尤须回溯全精度"
           "确认第 3 位真的是 0。行以变体名为键，矩形块占列 1-4、楔形块占列 5-8。")
    rows = T.data_rows(env, ncol=NCOL)
    c.check(len(rows) == 4, "tex 数据行数 = 4", f"实得 {len(rows)}")
    printed = {r[0].strip(): r for r in rows}
    c.check(list(printed) == [r[1] for r in ROWS], "行以变体名为键且顺序一致",
            " / ".join(printed))
    for k, (no, var, lab) in enumerate(ROWS):
        c.check(var in printed, f"行 `{var}` 存在", "")
        for b in BLOCKS:
            for j, f in enumerate(FREQS):
                c.eq(f"{var} {b['key']} {f}Hz", RR[b["key"]]["er"][f][k],
                     printed[var][b["col0"] + j])

    zeros = []
    for k, (no, var, _) in enumerate(ROWS):
        for b in BLOCKS:
            for j, f in enumerate(FREQS):
                cell = printed[var][b["col0"] + j]
                if cell.endswith("0"):
                    zeros.append((var, b["key"], f, cell, RR[b["key"]]["er"][f][k]))
    c.section("7. 末位为 0 的单元格：真值还是补 0")
    c.note("凡印刷值末位为 0 的格，单看数字无法排除『2 位补 1 个 0』，"
           "逐个回溯全精度源值确认第 3 位确实是 0 或由进位得到。")
    for var, key, f, cell, full in zeros:
        c.check(f"{full:.3f}" == cell, f"{var} {key} {f}Hz 末位 0 可由全精度复现",
                f"全精度 {full:.9f} → `{cell}`")
    c.check(True, f"末位为 0 的格子共 {len(zeros)} 个，全部回溯完毕", "")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 表头源坐标与所选样本一致（两块各 4 个）")
    c.note("表头每频率标 $(x,y)$（`\\srcxy`），须等于该频率**实际选中样本**的 "
           "source_pos；八个坐标互不相同，写错不会报编译错。")
    hdr = T.header_row(env) or ""
    got = [tuple(float(v) for v in mm)
           for mm in re.findall(r"\\srcxy\{([\d.]+)\}\{([\d.]+)\}", hdr)]
    c.check(len(got) == 8, "表头解析到 8 组源坐标（4 矩形 + 4 楔形）", str(got))
    for b in BLOCKS:
        for j, f in enumerate(FREQS):
            idx = (0 if b["key"] == "rect" else 4) + j
            sx, sy = RR[b["key"]]["src"][f]
            want = (round(sx, 1), round(sy, 1))
            c.check(idx < len(got) and got[idx] == want,
                    f"{b['key']} {f}Hz 源坐标",
                    f"tex `{got[idx] if idx < len(got) else '缺'}` / "
                    f"样本 {RR[b['key']]['sample'][f]} 实际 "
                    f"({sx:.5f}, {sy:.5f}) → `{want}`")

    # ── H ────────────────────────────────────────────────────────
    c.section("9. 表与图同源（Table 8 ↔ Fig. 的两块）")
    c.note("MAE 表和深度线图是同一次选线/选样本的两个产物。比对论文图件与成图"
           "脚本 out/ 下同名 PDF：内容逐字节相同（仅嵌入时间戳不同，比对前抹掉），"
           "则『表里的数』与『图里的线』必定来自同一次计算。")
    for b in BLOCKS:
        src_pdf = fig_pdf(b["group"])
        dst_pdf = os.path.join(paths.FIGDIR, b["fig"])
        c.check(os.path.exists(src_pdf), f"[{b['key']}] 脚本产出 PDF 存在",
                paths.rel(src_pdf))
        c.check(os.path.exists(dst_pdf), f"[{b['key']}] 论文图件存在",
                paths.rel(dst_pdf))
        h1, h2 = pdf_md5_no_ts(src_pdf), pdf_md5_no_ts(dst_pdf)
        c.check(h1 is not None and h1 == h2,
                f"[{b['key']}] 论文图件与脚本产物同源（抹时间戳后同 md5）",
                f"md5(no-ts) `{h1}`")
    c.exempt("PDF 逐字节 md5 相同",
             "matplotlib 每次运行写入 CreationDate（本机实测 D:2026…），"
             "逐字节比对必然不等；已改为抹掉时间戳后比对，同源判定不受影响。")

    # ── I ────────────────────────────────────────────────────────
    c.section("10. 加粗正确性（Best in bold，两块各自取列最小）")
    c.note("caption 声明『emphasis as in Table 7』，即每列最优加粗；并排后每列"
           "分属不同几何，最小值必须在各自块内取。**本表矩形 25 Hz 的最小值落在 "
           "w/o prior supervision（0.540）而非 Full model**，加粗须跟着数走。")
    mask = T.bold_mask(env, ncol=NCOL)
    bm = {rows[i][0].strip(): mask[i] for i in range(len(rows))}
    for b in BLOCKS:
        for j, f in enumerate(FREQS):
            col = [RR[b["key"]]["er"][f][k] for k in range(len(ROWS))]
            kbest = min(range(len(col)), key=lambda t: col[t])
            want_m = ROWS[kbest][1]
            got_m = [mm for mm in bm if bm[mm][b["col0"] + j]]
            c.check(got_m == [want_m], f"{b['key']} {f}Hz 加粗落在最小值行",
                    f"加粗 {got_m} / 最小值 {want_m} (`{col[kbest]:.3f}`)")

    # ── H2 ───────────────────────────────────────────────────────
    c.section("11. 同表小数位一致性")
    bad = [f"{var} {b['key']} {f}Hz `{printed[var][b['col0'] + j]}`"
           for _, var, _ in ROWS for b in BLOCKS for j, f in enumerate(FREQS)
           if not re.fullmatch(r"\d+\.\d{3}", printed[var][b["col0"] + j])]
    c.check(not bad, "全部 32 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))

    # ── J ────────────────────────────────────────────────────────
    c.section("12. 与 Table 7 的版式一致性")
    sib, sib_star = main_table(SIB)
    c.check(sib is not None, "Table 7 表体可定位", f"长度 {len(sib or '')}")
    c.check(sib_star, "Table 7 亦为 tabular*", f"is_star={sib_star}")
    p9, p8 = T.tabular_preamble(env), T.tabular_preamble(sib)
    c.check(p9 is not None and p8 is not None, "两表列定义可解析",
            f"Table 8 `{p9}` / Table 7 `{p8}`")
    c.check(p9 is not None and p9.endswith("EEEE EEEE@{}"),
            "Table 8 列类型序列为 `A EEEE EEEE`", f"`{p9}`")
    c.check(p8 is not None and p8.endswith("EEEE EEEE@{}"),
            "Table 7 列类型序列为 `M EEEE EEEE`（首列标签列类型名不同，宽度同）",
            f"`{p8}`")
    for p, nm in ((p9, "Table 8"), (p8, "Table 7")):
        c.check(p is not None and "extracolsep" in p,
                f"{nm} 用 \\extracolsep{{\\fill}} 均分列间余量", f"`{p}`")
    c.check("\\TABstyleDL" in style_span(LABEL) and "\\TABstyleDL" in style_span(SIB),
            "两表同用 \\TABstyleDL（整表紧凑列距）", "")

    widths = {}
    for lb in (LABEL, SIB):
        e, _ = main_table(lb)
        mm = re.search(r"\\begin\{tabular\*\}\{([^}]*)\}", e or "")
        widths[lb] = mm.group(1) if mm else None
    same = len(set(widths.values())) == 1 and None not in widths.values()
    c.check(same, "两表的 tabular* 总宽参数一致（等宽并排）",
            " / ".join(f"{k.split(':')[1]}=`{v}`" for k, v in widths.items()))

    # ── K ────────────────────────────────────────────────────────
    c.section("13. 正文引用精确性（4.5 节）")
    c.note("正文：`the graph correction provides particularly strong improvements "
           "at the higher frequencies, reducing the TL by $1.356$\\,dB at $75$\\,Hz "
           "and $1.834$\\,dB at $100$\\,Hz`（矩形块）。这两数是 w/o graph 与 "
           "Full model 之差。★ 须注意正文是按**表中印出的 3 位值**相减，"
           "与全精度相减在第 3 位可能差 1；两者分别核验，不混为一谈。")
    k_full, k_ng = 0, 2                       # Full model / w/o graph correction
    c.note("口径：正文的派生量按**表中印出的 3 位值**计算，与 4.3 节的 8.676 "
           "同源（3.852/0.444 用印刷值，全精度会得 8.670）。故此处以印刷值"
           "口径为准；全精度差值一并列出，若有第 3 位差异，读者能在报告里看到"
           "它来自口径而非数据。")
    for f, want in ((75, "1.356"), (100, "1.834")):
        e = RR["rect"]["er"][f]
        full = e[k_ng] - e[k_full]                      # 全精度相减
        iprt = round(e[k_ng], 3) - round(e[k_full], 3)  # 印刷值相减（正文口径）
        c.check(f"{iprt:.3f}" == want,
                f"正文 {want} dB @{f}Hz 由表中印刷值复现（正文口径）",
                f"`{round(e[k_ng], 3):.3f} − {round(e[k_full], 3):.3f} = {iprt:.3f}`")
        c.note(f"{f}Hz：全精度相减得 `{full:.9f}` → `{full:.3f}`；"
               + ("与正文同" if f"{full:.3f}" == want
                  else f"与正文的 {want} 差在末位，源于印刷值四舍五入，非数据出入"))

    txt = T.tex_text()
    for y in (71.9, 33.4):
        hits = T.sentences_with(re.escape(f"y={y}"), txt)
        c.check(bool(hits), f"深度线深度 y={y} m 在文中声明且与脚本 force_y 一致",
                f"tex 行 {T.line_of(hits[0][0])}" if hits else "未找到")
    c.note("4.5 节正文未以低位数复述本表单点深度线数值，故不设正文数值比对；"
           "正文的 `tens of decibels` 已由『去先验后 26-41 dB』的列值印证。")
    tens = [RR[b["key"]]["er"][f][1] for b in BLOCKS for f in FREQS]
    c.check(min(tens) >= 5.0, "正文『raises the depth-line TL to tens of decibels』成立",
            f"w/o prior 最小 `{min(tens):.3f}` dB（全部频率、两几何）")

    # ── L ────────────────────────────────────────────────────────
    c.section("14. 消融方向性（去掉模块应变差）")
    c.note("物理先验是主导项：去掉后误差应显著变差。楔形块 Full 四频全胜，"
           "矩形块 50-100 Hz Full 领先、25 Hz 由 w/o prior supervision 略胜——"
           "两处方向都必须由表内值直接印证，不套用结论。")
    for f in FREQS:
        a, bb = RR["rect"]["er"][f][1], RR["rect"]["er"][f][0]
        c.check(a > bb * 5, f"rect {f}Hz 去掉物理先验后误差 >5× Full",
                f"w/o prior `{a:.3f}` vs Full `{bb:.3f}` ({a / bb:.1f}×)")
    for f in FREQS:
        a, bb = RR["wedge"]["er"][f][1], RR["wedge"]["er"][f][0]
        c.check(a > bb * 5, f"wedge {f}Hz 去掉物理先验后误差 >5× Full",
                f"w/o prior `{a:.3f}` vs Full `{bb:.3f}` ({a / bb:.1f}×)")
    w_wedge = sum(1 for f in FREQS if RR["wedge"]["er"][f][0] == min(RR["wedge"]["er"][f]))
    c.check(w_wedge == 4, "楔形块 Full 在 4 个频率中全部占优",
            f"占优频率数 {w_wedge}")
    w_rect = sum(1 for f in FREQS if RR["rect"]["er"][f][0] == min(RR["rect"]["er"][f]))
    c.check(w_rect == 3, "矩形块 Full 在 4 个频率中占优 3 个（25 Hz 除外）",
            f"占优频率数 {w_rect}")
    # 正文对矩形块的表述须与上面 3/4 的事实一致
    c.check("the full model leading from $50$ to $100$\\,Hz" in
            T.tex_text().replace("\n", " "),
            "正文『the full model leading from 50 to 100 Hz』与矩形块 3/4 一致",
            "25 Hz 另由 w/o prior supervision 略胜")

    return c


if __name__ == "__main__":
    import sys
    sys.exit(run().finish())
