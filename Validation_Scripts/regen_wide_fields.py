#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
regen_wide_fields.py
====================
只重绘论文图6/7 的宽扁域 TL 场图：Case04_R2, Case05_R3 (rect),
Case10_W2, Case11_W3 (wedge)。这些域 Lx≫Ly，原图 aspect='equal' 下场图很矮、
色条却按整格高度画(shrink=0.8) → 色条比场图高好几倍，场图显得很小。

改法(内容不变，仅版式)：
  * 色条改用 make_axes_locatable 贴着场图右侧，**色条高度 == 场图高度**(对齐)；
  * 按域宽高比压缩每行高度，去掉大片竖直留白，使场图在 float 里占比更大 → 视觉更大；
  * 字号沿用 regen_results_bigfont 的大字号。

数据/渲染逻辑与 regen_results_bigfont.py 完全一致(griddata cubic + 遮罩 + clip)。
原图备份到 Figures/results/_bak_wide_<时间>/ 后覆盖。
"""
import os
import glob
import shutil
import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse as MplEllipse
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata

PAPER = r"D:\JASA\OE\els-cas-templates\Figures\results"
# npz 数据源(宽扁域案例在 D:\Data\Case3-14 下)
CASE_ROOT = r"D:\Data"

FS_LABEL = 16
FS_TITLE = 17
FS_CBAR = 15
FS_TICK = 14
STAR_MS = 16

# 图6/7 的四张宽扁域图(其余方形域图不动)
TARGETS = ["Case04_R2_TL", "Case05_R3_TL", "Case10_W2_TL", "Case11_W3_TL"]


def find_npz(case):
    prefix = case.split("_")[0]
    hits = glob.glob(os.path.join(CASE_ROOT, "Case*", f"{prefix}_*",
                                  "*__TL原始数据_ep200.npz"))
    return hits[0] if hits else None


def render(npz_path, out_pdf, method="cubic", grid_res=200):
    data = np.load(npz_path, allow_pickle=True)
    pred_tl_all = data["pred_tl"]
    fem_tl_all = data["fem_tl"]
    x_coords = data["x_coords"]
    y_coords = data["y_coords"]
    source_pos_all = data["source_pos"]
    freq_all = data["freq"]
    Lx_dom = float(data["Lx_dom"])
    Ly_dom = float(data["Ly_dom"])
    is_wedge = bool(data["is_wedge"])
    ellipse = data["ellipse"]
    vmin = float(data["vmin"])
    vmax = float(data["vmax"])
    epoch = int(data["epoch"])
    domain_label = str(data["domain_label"])

    has_ellipse = ellipse.size == 4
    if has_ellipse:
        cx, cy, a, b = [float(v) for v in ellipse]

    n = pred_tl_all.shape[0]
    gx_lin = np.linspace(0, Lx_dom, grid_res)
    gy_lin = np.linspace(0, Ly_dom, grid_res)
    grid_x, grid_y = np.meshgrid(gx_lin, gy_lin)
    wedge_outside = (grid_y > (Ly_dom / Lx_dom) * grid_x) if is_wedge \
        else np.zeros_like(grid_x, dtype=bool)
    extent = (0, Lx_dom, Ly_dom, 0)

    # 场图目标宽度尽量大、figW 只由 3 个场图构成(色条用 fraction 从场图区域内取，
    # 不额外膨胀 figW)，使 mapH/figW 达到"并排三列 + 等比"下的上限，
    # 场图页面尺寸不小于原图。行高压到 ~场图高 + 标题带，使色条(=绘图框高)与场图等高。
    cell_w = 6.2                     # 每个子图轴的目标宽度(in)
    ar = Ly_dom / Lx_dom             # 场图高/宽(<1 表示宽扁)
    map_h = cell_w * ar              # 场图高度
    row_h = map_h + 1.25             # + 双行标题/刻度/xlabel 的固定留白
    fig_w = cell_w * 3               # 不加横向余量，避免场图相对变小
    fig_h = row_h * n + 0.6

    fig, axes = plt.subplots(n, 3, figsize=(fig_w, fig_h))
    if n == 1:
        axes = axes.reshape(1, -1)

    for i in range(n):
        grid_pred = griddata((x_coords, y_coords), pred_tl_all[i],
                             (grid_x, grid_y), method=method)
        grid_fem = griddata((x_coords, y_coords), fem_tl_all[i],
                            (grid_x, grid_y), method=method)
        if has_ellipse:
            inside = ((grid_x - cx) / a) ** 2 + ((grid_y - cy) / b) ** 2 <= 1.0
            grid_pred[inside] = np.nan
            grid_fem[inside] = np.nan
        grid_pred[wedge_outside] = np.nan
        grid_fem[wedge_outside] = np.nan
        grid_pred = np.clip(grid_pred, vmin, vmax)
        grid_fem = np.clip(grid_fem, vmin, vmax)
        err = np.abs(grid_pred - grid_fem)
        avg_err = float(np.nanmean(err))
        err_vmax = min(float(np.nanmax(err)) if np.any(np.isfinite(err)) else 10.0,
                       10.0)
        src = source_pos_all[i]
        freq = freq_all[i]

        titles = [
            f"Ours TL (f={freq:.0f}Hz)\nSrc:({src[0]:.1f},{src[1]:.1f})",
            f"COMSOL TL (f={freq:.0f}Hz)",
            f"Error vs COMSOL | Avg:{avg_err:.2f} dB",
        ]
        data_list = [grid_pred, grid_fem, err]
        cmap_list = ["jet", "jet", "Reds"]
        vmin_list = [vmin, vmin, 0]
        vmax_list = [vmax, vmax, err_vmax]
        clbl_list = ["TL (dB)", "TL (dB)", "Error (dB)"]

        for j in range(3):
            ax = axes[i, j]
            im = ax.imshow(data_list[j], extent=extent, origin="upper",
                           cmap=cmap_list[j], aspect="equal",
                           vmin=vmin_list[j], vmax=vmax_list[j])
            if is_wedge:
                ax.plot([0, Lx_dom], [0, Ly_dom], "k-", linewidth=1.8)
                ax.plot([Lx_dom, Lx_dom], [0, Ly_dom], color="gray",
                        linewidth=1.2, linestyle="--")
            if has_ellipse:
                ax.add_patch(MplEllipse((cx, cy), width=2 * a, height=2 * b,
                                        fill=False, edgecolor="k",
                                        linewidth=1.8))
            ax.plot(src[0], src[1], "r*", markersize=STAR_MS)
            ax.set_xlabel("X / Range (m)", fontsize=FS_LABEL)
            ax.set_ylabel("Y / Depth (m)", fontsize=FS_LABEL)
            ax.set_title(titles[j], fontsize=FS_TITLE, fontweight="bold")
            ax.set_xlim(0, Lx_dom)
            ax.set_ylim(Ly_dom, 0)
            ax.tick_params(axis="both", labelsize=FS_TICK)
            # 色条高度 == 场图高度：行高已压到贴合场图，绘图框高≈场图高，
            # append_axes 的 cax 取绘图框高 → 色条与场图等高对齐。
            div = make_axes_locatable(ax)
            cax = div.append_axes("right", size="3.5%", pad=0.10,
                                  axes_class=plt.Axes)
            cbar = plt.colorbar(im, cax=cax)
            cbar.set_label(clbl_list[j], fontsize=FS_CBAR)
            cbar.ax.tick_params(labelsize=FS_TICK - 2)
            for spine in ax.spines.values():
                spine.set_edgecolor("black")
                spine.set_linewidth(1.5)

    plt.suptitle(f"[{domain_label}] TL Field  Epoch {epoch}",
                 fontsize=24, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.985])
    plt.savefig(out_pdf, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = os.path.join(PAPER, f"_bak_wide_{stamp}")
    os.makedirs(bak, exist_ok=True)
    for case in TARGETS:
        out = os.path.join(PAPER, case + ".pdf")
        npz = find_npz(case)
        if npz is None:
            print(f"[SKIP] {case}: npz 未找到")
            continue
        shutil.copy2(out, os.path.join(bak, case + ".pdf"))
        render(npz, out)
        print(f"[OK] {case}")
    print(f"\n[DONE] 原图备份 → {bak}")


if __name__ == "__main__":
    main()
