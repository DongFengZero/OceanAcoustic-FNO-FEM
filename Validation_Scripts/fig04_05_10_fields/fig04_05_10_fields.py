# -*- coding: utf-8 -*-
"""
compact_figs.py
===============
R1 审稿意见 3.4（坐标轴文字过小）——图 4 / 5 / 9 / 11 紧凑重排版。

与 regen_results_bigfont.py / regen_gen_extrap_bigfont.py 同一数据、同一插值
(griddata cubic, 200x200, 障碍/楔形遮罩, clip 到 [vmin, vmax])，同一样本，
只改排版：
  * 画布直接按纸面尺寸(pt)出图，tex 里以 scale=1 放置 → 字号即印刷字号；
  * 列名 Ours TL / COMSOL TL / Error 只在顶部写一次，每行一行小标题；
  * 坐标轴标签/刻度只保留最外侧（同一面板内各子图域尺寸相同）；
  * 色条合并为底部共享一条（所有子图 TL 色标均为 [-60, 0] dB，误差均为 [0, 10] dB）；
  * 去掉 "[Rectangle] TL Field Epoch 200" 大标题（轮次写在图题里）。

用法: python compact_figs.py            -> 输出到本目录 out/
"""
import os
import glob
import sys

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

# ---- 印刷字号 (pt)，画布 1:1 放置 ----
FS_HEAD = 7.0     # 列名
FS_ROW = 6.5      # 行小标题
FS_LABEL = 6.5    # 坐标轴标签 / 色条标签
FS_TICK = 6.0     # 刻度
STAR_MS = 5.0
LW = 0.6

# ---- 版式 (pt) ----
L_MARGIN = 25.0   # 左侧 y 刻度 + y 标签
R_MARGIN = 3.0
COL_GAP = 7.0
ROW_TITLE = 8.5   # 行小标题带
ROW_GAP = 1.5
HEAD = 9.0        # 列名带
X_BAND = 17.0     # 末行 x 刻度 + x 标签
CB_BAND = 25.0    # 底部共享色条带
TOP_PAD = 1.0

plt.rcParams.update({
    "pdf.fonttype": 42,
    "font.size": FS_TICK,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2.0, "ytick.major.size": 2.0,
    "xtick.major.pad": 1.5, "ytick.major.pad": 1.5,
})


def find_npz(prefix):
    return _figpaths.npz(prefix)


def fields(data, i, grid_res=200, method="cubic"):
    """与原脚本完全一致的插值 + 遮罩 + clip。"""
    xc, yc = data["x_coords"], data["y_coords"]
    Lx, Ly = float(data["Lx_dom"]), float(data["Ly_dom"])
    vmin, vmax = float(data["vmin"]), float(data["vmax"])
    GX, GY = np.meshgrid(np.linspace(0, Lx, grid_res),
                         np.linspace(0, Ly, grid_res))
    gp = griddata((xc, yc), data["pred_tl"][i], (GX, GY), method=method)
    gf = griddata((xc, yc), data["fem_tl"][i], (GX, GY), method=method)
    ell = data["ellipse"]
    if ell.size == 4:
        cx, cy, a, b = [float(v) for v in ell]
        inside = ((GX - cx) / a) ** 2 + ((GY - cy) / b) ** 2 <= 1.0
        gp[inside] = np.nan
        gf[inside] = np.nan
    if bool(data["is_wedge"]):
        outside = GY > (Ly / Lx) * GX
        gp[outside] = np.nan
        gf[outside] = np.nan
    gp = np.clip(gp, vmin, vmax)
    gf = np.clip(gf, vmin, vmax)
    err = np.abs(gp - gf)
    avg = float(np.nanmean(err))
    err_vmax = min(float(np.nanmax(err)) if np.any(np.isfinite(err)) else 10.0,
                   10.0)
    return gp, gf, err, avg, err_vmax


def ticks_for(L):
    step = {128: 50, 256: 100, 512: 200}.get(int(round(L)), L / 2)
    return np.arange(0, L + 1e-6, step)


