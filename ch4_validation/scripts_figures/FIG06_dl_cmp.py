#!/usr/bin/env python3
"""
Fig 6（fig:dl-cmp）核验 — R1

对象：五方法深度线 TL 对比图，**矩形 R1 与楔形 W1 合并为同一张图**，两个
      并排 subfloat：
        (a) fig:dl-cmp-r = Fig. 6a，comparison_R1_model_advantage.pdf，y=56.1 m，Cases 15-19
        (b) fig:dl-cmp-w = Fig. 6b，comparison_W1_model_advantage.pdf，y=30.4 m，Cases 20-24

R1 把原来分开的两张图（旧 fig:dl-cmp-rect / fig:dl-cmp-wedge = Fig 10/11）并为
一张，编号 6；两张表（旧 tab:dl-cmp-rect / -wedge）也并为 Table 8（tab:dl-cmp）。
故本脚本覆盖两个几何，每块的判据与合并前逐条相同，只是版式与编号变了。

与场图的差别：本组与 Table 8 是同一次 build_group 的两个产物（表给 MAE 数值、
图给曲线），故除数值复现外，还能用 md5 证明图与表同源。

★ 成图脚本 fig06_07_dl.py 写的是**纸面尺寸** PDF（240x142 pt = 0.49\\linewidth），
  在 fig06_07_dl/out/；common/depthline.py:figure_pdf() 指向的 cache/ 是
  core 自己的旧版大画布渲染（1181.8x855.1 pt），**不是**论文图件来源。

核验链
  A. 脚本同源      权威 core 与 repo 副本；GRID/METHOD/FREQS 口径防漂移
  B. epoch 自证    两组 npz 均为 ep200；caption 声明 last epoch 且不误写 best
  C. 图上 Src      4 组源坐标逐频吻合（PDF 文本层 vs npz 重算）
  D. 图表同源      论文图件 == 脚本 out/ 产物（抹掉嵌入时间戳后 md5 相同）
  E. 表头源坐标    8 个 (x,y) 与两组各自所选样本一致（★）
  F. 子图题注      subfloat 题注标明的 y 深度与重算、与 Table 8 一致
  G. 正文引用      图号 6；正文单点引用（R1 已取消区间引用）
"""
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import depthline as DL, paths, report, texparse as T  # noqa: E402

SLUG = "FIG06_dl_cmp"
LABEL = "fig:dl-cmp"
NUMBER = 6
SIB = "tab:dl-cmp"
FREQS = (25, 50, 75, 100)

# (子图 label, 组名, 深度 y, 案例区间, 几何词, 论文 PDF)
BLOCKS = [
    dict(lb="fig:dl-cmp-r", group="comparison_R1_model_advantage", y=56.1,
         cases="Cases~15--19", geo="Rectangular",
         pdf="comparison_r1_model_advantage.pdf"),
    dict(lb="fig:dl-cmp-w", group="comparison_W1_model_advantage", y=30.4,
         cases="Cases~20--24", geo="Wedge",
         pdf="comparison_w1_model_advantage.pdf"),
]
METHODS = ["Proposed", "DeepONet", "FNO", "KNO", "CNO"]

# 见上方注释：论文图件的来源是成图脚本的 out/，不是 depthline.FIG_DIR 的 cache/。
FIG_OUT = os.path.join(os.path.dirname(DL.AUTH), "out")


def fig_pdf(group):
    """成图脚本 out/ 下的纸面尺寸 PDF（论文 Fig. 6 的来源）。"""
    return os.path.join(FIG_OUT, f"{group}.pdf")


def pdf_md5_no_ts(p):
    """PDF 的 md5，先抹掉嵌入式创建/修改时间戳。

    matplotlib 每次运行都写入 CreationDate（本机实测 D:2026…），逐字节比对
    必然不等 —— 原始 md5 永远不可能等于论文里的副本。抹掉时间戳后若仍相同，
    则页面内容、字体、流对象完全一致，可判定同源。
    """
    if not p or not os.path.exists(p):
        return None
    b = open(p, "rb").read()
    b = re.sub(rb"/(?:CreationDate|ModDate)\s*\([^)]*\)", b"/DT(X)", b)
    return hashlib.md5(b).hexdigest()


