"""
paths.py — 第四章核验体系的唯一路径解析层
==========================================
所有脚本一律经本模块取路径，禁止在别处硬编码，
否则各节日志目录命名差异（4.2 用 train_*/logs，4.3 起用 training_run/logs）
会在每个脚本里各写一份 glob，随维护漂移。

三条源链（"源可追溯"的定义）：
  xlsx  汇总表   -> 表格值（全测试集、best epoch）
  log   训练日志 -> 表格值的独立第二渠道（同一 best epoch 的原始块）
  npz   ep200    -> 图片值（绘图样本子集，last epoch）
外加 Validation_Scripts/ 下的绘图脚本，界定图片的生成口径。
"""
import glob
import os

# ── 根路径 ────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))       # …/ch4_validation/common
PKG = os.path.dirname(_HERE)                              # …/ch4_validation/
REPO = os.path.dirname(PKG)                               # …/OceanAcoustic-FNO-FEM_github/
ROOT = os.path.dirname(REPO)                              # D:/Data

# 论文 tex 目录与原始数据目录在本机之外无法猜测，故给出默认值并允许用
# 环境变量覆盖，便于他人克隆后无需改动源码：
#   CH4_TEXDIR  论文 tex 所在目录（含 OE_submission.tex / .aux / Figures/results）
#   CH4_RAWROOT Raw_Experimental_Data 的父目录（含 Data_and_Code_Availability）
_TEXDIR = os.environ.get("CH4_TEXDIR", r"D:\JASA\OE\els-cas-templates")
_RAWROOT = os.environ.get("CH4_RAWROOT", ROOT)

TEX = os.path.join(_TEXDIR, "OE_submission.tex")
AUX = os.path.join(_TEXDIR, "OE_submission.aux")
FIGDIR = os.path.join(_TEXDIR, "Figures", "results")
PLOTDIR = os.path.join(REPO, "Validation_Scripts")   # 同 repo 内的兄弟目录

RAW = os.path.join(_RAWROOT, "Data_and_Code_Availability",
                   "Raw_Experimental_Data")

# 节号 -> Raw_Experimental_Data 下的目录名
SEC_DIR = {
    "4.2": "4.2_Validation",
    "4.3": "4.3_Forward",
    "4.4": "4.4_Comparison",
    "4.5": "4.5_Ablation",
    "4.6": "4.6_Mesh",
    "4.7": "4.7_Generalization",
    "4.8": "4.8_Performance",
}

# 节号 -> 汇总 xlsx 文件名（4.8 命名与其他节不同）
SEC_XLSX = {
    "4.2": "Case1-2_数据汇总.xlsx",
    "4.3": "Case3-14_数据汇总.xlsx",
    "4.4": "Case15-24_数据汇总.xlsx",
    "4.5": "Case25-32_数据汇总.xlsx",
    "4.6": "Case33-38_数据汇总.xlsx",
    "4.7": "Case39-42_数据汇总.xlsx",
    "4.8": "Case43-50_推理时间性能分析.xlsx",
}

# Case No. -> 节号。区间闭合，覆盖 1..50 全部。
_SEC_RANGES = [
    ("4.2", 1, 2), ("4.3", 3, 14), ("4.4", 15, 24), ("4.5", 25, 32),
    ("4.6", 33, 38), ("4.7", 39, 42), ("4.8", 43, 50),
]


def sec_of(no):
    """Case No. -> 所属节号。"""
    for sec, lo, hi in _SEC_RANGES:
        if lo <= no <= hi:
            return sec
    raise KeyError(f"Case {no} 不在 1..50 内")


def sec_root(sec):
    return os.path.join(RAW, SEC_DIR[sec])


def xlsx_path(sec):
    return os.path.join(sec_root(sec), SEC_XLSX[sec])


def case_dir(no):
    """Case No. -> NoNN_* 目录。命名后缀各节不同，故用 glob。"""
    sec = sec_of(no)
    hits = sorted(glob.glob(os.path.join(sec_root(sec), f"No{no:02d}_*")))
    if not hits:
        raise FileNotFoundError(f"Case {no}: 未找到 No{no:02d}_* 目录于 {sec_root(sec)}")
    return hits[0]


def log_path(no):
    """Case No. -> 训练日志。各节把 logs/ 挂在不同父目录下，一律深搜。"""
    hits = sorted(glob.glob(os.path.join(case_dir(no), "**", "logs", "full_run_*.log"),
                            recursive=True))
    if not hits:
        return None
    return hits[-1]          # 同案例多份时取最新一次完整运行


def npz_path(no):
    """Case No. -> ep200 TL 原始数据 npz（图片值的唯一来源）。"""
    hits = sorted(glob.glob(os.path.join(case_dir(no), "*TL原始数据_ep*.npz")))
    return hits[-1] if hits else None


def plot_script(name):
    """Validation_Scripts/ 下的绘图脚本路径，用于在报告里注明成图口径。"""
    return os.path.join(PLOTDIR, name)


def figure_pdf(name):
    """Figures/results/ 下的成图 PDF。"""
    return os.path.join(FIGDIR, name)


def report_path(slug):
    """对象 slug（如 T04_ideal_overall） -> 报告落地路径。"""
    return os.path.join(PKG, "reports", f"{slug}.md")


def rel(p):
    """报告里输出相对 D:/Data 的短路径，便于阅读又不丢可追溯性。"""
    if p is None:
        return "(缺失)"
    try:
        return os.path.relpath(p, ROOT).replace("\\", "/")
    except ValueError:
        return p.replace("\\", "/")
