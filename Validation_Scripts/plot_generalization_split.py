# -*- coding: utf-8 -*-
"""plot_generalization_split.py
================================
Generate the train/test source-distribution figure for the generalization
experiments (Cases 39-42: R9, R10, W9, W10) of Sec. 4.7.

Layout: 2 rows x 8 columns (16 panels). The four cases are placed left to
right (R9, R10, W9, W10); each case occupies a 2x2 quadrant showing its four
excitation frequencies (25/50 Hz on the top sub-row, 75/100 Hz on the bottom).
In every panel each acoustic source is a dot coloured by split:
blue = training set, red = test set. The held-out extrapolation region is
shaded; the elliptical obstacle and (for wedges) the sloping bottom are drawn.

Data source: the per-case dataset manifests
  Dataset/<CASE>/**/comsol_batch_manifest_*.mat
(available on Baidu Netdisk, see the repository README). Set DATASET_ROOT
below to the local path of the downloaded ``Dataset`` folder.

Output: generalization_split.pdf
"""
import glob
import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")  # torch+mpl OpenMP guard
import h5py
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from matplotlib.lines import Line2D

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
DATASET_ROOT = os.environ.get(
    "DATASET_ROOT",
    r"D:\Data\Data_and_Code_Availability\Dataset")
# Raw_Experimental_Data holds each case's authoritative train_test_split.pth
RAW_ROOT = os.environ.get(
    "RAW_ROOT",
    r"D:\Data\Data_and_Code_Availability\Raw_Experimental_Data\4.7_Generalization")
OUT_PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "generalization_split.pdf")

# case -> (No., dataset subdir, raw-case dir, is_wedge)
CASES = [
    ("R9",  39, "R9",  "No39_R9",  False),
    ("R10", 40, "R10", "No40_R10", False),
    ("W9",  41, "W9",  "No41_W9",  True),
    ("W10", 42, "W10", "No42_W10", True),
]
FREQS = [25, 50, 75, 100]
# frequency -> position within the case's 2x2 quadrant (row, col)
QUAD = {25: (0, 0), 50: (0, 1), 75: (1, 0), 100: (1, 1)}
def _deref(h, ref):
    return np.array(h[ref]).ravel()


def load_case(subdir, raw_case):
    """Return source coords, geometry, and the *actual* train/test labels.

    Source coordinates come from the dataset manifest; the authoritative
    train/test membership comes from the experiment's ``train_test_split.pth``
    (split_mode ``source_region_coord_outmix``: all in-region sources plus a
    seeded ``out_train_ratio`` fraction of out-region sources are training).
    The manifest source order is aligned with the split indices.
    """
    import torch
    pat = os.path.join(DATASET_ROOT, subdir, "**",
                       "comsol_batch_manifest_*.mat")
    files = glob.glob(pat, recursive=True)
    if not files:
        raise FileNotFoundError(
            f"manifest not found under {os.path.join(DATASET_ROOT, subdir)}; "
            "set DATASET_ROOT to the downloaded Dataset folder.")
    with h5py.File(files[0], "r") as h:
        src = np.array(h["all_src_depth"])            # (2, N): x, y
        fidx = np.array(h["all_freq_indices"]).ravel()  # 0..3 per source
        Lx = float(np.array(h["Lx_m"]).ravel()[0])
        Ly = float(np.array(h["Ly_m"]).ravel()[0])
        tmx = float(np.array(h["train_max_x_m"]).ravel()[0])
        tmy = float(np.array(h["train_max_y_m"]).ravel()[0])
        ell = [float(np.array(h[k]).ravel()[0]) for k in
               ("ellipse_cx_m", "ellipse_cy_m", "ellipse_a_m", "ellipse_b_m")]

    split_pth = os.path.join(RAW_ROOT, raw_case, "training_run",
                             "train_test_split.pth")
    if not os.path.isfile(split_pth):
        raise FileNotFoundError(
            f"train_test_split.pth not found at {split_pth}; "
            "set RAW_ROOT to the downloaded Raw_Experimental_Data/4.7 folder.")
    d = torch.load(split_pth, map_location="cpu", weights_only=False)
    is_train = np.zeros(src.shape[1], dtype=bool)
    is_train[np.asarray(d["train_indices"], dtype=int)] = True
    return dict(x=src[0], y=src[1], fidx=fidx, is_train=is_train,
                Lx=Lx, Ly=Ly, train_max_x=tmx, train_max_y=tmy, ell=ell,
                out_train_ratio=float(d.get("out_train_ratio", 0.10)))


