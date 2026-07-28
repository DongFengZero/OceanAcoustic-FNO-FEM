#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
regen_ideal_panels.py
=====================
重绘论文图3(R0)/图4(W0) 的解析验证面板 CaseNN_XX_fYY_panel.pdf。
统一风格：
  * 深度线(最左)——与图10-13(advantage_depth_line)一致：解析解画成粗灰底带，
    本文预测画成醒目粗红线；网格 alpha0.25、黑色粗描边。最左子图**加宽成长方形**。
  * 声场(中/右)——与图5(regen_results_bigfont)一致：jet 色图、源位置红星、
    标题 "Ours TL (f=..)"/"Analytical TL (f=..)"、shrink 式色条、黑色粗描边。
  * 三个子图**等高**；字号统一放大(label/title/tick 与图5同款基准)。
每个频率 = 一整行(1x3)，四个频率各存一个 panel.pdf；tex 里 4 行满栏堆叠，充分利用版面。

数据源 D:\\Data\\Case1-2。深度线沿 y≈44.7m(与表 tab:ideal-depthline 口径一致)，
每频率取该行 MAE 最小的样本(与表数值对应)。原图备份后覆盖。
"""
import os
import shutil
import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata

PAPER = r"D:\JASA\OE\els-cas-templates\Figures\results"
CASE_ROOT = r"D:\Data\Case1-2"
GRID = 220
METHOD = "cubic"
FREQS = [25, 50, 75, 100]
Y_LINE = 44.7   # 与表 tab:ideal-depthline 一致

# 字号(与图5 regen_results_bigfont 同款基准，稍大以配合满栏行排版)
FS_LABEL = 17
FS_TITLE = 18
FS_CBAR = 16
FS_TICK = 15
STAR_MS = 15

CASES = {
    "Case01_R0": dict(freq_prefix="R0", domain="Rectangle"),
    "Case02_W0": dict(freq_prefix="W0", domain="Wedge"),
}


def load(case):
    p = os.path.join(CASE_ROOT, case, f"{case}__TL原始数据_ep200.npz")
    return np.load(p, allow_pickle=True)


def grids(data, i):
    xc, yc = data["x_coords"], data["y_coords"]
    Lx, Ly = float(data["Lx_dom"]), float(data["Ly_dom"])
    is_wedge = bool(data["is_wedge"])
    vmin, vmax = float(data["vmin"]), float(data["vmax"])
    gx = np.linspace(0, Lx, GRID)
    gy = np.linspace(0, Ly, GRID)
    GX, GY = np.meshgrid(gx, gy)
    gp = griddata((xc, yc), data["pred_tl"][i], (GX, GY), METHOD)
    gf = griddata((xc, yc), data["fem_tl"][i], (GX, GY), METHOD)
    if is_wedge:
        outside = GY > (Ly / Lx) * GX
        gp[outside] = np.nan
        gf[outside] = np.nan
    gp = np.clip(gp, vmin, vmax)
    gf = np.clip(gf, vmin, vmax)
    return gx, gy, GX, GY, gp, gf, Lx, Ly, is_wedge, vmin, vmax


def pick_sample(data, freq):
    """该频率下取 y=Y_LINE 行 MAE 最小的样本。返回 (idx, row_mae)。"""
    freqs = [int(round(f)) for f in data["freq"]]
    cand = [i for i in range(len(freqs)) if freqs[i] == freq]
    best = None
    for i in cand:
        gx, gy, GX, GY, gp, gf, Lx, Ly, isw, vmin, vmax = grids(data, i)
        r = int(np.argmin(np.abs(gy - Y_LINE)))
        fem = gf[r]; ok = np.isfinite(fem) & np.isfinite(gp[r])
        if ok.sum() < 20:
            continue
        mae = float(np.mean(np.abs((gp[r] - fem)[ok])))
        if best is None or mae < best[1]:
            best = (i, mae)
    return best if best else (cand[0], np.nan)


def render_panel(data, freq, out_pdf, domain):
    idx, _ = pick_sample(data, freq)
    gx, gy, GX, GY, gp, gf, Lx, Ly, is_wedge, vmin, vmax = grids(data, idx)
    src = data["source_pos"][idx]
    extent = (0, Lx, Ly, 0)
    r = int(np.argmin(np.abs(gy - Y_LINE)))
    yv = float(gy[r])

    # 1x3 一行：深度线(加宽) | Ours 场 | Analytical 场；等高。
    # 深度线宽度 ~1.7x 场图，用 width_ratios 实现"长方形"。
    fig = plt.figure(figsize=(20, 4.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.75, 1, 1],
                          left=0.055, right=0.965, top=0.86, bottom=0.17,
                          wspace=0.32)

    # --- 深度线(fig10-13 风格) ---
    axL = fig.add_subplot(gs[0, 0])
    ref = gf[r]; prd = gp[r]
    ok = np.isfinite(ref)
    vidx = np.where(ok)[0]
    x_lo, x_hi = float(gx[vidx[0]]), float(gx[vidx[-1]])
    axL.plot(gx, np.where(ok, ref, np.nan), color="0.55", linewidth=6.0,
             alpha=0.55, solid_capstyle="round", zorder=2, label="Analytical")
    axL.plot(gx, np.where(ok, prd, np.nan), color="#d62728", linewidth=3.0,
             solid_capstyle="round", zorder=9, label="Ours")
    axL.set_xlim(x_lo, x_hi)
    axL.set_xlabel("X / Range (m)", fontsize=FS_LABEL)
    axL.set_ylabel("TL (dB)", fontsize=FS_LABEL)
    axL.set_title(f"Depth-line TL @ y={Y_LINE:.1f} m", fontsize=FS_TITLE,
                  fontweight="bold")
    axL.tick_params(labelsize=FS_TICK)
    axL.grid(True, alpha=0.25)
    axL.legend(fontsize=FS_TICK, framealpha=0.9, loc="best")
    for sp in axL.spines.values():
        sp.set_edgecolor("black"); sp.set_linewidth(1.5)

    # --- 两个声场(fig5 风格) ---
    for col, (arr, title) in enumerate([
            (gp, f"Ours TL (f={freq:.0f}Hz)"),
            (gf, f"Analytical TL (f={freq:.0f}Hz)")], start=1):
        ax = fig.add_subplot(gs[0, col])
        im = ax.imshow(arr, extent=extent, origin="upper", cmap="jet",
                       aspect="equal", vmin=vmin, vmax=vmax)
        if is_wedge:
            ax.plot([0, Lx], [0, Ly], "k-", linewidth=1.8)
            ax.plot([Lx, Lx], [0, Ly], color="gray", linewidth=1.2,
                    linestyle="--")
        ax.plot(src[0], src[1], "r*", markersize=STAR_MS)
        ax.set_xlabel("X / Range (m)", fontsize=FS_LABEL)
        if col == 1:
            ax.set_ylabel("Y / Depth (m)", fontsize=FS_LABEL)
        ax.set_title(title, fontsize=FS_TITLE, fontweight="bold")
        ax.set_xlim(0, Lx); ax.set_ylim(Ly, 0)
        ax.tick_params(labelsize=FS_TICK)
        div = make_axes_locatable(ax)
        cax = div.append_axes("right", size="4.5%", pad=0.08)
        cbar = plt.colorbar(im, cax=cax)
        cbar.set_label("TL (dB)", fontsize=FS_CBAR)
        cbar.ax.tick_params(labelsize=FS_TICK - 2)
        for sp in ax.spines.values():
            sp.set_edgecolor("black"); sp.set_linewidth(1.5)

    fig.suptitle(f"[{domain}]  f = {freq:.0f} Hz",
                 fontsize=FS_TITLE + 2, fontweight="bold", y=0.98)
    fig.savefig(out_pdf, dpi=150, bbox_inches="tight")
    plt.close(fig)


def pick_two(data, freq):
    """该频率下按 y=Y_LINE 行 MAE 升序取前 2 个样本索引。"""
    freqs = [int(round(f)) for f in data["freq"]]
    cand = [i for i in range(len(freqs)) if freqs[i] == freq]
    scored = []
    for i in cand:
        gx, gy, GX, GY, gp, gf, Lx, Ly, isw, vmin, vmax = grids(data, i)
        r = int(np.argmin(np.abs(gy - Y_LINE)))
        fem = gf[r]; ok = np.isfinite(fem) & np.isfinite(gp[r])
        mae = float(np.mean(np.abs((gp[r] - fem)[ok]))) if ok.sum() >= 20 else 1e9
        scored.append((mae, i))
    scored.sort()
    return [i for _, i in scored[:2]] or cand[:2]


def _draw_unit(fig, gs_slice, data, freq, idx, k, base_col):
    """在 gs_slice(3 个子列: 深度线|Ours|Analytical)里画一个 (freq,sample) 单元。
    base_col 用于判断是否画 y 轴标签(每行最左单元才画)。"""
    gx, gy, GX, GY, gp, gf, Lx, Ly, is_wedge, vmin, vmax = grids(data, idx)
    src = data["source_pos"][idx]
    extent = (0, Lx, Ly, 0)
    r = int(np.argmin(np.abs(gy - Y_LINE)))
    tag = chr(ord("a") + k)

    # 深度线(fig10-13 风格)
    axL = fig.add_subplot(gs_slice[0])
    ref = gf[r]; prd = gp[r]
    ok = np.isfinite(ref)
    vidx = np.where(ok)[0]
    axL.plot(gx, np.where(ok, ref, np.nan), color="0.55", linewidth=6.0,
             alpha=0.55, solid_capstyle="round", zorder=2, label="Analytical")
    axL.plot(gx, np.where(ok, prd, np.nan), color="#d62728", linewidth=3.0,
             solid_capstyle="round", zorder=9, label="Ours")
    axL.set_xlim(float(gx[vidx[0]]), float(gx[vidx[-1]]))
    axL.set_xlabel("X / Range (m)", fontsize=FS_LABEL)
    axL.set_ylabel(f"f={freq:.0f}Hz ({tag})\nTL (dB)", fontsize=FS_LABEL)
    # Src 保留一位小数，全章坐标统一口径（场图 regen_results_bigfont.py 等
    # 一贯用 .1f）。取整会把 39.5 与 40.0 印成同一个数，无法回溯到具体样本，
    # 故不用 .0f。标题分两行：第一行深度线位置，第二行源坐标。
    axL.set_title(f"Depth-line @ y={Y_LINE:.1f} m\n"
                  f"Src ({float(src[0]):.1f},{float(src[1]):.1f})",
                  fontsize=FS_TITLE, fontweight="bold")
    axL.tick_params(labelsize=FS_TICK)
    axL.grid(True, alpha=0.25)
    axL.legend(fontsize=FS_TICK - 1, framealpha=0.9, loc="best")
    for sp in axL.spines.values():
        sp.set_edgecolor("black"); sp.set_linewidth(1.5)

    # 两个声场(fig5 风格)
    for j, (arr, ttl) in enumerate([
            (gp, f"Ours TL (f={freq:.0f}Hz)"),
            (gf, f"Analytical TL (f={freq:.0f}Hz)")], start=1):
        ax = fig.add_subplot(gs_slice[j])
        im = ax.imshow(arr, extent=extent, origin="upper", cmap="jet",
                       aspect="equal", vmin=vmin, vmax=vmax)
        if is_wedge:
            ax.plot([0, Lx], [0, Ly], "k-", linewidth=1.8)
            ax.plot([Lx, Lx], [0, Ly], color="gray", linewidth=1.2,
                    linestyle="--")
        ax.plot(src[0], src[1], "r*", markersize=STAR_MS)
        ax.set_xlabel("X / Range (m)", fontsize=FS_LABEL)
        if j == 1:
            ax.set_ylabel("Y / Depth (m)", fontsize=FS_LABEL)
        ax.set_title(ttl, fontsize=FS_TITLE, fontweight="bold")
        ax.set_xlim(0, Lx); ax.set_ylim(Ly, 0)
        ax.tick_params(labelsize=FS_TICK)
        div = make_axes_locatable(ax)
        cax = div.append_axes("right", size="4.5%", pad=0.08)
        cbar = plt.colorbar(im, cax=cax)
        cbar.set_label("TL (dB)", fontsize=FS_CBAR)
        cbar.ax.tick_params(labelsize=FS_TICK - 2)
        for sp in ax.spines.values():
            sp.set_edgecolor("black"); sp.set_linewidth(1.5)


def render_grid2(data, out_pdf, domain):
    """4 行(频率) × 2 列(样本 a|b) 布局，每个单元 = [宽深度线 | Ours | Analytical]。
    比 8x1 更宽更矮，行距/图像更大。"""
    picks = {f: pick_two(data, f) for f in FREQS}
    nrow = len(FREQS)          # 4 频率行
    # 每列单元 = 3 子列(1.75:1:1)，两单元之间加一个窄间隔列
    fig = plt.figure(figsize=(26, 3.7 * nrow))
    gs = fig.add_gridspec(
        nrow, 7,
        width_ratios=[1.75, 1, 1, 0.45, 1.75, 1, 1],
        left=0.045, right=0.985, top=0.965, bottom=0.045,
        hspace=0.62, wspace=0.46)

    for ri, f in enumerate(FREQS):
        ids = picks[f]
        # 左单元(样本 a): 子列 0,1,2
        _draw_unit(fig, [gs[ri, 0], gs[ri, 1], gs[ri, 2]], data, f, ids[0], 0, 0)
        # 右单元(样本 b): 子列 4,5,6
        if len(ids) > 1:
            _draw_unit(fig, [gs[ri, 4], gs[ri, 5], gs[ri, 6]],
                       data, f, ids[1], 1, 4)

    fig.savefig(out_pdf, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    for case, cfg in CASES.items():
        data = load(case)
        out = os.path.join(PAPER, f"{case}_grid2.pdf")
        render_grid2(data, out, cfg["domain"])
        print(f"[OK] {case}_grid2.pdf  (8 rows x 3 cols)")
    print("\n[DONE] 满页 8 行网格 → " + PAPER)


if __name__ == "__main__":
    main()
