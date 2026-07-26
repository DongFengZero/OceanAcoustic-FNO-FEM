# -*- coding: utf-8 -*-
"""
paper_values.py
===============
Every printed value in the Chapter 4 tables of the paper, transcribed once and
kept data-only. The verifiers recompute the same quantities from raw data and
diff against these. Keeping the printed values here (rather than re-parsing the
LaTeX) makes the ground truth explicit and reviewable.

Units: Sol = field MSE in 1e-6; TL = TL-MAE in dB. `case_map` ties each No. to
its raw-data section/subdirectory so provenance is machine-checkable.
"""

# No. -> (section, case-subdir under Raw_Experimental_Data)
CASE_MAP = {
    1: ("4.2_Validation", "No01_R0"), 2: ("4.2_Validation", "No02_W0"),
    3: ("4.3_Forward", "No03_R1"), 4: ("4.3_Forward", "No04_R2"),
    5: ("4.3_Forward", "No05_R3"), 6: ("4.3_Forward", "No06_R4"),
    7: ("4.3_Forward", "No07_R5"), 8: ("4.3_Forward", "No08_R6"),
    9: ("4.3_Forward", "No09_W1"), 10: ("4.3_Forward", "No10_W2"),
    11: ("4.3_Forward", "No11_W3"), 12: ("4.3_Forward", "No12_W4"),
    13: ("4.3_Forward", "No13_W5"), 14: ("4.3_Forward", "No14_W6"),
    15: ("4.4_Comparison", "No15_R1_Proposed"), 16: ("4.4_Comparison", "No16_R1_DeepONet"),
    17: ("4.4_Comparison", "No17_R1_FNO"), 18: ("4.4_Comparison", "No18_R1_KNO"),
    19: ("4.4_Comparison", "No19_R1_CNO"), 20: ("4.4_Comparison", "No20_W1_Proposed"),
    21: ("4.4_Comparison", "No21_W1_DeepONet"), 22: ("4.4_Comparison", "No22_W1_FNO"),
    23: ("4.4_Comparison", "No23_W1_KNO"), 24: ("4.4_Comparison", "No24_W1_CNO"),
    25: ("4.5_Ablation", "No25_R1_Full"), 26: ("4.5_Ablation", "No26_R1_no_prior"),
    27: ("4.5_Ablation", "No27_R1_no_graph"), 28: ("4.5_Ablation", "No28_R1_no_prior_loss"),
    29: ("4.5_Ablation", "No29_W1_Full"), 30: ("4.5_Ablation", "No30_W1_no_prior"),
    31: ("4.5_Ablation", "No31_W1_no_graph"), 32: ("4.5_Ablation", "No32_W1_no_prior_loss"),
    33: ("4.6_Mesh", "No33_R4"), 34: ("4.6_Mesh", "No34_R7"), 35: ("4.6_Mesh", "No35_R8"),
    36: ("4.6_Mesh", "No36_W4"), 37: ("4.6_Mesh", "No37_W7"), 38: ("4.6_Mesh", "No38_W8"),
    39: ("4.7_Generalization", "No39_R9"), 40: ("4.7_Generalization", "No40_R10"),
    41: ("4.7_Generalization", "No41_W9"), 42: ("4.7_Generalization", "No42_W10"),
    43: ("4.8_Performance", "No43_R1"), 44: ("4.8_Performance", "No44_W1"),
    45: ("4.8_Performance", "No45_R4"), 46: ("4.8_Performance", "No46_R5"),
    47: ("4.8_Performance", "No47_R6"), 48: ("4.8_Performance", "No48_W4"),
    49: ("4.8_Performance", "No49_W5"), 50: ("4.8_Performance", "No50_W6"),
}