def pdftext(pdf_path):
    """PDF 文本层。必须 -raw：-layout 会把多行面板标题按列咬合。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=180)
        return out.stdout
    except Exception:
        return ""


def subfloat_title(lb):
    """subfloat[题注]{...} 里 \\label{lb} 所属的那条题注原文。"""
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

    c = report.Checker(SLUG, "五方法深度线对比 Fig 6（矩形+楔形合并）", "figure",
                       LABEL, str(NUMBER))

    c.source("印刷面 tex", paths.TEX,
             f"`\\label{{{LABEL}}}` 所在 figure* 浮动体（表+图同体）")
    c.source("成图/取数脚本（权威）", DL.AUTH,
             "组 comparison_R1_model_advantage / comparison_W1_model_advantage")
    c.source("同一脚本 repo 副本", DL.COPY, "legacy 副本，口径函数逐字符相同")
    c.source("成图脚本（纸面尺寸成图）",
             os.path.join(paths.PLOTDIR, "fig06_07_dl", "fig06_07_dl.py"),
             "Fig 6 的 240x142 pt 纸面尺寸版由它写到 out/")
    for b in BLOCKS:
        c.source(f"论文图件（{b['geo']}）", os.path.join(paths.FIGDIR, b["pdf"]),
                 "来源：成图脚本 out/ 下的纸面尺寸 PDF")

    # ── A ────────────────────────────────────────────────────────
    c.section("2. 源可追溯与口径防漂移")
    c.note("深度线的口径由 Validation_Scripts/fig06_07_dl/_depthline_core.py "
           "承载，成图脚本 fig06_07_dl.py 直接加载它、不复制算法；"
           "common/depthline.py 又直接 import 同一份 core，故三者口径不可能"
           "各自漂移。")
    c.check(os.path.exists(DL.AUTH), "权威 core 存在", paths.rel(DL.AUTH))
    c.check(os.path.exists(DL.COPY), "repo 副本存在", paths.rel(DL.COPY))
    c.note("权威 core 与 legacy 副本 md5 不同，属预期：_depthline_core.py 是原 "
           "advantage_depth_line.py 整理进仓库时改过路径解析层（_figpaths）的"
           "版本，口径函数本身未改；两者的 GRID/METHOD/FREQS 由下一段从模块"
           "对象现场读出断言，不靠 md5 证明同源。")
    c.exempt("成图脚本两份副本 md5 相同",
             "core 与 legacy 副本的 md5 不同是既定的整理结果（路径层被改写），"
             "口径一致性改由现场读出 GRID/METHOD/FREQS 断言")
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
    c.check("Profiles are from the last epoch" in cap,
            f"{LABEL} caption 声明 last epoch",
            "含 `Profiles are from the last epoch.`")
    c.check("best epoch" not in cap, f"{LABEL} caption 未误写 best epoch",
            "深度线族一律源自 ep200 npz，非 best epoch 汇总")
    c.check("five methods" in cap, "caption 声明 five methods", "")
    c.check("25--100Hz" in cap, "caption 声明频率范围 25--100 Hz",
            "含 `$25$--$100$\\,Hz`")
    c.check("obstacle" in cap and "beyond the plotted range" in cap,
            "caption 说明灰色障碍带与轴端虚线的含义", "")
    # R1 合并后深度值不写在合并图的大 caption 里，而落在两个 subfloat 题注上；
    # 故此处改核 subfloat（第 6 节逐块核其与重算一致）。
    c.note("R1 合并后，y=56.1 / y=30.4 由两个 subfloat 题注分别标明，不在大 "
           "caption 内；判据随之从 caption_of(图) 移到 subfloat 题注。")
    c.exempt("大 caption 内含 `y=56.1` / `y=30.4`",
             "R1 改为由 subfloat 题注 `Rectangular (R1), $y=56.1$\\,m` 标明，"
             "该值已在第 6 节逐块与重算深度比对")

    # ── C ────────────────────────────────────────────────────────
    c.section("4. 图上 Src 标注：npz 重算 vs PDF 文本层")
    c.note("每个频率面板标题带该频率实际选中样本的 source_pos，逐频独立选样，"
           "四组坐标互不相同，写错不报编译错。")
    for b in BLOCKS:
        txt = pdftext(os.path.join(paths.FIGDIR, b["pdf"]))
        got = re.findall(r"Src \(([0-9.]+), ([0-9.]+)\) m", txt)
        want = [(f"{rec[b['group']]['src'][f][0]:.1f}",
                 f"{rec[b['group']]['src'][f][1]:.1f}") for f in FREQS]
        c.check(got == want, f"{b['lb']} 4 组 Src 吻合",
                f"PDF {got} / npz {want}")
        got_f = re.findall(r"(\d+) Hz, Src", txt)
        c.check(got_f == [str(f) for f in FREQS],
                f"{b['lb']} 四个频率面板齐全（标题形如 `25 Hz, Src (x, y) m`）",
                f"图上 `{got_f}`")
        c.check("|Err|" in txt, f"{b['lb']} 含逐点误差面板", "")
        c.check("TL (dB)" in txt, f"{b['lb']} 含 TL 纵轴标签", "")

    # 方法名不在面板内，而在图下方的共用图例图 dl_legend_cmp.pdf（本组的第五条
    # 子图；R1 为省版面把图例单独成图）。图例与曲线同出一次 build_group。
    leg = pdftext(os.path.join(paths.FIGDIR, "dl_legend_cmp.pdf"))
    for name in METHODS:
        c.check(name in leg, f"图例（dl_legend_cmp.pdf）含 {name}", f"`{leg.strip()}`")
    c.check("COMSOL" in leg, "图例含 COMSOL 参考解", "")
    c.source("共用图例图", os.path.join(paths.FIGDIR, "dl_legend_cmp.pdf"),
             "本组五条曲线的方法名在此图中")

    # ── D ────────────────────────────────────────────────────────
    c.section("5. 图与表同源（Fig. 6 <-> Table 8）")
    c.note("MAE 表与深度线图是同一次 build_group 的两个产物。比对论文图件与成图"
           "脚本 out/ 下同名 PDF：抹掉嵌入时间戳后 md5 相同，即证明表里的数"
           "与图里的线出自同一次运行，不可能各自漂移。"
           "★ 不能比 raw md5：matplotlib 每次都写 CreationDate。")
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
             "该函数指向 fig06_07_dl/cache/，那里是 core 的旧版大画布渲染"
             "（MediaBox 1181.8x855.1 pt）；论文用的是成图脚本 out/ 下的纸面"
             "尺寸版（240x142 pt）。本脚本改读 out/。")

    # ── E ────────────────────────────────────────────────────────
    c.section("6. 表头源坐标与所选样本一致（两块各 4 个）")
    c.note("Table 8 表头每频率标 $(x,y)$（\\srcxy），须等于该频率**实际选中"
           "样本**的 source_pos；八个坐标互不相同，写错不会报编译错。"
           "★ 图的 subfloat 题注深度也在此一并核：题注写 1 位小数，重算给全精度。")
    env, star = T.table_body_of(SIB)
    c.check(env is not None, "Table 8 表体可定位", f"长度 {len(env or '')}")
    hdr = T.header_row(env) or ""
    got = [(float(a), float(b))
           for a, b in re.findall(r"\\srcxy\{([\d.]+)\}\{([\d.]+)\}", hdr)]
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
    c.section("7. 与 Table 8 的一致性（数与数同源）")
    c.note("图的 subfloat 题注声明的深度、案例区间必须与表 caption 同值；"
           "两者排在同一浮动体内并列同页，读者左右对读。")
    cap_t = flat(T.caption_of(SIB))
    for b in BLOCKS:
        c.check(b["cases"] in cap_t, f"Table 8 caption 声明 {b['cases']}",
                "与 subfloat 题注的几何对应")
        c.check(f"y={b['y']}" in cap_t,
                f"Table 8 caption 声明 {b['geo']} 深度 y={b['y']} m", "")
        c.check(f"y={b['y']}" in flat(subfloat_title(b["lb"])),
                f"{b['lb']} 题注深度与 Table 8 同值", "")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 正文引用与编号")
    txt_all = T.tex_text()
    aux = T.labels()
    c.check(aux.get(LABEL, {}).get("num") == str(NUMBER),
            f"{LABEL} 编号为 {NUMBER}",
            f"aux `{aux.get(LABEL, {}).get('num', '缺失')}`")
    needle = chr(92) + "ref{" + LABEL + "}"
    n_main = txt_all.count(needle)
    c.check(n_main >= 2, "正文多处引用 Fig. 6（4.4 引入段 + 4.5 消融段各一次）",
            f"`{needle}` 出现 {n_main} 处")
    for b in BLOCKS:
        n_sub = aux.get(b["lb"], {}).get("num", "缺失")
        c.check(n_sub != "缺失", f"子图 `{b['lb']}` 已在 aux 注册",
                f"aux `{n_sub}`")
    # R1 已取消区间引用（\ref{A}--\ref{B}），正文改为逐图单点引用。
    rng = re.findall(re.escape(chr(92) + "ref{fig:") + r"[^}]*\}--", txt_all)
    c.exempt("正文以区间引用覆盖两张图",
             "R1 合并后正文改为单点引用（Fig.~\\ref{fig:dl-cmp}），"
             f"全章已无 \\ref{{A}}--\\ref{{B}} 形式（实测 {len(rng)} 处）")
    # 子图计数器是全章全局递增的（Fig 3=3a/b, 4=4a/b, 5=8a-f, 6=9a/b, 7=10a/b），
    # 故 Fig 6 的面板在 aux 里是 9a/9b 而非 6a/6b。这是排版事实，正文从不引用
    # 这两个面板 label，读者看不到编号错位。
    c.check(aux.get("fig:dl-cmp-r", {}).get("num") == "9a",
            "子图编号为全章全局递增的 9a/9b（排版事实）",
            "aux 9a/9b：subfig 计数器跨图累加，正文不引用面板 label")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
