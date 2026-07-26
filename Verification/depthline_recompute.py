# -*- coding: utf-8 -*-
"""
depthline_recompute.py
======================
Re-run, from the raw npz field dumps, the exact depth-line selection that
`advantage_depth_line.py` uses to produce Tables T9-T12. This is deliberately a
faithful re-implementation of that script's selection math (cubic griddata onto
a 300x300 grid, wedge/ellipse masking, clip to [vmin,vmax], forced-y row, and
per-frequency best-"Full-advantage" sample by MAE) so the verifier reproduces
the printed MAE independently rather than trusting the cached json.

Also provides the ideal-geometry depth-line (T5) recompute: min-MAE sample per
frequency along a fixed y, matching regen_ideal_panels.py.
"""
import numpy as np
from scipy.interpolate import griddata

GRID = 300
METHOD = "cubic"
FREQS = (25, 50, 75, 100)

# Group -> ordered member case-dirs (raw-data subdir names) and labels.
GROUP_MEMBERS = {
    "comparison_R1_model_advantage": (
        "4.4_Comparison", 56.1,
        [("No15_R1_Proposed", "Proposed (Ours)"), ("No16_R1_DeepONet", "DeepONet"),
         ("No17_R1_FNO", "FNO"), ("No18_R1_KNO", "KNO"), ("No19_R1_CNO", "CNO")]),
    "comparison_W1_model_advantage": (
        "4.4_Comparison", 30.4,
        [("No20_W1_Proposed", "Proposed (Ours)"), ("No21_W1_DeepONet", "DeepONet"),
         ("No22_W1_FNO", "FNO"), ("No23_W1_KNO", "KNO"), ("No24_W1_CNO", "CNO")]),
    "ablation_R1_module_advantage": (
        "4.5_Ablation", 71.9,
        [("No25_R1_Full", "Full (Ours)"), ("No26_R1_no_prior", "w/o prior"),
         ("No27_R1_no_graph", "w/o graph"), ("No28_R1_no_prior_loss", "w/o prior-sup.")]),
    "ablation_W1_module_advantage": (
        "4.5_Ablation", 33.4,
        [("No29_W1_Full", "Full (Ours)"), ("No30_W1_no_prior", "w/o prior"),
         ("No31_W1_no_graph", "w/o graph"), ("No32_W1_no_prior_loss", "w/o prior-sup.")]),
}


def _grid_row_cache(datas, s, GX, GY, outside, inside_ell, vmin, vmax):
    d0 = datas[0]
    xc, yc = d0["x_coords"], d0["y_coords"]
    gf = griddata((xc, yc), d0["fem_tl"][s], (GX, GY), METHOD)
    gf[outside] = np.nan
    gf[inside_ell] = np.nan
    gf = np.clip(gf, vmin, vmax)
    gps = []
    for d in datas:
        gp = griddata((xc, yc), d["pred_tl"][s], (GX, GY), METHOD)
        gp[outside] = np.nan
        gp[inside_ell] = np.nan
        gp = np.clip(gp, vmin, vmax)
        gps.append(gp)
    return gf, gps


def _row_mae(gf, gps, r):
    fem = gf[r]
    ok = np.isfinite(fem)
    for gp in gps:
        ok &= np.isfinite(gp[r])
    npts = int(ok.sum())
    if npts == 0:
        return 0, None
    er = [float(np.mean(np.abs((gp[r] - fem)[ok]))) for gp in gps]
    return npts, er


