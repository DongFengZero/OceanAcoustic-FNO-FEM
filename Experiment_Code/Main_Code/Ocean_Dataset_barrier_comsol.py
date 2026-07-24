"""
Ocean_Dataset_barrier_comsol.py  (v2)
======================================
相对 v1 变更：
  1. --output_dir 子目录名自动嵌入 Lx/Ly/H/freqs/split 标识，
     与 MATLAB export_dir 的命名逻辑完全对应，避免不同配置互盖。
  2. 新增 --manifest 参数：显式指定 manifest 文件名
     （v4 MATLAB 生成的名称形如 comsol_batch_manifest_Lx128_Ly128_H1.000_f25_50_75_100.mat）
     默认回退到旧版 comsol_batch_manifest.mat。
  3. 新增 --split_train_test / --train_max_x / --train_max_y 参数：
     若 manifest 含 split_info，自动读取并写入 HDF5 元数据；
     同时在输出目录名中体现 split 标识。
  4. 从 manifest 读取并写入 HDF5 的 split_info 字段，
     供下游训练代码按训练/测试切分样本。
  5. .npy 源点文件名加入 split 标识。
  6. 修复 physical_to_node_indices 的唯一性隐患：
     映射完成后对每个频率做节点唯一性检查，若有碰撞则输出警告。

职责（与 v1 相同）：
  1. 读取 MATLAB/COMSOL 生成的 .mat 文件
  2. 写出 acoustic_dataset.h5（路径含区分标识）
  3. 保存 source_positions_physical_*.npy
  4. 保存 timing_statistics.json
  5. 用 tripcolor 绘制每样本 TL 对比图

用法示例（与 v4 MATLAB 配合）：
  python Ocean_Dataset_barrier_comsol.py \\
      --matlab_dir  "./comsol_dataset_export/Lx128_Ly128_H1.000_f25_50_75_100_spf2000_split64x64" \\
      --mat_dir     "./comsol_dataset_export/Lx128_Ly128_H1.000_f25_50_75_100_spf2000_split64x64" \\
      --mesh_file   "comsol_mesh_Lx128_Ly128_H1.000.mat" \\
      --manifest    "comsol_batch_manifest_Lx128_Ly128_H1.000_f25_50_75_100.mat" \\
      --output_dir  "../Ocean" \\
      --grid_x 128 --grid_y 128 --H 1.000 \\
      --frequencies 25 50 75 100 \\
      --samples_per_freq 2000 \\
      --split_train_test \\
      --train_max_x 64 --train_max_y 64
"""

import argparse
import datetime
import json
import logging
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import sys
import time
from pathlib import Path

import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import scipy.sparse as sp
from scipy.special import hankel1
from tqdm import tqdm

try:
    import torch
    import torch.distributed as dist
    DIST_AVAILABLE = True
except ImportError:
    DIST_AVAILABLE = False

try:
    import cupy as cp
    import cupyx.scipy.sparse as cp_sparse
    import cupyx.scipy.sparse.linalg as cp_linalg
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False


# ──────────────────────────────────────────────────────────────────────
# 日志配置
# ──────────────────────────────────────────────────────────────────────
def setup_logger(log_path: str, gpu_id: int = 0) -> logging.Logger:
    logger = logging.getLogger(f"dataset_gpu{gpu_id}")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    fmt = logging.Formatter(
        fmt="%(asctime)s  [GPU%(gpu_id)s]  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)
    try:
        sh.setStream(open(sys.stdout.fileno(), mode='w', encoding='utf-8', closefd=False))
    except Exception:
        pass

    logger.addHandler(fh)
    logger.addHandler(sh)

    old_factory = logging.getLogRecordFactory()
    _gid = gpu_id
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.gpu_id = _gid
        return record
    logging.setLogRecordFactory(record_factory)
    return logger


log: logging.Logger = logging.getLogger("dataset")


def _fmt_sec(s: float) -> str:
    s = float(s)
    if s >= 3600:
        return f"{int(s//3600)}h {int(s%3600//60)}m {s%60:.1f}s"
    if s >= 60:
        return f"{int(s//60)}m {s%60:.1f}s"
    return f"{s:.3f}s"


# ──────────────────────────────────────────────────────────────────────
# 命令行参数
# ──────────────────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description='COMSOL 数据集读取器 v2 — 路径区分 + split_info 支持'
    )
    # ★ 一站式: 只给数据目录,其余(matlab_dir/mat_dir/mesh/manifest + 网格/频率/
    #   椭圆等元数据)自动从目录下的 manifest 与文件名推断;缺啥再报错。
    parser.add_argument('--data_dir',    type=str, default=None,
                        help='COMSOL 导出目录(含 comsol_mesh*.mat 与 '
                             'comsol_batch_manifest*.mat)。给定后 matlab_dir/mat_dir '
                             '默认指向它,网格/频率/采样数/域/椭圆等参数自动从 manifest 读取。'
                             '显式传入的其它参数仍优先生效。')
    parser.add_argument('--matlab_dir',  type=str, default=None,
                        help='MATLAB 生成的 .mat 文件目录 (给了 --data_dir 可省略)')
    parser.add_argument('--grid_x',     type=int,   default=512)
    parser.add_argument('--grid_y',     type=int,   default=128)
    parser.add_argument('--c0',         type=float, default=1500.0)
    parser.add_argument('--H',          type=float, default=1.000)
    parser.add_argument('--amp',        type=float, default=1500.0)
    parser.add_argument('--frequencies',type=int, nargs='+', default=[25,50,75,100])
    parser.add_argument('--samples_per_freq',   type=int,   default=200)
    parser.add_argument('--samples_to_plot',    type=int,   default=9999999)
    parser.add_argument('--backup_ratio',       type=float, default=1.0)
    parser.add_argument('--boundary_margin',    type=float, default=5.0)
    parser.add_argument('--ellipse_cx',         type=float, default=256.0)
    parser.add_argument('--ellipse_cy',         type=float, default=64.0)
    parser.add_argument('--ellipse_a',          type=float, default=32.0)
    parser.add_argument('--ellipse_b',          type=float, default=8.0)
    parser.add_argument('--domain',          type=str, default=None)
    parser.add_argument('--use_ellipse',        action='store_true', default=True)
    parser.add_argument('--reuse_source_positions', action='store_true', default=False)
    parser.add_argument('--source_positions_file',  type=str, default=None)
    parser.add_argument('--mat_dir',     type=str,
                        default='D:/Ocean_Eng_Eng/Code/grid')
    parser.add_argument('--mesh_file',   type=str, default=None,
                        help='网格文件名（相对于 mat_dir）')
    # ★ v2 新增：显式 manifest 文件名
    parser.add_argument('--manifest',    type=str, default=None,
                        help='manifest 文件名（相对于 matlab_dir）。'
                             '默认自动搜索 comsol_batch_manifest*.mat')
    parser.add_argument('--output_dir', type=str, default='../Ocean')
    # ★ v2 新增：split 参数
    parser.add_argument('--split_train_test', action='store_true', default=False,
                        help='启用训练/测试分区（从 manifest split_info 读取元数据）')
    parser.add_argument('--train_max_x', type=float, default=None,
                        help='训练区 x 上界（仅用于路径命名，实际分区由 MATLAB 完成）')
    parser.add_argument('--train_max_y', type=float, default=None,
                        help='训练区 y 上界（仅用于路径命名）')
    parser.add_argument('--local_rank',          type=int, default=0)
    parser.add_argument('--timeout_minutes',     type=int, default=600)
    parser.add_argument('--checkpoint_interval', type=int, default=100)
    return parser.parse_args()


# ──────────────────────────────────────────────────────────────────────
# 边界节点工具（与原版完全一致）
# ──────────────────────────────────────────────────────────────────────
M_REF = np.array([[2., 1., 1.],
                  [1., 2., 1.],
                  [1., 1., 2.]], dtype=np.float64) / 12.0
M_EDGE_REF = np.array([[2., 1.], [1., 2.]], dtype=np.float64) / 6.0


def get_boundary_node_indices(B):
    gamma_upper = B[2, B[2, :] >= 0].tolist()
    gamma_left  = B[0, B[0, :] >= 0].tolist()
    gamma_right = B[1, B[1, :] >= 0].tolist()
    gamma_wedge = B[3, B[3, :] >= 0].tolist()
    gamma_upper_set = set(gamma_upper)
    gamma_robin = [i for i in (gamma_left + gamma_right)
                   if i not in gamma_upper_set]
    return gamma_upper, gamma_robin, gamma_wedge


