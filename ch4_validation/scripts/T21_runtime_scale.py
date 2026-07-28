#!/usr/bin/env python3
"""Table 21 — 域尺度增长性能（Cases 45–50，4.8 节）

单 DCU 测试，域尺度从 128m 到 512m，6 个 case（R4-6, W4-6）。
列：Case + Dataset + Lx(m) + N(节点数) + Time(ms)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import paths, registry, report, texparse as T
import pandas as pd

SLUG = "T21_runtime_scale"
r = registry.by_slug(SLUG)
LABEL, SEC = r["label"], r["sec"]
CASES = {45: "R4", 46: "R5", 47: "R6", 48: "W4", 49: "W5", 50: "W6"}

# 正文直接引用（4.8 节域尺度缩放段落）
PROSE = [
    ("Case 45 (R4) N", "21,737", (45, "n")),
    ("Case 47 (R6) N", "337,351", (47, "n")),
    ("Case 48 (W4) N", "10,680", (48, "n")),
    ("Case 50 (W6) N", "165,034", (50, "n")),
    ("Case 45 (R4) Time", "47.02", (45, "time")),
    ("Case 47 (R6) Time", "249.53", (47, "time")),
    ("Case 48 (W4) Time", "40.10", (48, "time")),
    ("Case 50 (W6) Time", "132.41", (50, "time")),
]


def load_xlsx():
    """从 xlsx 加载域尺度缩放数据。返回 {case: {dataset, lx, n, time}}"""
    xl = paths.xlsx_path(SEC)
    df = pd.read_excel(xl, sheet_name=1, header=2)
    data = {}
    for _, row in df.iloc[1:].iterrows():  # 跳过第一行（列名）
        case = int(row.iloc[0])
        dataset = str(row.iloc[1]).strip()
        lx = int(row.iloc[3])  # 第 4 列是 Lx
        n = int(row.iloc[5])   # 第 6 列是节点数
        time_ms = float(row.iloc[6])  # 第 7 列是时间
        data[case] = {"dataset": dataset, "lx": lx, "n": n, "time": time_ms}
    return data


def run():
    c = report.Checker(SLUG, r["desc"], "table", LABEL, r.get("number"))
    c.source("印刷面 tex", paths.TEX, f"Table {r.get('number')} 环境")
    c.source("xlsx 源", paths.xlsx_path(SEC), f"Cases {min(CASES)}–{max(CASES)} 域尺度缩放数据")

    xd = load_xlsx()

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源数据完整性")
    for no in CASES:
        c.check(no in xd, f"Case {no} 存在于 xlsx", "是" if no in xd else "缺失")

    # ── B ────────────────────────────────────────────────────────
    c.section("2. tex 表格结构")
    env = T.table_env(LABEL)
    c.check(env and f"\\label{{{LABEL}}}" in env,
            "tex 表格环境可定位且确实包住 label", f"`{LABEL}`，长度 {len(env or '')}")
    rows = T.data_rows(env, ncol=5)
    raws = T.data_rows_raw(env, ncol=5)
    c.check(len(rows) == 6, "tex 数据行数 = 6", f"实得 {len(rows)}")

    # 解析 tex 行
    printed = {}
    for row in rows:
        # 清理第一列的 \midrule 前缀
        cell0 = row[0]
        cell0 = cell0.replace('\\midrule', '').replace('\\toprule', '').replace('\\bottomrule', '')
        cell0 = cell0.strip()
        try:
            case = int(cell0)
        except ValueError:
            continue
        dataset = row[1].strip()
        lx = row[2].strip()
        n = row[3].strip()
        time_str = row[4].strip()
        printed[case] = {
            "dataset": dataset,
            "lx": lx,
            "n": n,
            "time": time_str
        }

    c.check(set(printed.keys()) == set(CASES.keys()), "tex 行 No. 覆盖 45-50",
            str(sorted(printed.keys())))

    # ── C ────────────────────────────────────────────────────────
    c.section("3. 印刷值比对（源值舍入到 2 位 vs tex）")
    c.note("列：Case, Dataset, Lx(m), N(节点数), Time(ms)。Time 精度 2 位。")
    for no in CASES:
        src = xd[no]
        prn = printed[no]
        # Dataset
        c.check(prn["dataset"] == CASES[no], f"Case {no} Dataset 名",
                f"tex `{prn['dataset']}`")
        # Lx (整数)
        c.check(prn["lx"] == str(src["lx"]), f"Case {no} Lx",
                f"源 {src['lx']} / 印刷 `{prn['lx']}`")
        # N (千位逗号格式，如 "21,737")
        n_formatted = f"{src['n']:,}"
        c.check(prn["n"].replace("{,}", ",") == n_formatted,
                f"Case {no} N",
                f"源 {src['n']} → `{n_formatted}` / 印刷 `{prn['n']}`")
        # Time (2 位小数)
        c.eq(f"Case {no} Time", src["time"], prn["time"], nd=2)

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 正文引用精确性（4.8 节）")
    c.note("验证正文段落中引用的数值与表格/源数据一致。")
    for desc, quoted, coord in PROSE:
        case, field = coord
        if field == "n":
            # N 是千位逗号格式
            n_formatted = f"{xd[case]['n']:,}"
            c.check(quoted == n_formatted, desc,
                    f"源 {xd[case]['n']} → `{n_formatted}` / 正文 `{quoted}`")
        else:
            # time 是浮点
            c.eq(desc, xd[case][field], quoted, nd=2)

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
