# -*- coding: utf-8 -*-
"""
data_sources.py
===============
Loaders that read the ARCHIVED RAW DATA (Baidu-hosted `Raw_Experimental_Data/`)
and expose it in a uniform form for the verifiers. Nothing here hard-codes a
printed paper value; every number returned is recomputed from the raw files.

Two kinds of raw source are handled:

1. Per-group summary spreadsheets  `Case*_数据汇总.xlsx`
     2-level header (rows 3-4); data from row 5. Each frequency block is
     4 columns wide: [损失(loss), MSE, "TL vs COMSOL", "Comsol vs sol"].
     Reliable reconstruction of the printed values:
         Sol_error(x1e-6) = (loss - comsol_vs_sol) * 1e4        (normal rows)
                          =  loss * 1e4                          (w/o prior-sup.)
         TL-MAE(dB)       = "TL vs COMSOL" column, verbatim
     (The MSE column is rounded to 1e-6 and is too coarse to trust; the loss
      column carries full precision, so we reconstruct Sol from it.)

2. Per-case field dumps  `Case*__TL原始数据_ep200.npz`
     keys: x_coords[N], y_coords[N], pred_tl[8,N], fem_tl[8,N],
           source_pos[8,2], freq[8], Lx_dom, Ly_dom, is_wedge, ellipse[4],
           vmin, vmax, epoch, domain_label
     8 = 4 frequencies x 2 plotted samples.

Set RAW_ROOT to the extracted `Raw_Experimental_Data/` directory (Baidu). By
default we look for it next to this package, then one level up.
"""
import os
import glob
import numpy as np

try:
    import pandas as pd
except Exception as e:  # pragma: no cover
    pd = None
    _PD_ERR = e

# --------------------------------------------------------------------------
# Locate the raw-data root
# --------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = [
    os.environ.get("RAW_ROOT", ""),
    os.path.join(_HERE, "Raw_Experimental_Data"),
    os.path.join(_HERE, "..", "Raw_Experimental_Data"),
    os.path.join(_HERE, "..", "..", "Data_and_Code_Availability",
                 "Raw_Experimental_Data"),
    r"D:\Data\Data_and_Code_Availability\Raw_Experimental_Data",
]


def raw_root():
    for c in _CANDIDATES:
        if c and os.path.isdir(c):
            return os.path.abspath(c)
    raise FileNotFoundError(
        "Raw_Experimental_Data not found. Download it from the Baidu link in "
        "README and set RAW_ROOT to its path. Tried:\n  " +
        "\n  ".join(repr(c) for c in _CANDIDATES if c))


# --------------------------------------------------------------------------
# Spreadsheet layout: per-group column bases for the four frequency blocks
# --------------------------------------------------------------------------
# base = column index of the freq block's `损失(loss)` cell; within the block
#   +0 loss, +1 MSE, +2 TL vs COMSOL, +3 Comsol vs sol.
FREQS = (25, 50, 75, 100)

SHEETS = {
    "forward":    dict(section="4.3_Forward",       file="Case3-14_数据汇总.xlsx",
                       bases={25: 11, 50: 15, 75: 19, 100: 23}, overall=7),
    "comparison": dict(section="4.4_Comparison",    file="Case15-24_数据汇总.xlsx",
                       bases={25: 12, 50: 16, 75: 20, 100: 24}, overall=8),
    "ablation":   dict(section="4.5_Ablation",      file="Case25-32_数据汇总.xlsx",
                       bases={25: 13, 50: 17, 75: 21, 100: 25}, overall=9),
    "mesh":       dict(section="4.6_Mesh",          file="Case33-38_数据汇总.xlsx",
                       bases={100: 11}, overall=7),
    "generalization": dict(section="4.7_Generalization", file="Case39-42_数据汇总.xlsx",
                       bases={25: 10, 50: 14, 75: 18, 100: 22}, overall=6),
    "validation": dict(section="4.2_Validation",    file="Case1-2_数据汇总.xlsx",
                       bases={25: 11, 50: 15, 75: 19, 100: 23}, overall=7),
}
# Rows whose loss column excludes the prior term (Sol = loss*1e4).
NO_PRIOR_LOSS_NOTE = "prior supervision"


