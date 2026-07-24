#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scan_depth_lines.py
===================
为 advantage_depth_line.py 的四个展示案例扫描 "更好的公共深度线"。

目标(用户要求)：当前 force_y 下某些频率 Ours/Full 相对次优方法优势过小(甚至落后)，
例如 消融_W1@100Hz 仅 +0.014dB、对比_R1@25Hz 仅 +0.006dB、消融_R1@25Hz Full 落后。

本脚本复用 advantage_depth_line 的几何/网格构建，对每个组遍历所有满足约定的深度线，
按 "四频率中最差的那一频率的优势(worst-margin)" 排序，打印候选，便于人工挑选更稳的 y。

约定(见 memory tl-redraw-pipeline)：避开椭圆障碍 y 带外还要**穿过障碍**(force_y 语义),
避开海面退化行(floor=0.12*Ly)、有效点数足够。这里同时报告 require_cross=True/False 两档。
"""
import os
import numpy as np
import advantage_depth_line as A

FREQS = A.FREQS


def build_geom_grids(cfg):
    members = cfg["members"]
    datas = []
    for case, _ in members:
        p = A._npz(cfg["grpdir"], case)
        if p is None:
            print(f"[ERR] 缺失 {case} @ {cfg['grpdir']}")
            return None
        datas.append(np.load(p, allow_pickle=True))
    d0 = datas[0]
    Lx, Ly = float(d0["Lx_dom"]), float(d0["Ly_dom"])
    is_wedge = bool(d0["is_wedge"])
    vmin, vmax = float(d0["vmin"]), float(d0["vmax"])
    cx, cy, a, b = [float(v) for v in d0["ellipse"]]
    gx = np.linspace(0, Lx, A.GRID)
    gy = np.linspace(0, Ly, A.GRID)
    GX, GY = np.meshgrid(gx, gy)
    outside = GY > (Ly / Lx) * GX if is_wedge else np.zeros_like(GX, dtype=bool)
    inside_ell = ((GX - cx) / (a * 1.10)) ** 2 + ((GY - cy) / (b * 1.10)) ** 2 <= 1.0
    freq_arr = d0["freq"]
    geom = dict(gx=gx, gy=gy, Lx=Lx, Ly=Ly, cx=cx, cy=cy, a=a, b=b,
                vmin=vmin, vmax=vmax)
    freq_sids = {f: [i for i in range(len(freq_arr))
                     if int(round(freq_arr[i])) == f] for f in FREQS}
    all_sids = sorted({s for v in freq_sids.values() for s in v})
    grids = {s: A._grid_row_cache(datas, s, GX, GY, outside, inside_ell, vmin, vmax)
             for s in all_sids}
    return geom, grids, freq_sids


def scan(cfg, min_pts=80, require_cross=True):
    """返回每行的 (worst_margin, total_margin, y, per_freq[(margin, ours, second)])。"""
    geom, grids, freq_sids = build_geom_grids(cfg)
    gy, Ly = geom["gy"], geom["Ly"]
    cy, b = geom["cy"], geom["b"]
    rows = []
    for r in range(A.GRID):
        yv = gy[r]
        if yv < 0.12 * Ly or yv > 0.90 * Ly:
            continue
        if require_cross and not (cy - b <= yv <= cy + b):
            continue
        worst = 1e9
        total = 0.0
        per = {}
        ok_all = True
        for f in FREQS:
            sids = freq_sids.get(f, [])
            best = None  # 选让 Ours 优势最大的样本
            for s in sids:
                gf, gps = grids[s]
                npts, er = A._row_mae(gf, gps, r)
                if er is None or npts < min_pts:
                    continue
                second = min(er[1:])
                margin = second - er[0]  # >0 表示 Ours 胜
                if best is None or margin > best[0]:
                    best = (margin, er[0], second, npts)
            if best is None:
                ok_all = False
                break
            per[f] = best
            worst = min(worst, best[0])
            total += best[0]
        if not ok_all:
            continue
        wins = sum(1 for f in FREQS if per[f][0] > 0)
        rows.append((wins, worst, total, float(yv), per))
    # 先按获胜频率数(wins)排序，再按最差频率优势(worst)、总优势(total)
    rows.sort(key=lambda t: (t[0], t[1], t[2]), reverse=True)
    return rows


def report(group_name, cfg):
    print(f"\n{'='*78}\n### {group_name}  ({cfg['domain']})  force_y_now={cfg.get('force_y')}")
    for rc in (True, False):
        rows = scan(cfg, min_pts=80, require_cross=rc)
        tag = "穿障碍" if rc else "全域"
        if not rows:
            print(f"  [{tag}] 无候选")
            continue
        print(f"  [{tag}] top6 (按获胜频率数 wins → worst-margin 排序):")
        for wins, worst, total, yv, per in rows[:6]:
            detail = "  ".join(
                f"{f}Hz:+{per[f][0]:.3f}(O={per[f][1]:.2f})" for f in FREQS)
            print(f"    y={yv:6.2f}  wins={wins}/4  worst=+{worst:.3f}  "
                  f"sum=+{total:.3f} | {detail}")
    # 当前 force_y 处的表现
    fy = cfg.get("force_y")
    if fy is not None:
        rows = scan(cfg, min_pts=80, require_cross=False)
        near = min(rows, key=lambda t: abs(t[3] - fy)) if rows else None
        if near:
            wins, worst, total, yv, per = near
            detail = "  ".join(
                f"{f}Hz:+{per[f][0]:.3f}" for f in FREQS)
            print(f"  [当前 force_y≈{fy}] 实得 y={yv:.2f} wins={wins}/4 "
                  f"worst=+{worst:.3f} | {detail}")


if __name__ == "__main__":
    for gname, cfg in A.GROUPS.items():
        report(gname, cfg)
