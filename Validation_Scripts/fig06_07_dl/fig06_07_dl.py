# -*- coding: utf-8 -*-
"""
fig06_07_dl.py
===============
生成论文 Fig. 6 (fig:dl-cmp) 与 Fig. 7 (fig:dl-abl) —— 深度线 TL 折线图。

R1 审稿意见 3.4（坐标轴文字过小 / 比较过多）。数据、插值、选线、选样本与
_depthline_core.py（原 advantage_depth_line.py 的原样副本）完全一致
(griddata cubic 300x300、障碍物 1.10 倍遮罩、clip 到 [vmin, vmax]、force_y 锁线)，
MAE 表值逐位复核后才出图；只改排版：画布按纸面尺寸(pt)出图、去掉大标题、
图例移出子图改为整幅底部一条。

输出：out/comparison_{R1,W1}_model_advantage.pdf, out/ablation_{R1,W1}_module_advantage.pdf,
      out/dl_legend_cmp.pdf, out/dl_legend_abl.pdf
"""
import os
import sys
import json
import importlib.util

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import _figpaths  # noqa: E402

OUT = _figpaths.figdir(__file__)

# 深度线的取数/选线/选样本与 advantage_depth_line.py 逐行相同；这里直接
# 加载本目录下的 _depthline_core.py（那份脚本的原样副本），不复制算法。
_spec = importlib.util.spec_from_file_location(
    "rp", os.path.join(HERE, "_depthline_core.py"))
rp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rp)

# ---- 印刷字号 (pt)，与图 4/5/9/11 一致 ----
FS_TITLE = 6.5
FS_LABEL = 6.5
FS_TICK = 6.0
FS_LEG = 6.5

# ---- 版式 (pt) ----
FIG_W = 240.0      # = 0.49\linewidth 的 minipage
L_MARGIN = 26.0    # 左列 y 标签 + 刻度
COL_GAP = 15.0     # 右列自带 y 刻度(各频率 y 量程不同)
R_MARGIN = 2.0
TITLE_H = 8.0
TL_H = 35.0
GAP_TE = 2.5       # TL 与 |Err| 面板间距
ERR_H = 14.0
ROW_GAP = 4.0
X_BAND = 18.0      # 末行 x 刻度 + x 标签
TOP_PAD = 1.0

# 方法/变体名与表 8/9 统一
NAMES = {"Proposed (Ours)": "Proposed", "Full (Ours)": "Full model",
         "w/o prior": "w/o physics prior", "w/o graph": "w/o graph correction",
         "w/o prior-sup.": "w/o prior supervision"}
REF_C = "0.55"
SHADE_C = "0.85"

plt.rcParams.update({
    "pdf.fonttype": 42,
    "font.size": FS_TICK,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2.0, "ytick.major.size": 2.0,
    "xtick.major.pad": 1.5, "ytick.major.pad": 1.2,
})

def compute_group(cfg):
    """与 _repro.build_group 前半段逐行一致：只算选线 / 样本 / 网格，不画图。"""
    members = cfg["members"]
    datas = [np.load(rp._npz(cfg["grpdir"], c), allow_pickle=True)
             for c, _ in members]
    d0 = datas[0]
    Lx, Ly = float(d0["Lx_dom"]), float(d0["Ly_dom"])
    is_wedge = bool(d0["is_wedge"])
    vmin, vmax = float(d0["vmin"]), float(d0["vmax"])
    cx, cy, a, b = [float(v) for v in d0["ellipse"]]
    gx = np.linspace(0, Lx, rp.GRID)
    gy = np.linspace(0, Ly, rp.GRID)
    GX, GY = np.meshgrid(gx, gy)
    outside = GY > (Ly / Lx) * GX if is_wedge else np.zeros_like(GX, dtype=bool)
    inside_ell = ((GX - cx) / (a * 1.10)) ** 2 + ((GY - cy) / (b * 1.10)) ** 2 <= 1.0
    freq_arr = d0["freq"]
    geom = dict(GX=GX, GY=GY, gx=gx, gy=gy, outside=outside, inside_ell=inside_ell,
                Lx=Lx, Ly=Ly, cx=cx, cy=cy, a=a, b=b, vmin=vmin, vmax=vmax)
    freq_sids = {f: [i for i in range(len(freq_arr))
                     if int(round(freq_arr[i])) == f] for f in rp.FREQS}
    all_sids = sorted({s for v in freq_sids.values() for s in v})
    grids = {s: rp._grid_row_cache(datas, s, GX, GY, outside, inside_ell, vmin, vmax)
             for s in all_sids}
    chosen = rp._find_common_line(grids, freq_sids, geom, force_y=cfg.get("force_y"))
    r = next(iter(chosen.values()))["r"]
    yv = float(gy[r])
    dy = (yv - cy) / b
    if abs(dy) <= 1:
        half = a * np.sqrt(1 - dy ** 2)
        x_shade = (cx - half, cx + half)
        pad = 2.0 + (gx[1] - gx[0]) * 2
        rim = (gx >= x_shade[0] - pad) & (gx <= x_shade[1] + pad)
    else:
        x_shade = None
        rim = np.zeros(rp.GRID, dtype=bool)
    src_all = d0["source_pos"]
    for f in rp.FREQS:
        chosen[f]["freq"] = f
        chosen[f]["src"] = src_all[chosen[f]["s"]]
        chosen[f]["x_shade"] = x_shade
        gf = chosen[f]["gf"].copy()
        gf[chosen[f]["r"], rim] = np.nan
        chosen[f]["gf"] = gf
    return chosen, geom, yv