def _as_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load_summary(group):
    """Return {No(int): {'dataset':str, 'note':str, freq(int): {'sol':x1e-6,'tl':dB}}}.

    Values are recomputed from the loss column, never read from a printed table.
    """
    if pd is None:
        raise RuntimeError("pandas is required: %r" % (_PD_ERR,))
    cfg = SHEETS[group]
    path = os.path.join(raw_root(), cfg["section"], cfg["file"])
    raw = pd.ExcelFile(path).parse(0, header=None)
    # Note column exists only in ablation sheet (col 6).
    note_col = 6 if group == "ablation" else None
    out = {}
    for r in range(5, raw.shape[0]):
        no = raw.iloc[r, 0]
        try:
            no = int(no)
        except (TypeError, ValueError):
            continue
        dataset = str(raw.iloc[r, 1]).strip()
        note = str(raw.iloc[r, note_col]).strip() if note_col is not None else ""
        no_prior = NO_PRIOR_LOSS_NOTE in note
        rec = {"dataset": dataset, "note": note}
        for f, base in cfg["bases"].items():
            loss = _as_float(raw.iloc[r, base])
            tl = _as_float(raw.iloc[r, base + 2])
            if loss is None or tl is None:
                continue
            if no_prior:
                sol = loss * 1e4
            else:
                cvs = _as_float(raw.iloc[r, base + 3]) or 0.0
                sol = (loss - cvs) * 1e4
            rec[f] = {"sol": sol, "tl": tl}
        out[no] = rec
    return out, os.path.relpath(path, raw_root())


# --------------------------------------------------------------------------
# Performance spreadsheet (two sheets)
# --------------------------------------------------------------------------
def load_perf():
    """Return (runtime_rows, scale_rows, relpath).

    runtime_rows: list of dict(case,dataset,geom,N,method,time_ms,thr,speedup)
    scale_rows:   list of dict(case,dataset,geom,Lx,Ly,N,time_ms,thr)
    """
    if pd is None:
        raise RuntimeError("pandas is required: %r" % (_PD_ERR,))
    path = os.path.join(raw_root(), "4.8_Performance",
                        "Case43-50_推理时间性能分析.xlsx")
    xl = pd.ExcelFile(path)
    s1 = xl.parse("COMSOL_vs_GPU加速", header=None)
    runtime = []
    for r in range(4, s1.shape[0]):
        case = _as_float(s1.iloc[r, 0])
        if case is None:
            continue
        runtime.append(dict(
            case=int(case), dataset=str(s1.iloc[r, 1]).strip(),
            geom=str(s1.iloc[r, 2]).strip(), N=_as_float(s1.iloc[r, 3]),
            method=str(s1.iloc[r, 4]).strip(), time_ms=_as_float(s1.iloc[r, 5]),
            thr=_as_float(s1.iloc[r, 6]), wallclock=_as_float(s1.iloc[r, 7]),
            speedup=_as_float(s1.iloc[r, 8])))
    s2 = xl.parse("域尺寸缩放推理", header=None)
    scale = []
    for r in range(4, s2.shape[0]):
        case = _as_float(s2.iloc[r, 0])
        if case is None:
            continue
        scale.append(dict(
            case=int(case), dataset=str(s2.iloc[r, 1]).strip(),
            geom=str(s2.iloc[r, 2]).strip(), Lx=_as_float(s2.iloc[r, 3]),
            Ly=_as_float(s2.iloc[r, 4]), N=_as_float(s2.iloc[r, 5]),
            time_ms=_as_float(s2.iloc[r, 6]), thr=_as_float(s2.iloc[r, 7])))
    return runtime, scale, os.path.relpath(path, raw_root())


# --------------------------------------------------------------------------
# NPZ field dumps
# --------------------------------------------------------------------------
def find_npz(section, case_dir):
    """Locate the `*__TL原始数据_ep200.npz` under a case directory."""
    d = os.path.join(raw_root(), section, case_dir)
    hits = glob.glob(os.path.join(d, "*TL原始数据*.npz"))
    return hits[0] if hits else None


def load_npz(section, case_dir):
    p = find_npz(section, case_dir)
    if p is None:
        return None, None
    return np.load(p, allow_pickle=True), os.path.relpath(p, raw_root())
