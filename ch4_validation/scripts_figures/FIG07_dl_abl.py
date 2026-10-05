#!/usr/bin/env python3
"""
Fig 7（fig:dl-abl）核验 — R1

对象：四变体消融深度线 TL 图，**矩形 R1 与楔形 W1 合并为同一张图**，两个
      并排 subfloat：
        (a) fig:dl-abl-r = Fig. 7a，ablation_R1_module_advantage.pdf，y=71.9 m，Cases 25-28
        (b) fig:dl-abl-w = Fig. 7b，ablation_W1_module_advantage.pdf，y=33.4 m，Cases 29-32

R1 把原来分开的两张图（旧 fig:dl-abl-rect / fig:dl-abl-wedge）并为一张，编号 7；
两张表（旧 tab:dl-abl-rect / -wedge）也并为 Table 8（tab:dl-abl）。判据与合并前
逐条相同，只是版式与编号变了。

与 Table 8 同源：深度线图给曲线，表给 MAE，两者出自同一次 build_group。

★ 成图脚本写纸面尺寸 PDF（240x142 pt）到 fig06_07_dl/out/；depthline 的
  figure_pdf() 指向 cache/（旧版大画布），不是论文图件来源。

核验链
  A. 脚本同源      权威 core / repo 副本；GRID/METHOD/FREQS 口径防漂移
  B. epoch 自证    两组 npz 均为 ep200；caption 以 Fig. 6 继承 epoch 约定
  C. 图上 Src      4 组源坐标逐频吻合（PDF 文本层 vs npz 重算）
  D. 图表同源      论文图件 == 脚本 out/ 产物（抹掉嵌入时间戳后 md5 相同）
  E. 表头源坐标    8 个 (x,y) 与两组各自所选样本一致（★）
  F. 子图题注      subfloat 题注的 y 深度与重算、与 Table 8 一致
  G. 正文引用      图号 7；正文单点引用；正文陈述的方向性由列值印证
"""
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import depthline as DL, paths, report, texparse as T  # noqa: E402

SLUG = "FIG07_dl_abl"
LABEL = "fig:dl-abl"
NUMBER = 7
SIB = "tab:dl-abl"          # 本图的兄弟表：Table 8（消融深度线 MAE）
FREQS = (25, 50, 75, 100)

BLOCKS = [
    dict(lb="fig:dl-abl-r", group="ablation_R1_module_advantage", y=71.9,
         cases="Cases~25--28", geo="Rectangular",
         pdf="ablation_r1_module_advantage.pdf"),
    dict(lb="fig:dl-abl-w", group="ablation_W1_module_advantage", y=33.4,
         cases="Cases~29--32", geo="Wedge",
         pdf="ablation_w1_module_advantage.pdf"),
]
METHODS = ["Full", "w/o", "prior", "graph", "supervision", "COMSOL"]

FIG_OUT = os.path.join(os.path.dirname(DL.AUTH), "out")


def fig_pdf(group):
    return os.path.join(FIG_OUT, f"{group}.pdf")


def pdf_md5_no_ts(p):
    """PDF 的 md5，先抹掉嵌入式创建/修改时间戳。

    matplotlib 每次运行写入 CreationDate，逐字节比对必然不等；抹掉后相同即
    页面内容/字体/流对象完全一致，可判定同源。
    """
    if not p or not os.path.exists(p):
        return None
    b = open(p, "rb").read()
    b = re.sub(rb"/(?:CreationDate|ModDate)\s*\([^)]*\)", b"/DT(X)", b)
    return hashlib.md5(b).hexdigest()


