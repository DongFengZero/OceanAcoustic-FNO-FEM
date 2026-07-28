#!/usr/bin/env python3
"""Table 3 — Dataset 总览表（Cases 1–50，4.1 节）

从 Dataset 目录读取配置并验证 Table 3 的印刷值。
验证：Lx, Ly, Δ, N(节点数), Obstacle(椭圆参数)。
"""
import os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import paths, registry, report, texparse as T
import h5py

SLUG = "T03_datasets"
r = registry.by_slug(SLUG)
LABEL, SEC = r["label"], r["sec"]
DATASET_DIR = "D:/Data/Data_and_Code_Availability/Dataset"

# 从注册表和 tex 已知的 Dataset ID 映射
EXPECTED_DATASETS = {
    1: "R0", 2: "W0",
    3: "R1", 4: "R2", 5: "R3",
    6: "R4", 7: "R5", 8: "R6",
    9: "W1", 10: "W2", 11: "W3",
    12: "W4", 13: "W5", 14: "W6",
    15: "R1", 16: "R1", 17: "R1", 18: "R1", 19: "R1",  # baseline 复用
    20: "W1", 21: "W1", 22: "W1", 23: "W1", 24: "W1",
    25: "R1", 26: "R1", 27: "R1", 28: "R1",  # ablation 复用
    29: "W1", 30: "W1", 31: "W1", 32: "W1",
    33: "R4", 34: "R7", 35: "R8",  # mesh independence
    36: "W4", 37: "W7", 38: "W8",
    39: "R9", 40: "R10", 41: "W9", 42: "W10",  # generalization
    43: "R1", 44: "W1",  # runtime
    45: "R4", 46: "R5", 47: "R6",  # runtime scale
    48: "W4", 49: "W5", 50: "W6",
}

GEOM = {no: ("Rect." if ds.startswith("R") else "Wedge") for no, ds in EXPECTED_DATASETS.items()}


def load_dataset_config(dataset_id):
    """从 Dataset/{dataset_id}/ 目录读取配置。返回 {lx, ly, delta, n, obstacle}"""
    ds_path = os.path.join(DATASET_DIR, dataset_id)
    if not os.path.exists(ds_path):
        return None

    # 找子目录（只有一个）
    subdirs = [d for d in os.listdir(ds_path) if os.path.isdir(os.path.join(ds_path, d))]
    if len(subdirs) != 1:
        return None

    subdir = os.path.join(ds_path, subdirs[0])

    # 读取 mesh 文件
    mesh_files = glob.glob(os.path.join(subdir, "comsol_mesh_*.mat"))
    if not mesh_files:
        return None

    mesh_file = mesh_files[0]
    try:
        with h5py.File(mesh_file, 'r') as f:
            lx = float(f['Lx'][0, 0])
            ly = float(f['Ly'][0, 0])
            delta = float(f['H_grid'][0, 0])
            n = int(f['N_mesh'][0, 0])
    except Exception as e:
        return None

    # 读取 manifest 文件获取障碍物参数
    manifest_files = glob.glob(os.path.join(subdir, "comsol_batch_manifest_*.mat"))
    obstacle = None
    if manifest_files:
        try:
            with h5py.File(manifest_files[0], 'r') as f:
                use_ellipse = int(f['use_ellipse_m'][0, 0])
                if use_ellipse:
                    cx = float(f['ellipse_cx_m'][0, 0])
                    cy = float(f['ellipse_cy_m'][0, 0])
                    a = float(f['ellipse_a_m'][0, 0])
                    b = float(f['ellipse_b_m'][0, 0])
                    obstacle = (cx, cy, a, b)
        except:
            pass

    return {"lx": lx, "ly": ly, "delta": delta, "n": n, "obstacle": obstacle}


