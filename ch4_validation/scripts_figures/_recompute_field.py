#!/usr/bin/env python3
"""
场图（Fig 5/6/7 等）的公共重算层。

复刻 regen_results_bigfont.py 的 render() 内层算法，逐样本重算：
  · Avg 误差（图上 "Error vs COMSOL | Avg:x.xx dB" 标注）
  · Src 坐标（图上 "Src:(x,y)" 标注）

口径与绘图脚本严格一致：griddata cubic / grid_res=200 /
椭圆与楔形域外置 NaN / clip 到 [vmin,vmax] / err=|pred-fem| / nanmean。
"""
import numpy as np
from scipy.interpolate import griddata

METHOD = "cubic"
GRID_RES = 200


def recompute(npz_path, method=METHOD, grid_res=GRID_RES):
    """返回 [(idx, freq, src_x, src_y, avg_err), ...]，逐样本。"""
    d = np.load(npz_path)
    pred_all = d["pred_tl"]
    fem_all = d["fem_tl"]
    xc = d["x_coords"]
    yc = d["y_coords"]
    src_all = d["source_pos"]
    freq_all = d["freq"]
    Lx = float(d["Lx_dom"])
    Ly = float(d["Ly_dom"])
    is_wedge = bool(d["is_wedge"])
    ellipse = d["ellipse"]
    vmin = float(d["vmin"])
    vmax = float(d["vmax"])

    has_ellipse = ellipse.size == 4
    if has_ellipse:
        cx, cy, a, b = [float(v) for v in ellipse]

    n = pred_all.shape[0]
    gx_lin = np.linspace(0, Lx, grid_res)
    gy_lin = np.linspace(0, Ly, grid_res)
    grid_x, grid_y = np.meshgrid(gx_lin, gy_lin)

    if is_wedge:
        wedge_outside = grid_y > (Ly / Lx) * grid_x
    else:
        wedge_outside = np.zeros_like(grid_x, dtype=bool)

    out = []
    for i in range(n):
        gp = griddata((xc, yc), pred_all[i], (grid_x, grid_y), method=method)
        gf = griddata((xc, yc), fem_all[i], (grid_x, grid_y), method=method)

        if has_ellipse:
            inside = ((grid_x - cx) / a) ** 2 + ((grid_y - cy) / b) ** 2 <= 1.0
            gp[inside] = np.nan
            gf[inside] = np.nan

        gp[wedge_outside] = np.nan
        gf[wedge_outside] = np.nan
        gp = np.clip(gp, vmin, vmax)
        gf = np.clip(gf, vmin, vmax)

        err = np.abs(gp - gf)
        avg_err = float(np.nanmean(err))

        out.append(dict(idx=i, freq=float(freq_all[i]),
                        src=(float(src_all[i][0]), float(src_all[i][1])),
                        avg_err=avg_err))
    return dict(epoch=int(d["epoch"]), n=n, samples=out)
