#!/usr/bin/env python3
"""table04_S1_ideal.py — 打印 Table 4（tab:ideal-overall）与 Table S1（tab:S1）

对象：4.2 节理想波导，R0 (Case 1) / W0 (Case 2)，与解析解对比。
  Table 4  场精度：逐频 Sol/TL + Avg.
  Table S1  深度线精度：单样本沿深度剖面的 MAE

取数层
  Table 4  归档汇总 xlsx（该 xlsx 可用 build_accuracy_xlsx.py 从训练日志重建，
           --check 已验证 420 项逐值一致）
  Table S1  源数据：从 ep200 的 .npz 现场重算

    python table04_S1_ideal.py [--tex]
"""
import _acctable as A
import _tblcommon as K

CASES = {1: "R0 (rect.)", 2: "W0 (wedge)"}


def table04():
    A.print_acc("tab:ideal-overall",
                "Cases 1-2 · 理想波导场精度（vs 解析解）", "4.2", CASES,
                ["Avg. 列 = 四频均值（caption 声明，verify.py 有断言）"])


def tableS1():
    import numpy as np
    K.head("tab:S1", "Supplementary Table S1 · Cases 1-2 · 深度线 TL-MAE 与源位（vs 解析解）")
    mod = K.checker_module("TS1_ideal_depthline")
    K.note("取数：复用 TS1_ideal_depthline.py 的 pick_sample()，即成图脚本 "
           "regen_ideal_panels.py 的同一提取算法")
    K.note(f"口径常量：GRID={mod.GRID}  METHOD={mod.METHOD}  "
           f"Y_LINE={mod.Y_LINE} m（每频率取该行 MAE 最小的样本）")
    w = [20, 26, 26, 26, 26]
    K.row(["Case / label"] + [f"{f}Hz  TL-MAE / Src(x,y)" for f in K.FREQS], w)
    K.rule(w)
    for no, (dsname, _) in mod.CASES.items():
        data = np.load(K.paths.npz_path(no), allow_pickle=True)
        cells = [f"{no}  {dsname}"]
        for f in K.FREQS:
            got = mod.pick_sample(data, f)
            if got is None:
                cells.append("—")
                continue
            idx, mae, (sx, sy), yv = got
            cells.append(f"{mae:.3f}  ({sx:.1f}, {sy:.1f})")
        K.row(cells, w)
    K.rule(w)
    K.note("TL-MAE 单位 dB（印刷 3 位）；Src 为该样本源位，印刷 1 位小数")
    if K.want_tex():
        print("\n  （Table S1 排在 OE_supplementary.tex 中，--tex 不在此处打印）")


if __name__ == "__main__":
    table04()
    tableS1()
    print()
