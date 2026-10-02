#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fig12_gen_extrap.py
===================
生成论文 Fig. 12 (fig:gen-grid) 的楔形两幅 (Cases 41-42, W9/W10) —— 源位置外推场图。

注意：Fig. 12 的矩形两幅 (gen_extrap_R9/R10) 版式不同，由
fig04_05_10_fields.py 一并生成；本脚本负责楔形两幅。

4 行频率 (25/50/75/100 Hz) x 3 列 (Ours / COMSOL / Error)；每个频率的两个
候选样本中取网格平均误差与原图标题 'Avg X.XX dB' 最接近者，确保重绘的就是
原图那一个样本。渲染口径 (griddata cubic + 障碍/楔形遮罩 + clip) 与
fig04_05_10_fields.py 相同。

输出：$CH4_FIGDIR/gen_extrap_{W9,W10}.pdf
      默认写论文 Figures/results（就地覆盖，原图先备份到 _bak_gen_extrap_*）
"""
import os
import re
import sys
import shutil
import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse as MplEllipse
from scipy.interpolate import griddata
import fitz

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _figpaths  # noqa: E402

# 默认写论文 Figures/results（就地覆盖，原图先备份）；设 CH4_FIGDIR
# 可改为写到别处，便于离线核对而不动论文成图。
PAPER = os.environ.get("CH4_FIGDIR", _figpaths.FIGDIR_PAPER)
CASEDIR = os.environ.get("CH4_GENCASE",
                         os.path.join(_figpaths.RAWROOT, "Case39-42"))

# 与 33-38(regen_results_bigfont.py, 图18/19)完全同款渲染：字号/色条/标题/figsize
# 全部照搬。gen 每频率一行(共4行)，figsize=(18, 5*4)，每行尺寸=一条 mesh 行，
# tex 里同样用 width=\linewidth(不再限高) → 纸面字号与 33-38 自动一致。
FS_LABEL = 24
FS_TITLE = 26
FS_CBAR = 23
FS_TICK = 21
FS_SUPTITLE = 36
STAR_MS = 24

FREQS = [25, 50, 75, 100]

FIGS = {
    "gen_extrap_R9":  "Case39_R9",
    "gen_extrap_R10": "Case40_R10",
    "gen_extrap_W9":  "Case41_W9",
    "gen_extrap_W10": "Case42_W10",
}


def embedded_avgs(pdf_path):
    """从原 PDF 抽取每行 'Error | Avg X.XX dB' 的数值，按出现顺序(=25/50/75/100Hz)。"""
    d = fitz.open(pdf_path)
    t = d[0].get_text()
    d.close()
    return [float(x) for x in re.findall(r"Avg\s+([0-9.]+)\s*dB", t)]


def load_case(case):
    npz = os.path.join(CASEDIR, case, f"{case}__TL原始数据_ep200.npz")
    return np.load(npz, allow_pickle=True)


def grid_fields(data, i, grid_res=200, method="cubic"):
    """复算样本 i 的 pred/fem/err 网格与 avg err(与渲染完全一致)。"""
    xc, yc = data["x_coords"], data["y_coords"]
    Lx, Ly = float(data["Lx_dom"]), float(data["Ly_dom"])
    is_wedge = bool(data["is_wedge"])
    vmin, vmax = float(data["vmin"]), float(data["vmax"])
    ellipse = data["ellipse"]
    gx = np.linspace(0, Lx, grid_res)
    gy = np.linspace(0, Ly, grid_res)
    GX, GY = np.meshgrid(gx, gy)
    gp = griddata((xc, yc), data["pred_tl"][i], (GX, GY), method=method)
    gf = griddata((xc, yc), data["fem_tl"][i], (GX, GY), method=method)
    if ellipse.size == 4:
        cx, cy, a, b = [float(v) for v in ellipse]
        inside = ((GX - cx) / a) ** 2 + ((GY - cy) / b) ** 2 <= 1.0
        gp[inside] = np.nan
        gf[inside] = np.nan
    if is_wedge:
        outside = GY > (Ly / Lx) * GX
        gp[outside] = np.nan
        gf[outside] = np.nan
    gp = np.clip(gp, vmin, vmax)
    gf = np.clip(gf, vmin, vmax)
    err = np.abs(gp - gf)
    avg = float(np.nanmean(err))
    return gp, gf, err, avg, (Lx, Ly, is_wedge, vmin, vmax, ellipse)


def pick_rows(data, nsample=2):
    """每频率取前 nsample 个样本，返回 [(freq, idx, k), ...]。"""
    freqs = [int(round(f)) for f in data["freq"]]
    rows = []
    for f in FREQS:
        ids = [i for i in range(len(freqs)) if freqs[i] == f][:nsample]
        for k, idx in enumerate(ids):
            rows.append((f, idx, k))
    return rows


def render(figname, case, out_pdf):
    data = load_case(case)
    rows = pick_rows(data, nsample=2)
    domain_label = str(data["domain_label"])
    epoch = int(data["epoch"])

    n = len(rows)   # 8 = 4 频率 × 2 样本
    # 与 mesh(regen_results_bigfont)完全一致：每行 5in 高，figsize=(18, 5*n)
    fig, axes = plt.subplots(n, 3, figsize=(18, 5 * n))
    for r, (f, idx, k) in enumerate(rows):
        tag = chr(ord("a") + k)
        gp, gf, err, avg, geom = grid_fields(data, idx)
        Lx, Ly, is_wedge, vmin, vmax, ellipse = geom
        extent = (0, Lx, Ly, 0)
        src = data["source_pos"][idx]
        err_vmax = min(float(np.nanmax(err)) if np.any(np.isfinite(err)) else 10.0,
                       10.0)
        # 标题格式与 mesh 完全一致(加样本标签 a/b)
        titles = [
            f"Ours TL\n(f={f:.0f}Hz, {tag})\nSrc ({src[0]:.1f}, {src[1]:.1f})",
            f"COMSOL TL\n(f={f:.0f}Hz, {tag})",
            f"Error\n(Avg {avg:.2f} dB)",
        ]
        cols = [
            (gp, "jet", vmin, vmax, "TL (dB)"),
            (gf, "jet", vmin, vmax, "TL (dB)"),
            (err, "Reds", 0, err_vmax, "Error (dB)"),
        ]
        for c, (arr, cmap, vlo, vhi, clbl) in enumerate(cols):
            ax = axes[r, c]
            im = ax.imshow(arr, extent=extent, origin="upper", cmap=cmap,
                           aspect="equal", vmin=vlo, vmax=vhi)
            if is_wedge:
                ax.plot([0, Lx], [0, Ly], "k-", linewidth=1.8)
                ax.plot([Lx, Lx], [0, Ly], color="gray", linewidth=1.2,
                        linestyle="--")
            if ellipse.size == 4:
                cx, cy, a, b = [float(v) for v in ellipse]
                ax.add_patch(MplEllipse((cx, cy), width=2 * a, height=2 * b,
                                        fill=False, edgecolor="k",
                                        linewidth=1.8))
            ax.plot(src[0], src[1], "r*", markersize=STAR_MS)
            ax.set_xlabel("X / Range (m)", fontsize=FS_LABEL)
            ax.set_ylabel("Y / Depth (m)", fontsize=FS_LABEL)
            ax.set_title(titles[c], fontsize=FS_TITLE, fontweight="bold")
            ax.set_xlim(0, Lx)
            ax.set_ylim(Ly, 0)
            ax.tick_params(axis="both", labelsize=FS_TICK)
            # 色条与 mesh 完全一致
            cbar = plt.colorbar(im, ax=ax, fraction=0.035, pad=0.04, shrink=0.8)
            cbar.set_label(clbl, fontsize=FS_CBAR)
            cbar.ax.tick_params(labelsize=FS_TICK - 2)
            for sp in ax.spines.values():
                sp.set_edgecolor("black")
                sp.set_linewidth(1.5)

    plt.suptitle(f"[{domain_label}] TL Field  Epoch {epoch}",
                 fontsize=FS_SUPTITLE, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.98], w_pad=0.6, h_pad=1.8)
    plt.savefig(out_pdf, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return rows


def main():
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = os.path.join(PAPER, f"_bak_gen_extrap_{stamp}")
    os.makedirs(bak, exist_ok=True)
    for figname, case in FIGS.items():
        src_pdf = os.path.join(PAPER, figname + ".pdf")
        if os.path.exists(src_pdf):
            shutil.copy2(src_pdf, os.path.join(bak, figname + ".pdf"))
        rows = render(figname, case, src_pdf)
        print(f"[OK] {figname} <- {case}  ({len(rows)} rows = 4 freq x 2 samples)")
    print(f"\n[DONE] 原图备份 → {bak}")


if __name__ == "__main__":
    main()
