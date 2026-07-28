"""
metrics.py — Sol / TL 的唯一口径定义
=====================================
两条渠道读同一个量，必须给出同一个数，否则口径就是错的。

Sol（论文列名，单位 1e-6）
    = 场复数解的均方误差 MSE × 1e6
    xlsx 渠道：每频率块的 "MSE" 列（块内第 2 列）
    log  渠道：(总损失 − w_prior × prior) / w_rel
               即日志 "Loss-ComplexMSE (w=...)" 除以 w_rel

TL（dB）
    xlsx 渠道："TL vs COMSOL" 列（块内第 3 列）
    log  渠道：按频率统计表的 "TL vs COMSOL" 列；Overall 取汇总行

★ 两个历史坑，改动前先读：
  1) Sol 不是 "Comsol vs sol" / 日志 "非修正解 vs COMSOL误差" —— 那是未经修正的
     先验误差（prior_mse），量级差一个数量级。曾把 Case 3 @25Hz 读成 11.107（正确 2.476）。
  2) 损失权重不是常数。消融的 no_prior_loss 变体日志里 prior=0.00e+00，
     套用 w_prior=1 会算出负的 Sol。必须从日志现场解析 "Loss Weights:" 行。
"""
import glob
import os
import re

import openpyxl

FREQS = (25, 50, 75, 100)
GROUPS = ("Overall",) + FREQS          # xlsx 频率块顺序
SUBCOLS = ("损失", "MSE", "TL vs COMSOL", "Comsol vs sol")

_wb_cache = {}


# ══════════════════════════════════════════════════════════════════════
#  xlsx 渠道
# ══════════════════════════════════════════════════════════════════════
def load_sheet(path, sheet=0):
    """按 (path, sheet) 缓存，避免同一表被反复解压。返回行元组列表。"""
    key = (os.path.abspath(path), sheet)
    if key not in _wb_cache:
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb.worksheets[sheet] if isinstance(sheet, int) else wb[sheet]
        _wb_cache[key] = list(ws.iter_rows(values_only=True))
    return _wb_cache[key]


def find_header(rows):
    """定位表头行：含 'No.' 的行是组标签行，其下一行是子列行。

    返回 (group_row_idx, sub_row_idx)，0-based。
    不写死行号——各节汇总表前面的说明行数不一致。
    """
    for i, r in enumerate(rows):
        if r and any(isinstance(c, str) and c.strip() == "No." for c in r):
            return i, i + 1
    raise ValueError("未找到表头行（应含单元格 'No.'）")


def group_columns(rows):
    """组标签 -> 该组起始列号(0-based)。

    组标签行形如 [... 'Overall', None, None, None, '25Hz', None, ...]，
    合并单元格只在首列留值，故顺序扫描非空标签即得各组起点。
    """
    gi, _ = find_header(rows)
    out = {}
    for j, c in enumerate(rows[gi]):
        if not isinstance(c, str):
            continue
        lab = c.strip()
        if lab == "Overall":
            out["Overall"] = j
        else:
            m = re.fullmatch(r"(\d+)\s*Hz", lab)
            if m:
                out[int(m.group(1))] = j
    return out


def best_epoch_col(rows):
    """'Best Epoch' 列号。表头里该单元格含换行（'Best\\nEpoch'）。"""
    gi, _ = find_header(rows)
    for j, c in enumerate(rows[gi]):
        if isinstance(c, str) and re.sub(r"\s+", " ", c).strip().lower() == "best epoch":
            return j
    return None


def case_row(rows, no):
    """No. 列等于 no 的数据行。"""
    for r in rows:
        if not r:
            continue
        v = r[0]
        if isinstance(v, (int, float)) and int(v) == no:
            return r
        if isinstance(v, str) and v.strip().isdigit() and int(v.strip()) == no:
            return r
    return None


def xlsx_case(path, no, sheet=0):
    """一个案例的全部 Sol/TL + best epoch。

    返回 {'best_epoch': int|None,
          'Overall': {'sol':…, 'tl':…, 'loss':…, 'prior':…},
          25: {...}, 50: {...}, 75: {...}, 100: {...}}
    Sol 已乘 1e6，与论文印刷单位一致。
    """
    rows = load_sheet(path, sheet)
    r = case_row(rows, no)
    if r is None:
        raise ValueError(f"xlsx 中无 No.={no} 行: {path}")
    groups = group_columns(rows)
    bec = best_epoch_col(rows)

    def num(j):
        try:
            return float(r[j])
        except (TypeError, ValueError, IndexError):
            return None

    out = {}
    be = num(bec) if bec is not None else None
    out["best_epoch"] = int(be) if be is not None else None
    for g, j in groups.items():
        loss, mse, tl, prior = num(j), num(j + 1), num(j + 2), num(j + 3)
        out[g] = {
            "loss": loss,
            "sol": None if mse is None else mse * 1e6,
            "tl": tl,
            "prior": prior,
        }
    return out