def infer_domain_shape(mani: dict | None = None,
                       mesh_mat: dict | None = None,
                       p_nodes: np.ndarray | None = None) -> str:
    """
    自动推断域形状，优先级：
      1. manifest 的 domain_m 字段（MATLAB v6 写入）
      2. 网格 .mat 文件的 domain 字段（MATLAB v6 写入）
      3. 节点坐标分布自动检测（占空比 + y 跨度变异系数）

    返回 'rectangle' 或 'wedge'。
    """
    _NORM = {'rectangle': 'rectangle', 'rect': 'rectangle',
             'wedge': 'wedge', 'right_triangle': 'wedge'}

    # ── 1. manifest domain_m ──────────────────────────────────────────
    if mani is not None:
        raw = mani.get('domain_m', None)
        if raw is not None:
            # v7.3(h5py) 下 MATLAB char 存为 uint16 字符码数组，需逐码转字符；
            # scipy.io 下为 char array/str，str() 即可。
            if isinstance(raw, np.ndarray) and raw.dtype.kind in ('u', 'i'):
                try:
                    s = ''.join(chr(int(c)) for c in raw.ravel()).strip().lower()
                except Exception:
                    s = str(raw).strip().lower()
            else:
                s = str(raw).strip().lower().strip("'\"")
            if s in _NORM:
                result = _NORM[s]
                logging.getLogger('dataset').info(
                    f"  [domain 推断] manifest.domain_m='{s}' → '{result}'")
                return result

    # ── 2. mesh .mat domain 字段 ─────────────────────────────────────
    if mesh_mat is not None:
        raw = mesh_mat.get('domain', None)
        if raw is not None:
            if isinstance(raw, np.ndarray):
                # h5py 读出可能是 char array
                try:
                    s = ''.join(chr(int(c)) for c in raw.ravel()).strip().lower()
                except Exception:
                    s = str(raw).strip().lower()
            else:
                s = str(raw).strip().lower().strip("'\"")
            if s in _NORM:
                result = _NORM[s]
                logging.getLogger('dataset').info(
                    f"  [domain 推断] mesh.domain='{s}' → '{result}'")
                return result

    # ── 3. 节点坐标分布自动检测 ──────────────────────────────────────
    if p_nodes is not None:
        # p_nodes: [2,N] 或 [N,2]
        if p_nodes.ndim == 2 and p_nodes.shape[0] == 2:
            x, y = p_nodes[0], p_nodes[1]
        elif p_nodes.ndim == 2 and p_nodes.shape[1] == 2:
            x, y = p_nodes[:, 0], p_nodes[:, 1]
        else:
            x = y = None

        if x is not None and len(x) > 10:
            xr = x.max() - x.min()
            yr = y.max() - y.min()
            if xr > 1e-8 and yr > 1e-8:
                xn = ((x - x.min()) / xr).clip(0, 1)
                yn = ((y - y.min()) / yr).clip(0, 1)
                # 32×32 占空比
                ix = np.clip((xn * 31).astype(int), 0, 31)
                iy = np.clip((yn * 31).astype(int), 0, 31)
                occ = np.zeros((32, 32), dtype=bool)
                occ[ix, iy] = True
                occ_ratio = float(occ.mean())
                # 各 x 列 y 跨度变异系数
                x_edges = np.linspace(0, 1, 17)
                spans = []
                for bi in range(16):
                    mb = (xn >= x_edges[bi]) & (xn < x_edges[bi + 1])
                    if mb.sum() >= 6:
                        yb = yn[mb]
                        spans.append(float(yb.max() - yb.min()))
                if len(spans) >= 4:
                    s_arr = np.array(spans)
                    cv = float(s_arr.std() / max(s_arr.mean(), 1e-6))
                else:
                    cv = 1.0
                result = 'rectangle' if (occ_ratio > 0.55 and cv < 0.35) else 'wedge'
                logging.getLogger('dataset').info(
                    f"  [domain 推断] 节点分布检测: occ={occ_ratio:.3f}, cv={cv:.3f}"
                    f" → '{result}'")
                return result

    logging.getLogger('dataset').warning(
        "  [domain 推断] 无法从 manifest/mesh/节点推断域形状，默认 'rectangle'")
    return 'rectangle'


def get_ellipse_excluded_nodes(p, cx, cy, a, b, tol=1e-1):
    X, Y = p[0, :], p[1, :]
    dist_sq = ((X - cx) / a) ** 2 + ((Y - cy) / b) ** 2
    delta = tol / min(a, b)
    mask = dist_sq <= (1.0 + delta) ** 2
    return set(np.where(mask)[0].tolist())


# ──────────────────────────────────────────────────────────────────────
# TL 计算
# ──────────────────────────────────────────────────────────────────────
def assemble_p1_helmholtz_matrix(p, t, e, B, k, c0, USE_ELLIPSE=False,
                                  ELLIPSE_CX=None, ELLIPSE_CY=None,
                                  ELLIPSE_A=None, ELLIPSE_B=None):
    N  = p.shape[1]
    x1, y1 = p[0, t[0]], p[1, t[0]]
    x2, y2 = p[0, t[1]], p[1, t[1]]
    x3, y3 = p[0, t[2]], p[1, t[2]]
    areas = 0.5 * np.abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))

    inv_2A   = 0.5 / areas
    dphi1_dx = (y2-y3)*inv_2A;  dphi1_dy = (x3-x2)*inv_2A
    dphi2_dx = (y3-y1)*inv_2A;  dphi2_dy = (x1-x3)*inv_2A
    dphi3_dx = (y1-y2)*inv_2A;  dphi3_dy = (x2-x1)*inv_2A

    S11=(dphi1_dx**2+dphi1_dy**2)*areas; S22=(dphi2_dx**2+dphi2_dy**2)*areas
    S33=(dphi3_dx**2+dphi3_dy**2)*areas
    S12=(dphi1_dx*dphi2_dx+dphi1_dy*dphi2_dy)*areas
    S13=(dphi1_dx*dphi3_dx+dphi1_dy*dphi3_dy)*areas
    S23=(dphi2_dx*dphi3_dx+dphi2_dy*dphi3_dy)*areas

    k2  = k * k
    M11=M_REF[0,0]*areas; M12=M_REF[0,1]*areas; M13=M_REF[0,2]*areas
    M22=M_REF[1,1]*areas; M23=M_REF[1,2]*areas; M33=M_REF[2,2]*areas

    v11=S11-k2*M11; v12=S12-k2*M12; v13=S13-k2*M13
    v22=S22-k2*M22; v23=S23-k2*M23; v33=S33-k2*M33

    i0, i1, i2 = t[0], t[1], t[2]
    rows_v = np.concatenate([i0, i0, i0, i1, i1, i2,   i1, i2, i2])
    cols_v = np.concatenate([i0, i1, i2, i1, i2, i2,   i0, i0, i1])
    vals_v = np.concatenate([v11,v12,v13,v22,v23,v33,  v12,v13,v23])
    A = sp.coo_matrix((vals_v, (rows_v, cols_v)), shape=(N, N)).tocsr()

    gamma_upper, gamma_robin, gamma_wedge = get_boundary_node_indices(B)
    gamma_upper_set = set(gamma_upper)
    gamma_robin_set = set(gamma_robin)
    gamma_wedge_set = set(gamma_wedge)

    rr, rc, rv = [], [], []
    for ib in range(e.shape[1]):
        n1, n2 = int(e[0, ib]), int(e[1, ib])
        if n1 < 0 or n2 < 0 or n1 >= N or n2 >= N:
            continue
        if not (n1 in gamma_robin_set and n2 in gamma_robin_set):
            continue
        if (n1 in gamma_upper_set or n2 in gamma_upper_set or
                n1 in gamma_wedge_set or n2 in gamma_wedge_set):
            continue
        dx = p[0, n2]-p[0, n1];  dy = p[1, n2]-p[1, n1]
        L  = np.sqrt(dx*dx + dy*dy)
        Me = M_EDGE_REF * L
        fv = -1j * k
        for li in range(2):
            for lj in range(2):
                rr.append([n1, n2][li])
                rc.append([n1, n2][lj])
                rv.append(fv * Me[li, lj])

    if rr:
        A_robin = sp.coo_matrix(
            (np.array(rv, dtype=np.complex128),
             (np.array(rr, dtype=np.int32), np.array(rc, dtype=np.int32))),
            shape=(N, N)
        ).tocsr()
        A = A + A_robin

    dirichlet_set = set(gamma_upper)
    if USE_ELLIPSE and None not in (ELLIPSE_CX, ELLIPSE_CY, ELLIPSE_A, ELLIPSE_B):
        X, Y    = p[0, :], p[1, :]
        dist_sq = ((X-ELLIPSE_CX)/ELLIPSE_A)**2 + ((Y-ELLIPSE_CY)/ELLIPSE_B)**2
        tol_delta = 0.1 / min(ELLIPSE_A, ELLIPSE_B)
        ell_nodes = np.where(dist_sq <= (1.0 + tol_delta)**2)[0]
        dirichlet_set |= set(ell_nodes.tolist())

    dirichlet_nodes = np.array(sorted(dirichlet_set), dtype=np.int32)
    A = A.tocsr().astype(np.complex128)
    for d in dirichlet_nodes:
        A.data[A.indptr[d]:A.indptr[d+1]] = 0.0
    A = A.T.tocsr()
    for d in dirichlet_nodes:
        A.data[A.indptr[d]:A.indptr[d+1]] = 0.0
    A = A.T.tocsr()
    A.eliminate_zeros()
    A = A.tolil()
    for d in dirichlet_nodes:
        A[d, d] = 1.0 + 0.0j
    A = A.tocsr()
    return A.tocsc()


def compute_tl(pressure, p_ref):
    with np.errstate(divide='ignore', invalid='ignore'):
        return 20.0 * np.log10(np.abs(pressure) / float(np.abs(p_ref)))


def check_nan_inf(data, name='data'):
    if np.iscomplexobj(data):
        nan_mask = np.isnan(data.real) | np.isnan(data.imag)
        inf_mask = np.isinf(data.real) | np.isinf(data.imag)
    else:
        nan_mask = np.isnan(data)
        inf_mask = np.isinf(data)
    return bool(nan_mask.any() or inf_mask.any()), int(nan_mask.sum()), int(inf_mask.sum())


