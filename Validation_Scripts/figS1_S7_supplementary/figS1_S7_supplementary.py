# -*- coding: utf-8 -*-
"""
figS1_S7_supplementary.py
=====================
Supplementary Material, Figs. S1-S7 -- the field figures moved out of the main
text in R1, redrawn at printed size with the same renderers as the main-text
figures (so their type size, colour scales, interpolation and masking match).

  S1  Case04  R2  rectangular  256 x 128 m   (orig. Fig. 6a)
  S2  Case10  W2  wedge        256 x 128 m   (orig. Fig. 6b)
  S3  Case05  R3  rectangular  512 x 128 m   (orig. Fig. 7a)
  S4  Case11  W3  wedge        512 x 128 m   (orig. Fig. 7b)
  S5  Cases 25-28  R1 ablation variants     (orig. Fig. 16)
  S6  Cases 29-32  W1 ablation variants     (orig. Fig. 17)
  S7  Cases 40-41  R10 / W9 extrapolation    (orig. Figs. 21 and 22; the other two
                                              panels, R9 / W10, are main-text Fig. 12)

Numbering follows first citation in the manuscript (Secs. 4.3, 4.5, 4.7).

Field panels (S1-S4, S7): fig04_05_10_fields.fields() -- griddata cubic 200x200,
obstacle/wedge mask, clip to [vmin, vmax]; S7 also reuses its make_panel().
The long 256/512 m domains get panels at their true aspect ratio, sized so a
page holds all eight rows (4 frequencies x 2 held-out samples, as in Fig. 4).
Ablation grids (S5-S6): fig08_09_perf_grid.render() with the four variants in
place of the five methods.

    python figS1_S7_supplementary.py      -> out/figS1.pdf ... figS7_*.pdf
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "fig04_05_10_fields"))
sys.path.insert(0, os.path.join(ROOT, "fig08_09_perf_grid"))
import _figpaths                      # noqa: E402
import fig04_05_10_fields as FF       # noqa: E402  场图渲染器（正文 Fig. 4/5/10/12）
import fig08_09_perf_grid as PG       # noqa: E402  网格渲染器（正文 Fig. 8/9）

import matplotlib.pyplot as plt                    # noqa: E402
from matplotlib.patches import Ellipse as MplEllipse  # noqa: E402

OUT = _figpaths.figdir(__file__)
W_PAGE = 491.5        # \textwidth 494.5 pt 减去少量余量，与正文整宽图一致
H_PAGE = 640.0        # 留出图题空间（textheight 约 689 pt）


def wide_panel(prefix, out_pdf):
    """长条形计算域：3 列 (Ours | COMSOL | Error) x 8 行，子图按真实宽高比。"""
    rows = FF.rows_multi(prefix)
    d0 = rows[0][0]
    Lx, Ly = float(d0["Lx_dom"]), float(d0["Ly_dom"])
    a = Ly / Lx
    n = len(rows)
    fixed = (FF.TOP_PAD + FF.HEAD + n * FF.ROW_TITLE + (n - 1) * FF.ROW_GAP
             + FF.X_BAND + FF.CB_BAND)
    w_width = (W_PAGE - FF.L_MARGIN - FF.R_MARGIN - 2 * FF.COL_GAP) / 3.0
    w_height = (H_PAGE - fixed) / (n * a)
    w = min(w_width, w_height)
    h = w * a
    W = W_PAGE
    W_need = FF.L_MARGIN + 3 * w + 2 * FF.COL_GAP + FF.R_MARGIN
    x0 = FF.L_MARGIN + (W - W_need) / 2.0
    H = fixed + n * h
    fig = plt.figure(figsize=(W / 72.0, H / 72.0))

    def box(x, y_top, bw, bh):
        return [x / W, 1 - (y_top + bh) / H, bw / W, bh / H]

    cols_x = [x0 + j * (w + FF.COL_GAP) for j in range(3)]
    # 子图矮于纵轴名长度时，每行都写纵轴名会串到相邻行：改为全图只写一次
    thin = h < 55.0
    y = FF.TOP_PAD
    for j, name in enumerate(["Ours TL", "COMSOL TL", "Error"]):
        fig.text((cols_x[j] + w / 2) / W, 1 - (y + FF.HEAD * 0.55) / H, name,
                 ha="center", va="center", fontsize=FF.FS_HEAD, fontweight="bold")
    y += FF.HEAD
    ims = None
    for r, (data, idx, left) in enumerate(rows):
        gp, gf, err, avg, _ = FF.fields(data, idx)
        vmin, vmax = float(data["vmin"]), float(data["vmax"])
        src = data["source_pos"][idx]
        is_wedge = bool(data["is_wedge"])
        ell = data["ellipse"]
        ty = 1 - (y + FF.ROW_TITLE - 2.0) / H
        fig.text(cols_x[0] / W, ty, left, ha="left", va="baseline", fontsize=FF.FS_ROW)
        fig.text((cols_x[2] + w) / W, ty, "Avg %.2f dB" % avg, ha="right",
                 va="baseline", fontsize=FF.FS_ROW)
        y += FF.ROW_TITLE
        last = r == n - 1
        cur = []
        for j, (arr, cmap, lo, hi) in enumerate([(gp, "jet", vmin, vmax),
                                                 (gf, "jet", vmin, vmax),
                                                 (err, "Reds", 0, 10.0)]):
            ax = fig.add_axes(box(cols_x[j], y, w, h))
            im = ax.imshow(arr, extent=(0, Lx, Ly, 0), origin="upper", cmap=cmap,
                           aspect="auto", vmin=lo, vmax=hi, interpolation="nearest")
            cur.append(im)
            if is_wedge:
                ax.plot([0, Lx], [0, Ly], "k-", linewidth=FF.LW)
                ax.plot([Lx, Lx], [0, Ly], color="gray", linewidth=0.5, linestyle="--")
            if ell.size == 4:
                cx, cy, ea, eb = [float(v) for v in ell]
                ax.add_patch(MplEllipse((cx, cy), width=2 * ea, height=2 * eb,
                                        fill=False, edgecolor="k", linewidth=FF.LW))
            ax.plot(src[0], src[1], "r*", markersize=FF.STAR_MS,
                    markeredgewidth=0.3, markeredgecolor="darkred")
            ax.set_xlim(0, Lx)
            ax.set_ylim(Ly, 0)
            ax.set_xticks(FF.ticks_for(Lx))
            ax.set_yticks([0, 64, 128] if not thin else [0, 128])
            ax.tick_params(labelsize=FF.FS_TICK, labelbottom=last, labelleft=(j == 0))
            if last:
                ax.set_xlabel("X / Range (m)", fontsize=FF.FS_LABEL, labelpad=1.5)
            if j == 0 and not thin:
                ax.set_ylabel("Y / Depth (m)", fontsize=FF.FS_LABEL, labelpad=1.5)
        ims = cur
        y += h + (0 if last else FF.ROW_GAP)
    if thin:
        y_top = FF.TOP_PAD + FF.HEAD
        fig.text(4.0 / W, 1 - (y_top + y) / 2 / H, "Y / Depth (m)", rotation=90,
                 ha="left", va="center", fontsize=FF.FS_LABEL)
    y += FF.X_BAND
    for (xa, xb, im, lbl, tk) in [(cols_x[0], cols_x[1] + w, ims[0], "TL (dB)", [-60, -40, -20, 0]),
                                  (cols_x[2], cols_x[2] + w, ims[2], "Error (dB)", [0, 5, 10])]:
        cax = fig.add_axes(box(xa, y + 2.0, xb - xa, 3.5))
        cb = fig.colorbar(im, cax=cax, orientation="horizontal", ticks=tk)
        cb.outline.set_linewidth(0.5)
        cb.ax.tick_params(labelsize=FF.FS_TICK, length=1.5, pad=1.0, width=0.5)
        cb.set_label(lbl, fontsize=FF.FS_LABEL, labelpad=1.0)
    fig.savefig(out_pdf, dpi=300)
    plt.close(fig)
    return W, H, w, h


def ablation_grid(cases, out_pdf):
    """正文 Fig. 8/9 的网格渲染器，方法换成四个消融变体。"""
    saved = PG.METHODS
    PG.METHODS = ["Full model", "w/o physics prior", "w/o graph correction",
                  "w/o prior supervision"]
    try:
        W, H, w = PG.render(dict(cases=cases, rows=PG.ROWS_2S, cbar=True), out_pdf)
    finally:
        PG.METHODS = saved
    return W, H, w


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [("figS1_case04_r2", "Case04"), ("figS2_case10_w2", "Case10"),
            ("figS3_case05_r3", "Case05"), ("figS4_case11_w3", "Case11")]
    for name, prefix in jobs:
        W, H, w, h = wide_panel(prefix, os.path.join(OUT, name + ".pdf"))
        print(f"[S] {name:22s} {W:.1f} x {H:.1f} pt, panel {w:.1f} x {h:.1f} pt")
    for name, cases in [("figS5_abl_r1", ["Case25_R1_Full", "Case26_R1_no_prior",
                                          "Case27_R1_no_graph", "Case28_R1_no_prior_loss"]),
                        ("figS6_abl_w1", ["Case29_W1_Full", "Case30_W1_no_prior",
                                          "Case31_W1_no_graph", "Case32_W1_no_prior_loss"])]:
        W, H, w = ablation_grid(cases, os.path.join(OUT, name + ".pdf"))
        print(f"[S] {name:22s} {W:.1f} x {H:.1f} pt, panel {w:.1f} pt")
    # S7：与正文 Fig. 12（R9/W10）同一版式，两幅并排——余下的 R10/W9
    for name, prefix in [("figS7a_gen_extrap_r10", "Case40"), ("figS7b_gen_extrap_w9", "Case41")]:
        W, H = FF.make_panel(FF.rows_multi(prefix, tags=True), FF.W_TALL,
                             os.path.join(OUT, name + ".pdf"))
        print(f"[S] {name:22s} {W:.1f} x {H:.1f} pt")
    print("-> " + OUT)


if __name__ == "__main__":
    main()