# ══════════════════════════════════════════════════════════════════════
#  log 渠道
# ══════════════════════════════════════════════════════════════════════
_RE_WEIGHTS = re.compile(r"Loss Weights:\s*rel_mse=([0-9.eE+-]+),\s*prior=([0-9.eE+-]+)")
# 训练块写"总损失"，评估块写"测试损失"，两者都要认
_RE_TOTAL = re.compile(r"(?:总损失|测试损失):\s*([0-9.eE+-]+)")
_RE_CMSE = re.compile(r"Loss-ComplexMSE\s*\(w=[^)]*\):\s*([0-9.eE+-]+)")
_RE_PRIOR = re.compile(r"Loss-Prior\([^)]*\)\s*\(w=[^)]*\):\s*([0-9.eE+-]+)")
# 按频率行： 频率 样本数 损失 Sol_vs_COMSOL TL_vs_COMSOL 时间 占比
_RE_FREQ = re.compile(
    r"^\s*(\d+)\s+(\d+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.]+)\s*%?",
    re.M)
_RE_OVERALL = re.compile(
    r"^\s*Overall\s+(\d+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.]+)\s*%?",
    re.M)


_RE_ANY_EPOCH = re.compile(r"(?:训练|评估) Epoch \d+ 完成")


def epoch_block(log_text, epoch, phase="eval"):
    """截取某一轮某一阶段的统计块。

    ★ 每一轮日志有两个块，指标不同源，必须显式选择：
        "训练 Epoch N 完成"  → 训练集（写"总损失"）
        "评估 Epoch N 完成"  → 测试集（写"测试损失"）
      论文所有 Sol/TL 均为**held-out 测试集**评估值，故缺省 phase='eval'。
      Case 1 @ep200：训练集 ComplexMSE=8.578e-05，测试集=2.090e-04，
      xlsx 记的是后者（Sol=2.090）。早期版本误取训练块，Overall 差 2.4 倍。
    """
    head = "评估" if phase == "eval" else "训练"
    m = re.search(rf"{head} Epoch {epoch} 完成", log_text)
    if not m:
        return None
    nxt = _RE_ANY_EPOCH.search(log_text, m.end())
    return log_text[m.start(): nxt.start() if nxt else len(log_text)]


def log_epoch(log_path, epoch, phase="eval"):
    """日志中某一轮的 Sol/TL（缺省取测试集评估块，与论文口径一致）。

    Sol = (损失 − w_prior × prior) / w_rel × 1e6，权重现场解析。
    返回结构同 xlsx_case（无 best_epoch 键）。
    """
    txt = open(log_path, encoding="utf-8", errors="ignore").read()
    blk = epoch_block(txt, epoch, phase)
    if blk is None:
        return None

    mw = _RE_WEIGHTS.search(blk)
    w_rel, w_prior = (float(mw.group(1)), float(mw.group(2))) if mw else (100.0, 1.0)

    out = {"weights": (w_rel, w_prior), "phase": phase}

    # Overall：优先用 Loss-ComplexMSE（已是 w_rel×MSE），退化到总损失−prior
    mc, mt, mp = _RE_CMSE.search(blk), _RE_TOTAL.search(blk), _RE_PRIOR.search(blk)
    ov_sol = None
    if mc:
        ov_sol = float(mc.group(1)) / w_rel * 1e6
    elif mt and mp:
        ov_sol = (float(mt.group(1)) - w_prior * float(mp.group(1))) / w_rel * 1e6

    mo = _RE_OVERALL.search(blk)
    out["Overall"] = {
        "sol": ov_sol,
        "tl": float(mo.group(4)) if mo else None,
        "loss": float(mt.group(1)) if mt else None,
        "prior": float(mp.group(1)) if mp else None,
        "time_ms": float(mo.group(5)) if mo else None,
    }

    for m in _RE_FREQ.finditer(blk):
        f = int(m.group(1))
        if f not in FREQS:
            continue
        loss, prior, tl, t = (float(m.group(3)), float(m.group(4)),
                              float(m.group(5)), float(m.group(6)))
        out[f] = {
            "sol": (loss - w_prior * prior) / w_rel * 1e6,
            "tl": tl,
            "loss": loss,
            "prior": prior,
            "time_ms": t,
        }
    return out


def log_best_epoch(log_path):
    """日志里最后一次 "保存最佳模型 ... (Epoch N, ...)" 的 N。

    这是日志自证的 best epoch，用来独立校验 xlsx 的 Best Epoch 列。
    """
    txt = open(log_path, encoding="utf-8", errors="ignore").read()
    hits = re.findall(r"保存最佳模型.*?\(Epoch (\d+),", txt)
    return int(hits[-1]) if hits else None


# ══════════════════════════════════════════════════════════════════════
#  印刷值比对
# ══════════════════════════════════════════════════════════════════════
def fmt(v, nd=3):
    return None if v is None else f"{v:.{nd}f}"


def eq_print(src, printed, nd=3):
    """源值按印刷位数四舍五入后是否与印刷值逐字符相等。

    不设数值容差：容差会掩盖真实偏差，也会把"补 0"伪造的值判为通过。
    """
    if src is None or printed is None:
        return False
    return fmt(src, nd) == f"{float(printed):.{nd}f}"