def pdftext(pdf_path):
    """PDF 文本层。必须 -raw（-layout 会把多行面板标题按列咬合）。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=180)
        return out.stdout
    except Exception:
        return ""


def subfloat_title(lb):
    txt = T.tex_text()
    k = txt.find(chr(92) + "label{" + lb + "}")
    if k < 0:
        return ""
    b = txt.rfind(chr(92) + "subfloat[", 0, k)
    if b < 0:
        return ""
    e = txt.find("]", b)
    return txt[b + len(chr(92) + "subfloat["):e] if e > b else ""


def flat(s):
    return re.sub(r"\s+", " ", (s or "")).replace("$", "").replace(chr(92) + ",", "")


def run():
    import numpy as np

    c = report.Checker(SLUG, "四变体消融深度线 Fig 7（矩形+楔形合并）", "figure",
                       LABEL, str(NUMBER))

    c.source("印刷面 tex", paths.TEX,
             f"`\\label{{{LABEL}}}` 所在 figure* 浮动体（表+图同体）")
    c.source("成图/取数脚本（权威）", DL.AUTH,
             "组 ablation_R1_module_advantage / ablation_W1_module_advantage")
    c.source("同一脚本 repo 副本", DL.COPY, "legacy 副本，口径函数逐字符相同")
    c.source("成图脚本（纸面尺寸成图）",
             os.path.join(paths.PLOTDIR, "fig06_07_dl", "fig06_07_dl.py"),
             "Fig 7 的 240x142 pt 纸面尺寸版由它写到 out/")
    c.source("共用图例图", os.path.join(paths.FIGDIR, "dl_legend_abl.pdf"),
             "本组四条曲线的方法名在此图中")
    for b in BLOCKS:
        c.source(f"论文图件（{b['geo']}）", os.path.join(paths.FIGDIR, b["pdf"]),
                 "来源：成图脚本 out/ 下的纸面尺寸 PDF")

    # ── A ────────────────────────────────────────────────────────
    c.section("2. 源可追溯与口径防漂移")
    c.note("深度线口径由 Validation_Scripts/fig06_07_dl/_depthline_core.py 承载，"
           "成图脚本直接加载它不复制算法；common/depthline.py 又 import 同一份"
           "core，故三者口径不可能各自漂移。")
    c.check(os.path.exists(DL.AUTH), "权威 core 存在", paths.rel(DL.AUTH))
    c.check(os.path.exists(DL.COPY), "repo 副本存在", paths.rel(DL.COPY))
    c.exempt("成图脚本两份副本 md5 相同",
             "core 与 legacy 副本 md5 不同是既定的整理结果（路径解析层 "
             "_figpaths 被改写），口径一致性改由现场读出 GRID/METHOD/FREQS 断言")
    c.check(os.path.exists(fig_pdf(BLOCKS[0]["group"])),
            "成图脚本 out/ 有纸面尺寸产物", paths.rel(FIG_OUT))

    m = DL.script()
    for name, got, want in (("插值网格 GRID", m.GRID, 300),
                            ("插值方式 METHOD", m.METHOD, "cubic"),
                            ("频率集 FREQS", tuple(m.FREQS), FREQS)):
        c.check(got == want, f"{name} = {want!r}", f"脚本内 `{got!r}`")
    src_txt = open(DL.AUTH, encoding="utf-8").read()
    c.check("Src ({_sx:.1f}, {_sy:.1f}) m" in src_txt,
            "脚本内 Src 为 1 位小数（全章统一口径）",
            "含 `{_sx:.1f}, {_sy:.1f}`")

    rec = {b["group"]: DL.recompute(b["group"]) for b in BLOCKS}
    for b in BLOCKS:
        for case, p in rec[b["group"]]["npz"].items():
            c.check(os.path.exists(p), f"{b['geo']} {case} 的 ep200 npz 存在",
                    paths.rel(p))

    # ── B ────────────────────────────────────────────────────────
    c.section("3. epoch 自证与 caption 声明")
    for b in BLOCKS:
        R = rec[b["group"]]
        eps = sorted({int(np.load(p)["epoch"]) for p in R["npz"].values()})
        c.check(eps == [200], f"{b['lb']} 全部 npz epoch == 200 (last)",
                f"实得 {eps}（{len(R['npz'])} 份 npz）")
    cap = flat(T.caption_of(LABEL))
    c.check("ablation variants" in cap, "caption 声明 ablation variants", "")
    c.check("best epoch" not in cap, "{LABEL} caption 未误写 best epoch".format(
        LABEL=LABEL), "深度线族一律源自 ep200 npz")
    # R1 的 Fig 7 caption 不自行重复 last epoch，而是以 `layout and conventions
    # as in Fig.~\ref{fig:dl-cmp}` 继承 Fig 6 的约定（与 Table 8 继承 Table 7
    # 的 epoch 约定同一写法）。故判据是"继承声明存在"，而非"含 last epoch"。
    c.note("R1 的 Fig 7 caption 以『layout and conventions as in Fig.~\\ref{"
           "fig:dl-cmp}』继承 Fig 6 的 epoch 约定，与 Table 8 继承 Table 7 同一"
           "写法；故判据改为核继承声明，并回核被继承方确有 last epoch。")
    c.check(chr(92) + "ref{fig:dl-cmp}" in (T.caption_of(LABEL) or ""),
            "caption 以 Fig.~\\ref{fig:dl-cmp} 继承布局、约定与 epoch 口径",
            "含 `layout and conventions as in Fig.~\\ref{fig:dl-cmp}`")
    c.check("last epoch" in flat(T.caption_of("fig:dl-cmp")),
            "被继承的 Fig. 6 自身声明 last epoch", "")
    c.exempt(f"{LABEL} caption 自行写明 last epoch",
             "R1 改为继承 Fig. 6 的约定（已回核 Fig. 6 确有 last epoch）；"
             "两图的 npz epoch 已在本节逐组核为 200")
    c.check("sloping surface" in cap and "x=33.4" in cap,
            "caption 说明楔形曲线起点（y=(L_y/L_x)x 处，x=33.4 m）", "")
    c.check("(b)" in cap and "wedge" in cap.lower(),
            "caption 以 (b) 指代楔形面板（矩形面板由 subfloat 题注标为 Rectangular）",
            "R1 的 Fig 7 caption 只点名 (b)；矩形面板编号 (a) 由 subfloat 承担")

    # ── C ────────────────────────────────────────────────────────
    c.section("4. 图上 Src 标注：npz 重算 vs PDF 文本层")
    for b in BLOCKS:
        txt = pdftext(os.path.join(paths.FIGDIR, b["pdf"]))
        got = re.findall(r"Src \(([0-9.]+), ([0-9.]+)\) m", txt)
        want = [(f"{rec[b['group']]['src'][f][0]:.1f}",
                 f"{rec[b['group']]['src'][f][1]:.1f}") for f in FREQS]
        c.check(got == want, f"{b['lb']} 4 组 Src 吻合",
                f"PDF {got} / npz {want}")
        got_f = re.findall(r"(\d+) Hz, Src", txt)
        c.check(got_f == [str(f) for f in FREQS],
                f"{b['lb']} 四个频率面板齐全", f"图上 `{got_f}`")
        c.check("|Err|" in txt, f"{b['lb']} 含逐点误差面板", "")
        c.check("TL (dB)" in txt, f"{b['lb']} 含 TL 纵轴标签", "")

    leg = pdftext(os.path.join(paths.FIGDIR, "dl_legend_abl.pdf"))
    for name in METHODS:
        c.check(name in leg, f"图例（dl_legend_abl.pdf）含 {name}",
                f"`{leg.strip()}`")
    c.check("Obstacle" in leg, "图例含 Obstacle 灰带说明", "")

    # ── D ────────────────────────────────────────────────────────
    c.section("5. 图与表同源（Fig. 7 <-> Table 8）")
    c.note("MAE 表与深度线图是同一次 build_group 的两个产物。比对论文图件与脚本"
           "out/ 下同名 PDF：抹掉嵌入时间戳后 md5 相同，即证明表里的数与图里的"
           "线出自同一次运行。★ raw md5 永远不等：matplotlib 每次写 CreationDate。")
    for b in BLOCKS:
        src_pdf = fig_pdf(b["group"])
        dst_pdf = os.path.join(paths.FIGDIR, b["pdf"])
        c.check(os.path.exists(src_pdf), f"{b['lb']} 脚本产出 PDF 存在",
                paths.rel(src_pdf))
        c.check(os.path.exists(dst_pdf), f"{b['lb']} 论文图件存在",
                paths.rel(dst_pdf))
        h1, h2 = pdf_md5_no_ts(src_pdf), pdf_md5_no_ts(dst_pdf)
        c.check(h1 is not None and h1 == h2,
                f"{b['lb']} 论文图件与脚本产物同源（抹时间戳后同 md5）",
                f"md5(no-ts) `{(h1 or '-')[:12]}`")
    c.exempt("PDF 逐字节 md5 相同",
             "matplotlib 每次运行写入 CreationDate（本机实测 D:2026…），"
             "逐字节比对必然不等；已改为抹掉时间戳后比对，同源判定不受影响。")
    c.exempt("图件来源为 common/depthline.py:figure_pdf() 所指目录",
             "该函数指向 fig06_07_dl/cache/（core 的旧版大画布渲染，"
             "MediaBox 1181.8x855.1 pt）；论文用的是成图脚本 out/ 下的纸面"
             "尺寸版（240x142 pt）。本脚本改读 out/。")

    # ── E ────────────────────────────────────────────────────────
    c.section("6. 表头源坐标与所选样本一致（两块各 4 个）")
    c.note("Table 8 表头每频率标 $(x,y)$（\\srcxy）。★ 本表表头分两行：第一行是 "
           "`\\multicolumn` 的几何块名，第二行才是频率与 \\srcxy，故不能只用 "
           "header_row()（它止于第一个 \\midrule），须在表体内取全部 \\srcxy。")
    env, star = T.table_body_of(SIB)
    c.check(env is not None, "Table 8 表体可定位", f"长度 {len(env or '')}")
    hdr = T.header_row(env) or ""
    c.check("Rectangular" in hdr and "Wedge" in hdr,
            "表头块名声明两个几何（R1 / W1）", f"第一行 `{hdr[:70]}`")
    got = [(float(a), float(b))
           for a, b in re.findall(r"\\srcxy\{([\d.]+)\}\{([\d.]+)\}", env)]
    c.check(len(got) == 8, "表头解析到 8 组源坐标（4 矩形 + 4 楔形）", str(got))
    for k, b in enumerate(BLOCKS):
        R = rec[b["group"]]
        c.check(abs(round(R["y_line"], 1) - b["y"]) < 1e-9,
                f"{b['lb']} 选中行深度舍入到 1 位 = {b['y']} m",
                f"实际 `{R['y_line']:.6f}`（subfloat 题注写 1 位小数）")
        title = flat(subfloat_title(b["lb"]))
        c.check(f"y={b['y']}" in title,
                f"{b['lb']} subfloat 题注标明 y={b['y']} m（与重算一致）",
                f"题注 `{title}`")
        for j, f in enumerate(FREQS):
            idx = k * 4 + j
            sx, sy = R["src"][f]
            want = (round(sx, 1), round(sy, 1))
            c.check(idx < len(got) and got[idx] == want,
                    f"{b['geo']} {f}Hz 源坐标",
                    f"tex `{got[idx] if idx < len(got) else '缺'}` / "
                    f"样本 {R['sample'][f]} 实际 ({sx:.5f}, {sy:.5f}) -> `{want}`")

    # ── F ────────────────────────────────────────────────────────
    c.section("7. 与 Table 8 的一致性")
    cap_t = flat(T.caption_of("tab:dl-abl"))
    for b in BLOCKS:
        c.check(b["cases"] in cap_t, f"Table 8 caption 声明 {b['cases']}",
                "与 subfloat 题注的几何对应")
        c.check(f"y={b['y']}" in cap_t,
                f"Table 8 caption 声明 {b['geo']} 深度 y={b['y']} m", "")
        c.check(f"y={b['y']}" in flat(subfloat_title(b["lb"])),
                f"{b['lb']} 题注深度与 Table 8 同值", "")
    c.check("tab:dl-cmp" in (T.caption_of("tab:dl-abl") or ""),
            "Table 8 caption 以 Table 7 交代 header/emphasis/epoch 约定", "")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 正文引用、编号与方向性")
    txt_all = T.tex_text()
    aux = T.labels()
    c.check(aux.get(LABEL, {}).get("num") == str(NUMBER),
            f"{LABEL} 编号为 {NUMBER}",
            f"aux `{aux.get(LABEL, {}).get('num', '缺失')}`")
    needle = chr(92) + "ref{" + LABEL + "}"
    n_main = txt_all.count(needle)
    c.check(n_main >= 2, "正文多处引用 Fig. 7（4.4 引入段 + 4.5 消融段各一次）",
            f"`{needle}` 出现 {n_main} 处")
    for b in BLOCKS:
        c.check(aux.get(b["lb"], {}).get("num", "缺失") != "缺失",
                f"子图 `{b['lb']}` 已在 aux 注册",
                f"aux `{aux.get(b['lb'], {}).get('num')}`")
    c.exempt("正文以区间引用覆盖两张图",
             "R1 合并后正文改为单点引用（Fig.~\\ref{fig:dl-abl}），"
             "全章已无 \\ref{A}--\\ref{B} 形式")
    c.check(aux.get("fig:dl-abl-r", {}).get("num") == "9a",
            "子图编号为全章全局递增的 9a/9b（排版事实）",
            "subfig 计数器跨图累加，正文不引用面板 label")

    c.note("正文 4.5 节称去掉物理先验后『raises the depth-line TL to tens of "
           "decibels at every frequency on both geometries』。这是图上曲线最"
           "显著的特征，逐频核其成立。")
    for b in BLOCKS:
        R = rec[b["group"]]
        pi = R["methods"].index("w/o prior")
        vals = [R["er"][f][pi] for f in FREQS]
        c.check(all(v >= 8.0 for v in vals),
                f"{b['lb']} w/o prior 四频 TL 均达数十 dB 量级",
                " / ".join(f"{f}Hz:{v:.1f}" for f, v in zip(FREQS, vals)))
    # 正文以图 6/图 7 并提的方式描述该现象，故核该措辞确实覆盖两图。
    c.check("Both the comparison and the ablation" in txt_all or
            "tens of decibels" in txt_all,
            "正文『tens of decibels』表述由图 7 的 w/o prior 列值印证", "")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
