# -*- coding: utf-8 -*-
"""
fig08_09_perf_grid.py
=====================
生成论文 Fig. 8 (fig:perf-cmp-r, R1) 与 Fig. 9 (fig:perf-cmp-w, W1) —— 五方法 TL 场对比。

R1 审稿意见 3.4：原图每几何 8 行(4 频 x 2 样本) x 11 列，缩放到 0.41\textheight 后
字号约 2-3 pt。现拆为两张独立图，每频率一行：COMSOL | (Pred, |Err|) x 5，
|Err| 上方标区域平均误差。画布宽 = \textwidth (pt)，1:1 放置 → 字号即印刷字号。
色条共享（TL [-60,0] dB、误差 [0,10] dB）。插值/遮罩/clip 与
_figpaths 的 npz 口径一致（griddata cubic 200x200）。

输出：out/perf_grid_r1.pdf, out/perf_grid_w1.pdf
"""
import os
import sys
import glob

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse as MplEllipse
from scipy.interpolate import griddata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import _figpaths  # noqa: E402

OUT = _figpaths.figdir(__file__)

# ---- 印刷字号 (pt)，与图 4/5/6/7/9/11 一致 ----
FS_HEAD = 7.0
FS_ROW = 6.5
FS_SUB = 6.0
FS_LABEL = 6.5
FS_TICK = 6.0
FS_AVG = 6.0
STAR_MS = 4.5
LW = 0.6

# ---- 版式 (pt) ----  画布宽 = \textwidth，tex 中 scale=1 放置
W_FIG = 491.5     # \textwidth 494.5 减去 subfloat 内边距(494.5 时 overfull 1.84 pt)
L_MARGIN = 25.0
R_MARGIN = 2.0
PAIR_GAP = 1.5     # 同一方法 Pred 与 |Err| 之间
GRP_GAP = 5.0      # 方法组之间(含 COMSOL 与第一组)
HEAD = 8.5         # 方法名带
SUBHEAD = 7.0      # Pred / |Err| 小标题带
ROW_TITLE = 8.0    # 每行: 频率/声源(左) + 各误差格平均误差
X_BAND = 17.0
CB_BAND = 25.0
TOP_PAD = 1.0
ERR_HI = 10.0

plt.rcParams.update({
    "pdf.fonttype": 42,
    "font.size": FS_TICK,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2.0, "ytick.major.size": 2.0,
    "xtick.major.pad": 1.5, "ytick.major.pad": 1.5,
})

METHODS = ["Proposed", "DeepONet", "FNO", "KNO", "CNO"]
# R1 / W1 拆成两张独立整页图后恢复每频率 2 个样本(npz 中索引 2k, 2k+1)，
# 其中包含图 6 / 表 8 (fig:dl-cmp, tab:dl-cmp) 表头所用声源
ROWS_2S = [(25, 0), (25, 1), (50, 2), (50, 3),
           (75, 4), (75, 5), (100, 6), (100, 7)]
GROUPS = {
    "perf_grid_r1": dict(cases=["Case15_R1_Proposed", "Case16_R1_DeepONet",
                                "Case17_R1_FNO", "Case18_R1_KNO",
                                "Case19_R1_CNO"],
                         rows=ROWS_2S, cbar=True),
    "perf_grid_w1": dict(cases=["Case20_W1_Proposed", "Case21_W1_DeepONet",
                                "Case22_W1_FNO", "Case23_W1_KNO",
                                "Case24_W1_CNO"],
                         rows=ROWS_2S, cbar=True),
}


def find_npz(sub):
    return _figpaths.npz(sub)


def interp(data, key, i, grid_res=200, method="cubic"):
    """与 regen_method_grid.grid_of / fem_grid 一致的插值 + 遮罩 + clip。"""
    xc, yc = data["x_coords"], data["y_coords"]
    Lx, Ly = float(data["Lx_dom"]), float(data["Ly_dom"])
    vmin, vmax = float(data["vmin"]), float(data["vmax"])
    GX, GY = np.meshgrid(np.linspace(0, Lx, grid_res),
                         np.linspace(0, Ly, grid_res))
    g = griddata((xc, yc), data[key][i], (GX, GY), method=method)
    if bool(data["is_wedge"]):
        g[GY > (Ly / Lx) * GX] = np.nan
    ell = data["ellipse"]
    if ell.size == 4:
        cx, cy, a, b = [float(v) for v in ell]
        g[((GX - cx) / a) ** 2 + ((GY - cy) / b) ** 2 <= 1.0] = np.nan
    return np.clip(g, vmin, vmax)


