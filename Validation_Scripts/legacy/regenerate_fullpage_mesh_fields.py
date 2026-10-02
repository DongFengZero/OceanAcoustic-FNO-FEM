#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
regen_results_bigfont.py
========================
生成论文图（第四章）——本脚本是这 7 张图的成图入口：
    Fig. 5   fig:res-128        Cases 3, 9        (R1/W1, 多频, 128 m)  4.3 节
    Fig. 6   fig:res-256        Cases 4, 10       (R2/W2, 多频, 256 m)  4.3 节
    Fig. 7   fig:res-512        Cases 5, 11       (R3/W3, 多频, 512 m)  4.3 节
    Fig. 8   fig:res-rect-100   Cases 6, 7, 8     (R4/R5/R6, 100 Hz)    4.3 节
    Fig. 9   fig:res-wedge-100  Cases 12, 13, 14  (W4/W5/W6, 100 Hz)    4.3 节
    Fig. 18  fig:mesh-rect      Cases 33, 34, 35  (R4/R7/R8, 网格无关)  4.6 节
    Fig. 19  fig:mesh-wedge     Cases 36, 37, 38  (W4/W7/W8, 网格无关)  4.6 节

重绘 results/ 下当前论文使用的 36 张 TL 对比图 (CaseNN_XX_TL.pdf)。
结构与原图完全一致 (每个 case 8×3 网格: Ours / COMSOL / Error)，
仅放大字体、加粗刻度与标记，解决原图字体偏小的问题。

数据来源: 各 case 目录内自带的 `*__TL原始数据_ep200.npz`
(与 restore_tl_figure.py 使用的同一数据、同一渲染逻辑)。

原图自动备份到 results/_原图备份/ 后再覆盖。
"""
import os
import sys
import glob
import shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse as MplEllipse
from scipy.interpolate import griddata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _figpaths  # noqa: E402
OUT = _figpaths.figdir(__file__)
RESULTS = OUT
BACKUP = os.path.join(RESULTS, "_原图备份")

# ---- 放大后的字号/线宽 (原值见注释) ----
FS_LABEL = 19      # 原 10
FS_TITLE = 20      # 原 10
FS_CBAR = 17       # 原 9
FS_TICK = 16       # 原默认 ~10
FS_SUPTITLE = 28   # 原 12
STAR_MS = 19       # 原 10


def _find_case_npz(case):
    """按 CaseNN 前缀定位 npz（兼容 results 命名与目录命名的差异）。"""
    prefix = case.split("_")[0]  # e.g. Case24
    try:
        return _figpaths.npz(prefix)
    except FileNotFoundError:
        try:
            return _figpaths.npz(case)
        except FileNotFoundError:
            return None


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

    if is_wedge:
        wedge_outside = grid_y > (Ly_dom / Lx_dom) * grid_x
    else:
        wedge_outside = np.zeros_like(grid_x, dtype=bool)

    fig, axes = plt.subplots(n, 3, figsize=(14, 4.2 * n))
    if n == 1:
        axes = axes.reshape(1, -1)

    extent = (0, Lx_dom, Ly_dom, 0)

    for i in range(n):
        pred_tl = pred_tl_all[i]
        fem_tl = fem_tl_all[i]
        source_pos = source_pos_all[i]
        freq = freq_all[i]

        grid_pred = griddata((x_coords, y_coords), pred_tl,
                             (grid_x, grid_y), method=method)
        grid_fem = griddata((x_coords, y_coords), fem_tl,
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

        titles = [
            f"Ours TL (f={freq:.0f}Hz)\nSrc:({source_pos[0]:.1f},{source_pos[1]:.1f})",
            f"COMSOL TL (f={freq:.0f}Hz)",
            f"Error vs COMSOL | Avg:{avg_err:.2f} dB",
        ]
        data_list = [grid_pred, grid_fem, err]
        cmap_list = ["jet", "jet", "Reds"]
        vmin_list = [vmin, vmin, 0]
        vmax_list = [vmax, vmax, err_vmax]

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
                                        linewidth=1.8, linestyle="-"))
            ax.plot(source_pos[0], source_pos[1], "r*", markersize=STAR_MS)
            ax.set_xlabel("X / Range (m)", fontsize=FS_LABEL)
            ax.set_ylabel("Y / Depth (m)", fontsize=FS_LABEL)
            ax.set_title(titles[j], fontsize=FS_TITLE, fontweight="bold")
            ax.set_xlim(0, Lx_dom)
            ax.set_ylim(Ly_dom, 0)
            ax.tick_params(axis="both", labelsize=FS_TICK)
            cbar = plt.colorbar(im, ax=ax, fraction=0.035, pad=0.04, shrink=0.8)
            cbar.set_label("TL (dB)" if j < 2 else "Error (dB)",
                           fontsize=FS_CBAR)
            cbar.ax.tick_params(labelsize=FS_TICK - 2)
            for spine in ax.spines.values():
                spine.set_edgecolor("black")
                spine.set_linewidth(1.5)

    plt.suptitle(f"[{domain_label}] TL Field  Epoch {epoch}",
                 fontsize=FS_SUPTITLE, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.97], w_pad=0.25, h_pad=0.5)
    plt.savefig(out_pdf, dpi=150, bbox_inches="tight")
    plt.close(fig)


# 本图对应的 6 张网格无关性场图（Fig. 10 的六个子图）
MESH_CASES = ["Case33_R4", "Case34_R7", "Case35_R8",
              "Case36_W4", "Case37_W7", "Case38_W8"]


def main():
    """重绘 Fig. 10 的 6 张场图。

    注意：本脚本按“就地覆盖”设计（原图先备份到 out/_原图备份/）。它采用本
    文件顶部的字号常量出图，**不**是论文里 207 pt 小面板那一版；论文的版式
    由 fig04_res_128.py 的 rows_single() 负责。因此默认需要显式指定来源
    目录，避免误覆盖论文成图。
    """
    src_dir = os.environ.get("CH4_FIGSRC", "")
    if not src_dir:
        raise SystemExit(
            "本脚本会就地覆盖输入图，因此需要显式指定来源目录："
            "设置 CH4_FIGSRC=<论文>/Figures/results 后重跑。"
            "论文版式的网格图由 fig04_res_128.py 生成。")
    pdfs = [os.path.join(src_dir, c + "_TL.pdf") for c in MESH_CASES
            if os.path.exists(os.path.join(src_dir, c + "_TL.pdf"))]
    if not pdfs:
        raise SystemExit("未找到 Fig.10 的场图: %s" % src_dir)

    os.makedirs(BACKUP, exist_ok=True)

    ok, fail = 0, 0
    for p in pdfs:
        fname = os.path.basename(p)
        case = fname[:-7]  # 去掉 _TL.pdf
        npz = _find_case_npz(case)
        if npz is None:
            print(f"[SKIP] {case}: 未找到 npz")
            fail += 1
            continue

        # 备份原图（若备份不存在）
        bak = os.path.join(BACKUP, fname)
        if not os.path.exists(bak):
            shutil.copy2(p, bak)

        try:
            render(npz, p)
            print(f"[OK] {case}")
            ok += 1
        except Exception as e:
            print(f"[FAIL] {case}: {e}")
            fail += 1

    print(f"\n[DONE] 重绘 {ok} 张, 失败/跳过 {fail} 张")
    print(f"[DONE] 原图已备份 → {BACKUP}")


if __name__ == "__main__":
    main()