def recompute_group(loader, group):
    """Return {freq: {label: MAE}} recomputed from raw npz for one depth-line group.

    loader: callable(section, case_dir) -> (npz, relpath) (data_sources.load_npz)
    """
    section, force_y, members = GROUP_MEMBERS[group]
    datas, sources = [], []
    for case_dir, _lbl in members:
        z, rel = loader(section, case_dir)
        if z is None:
            raise FileNotFoundError("missing npz for %s/%s" % (section, case_dir))
        datas.append(z)
        sources.append(rel)
    d0 = datas[0]
    Lx, Ly = float(d0["Lx_dom"]), float(d0["Ly_dom"])
    is_wedge = bool(d0["is_wedge"])
    vmin, vmax = float(d0["vmin"]), float(d0["vmax"])
    cx, cy, a, b = [float(v) for v in d0["ellipse"]]
    gx = np.linspace(0, Lx, GRID)
    gy = np.linspace(0, Ly, GRID)
    GX, GY = np.meshgrid(gx, gy)
    outside = GY > (Ly / Lx) * GX if is_wedge else np.zeros_like(GX, dtype=bool)
    inside_ell = ((GX - cx) / (a * 1.10)) ** 2 + ((GY - cy) / (b * 1.10)) ** 2 <= 1.0
    freq_arr = d0["freq"]
    freq_sids = {f: [i for i in range(len(freq_arr))
                     if int(round(float(freq_arr[i]))) == f] for f in FREQS}
    all_sids = sorted({s for v in freq_sids.values() for s in v})
    grids = {s: _grid_row_cache(datas, s, GX, GY, outside, inside_ell, vmin, vmax)
             for s in all_sids}
    r0 = int(np.argmin(np.abs(gy - force_y)))
    labels = [m[1] for m in members]
    out = {}
    for f in FREQS:
        best = None
        for min_pts in (120, 80, 50, 30, 20):
            for s in freq_sids[f]:
                gf, gps = grids[s]
                npts, er = _row_mae(gf, gps, r0)
                if er is None or npts < min_pts:
                    continue
                adv = min(er[1:]) - er[0]
                if best is None or adv > best[0]:
                    best = (adv, er)
            if best is not None:
                break
        if best is None:
            raise RuntimeError("no valid sample for %s %dHz" % (group, f))
        out[f] = {labels[k]: round(best[1][k], 3) for k in range(len(labels))}
    return out, float(gy[r0]), sources


def ideal_depthline(z, y_line=44.7):
    """T5 recompute: min-MAE plotted sample per frequency along fixed y (nearest
    grid row after cubic interpolation), matching the ideal-panel figures.
    Returns {freq: (MAE, (src_x, src_y))}."""
    Lx, Ly = float(z["Lx_dom"]), float(z["Ly_dom"])
    is_wedge = bool(z["is_wedge"])
    vmin, vmax = float(z["vmin"]), float(z["vmax"])
    gx = np.linspace(0, Lx, GRID)
    gy = np.linspace(0, Ly, GRID)
    GX, GY = np.meshgrid(gx, gy)
    outside = GY > (Ly / Lx) * GX if is_wedge else np.zeros_like(GX, dtype=bool)
    xc, yc = z["x_coords"], z["y_coords"]
    freq_arr = z["freq"]
    sp = z["source_pos"]
    r0 = int(np.argmin(np.abs(gy - y_line)))
    out = {}
    for f in FREQS:
        sids = [i for i in range(len(freq_arr))
                if int(round(float(freq_arr[i]))) == f]
        best = None
        for s in sids:
            gf = griddata((xc, yc), z["fem_tl"][s], (GX, GY), METHOD)
            gp = griddata((xc, yc), z["pred_tl"][s], (GX, GY), METHOD)
            gf[outside] = np.nan
            gp[outside] = np.nan
            gf = np.clip(gf, vmin, vmax)
            gp = np.clip(gp, vmin, vmax)
            fem = gf[r0]
            ok = np.isfinite(fem) & np.isfinite(gp[r0])
            if ok.sum() < 20:
                continue
            mae = float(np.mean(np.abs((gp[r0] - fem)[ok])))
            if best is None or mae < best[0]:
                best = (mae, (float(sp[s, 0]), float(sp[s, 1])))
        if best is not None:
            out[f] = (round(best[0], 2), best[1])
    return out, float(gy[r0])
