#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
restore_tl_figure.py
====================
从训练末轮保存的绘图原始张量 (`*_tl_raw_epoch*.npz`) 离线复现 TL 对比图，
无需重跑训练。复刻 ocean_trainer_forward_b.py 中 visualize_results 的
插值 + 绘图逻辑（节点级 pred_tl/fem_tl → griddata 插值 → imshow）。

npz 内容（由 Trainer._save_plot_raw_tensors 写出）：
    x_coords, y_coords : [Nnode]        FEM 节点坐标（物理坐标，x向右/y向下）
    pred_tl            : [n, Nnode]     每个样本的模型 TL（节点级，插值前）
    fem_tl             : [n, Nnode]     每个样本的 COMSOL TL（节点级）
    source_pos         : [n, 2]         声源坐标
    freq               : [n]            每个样本的频率 (Hz)
    Lx_dom, Ly_dom     : 标量           域尺寸
    is_wedge           : bool           楔形域标志
    ellipse            : [4] 或 []       椭圆障碍 [cx,cy,a,b]；空数组=无椭圆
    vmin, vmax         : 标量           TL 色标范围（默认 -60, 0 dB）
    epoch              : int
    domain_label       : str            'Wedge' / 'Rectangle'

用法
----
    # 复现并保存为 PDF（默认输出到 npz 同目录）
    python restore_tl_figure.py path/to/periodic_tl_raw_epoch200.npz

    # 指定输出文件
    python restore_tl_figure.py raw.npz -o my_figure.png

    # 屏幕显示（不保存）
    python restore_tl_figure.py raw.npz --show

    # 改插值方法 / 分辨率
    python restore_tl_figure.py raw.npz --method linear --grid 300
"""
import argparse
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")  # 默认无界面后端；--show 时会切换
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse as MplEllipse
from scipy.interpolate import griddata


def restore_figure(npz_path, out_path=None, method="cubic",
                   grid_res=200, show=False):
    data = np.load(npz_path, allow_pickle=True)

    x_coords = data["x_coords"]
    y_coords = data["y_coords"]
    pred_tl_all = data["pred_tl"]          # [n, Nnode]
    fem_tl_all = data["fem_tl"]            # [n, Nnode]
    source_pos_all = data["source_pos"]    # [n, 2]
    freq_all = data["freq"]                # [n]
    Lx_dom = float(data["Lx_dom"])
    Ly_dom = float(data["Ly_dom"])
    is_wedge = bool(data["is_wedge"])
    ellipse = data["ellipse"]              # [4] or []
    vmin = float(data["vmin"])
    vmax = float(data["vmax"])
    epoch = int(data["epoch"])
    domain_label = str(data["domain_label"])

    has_ellipse = ellipse.size == 4
    if has_ellipse:
        cx, cy, a, b = [float(v) for v in ellipse]

    n = pred_tl_all.shape[0]

    # 规则插值网格（与训练时一致）
    gx_lin = np.linspace(0, Lx_dom, grid_res)
    gy_lin = np.linspace(0, Ly_dom, grid_res)
    grid_x, grid_y = np.meshgrid(gx_lin, gy_lin)

    # 楔形域外遮罩：斜底 y = (Ly/Lx)*x，域外 (y > 斜底) 置 NaN
    if is_wedge:
        wedge_outside = grid_y > (Ly_dom / Lx_dom) * grid_x
    else:
        wedge_outside = np.zeros_like(grid_x, dtype=bool)

    fig, axes = plt.subplots(n, 3, figsize=(18, 5 * n))
    if n == 1:
        axes = axes.reshape(1, -1)

    extent = (0, Lx_dom, Ly_dom, 0)  # top=0 → 海面 y=0 在顶

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
                ax.plot([0, Lx_dom], [0, Ly_dom], "k-", linewidth=1.5)
                ax.plot([Lx_dom, Lx_dom], [0, Ly_dom], color="gray",
                        linewidth=1.0, linestyle="--")
            if has_ellipse:
                ax.add_patch(MplEllipse((cx, cy), width=2 * a, height=2 * b,
                                        fill=False, edgecolor="k",
                                        linewidth=1.5, linestyle="-"))
            ax.plot(source_pos[0], source_pos[1], "r*", markersize=10)
            ax.set_xlabel("X / Range (m)", fontsize=10)
            ax.set_ylabel("Y / Depth (m)", fontsize=10)
            ax.set_title(titles[j], fontsize=10, fontweight="bold")
            ax.set_xlim(0, Lx_dom)
            ax.set_ylim(Ly_dom, 0)
            cbar = plt.colorbar(im, ax=ax, fraction=0.035, pad=0.04, shrink=0.8)
            cbar.set_label("TL (dB)" if j < 2 else "Error (dB)", fontsize=9)
            for spine in ax.spines.values():
                spine.set_edgecolor("black")
                spine.set_linewidth(1.5)

    plt.suptitle(f"[{domain_label}] TL Field  Epoch {epoch}",
                 fontsize=12, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    if show:
        # 切到交互后端显示
        plt.show()
    else:
        if out_path is None:
            base = os.path.splitext(npz_path)[0]
            out_path = base + "_restored.pdf"
        plt.savefig(out_path, dpi=150, bbox_inches="tight")
        print(f"[OK] 已复现图像 → {out_path}")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(
        description="从训练保存的原始张量 (.npz) 复现 TL 对比图")
    ap.add_argument("npz", help="*_tl_raw_epoch*.npz 文件路径")
    ap.add_argument("-o", "--output", default=None,
                    help="输出图像路径（默认 <npz>_restored.pdf）")
    ap.add_argument("--method", default="cubic",
                    choices=["cubic", "linear", "nearest"],
                    help="griddata 插值方法（默认 cubic，与训练一致）")
    ap.add_argument("--grid", type=int, default=200,
                    help="插值网格分辨率（默认 200）")
    ap.add_argument("--show", action="store_true",
                    help="屏幕显示而非保存（需要图形界面）")
    args = ap.parse_args()

    if args.show:
        matplotlib.use("TkAgg", force=True)
        globals()["plt"] = __import__("matplotlib.pyplot",
                                      fromlist=["pyplot"])

    if not os.path.exists(args.npz):
        raise SystemExit(f"文件不存在: {args.npz}")

    restore_figure(args.npz, out_path=args.output, method=args.method,
                   grid_res=args.grid, show=args.show)


if __name__ == "__main__":
    main()
