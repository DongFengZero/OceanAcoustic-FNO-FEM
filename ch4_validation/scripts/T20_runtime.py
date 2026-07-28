#!/usr/bin/env python3
"""Table 20 — 运行时性能对比（Cases 43–44，4.8 节）

运行时表特殊：无训练日志、无频率维度，数据为测试集吞吐量。
每个 Case 4 行（COMSOL + 1/2/4 GPU），共 8 行。
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import paths, registry, report, texparse as T
import pandas as pd

SLUG = "T20_runtime"
r = registry.by_slug(SLUG)
LABEL, SEC = r["label"], r["sec"]
CASES = {43: "R1", 44: "W1"}

# 正文直接引用（4.8 节运行时性能段落）
PROSE = [
    ("Case 43 1 GPU Time", "17.08", (43, "1 GPU", "time")),
    ("Case 44 1 GPU Time", "14.04", (44, "1 GPU", "time")),
    ("Case 43 COMSOL Time", "873.10", (43, "COMSOL", "time")),
    ("Case 44 COMSOL Time", "503.00", (44, "COMSOL", "time")),
    ("Case 43 1 GPU Speed-up", "45.93", (43, "1 GPU", "speedup_calc")),
    ("Case 44 1 GPU Speed-up", "31.37", (44, "1 GPU", "speedup_calc")),
    ("Case 43 1 GPU Thr.", "52.82", (43, "1 GPU", "thr")),
    ("Case 43 2 GPU Thr.", "98.22", (43, "2 GPU", "thr")),
    ("Case 43 4 GPU Thr.", "163.78", (43, "4 GPU", "thr")),
    ("Case 43 4 GPU Speed-up", "142.42", (43, "4 GPU", "speedup_calc")),
    ("Case 44 4 GPU Speed-up", "106.42", (44, "4 GPU", "speedup_calc")),
]
METHODS = ["COMSOL", "1 GPU", "2 GPU", "4 GPU"]


def load_xlsx():
    """从 xlsx 加载运行时数据。返回 {case: {method: {time, thr, speedup}}}"""
    xl = paths.xlsx_path(SEC)
    df = pd.read_excel(xl, sheet_name=0, header=2)
    data = {}
    for _, row in df.iloc[1:].iterrows():  # 跳过第一行（列名）
        case = int(row.iloc[0])
        method_raw = str(row.iloc[4])
        time_ms = row.iloc[5]
        thr = row.iloc[6]
        speedup_raw = row.iloc[8]
        # 规范化 method
        if "COMSOL" in method_raw:
            method = "COMSOL"
        elif "1" in method_raw and "GPU" in method_raw:
            method = "1 GPU"
        elif "2" in method_raw:
            method = "2 GPU"
        elif "4" in method_raw:
            method = "4 GPU"
        else:
            continue
        # speedup 处理（可能是倍数或 "基准"）
        if isinstance(speedup_raw, str) or speedup_raw == 1:
            speedup = 1.0
        else:
            speedup = float(speedup_raw)
        if case not in data:
            data[case] = {}
        data[case][method] = {"time": float(time_ms), "thr": float(thr), "speedup": speedup}
    return data


def run():
    c = report.Checker(SLUG, r["desc"], "table", LABEL, r.get("number"))
    c.source("印刷面 tex", paths.TEX, f"Table {r.get('number')} 环境")
    c.source("xlsx 源", paths.xlsx_path(SEC), f"Cases {min(CASES)}–{max(CASES)} 运行时数据")

    xd = load_xlsx()

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源数据完整性")
    for no in CASES:
        c.check(no in xd, f"Case {no} 存在于 xlsx", "是" if no in xd else "缺失")
        for m in METHODS:
            ok = m in xd.get(no, {})
            c.check(ok, f"Case {no} {m} 数据存在", "是" if ok else "缺失")

    # ── B ────────────────────────────────────────────────────────
    c.section("2. tex 表格结构")
    env = T.table_env(LABEL)
    c.check(env and f"\\label{{{LABEL}}}" in env,
            "tex 表格环境可定位且确实包住 label", f"`{LABEL}`，长度 {len(env or '')}")
    rows = T.data_rows(env, ncol=5)
    raws = T.data_rows_raw(env, ncol=5)
    c.check(len(rows) == 8, "tex 数据行数 = 8", f"实得 {len(rows)}")

    # 解析 tex 行（每 4 行为一组）
    printed = {}
    for i, row in enumerate(rows):
        case_idx = i // 4
        method_idx = i % 4
        case = [43, 44][case_idx]
        method = METHODS[method_idx]
        if case not in printed:
            printed[case] = {}
        # 列：Case(multirow) + Method + Time + Thr. + Speed-up
        # multirow 第一行有 case 号，后续行为空
        time_str = row[2].strip()
        thr_str = row[3].strip()
        speedup_str = row[4].strip()
        printed[case][method] = {
            "time": time_str,
            "thr": thr_str,
            "speedup": speedup_str
        }

    # ── C ────────────────────────────────────────────────────────
    c.section("3. 印刷值比对（源值舍入到 2 位 vs tex）")
    c.note("运行时数据精度：Time(ms) 2 位、Thr.(samp/s) 2 位、Speed-up 2 位。")
    for no in CASES:
        for m in METHODS:
            src = xd[no][m]
            prn = printed[no][m]
            # Time
            c.eq(f"Case {no} {m} Time", src["time"], prn["time"], nd=2)
            # Throughput
            c.eq(f"Case {no} {m} Thr.", src["thr"], prn["thr"], nd=2)
            # Speed-up（特殊：COMSOL 为 "1$x$"，其他从 Thr. 现场计算）
            if m == "COMSOL":
                c.check(prn["speedup"] in ("1$\\times$", "1$x$"),
                        f"Case {no} {m} Speed-up = 1×",
                        f"印刷 `{prn['speedup']}`")
            else:
                # Speed-up = 本方法 Thr. / COMSOL Thr.
                comsol_thr = xd[no]["COMSOL"]["thr"]
                speedup_calc = src["thr"] / comsol_thr
                speedup_val = re.sub(r'\$.*?\$', '', prn["speedup"]).strip()
                c.eq(f"Case {no} {m} Speed-up", speedup_calc, speedup_val, nd=2)

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 正文引用精确性（4.8 节）")
    c.note("验证正文段落中引用的数值与表格/源数据一致。Speed-up 为派生计算。")
    for desc, quoted, coord in PROSE:
        case, method, field = coord
        if field == "speedup_calc":
            # 派生：Speed-up = 本方法 Thr. / COMSOL Thr.
            comsol_thr = xd[case]["COMSOL"]["thr"]
            speedup = xd[case][method]["thr"] / comsol_thr
            c.eq(desc, speedup, quoted, nd=2)
        else:
            # 直接值
            c.eq(desc, xd[case][method][field], quoted, nd=2)

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
