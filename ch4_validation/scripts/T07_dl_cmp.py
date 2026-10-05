"""
T07_dl_cmp.py — Table 7（tab:dl-cmp）核验
=========================================
对象：R1 矩形域（Cases 15-19，y=56.1 m）与 W1 楔形域（Cases 20-24，y=30.4 m）
      深度线上五种方法的逐频 TL-MAE (dB)。R1 把原来分开的两张表（旧
      tab:dl-cmp-rect / tab:dl-cmp-wedge）并成一张：9 列
      `Method | 25 50 75 100 (rect) | 25 50 75 100 (wedge)`，
      No. 列取消，行以**方法名**为键，矩形块在前（列 1-4）、楔形块在后（5-8）。

这张表**不在 xlsx 里**，源是成图脚本 `fig06_07_dl.py` 从 ep200 npz 的现场提取
（组 `comparison_R1_model_advantage` 与 `comparison_W1_model_advantage`），
故 caption 标 last epoch。核验链与 Table 4/5/6/9-13 完全不同：

  A. 脚本同源      权威副本与 repo 副本 md5 比对
  B. 口径防漂移    从脚本对象读 GRID/METHOD/FREQS/force_y，断言未被改动（两组分别）
  C. 全精度重算    复用脚本自身函数重算，**不复制算法**（★核心）
  D. json 一致     脚本导出的 _mae_tables.json 与重算值一致
  E. 补 0 判别     json 只存 round(er,3)，`1.210` 真伪必须靠全精度裁定（★）
  F. 印刷值        40 格逐字符比对（两几何分别对块）
  G. 表头源坐标    8 个 (x,y) 与两组各自所选样本的 source_pos 一致（★）
  H. 图表同源      论文 Fig. 的 PDF 与 MAE 表出自同一次运行（★）
  I. 加粗正确性    Best in bold 须真的落在每列最小值上，**两块各自取最小**
  J. 跨表版式      与 Table 8 用同一 \\TABstyleDL 与同一 tabular* 总宽
  K. 正文引用      1.515 / 0.666 / y=56.1 / y=30.4 / DeepONet exceeds 5 dB
"""
import hashlib
import os
import re

import _boot  # noqa: F401
from common import depthline as DL
from common import paths, registry, report, texparse as T

SLUG = "T07_dl_cmp"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
SIB = "tab:dl-abl"

# 两个几何块：每个块自带脚本组、图件与列偏移
#   key / 脚本组名 / 论文图件 / 数据列起点（0 起）
BLOCKS = [
    dict(key="rect", title="矩形 R1", group="comparison_R1_model_advantage",
         fig="comparison_R1_model_advantage.pdf", y=56.1, domain="Rectangle",
         grpdir="Case15-24", col0=1),
    dict(key="wedge", title="楔形 W1", group="comparison_W1_model_advantage",
         fig="comparison_W1_model_advantage.pdf", y=30.4, domain="Wedge",
         grpdir="Case15-24", col0=5),
]

# tex 行序 → (No., Method 印刷名, 脚本内方法标签)，两块共用同一组方法
ROWS = [
    (15, "Proposed", "Proposed (Ours)"),
    (16, "DeepONet", "DeepONet"),
    (17, "FNO", "FNO"),
    (18, "KNO", "KNO"),
    (19, "CNO", "CNO"),
]
# 楔形块的 No. 只是核验用的定位符（印刷面已无 No. 列），与 tex memo 对齐
NO_WEDGE = [20, 21, 22, 23, 24]
FREQS = (25, 50, 75, 100)
NCOL = 9

# DL.FIG_DIR / DL.figure_pdf() 指向 fig06_07_dl/cache/，那儿放的是 core 自己
# 的旧版大画布图（15.5x12.5 in）；R1 论文用的纸面尺寸图由**成图脚本
# fig06_07_dl.py** 写到它同级的 out/。核验以 out/ 为准（已实测与论文图件
# 除嵌入时间戳外逐字节相同）。
FIG_OUT = os.path.join(os.path.dirname(DL.AUTH), "out")


def fig_pdf(group):
    """成图脚本 out/ 下的纸面尺寸 PDF（论文图件的来源）。"""
    return os.path.join(FIG_OUT, f"{group}.pdf")


def pdf_md5_no_ts(p):
    """PDF 的 md5，但先抹掉嵌入式创建/修改时间戳。

    matplotlib 每次都写入 CreationDate，逐字节比对必然不等；抹掉时间戳后
    若仍相同，则两文件的页面内容、字体、流对象完全一致，可判定同源。
    """
    if not p or not os.path.exists(p):
        return None
    b = open(p, "rb").read()
    b = re.sub(rb"/(?:CreationDate|ModDate)\s*\([^)]*\)", b"/DT(X)", b)
    return hashlib.md5(b).hexdigest()


def main_table(label):
    """该 label 自己的 tabular 源码。

    R1 把多张表绑进同一个 figure* 浮动体，T.table_env() 会解析到同浮动体内的
    邻居（实测 tab:dl-abl 取回了 tab:dl-cmp 的 tabular），故这里一律走
    T.table_body_of()，并且 caption 也从 label 往前就地取，不用 caption_of()。
    """
    src, star = T.table_body_of(label)
    return src, star