# ──────────────────────────────────────────────────────────────────────
# 绘图
# ──────────────────────────────────────────────────────────────────────
def plot_tl_comparison(p, t, fem_tl, source_pos,
                       sample_idx, plot_dir, frequency,
                       domain_shape: str = 'rectangle'):
    """
    可视化 TL 对比图。
    坐标约定（矩形/楔形通用）：左上角 (0,0)，x 向右，y 向下，invert_yaxis 保证显示正确。
    楔形时额外绘制斜底边界线（海底 Rigid：y = (Ly/Lx)*x，从楔尖 (0,0) 到右下角 (Lx,Ly)）；Robin 仅在右截断边 x=Lx，与 COMSOL/上游约定一致。
    """
    X, Y = p[0], p[1]
    Lx_dom = float(X.max())
    Ly_dom = float(Y.max())
    vmin, vmax = -60.0, 0.0
    fem_finite = fem_tl[np.isfinite(fem_tl)]
    if len(fem_finite) == 0:
        return

    is_wedge = domain_shape in ('wedge', 'right_triangle')

    plt.ioff()
    fig, ax = plt.subplots(1, 1, figsize=(6, 6), dpi=100)

    def _decorate(ax, title):
        ax.set_title(title)
        ax.set_xlabel('X (m)'); ax.set_ylabel('Y / Depth (m)')
        ax.invert_yaxis()   # y=0 在顶部（海面），y=Ly 在底部（海底）
        ax.set_aspect('equal', adjustable='box')
        if is_wedge:
            # 斜底边（海底 Rigid）：从楔尖 (0,0) 到 (Lx,Ly)，即 y = (Ly/Lx)*x
            ax.plot([0, Lx_dom], [0, Ly_dom], 'k-', linewidth=1.5,
                    label='Rigid boundary')
            # 右截断边 x=Lx（Robin/Nonreflecting）；左侧 x=0 为楔尖退化点，无边界
            ax.plot([Lx_dom, Lx_dom], [0, Ly_dom], color='gray', linewidth=1.0,
                    linestyle='--', label='Nonreflecting (x=Lx)')
        # 标注声源
        ax.plot(source_pos[0], source_pos[1], 'r*', markersize=10, label='Source')

    tpc = ax.tripcolor(X, Y, t.T, fem_tl, shading='flat', cmap='jet',
                       vmin=vmin, vmax=vmax, rasterized=True)
    _decorate(ax, 'FEM TL (dB)')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.83, 0.15, 0.03, 0.7])
    fig.colorbar(tpc, cax=cbar_ax, label='TL (dB)')

    domain_label = 'Wedge' if is_wedge else 'Rectangle'
    plt.suptitle(
        f"[{domain_label}] Sample {sample_idx}  f={frequency} Hz  "
        f"Src=({source_pos[0]:.1f}, {source_pos[1]:.1f})",
        fontsize=9
    )
    plt.tight_layout(rect=[0, 0, 0.8, 1])
    path = os.path.join(plot_dir, f"TL_comparison_sample_{sample_idx:05d}.png")
    plt.savefig(path, dpi=100, bbox_inches='tight')
    plt.close(fig)
    plt.ion()


# ──────────────────────────────────────────────────────────────────────
# MAT 文件读取
# ──────────────────────────────────────────────────────────────────────
def load_mat(path):
    try:
        return scipy.io.loadmat(path, squeeze_me=False)
    except Exception:
        import h5py as _h5
        data = {}

        def _convert(arr):
            if not isinstance(arr, np.ndarray):
                return arr
            if arr.dtype.names and 'real' in arr.dtype.names and 'imag' in arr.dtype.names:
                arr = arr['real'].astype(np.float64) + 1j * arr['imag'].astype(np.float64)
            if arr.ndim >= 2:
                arr = arr.T
            return arr

        with _h5.File(path, 'r') as f:
            def _visit(name, obj):
                if isinstance(obj, _h5.Dataset):
                    key = name.split('/')[-1]
                    data[key] = _convert(obj[()])
            for k in f.keys():
                obj = f[k]
                if isinstance(obj, _h5.Dataset):
                    data[k] = _convert(obj[()])
                elif isinstance(obj, _h5.Group):
                    obj.visititems(_visit)
        return data


def mat_scalar(v):
    if isinstance(v, np.ndarray):
        return v.flat[0]
    return v


def _mani_str(mani: dict, key: str):
    """从 manifest 读取字符串字段，兼容 scipy.io（char array / str）与
    h5py（v7.3 下 MATLAB char 存为 uint16 字符码数组）两种读取方式。
    缺字段返回 None。"""
    if key not in mani:
        return None
    v = mani[key]
    try:
        if isinstance(v, np.ndarray):
            if v.dtype.kind in ('U', 'S'):        # 已是字符串数组
                return ''.join(v.ravel().astype(str).tolist()).strip()
            if v.dtype.kind in ('u', 'i', 'f'):   # h5py: MATLAB char → 字符码
                return ''.join(chr(int(c)) for c in v.ravel()).strip()
            return str(v.ravel()[0]).strip()
        return str(v).strip()
    except Exception:
        return None


def mat_complex(v):
    if isinstance(v, np.ndarray):
        if v.dtype.names and 'real' in v.dtype.names and 'imag' in v.dtype.names:
            return v['real'].astype(np.float64) + 1j * v['imag'].astype(np.float64)
        if np.iscomplexobj(v):
            return v.astype(np.complex128)
        return v.astype(np.float64)
    return complex(v)


def _to_complex128(arr: np.ndarray) -> np.ndarray:
    if arr.dtype.names and 'real' in arr.dtype.names and 'imag' in arr.dtype.names:
        return (arr['real'].astype(np.float64)
                + 1j * arr['imag'].astype(np.float64))
    return arr.astype(np.complex128)


def reconstruct_csc(K_i0, K_j0, K_data, K_shape):
    N = int(K_shape[0])
    rows = K_i0.ravel().astype(np.int32)
    cols = K_j0.ravel().astype(np.int32)
    data = K_data.ravel().astype(np.complex128)
    A = sp.coo_matrix((data, (rows, cols)), shape=(N, N))
    return A.tocsc()


def save_source_positions_physical(filepath, positions, backup_positions,
                                   freq_indices, backup_freq_indices,
                                   grid_x, grid_y, samples_per_freq,
                                   num_frequencies, selected_freqs,
                                   current_H, split_info_list=None, note=''):
    save_data = {
        'source_positions_physical': positions,
        'backup_positions_physical': backup_positions,
        'frequency_indices':         freq_indices,
        'backup_frequency_indices':  backup_freq_indices,
        'grid_x':                    grid_x,
        'grid_y':                    grid_y,
        'grid_resolution_H':         float(current_H),
        'samples_per_freq':          samples_per_freq,
        'num_frequencies':           num_frequencies,
        'selected_frequencies':      selected_freqs,
        'storage_type':              'physical',
        'note': note if note else f'H={current_H} COMSOL generated',
    }
    if split_info_list:
        save_data['split_info'] = split_info_list
    np.save(filepath, save_data)
    logging.getLogger('dataset').info(f"  [OK] 源点坐标已保存: {filepath}")


def _rebuild_gaussian_rhs(p, t, elem_areas, src_pos, k, p_ref, N,
                          gamma_upper, H_GRID=1.0):
    sigma  = 1.5 * H_GRID
    norm2  = 2.0 * np.pi * sigma ** 2
    xs, ys = float(src_pos[0]), float(src_pos[1])
    cx = (p[0, t[0]] + p[0, t[1]] + p[0, t[2]]) / 3.0
    cy = (p[1, t[0]] + p[1, t[1]] + p[1, t[2]]) / 3.0
    G = np.exp(-((cx - xs) ** 2 + (cy - ys) ** 2) / (2.0 * sigma ** 2)) / norm2
    F = np.zeros(N, dtype=np.complex128)
    contrib = (G * elem_areas / 3.0).astype(np.complex128)
    np.add.at(F, t[0], contrib)
    np.add.at(F, t[1], contrib)
    np.add.at(F, t[2], contrib)
    F *= p_ref
    F[gamma_upper] = 0.0 + 0j
    return F


# ──────────────────────────────────────────────────────────────────────
# ★ v2 新增：解析 MATLAB split_info struct
# ──────────────────────────────────────────────────────────────────────
def parse_split_info(mani: dict, num_freqs: int) -> list:
    """
    从 manifest 中读取 split_info 结构，返回 list of dict。
    MATLAB struct array 在 h5py 中以不同方式存储，做兼容处理。
    若 manifest 中无 split_info，返回 None。
    """
    raw = mani.get('split_info', None)
    if raw is None:
        return None

    result = []
    try:
        # scipy.io 读取：struct array → numpy structured array 或 object array
        if isinstance(raw, np.ndarray) and raw.dtype.names:
            # structured array：每个字段是 shape (1, num_freqs) 的数组
            fields = raw.dtype.names
            for i in range(raw.size):
                elem = raw.flat[i]
                d = {}
                for f in fields:
                    v = elem[f]
                    if isinstance(v, np.ndarray):
                        v = v.flat[0]
                    d[f] = int(v) if f not in ('freq',) else float(v)
                result.append(d)
        elif isinstance(raw, np.ndarray) and raw.dtype == object:
            # object array（cell-like）
            for i in range(raw.size):
                elem = raw.flat[i]
                if isinstance(elem, np.ndarray) and elem.dtype.names:
                    d = {}
                    for f in elem.dtype.names:
                        v = elem[f]
                        if isinstance(v, np.ndarray): v = v.flat[0]
                        d[f] = float(v) if f == 'freq' else int(v)
                    result.append(d)
        elif isinstance(raw, dict):
            # h5py 读取：dict of arrays，每个 key 对应一个字段
            keys = list(raw.keys())
            n = None
            for k in keys:
                v = np.atleast_1d(raw[k]).ravel()
                if n is None: n = len(v)
            for i in range(n):
                d = {}
                for k in keys:
                    v = np.atleast_1d(raw[k]).ravel()
                    d[k] = float(v[i]) if k == 'freq' else int(v[i])
                result.append(d)
    except Exception as e:
        logging.getLogger('dataset').warning(f"  split_info 解析失败: {e}，将忽略分区信息")
        return None

    if len(result) == 0:
        return None
    return result


