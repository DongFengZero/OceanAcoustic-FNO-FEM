#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
regen_method_grid.py
====================
把图14-17(方法对比 R1/W1、消融 R1/W1)从"5(或4)个方法各自一张 8x3 全图并排"
(COMSOL 列重复 4-5 次、96-120 个微型子图、字迹不可辨)重构为**单张统一网格**：

  行 = 4 个频率(25/50/75/100 Hz，各取 1 个代表样本)
  列 = COMSOL(只出一次) | 各方法 (Prediction, |Error|) 成对

这样去掉了 COMSOL 的 4-5 次重复、样本行减半，子图显著放大、文字可辨。
每组输出一个 PDF：perf_grid_R1 / perf_grid_W1 / abl_grid_R1 / abl_grid_W1。
数据源 D:\\Data\\Case*；同组各方法共享同一 COMSOL/源位置(已核验)。
"""
import os
import glob
import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse as MplEllipse
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata

PAPER = r"D:\JASA\OE\els-cas-templates\Figures\results"
GRID = 200
METHOD = "cubic"
FREQS = [25, 50, 75, 100]

# 字号放大 ~1.4x：两张 8 行网格要挤进一页(各约 0.72 栏高)，在 tex 里会被
# 缩到约 0.72x 显示；放大 native 字号补偿，使纸面文字仍清晰(目标 ~3pt)。
FS_LABEL = 21
FS_TITLE = 22
FS_CBAR = 18
FS_TICK = 17
STAR_MS = 15
ERR_HI = 10.0

GROUPS = {
    "perf_grid_R1": dict(domain="Rectangle", nsample=2, methods=[
        ("Case15_R1_Proposed", "Proposed"), ("Case16_R1_DeepONet", "DeepONet"),
        ("Case17_R1_FNO", "FNO"), ("Case18_R1_KNO", "KNO"),
        ("Case19_R1_CNO", "CNO")]),
    "perf_grid_W1": dict(domain="Wedge", nsample=2, methods=[
        ("Case20_W1_Proposed", "Proposed"), ("Case21_W1_DeepONet", "DeepONet"),
        ("Case22_W1_FNO", "FNO"), ("Case23_W1_KNO", "KNO"),
        ("Case24_W1_CNO", "CNO")]),
    "abl_grid_R1": dict(domain="Rectangle", methods=[
        ("Case25_R1_Full", "Full model"), ("Case26_R1_no_prior", "w/o prior"),
        ("Case27_R1_no_graph", "w/o graph"),
        ("Case28_R1_no_prior_loss", "w/o prior-sup.")]),
    "abl_grid_W1": dict(domain="Wedge", methods=[
        ("Case29_W1_Full", "Full model"), ("Case30_W1_no_prior", "w/o prior"),
        ("Case31_W1_no_graph", "w/o graph"),
        ("Case32_W1_no_prior_loss", "w/o prior-sup.")]),
}


def find_npz(sub):
    h = glob.glob(rf"D:\Data\Case*\{sub}\*__TL原始数据_ep200.npz")
    return h[0] if h else None


def grid_of(data, i):
    xc, yc = data["x_coords"], data["y_coords"]
    Lx, Ly = float(data["Lx_dom"]), float(data["Ly_dom"])
    is_wedge = bool(data["is_wedge"])
    vmin, vmax = float(data["vmin"]), float(data["vmax"])
    ell = data["ellipse"]
    gx = np.linspace(0, Lx, GRID)
    gy = np.linspace(0, Ly, GRID)
    GX, GY = np.meshgrid(gx, gy)
    g = griddata((xc, yc), data["pred_tl"][i], (GX, GY), METHOD)
    if is_wedge:
        g[GY > (Ly / Lx) * GX] = np.nan
    if ell.size == 4:
        cx, cy, a, b = [float(v) for v in ell]
        g[((GX - cx) / a) ** 2 + ((GY - cy) / b) ** 2 <= 1.0] = np.nan
    return np.clip(g, vmin, vmax), (Lx, Ly, is_wedge, vmin, vmax, ell)


def fem_grid(data, i):
    xc, yc = data["x_coords"], data["y_coords"]
    Lx, Ly = float(data["Lx_dom"]), float(data["Ly_dom"])
    is_wedge = bool(data["is_wedge"])
    vmin, vmax = float(data["vmin"]), float(data["vmax"])
    ell = data["ellipse"]
    gx = np.linspace(0, Lx, GRID)
    gy = np.linspace(0, Ly, GRID)
    GX, GY = np.meshgrid(gx, gy)
    g = griddata((xc, yc), data["fem_tl"][i], (GX, GY), METHOD)
    if is_wedge:
        g[GY > (Ly / Lx) * GX] = np.nan
    if ell.size == 4:
        cx, cy, a, b = [float(v) for v in ell]
        g[((GX - cx) / a) ** 2 + ((GY - cy) / b) ** 2 <= 1.0] = np.nan
    return np.clip(g, vmin, vmax)


N_SAMPLE = 2   # 默认每频率展示的样本数(可被 group 的 nsample 覆盖)


def pick_rows(data, nsample=N_SAMPLE):
    """返回 [(freq, sample_idx, k), ...]，每频率取前 nsample 个样本作为独立行。"""
    freqs = [int(round(f)) for f in data["freq"]]
    rows = []
    for f in FREQS:
        ids = [i for i in range(len(freqs)) if freqs[i] == f][:nsample]
        for k, idx in enumerate(ids):
            rows.append((f, idx, k))
    return rows


def render(gname, cfg, out_pdf):
    methods = cfg["methods"]
    datas = [np.load(find_npz(sub), allow_pickle=True) for sub, _ in methods]
    base = datas[0]
    rows = pick_rows(base, cfg.get("nsample", N_SAMPLE))

    ncol = 1 + 2 * len(methods)   # COMSOL + (Pred,Err)*N
    nrow = len(rows)
    # 每列宽 3.05in，色条(make_axes_locatable 4.5%+pad)吃掉部分宽度后方形图约 2.85in 高。
    # 行高因子设为 ~2.9 贴合方形图高度，消除 aspect-equal 造成的行内竖直空白 → 图变大、行距变小。
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.05 * ncol, 2.9 * nrow))

    for ri, (f, idx, k) in enumerate(rows):
        gfem = fem_grid(base, idx)
        _, geom = grid_of(base, idx)
        Lx, Ly, is_wedge, vmin, vmax, ell = geom
        extent = (0, Lx, Ly, 0)
        src = base["source_pos"][idx]

        bottom = (ri == nrow - 1)

        def style(ax, first_col=False):
            if is_wedge:
                ax.plot([0, Lx], [0, Ly], "k-", linewidth=1.5)
                ax.plot([Lx, Lx], [0, Ly], color="gray", linewidth=1.0,
                        linestyle="--")
            if ell.size == 4:
                cx, cy, a, b = [float(v) for v in ell]
                ax.add_patch(MplEllipse((cx, cy), width=2 * a, height=2 * b,
                                        fill=False, edgecolor="k", linewidth=1.5))
            ax.plot(src[0], src[1], "r*", markersize=STAR_MS)
            ax.set_xlim(0, Lx); ax.set_ylim(Ly, 0)
            ax.tick_params(labelsize=FS_TICK)
            # 隐藏冗余刻度标签：非底行不标 x 刻度、非首列不标 y 刻度
            # (每行同一空间域，x/y 轴完全相同) → 压紧行/列间距，图像放大
            if not bottom:
                ax.tick_params(labelbottom=False)
            if not first_col:
                ax.tick_params(labelleft=False)
            for sp in ax.spines.values():
                sp.set_edgecolor("black"); sp.set_linewidth(1.2)

        def addcbar(ax, im, label):
            div = make_axes_locatable(ax)
            cax = div.append_axes("right", size="4.5%", pad=0.05)
            cb = plt.colorbar(im, cax=cax)
            cb.set_label(label, fontsize=FS_CBAR)
            cb.ax.tick_params(labelsize=FS_TICK - 2)

        # col 0: COMSOL (只出一次)
        ax = axes[ri, 0]
        im = ax.imshow(gfem, extent=extent, origin="upper", cmap="jet",
                       aspect="equal", vmin=vmin, vmax=vmax)
        style(ax, first_col=True); addcbar(ax, im, "TL (dB)")
        tag = chr(ord("a") + k)
        ax.set_ylabel(f"f = {f:.0f} Hz ({tag})\nY / Depth (m)", fontsize=FS_LABEL)
        if ri == 0:
            ax.set_title("COMSOL (Ref)", fontsize=FS_TITLE, fontweight="bold")
        if ri == nrow - 1:
            ax.set_xlabel("X / Range (m)", fontsize=FS_LABEL)

        # 各方法: Pred, |Err|
        for mi, (sub, label) in enumerate(methods):
            gp, _ = grid_of(datas[mi], idx)
            err = np.abs(gp - gfem)
            evmax = min(float(np.nanmax(err)) if np.any(np.isfinite(err)) else
                        ERR_HI, ERR_HI)
            cP = 1 + 2 * mi
            axP = axes[ri, cP]
            imP = axP.imshow(gp, extent=extent, origin="upper", cmap="jet",
                             aspect="equal", vmin=vmin, vmax=vmax)
            style(axP); addcbar(axP, imP, "TL (dB)")
            if ri == 0:
                axP.set_title(f"{label}\nPred.", fontsize=FS_TITLE,
                              fontweight="bold")
            if ri == nrow - 1:
                axP.set_xlabel("X / Range (m)", fontsize=FS_LABEL)

            axE = axes[ri, cP + 1]
            imE = axE.imshow(err, extent=extent, origin="upper", cmap="Reds",
                             aspect="equal", vmin=0, vmax=evmax)
            style(axE); addcbar(axE, imE, "|Err| (dB)")
            if ri == 0:
                axE.set_title(f"{label}\n|Error|", fontsize=FS_TITLE,
                              fontweight="bold")
            if ri == nrow - 1:
                axE.set_xlabel("X / Range (m)", fontsize=FS_LABEL)

    fig.suptitle(f"[{cfg['domain']}]  Prediction & |Error| by method "
                 f"(COMSOL reference shown once per row)",
                 fontsize=FS_TITLE + 3, fontweight="bold", y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    # 行距压紧(hspace 小)，列距放宽(wspace 大)避免色条刻度与右侧格子相互遮挡
    fig.subplots_adjust(hspace=0.06, wspace=0.55)
    fig.savefig(out_pdf, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = os.path.join(PAPER, f"_bak_methodgrid_{stamp}")
    os.makedirs(bak, exist_ok=True)
    for gname, cfg in GROUPS.items():
        out = os.path.join(PAPER, gname + ".pdf")
        render(gname, cfg, out)
        print(f"[OK] {gname}  ({1 + 2*len(cfg['methods'])} cols x "
              f"{len(FREQS)*cfg.get('nsample', N_SAMPLE)} rows)")
    print(f"\n[DONE] 统一网格图 → {PAPER}\n[备份空目录]{bak}")


if __name__ == "__main__":
    main()