# ---- Per-(No,freq) accuracy tables: {No: {freq: (Sol, TL)}} --------------
# T4  ideal overall (No.1-2)
T4 = {
    1: {25: (2.94, 0.41), 50: (0.99, 0.13), 75: (2.92, 0.73), 100: (1.51, 0.77)},
    2: {25: (6.12, 0.36), 50: (0.46, 0.15), 75: (2.77, 0.59), 100: (4.18, 0.96)},
}
# T6 forward multi-freq (No.3-5, 9-11)
T6 = {
    3:  {25: (2.48, 0.70), 50: (0.27, 0.52), 75: (2.16, 1.09), 100: (1.85, 1.49)},
    4:  {25: (3.01, 0.79), 50: (1.10, 0.66), 75: (4.02, 1.42), 100: (6.98, 2.60)},
    5:  {25: (3.95, 0.88), 50: (6.62, 1.14), 75: (15.97, 2.57), 100: (26.11, 4.04)},
    9:  {25: (3.96, 0.71), 50: (0.27, 0.61), 75: (1.92, 1.01), 100: (2.34, 1.27)},
    10: {25: (2.15, 0.95), 50: (1.09, 0.73), 75: (5.12, 1.41), 100: (5.15, 1.63)},
    11: {25: (5.67, 2.00), 50: (5.15, 1.08), 75: (12.26, 1.77), 100: (20.12, 2.57)},
}
# T7/T8 forward 100Hz square (No.6-8, 12-14) — single freq
T78 = {
    6: (0.058, 0.44), 7: (1.23, 1.22), 8: (10.42, 3.85),
    12: (0.10, 0.61), 13: (1.23, 0.93), 14: (16.11, 3.41),
}
# T13/T14 comparison per-freq (No.15-24)
T1314 = {
    15: {25: (2.48, 0.70), 50: (0.27, 0.52), 75: (2.16, 1.09), 100: (1.85, 1.49)},
    16: {25: (32.02, 1.51), 50: (18.37, 1.87), 75: (53.55, 3.49), 100: (81.20, 7.07)},
    17: {25: (4.02, 0.83), 50: (0.44, 0.61), 75: (4.75, 1.53), 100: (5.71, 2.26)},
    18: {25: (37.51, 1.76), 50: (12.22, 1.91), 75: (29.49, 3.00), 100: (34.65, 4.28)},
    19: {25: (35.93, 1.83), 50: (4.91, 1.35), 75: (34.55, 2.87), 100: (32.66, 4.49)},
    20: {25: (3.96, 0.71), 50: (0.27, 0.61), 75: (1.92, 1.01), 100: (2.34, 1.27)},
    21: {25: (23.32, 1.30), 50: (12.68, 1.38), 75: (45.68, 2.81), 100: (127.98, 5.51)},
    22: {25: (5.42, 0.90), 50: (0.40, 0.67), 75: (2.33, 1.16), 100: (4.57, 1.64)},
    23: {25: (46.23, 1.35), 50: (5.18, 1.22), 75: (24.49, 2.33), 100: (28.63, 3.01)},
    24: {25: (57.72, 1.33), 50: (6.57, 1.21), 75: (53.37, 2.83), 100: (70.37, 4.12)},
}
# T15/T16 ablation per-freq (No.25-32)
T1516 = {
    25: {25: (16.64, 1.38), 50: (0.51, 0.60), 75: (10.13, 1.99), 100: (18.65, 3.67)},
    26: {25: (1563.1, 22.93), 50: (479.5, 32.72), 75: (424.6, 46.47), 100: (129.6, 53.08)},
    27: {25: (10.37, 1.09), 50: (0.58, 0.63), 75: (19.54, 2.56), 100: (22.92, 4.54)},
    28: {25: (3.19, 0.74), 50: (0.54, 0.63), 75: (19.97, 2.61), 100: (21.54, 4.31)},
    29: {25: (33.35, 1.29), 50: (0.70, 0.72), 75: (19.45, 2.14), 100: (33.08, 3.59)},
    30: {25: (9691, 9.45), 50: (1386, 55.80), 75: (685.3, 83.01), 100: (327.9, 46.94)},
    31: {25: (162.6, 2.04), 50: (1.31, 0.85), 75: (21.83, 2.34), 100: (55.65, 4.54)},
    32: {25: (57.36, 1.58), 50: (1.00, 0.75), 75: (32.38, 2.75), 100: (60.98, 5.05)},
}
# T17/T18 mesh independence (No.33-38) — single freq 100Hz
T1718 = {
    33: (0.058, 0.44), 34: (0.131, 0.38), 35: (0.287, 0.39),
    36: (0.100, 0.61), 37: (0.196, 0.36), 38: (0.326, 0.31),
}
# T19 generalization per-freq (No.39-42)
T19 = {
    39: {25: (56.0, 2.44), 50: (48.9, 3.35), 75: (95.5, 4.30), 100: (50.7, 4.48)},
    40: {25: (75.6, 2.03), 50: (35.2, 2.46), 75: (67.0, 3.63), 100: (29.2, 3.75)},
    41: {25: (686, 2.91), 50: (206, 3.83), 75: (214, 5.60), 100: (149, 5.05)},
    42: {25: (828, 4.22), 50: (179, 3.78), 75: (173, 4.74), 100: (122, 5.00)},
}

