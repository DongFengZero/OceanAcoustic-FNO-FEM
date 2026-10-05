# -*- coding: utf-8 -*-
"""
fig13_perf.py
==============
生成论文 Fig. 13 (fig:perf, Cases 43-50) —— 推理性能三联图。

(a) 多 GPU 吞吐          Cases 43, 44   (cf. Table 13a)
(b) 相对 COMSOL 的加速比   Cases 43, 44   (cf. Table 13a)
(c) 单 DCU 逐样本时延      Cases 45-50   (cf. Table 13b)

本图绘制硬编码常量，须与 Table 13 同步；ch4_validation/scripts_figures/FIG23_perf.py
用 ast 解析这些常量并与 xlsx 比对，防止表更新而图未跟上。
build_perf.py 是另一个脚本 —— 它写运行时 xlsx，不画图。
Annotations are kept inside the axes frame.

输出：$CH4_TEXDIR/Figures/results/perf_merged.pdf
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _figpaths  # noqa: E402

# 本图以硬编码常量绘图（值须与 Tables 20/21 一致，由 FIG23_perf.py 断言）。
# 默认写论文 Figures/results，便于直接用重绘结果覆盖纸面图；设 CH4_FIGDIR
# 可改为写到本目录，仅做离线核对。
OUT = os.environ.get("CH4_FIGDIR", _figpaths.FIGDIR_PAPER)
plt.rcParams.update({
    "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8,
    "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "axes.grid": True, "grid.alpha": 0.3, "figure.dpi": 150,
})

# ---- data ----
gpus = [1, 2, 4]
thr = {"R1": [52.82, 98.22, 163.78], "W1": [62.42, 120.35, 211.77]}
spd = {"R1": [45.9, 85.4, 142.4],   "W1": [31.4, 60.5, 106.4]}
# single-DCU scaling (from tab:runtime-scale, authoritative)
nodes_R = [21737, 85353, 337351]; time_R = [47.53, 86.50, 251.39]
nodes_W = [10680, 41633, 165034]; time_W = [40.57, 58.04, 133.09]
edge = [128, 256, 512]

# long, wide, short strip
fig, ax = plt.subplots(1, 3, figsize=(9.6, 2.0))

# (a) throughput
x = range(len(gpus)); w = 0.36
b1 = ax[0].bar([i - w/2 for i in x], thr["R1"], w, label="R1 (rect.)", color="#3b6ea5")
b2 = ax[0].bar([i + w/2 for i in x], thr["W1"], w, label="W1 (wedge)", color="#c0603a")
ax[0].bar_label(b1, fmt="%.0f", fontsize=6, padding=1)
ax[0].bar_label(b2, fmt="%.0f", fontsize=6, padding=1)
ax[0].set_xticks(list(x)); ax[0].set_xticklabels([f"{g}" for g in gpus])
ax[0].set_xlabel("Number of A800 GPUs"); ax[0].set_ylabel("Throughput (samples/s)")
ax[0].set_title("(a) Multi-GPU inference throughput")
ax[0].set_ylim(0, max(thr["W1"]) * 1.28)
ax[0].legend(frameon=False, loc="upper left")

# (b) speed-up
ax[1].plot(gpus, spd["R1"], "o-", label="R1 (rect.)", color="#3b6ea5")
ax[1].plot(gpus, spd["W1"], "s-", label="W1 (wedge)", color="#c0603a")
for g, v in zip(gpus, spd["R1"]):
    ax[1].annotate(f"{v:.0f}$\\times$", (g, v), textcoords="offset points",
                   xytext=(0, 6), fontsize=6, color="#3b6ea5", ha="center")
for g, v in zip(gpus, spd["W1"]):
    ax[1].annotate(f"{v:.0f}$\\times$", (g, v), textcoords="offset points",
                   xytext=(0, -10), fontsize=6, color="#c0603a", ha="center")
ax[1].set_xticks(gpus)
ax[1].set_xlabel("Number of A800 GPUs"); ax[1].set_ylabel(r"Speed-up over COMSOL ($\times$)")
ax[1].set_title("(b) Throughput speed-up vs. COMSOL")
ax[1].set_ylim(0, max(spd["R1"]) * 1.28)
ax[1].legend(frameon=False, loc="upper left")

# (c) scaling (log-log): put markers, keep labels clear of the line
ax[2].plot(nodes_R, time_R, "o-", label="R1 (rect.)", color="#3b6ea5")
ax[2].plot(nodes_W, time_W, "s-", label="W1 (wedge)", color="#c0603a")
# rect labels above-left, wedge labels below-right, so neither sits on a line
for nx, ty, e in zip(nodes_R, time_R, edge):
    ax[2].annotate(f"{e} m", (nx, ty), textcoords="offset points",
                   xytext=(-2, 9), fontsize=6.5, color="#3b6ea5", ha="right")
for nx, ty, e in zip(nodes_W, time_W, edge):
    ax[2].annotate(f"{e} m", (nx, ty), textcoords="offset points",
                   xytext=(4, -11), fontsize=6.5, color="#c0603a", ha="left")
ax[2].set_xscale("log"); ax[2].set_yscale("log")
ax[2].set_xlabel("Mesh nodes"); ax[2].set_ylabel("Inference time (ms)")
ax[2].set_title("(c) Single-DCU scaling with domain size")
# generous padding so annotations never touch the frame or the line
ax[2].set_xlim(min(nodes_W) * 0.45, max(nodes_R) * 2.4)
ax[2].set_ylim(min(time_W) * 0.5, max(time_R) * 2.2)
ax[2].legend(frameon=False, loc="lower right")

fig.tight_layout(pad=0.5, w_pad=1.5)
out = f"{OUT}/perf_merged.pdf"
fig.savefig(out, bbox_inches="tight")
print("wrote", out)