# ──────────────────────────────────────────────────────────────────────
# ★ v2 新增：自动查找 manifest 文件
# ──────────────────────────────────────────────────────────────────────
def find_manifest(matlab_dir: str, manifest_arg: str | None) -> str:
    """
    优先使用 --manifest 指定的文件名；
    若未指定则在 matlab_dir 中搜索 comsol_batch_manifest*.mat，
    若有多个则按文件名排序取第一个并发出警告。
    """
    if manifest_arg is not None:
        p = os.path.join(matlab_dir, manifest_arg)
        if not os.path.exists(p):
            raise FileNotFoundError(f"指定的 manifest 不存在: {p}")
        return p

    import glob
    candidates = sorted(glob.glob(os.path.join(matlab_dir, 'comsol_batch_manifest*.mat')))
    if len(candidates) == 0:
        raise FileNotFoundError(
            f"在 {matlab_dir} 中未找到任何 comsol_batch_manifest*.mat\n"
            f"  请用 --manifest 显式指定文件名。"
        )
    if len(candidates) > 1:
        logging.getLogger('dataset').warning(
            f"  找到多个 manifest 文件，使用第一个: {candidates[0]}\n"
            f"  其余: {candidates[1:]}\n"
            f"  若需指定，请用 --manifest 参数。"
        )
    return candidates[0]


# ──────────────────────────────────────────────────────────────────────
# 主程序
# ──────────────────────────────────────────────────────────────────────
def _autofill_from_data_dir(args):
    """给定 --data_dir 时,自动解析路径并从 manifest 读取生成参数。

    优先级: 用户显式传入的命令行参数 > manifest 读取值 > argparse 默认。
    缺关键文件(目录/manifest)时直接报错。
    """
    import glob, sys
    if not args.data_dir:
        if args.matlab_dir is None:
            raise SystemExit("必须给 --data_dir 或 --matlab_dir 之一")
        return args   # 未用一站式模式,保持原行为

    d = args.data_dir
    if not os.path.isdir(d):
        raise SystemExit(f"--data_dir 不是有效目录: {d}")

    # 用户在命令行显式给过的参数名 (这些不被 manifest 覆盖)
    _explicit = {a.lstrip('-').split('=')[0] for a in sys.argv[1:] if a.startswith('--')}
    def _set_if_absent(name, value):
        if name not in _explicit and value is not None:
            setattr(args, name, value)

    # 路径默认指向 data_dir
    _set_if_absent('matlab_dir', d)
    _set_if_absent('mat_dir', d)

    # 定位 manifest 与 mesh (glob)
    mani_list = sorted(glob.glob(os.path.join(d, 'comsol_batch_manifest*.mat')))
    if not mani_list:
        raise SystemExit(f"--data_dir 下未找到 comsol_batch_manifest*.mat: {d}")
    mesh_list = sorted(glob.glob(os.path.join(d, 'comsol_mesh*.mat')))
    if not mesh_list:
        raise SystemExit(f"--data_dir 下未找到 comsol_mesh*.mat: {d}")
    _set_if_absent('manifest', os.path.basename(mani_list[0]))
    _set_if_absent('mesh_file', os.path.basename(mesh_list[0]))

    # 从 manifest 读生成参数
    mani = load_mat(mani_list[0])
    def _scalar(key):
        if key not in mani:
            return None
        try:
            return float(np.asarray(mani[key]).reshape(-1)[0])
        except Exception:
            return None
    def _vec_int(key):
        if key not in mani:
            return None
        try:
            return sorted(int(round(v)) for v in np.asarray(mani[key]).reshape(-1))
        except Exception:
            return None

    _g = lambda k: _scalar(k)
    if _g('Lx_m') is not None:        _set_if_absent('grid_x', int(round(_g('Lx_m'))))
    if _g('Ly_m') is not None:        _set_if_absent('grid_y', int(round(_g('Ly_m'))))
    if _g('H_grid_m') is not None:    _set_if_absent('H', _g('H_grid_m'))
    if _g('c0_m') is not None:        _set_if_absent('c0', _g('c0_m'))
    if _g('amp_m') is not None:       _set_if_absent('amp', _g('amp_m'))
    if _g('samples_per_frequency') is not None:
        _set_if_absent('samples_per_freq', int(round(_g('samples_per_frequency'))))
    _freqs = _vec_int('selected_frequencies')
    if _freqs is not None:            _set_if_absent('frequencies', _freqs)
    # 椭圆 (与 manifest 一致,避免域外 0 节点)
    if _g('use_ellipse_m') is not None: _set_if_absent('use_ellipse', bool(_g('use_ellipse_m')))
    if _g('ellipse_cx_m') is not None:  _set_if_absent('ellipse_cx', _g('ellipse_cx_m'))
    if _g('ellipse_cy_m') is not None:  _set_if_absent('ellipse_cy', _g('ellipse_cy_m'))
    if _g('ellipse_a_m') is not None:   _set_if_absent('ellipse_a', _g('ellipse_a_m'))
    if _g('ellipse_b_m') is not None:   _set_if_absent('ellipse_b', _g('ellipse_b_m'))
    # split 元数据
    if _g('split_train_test_m') is not None and bool(_g('split_train_test_m')):
        _set_if_absent('split_train_test', True)
    if _g('train_max_x_m') is not None: _set_if_absent('train_max_x', _g('train_max_x_m'))
    if _g('train_max_y_m') is not None: _set_if_absent('train_max_y', _g('train_max_y_m'))

    print(f"[一站式] 从 {d} 自动解析: grid={args.grid_x}x{args.grid_y} H={args.H} "
          f"freqs={args.frequencies} spf={args.samples_per_freq} "
          f"椭圆=({args.ellipse_cx},{args.ellipse_cy},{args.ellipse_a},{args.ellipse_b}) "
          f"mesh={args.mesh_file} manifest={args.manifest}")
    return args