# ---- Depth-line MAE tables (selection pipeline) -------------------------
# T5 ideal depth-line, y=44.7, min-MAE sample per freq: {No:{freq:(MAE,src)}}
T5 = {
    1: {25: (0.15, (40, 36)), 50: (0.13, (49, 38)), 75: (0.34, (88, 108)), 100: (0.43, (23, 54))},
    2: {25: (0.11, (63, 14)), 50: (0.07, (83, 56)), 75: (0.45, (92, 53)), 100: (1.23, (121, 58))},
}
# T9-T12 comparison/ablation depth-line: {group: {freq: {method: MAE}}}
# groups map to advantage_depth_line.py GROUPS keys.
DEPTHLINE = {
    "comparison_R1_model_advantage": {
        "force_y": 56.1,
        25: {"Proposed (Ours)": 0.469, "DeepONet": 0.736, "FNO": 0.582, "KNO": 1.210, "CNO": 1.697},
        50: {"Proposed (Ours)": 0.696, "DeepONet": 3.570, "FNO": 0.873, "KNO": 2.477, "CNO": 1.737},
        75: {"Proposed (Ours)": 0.579, "DeepONet": 2.243, "FNO": 0.916, "KNO": 2.456, "CNO": 1.840},
        100: {"Proposed (Ours)": 1.515, "DeepONet": 5.479, "FNO": 2.143, "KNO": 2.965, "CNO": 4.033},
    },
    "comparison_W1_model_advantage": {
        "force_y": 30.4,
        25: {"Proposed (Ours)": 0.195, "DeepONet": 0.793, "FNO": 0.446, "KNO": 0.832, "CNO": 0.762},
        50: {"Proposed (Ours)": 0.144, "DeepONet": 1.982, "FNO": 0.417, "KNO": 0.826, "CNO": 1.055},
        75: {"Proposed (Ours)": 0.576, "DeepONet": 1.468, "FNO": 1.281, "KNO": 2.496, "CNO": 2.836},
        100: {"Proposed (Ours)": 0.666, "DeepONet": 7.038, "FNO": 1.189, "KNO": 4.315, "CNO": 3.160},
    },
    "ablation_R1_module_advantage": {
        "force_y": 71.9,
        25: {"Full (Ours)": 1.092, "w/o prior": 26.344, "w/o graph": 0.968, "w/o prior-sup.": 0.540},
        50: {"Full (Ours)": 0.533, "w/o prior": 30.274, "w/o graph": 0.547, "w/o prior-sup.": 0.649},
        75: {"Full (Ours)": 1.547, "w/o prior": 34.122, "w/o graph": 2.903, "w/o prior-sup.": 3.003},
        100: {"Full (Ours)": 3.174, "w/o prior": 35.063, "w/o graph": 5.008, "w/o prior-sup.": 5.244},
    },
    "ablation_W1_module_advantage": {
        "force_y": 33.4,
        25: {"Full (Ours)": 0.545, "w/o prior": 8.733, "w/o graph": 1.440, "w/o prior-sup.": 1.008},
        50: {"Full (Ours)": 0.205, "w/o prior": 32.909, "w/o graph": 0.306, "w/o prior-sup.": 0.425},
        75: {"Full (Ours)": 1.417, "w/o prior": 40.582, "w/o graph": 2.289, "w/o prior-sup.": 2.210},
        100: {"Full (Ours)": 4.094, "w/o prior": 34.329, "w/o graph": 4.623, "w/o prior-sup.": 4.219},
    },
}