def _segments(mask):
    segs, s = [], None
    for i, mk in enumerate(mask):
        if mk and s is None:
            s = i
        elif not mk and s is not None:
            segs.append((s, i)); s = None
    if s is not None:
        segs.append((s, len(mask)))
    return segs


def mark_over(ax, gx, y, color, lo, hi, top_only=False):
    """越界区段：在对应边界画一条同色短虚线(与原图口径相同，仅线宽按纸面缩小)。"""
    y = np.asarray(y, float)
    fin = np.isfinite(y)
    masks = [(fin & (y > hi), hi)] + ([] if top_only else [(fin & (y < lo), lo)])
    for mask, bd in masks:
        for a, b in _segments(mask):
            ax.plot([gx[a], gx[b - 1]], [bd, bd], color=color, lw=1.1,
                    ls=(0, (2.5, 1.5)), solid_capstyle="butt", clip_on=False,
                    zorder=12)


def plot_cell(fig, box_tl, box_err, panel, members, geom, left, bottom):
    gx = geom["gx"]
    r = panel["r"]
    ref = rp.masked(panel["gf"][r])
    valid = np.isfinite(ref)
    vidx = np.where(valid)[0]
    x_lo, x_hi = float(gx[vidx[0]]), float(gx[vidx[-1]])
    rmin, rmax = float(np.nanmin(ref)), float(np.nanmax(ref))
    y_lo = max(geom["vmin"], rmin - 4.0)
    y_hi = min(geom["vmax"], rmax + 4.0)
    xs = panel["x_shade"]

    axT = fig.add_axes(box_tl)
    axE = fig.add_axes(box_err, sharex=axT)
    for ax in (axT, axE):
        if xs is not None:
            ax.axvspan(xs[0], xs[1], color=SHADE_C, lw=0, zorder=0)
        ax.grid(True, lw=0.3, alpha=0.35)

    axT.plot(gx, ref, color=REF_C, lw=3.0, alpha=0.55, solid_capstyle="round",
             zorder=2)
    for k in range(1, len(members)):
        c = rp.COLORS[members[k][1]]
        yl = np.where(valid, rp.masked(panel["gps"][k][r]), np.nan)
        axT.plot(gx, np.clip(yl, y_lo, y_hi), color=c, lw=0.75, ls=(0, (3, 1.5)),
                 alpha=0.75, zorder=4)
        mark_over(axT, gx, yl, c, y_lo, y_hi)
    c0 = rp.COLORS[members[0][1]]
    y0 = np.where(valid, rp.masked(panel["gps"][0][r]), np.nan)
    axT.plot(gx, np.clip(y0, y_lo, y_hi), color=c0, lw=1.2, zorder=9)
    mark_over(axT, gx, y0, c0, y_lo, y_hi)
    axT.set_xlim(x_lo, x_hi)
    axT.set_ylim(y_lo, y_hi)
    sx, sy = float(panel["src"][0]), float(panel["src"][1])
    axT.set_title("%d Hz,  Src (%.1f, %.1f) m" % (panel["freq"], sx, sy),
                  fontsize=FS_TITLE, pad=1.5)
    tk = matplotlib.ticker.MaxNLocator(4).tick_values(y_lo, y_hi)
    span = y_hi - y_lo
    axT.set_yticks([t for t in tk if y_lo + 0.18 * span <= t <= y_hi])
    axT.tick_params(labelsize=FS_TICK, labelbottom=False)

    for k in range(len(members)):
        c = rp.COLORS[members[k][1]]
        e = np.abs(np.where(valid, rp.masked(panel["gps"][k][r]), np.nan) - ref)
        ec = np.minimum(e, rp.ERR_HI)
        if k == 0:
            axE.plot(gx, ec, color=c, lw=1.0, zorder=9)
        else:
            axE.plot(gx, ec, color=c, lw=0.6, ls=(0, (3, 1.5)), alpha=0.75,
                     zorder=4)
        mark_over(axE, gx, e, c, 0.0, rp.ERR_HI, top_only=True)
    axE.set_ylim(0, rp.ERR_HI)
    axE.set_yticks([0, 10])
    axE.tick_params(labelsize=FS_TICK, labelbottom=bottom)
    axE.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(40))
    if bottom:
        axE.set_xlabel("Range $x$ (m)", fontsize=FS_LABEL, labelpad=1.0)
    if left:
        axT.set_ylabel("TL (dB)", fontsize=FS_LABEL, labelpad=1.5)
        axE.set_ylabel("|Err|", fontsize=FS_LABEL, labelpad=1.5)
    for ax in (axT, axE):
        for sp in ax.spines.values():
            sp.set_linewidth(0.5)


