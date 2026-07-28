"""
depthline.py — 深度线族（Tables 9-12 / Figs 12-15）的公共重算层
================================================================
这些表的源不是 xlsx，而是成图脚本 `advantage_depth_line.py` 从 ep200 npz
的现场提取。为杜绝口径漂移，本模块**不复制算法**：直接 import 那份脚本，
调用它自己的 `_npz / _grid_row_cache / _find_common_line`，
所以任何一天脚本改了口径，这里跟着变、核验立刻反映出来。

权威副本是 `D:\\Data\\advantage_depth_line.py`：脚本用
`ROOT = dirname(__file__)` 定位数据（`ROOT/Case15-24/...`）与产物
（`ROOT/重绘结果/...`），只有放在 D:\\Data 下这两条路径才成立。
repo 内 `Validation_Scripts/` 的同名文件是副本，md5 相同但 ROOT 不通。
"""
import functools
import hashlib
import importlib.util
import json
import os

import numpy as np

from . import paths

AUTH = os.path.join(paths.ROOT, "advantage_depth_line.py")
COPY = os.path.join(paths.PLOTDIR, "advantage_depth_line.py")
MAE_JSON = os.path.join(paths.ROOT, "重绘结果",
                        "advantage_depthline_MAE_bigfont", "_mae_tables.json")
FIG_DIR = os.path.join(paths.ROOT, "重绘结果", "advantage_depthline_MAE_bigfont")


def md5(p):
    if not p or not os.path.exists(p):
        return None
    h = hashlib.md5()
    with open(p, "rb") as fp:
        for blk in iter(lambda: fp.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


@functools.lru_cache(maxsize=1)
def script():
    """import 权威成图脚本（不执行 main）。"""
    spec = importlib.util.spec_from_file_location("adl_auth", AUTH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@functools.lru_cache(maxsize=1)
def mae_json():
    """成图脚本导出的 MAE 表（已 round 到 3 位），按 group 名索引。"""
    with open(MAE_JSON, encoding="utf-8") as fp:
        return {g["group"]: g for g in json.load(fp)}


@functools.lru_cache(maxsize=8)
def recompute(group):
    """复用脚本自身的函数重算一个组，返回全精度结果。

    json 里的 `mae_table` 是 `round(er, 3)`，无法区分 `1.210` 是真值
    还是补 0 —— 必须回到 npz 拿全精度才能判定，这就是本函数存在的理由。

    返回 dict:
      y_line   选中行的实际深度 (m)
      row      行号 r（GRID 网格内）
      methods  方法标签，顺序即表格行序
      er       {freq: [各方法全精度 MAE]}
      src      {freq: (x, y)} 该频率所选样本的声源坐标
      sample   {freq: 样本索引}
      npz      {case: npz 路径}
    """
    m = script()
    cfg = m.GROUPS[group]
    npzs = {c: m._npz(cfg["grpdir"], c) for c, _ in cfg["members"]}
    missing = [c for c, p in npzs.items() if p is None]
    if missing:
        raise FileNotFoundError(f"{group} 缺 npz: {missing}")
    datas = [np.load(npzs[c], allow_pickle=True) for c, _ in cfg["members"]]

    d0 = datas[0]
    Lx, Ly = float(d0["Lx_dom"]), float(d0["Ly_dom"])
    cx, cy, a, b = [float(v) for v in d0["ellipse"]]
    gx = np.linspace(0, Lx, m.GRID)
    gy = np.linspace(0, Ly, m.GRID)
    GX, GY = np.meshgrid(gx, gy)
    outside = (GY > (Ly / Lx) * GX) if bool(d0["is_wedge"]) \
        else np.zeros_like(GX, dtype=bool)
    inside_ell = ((GX - cx) / (a * 1.10)) ** 2 + ((GY - cy) / (b * 1.10)) ** 2 <= 1.0
    vmin, vmax = float(d0["vmin"]), float(d0["vmax"])

    fa = d0["freq"]
    fsid = {f: [i for i in range(len(fa)) if int(round(fa[i])) == f] for f in m.FREQS}
    grids = {s: m._grid_row_cache(datas, s, GX, GY, outside, inside_ell, vmin, vmax)
             for s in sorted({s for v in fsid.values() for s in v})}
    geom = dict(GX=GX, GY=GY, gx=gx, gy=gy, outside=outside, inside_ell=inside_ell,
                Lx=Lx, Ly=Ly, cx=cx, cy=cy, a=a, b=b, vmin=vmin, vmax=vmax)

    chosen = m._find_common_line(grids, fsid, geom, force_y=cfg.get("force_y"))
    if chosen is None:
        raise RuntimeError(f"{group} 未能确定公共深度线")

    r = next(iter(chosen.values()))["r"]
    src_all = d0["source_pos"]
    return dict(
        y_line=float(gy[r]), row=int(r),
        force_y=cfg.get("force_y"), domain=cfg["domain"], grpdir=cfg["grpdir"],
        methods=[lb for _, lb in cfg["members"]],
        cases=[c for c, _ in cfg["members"]],
        er={f: [float(v) for v in chosen[f]["er"]] for f in m.FREQS},
        src={f: tuple(float(v) for v in src_all[chosen[f]["s"]]) for f in m.FREQS},
        sample={f: int(chosen[f]["s"]) for f in m.FREQS},
        npz=npzs,
    )


def figure_pdf(group):
    """成图脚本产出的 PDF（与论文 Figures/results/ 下同名文件应逐字节相同）。"""
    return os.path.join(FIG_DIR, f"{group}.pdf")
