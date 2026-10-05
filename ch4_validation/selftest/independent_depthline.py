# -*- coding: utf-8 -*-
"""
Independent re-implementation of the depth-line TL-MAE (Tables 7 and 8).

Purpose: the verification suite computes these values by *importing the plotting
script's own functions* (common/depthline.py, fig03_ideal/_ideal_core.py). That
guarantees the same definition, but if those functions had a bug, the table, the
figure and the check would all agree on the wrong number. This file shares no code
with them: it parses the .tex itself, locates the npz files itself, identifies each
sample from the source position printed in the table header, and evaluates the
interpolant directly at the points of the depth line (CloughTocher2DInterpolator)
instead of interpolating a full grid and slicing a row.

Definition (from the paper and the generator constants, which are read from the
generator *source text* -- not imported -- and asserted equal):
  * TL from the finite element nodes is interpolated with a C1 Clough-Tocher
    (piecewise cubic) interpolant -- what scipy's griddata(method="cubic") uses;
  * the depth line is the grid row nearest the printed depth y on an
    n-point grid in [0, Ly]; it is sampled at n points in [0, Lx];
  * points outside the wedge and inside the obstacle (ellipse enlarged by
    a factor m) are excluded; both fields are clipped to [vmin, vmax];
  * MAE = mean |TL_pred - TL_ref| over the remaining points.
"""
import glob, io, os, re, sys
import numpy as np
from scipy.interpolate import CloughTocher2DInterpolator

TEX = os.path.join(os.environ.get("CH4_TEXDIR", r"D:\JASA\OE\OE_Revision_R1_Submission"), "OE_submission.tex")
RAW = os.path.join(os.environ.get("CH4_RAWROOT", r"D:\Data"), "Data_and_Code_Availability", "Raw_Experimental_Data")
GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Validation_Scripts")
B = chr(92)


def gen_const(path, name):
    m = re.search(r"^" + name + r"\s*=\s*([0-9.]+)", open(path, encoding="utf8").read(), re.M)
    return float(m.group(1))


def ell_margin(path):
    m = re.search(r"\(a \* ([0-9.]+)\)\) \*\* 2", open(path, encoding="utf8").read())
    return float(m.group(1)) if m else 1.0


DL_CORE = os.path.join(GEN, "fig06_07_dl", "_depthline_core.py")
ID_CORE = os.path.join(GEN, "fig03_ideal", "_ideal_core.py")
SUITE_DL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common", "depthline.py")
DEF = {
    "dl":    dict(n=300, margin=1.10, method="cubic"),
    "ideal": dict(n=220, margin=None, method="cubic"),
}
# 定义参数与成图脚本源码中的常量逐一对照（只读文本）
assert gen_const(DL_CORE, "GRID") == DEF["dl"]["n"]
assert gen_const(ID_CORE, "GRID") == DEF["ideal"]["n"]
assert ell_margin(SUITE_DL) == DEF["dl"]["margin"]
assert '"cubic"' in open(DL_CORE, encoding="utf8").read() and '"cubic"' in open(ID_CORE, encoding="utf8").read()


def find_npz(case_no):
    hits = glob.glob(os.path.join(RAW, "*", f"No{case_no:02d}_*", f"Case{case_no:02d}_*__TL*_ep200.npz"))
    assert len(hits) == 1, (case_no, hits)
    return hits[0]


def line_mae(d, s, y_print, n, margin):
    """沿 y≈y_print 的深度线逐点求值，返回 MAE（全精度）。"""
    xc, yc = d["x_coords"], d["y_coords"]
    Lx, Ly = float(d["Lx_dom"]), float(d["Ly_dom"])
    vmin, vmax = float(d["vmin"]), float(d["vmax"])
    gy = np.linspace(0, Ly, n)
    y0 = gy[int(np.argmin(np.abs(gy - y_print)))]
    x = np.linspace(0, Lx, n)
    pts = np.column_stack([x, np.full_like(x, y0)])
    ref = CloughTocher2DInterpolator(np.column_stack([xc, yc]), d["fem_tl"][s])(pts)
    pred = CloughTocher2DInterpolator(np.column_stack([xc, yc]), d["pred_tl"][s])(pts)
    keep = np.ones_like(x, dtype=bool)
    if bool(d["is_wedge"]):
        keep &= ~(y0 > (Ly / Lx) * x)
    if margin is not None and d["ellipse"].size == 4:
        cx, cy, a, b = [float(v) for v in d["ellipse"]]
        keep &= ((x - cx) / (a * margin)) ** 2 + ((y0 - cy) / (b * margin)) ** 2 > 1.0
    ref, pred = np.clip(ref, vmin, vmax), np.clip(pred, vmin, vmax)
    ok = keep & np.isfinite(ref) & np.isfinite(pred)
    return float(np.mean(np.abs(pred[ok] - ref[ok]))), y0


def sample_of(d, freq, src):
    """按表头印出的声源坐标 (1 位小数) 在该频率的样本中唯一定位。"""
    fr = [int(round(f)) for f in d["freq"]]
    hits = [i for i in range(len(fr)) if fr[i] == freq
            and f"{d['source_pos'][i][0]:.1f}" == src[0] and f"{d['source_pos'][i][1]:.1f}" == src[1]]
    assert len(hits) == 1, (freq, src, hits)
    return hits[0]


tex = io.open(TEX, encoding="utf8").read()
total = bad = 0
FREQS = [25, 50, 75, 100]

# ── Tables 7 / 8 ───────────────────────────────────────────────
for label, rect_cases, wedge_cases in (("tab:dl-cmp", range(15, 20), range(20, 25)),
                                       ("tab:dl-abl", range(25, 29), range(29, 33))):
    i = tex.index(B + "label{" + label + "}")
    cap = tex[tex.rindex(B + "captionof{table}", 0, i):i]
    body = tex[i:tex.index(B + "bottomrule", i)]
    ys = re.findall(r"along \$y=([0-9.]+)\$", cap)
    srcs = re.findall(B + B + r"srcxy\{([0-9.]+)\}\{([0-9.]+)\}", body)
    rows = [r for r in body.split(B + "midrule")[1].split(B + B) if "&" in r]
    printed = [[re.sub(r"\\textbf\{([^}]*)\}", r"\1", c).strip() for c in r.split("&")[1:]] for r in rows]
    names = [r.split("&")[0].strip() for r in rows]
    for g, (cases, y) in enumerate(((rect_cases, ys[0]), (wedge_cases, ys[1]))):
        datas = [np.load(find_npz(c), allow_pickle=True) for c in cases]
        for k, f in enumerate(FREQS):
            src = srcs[4 * g + k]
            s = sample_of(datas[0], f, src)
            for m, d in enumerate(datas):
                v, y0 = line_mae(d, s, float(y), **{k2: DEF["dl"][k2] for k2 in ("n", "margin")})
                got, want = f"{v:.3f}", printed[m][4 * g + k]
                total += 1
                if got != want:
                    bad += 1
                    print(f"  MISMATCH {label} {names[m]:22s} {['R1','W1'][g]} {f:3d} Hz: indep {v:.6f} -> {got} / printed {want}")
    print(f"{label}: checked, running total {total} cells, {bad} mismatches "
          f"(depth lines y = {ys[0]}, {ys[1]} m)")

print(f"\nINDEPENDENT RECOMPUTE: {total} printed depth-line cells, {bad} mismatches")