def run():
    c = report.Checker(SLUG, r["desc"], "table", LABEL, r.get("number"))
    c.source("印刷面 tex", paths.TEX, f"Table {r.get('number')} 环境")
    c.source("Dataset 目录", DATASET_DIR, "22 个数据集配置")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. tex 表格结构")
    env = T.table_env(LABEL)
    c.check(env and f"\\label{{{LABEL}}}" in env,
            "tex 表格环境可定位且确实包住 label", f"`{LABEL}`，长度 {len(env or '')}")
    rows = T.data_rows(env, ncol=13)
    c.check(len(rows) == 50, "tex 数据行数 = 50", f"实得 {len(rows)}")

    # 解析 tex 行
    printed = {}
    for row in rows:
        # 清理第一列的 \midrule 前缀
        cell0 = row[0].replace('\\midrule', '').replace('\\toprule', '').replace('\\bottomrule', '').strip()
        try:
            case = int(cell0)
        except ValueError:
            continue
        dataset = row[1].strip()
        geom = row[2].strip()
        lx = row[4].strip()
        ly = row[5].strip()
        delta = row[6].strip()
        obstacle = row[9].strip()
        printed[case] = {
            "dataset": dataset,
            "geom": geom,
            "lx": lx,
            "ly": ly,
            "delta": delta,
            "obstacle": obstacle
        }

    c.check(set(printed.keys()) == set(range(1, 51)), "tex 行 No. 覆盖 1-50",
            f"实得 {sorted(printed.keys())[:5]}...{sorted(printed.keys())[-5:]}")

    # ── B ────────────────────────────────────────────────────────
    c.section("2. Dataset ID 一致性")
    c.note("与 Dataset 目录中的 22 个数据集标签比对。")
    for no in range(1, 51):
        if no not in printed:
            c.check(False, f"Case {no} 缺失", "")
            continue
        c.check(printed[no]["dataset"] == EXPECTED_DATASETS[no],
                f"Case {no} Dataset ID",
                f"tex `{printed[no]['dataset']}` / 预期 `{EXPECTED_DATASETS[no]}`")

    # ── C ────────────────────────────────────────────────────────
    c.section("3. 几何类型一致性")
    c.note("Rect. / Wedge 与 Dataset ID 前缀（R/W）一致。")
    for no in range(1, 51):
        if no not in printed:
            continue
        c.check(printed[no]["geom"] == GEOM[no],
                f"Case {no} Geom.",
                f"tex `{printed[no]['geom']}` / 预期 `{GEOM[no]}`")

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 配置参数验证（Lx, Ly, Δ, Obstacle）")
    c.note("从 Dataset 目录读取 mesh 和 manifest 文件，验证印刷值。")

    # 只验证唯一的 22 个 dataset（跳过复用）
    unique_datasets = set(EXPECTED_DATASETS.values())
    dataset_configs = {}

    for ds_id in unique_datasets:
        cfg = load_dataset_config(ds_id)
        if cfg:
            dataset_configs[ds_id] = cfg

    c.note(f"成功加载 {len(dataset_configs)}/22 个数据集配置。")

    for no in range(1, 51):
        if no not in printed:
            continue
        ds_id = EXPECTED_DATASETS[no]
        if ds_id not in dataset_configs:
            c.check(False, f"Case {no} ({ds_id}) 配置缺失", "Dataset 目录未找到")
            continue

        cfg = dataset_configs[ds_id]
        prn = printed[no]

        # Lx
        c.check(prn["lx"] == str(int(cfg["lx"])), f"Case {no} Lx",
                f"源 {cfg['lx']} / 印刷 `{prn['lx']}`")
        # Ly
        c.check(prn["ly"] == str(int(cfg["ly"])), f"Case {no} Ly",
                f"源 {cfg['ly']} / 印刷 `{prn['ly']}`")
        # Δ
        c.eq(f"Case {no} Δ", cfg["delta"], prn["delta"], nd=2)

        # Obstacle
        if cfg["obstacle"] is None:
            c.check(prn["obstacle"] == "--", f"Case {no} Obstacle (无)",
                    f"印刷 `{prn['obstacle']}`")
        else:
            cx, cy, a, b = cfg["obstacle"]
            expected = f"({int(cx)},{int(cy)},{int(a)},{int(b)})"
            c.check(prn["obstacle"] == expected, f"Case {no} Obstacle",
                    f"源 {expected} / 印刷 `{prn['obstacle']}`")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