def make_panel(rows, w, out_pdf, head=True, xlabel=True, cbar=True,
               width=None):
    """rows: [(data, idx, left_title), ...]，一行 = Ours | COMSOL | Error。
    w: 子图边长(pt)。width: 画布宽(pt)，None 则按内容紧凑。返回画布尺寸。"""
    n = len(rows)
    W_need = L_MARGIN + 3 * w + 2 * COL_GAP + R_MARGIN
    W = max(W_need, width or 0)
    x0 = L_MARGIN + (W - W_need) / 2.0          # 内容水平居中
    H = (TOP_PAD + (HEAD if head else 0) + n * (ROW_TITLE + w + ROW_GAP)
         - ROW_GAP + (X_BAND if xlabel else 10.0) + (CB_BAND if cbar else 0))
    fig = plt.figure(figsize=(W / 72.0, H / 72.0))

    def box(x, y_top, bw, bh):                  # pt(左上原点) -> figure 分数
        return [x / W, 1 - (y_top + bh) / H, bw / W, bh / H]

    cols_x = [x0 + j * (w + COL_GAP) for j in range(3)]
    y = TOP_PAD
    if head:
        for j, name in enumerate(["Ours TL", "COMSOL TL", "Error"]):
            fig.text((cols_x[j] + w / 2) / W, 1 - (y + HEAD * 0.55) / H, name,
                     ha="center", va="center", fontsize=FS_HEAD,
                     fontweight="bold")
        y += HEAD

    ims = None
    for r, (data, idx, left) in enumerate(rows):
        gp, gf, err, avg, err_vmax = fields(data, idx)
        if abs(err_vmax - 10.0) > 1e-9:
            print("  [WARN] err_vmax=%.2f (shared colorbar assumes 10)" % err_vmax)
        Lx, Ly = float(data["Lx_dom"]), float(data["Ly_dom"])
        vmin, vmax = float(data["vmin"]), float(data["vmax"])
        src = data["source_pos"][idx]
        is_wedge = bool(data["is_wedge"])
        ell = data["ellipse"]
        # 行小标题: 左 = 频率/声源, 右(误差列上方) = 平均误差
        ty = 1 - (y + ROW_TITLE - 2.0) / H
        fig.text(cols_x[0] / W, ty, left, ha="left", va="baseline",
                 fontsize=FS_ROW)
        fig.text((cols_x[2] + w) / W, ty, "Avg %.2f dB" % avg, ha="right",
                 va="baseline", fontsize=FS_ROW)
        y += ROW_TITLE
        last = r == n - 1
        cur = []
        for j, (arr, cmap, lo, hi) in enumerate([
                (gp, "jet", vmin, vmax), (gf, "jet", vmin, vmax),
                (err, "Reds", 0, 10.0)]):
            ax = fig.add_axes(box(cols_x[j], y, w, w))
            im = ax.imshow(arr, extent=(0, Lx, Ly, 0), origin="upper",
                           cmap=cmap, aspect="equal", vmin=lo, vmax=hi,
                           interpolation="nearest")
            cur.append(im)
            if is_wedge:
                ax.plot([0, Lx], [0, Ly], "k-", linewidth=LW)
                ax.plot([Lx, Lx], [0, Ly], color="gray", linewidth=0.5,
                        linestyle="--")
            if ell.size == 4:
                cx, cy, a, b = [float(v) for v in ell]
                ax.add_patch(MplEllipse((cx, cy), width=2 * a, height=2 * b,
                                        fill=False, edgecolor="k",
                                        linewidth=LW))
            ax.plot(src[0], src[1], "r*", markersize=STAR_MS,
                    markeredgewidth=0.3, markeredgecolor="darkred")
            ax.set_xlim(0, Lx)
            ax.set_ylim(Ly, 0)
            ax.set_xticks(ticks_for(Lx))
            ax.set_yticks(ticks_for(Ly))
            ax.tick_params(labelsize=FS_TICK, labelbottom=last,
                           labelleft=(j == 0))
            if last and xlabel:
                ax.set_xlabel("X / Range (m)", fontsize=FS_LABEL, labelpad=1.5)
            if j == 0:
                ax.set_ylabel("Y / Depth (m)", fontsize=FS_LABEL, labelpad=1.5)
        ims = cur
        y += w + (0 if last else ROW_GAP)

    y += X_BAND if xlabel else 10.0
    if cbar:
        bh = 3.5
        for (xa, xb, im, lbl, tk) in [
                (cols_x[0], cols_x[1] + w, ims[0], "TL (dB)",
                 [-60, -40, -20, 0]),
                (cols_x[2], cols_x[2] + w, ims[2], "Error (dB)", [0, 5, 10])]:
            cax = fig.add_axes(box(xa, y + 2.0, xb - xa, bh))
            cb = fig.colorbar(im, cax=cax, orientation="horizontal", ticks=tk)
            cb.outline.set_linewidth(0.5)
            cb.ax.tick_params(labelsize=FS_TICK, length=1.5, pad=1.0,
                              width=0.5)
            cb.set_label(lbl, fontsize=FS_LABEL, labelpad=1.0)
            # 两条色条相邻端的 0 往内收，避免挤在一起
            tl = cb.ax.get_xticklabels()
            if tk[-1] == 0:
                tl[-1].set_ha("right")
            else:
                tl[0].set_ha("left")
    fig.savefig(out_pdf, dpi=300)
    plt.close(fig)
    return W, H