def main():
    args = parse_args()
    args = _autofill_from_data_dir(args)

    GRID_SIZE_X          = args.grid_x
    GRID_SIZE_Y          = args.grid_y
    GRID_X               = GRID_SIZE_X
    GRID_Y               = GRID_SIZE_Y
    c0                   = args.c0
    amp                  = args.amp
    C0                   = c0
    AMP                  = amp
    H                    = f"{args.H:.3f}"
    SELECTED_FREQUENCIES = sorted(args.frequencies)
    SAMPLES_PER_FREQUENCY = args.samples_per_freq
    SAMPLES_PER_FREQ     = SAMPLES_PER_FREQUENCY
    SAMPLES_TO_PLOT      = args.samples_to_plot
    BACKUP_RATIO         = args.backup_ratio
    USE_ELLIPSE          = args.use_ellipse
    ELLIPSE_CX = args.ellipse_cx if args.ellipse_cx is not None else GRID_SIZE_X / 2.0
    ELLIPSE_CY = args.ellipse_cy if args.ellipse_cy is not None else GRID_SIZE_Y / 2.0
    ELLIPSE_A            = args.ellipse_a
    ELLIPSE_B            = args.ellipse_b
    NUM_FREQS            = len(SELECTED_FREQUENCIES)
    NUM_SAMPLES          = SAMPLES_PER_FREQUENCY * NUM_FREQS
    BACKUP_PER_FREQ      = int(SAMPLES_PER_FREQUENCY * BACKUP_RATIO)
    MATLAB_DIR           = args.matlab_dir
    WEDGE_ANGLE          = np.arctan(GRID_SIZE_Y / GRID_SIZE_X)
    AVAILABLE_FREQUENCIES = [25, 50, 75, 100]

    SPLIT_TRAIN_TEST = args.split_train_test
    TRAIN_MAX_X      = args.train_max_x
    TRAIN_MAX_Y      = args.train_max_y

    # ── 分布式初始化 ────────────────────────────────────────────────
    if 'RANK' in os.environ and 'WORLD_SIZE' in os.environ:
        if not DIST_AVAILABLE:
            raise RuntimeError("torch.distributed 不可用")
        rank       = int(os.environ['RANK'])
        world_size = int(os.environ['WORLD_SIZE'])
        local_rank = int(os.environ['LOCAL_RANK'])
        from datetime import timedelta
        dist.init_process_group(
            backend='nccl',
            timeout=timedelta(minutes=args.timeout_minutes),
            init_method='env://',
        )
        torch.cuda.set_device(local_rank)
        args.local_rank = local_rank
    else:
        rank = 0
        world_size = 1
        local_rank = args.local_rank

    for freq in SELECTED_FREQUENCIES:
        if freq not in AVAILABLE_FREQUENCIES:
            raise ValueError(f"频率 {freq} 不在可选频率池 {AVAILABLE_FREQUENCIES} 中")

    # ── ★ 第0步：提前读 manifest 推断 domain_tag，再构建输出路径 ─────
    # 必须在 output_dir 构建之前完成，否则路径前缀永远是默认值。
    _manifest_path_early = find_manifest(MATLAB_DIR, args.manifest)
    _mani_early = load_mat(_manifest_path_early)

    # 尝试从 manifest 读网格文件路径推断 mesh（仅用于 domain 推断，可选）
    _mesh_early = None
    _mesh_file_early = os.path.join(
        MATLAB_DIR, f"comsol_mesh_Lx{GRID_SIZE_X}_Ly{GRID_SIZE_Y}_H{H}.mat"
    )
    if os.path.exists(_mesh_file_early):
        try:
            _mesh_early = load_mat(_mesh_file_early)
        except Exception:
            _mesh_early = None

    domain_tag = infer_domain_shape(
        mani=_mani_early, mesh_mat=_mesh_early, p_nodes=None
    )
    print(f"[domain 推断] '{domain_tag}' (manifest+mesh 预读取)")

    # ── ★ v2：构建区分性输出路径 ────────────────────────────────────
    freq_str = "_".join(map(str, SELECTED_FREQUENCIES))

    # split 标识（与 MATLAB 端逻辑对称）
    if SPLIT_TRAIN_TEST and TRAIN_MAX_X is not None and TRAIN_MAX_Y is not None:
        split_tag = f"_split{TRAIN_MAX_X:.0f}x{TRAIN_MAX_Y:.0f}"
    else:
        split_tag = ""

    # ── 参考解类型标识（解析解 vs COMSOL/FEM）──────────────────────────
    # data_generate_comsol_sol.m 生成的解析解数据集在 manifest 写入
    # reference_solution_type_m='analytic'，据此给输出目录加 _analyticsol 后缀，
    # 与 MATLAB 导出目录命名对齐，避免和同网格/频率的 COMSOL 参考数据集互相覆盖。
    reference_solution_type = _mani_str(_mani_early, 'reference_solution_type_m')
    if reference_solution_type is None:
        reference_solution_type = 'FEM'
    sol_tag = "_analyticsol" if reference_solution_type.strip().lower() == 'analytic' else ""

    subdir_name = (
        f"{domain_tag}"
        f"_Lx{GRID_SIZE_X}_Ly{GRID_SIZE_Y}_H{H}"
        f"_f{freq_str}"
        f"_spf{SAMPLES_PER_FREQUENCY}"
        f"{split_tag}"
        f"{sol_tag}"
    )
    output_dir = os.path.join(args.output_dir, subdir_name)
    plot_dir   = os.path.join(output_dir, "TL_Comparison_Plots")
    ckpt_dir   = os.path.join(output_dir, "checkpoints")

    if rank == 0:
        for d in [output_dir, plot_dir, ckpt_dir]:
            os.makedirs(d, exist_ok=True)

    if world_size > 1:
        dist.barrier()

    log_path = os.path.join(output_dir, f"run_gpu{args.local_rank}.log")
    global log
    log = setup_logger(log_path, gpu_id=args.local_rank)

    t_program_start = time.time()
    start_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if rank == 0:
        log.info("")
        log.info("=" * 80)
        log.info("海洋声学数据集生成器 v2 (COMSOL后端 + 路径区分 + split_info)")
        log.info("=" * 80)
        log.info(f"程序启动时间: {start_ts}")
        log.info(f"域形状（自动推断）: {domain_tag}")
        log.info(f"网格物理尺寸: {GRID_SIZE_X} x {GRID_SIZE_Y} m")
        log.info(f"网格分辨率: H = {H} m")
        log.info(f"声速: {c0} m/s")
        log.info(f"频率: {SELECTED_FREQUENCIES} Hz")
        log.info(f"每个频率样本数: {SAMPLES_PER_FREQUENCY}")
        log.info(f"总样本数: {NUM_SAMPLES}")
        if SPLIT_TRAIN_TEST:
            log.info(f"训练/测试分区: 启用 (训练区 x≤{TRAIN_MAX_X} AND y≤{TRAIN_MAX_Y})")
        else:
            log.info(f"训练/测试分区: 关闭")
        log.info(f"输出目录: {output_dir}")
        log.info("=" * 80)

    if world_size > 1:
        dist.barrier()

    # ── 1. 读取全局清单（复用已预读取的结果）──────────────────────────
    t_step = time.time()
    manifest_path = _manifest_path_early
    log.info(f"\n读取清单: {manifest_path}")
    mani = _mani_early
    log.info(f"  domain（最终确认）: '{domain_tag}'")

    # ── 椭圆参数: 优先从 manifest 读取 MATLAB 实际生成值,避免与转换器默认不一致 ──
    # MATLAB(data_generate_comsol.m) 把椭圆参数存为 ellipse_cx_m/cy_m/a_m/b_m/use_ellipse_m。
    # 不读会用 argparse 默认(cx=256...),落在 128 域外 → 0 节点,约束/绘图全失效。
    def _mani_scalar(key):
        if key not in mani:
            return None
        v = mani[key]
        try:
            return float(np.asarray(v).reshape(-1)[0])
        except Exception:
            return None
    _ell_cx = _mani_scalar('ellipse_cx_m')
    _ell_cy = _mani_scalar('ellipse_cy_m')
    _ell_a  = _mani_scalar('ellipse_a_m')
    _ell_b  = _mani_scalar('ellipse_b_m')
    _ell_use = _mani_scalar('use_ellipse_m')
    if _ell_cx is not None and _ell_cy is not None \
            and _ell_a is not None and _ell_b is not None:
        log.info(f"  [椭圆] 从 manifest 读取: cx={_ell_cx:.1f} cy={_ell_cy:.1f} "
                 f"a={_ell_a:.1f} b={_ell_b:.1f} (覆盖转换器默认 "
                 f"{ELLIPSE_CX:.1f},{ELLIPSE_CY:.1f},{ELLIPSE_A:.1f},{ELLIPSE_B:.1f})")
        ELLIPSE_CX, ELLIPSE_CY = _ell_cx, _ell_cy
        ELLIPSE_A,  ELLIPSE_B  = _ell_a,  _ell_b
        if _ell_use is not None:
            USE_ELLIPSE = bool(_ell_use)
    else:
        log.warning(f"  [椭圆] manifest 无椭圆参数,沿用转换器默认 "
                    f"cx={ELLIPSE_CX:.1f} cy={ELLIPSE_CY:.1f} a={ELLIPSE_A:.1f} b={ELLIPSE_B:.1f} "
                    f"(若与 MATLAB 不一致会导致 0 内边界节点)")

    all_src_depth    = mani['all_src_depth'].astype(np.float64)
    backup_src_depth = mani['backup_src_depth'].astype(np.float64)
    all_freq_indices = mani['all_freq_indices'].ravel().astype(np.int64)
    backup_freq_idx  = mani['backup_freq_idx'].ravel().astype(np.int64)

    log.info(f"  all_src_depth.shape    = {all_src_depth.shape}  (期望 [N, 2])")
    log.info(f"  backup_src_depth.shape = {backup_src_depth.shape}")

    def _ensure_n2(arr, name):
        if arr.ndim == 2 and arr.shape[1] != 2 and arr.shape[0] == 2:
            log.warning(f"  {name} 仍反置 {arr.shape}，再次转置 → {arr.T.shape}")
            return arr.T
        return arr
    all_src_depth    = _ensure_n2(all_src_depth,    'all_src_depth')
    backup_src_depth = _ensure_n2(backup_src_depth, 'backup_src_depth')

    # ★ 读取并解析 split_info
    split_info_list = parse_split_info(mani, NUM_FREQS)
    if split_info_list:
        log.info(f"  ✓ 读取到 split_info（{len(split_info_list)} 个频率段）")
        for si in split_info_list:
            log.info(f"    {si.get('freq','')} Hz: "
                     f"train_start={si.get('train_start','')} n_train={si.get('n_train','')} "
                     f"test_start={si.get('test_start','')} n_test={si.get('n_test','')}")
    else:
        if SPLIT_TRAIN_TEST:
            log.warning("  ⚠ --split_train_test 已启用，但 manifest 中无 split_info。"
                        "输出 HDF5 中将无分区元数据。")

    # 频率过滤 & 重映射
    mani_freqs = mani.get('selected_frequencies', None)
    if mani_freqs is not None:
        mani_freqs = np.atleast_1d(mani_freqs).ravel().astype(np.int64)
        matlab_fi_to_selected = {}
        for py_fi, freq in enumerate(SELECTED_FREQUENCIES):
            for mat_fi, mf in enumerate(mani_freqs):
                if mf == freq:
                    matlab_fi_to_selected[mat_fi] = py_fi
        log.info(f"  MATLAB频率: {mani_freqs.tolist()}  选中: {SELECTED_FREQUENCIES}")
        log.info(f"  freq_idx 映射: {matlab_fi_to_selected}")
    else:
        matlab_fi_to_selected = {fi: fi for fi in range(NUM_FREQS)}

    keep_mask = np.isin(all_freq_indices, list(matlab_fi_to_selected.keys()))
    all_src_depth    = all_src_depth[keep_mask]
    all_freq_indices = all_freq_indices[keep_mask]
    all_freq_indices = np.array(
        [matlab_fi_to_selected[int(fi)] for fi in all_freq_indices], dtype=np.int64)

    keep_bak = np.isin(backup_freq_idx, list(matlab_fi_to_selected.keys()))
    backup_src_depth = backup_src_depth[keep_bak]
    backup_freq_idx  = backup_freq_idx[keep_bak]
    backup_freq_idx  = np.array(
        [matlab_fi_to_selected[int(fi)] for fi in backup_freq_idx], dtype=np.int64)

    ACTUAL_SAMPLES = len(all_src_depth)
    if ACTUAL_SAMPLES != NUM_SAMPLES:
        log.warning(f"  清单实际样本数 {ACTUAL_SAMPLES} ≠ 期望 {NUM_SAMPLES}，以实际为准")
    NUM_SAMPLES           = ACTUAL_SAMPLES
    SAMPLES_PER_FREQUENCY = NUM_SAMPLES // NUM_FREQS
    log.info(f"  实际使用: 总样本={NUM_SAMPLES}  每频率≈{SAMPLES_PER_FREQUENCY}")
    log.info(f"  步骤1耗时: {_fmt_sec(time.time()-t_step)}")

    # ── 2. 读取网格文件 ────────────────────────────────────────────
    if args.mesh_file is not None:
        mat_file = os.path.join(args.mat_dir, args.mesh_file)
    else:
        mat_file = os.path.join(
            args.mat_dir,
            f"comsol_mesh_Lx{GRID_SIZE_X}_Ly{GRID_SIZE_Y}_H{H}.mat"
        )
    if not os.path.exists(mat_file):
        log.error(f"找不到网格文件: {mat_file}")
        exit()
    mesh_mat = load_mat(mat_file)
    log.info(f"成功读取网格: {mat_file}")

    p = mesh_mat['p_out'].astype(np.float64)

    # 网格节点加载后，用节点坐标做最终兜底确认
    # （若 manifest/mesh 字段已给出则保持，否则用坐标分布检测覆盖）
    domain_tag_final = infer_domain_shape(
        mani=mani, mesh_mat=mesh_mat, p_nodes=p
    )
    if domain_tag_final != domain_tag:
        log.info(f"  [domain 推断] 节点坐标兜底检测修正: "
                 f"'{domain_tag}' → '{domain_tag_final}'")
        domain_tag = domain_tag_final
    else:
        log.info(f"  [domain 推断] 节点坐标检测一致: '{domain_tag}' ✓")
    t = mesh_mat['t_out'].astype(np.int32) - 1

    if 'e' in mesh_mat:
        e = mesh_mat['e'].astype(np.int32) - 1
    elif 'e_out' in mesh_mat:
        e = mesh_mat['e_out'].astype(np.int32) - 1
    else:
        e = np.zeros((2, 0), dtype=np.int32)

    if 'B' in mesh_mat:
        B_raw = mesh_mat['B'].astype(np.int32)
    elif 'B_out' in mesh_mat:
        B_raw = mesh_mat['B_out'].astype(np.int32)
    else:
        raise KeyError(f"网格文件缺少边界矩阵 B/B_out: {mat_file}")

    B  = np.where(B_raw > 0, B_raw - 1, -1)
    N  = p.shape[1]
    Ne = t.shape[1]
    log.info(f"节点数: {N}, 单元数: {Ne}")

    # 探测 COMSOL DOF 数
    _batch_file_template = os.path.join(
        MATLAB_DIR,
        f'comsol_batch_Lx{GRID_SIZE_X}_Ly{GRID_SIZE_Y}_H{H}_f{SELECTED_FREQUENCIES[0]}Hz.mat'
    )
    # 兼容旧命名（v3 及以前）
    _batch_file_legacy = os.path.join(
        MATLAB_DIR, f'comsol_batch_f{SELECTED_FREQUENCIES[0]}Hz.mat'
    )
    _first_mat = _batch_file_template if os.path.exists(_batch_file_template) \
                 else _batch_file_legacy
    if os.path.exists(_first_mat):
        _d = load_mat(_first_mat)
        _K_shape = _d.get('K_shape', None)
        N_dof = int(np.atleast_1d(_K_shape).ravel()[0]) if _K_shape is not None else N
        if N_dof != N:
            log.warning(f"  COMSOL DOF={N_dof} ≠ 节点数={N} (P2单元)")
    else:
        N_dof = N

    # ── 步骤2: 读取 MATLAB 导出的节点索引（直接使用，不做坐标 snap）──
    t_step = time.time()
    log.info("\n步骤 2/5: 读取声源节点索引...")

    # MATLAB 导出的是 1-based int32，转为 0-based int64
    if 'all_src_node_idx' not in mani:
        raise KeyError(
            "manifest 中缺少 all_src_node_idx 字段。\n"
            "  请使用 data_generate_comsol_v5.m 重新生成数据集。"
        )
    source_node_indices = mani['all_src_node_idx'].ravel().astype(np.int64) - 1
    backup_node_indices = mani['bak_src_node_idx'].ravel().astype(np.int64) - 1

    # 过滤：只保留当前选中频率的索引（与坐标过滤同步）
    source_node_indices = source_node_indices[keep_mask]
    backup_node_indices = backup_node_indices[keep_bak]

    # 边界检查：索引须在 [0, N) 内
    if source_node_indices.min() < 0 or source_node_indices.max() >= N:
        raise ValueError(
            f"source_node_indices 越界: min={source_node_indices.min()} "
            f"max={source_node_indices.max()} N={N}"
        )

    # 唯一性断言：MATLAB 已保证，此处作为验证门禁，失败说明上游有 bug
    for fi, freq in enumerate(SELECTED_FREQUENCIES):
        mask_fi  = (all_freq_indices == fi)
        nodes_fi = source_node_indices[mask_fi]
        n_uniq   = len(np.unique(nodes_fi))
        if n_uniq < len(nodes_fi):
            raise RuntimeError(
                f"{freq} Hz 节点唯一性验证失败: "
                f"总样本={len(nodes_fi)}, 唯一节点={n_uniq}, "
                f"碰撞={len(nodes_fi)-n_uniq}。\n"
                f"  请检查 data_generate_comsol_v5.m 的采样逻辑。"
            )
        log.info(f"  {freq} Hz 节点唯一性 ✓ ({len(nodes_fi)} 样本 / {n_uniq} 唯一节点)")

    was_reused = False
    reuse_mode = 'generated'
    # 映射误差（源点坐标与网格节点坐标之差，理论上应为浮点精度量级）
    src_coords   = p[:, source_node_indices]          # [2, NUM_SAMPLES]
    coord_errors = np.sqrt(
        (all_src_depth[:, 0] - src_coords[0]) ** 2 +
        (all_src_depth[:, 1] - src_coords[1]) ** 2
    )
    max_err  = float(coord_errors.max())
    mean_err = float(coord_errors.mean())
    mapping_stats = {'max_error': max_err, 'mean_error': mean_err, 'errors': coord_errors}
    log.info(f"  坐标一致性校验: max_err={max_err:.2e} m  mean_err={mean_err:.2e} m")
    if max_err > 1e-4:
        log.warning(
            f"  [警告] 坐标误差 {max_err:.2e} m 超过预期浮点精度阈值 1e-4 m。\n"
            f"    可能原因：h5py 读取时发生了意外转置或类型转换。\n"
            f"    请检查 load_mat 对 all_src_depth / all_src_node_idx 的读取结果。"
        )

    x1, y1 = p[0, t[0]], p[1, t[0]]
    x2, y2 = p[0, t[1]], p[1, t[1]]
    x3, y3 = p[0, t[2]], p[1, t[2]]
    elem_areas_py = 0.5 * np.abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))

    gamma_upper, gamma_robin, gamma_wedge = get_boundary_node_indices(B)

    log.info(f"  步骤2耗时: {_fmt_sec(time.time()-t_step)}")

    # ── 步骤3: 读取 COMSOL 顶点级解 ─────────────────────────────────
    if rank == 0:
        log.info("\n步骤 3/5: 读取 COMSOL 顶点级解...")

    K_matrices_csc = {}
    U_batch_dict   = {}
    p_refs         = {}
    wavenumbers_dict = {}

    for fi, freq in enumerate(SELECTED_FREQUENCIES):
        # v4 命名优先，回退 v3 命名
        batch_v4 = os.path.join(
            MATLAB_DIR,
            f'comsol_batch_Lx{GRID_SIZE_X}_Ly{GRID_SIZE_Y}_H{H}_f{freq}Hz.mat'
        )
        batch_v3 = os.path.join(MATLAB_DIR, f'comsol_batch_f{freq}Hz.mat')
        mat_path = batch_v4 if os.path.exists(batch_v4) else batch_v3
        if not os.path.exists(mat_path):
            raise FileNotFoundError(f"找不到频率文件: {mat_path}")
        d = load_mat(mat_path)

        k_wave = float(mat_scalar(d['wavenumber']))
        A_p1 = assemble_p1_helmholtz_matrix(
            p, t, e, B, k_wave, C0,
            USE_ELLIPSE=USE_ELLIPSE,
            ELLIPSE_CX=ELLIPSE_CX, ELLIPSE_CY=ELLIPSE_CY,
            ELLIPSE_A=ELLIPSE_A, ELLIPSE_B=ELLIPSE_B,
        )
        K_matrices_csc[fi] = A_p1

        U_v = _to_complex128(np.asarray(d['U_vertex_batch']))
        U_batch_dict[fi] = U_v
        log.info(f"  [{fi+1}/{NUM_FREQS}] {freq}Hz: U_vertex={U_v.shape}")

        p_ref_val = complex(mat_scalar(d['p_ref_val']))
        if hasattr(d['p_ref_val'], 'dtype') and d['p_ref_val'].dtype.names:
            pv = d['p_ref_val'].ravel()[0]
            p_ref_val = complex(float(pv['real']), float(pv['imag']))
        p_refs[fi] = p_ref_val
        wavenumbers_dict[fi] = k_wave

    # ── 步骤4: 组装数据 ──────────────────────────────────────────────
    sample_indices_this_rank = [i for i in range(NUM_SAMPLES) if i % world_size == rank]
    if rank == 0:
        log.info(f"\n步骤 4/5: 组装顶点级数据 (总样本={NUM_SAMPLES})...")

    fem_solutions_all = np.zeros((NUM_SAMPLES, N), dtype=np.complex128)
    fem_tl_all        = np.zeros((NUM_SAMPLES, N), dtype=np.float64)
    solve_times_all   = np.zeros(NUM_SAMPLES, dtype=np.float64)
    validation_status_all:  dict = {}
    replaced_samples_all:   dict = {}
    total_invalid  = 0
    total_replaced = 0

    pbar = tqdm(sample_indices_this_rank, desc=f"GPU {rank}", position=rank, leave=True)
    t_global_start = time.time()
    for global_idx in pbar:
        fi   = int(all_freq_indices[global_idx])
        freq = SELECTED_FREQUENCIES[fi]
        p_ref = p_refs[fi]

        fgi  = np.where(all_freq_indices == fi)[0]
        isrc = int(np.searchsorted(fgi, global_idx))

        u_np = U_batch_dict[fi][isrc, :]
        tl_s = compute_tl(u_np, p_ref)
        fem_solutions_all[global_idx] = u_np
        fem_tl_all[global_idx]        = tl_s
        validation_status_all[global_idx] = 'valid'

        if global_idx < SAMPLES_TO_PLOT:
            sn    = int(source_node_indices[global_idx])
            s_pos = p[:, sn]
            plot_tl_comparison(p, t, tl_s, s_pos, global_idx, plot_dir, freq,
                               domain_shape=domain_tag)
        pbar.set_postfix({'sample': global_idx, 'f(Hz)': freq, 'status': 'OK'})

    pbar.close()
    t_elapsed = time.time() - t_global_start
    total_solve_time_all_gpus = float(np.sum(solve_times_all))

    valid_count = sum(1 for v in validation_status_all.values() if str(v) == 'valid')
    log.info(f"\n{'='*60}")
    log.info(f"GPU {rank}: 总={len(sample_indices_this_rank)} 有效={valid_count} "
             f"无效={total_invalid} 耗时={_fmt_sec(t_elapsed)}")
    log.info(f"{'='*60}")

    # ── all_gather ────────────────────────────────────────────────────
    if world_size > 1:
        dist.barrier()
        local_pkg = {
            'rank': rank,
            'fem_solutions':     {i: fem_solutions_all[i] for i in sample_indices_this_rank},
            'fem_tl':            {i: fem_tl_all[i]        for i in sample_indices_this_rank},
            'solve_times':       {i: float(solve_times_all[i]) for i in sample_indices_this_rank},
            'validation_status': {i: validation_status_all.get(i, 'valid')
                                  for i in sample_indices_this_rank},
            'replaced_samples':  {i: replaced_samples_all[i]
                                  for i in sample_indices_this_rank
                                  if i in replaced_samples_all},
            'timing_summary': {
                'total_solve_time':    total_solve_time_all_gpus,
                'total_analytical_time': 0.0,
                'invalid_samples':     total_invalid,
                'replaced_samples':    total_replaced,
            },
        }
        all_results = [None] * world_size
        dist.all_gather_object(all_results, local_pkg)
        dist.barrier()

        if rank == 0:
            total_invalid = total_replaced = 0
            total_solve_time_all_gpus = 0.0
            for pkg in all_results:
                for i, u   in pkg['fem_solutions'].items():  fem_solutions_all[i] = u
                for i, tl  in pkg['fem_tl'].items():         fem_tl_all[i] = tl
                for i, st  in pkg['solve_times'].items():    solve_times_all[i] = st
                validation_status_all.update(pkg['validation_status'])
                replaced_samples_all.update(pkg['replaced_samples'])
                ts = pkg['timing_summary']
                total_invalid  += ts.get('invalid_samples', 0)
                total_replaced += ts.get('replaced_samples', 0)
                total_solve_time_all_gpus += ts.get('total_solve_time', 0.0)
    else:
        log.info(f"  总无效={total_invalid}  总替换={total_replaced}")

    if rank != 0:
        if world_size > 1:
            dist.barrier()
            dist.destroy_process_group()
        return

    # ── 步骤5: 最终验证 + 保存 ──────────────────────────────────────
    log.info("\n步骤 5/5: 最终验证 + 保存...")
    final_invalid_count = 0
    for i in tqdm(range(NUM_SAMPLES), desc="最终验证"):
        has_inv, _, _ = check_nan_inf(fem_solutions_all[i])
        if has_inv:
            fem_solutions_all[i] = np.nan_to_num(
                fem_solutions_all[i], nan=0., posinf=0., neginf=0.)
            final_invalid_count += 1

    N_out = N
    analytical_tl_batch = fem_tl_all.copy()

    source_vectors_2ch     = np.zeros((NUM_SAMPLES, 2, N_out), dtype=np.float64)
    final_vectors_2ch      = np.zeros((NUM_SAMPLES, 2 * N_out), dtype=np.float64)
    analytical_vectors_2ch = np.zeros((NUM_SAMPLES, 2 * N_out), dtype=np.float64)

    for i in tqdm(range(NUM_SAMPLES), desc="格式化数据"):
        fi   = int(all_freq_indices[i])
        fgi  = np.where(all_freq_indices == fi)[0]
        isrc = int(np.searchsorted(fgi, i))
        src_pos = all_src_depth[i]

        F_src = _rebuild_gaussian_rhs(
            p, t, elem_areas_py, src_pos, wavenumbers_dict[fi],
            p_refs[fi], N, gamma_upper, H_GRID=float(args.H)
        )
        fem_clean = np.nan_to_num(fem_solutions_all[i], nan=0., posinf=0., neginf=0.)
        F_clean   = np.nan_to_num(F_src,               nan=0., posinf=0., neginf=0.)

        source_vectors_2ch[i, 0]  = F_clean.real
        source_vectors_2ch[i, 1]  = F_clean.imag
        final_vectors_2ch[i]      = np.concatenate([fem_clean.real, fem_clean.imag])
        analytical_vectors_2ch[i] = final_vectors_2ch[i]

    # 完整性检查
    all_data_valid = True
    for data, name in [
        (source_vectors_2ch,     "载荷向量"),
        (final_vectors_2ch,      "FEM解"),
    ]:
        has_inv, nan_c, inf_c = check_nan_inf(data)
        if has_inv:
            log.error(f"  ✗ {name}: 包含 {nan_c} NaN, {inf_c} Inf")
            all_data_valid = False
        else:
            log.info(f"  [OK] {name}: 无NaN/Inf")

    # ── 写 HDF5 ──────────────────────────────────────────────────────
    h5_path = os.path.join(output_dir, 'acoustic_dataset.h5')
    log.info(f"  HDF5路径: {h5_path}")
    t_h5 = time.time()

    source_positions_physical = all_src_depth
    backup_positions_physical = backup_src_depth
    freq_indices_arr          = all_freq_indices
    backup_freq_indices_arr   = backup_freq_idx
    solve_times_array         = solve_times_all
    analytical_times_array    = np.zeros(NUM_SAMPLES, dtype=np.float64)
    total_solve_time          = total_solve_time_all_gpus
    total_analytical_time     = 0.0

    with h5py.File(h5_path, 'w') as hf:
        # 网格
        hf.create_dataset('mesh/nodes',    data=p)
        hf.create_dataset('mesh/elements', data=t)
        hf.create_dataset('mesh/edges',    data=e)
        hf.create_dataset('mesh/boundary', data=B)

        # Helmholtz 矩阵
        mg = hf.create_group('matrices')
        for fi, freq in enumerate(SELECTED_FREQUENCIES):
            A_csc = K_matrices_csc[fi].tocsc()
            fg    = mg.create_group(f'freq_{freq}Hz')
            fg.create_dataset('A_data',    data=A_csc.data)
            fg.create_dataset('A_indices', data=A_csc.indices)
            fg.create_dataset('A_indptr',  data=A_csc.indptr)
            fg.create_dataset('A_shape',   data=np.array(A_csc.shape, dtype=np.int64))
            fg.attrs['frequency']  = freq
            fg.attrs['wavenumber'] = wavenumbers_dict[fi]

        # 样本数据
        hf.create_dataset('source_positions_physical', data=source_positions_physical)
        hf.create_dataset('backup_positions_physical', data=backup_positions_physical)
        hf.create_dataset('source_node_indices',       data=source_node_indices)
        hf.create_dataset('backup_node_indices',       data=backup_node_indices)
        hf.create_dataset('source_positions',
                          data=p[:, source_node_indices].T)
        hf.create_dataset('frequency_indices',         data=freq_indices_arr)
        hf.create_dataset('backup_frequency_indices',  data=backup_freq_indices_arr)

        # 映射误差
        mmg = hf.create_group('mapping_statistics')
        mmg.attrs['max_error']  = mapping_stats['max_error']
        mmg.attrs['mean_error'] = mapping_stats['mean_error']
        mmg.create_dataset('errors', data=mapping_stats['errors'])

        # ★ v2 新增：split_info 写入 HDF5
        if split_info_list:
            sg = hf.create_group('split_info')
            for si in split_info_list:
                freq_key = f"freq_{int(si.get('freq', 0))}Hz"
                fg_si    = sg.create_group(freq_key)
                for k, v in si.items():
                    fg_si.attrs[k] = v
            hf.attrs['has_split_info'] = 1
            hf.attrs['split_train_test'] = int(SPLIT_TRAIN_TEST)
            if TRAIN_MAX_X is not None:
                hf.attrs['train_max_x'] = TRAIN_MAX_X
            if TRAIN_MAX_Y is not None:
                hf.attrs['train_max_y'] = TRAIN_MAX_Y
        else:
            hf.attrs['has_split_info'] = 0

        # 验证信息
        vg = hf.create_group('validation_info')
        vg.attrs['total_invalid_samples']   = total_invalid
        vg.attrs['total_replaced_samples']  = total_replaced
        vg.attrs['backup_ratio']            = BACKUP_RATIO
        vg.attrs['reference_solution_type'] = 'FEM'
        status_strs = [f"{k}:{v}" for k, v in validation_status_all.items()]
        vg.create_dataset('validation_status', data=np.array(status_strs, dtype='S'))
        if replaced_samples_all:
            vg.attrs['replacement_details'] = json.dumps(replaced_samples_all)

        # 时间统计
        tg = hf.create_group('timing_statistics')
        tg.create_dataset('solve_times_per_sample',      data=solve_times_array)
        tg.create_dataset('analytical_times_per_sample', data=analytical_times_array)
        tg.attrs['total_solve_time']       = total_solve_time
        tg.attrs['total_analytical_time']  = total_analytical_time
        pos_mask = solve_times_array > 0
        tg.attrs['avg_solve_time'] = (
            float(np.mean(solve_times_array[pos_mask])) if pos_mask.any() else 0.0)
        tg.attrs['avg_analytical_time'] = 0.0
        tg.attrs['num_gpus'] = world_size

        # TL + 向量
        hf.create_dataset('fem_tl',         data=fem_tl_all)
        hf.create_dataset('analytical_tl',  data=analytical_tl_batch)
        hf.create_dataset('source_vectors',      data=source_vectors_2ch)
        hf.create_dataset('final_vectors',       data=final_vectors_2ch)
        hf.create_dataset('analytical_vectors',  data=analytical_vectors_2ch)

        # 元数据
        hf.attrs['num_samples']           = NUM_SAMPLES
        hf.attrs['samples_per_frequency'] = SAMPLES_PER_FREQUENCY
        hf.attrs['num_nodes']             = N
        hf.attrs['num_elements']          = Ne
        hf.attrs['num_frequencies']       = NUM_FREQS
        hf.attrs['selected_frequencies']  = SELECTED_FREQUENCIES
        hf.attrs['speed_of_sound']        = C0
        hf.attrs['amplitude']             = AMP
        hf.attrs['wedge_angle']           = WEDGE_ANGLE
        hf.attrs['grid_size_x']           = GRID_X
        hf.attrs['grid_size_y']           = GRID_Y
        hf.attrs['grid_resolution_H']     = float(args.H)
        hf.attrs['use_ellipse_inner_boundary'] = int(USE_ELLIPSE)
        if USE_ELLIPSE:
            hf.attrs['ellipse_cx'] = ELLIPSE_CX
            hf.attrs['ellipse_cy'] = ELLIPSE_CY
            hf.attrs['ellipse_a']  = ELLIPSE_A
            hf.attrs['ellipse_b']  = ELLIPSE_B
        hf.attrs['reference_solution_type'] = reference_solution_type
        hf.attrs['num_gpus_used']           = world_size
        hf.attrs['source_positions_reused'] = was_reused
        hf.attrs['reuse_mode']              = reuse_mode
        hf.attrs['source_coordinate_type']  = 'physical'
        hf.attrs['domain_shape']            = domain_tag
        hf.attrs['mesh_file']               = os.path.basename(mat_file)
        hf.attrs['manifest_file']           = os.path.basename(manifest_path)

    log.info(f"数据已保存: {h5_path}  ({_fmt_sec(time.time()-t_h5)})")

    # ── 保存源点 .npy（★ v2：文件名含 split 标识）────────────────────
    npy_name = (
        f"source_positions_physical"
        f"_x{GRID_SIZE_X}_y{GRID_SIZE_Y}_H{H}"
        f"_f{freq_str}"
        f"{split_tag}.npy"
    )
    npy_path = os.path.join(output_dir, npy_name)
    note_str = (f"求解后最终版本(替换{total_replaced}个无效源点)"
                if total_replaced > 0
                else "COMSOL generated, y=0 surface, y=Ly seabed")
    save_source_positions_physical(
        npy_path,
        source_positions_physical,
        backup_positions_physical,
        freq_indices_arr,
        backup_freq_indices_arr,
        GRID_SIZE_X, GRID_SIZE_Y,
        SAMPLES_PER_FREQUENCY, NUM_FREQS,
        SELECTED_FREQUENCIES,
        args.H,
        split_info_list=split_info_list,
        note=note_str,
    )

    # ── timing_statistics.json ────────────────────────────────────────
    timing_stats_file = os.path.join(output_dir, 'timing_statistics.json')
    pos_mask = solve_times_array > 0
    timing_stats = {
        'total_samples':        NUM_SAMPLES,
        'num_gpus':             world_size,
        'grid_resolution_H':    float(args.H),
        'selected_frequencies': SELECTED_FREQUENCIES,
        'overall': {
            'total_solve_time_seconds':      float(total_solve_time),
            'total_analytical_time_seconds': 0.0,
            'avg_solve_time_ms':    float(np.mean(solve_times_array[pos_mask])*1000) if pos_mask.any() else 0.0,
            'avg_analytical_time_ms': 0.0,
            'median_solve_time_ms': float(np.median(solve_times_array[pos_mask])*1000) if pos_mask.any() else 0.0,
            'std_solve_time_ms':    float(np.std(solve_times_array[pos_mask])*1000) if pos_mask.any() else 0.0,
            'min_solve_time_ms':    float(np.min(solve_times_array[pos_mask])*1000) if pos_mask.any() else 0.0,
            'max_solve_time_ms':    float(np.max(solve_times_array[pos_mask])*1000) if pos_mask.any() else 0.0,
            'throughput_samples_per_second':
                float(NUM_SAMPLES / total_solve_time) if total_solve_time > 0 else 0.0,
        },
        'per_frequency': {},
    }
    for fi, freq in enumerate(SELECTED_FREQUENCIES):
        mask = (freq_indices_arr == fi)
        ft   = solve_times_array[mask]
        ft_p = ft[ft > 0]
        timing_stats['per_frequency'][str(freq)] = {
            'num_samples':       int(mask.sum()),
            'avg_solve_time_ms': float(np.mean(ft_p)*1000) if len(ft_p) else 0.0,
            'median_solve_time_ms': float(np.median(ft_p)*1000) if len(ft_p) else 0.0,
            'std_solve_time_ms':    float(np.std(ft_p)*1000) if len(ft_p) else 0.0,
        }
    with open(timing_stats_file, 'w') as jf:
        json.dump(timing_stats, jf, indent=2)
    log.info(f"时间统计已保存: {timing_stats_file}")

    # ── 最终汇总 ─────────────────────────────────────────────────────
    t_total_elapsed = time.time() - t_program_start
    plot_count = len([f for f in os.listdir(plot_dir) if f.endswith('.png')])
    log.info("\n" + "=" * 70)
    log.info("数据集生成完成!")
    log.info("=" * 70)
    log.info(f"总样本数: {NUM_SAMPLES}")
    log.info(f"每个频率样本数: {SAMPLES_PER_FREQUENCY}")
    for fi, freq in enumerate(SELECTED_FREQUENCIES):
        cnt  = int((freq_indices_arr == fi).sum())
        uniq = len(np.unique(source_node_indices[freq_indices_arr == fi]))
        log.info(f"  {freq} Hz: {cnt} 样本, {uniq} 个唯一节点")
    if split_info_list:
        log.info("训练/测试分区（来自 manifest split_info）:")
        for si in split_info_list:
            log.info(f"  {si.get('freq','')} Hz: "
                     f"训练={si.get('n_train','')} (start={si.get('train_start','')}) "
                     f"测试={si.get('n_test','')} (start={si.get('test_start','')}) "
                     f"训练备={si.get('n_bak_train','?')} 测试备={si.get('n_bak_test','?')}")
    log.info(f"程序总运行时间: {_fmt_sec(t_total_elapsed)}")
    log.info(f"输出目录: {output_dir}")
    log.info(f"HDF5: {h5_path}")
    log.info(f"NPY: {npy_path}")
    log.info(f"对比图: {plot_dir}/ ({plot_count} 个)")
    log.info(f"日志: {log_path}")
    log.info("=" * 70)

    if world_size > 1:
        dist.barrier()
        dist.destroy_process_group()


if __name__ == '__main__':
    main()