def draw_panel(ax, d, fi, is_wedge):
    """Scatter one frequency panel: blue=train, red=test."""
    sel = d["fidx"] == fi
    x, y, tr = d["x"][sel], d["y"][sel], d["is_train"][sel]
    Lx, Ly = d["Lx"], d["Ly"]
    tmx, tmy = d["train_max_x"], d["train_max_y"]

    # held-out extrapolation region (shaded): depth split -> y>tmy; range -> x>tmx
    if tmy < Ly - 1e-6:            # depth extrapolation (y > tmy)
        ax.add_patch(Rectangle((0, tmy), Lx, Ly - tmy,
                               facecolor="0.85", edgecolor="none", zorder=0))
    if tmx < Lx - 1e-6:            # range extrapolation (x > tmx)
        ax.add_patch(Rectangle((tmx, 0), Lx - tmx, Ly,
                               facecolor="0.85", edgecolor="none", zorder=0))

    ax.scatter(x[tr], y[tr], s=2.0, c="tab:blue", marker=".",
               linewidths=0, zorder=2)
    ax.scatter(x[~tr], y[~tr], s=2.0, c="tab:red", marker=".",
               linewidths=0, zorder=3)

    # obstacle ellipse
    cx, cy, a, b = d["ell"]
    ax.add_patch(Ellipse((cx, cy), 2 * a, 2 * b, facecolor="none",
                         edgecolor="k", lw=0.6, zorder=4))
    # wedge sloping bottom (y = Ly/Lx * x): mask below the slope
    if is_wedge:
        ax.plot([0, Lx], [0, Ly], "k-", lw=0.7, zorder=4)

    ax.set_xlim(0, Lx)
    ax.set_ylim(Ly, 0)                  # depth increases downward
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"{FREQS[fi]} Hz", fontsize=7, pad=1.5)


def main():
    fig = plt.figure(figsize=(13, 3.6))
    # outer grid: 2 rows x 8 cols; each case = a 2x2 block of columns [2c,2c+2)
    gs = fig.add_gridspec(2, 8, wspace=0.12, hspace=0.32,
                          left=0.03, right=0.995, top=0.80, bottom=0.08)
    for ci, (name, no, subdir, raw_case, is_wedge) in enumerate(CASES):
        d = load_case(subdir, raw_case)
        for fi in range(4):
            r, c = QUAD[FREQS[fi]]
            ax = fig.add_subplot(gs[r, 2 * ci + c])
            draw_panel(ax, d, fi, is_wedge)
            if r == 0 and c == 0:
                region = ("depth $y>%.0f$ m" % d["train_max_y"]
                          if d["train_max_y"] < d["Ly"] - 1e-6
                          else "range $x>%.0f$ m" % d["train_max_x"])
                ax.annotate(f"No.{no}  {name}\n({region})",
                            xy=(0.0, 1.0), xytext=(0, 20),
                            xycoords="axes fraction",
                            textcoords="offset points",
                            fontsize=8, fontweight="bold", ha="left")
    handles = [Line2D([0], [0], marker="o", color="w", label="Train",
                      markerfacecolor="tab:blue", markersize=6),
               Line2D([0], [0], marker="o", color="w", label="Test",
                      markerfacecolor="tab:red", markersize=6),
               Rectangle((0, 0), 1, 1, facecolor="0.85",
                         edgecolor="none", label="Extrapolation region")]
    fig.legend(handles=handles, loc="lower center", ncol=3,
               fontsize=9, frameon=False, bbox_to_anchor=(0.5, 0.0))
    fig.savefig(OUT_PDF, dpi=200, bbox_inches="tight")
    print("saved:", OUT_PDF)


if __name__ == "__main__":
    main()