def rows_multi(prefix, tags=False):
    """图4 / 图11: 每频率前 2 个样本 (与原图同一选样)。"""
    data = np.load(find_npz(prefix), allow_pickle=True)
    freqs = [int(round(f)) for f in data["freq"]]
    rows = []
    for f in [25, 50, 75, 100]:
        ids = [i for i in range(len(freqs)) if freqs[i] == f][:2]
        for k, i in enumerate(ids):
            s = data["source_pos"][i]
            tag = " (%s)" % "ab"[k] if tags else ""
            rows.append((data, i, "f = %d Hz%s,  Src (%.1f, %.1f)"
                         % (f, tag, s[0], s[1])))
    return rows


def rows_single(prefix):
    """图5 / 图9: 每个 case 两个 100 Hz 样本。"""
    data = np.load(find_npz(prefix), allow_pickle=True)
    rows = []
    for i in range(data["pred_tl"].shape[0]):
        s = data["source_pos"][i]
        rows.append((data, i, "f = %d Hz,  Src (%.1f, %.1f)"
                     % (round(float(data["freq"][i])), s[0], s[1])))
    return rows


# 子图边长 (pt)，由版面预算确定 (textwidth 494.5pt, textheight 689.4pt)
W_TALL = 61.0     # 图4 / 图11: 8 行 x 2 面板并排，整页
W_STACK = 55.0    # 图5 / 图9: 3 面板竖排 x 2 列，与表格同页

FIG4 = [("Case03", "case03_r1_tl"), ("Case09", "case09_w1_tl")]
FIG11 = [("Case39", "gen_extrap_r9"), ("Case40", "gen_extrap_r10")]
FIG5 = [["Case06", "Case07", "Case08"], ["Case12", "Case13", "Case14"]]
FIG9 = [["Case33", "Case34", "Case35"], ["Case36", "Case37", "Case38"]]
NAMES = {"Case06": "case06_r4_tl", "Case07": "case07_r5_tl",
         "Case08": "case08_r6_tl", "Case12": "case12_w4_tl",
         "Case13": "case13_w5_tl", "Case14": "case14_w6_tl",
         "Case33": "case33_r4_tl", "Case34": "case34_r7_tl",
         "Case35": "case35_r8_tl", "Case36": "case36_w4_tl",
         "Case37": "case37_w7_tl", "Case38": "case38_w8_tl"}


def main():
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    for tag, spec, tags in [("fig4", FIG4, False), ("fig11", FIG11, True)]:
        if only and tag not in only:
            continue
        for prefix, name in spec:
            W, H = make_panel(rows_multi(prefix, tags), W_TALL,
                              os.path.join(OUT, name + ".pdf"))
            print("[%s] %-16s %.1f x %.1f pt" % (tag, name, W, H))
    for tag, spec in [("fig5", FIG5), ("fig9", FIG9)]:
        if only and tag not in only:
            continue
        for col in spec:
            for k, prefix in enumerate(col):
                W, H = make_panel(rows_single(prefix), W_STACK,
                                  os.path.join(OUT, NAMES[prefix] + ".pdf"),
                                  head=(k == 0), xlabel=(k == len(col) - 1),
                                  cbar=(k == len(col) - 1))
                print("[%s] %-16s %.1f x %.1f pt" % (tag, NAMES[prefix], W, H))
    print("-> " + OUT)


if __name__ == "__main__":
    main()
