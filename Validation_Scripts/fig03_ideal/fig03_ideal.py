# -*- coding: utf-8 -*-
"""
fig03_ideal.py
==============
生成论文 Fig. 3 (fig:ideal, Cases 1-2 R0/W0) —— 解析解验证。

R1 审稿意见 3.4：原图坐标轴文字过小。本脚本在纸面尺寸(pt)画布上 1:1 出图，
字号即印刷字号（刻度 6 pt / 标签 6.5 pt）。数据、插值、选样本与
_ideal_core.py 完全相同（griddata cubic 220x220，每频率按 y=44.7 m 深度线
MAE 升序取两个样本），左样本的深度线 MAE 与 原 Table 5 逐位核对后才出图。

输出：out/case01_r0_grid2.pdf, out/case02_w0_grid2.pdf
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator

HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(HERE)
sys.path.insert(0, _PARENT)
import _figpaths  # noqa: E402

OUT = _figpaths.figdir(__file__)
sys.path.insert(0, HERE)
import _ideal_core as src  # noqa: E402  (load / grids / pick_two / Y_LINE)

# 表 5 (tab:ideal-depthline) 的值，用于逐位核对
TABLE5 = {"Case01_R0": {25: 0.151, 50: 0.130, 75: 0.341, 100: 0.430},
          "Case02_W0": {25: 0.114, 50: 0.069, 75: 0.449, 100: 1.235}}

# ---- 印刷字号 (pt)，与图 4-8 一致 ----
FS_HEAD = 7.0
FS_ROW = 6.5
FS_LABEL = 6.5
FS_TICK = 6.0
FS_NOTE = 6.0
STAR_MS = 4.5
LW = 0.6

# ---- 版式 (pt) ----
W_FIG = 491.5      # \textwidth 减 subfloat 内边距
L_MARGIN = 24.0    # 左侧 TL 轴标签 + 刻度
DL_FIELD = 26.0    # 深度线 -> 预测场 (场图 y 刻度 + Depth 标签)
PAIR_GAP = 2.0     # 预测场 -> 解析场
GRP_GAP = 24.0     # 样本 a -> 样本 b (样本 b 深度线 y 刻度)
R_MARGIN = 2.0
S = 53.0           # 场图边长
HEAD = 9.0
ROW_TITLE = 9.0
X_BAND = 17.0
CB_BAND = 24.0
TOP_PAD = 1.0
REF_C = "0.55"
SHADE_C = "0.85"   # 楔形区灰色, 与图 6/7 障碍物区相同
PRED_C = "#d62728"

plt.rcParams.update({
    "pdf.fonttype": 42,
    "font.size": FS_TICK,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2.0, "ytick.major.size": 2.0,
    "xtick.major.pad": 1.5, "ytick.major.pad": 1.5,
})

CASES = ["Case01_R0", "Case02_W0"]
FREQS = [25, 50, 75, 100]


def render(case, out_pdf):
    data = src.load(case)
    freqs_all = [int(round(f)) for f in data["freq"]]
    nunit = 2
    DL = (W_FIG - L_MARGIN - R_MARGIN - (nunit - 1) * GRP_GAP
          - nunit * (DL_FIELD + 2 * S + PAIR_GAP)) / nunit
    assert DL > 60, DL
    W = W_FIG
    nrow = len(FREQS)
    H = TOP_PAD + HEAD + nrow * (ROW_TITLE + S) + X_BAND + CB_BAND
    fig = plt.figure(figsize=(W / 72.0, H / 72.0))

    def box(x, y_top, bw, bh):
        return [x / W, 1 - (y_top + bh) / H, bw / W, bh / H]

    unit_w = DL + DL_FIELD + 2 * S + PAIR_GAP
    x_dl = [L_MARGIN + u * (unit_w + GRP_GAP) for u in range(nunit)]
    x_pr = [x + DL + DL_FIELD for x in x_dl]
    x_an = [x + S + PAIR_GAP for x in x_pr]

    y = TOP_PAD
    yc = 1 - (y + HEAD * 0.5) / H
    for u in range(nunit):
        for x, w, t in [(x_dl[u], DL, "Depth line, y = %.1f m" % src.Y_LINE),
                        (x_pr[u], S, "Proposed"), (x_an[u], S, "Analytical")]:
            fig.text((x + w / 2) / W, yc, t, ha="center", va="center",
                     fontsize=FS_HEAD, fontweight="bold")
    y += HEAD
    y_axes0 = y

    texts, all_axes, report = [], [], []
    im = None
    for ri, f in enumerate(FREQS):
        ids = src.pick_two(data, f)
        assert len(ids) == 2
        last = ri == nrow - 1
        yb = 1 - (y + ROW_TITLE - 1.8) / H
        y += ROW_TITLE
        for u, idx in enumerate(ids):
            assert freqs_all[idx] == f
            gx, gy, GX, GY, gp, gf, Lx, Ly, is_wedge, vmin, vmax = src.grids(data, idx)
            sp = data["source_pos"][idx]
            r = int(np.argmin(np.abs(gy - src.Y_LINE)))
            ref, prd = gf[r], gp[r]
            ok = np.isfinite(ref) & np.isfinite(prd)
            mae = float(np.mean(np.abs((prd - ref)[ok])))
            report.append((f, u, idx, mae))
            if u == 0:
                assert round(mae, 3) == TABLE5[case][f], (case, f, mae)
            texts.append(fig.text(x_dl[u] / W, yb, "%d Hz (%s), Src (%.1f, %.1f) m"
                                  % (f, "ab"[u], sp[0], sp[1]), ha="left",
                                  va="baseline", fontsize=FS_ROW,
                                  fontweight="bold"))
            texts.append(fig.text((x_an[u] + S) / W, yb, "line MAE %.3f dB" % mae,
                                  ha="right", va="baseline", fontsize=FS_NOTE))
            # depth line
            ax = fig.add_axes(box(x_dl[u], y, DL, S))
            vi = np.where(ok)[0]
            ax.plot(gx, np.where(ok, ref, np.nan), color=REF_C, lw=3.0,
                    alpha=0.55, solid_capstyle="round", zorder=2)
            ax.plot(gx, np.where(ok, prd, np.nan), color=PRED_C, lw=1.0, zorder=9)
            if is_wedge:
                # 与图 6/7 障碍物区一致: 深度线落在楔形(海底)内的区段用灰色标出
                x_w = float(gy[r]) * Lx / Ly
                ax.axvspan(0.0, x_w, color=SHADE_C, lw=0, zorder=0)
                ax.set_xlim(0.0, float(gx[vi[-1]]))
            else:
                ax.set_xlim(float(gx[vi[0]]), float(gx[vi[-1]]))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=4, prune="both", min_n_ticks=2))
            ax.set_xticks([0, 40, 80, 120])
            ax.grid(True, alpha=0.25, lw=0.4)
            ax.tick_params(labelsize=FS_TICK, labelbottom=last)
            all_axes.append(ax)
            # fields
            for x, arr in [(x_pr[u], gp), (x_an[u], gf)]:
                axf = fig.add_axes(box(x, y, S, S))
                im = axf.imshow(arr, extent=(0, Lx, Ly, 0), origin="upper",
                                cmap="jet", aspect="equal", vmin=vmin,
                                vmax=vmax, interpolation="nearest")
                if is_wedge:
                    axf.fill([0, 0, Lx], [0, Ly, Ly], color=SHADE_C, lw=0,
                             zorder=1.5)
                    axf.plot([0, Lx], [0, Ly], "k-", lw=LW)
                axf.plot([0, Lx], [gy[r], gy[r]], color="w", lw=0.6,
                         ls=(0, (2.5, 1.5)))
                axf.plot(sp[0], sp[1], "r*", ms=STAR_MS, mew=0.3, mec="darkred")
                axf.set_xlim(0, Lx); axf.set_ylim(Ly, 0)
                axf.set_xticks([0, 50, 100]); axf.set_yticks([0, 50, 100])
                axf.tick_params(labelsize=FS_TICK, labelbottom=last,
                                labelleft=(x == x_pr[u]))
                if x == x_pr[u]:
                    axf.set_ylabel("Depth (m)", fontsize=FS_LABEL, labelpad=1.0)
                all_axes.append(axf)
        y += S

    # 共享轴名
    ymid = 1 - (y_axes0 + y) / 2 / H
    fig.text(3.0 / W, ymid, "TL (dB)", rotation=90, ha="left", va="center",
             fontsize=FS_LABEL)
    for u in range(nunit):
        yl = 1 - (y + X_BAND - 3.0) / H
        fig.text((x_dl[u] + DL / 2) / W, yl, "Range x (m)", ha="center",
                 va="baseline", fontsize=FS_LABEL)
        fig.text((x_pr[u] + S + PAIR_GAP / 2) / W, yl, "Range x (m)",
                 ha="center", va="baseline", fontsize=FS_LABEL)
    y += X_BAND

    # 底部: 左 图例，右 色条
    yl = 1 - (y + 9.0) / H
    hand = [Line2D([0], [0], color=REF_C, lw=3.0, alpha=0.55,
                   solid_capstyle="round", label="Analytical"),
            Line2D([0], [0], color=PRED_C, lw=1.0, label="Proposed"),
            Line2D([0], [0], color="0.3", lw=0.6, ls=(0, (2.5, 1.5)),
                   label="Depth line (on fields)")]
    if is_wedge:
        hand.append(Patch(facecolor=SHADE_C, edgecolor="none",
                          label="Wedge region"))
    leg = fig.legend(handles=hand, loc="center left", ncol=len(hand), fontsize=FS_LABEL,
                     frameon=False, handlelength=2.2, columnspacing=1.2,
                     bbox_to_anchor=(x_dl[0] / W, yl))
    xa, xb = x_pr[1], x_an[1] + S
    cax = fig.add_axes(box(xa, y + 2.0, xb - xa, 3.5))
    cb = fig.colorbar(im, cax=cax, orientation="horizontal",
                      ticks=[-60, -40, -20, 0])
    cb.outline.set_linewidth(0.5)
    cb.ax.tick_params(labelsize=FS_TICK, length=1.5, pad=1.0, width=0.5)
    cb.set_label("TL (dB)", fontsize=FS_LABEL, labelpad=1.0)

    # 重叠检查: 文本之间、刻度标签之间、图例与色条
    fig.canvas.draw()
    rr = fig.canvas.get_renderer()
    texts += [a.yaxis.label for a in all_axes if a.yaxis.label.get_text()]
    bbs = [t.get_window_extent(rr) for t in texts]
    for i in range(len(bbs)):
        for j in range(i + 1, len(bbs)):
            assert not bbs[i].overlaps(bbs[j]), (texts[i].get_text(), texts[j].get_text())
    tk = []
    for ai, ax in enumerate(all_axes):
        tk += [(t.get_window_extent(rr), t.get_text(), ai) for t in ax.get_xticklabels() + ax.get_yticklabels()
               if t.get_visible() and t.get_text()]
    for i in range(len(tk)):
        for j in range(i + 1, len(tk)):
            assert not tk[i][0].overlaps(tk[j][0]), ("tick labels collide", tk[i][1:], tk[j][1:])
    assert not leg.get_window_extent(rr).overlaps(cb.ax.get_tightbbox(rr)), "legend/cbar"
    fig.savefig(out_pdf, dpi=300)
    plt.close(fig)
    return W, H, DL, report


def main():
    os.makedirs(OUT, exist_ok=True)
    for c in CASES:
        W, H, DL, rep = render(c, os.path.join(OUT, c.lower() + "_grid2.pdf"))
        print("[fig3] %s %.1f x %.1f pt, depth-line w %.1f pt" % (c, W, H, DL))
        print("   " + "  ".join("%dHz%s=%.3f" % (f, "ab"[u], m) for f, u, _, m in rep))
    print("ALL TABLE 5 VALUES MATCH ->", OUT)


if __name__ == "__main__":
    main()
