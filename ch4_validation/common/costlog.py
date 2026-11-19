"""
costlog.py — 4.8 节离线成本段的源日志（R2 新增段落）
======================================================
Sec. 4.8 末段（回应审稿人 #4 意见 4.5）给出的离线成本与盈亏点不在任何表里，
源头是归档数据里的两类日志：

  COMSOL 批量生成日志  Dataset/<ID>/<cfg>/run_*.log
      末尾"全局每样本求解时间统计（所有频率合并）"块：总样本数、均值 / 中位数 /
      P95（ms）、求解总计（s）。
  训练统计 JSON        Raw_Experimental_Data/<sec>/NoNN_*/training_run/logs/
      statistics_epoch200.json 的 timing_summary.train.total_s（全精度训练墙钟）；
      同目录 full_run_*.log 的"使用GPU数量"给出卡数。
  单卡推理日志         4.8_Performance/No43_R1/training_run/logs/gpu1_full_run_*.log
      "推理时间统计摘要 → 测试集 → 平均每样本时间"。

本模块只负责读数；比对逻辑在 scripts/PROSE_cost.py，PROSE_numbers.py 也从
这里取值，使 4.8 节正文的小数都有出处。
"""
import glob
import json
import os
import re

from . import paths


def _read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def comsol_stats(dataset_id="R1"):
    """COMSOL 生成日志末尾的全局统计块。返回 dict 或 None（日志缺失）。"""
    p = paths.gen_log(dataset_id)
    if not p:
        return None
    txt = _read(p)
    i = txt.find("全局每样本求解时间统计")
    tail = txt[i:] if i >= 0 else txt
    pats = {"n": r"总样本数\s*:\s*(\d+)",
            "mean_ms": r"均值\s*:\s*([\d.]+)\s*ms",
            "median_ms": r"中位数\s*:\s*([\d.]+)\s*ms",
            "p95_ms": r"P95\s*:\s*([\d.]+)\s*ms",
            "total_s": r"求解总计\s*:\s*([\d.]+)\s*s"}
    out = {"path": p}
    for k, pat in pats.items():
        m = re.search(pat, tail)
        out[k] = float(m.group(1)) if m else None
    return out


def train_stats(no=15):
    """Case no 的训练墙钟（JSON 全精度）、epoch 数与卡数（日志）。"""
    d = paths.case_dir(no)
    js = sorted(glob.glob(os.path.join(d, "**", "logs", "statistics_epoch200.json"),
                          recursive=True))
    log = paths.log_path(no)
    out = {"json": js[-1] if js else None, "log": log,
           "total_s": None, "epoch": None, "n_gpu": None}
    if js:
        j = json.load(open(js[-1], encoding="utf-8"))
        out["total_s"] = float(j["timing_summary"]["train"]["total_s"])
        out["epoch"] = int(j["epoch"])
    if log:
        m = re.search(r"使用GPU数量\s*:\s*(\d+)", _read(log))
        out["n_gpu"] = int(m.group(1)) if m else None
    return out


def single_gpu_infer_ms(no=43):
    """Case no 单卡日志的测试集平均每样本时间（ms）。返回 (值, 日志路径)。"""
    d = paths.case_dir(no)
    hits = sorted(glob.glob(os.path.join(d, "**", "logs", "gpu1_full_run_*.log"),
                            recursive=True))
    if not hits:
        return None, None
    t = _read(hits[-1])
    i = t.find("推理时间统计摘要")
    j = t.find("测试集:", i) if i >= 0 else -1
    m = re.search(r"平均每样本时间\s*:\s*([\d.]+)\s*ms", t[j:]) if j >= 0 else None
    return (float(m.group(1)) if m else None), hits[-1]