def render(cfg, out_pdf):
    datas = [np.load(find_npz(c), allow_pickle=True) for c in cfg["cases"]]
    d0 = datas[0]
    # 同组各方法共享同一 COMSOL / 声源 / 频率
    for d in datas[1:]:
        assert np.allclose(d["fem_tl"], d0["fem_tl"])
        assert np.allclose(d["source_pos"], d0["source_pos"])
    Lx, Ly = float(d0["Lx_dom"]), float(d0["Ly_dom"])
    vmin, vmax = float(d0["vmin"]), float(d0["vmax"])
    is_wedge = bool(d0["is_wedge"])
    ell = d0["ellipse"]
    freqs = [int(round(f)) for f in d0["freq"]]

    nm = len(METHODS)
    W = W_FIG
    # 列宽由 \textwidth 反推: COMSOL + nm x (Pred, |Err|)
    w = (W - L_MARGIN - R_MARGIN - nm * PAIR_GAP - nm * GRP_GAP) / (1 + 2 * nm)
    nrow = len(cfg["rows"])
    H = (TOP_PAD + HEAD + SUBHEAD + nrow * (ROW_TITLE + w) + X_BAND
         + (CB_BAND if cfg["cbar"] else 0))
    fig = plt.figure(figsize=(W / 72.0, H / 72.0))

    def box(x, y_top, bw, bh):                  # pt(左上原点) -> figure 分数
        return [x / W, 1 - (y_top + bh) / H, bw / W, bh / H]

    x_ref = L_MARGIN
    x_pred = [L_MARGIN + w + GRP_GAP + m * (2 * w + PAIR_GAP + GRP_GAP)
              for m in range(nm)]
    x_err = [x + w + PAIR_GAP for x in x_pred]

    y = TOP_PAD
    yc = 1 - (y + HEAD * 0.55) / H
    fig.text((x_ref + w / 2) / W, yc, "COMSOL", ha="center", va="center",
             fontsize=FS_HEAD, fontweight="bold")
    for m, name in enumerate(METHODS):
        fig.text((x_pred[m] + w + PAIR_GAP / 2) / W, yc, name, ha="center",
                 va="center", fontsize=FS_HEAD, fontweight="bold")
    y += HEAD
    yc = 1 - (y + SUBHEAD * 0.5) / H
    fig.text((x_ref + w / 2) / W, yc, "Reference", ha="center", va="center",
             fontsize=FS_SUB, style="italic")
    for m in range(nm):
        fig.text((x_pred[m] + w / 2) / W, yc, "Pred.", ha="center",
                 va="center", fontsize=FS_SUB, style="italic")
        fig.text((x_err[m] + w / 2) / W, yc, "|Err|", ha="center",
                 va="center", fontsize=FS_SUB, style="italic")
    y += SUBHEAD
    y_axes0 = y

    def draw(ax, arr, cmap, lo, hi, src, xlab, ylab):
        im = ax.imshow(arr, extent=(0, Lx, Ly, 0), origin="upper", cmap=cmap,
                       aspect="equal", vmin=lo, vmax=hi,
                       interpolation="nearest")
        if is_wedge:
            ax.plot([0, Lx], [0, Ly], "k-", linewidth=LW)
            ax.plot([Lx, Lx], [0, Ly], color="gray", linewidth=0.5,
                    linestyle="--")
        if ell.size == 4:
            cx, cy, a, b = [float(v) for v in ell]
            ax.add_patch(MplEllipse((cx, cy), width=2 * a, height=2 * b,
                                    fill=False, edgecolor="k", linewidth=LW))
        ax.plot(src[0], src[1], "r*", markersize=STAR_MS,
                markeredgewidth=0.3, markeredgecolor="darkred")
        ax.set_xlim(0, Lx)
        ax.set_ylim(Ly, 0)
        ax.set_xticks([0, 50, 100])
        ax.set_yticks([0, 50, 100])
        ax.tick_params(labelsize=FS_TICK, labelbottom=xlab, labelleft=ylab)
        field_axes.append(ax)
        return im

    im_tl = im_err = None
    texts = []
    field_axes = []
    for r, (f, idx) in enumerate(cfg["rows"]):
        assert freqs[idx] == f, (cfg["cases"][0], idx, freqs[idx], f)
        src = d0["source_pos"][idx]
        gf = interp(d0, "fem_tl", idx)
        last = r == nrow - 1
        yb = 1 - (y + ROW_TITLE - 1.8) / H     # 行小标题基线
        texts.append(fig.text(x_ref / W, yb, "%d Hz (%.1f, %.1f)"
                              % (f, src[0], src[1]), ha="left",
                              va="baseline", fontsize=FS_ROW,
                              fontweight="bold"))
        y += ROW_TITLE
        im_tl = draw(fig.add_axes(box(x_ref, y, w, w)), gf, "jet",
                     vmin, vmax, src, last, True)
        for m, d in enumerate(datas):
            gp = interp(d, "pred_tl", idx)
            draw(fig.add_axes(box(x_pred[m], y, w, w)), gp, "jet",
                 vmin, vmax, src, last, False)
            err = np.abs(gp - gf)
            texts.append(fig.text((x_err[m] + w) / W, yb,
                                  "%.2f dB" % float(np.nanmean(err)),
                                  ha="right", va="baseline", fontsize=FS_AVG))
            im_err = draw(fig.add_axes(box(x_err[m], y, w, w)), err, "Reds",
                          0, ERR_HI, src, last, False)
        y += w

    # 共享轴名: 纵轴一次(居中于全部行)，横轴一次(居中于全宽)
    fig.text(4.0 / W, 1 - (y_axes0 + y) / 2 / H, "Y / Depth (m)",
             rotation=90, ha="left", va="center", fontsize=FS_LABEL)
    fig.text((x_ref + (x_err[-1] + w)) / 2 / W, 1 - (y + X_BAND - 3.0) / H,
             "X / Range (m)", ha="center", va="baseline", fontsize=FS_LABEL)
    y += X_BAND
    if cfg["cbar"]:
        bh = 3.5
        for (xa, xb, im, lbl, tk) in [
                (x_ref, x_err[1] + w, im_tl, "TL (dB)", [-60, -40, -20, 0]),
                (x_pred[3], x_err[4] + w, im_err, "|Error| (dB)",
                 [0, 2, 4, 6, 8, 10])]:
            cax = fig.add_axes(box(xa, y + 2.0, xb - xa, bh))
            cb = fig.colorbar(im, cax=cax, orientation="horizontal", ticks=tk)
            cb.outline.set_linewidth(0.5)
            cb.ax.tick_params(labelsize=FS_TICK, length=1.5, pad=1.0,
                              width=0.5)
            cb.set_label(lbl, fontsize=FS_LABEL, labelpad=1.0)

    # 行标题与平均误差标注不得互相重叠
    fig.canvas.draw()
    rr = fig.canvas.get_renderer()
    bbs = [t.get_window_extent(rr) for t in texts]
    # 末行相邻格(Pred 与 |Err| 仅隔 PAIR_GAP)横轴刻度标签不得相碰
    ticks = [t.get_window_extent(rr) for ax in field_axes
             for t in ax.get_xticklabels() if t.get_visible() and t.get_text()]
    for i in range(len(ticks)):
        for j in range(i + 1, len(ticks)):
            assert not ticks[i].overlaps(ticks[j]), "x tick labels collide"
    for i in range(len(bbs)):
        for j in range(i + 1, len(bbs)):
            assert not bbs[i].overlaps(bbs[j]), (texts[i].get_text(),
                                                 texts[j].get_text())
    fig.savefig(out_pdf, dpi=300)
    plt.close(fig)
    return W, H, w


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, cfg in GROUPS.items():
        W, H, w = render(cfg, os.path.join(OUT, name + ".pdf"))
        print("[fig8] %-14s %.1f x %.1f pt, panel %.1f pt" % (name, W, H, w))
    print("-> " + OUT)


if __name__ == "__main__":
    main()
