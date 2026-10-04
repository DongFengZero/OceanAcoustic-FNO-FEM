# -*- coding: utf-8 -*-
"""_figpaths.py — 成图脚本的唯一路径解析层。

成图脚本不硬编码数据目录：一律经本模块取根路径，克隆仓库后只要设好环境
变量就能直接跑。变量名与 ch4_validation/common/paths.py 保持一致，两处
指的是同一个根，避免各写一套而慢慢漂移。

    CH4_RAWROOT   Raw_Experimental_Data 的父目录（含 Data_and_Code_Availability）
                  默认 <repo>/.. 即与仓库平级的目录
    CH4_DATASET   Dataset 目录（各 case 的 comsol_batch_manifest_*.mat）
                  默认 $CH4_RAWROOT/Data_and_Code_Availability/Dataset
    CH4_IDEAL_ROOT 可选：解析解 npz 的另一份副本（<root>/Case0X_*/ 布局）；
                  不设时 fig03_ideal 读公开数据 Raw_Experimental_Data/4.2_Validation
    CH4_TEXDIR    论文目录（含 Figures/results）；默认 <repo>/../els-cas-templates
    CH4_FIGDIR    成图输出目录；默认与脚本同级的 out/

npz 与 manifest 的落点在各 case 目录下，由本模块统一 glob，脚本不再各写一份。
"""
import glob
import os

_HERE = os.path.dirname(os.path.abspath(__file__))   # …/Validation_Scripts
REPO = os.path.dirname(_HERE)                        # …/OceanAcoustic-FNO-FEM_github

# 默认假设仓库与数据目录平级（与 README 的目录约定一致）
_DEFAULT_ROOT = os.path.dirname(REPO)

RAWROOT = os.environ.get("CH4_RAWROOT", _DEFAULT_ROOT)
DATASET = os.environ.get(
    "CH4_DATASET", os.path.join(RAWROOT, "Data_and_Code_Availability", "Dataset"))
RAW = os.path.join(RAWROOT, "Data_and_Code_Availability", "Raw_Experimental_Data")
IDEAL_ROOT = os.environ.get("CH4_IDEAL_ROOT")      # 可选覆盖；默认读公开数据
TEXDIR = os.environ.get("CH4_TEXDIR", os.path.join(_DEFAULT_ROOT, "els-cas-templates"))

FIGDIR_PAPER = os.path.join(TEXDIR, "Figures", "results")


def figdir(script_file=None, local="out"):
    """成图输出目录。

    CH4_FIGDIR 优先（把全部图写到一个地方）；否则写脚本自己所在目录下的
    local/，这样每张图与它的脚本放在一起，仓库里按图号就能找到产物。
    """
    if os.environ.get("CH4_FIGDIR"):
        return os.environ["CH4_FIGDIR"]
    base = os.path.dirname(os.path.abspath(script_file)) if script_file else _HERE
    return os.path.join(base, local)


def npz(case, section=None):
    """Case 号或目录名 -> 该 case 的 ep200 TL npz 路径。

    两种布局都支持：按节分组（Raw_Experimental_Data/4.4_Comparison/No15_*/…）
    与按案例分组（Case15-24/Case15_*/…）。
    """
    pats = []
    if section:
        pats.append(os.path.join(RAW, section, "*", "**", "*__TL*_ep200.npz"))
    pats.append(os.path.join(RAWROOT, "Case*", "*", "*__TL*_ep200.npz"))
    pats.append(os.path.join(RAWROOT, "Case*", "*", "*__TL原始数据_ep200.npz"))
    for pat in pats:
        for p in sorted(glob.glob(pat, recursive=True)):
            base = os.path.basename(os.path.dirname(p))
            if str(case) in base:
                return p
    raise FileNotFoundError("npz not found for case %s under %s" % (case, RAWROOT))


def manifest(case):
    """Case 号或 Dataset 子目录名 -> comsol_batch_manifest_*.mat 路径。"""
    pat = os.path.join(DATASET, str(case), "**", "comsol_batch_manifest_*.mat")
    hits = sorted(glob.glob(pat, recursive=True))
    if not hits:
        raise FileNotFoundError("manifest not found under " + os.path.join(DATASET, str(case)))
    return hits[0]
