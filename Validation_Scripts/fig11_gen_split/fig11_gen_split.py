# -*- coding: utf-8 -*-
"""
fig11_gen_split.py
==================
生成论文 Fig. 11 (fig:gen-split, Cases 39-42) —— 训练/测试源位置分布。

每列一个配置 (a) R9 / (b) R10 / (c) W9 / (d) W10，每块 2x2 子图对应四个频率
(25/50 上行、75/100 下行)，各自是独立抽取的源分布。频率值印在子图外的
标注带上，不覆盖点云；块内共享坐标轴，只在最外缘标刻度。

数据与 train/test 标签取自 _gen_split_core.py（manifest 坐标 + 权威
train_test_split.pth）：区外样本 100% 进训练，区内按 1:9 划分。

输出：out/generalization_split.pdf
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, Patch, Polygon, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import _figpaths  # noqa: E402

OUT = _figpaths.figdir(__file__)
sys.path.insert(0, HERE)
import _gen_split_core as src  # noqa: E402

FS_HDR = 5.5
FS_LABEL = 6.0
FS_TICK = 6.0
FS_NOTE = 6.0

W_FIG = 491.5
L_MARGIN = 24.0
R_MARGIN = 9.0    # room for the last panel's "128" x tick label
GAP_X = 5.0        # between the 8 outer columns
GAP_Y = 6.0        # between the 2 outer rows
BLOCK_PAD = 6.0    # between the two sub-columns of a case block
X_BAND = 18.0
LEG_BAND = 13.0
HDR = 9.0
TOP_PAD = 1.0
FREQ_BAND = 8.0    # band above each sub-row holding the frequency label

TRAIN_C = "#0072B2"
TEST_C = "#D55E00"
REGION_C = "#FBE3D3"
SOLID_C = "0.82"
EDGE_C = "0.15"

QUAD = {25: (0, 0), 50: (0, 1), 75: (1, 0), 100: (1, 1)}

plt.rcParams.update({
    "pdf.fonttype": 42,
    "font.size": FS_TICK,
    "axes.linewidth": 0.4,
    "xtick.major.width": 0.4, "ytick.major.width": 0.4,
    "xtick.major.size": 1.5, "ytick.major.size": 1.5,
    "xtick.major.pad": 1.0, "ytick.major.pad": 1.0,
})


def draw_panel(ax, d, fi, is_wedge, Lx, Ly, tmx, tmy, deep):
    if deep:
        ax.add_patch(Rectangle((0, tmy), Lx, Ly - tmy, facecolor=REGION_C,
                               edgecolor="none", zorder=0))
        xa = tmy * Lx / Ly if is_wedge else 0.0
        ax.plot([xa, Lx], [tmy, tmy], color=EDGE_C, lw=0.5,
                ls=(0, (2.5, 1.2)), zorder=5)
    else:
        ax.add_patch(Rectangle((tmx, 0), Lx - tmx, Ly, facecolor=REGION_C,
                               edgecolor="none", zorder=0))
        yb = tmx * Ly / Lx if is_wedge else Ly
        ax.plot([tmx, tmx], [0, yb], color=EDGE_C, lw=0.5,
                ls=(0, (2.5, 1.2)), zorder=5)

    s = d["fidx"] == fi
    x, y, tr = d["x"][s], d["y"][s], d["is_train"][s]
    ax.scatter(x[tr], y[tr], s=0.5, c=TRAIN_C, marker="o", linewidths=0,
               zorder=2)
    ax.scatter(x[~tr], y[~tr], s=1.1, c=TEST_C, marker="o", linewidths=0,
               zorder=3)

    if is_wedge:
        ax.add_patch(Polygon([[0, 0], [0, Ly], [Lx, Ly]], closed=True,
                             facecolor=SOLID_C, edgecolor="none", zorder=4))
        ax.plot([0, Lx], [0, Ly], color="k", lw=0.5, zorder=6)
    cx, cy, a, b = d["ell"]
    ax.add_patch(Ellipse((cx, cy), 2 * a, 2 * b, facecolor=SOLID_C,
                         edgecolor="k", lw=0.4, zorder=6))
    ax.set_xlim(0, Lx); ax.set_ylim(Ly, 0)
    ax.set_aspect("equal")
    # 0/64/128 on both axes; the visibility pass below keeps only the labels
    # that belong to this panel's position in the outer grid
    ax.set_xticks([0, 64, 128]); ax.set_yticks([0, 64, 128])


def render(out_pdf):
    ncase = len(src.CASES)
    ncol = 2 * ncase                      # 8 outer columns
    S = (W_FIG - L_MARGIN - R_MARGIN - (ncol - 1) * GAP_X) / ncol
    W = W_FIG
    H = (TOP_PAD + HDR + FREQ_BAND + S
         + GAP_Y + FREQ_BAND + S + X_BAND + LEG_BAND)
    fig = plt.figure(figsize=(W / 72.0, H / 72.0))

    def box(x, y_top, bw, bh):
        return [x / W, 1 - (y_top + bh) / H, bw / W, bh / H]

    texts, axes = [], []
    y_top0 = TOP_PAD + HDR + FREQ_BAND   # first panel starts below its label band
    for ci, (name, no, subdir, raw_case, is_wedge) in enumerate(src.CASES):
        d = src.load_case(subdir, raw_case)
        Lx, Ly = d["Lx"], d["Ly"]
        tmx, tmy = d["train_max_x"], d["train_max_y"]
        deep = tmy < Ly - 1e-6
        x0 = L_MARGIN + 2 * ci * (S + GAP_X)
        thr = ("$y>%.0f$" % tmy) if deep else ("$x>%.0f$" % tmx)
        geom = "rect." if name.startswith("R") else "wedge"
        texts.append(fig.text(x0 / W, 1 - (TOP_PAD + HDR - 2.0) / H,
                              "(%s) %s, %s, %s" % ("abcd"[ci], name, geom, thr),
                              ha="left", va="baseline", fontsize=FS_HDR,
                              fontweight="bold"))
        for f in src.FREQS:
            r, c = QUAD[f]
            y_row = y_top0 + r * (FREQ_BAND + S + GAP_Y)
            ax = fig.add_axes(box(x0 + c * (S + BLOCK_PAD), y_row, S, S))
            draw_panel(ax, d, src.FREQS.index(f), is_wedge, Lx, Ly, tmx, tmy,
                       deep)
            axes.append(ax)
            # x labels on the bottom sub-row of each block; y labels only on the
            # leftmost sub-column.  The 0 tick is dropped wherever it would sit
            # beside a neighbour's 128 and the two would touch: that happens at
            # the right edge of every block's left sub-column, and at the very
            # right of the figure.
            # x labels on the bottom sub-row only.  At a block join the
            # neighbour's labels are closer than one label width, so each
            # block's right sub-column keeps just the middle tick.
            for t in ax.get_xticklabels():
                vis = (r == 1)
                txt = t.get_text()
                if c == 1 and txt == "0":
                    vis = False
                # the "128" is dropped at an interior block join, where the next
                # block's frame is only a few points away; the outermost block
                # keeps it
                if c == 1 and txt == "128" and ci < ncase - 1:
                    vis = False
                if c == 0 and ci == 0 and txt == "0":
                    vis = False
                t.set_visible(vis)
            for t in ax.get_yticklabels():
                t.set_visible(c == 0 and ci == 0 and r == 1)
            if r == 1 and c == 0 and ci == 0:
                ax.set_xlabel("Range (m)", fontsize=FS_LABEL, labelpad=2.0)
                ax.set_ylabel("Depth y (m)", fontsize=FS_LABEL, labelpad=0.8)
            # frequency label, in its own band above the panel
            texts.append(fig.text((x0 + c * (S + BLOCK_PAD)) / W,
                                  1 - (y_row - 1.5) / H, "%d Hz" % f,
                                  ha="left", va="baseline", fontsize=FS_NOTE))

    hand = [Line2D([0], [0], marker="o", ls="none", color=TRAIN_C, ms=2.6,
                   mew=0, label="Train (1820)"),
            Line2D([0], [0], marker="o", ls="none", color=TEST_C, ms=2.6,
                   mew=0, label="Test (180)"),
            Patch(facecolor=REGION_C, edgecolor=EDGE_C, lw=0.5,
                  ls=(0, (2.5, 1.2)),
                  label="Extrapolation region (200 sources, 20 in training)"),
            Patch(facecolor=SOLID_C, edgecolor="k", lw=0.5,
                  label="Obstacle / wedge bottom")]
    yl = 1 - (H - LEG_BAND * 0.5) / H
    fig.legend(handles=hand, loc="center", ncol=len(hand), fontsize=FS_LABEL,
               frameon=False, handlelength=1.4, handletextpad=0.4,
               columnspacing=1.3,
               bbox_to_anchor=(0.5 + (L_MARGIN - R_MARGIN) / 2 / W, yl))
    fig.savefig(out_pdf)
    plt.close(fig)
    return W, H, S


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    W, H, S = render(os.path.join(OUT, "generalization_split.pdf"))
    print("[2x8] %.1f x %.1f pt, panel %.1f pt" % (W, H, S))
    import fitz
    d = fitz.open(os.path.join(OUT, "generalization_split.pdf"))
    d[0].get_pixmap(dpi=200).save(os.path.join(OUT, "preview.png"))