def fig_size():
    cell = TITLE_H + TL_H + GAP_TE + ERR_H
    return FIG_W, TOP_PAD + 2 * cell + ROW_GAP + X_BAND


def make_fig(chosen, members, geom, out_pdf):
    W, H = fig_size()
    fig = plt.figure(figsize=(W / 72.0, H / 72.0))
    pw = (W - L_MARGIN - COL_GAP - R_MARGIN) / 2.0

    def box(x, y_top, bw, bh):
        return [x / W, 1 - (y_top + bh) / H, bw / W, bh / H]

    for i, f in enumerate(rp.FREQS):
        rr, cc = divmod(i, 2)
        x = L_MARGIN + cc * (pw + COL_GAP)
        y = TOP_PAD + rr * (TITLE_H + TL_H + GAP_TE + ERR_H + ROW_GAP) + TITLE_H
        plot_cell(fig, box(x, y, pw, TL_H), box(x, y + TL_H + GAP_TE, pw, ERR_H),
                  chosen[f], members, geom, left=(cc == 0), bottom=(rr == 1))
    fig.savefig(out_pdf)
    plt.close(fig)
    return W, H


def make_legend(members, out_pdf, width, ncol=None):
    h = [Line2D([0], [0], color=REF_C, lw=3.0, alpha=0.55,
                solid_capstyle="round", label="COMSOL (reference)"),
         Line2D([0], [0], color=rp.COLORS[members[0][1]], lw=1.2,
                label=NAMES.get(members[0][1], members[0][1]))]
    for _, lbl in members[1:]:
        h.append(Line2D([0], [0], color=rp.COLORS[lbl], lw=0.75,
                        ls=(0, (3, 1.5)), label=NAMES.get(lbl, lbl)))
    h.append(Patch(facecolor=SHADE_C, edgecolor="none", label="Obstacle"))
    h.append(Line2D([0], [0], color="0.3", lw=1.1, ls=(0, (2.5, 1.5)),
                    label="Beyond axis range"))
    ncol = ncol or len(h)
    H = 11.0 * int(np.ceil(len(h) / ncol)) - (2.0 if len(h) > ncol else 0.0)
    fig = plt.figure(figsize=(width / 72.0, H / 72.0))
    fig.legend(handles=h, loc="center", ncol=ncol, fontsize=FS_LEG,
               frameon=False, handlelength=1.8, handletextpad=0.4,
               columnspacing=1.0, borderaxespad=0.0)
    fig.savefig(out_pdf)
    plt.close(fig)


# 论文表 8/9 现值 —— 出图前逐位核对，确保图与表出自同一选线/样本
TABLE = {
    "comparison_R1_model_advantage": [[0.469, 0.736, 0.582, 1.210, 1.697],
                                      [0.696, 3.570, 0.873, 2.477, 1.737],
                                      [0.579, 2.243, 0.916, 2.456, 1.840],
                                      [1.515, 5.479, 2.143, 2.965, 4.033]],
    "comparison_W1_model_advantage": [[0.195, 0.793, 0.446, 0.832, 0.762],
                                      [0.144, 1.982, 0.417, 0.826, 1.055],
                                      [0.576, 1.468, 1.281, 2.496, 2.836],
                                      [0.666, 7.038, 1.189, 4.315, 3.160]],
    "ablation_R1_module_advantage": [[1.092, 26.344, 0.968, 0.540],
                                     [0.533, 30.274, 0.547, 0.649],
                                     [1.547, 34.122, 2.903, 3.003],
                                     [3.174, 35.063, 5.008, 5.244]],
    "ablation_W1_module_advantage": [[0.545, 8.733, 1.440, 1.008],
                                     [0.205, 32.909, 0.306, 0.425],
                                     [1.417, 40.582, 2.289, 2.210],
                                     [4.094, 34.329, 4.623, 4.219]],
}


def main():
    os.makedirs(OUT, exist_ok=True)
    ok = True
    for gname, cfg in rp.GROUPS.items():
        chosen, geom, yv = compute_group(cfg)
        got = [[round(v, 3) for v in chosen[f]["er"]] for f in rp.FREQS]
        same = np.allclose(got, TABLE[gname], atol=5e-4)
        ok &= same
        src = ["(%.1f, %.1f)" % tuple(chosen[f]["src"][:2]) for f in rp.FREQS]
        print("[%s] y=%.2f  table-match=%s  src=%s" % (gname, yv, same, src))
        if not same:
            print("   got  ", got); print("   table", TABLE[gname])
        W, H = make_fig(chosen, cfg["members"], geom,
                        os.path.join(OUT, gname.lower() + ".pdf"))
        print("   %.1f x %.1f pt" % (W, H))
    make_legend(rp.GROUPS["comparison_R1_model_advantage"]["members"],
                os.path.join(OUT, "dl_legend_cmp.pdf"), 490.0)
    make_legend(rp.GROUPS["ablation_R1_module_advantage"]["members"],
                os.path.join(OUT, "dl_legend_abl.pdf"), 490.0, ncol=4)
    print("ALL TABLE VALUES MATCH" if ok else "!!! TABLE MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