# ---- Runtime tables -----------------------------------------------------
# T20 base-scale (No.43-44): {(case,method): (time_ms, thr, speedup)}
T20 = {
    (43, "COMSOL"): (873.1, 1.15, 1.0), (43, "1 GPU"): (17.08, 52.82, 45.9),
    (43, "2 GPU"): (17.64, 98.22, 85.4), (43, "4 GPU"): (18.28, 163.78, 142.4),
    (44, "COMSOL"): (503.0, 1.99, 1.0), (44, "1 GPU"): (14.04, 62.42, 31.4),
    (44, "2 GPU"): (14.15, 120.35, 60.5), (44, "4 GPU"): (14.74, 211.77, 106.4),
}
# T21 scale with domain size (No.45-50): {case: (Lx, N, time_ms)}
T21 = {
    45: (128, 21737, 47.02), 46: (256, 85353, 85.86), 47: (512, 337351, 249.53),
    48: (128, 10680, 40.10), 49: (256, 41633, 58.24), 50: (512, 165034, 132.41),
}
# Text-cited node counts (Sec 4.8) that must equal npz N and T21 N.
NODE_COUNTS = {6: 21737, 7: 85353, 8: 337351, 12: 10680, 13: 41633, 14: 165034}

# ---- Figures: label -> (kind, [case Nos it renders]) --------------------
# kind: "field" = TL prediction/reference/error grid from per-case npz;
#       "depthline" = advantage depth-line plot; "split" = source scatter.
FIGURES = {
    "fig:ideal-rect":      ("field", [1]),
    "fig:ideal-wedge":     ("field", [2]),
    "fig:res-128":         ("field", [3, 9]),
    "fig:res-256":         ("field", [4, 10]),
    "fig:res-512":         ("field", [5, 11]),
    "fig:res-rect-100":    ("field", [6, 7, 8]),
    "fig:res-wedge-100":   ("field", [12, 13, 14]),
    "fig:dl-cmp-rect":     ("depthline", ["comparison_R1_model_advantage"]),
    "fig:dl-cmp-wedge":    ("depthline", ["comparison_W1_model_advantage"]),
    "fig:dl-abl-rect":     ("depthline", ["ablation_R1_module_advantage"]),
    "fig:dl-abl-wedge":    ("depthline", ["ablation_W1_module_advantage"]),
    "fig:perf-rect":       ("field", [15, 16, 17, 18, 19]),
    "fig:perf-wedge":      ("field", [20, 21, 22, 23, 24]),
    "fig:abl-rect":        ("field", [25, 26, 27, 28]),
    "fig:abl-wedge":       ("field", [29, 30, 31, 32]),
    "fig:mesh-rect":       ("field", [33, 34, 35]),
    "fig:mesh-wedge":      ("field", [36, 37, 38]),
    "fig:gen-split":       ("split", [39, 40, 41, 42]),
    "fig:gen-grid":        ("field", [39, 40]),
    "fig:gen-grid-wedge":  ("field", [41, 42]),
    "fig:perf":            ("runtime", [43, 44, 45, 46, 47, 48, 49, 50]),
}