def caption_before(env_src, label):
    """label 紧邻其上的 captionof 文本（tab:dl-cmp 排法为 caption→label→tabular）。"""
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


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, T.number_of(LABEL))

    c.source("印刷面 tex", paths.TEX, f"`\\label{{{LABEL}}}` 所在 tabular*")
    c.source("成图/取数脚本（权威）", DL.AUTH,
             "组 `comparison_R1_model_advantage` / `comparison_W1_model_advantage`")
    c.source("同一脚本 repo 副本", DL.COPY, "md5 应与权威副本相同")
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
        R = DL.recompute(b["group"])
        for case, p in R["npz"].items():
            c.check(os.path.exists(p), f"{case} 的 ep200 npz 存在", paths.rel(p))

    # ── B ────────────────────────────────────────────────────────
    c.section("3. 提取口径防漂移")
    c.note("口径直接从脚本对象读出再断言，脚本改了这里立刻失败，"
           "不会出现『核验脚本按旧口径算、论文按新口径印』的错位。")
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
                f"[{b['key']}] 脚本方法顺序与 tex 行序一致",
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
    cap = caption_before(env, LABEL) or ""
    flat = cap.replace("$", "").replace("\\,", "").replace(" ", "")
    for b in BLOCKS:
        c.check(f"y={b['y']}" in flat,
                f"caption 声明 {b['key']} 深度 y={b['y']} m（与重算一致）",
                "caption 含该值")
    c.check("last epoch" in cap, "caption 声明 last epoch",
            "深度线由 ep200 npz 现场提取，非 best epoch 汇总")
    c.check("Cases~15--19" in flat and "Cases~20--24" in flat,
            "caption 声明两组 Case 区间 15-19 / 20-24", "")

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
    c.note("判定用全精度值，不用 json —— json 已是 round(...,3)，"
           "拿它比对等于自证，无法识别补 0（如 KNO@25Hz 印 `1.210`，"
           "全精度 1.210xxx 才是真值来源）。行以方法名为键，矩形块占列 1-4、"
           "楔形块占列 5-8。")
    rows = T.data_rows(env, ncol=NCOL)
    c.check(len(rows) == 5, "tex 数据行数 = 5", f"实得 {len(rows)}")
    printed = {r[0].strip(): r for r in rows}
    c.check(list(printed) == [r[1] for r in ROWS], "行以方法名为键且顺序一致",
            " / ".join(printed))
    for k, (no, meth, lab) in enumerate(ROWS):
        c.check(meth in printed, f"行 `{meth}` 存在", "")
        for b in BLOCKS:
            for j, f in enumerate(FREQS):
                c.eq(f"{meth} {b['key']} {f}Hz", RR[b["key"]]["er"][f][k],
                     printed[meth][b["col0"] + j])

    # 补 0 判别：报告里显式列出末位为 0 的格子及其全精度来源
    zeros = []
    for k, (no, meth, _) in enumerate(ROWS):
        for b in BLOCKS:
            for j, f in enumerate(FREQS):
                cell = printed[meth][b["col0"] + j]
                if cell.endswith("0"):
                    zeros.append((meth, b["key"], f, cell, RR[b["key"]]["er"][f][k]))
    c.section("7. 末位为 0 的单元格：真值还是补 0")
    c.note("凡印刷值末位为 0 的格，单看数字无法排除『2 位补 1 个 0』，"
           "逐个回溯全精度源值确认第 3 位确实是 0 或由进位得到。")
    for meth, key, f, cell, full in zeros:
        c.check(f"{full:.3f}" == cell, f"{meth} {key} {f}Hz 末位 0 可由全精度复现",
                f"全精度 {full:.9f} → `{cell}`")
    c.check(True, f"末位为 0 的格子共 {len(zeros)} 个，全部回溯完毕", "")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 表头源坐标与所选样本一致（两块各 4 个）")
    c.note("表头每频率标 $(x,y)$（`\\srcxy`），须等于该频率**实际选中样本**的 "
           "source_pos；选线算法逐频独立挑样本，八个坐标互不相同，写错不会报编译错。")
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
    c.section("9. 表与图同源（Table 7 ↔ Fig. 的两块）")
    c.note("MAE 表和深度线图是同一次选线/选样本的两个产物。比对论文图件与成图"
           "脚本 out/ 下同名 PDF：内容逐字节相同（仅嵌入时间戳不同，比对前抹掉），"
           "则『表里的数』与『图里的线』必定来自同一次计算，不可能各自漂移。")
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
    c.note("caption 只声明『每列最优加粗』；两张表并排后每列分属不同几何，"
           "故最小值必须在各自块内取，不能用跨块的全局最小。")
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
    bad = [f"{meth} {b['key']} {f}Hz `{printed[meth][b['col0'] + j]}`"
           for _, meth, _ in ROWS for b in BLOCKS for j, f in enumerate(FREQS)
           if not re.fullmatch(r"\d+\.\d{3}", printed[meth][b["col0"] + j])]
    c.check(not bad, "全部 40 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))

    # ── J ────────────────────────────────────────────────────────
    c.section("12. 与 Table 8 的版式一致性")
    sib, sib_star = main_table(SIB)
    c.check(sib is not None, "Table 8 表体可定位", f"长度 {len(sib or '')}")
    c.check(sib_star, "Table 8 亦为 tabular*", f"is_star={sib_star}")
    # 两表首列列类型名不同（M=方法标签 / A=变体标签），但都是
    # >{\srcvar\raggedright\arraybackslash}l，八个数据列同为 c；
    # 故断言的"一致"是排版宽度一致，而不是列类型字面相同。
    p8, p9 = T.tabular_preamble(env), T.tabular_preamble(sib)
    c.check(p8 is not None and p9 is not None, "两表列定义可解析",
            f"Table 7 `{p8}` / Table 8 `{p9}`")
    c.check(p8 is not None and p8.endswith("EEEE EEEE@{}"),
            "Table 7 列类型序列为 `M EEEE EEEE`", f"`{p8}`")
    c.check(p9 is not None and p9.endswith("EEEE EEEE@{}"),
            "Table 8 列类型序列为 `A EEEE EEEE`", f"`{p9}`")
    for p, nm in ((p8, "Table 7"), (p9, "Table 8")):
        c.check(p is not None and "extracolsep" in p,
                f"{nm} 用 \\extracolsep{{\\fill}} 均分列间余量", f"`{p}`")
    # 断言 \TABstyleDL 而非 \TABstyle：后者是前者的子串，用 in 判断会假通过。
    # 样式宏排在 \label 与 \begin{tabular*} 之间，不在 table_body_of() 的
    # tabular 区间内，故按"label 之后的一小段"取。
    def style_span(lb):
        li = T.tex_text().find(f"\\label{{{lb}}}")
        return T.tex_text()[li:li + 200] if li >= 0 else ""
    c.check("\\TABstyleDL" in style_span(LABEL) and "\\TABstyleDL" in style_span(SIB),
            "两表同用 \\TABstyleDL（整表紧凑列距）", "")

    # 总宽须相同：两表并排，宽度不一致时边缘对不齐。tabular* 的宽度参数
    # 就是总宽，R1 两处都写作 \linewidth（浮动体已由 \CapFitWidth 统一）。
    widths = {}
    for lb in (LABEL, SIB):
        e, _ = main_table(lb)
        mm = re.search(r"\\begin\{tabular\*\}\{([^}]*)\}", e or "")
        widths[lb] = mm.group(1) if mm else None
    same = len(set(widths.values())) == 1 and None not in widths.values()
    c.check(same, "两表的 tabular* 总宽参数一致（等宽并排）",
            " / ".join(f"{k.split(':')[1]}=`{v}`" for k, v in widths.items()))

    # ── K ────────────────────────────────────────────────────────
    c.section("13. 正文引用精确性（4.4 节）")
    c.note("正文 `$1.515$\\,dB on the rectangular line and $0.666$\\,dB on the "
           "wedge line` 是**分几何**的本文法最大值，不是跨块全局最大。")
    prop_rect = max(RR["rect"]["er"][f][0] for f in FREQS)
    prop_wedge = max(RR["wedge"]["er"][f][0] for f in FREQS)
    four_r = [f"{RR['rect']['er'][f][0]:.3f}" for f in FREQS]
    four_w = [f"{RR['wedge']['er'][f][0]:.3f}" for f in FREQS]
    c.check(f"{prop_rect:.3f}" == "1.515",
            "正文『at or below 1.515 dB on the rectangular line』",
            f"矩形四频 {four_r} → 最大 `{prop_rect:.3f}`")
    c.check(f"{prop_wedge:.3f}" == "0.666",
            "正文『0.666 dB on the wedge line』",
            f"楔形四频 {four_w} → 最大 `{prop_wedge:.3f}`")
    txt = T.tex_text()
    for y in (56.1, 30.4):
        hits = T.sentences_with(re.escape(f"y={y}"), txt)
        c.check(bool(hits), f"正文声明的深度线 y={y} m 与脚本 force_y 一致",
                f"tex 行 {T.line_of(hits[0][0])}" if hits else "未找到")
    dn = max(max(RR[b["key"]]["er"][f][1] for f in FREQS) for b in BLOCKS)
    c.check(dn > 5.0, "正文『DeepONet exceeds 5 dB』成立（阈值断言，不指某格）",
            f"DeepONet 最大 `{dn:.3f}` > 5")
    c.exempt("正文 `$5$\\,dB` 不作字面比对",
             "该数是阈值表述（exceeds 5 dB），非某单元格的印刷值")

    c.section("14. 本文法逐频占优（两块分别）")
    for b in BLOCKS:
        for f in FREQS:
            col = RR[b["key"]]["er"][f]
            c.check(col[0] == min(col), f"{b['key']} {f}Hz Proposed 为最小",
                    f"Proposed `{col[0]:.3f}` vs 次优 `{min(col[1:]):.3f}`")

    return c


if __name__ == "__main__":
    import sys
    sys.exit(run().finish())
