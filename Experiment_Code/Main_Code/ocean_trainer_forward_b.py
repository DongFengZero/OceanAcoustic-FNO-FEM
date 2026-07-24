import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, Subset, Sampler
from torch.optim.lr_scheduler import StepLR
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from tqdm import tqdm
import os
import argparse
from datetime import datetime
import json
from sklearn.model_selection import StratifiedShuffleSplit
from deq_modules.models import *
from scipy.sparse import csc_matrix
import scipy.sparse
import time
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler
import socket

# ==================== 模块级日志工具 ====================
import sys as _sys
import logging as _logging

# 全局日志文件句柄（由 _setup_file_logging 在 output_dir 就绪后设置）。
# 在此之前 _log 只写 stdout + 内存缓冲；文件就绪后缓冲一次性回放并落盘，
# 从而把「执行命令 + 全部参数 + Trainer 创建前的全部输出」都完整保存。
_LOG_FILE_PATH = None
_LOG_BUFFER = []          # output_dir 就绪前的输出缓冲
_LOG_BUFFER_ENABLED = True

def _log(msg: str = "") -> None:
    """模块级日志：输出到 stdout，并写入日志文件（文件未就绪时先缓冲）。"""
    text = str(msg)
    print(text)
    global _LOG_BUFFER_ENABLED
    if _LOG_FILE_PATH is not None:
        try:
            with open(_LOG_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(text + '\n')
        except Exception:
            pass
    elif _LOG_BUFFER_ENABLED:
        _LOG_BUFFER.append(text)

def _setup_file_logging(output_dir: str, header_lines=None) -> str:
    """在 output_dir 就绪后创建统一日志文件，回放此前缓冲的所有输出。

    header_lines: 可选，最先写入文件的若干行（如执行命令、参数、时间戳）。
    返回日志文件绝对路径；供 Trainer 复用同一文件。
    """
    global _LOG_FILE_PATH, _LOG_BUFFER, _LOG_BUFFER_ENABLED
    log_dir = os.path.join(output_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(
        log_dir, f'full_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    with open(path, 'w', encoding='utf-8') as f:
        if header_lines:
            for ln in header_lines:
                f.write(str(ln) + '\n')
        # 回放缓冲：Trainer 创建前的全部 _log 输出
        for ln in _LOG_BUFFER:
            f.write(ln + '\n')
    _LOG_FILE_PATH = path
    _LOG_BUFFER = []
    _LOG_BUFFER_ENABLED = False
    return path

def _build_run_header(argv) -> list:
    """构造运行头信息：时间戳 + 完整执行命令 + 逐项参数。"""
    lines = []
    lines.append("=" * 70)
    lines.append(f"运行开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"工作目录: {os.getcwd()}")
    # 完整执行命令（尽量还原为可复制的命令行）
    try:
        import shlex
        cmd = ' '.join(shlex.quote(a) for a in ([_sys.executable] + list(argv)))
    except Exception:
        cmd = ' '.join([_sys.executable] + list(argv))
    lines.append("执行命令:")
    lines.append(f"  {cmd}")
    lines.append("=" * 70)
    return lines
# =========================================================


    
def find_free_port():
    """查找可用端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def setup_distributed():
    """
    初始化分布式训练环境
    自动检测可用GPU数量并配置
    支持三种启动方式：
    1. torchrun/torch.distributed.launch (推荐)
    2. 手动设置环境变量
    3. 单机多卡自动配置
    """
    # 检查是否通过 torchrun 或 torch.distributed.launch 启动
    if 'RANK' in os.environ and 'WORLD_SIZE' in os.environ:
        # 方式1: 标准分布式启动
        rank = int(os.environ["RANK"])
        world_size = int(os.environ['WORLD_SIZE'])
        local_rank = int(os.environ.get('LOCAL_RANK', 0))
        
        _log(f"[检测] 通过分布式启动器启动: Rank={rank}, World={world_size}, Local={local_rank}")
        
    elif 'LOCAL_RANK' in os.environ:
        # 方式2: 只有 LOCAL_RANK (某些启动器)
        local_rank = int(os.environ['LOCAL_RANK'])
        world_size = torch.cuda.device_count()
        rank = local_rank
        
        _log(f"[检测] 检测到LOCAL_RANK: Rank={rank}, World={world_size}")
        
    else:
        # 方式3: 单机多卡手动配置
        if not torch.cuda.is_available():
            raise RuntimeError("分布式训练需要GPU支持")
        
        world_size = torch.cuda.device_count()
        
        if world_size <= 1:
            raise RuntimeError(f"分布式训练需要多于1个GPU，当前检测到 {world_size} 个GPU")
        
        # 手动设置环境变量
        rank = 0  # 主进程
        local_rank = 0
        
        # 设置必需的环境变量
        os.environ['MASTER_ADDR'] = 'localhost'
        os.environ['MASTER_PORT'] = str(find_free_port())
        os.environ['RANK'] = str(rank)
        os.environ['LOCAL_RANK'] = str(local_rank)
        os.environ['WORLD_SIZE'] = str(world_size)
        
        _log(f"[配置] 手动配置单机多卡环境:")
        _log(f"  - MASTER_ADDR: {os.environ['MASTER_ADDR']}")
        _log(f"  - MASTER_PORT: {os.environ['MASTER_PORT']}")
        _log(f"  - WORLD_SIZE: {world_size}")
        _log(f"  - 当前进程: Rank={rank}")
        _log(f"\n[警告] 手动启动只能使用单进程！")
        _log(f"[建议] 使用以下命令启动多进程训练:")
        _log(f"  torchrun --nproc_per_node={world_size} {' '.join(sys.argv)}")
        
        # 对于手动启动，不能真正使用多卡，返回单卡配置
        world_size = 1
        rank = 0
        local_rank = 0
        _log(f"\n[回退] 使用单GPU模式: GPU {local_rank}")
    
    # 设置当前进程使用的GPU
    torch.cuda.set_device(local_rank)
    gpu = local_rank
    
    # 只有在真正的多进程环境下才初始化进程组
    if world_size > 1:
        try:
            # 初始化进程组
            dist.init_process_group(
                backend='nccl',  # NVIDIA GPU使用nccl
                init_method='env://',
                world_size=world_size,
                rank=rank
            )
            
            # 同步所有进程
            dist.barrier()
            
            _log(f"[成功] GPU {rank}/{world_size} 初始化完成")
            
        except Exception as e:
            _log(f"[错误] 分布式初始化失败: {e}")
            _log(f"[回退] 使用单GPU模式")
            world_size = 1
            rank = 0
    
    return rank, world_size, gpu

def cleanup_distributed():
    """清理分布式训练环境"""
    if dist.is_initialized():
        dist.destroy_process_group()
    

#--------------------梯度处理---------------------
from scipy.special import hankel1
import hashlib
from pathlib import Path
def unique_xy_keep_order(x_vals: torch.Tensor) -> torch.Tensor:
    """
    对输入的 [N, 2] 形状的坐标张量进行去重 (适用于 PyTorch 1.11+)。
    """
    if x_vals.dim() != 2 or x_vals.size(1) != 2:
        raise ValueError("输入张量 x_vals 必须是 [N, 2] 的形状。")

    # torch.unique(dim=0) 直接按行去重。
    # ⚠️ 检查你的 PyTorch 版本是否支持 dim 参数。
    unique_coords = torch.unique(x_vals, dim=0)
    
    return unique_coords
        
def _get_mask_cache_path(num_points: int, keep_ratio: float, 
                        cache_dir: str, seed: int = 42) -> str:
    """生成mask缓存文件路径"""
    os.makedirs(cache_dir, exist_ok=True)
    filename = f"mask_n{num_points}_r{keep_ratio:.4f}_s{seed}.pt"
    return os.path.join(cache_dir, filename)


def create_fixed_mask(num_points: int, keep_ratio: float = 0.1, 
                     device=None, cache_dir: str = "./mask_cache", 
                     use_cache: bool = False, seed: int = 42):
    """
    创建固定的mask，使用均匀随机挑选，带本地缓存机制
    
    Args:
        num_points: 点的数量
        keep_ratio: 保留的比例，默认0.05
        device: torch设备，默认为cpu
        cache_dir: 缓存目录，默认为"./mask_cache"
        use_cache: 是否使用缓存，默认False
        seed: 随机种子，确保可重复性，默认42
    
    Returns:
        mask张量 [num_points]，随机选择keep_ratio*num_points个位置为1，其余为0
    
    Example:
        >>> mask = create_fixed_mask(1000, keep_ratio=0.05, seed=42)
        >>> # 第二次调用会从本地缓存加载（如果use_cache=True）
        >>> mask = create_fixed_mask(1000, keep_ratio=0.05, use_cache=True, seed=42)
    """
    if device is None:
        device = torch.device('cpu')
    
    cache_file = _get_mask_cache_path(num_points, keep_ratio, cache_dir, seed)
    
    # 尝试从缓存加载
    if use_cache and os.path.exists(cache_file):
        try:
            mask = torch.load(cache_file, map_location=device, weights_only=True)
            _log(f"Loaded mask from cache: {cache_file}")
            return mask
        except Exception as e:
            _log(f"Failed to load cache, creating new mask: {e}")
    
    # 创建新的mask - 使用均匀随机挑选
    num_keep = max(1, int(num_points * keep_ratio))
    
    # 设置随机种子以确保可重复性
    generator = torch.Generator(device='cpu')
    generator.manual_seed(seed)
    
    # 随机选择索引
    indices = torch.randperm(num_points, generator=generator)[:num_keep]
    
    # 创建mask
    mask = torch.zeros(num_points, device=device)
    mask[indices] = 1.0
    
    # 保存到缓存
    if use_cache:
        try:
            os.makedirs(cache_dir, exist_ok=True)
            # 保存到CPU以便跨设备使用
            torch.save(mask.cpu(), cache_file)
            _log(f"Saved mask to cache: {cache_file}")
        except Exception as e:
            _log(f"Failed to save cache: {e}")
    
    return mask


def apply_mask_to_batch(tensor: torch.Tensor, keep_ratio: float = 0.1, 
                       cache_dir: str = "./mask_cache", use_cache: bool = True):
    """
    对batch张量应用mask，保留keep_ratio的元素，其他置0
    
    Args:
        tensor: 输入张量 [batch_size, num_points]
        keep_ratio: 保留的比例，默认0.05
        cache_dir: 缓存目录
        use_cache: 是否使用缓存
    
    Returns:
        masked后的张量 [batch_size, num_points]
    
    Example:
        >>> x = torch.randn(4, 1000)
        >>> masked_x = apply_mask_to_batch(x, keep_ratio=0.05)
        >>> print((masked_x != 0).sum(dim=1))  # 每个样本保留50个元素
    """
    batch_size, num_points = tensor.shape
    
    # 获取或创建mask（带缓存）
    mask = create_fixed_mask(num_points, keep_ratio, tensor.device, 
                            cache_dir, use_cache)
    
    # 扩展mask到batch维度并应用
    masked_tensor = tensor * mask.unsqueeze(0)
    
    return masked_tensor


def clear_mask_cache(cache_dir: str = "./mask_cache"):
    """
    清除所有mask缓存文件
    
    Args:
        cache_dir: 缓存目录
    """
    if os.path.exists(cache_dir):
        cache_files = list(Path(cache_dir).glob("mask_*.pt"))
        for file in cache_files:
            os.remove(file)
            _log(f"Removed cache file: {file}")
        _log(f"Cleared {len(cache_files)} cache files")
    else:
        _log(f"Cache directory does not exist: {cache_dir}")


def list_cached_masks(cache_dir: str = "./mask_cache"):
    """
    列出所有缓存的mask
    
    Args:
        cache_dir: 缓存目录
    
    Returns:
        缓存文件列表
    """
    if not os.path.exists(cache_dir):
        _log(f"Cache directory does not exist: {cache_dir}")
        return []
    
    cache_files = list(Path(cache_dir).glob("mask_*.pt"))
    _log(f"Found {len(cache_files)} cached masks:")
    for file in cache_files:
        size_kb = os.path.getsize(file) / 1024
        _log(f"  - {file.name} ({size_kb:.2f} KB)")
    
    return cache_files

class TLComputation(torch.autograd.Function):
    """
    自定义可微分TL计算算子
    前向：完全使用参考函数的逻辑
    反向：手动计算梯度
    """
    
    @staticmethod
    def forward(ctx, u_real, u_imag, amp=None):
        """
        u_real, u_imag: torch tensor (GPU, float32)
        amp: scalar (可以是实数或复数), 参考压力幅值
        返回: TL (torch tensor, GPU, float32)
        """
        # 参数验证
        if amp is None:
            amp = 1.0
        
        # 1) 转到CPU，用float64计算
        u_real_np = u_real.detach().cpu().numpy().astype(np.float64)
        u_imag_np = u_imag.detach().cpu().numpy().astype(np.float64)
        
        # 2) 构造复数压力场
        pressure = u_real_np + 1j * u_imag_np
        
        # 3) 计算TL，与数据生成端 TL_MAX=200 dB 约定一致：
        #    -Inf (p=0节点) → -200 dB，+Inf / NaN → 0.0
        _TL_MAX = 200.0
        with np.errstate(divide='ignore', invalid='ignore'):
            TL = 20 * np.log10(np.abs(pressure / amp))
        TL = np.where(np.isneginf(TL), -_TL_MAX, TL)
        TL = np.where(np.isposinf(TL),     0.0,  TL)
        TL = np.where(np.isnan(TL),         0.0,  TL)
        
        # 4) 保存用于反向传播的变量
        ctx.save_for_backward(u_real, u_imag)
        
        # 计算并保存 |u| 用于梯度计算
        u_mag = np.abs(pressure)
        ctx.u_mag = torch.from_numpy(u_mag).double().to(u_real.device)
        
        # 5) 转回GPU float32
        tl_torch = torch.from_numpy(TL.real).double().to(u_real.device)
        
        return tl_torch
    
    @staticmethod
    def backward(ctx, grad_output):
        """
        计算梯度: dL/d(u_real), dL/d(u_imag)
        
        TL = -20*log10(amp/|u|) = -20*log10(amp) + 20*log10(|u|)
        
        其中 |u|² = u_real² + u_imag²
        
        d(TL)/d(u_real) = 20/(ln(10)) * d(ln(|u|))/d(u_real)
                        = 20/(ln(10)) * 1/|u| * d|u|/d(u_real)
                        = 20/(ln(10)) * 1/|u| * u_real/|u|
                        = 20/(ln(10)*|u|²) * u_real
        
        同理: d(TL)/d(u_imag) = 20/(ln(10)*|u|²) * u_imag
        """
        u_real, u_imag = ctx.saved_tensors
        u_mag = ctx.u_mag
        
        # 常数: 20 / ln(10) ≈ 8.68588964
        GRAD_SCALE = 20.0 / np.log(10)
        
        # 计算 |u|²，添加小的epsilon避免除零
        # 使用更合理的epsilon：相对于幅值的量级
        u_mag_sq = u_mag.square()
        
        # 创建有效掩码：只对 |u| > 0 的位置计算梯度
        # 这样可以避免在 TL=0 的位置产生无意义的梯度
        valid_mask = u_mag > 1e-10
        
        # 初始化梯度为零
        grad_u_real = torch.zeros_like(u_real)
        grad_u_imag = torch.zeros_like(u_imag)
        
        if valid_mask.any():
            # 只在有效位置计算梯度
            # 添加小的epsilon避免数值问题，但只在需要的地方
            u_mag_sq_safe = torch.where(
                valid_mask,
                u_mag_sq + 1e-20,  # 非常小的值，只是为了数值稳定
                torch.ones_like(u_mag_sq)  # 无效位置填充1（不会被使用）
            )
            
            # 计算梯度系数
            coeff = GRAD_SCALE / u_mag_sq_safe
            
            # 自适应梯度裁剪：基于输入的量级
            # 避免硬编码的裁剪阈值
            max_coeff = 1e6 / (u_real.abs().mean() + 1e-8)
            coeff = torch.clamp(coeff, max=max_coeff)
            
            # 只在有效位置应用梯度
            coeff_masked = torch.where(valid_mask, coeff, torch.zeros_like(coeff))
            
            # 计算最终梯度
            grad_base = grad_output * coeff_masked
            grad_u_real = grad_base * u_real
            grad_u_imag = grad_base * u_imag
            
            # 最后的安全检查：确保梯度有限
            grad_u_real = torch.nan_to_num(grad_u_real, nan=0.0, posinf=0.0, neginf=0.0)
            grad_u_imag = torch.nan_to_num(grad_u_imag, nan=0.0, posinf=0.0, neginf=0.0)
        return grad_u_real, grad_u_imag, None  # amp不需要梯度


# 使用方法
tl_computation_autograd = TLComputation.apply

    
    
# ==================== 自定义采样器:按频率分组 ====================
class FrequencyGroupedSampler(Sampler):
    """
    确保每个batch中的样本具有相同的频率索引
    """
    def __init__(self, frequency_indices, batch_size, shuffle=True):
        """
        Args:
            frequency_indices: numpy array or list, 每个样本的频率索引
            batch_size: int, 批大小
            shuffle: bool, 是否打乱数据
        """
        self.frequency_indices = np.array(frequency_indices)
        self.batch_size = batch_size
        self.shuffle = shuffle
        
        # 按频率分组样本索引
        self.freq_to_indices = {}
        for idx, freq_idx in enumerate(self.frequency_indices):
            if freq_idx not in self.freq_to_indices:
                self.freq_to_indices[freq_idx] = []
            self.freq_to_indices[freq_idx].append(idx)
        
        # 为每个频率创建批次
        self.batches = []
        for freq_idx, indices in self.freq_to_indices.items():
            indices = np.array(indices)
            if self.shuffle:
                np.random.shuffle(indices)
            
            # 将该频率的样本分成多个batch
            for i in range(0, len(indices), self.batch_size):
                batch = indices[i:i + self.batch_size].tolist()
                self.batches.append(batch)
        
        # 打乱batch顺序(但batch内样本频率仍相同)
        if self.shuffle:
            np.random.shuffle(self.batches)
    
    def __iter__(self):
        # 重新打乱
        if self.shuffle:
            for freq_idx in self.freq_to_indices.keys():
                np.random.shuffle(self.freq_to_indices[freq_idx])
            
            self.batches = []
            for freq_idx, indices in self.freq_to_indices.items():
                for i in range(0, len(indices), self.batch_size):
                    batch = indices[i:i + self.batch_size]
                    self.batches.append(batch)
            
            np.random.shuffle(self.batches)
        
        for batch in self.batches:
            yield batch
    
    def __len__(self):
        return len(self.batches)
class DistributedFrequencyGroupedSampler(Sampler):
    """
    分布式版本的频率分组采样器
    确保：
    1. 每个batch中样本频率相同
    2. 数据在多GPU间均匀分布
    3. 每个epoch数据打乱但可复现
    """
    def __init__(self, frequency_indices, batch_size, num_replicas=None, 
                 rank=None, shuffle=True, seed=0):
        """
        Args:
            frequency_indices: 每个样本的频率索引
            batch_size: 批大小
            num_replicas: GPU数量
            rank: 当前GPU编号
            shuffle: 是否打乱
            seed: 随机种子
        """
        if num_replicas is None:
            if not dist.is_available():
                raise RuntimeError("需要分布式包支持")
            num_replicas = dist.get_world_size()
        if rank is None:
            if not dist.is_available():
                raise RuntimeError("需要分布式包支持")
            rank = dist.get_rank()
        
        self.frequency_indices = np.array(frequency_indices)
        self.batch_size = batch_size
        self.num_replicas = num_replicas
        self.rank = rank
        self.epoch = 0
        self.shuffle = shuffle
        self.seed = seed
        
        # 按频率分组样本索引
        self.freq_to_indices = {}
        for idx, freq_idx in enumerate(self.frequency_indices):
            if freq_idx not in self.freq_to_indices:
                self.freq_to_indices[freq_idx] = []
            self.freq_to_indices[freq_idx].append(idx)
        
        # 为每个频率创建批次
        self.all_batches = []
        for freq_idx, indices in self.freq_to_indices.items():
            indices = np.array(indices)
            
            # 将该频率的样本分成多个batch
            for i in range(0, len(indices), self.batch_size):
                batch = indices[i:i + self.batch_size].tolist()
                self.all_batches.append(batch)  # 不再丢弃不完整batch
        
        # 计算每个GPU应处理的batch数（向上取整保证覆盖所有数据）
        self.num_samples = int(np.ceil(len(self.all_batches) / self.num_replicas))
        self.total_size = self.num_samples * self.num_replicas
    
    def __iter__(self):
        # 设置随机种子（epoch变化确保每个epoch打乱方式不同）
        if self.shuffle:
            g = torch.Generator()
            g.manual_seed(self.seed + self.epoch)
            indices = torch.randperm(len(self.all_batches), generator=g).tolist()
            batches = [self.all_batches[i] for i in indices]
        else:
            batches = list(self.all_batches)
        
        num_real = len(batches)  # 记录真实batch数量
        
        # 填充到total_size（确保所有GPU处理相同数量的batch）
        original_batches = list(batches)
        while len(batches) < self.total_size:
            batches.append(original_batches[len(batches) % len(original_batches)])
        assert len(batches) == self.total_size
        
        # 标记每个batch是否为填充（True=真实，False=填充）
        is_real = [i < num_real for i in range(self.total_size)]
        
        # 为当前GPU选择对应的batch
        my_batches = [batches[i] for i in range(self.rank, self.total_size, self.num_replicas)]
        my_is_real = [is_real[i] for i in range(self.rank, self.total_size, self.num_replicas)]
        assert len(my_batches) == self.num_samples
        
        # 保存当前epoch的填充标记，供外部查询
        self._batch_is_real = my_is_real
        self._current_batch_idx = 0
        
        for batch in my_batches:
            yield batch
    
    def is_current_batch_real(self):
        """返回当前batch是否为真实数据（非填充）"""
        if not hasattr(self, '_batch_is_real'):
            return True
        idx = self._current_batch_idx
        self._current_batch_idx += 1
        if idx < len(self._batch_is_real):
            return self._batch_is_real[idx]
        return True
    
    def __len__(self):
        return self.num_samples
    
    def set_epoch(self, epoch):
        """
        设置当前epoch（用于打乱数据）
        必须在每个epoch开始前调用
        """
        self.epoch = epoch
        
# ==================== 数据集加载器 ====================
class AcousticDataset(Dataset):
    def __init__(self, h5_path, edge_index, edge_attr):
        with h5py.File(h5_path, 'r') as f:
            # 加载样本数据
            self.source_vectors = torch.from_numpy(f['source_vectors'][:]).double()  # (N, 2, num_nodes)
            self.fem_sol_vectors = torch.from_numpy(f['final_vectors'][:]).double()
            # p=0 节点处 TL = 20·log10(0) = -Inf，截断为 -200 dB（与数据生成端 TL_MAX 一致）
            _TL_MAX = 200.0
            def _sanitize_tl(arr: np.ndarray) -> torch.Tensor:
                t = torch.from_numpy(arr).double()
                t = torch.where(torch.isneginf(t), torch.full_like(t, -_TL_MAX), t)
                t = torch.nan_to_num(t, nan=0.0, posinf=0.0, neginf=-_TL_MAX)
                return t
            self.fem_tl        = _sanitize_tl(f['fem_tl'][:])        # (N, num_nodes)
            self.analytical_tl = _sanitize_tl(f['analytical_tl'][:]) # (N, num_nodes)
            self.analytical_vectors = torch.from_numpy(f['analytical_vectors'][:]).double()
            self.source_positions = torch.from_numpy(f['source_positions'][:]).double()
            self.frequency_indices = torch.from_numpy(f['frequency_indices'][:]).long()
            
            # 加载网格
            self.nodes = torch.from_numpy(f['mesh/nodes'][:]).double()
            self.elements = torch.from_numpy(f['mesh/elements'][:]).long()
            
            # 加载元数据
            self.num_nodes = f.attrs['num_nodes']
            self.num_frequencies = f.attrs['num_frequencies']
            self.selected_frequencies = f.attrs['selected_frequencies']
            self.amplitude = f.attrs['amplitude']
            
            # 加载所有频率的A矩阵数据（实化后的边属性）
            self.A_coo_data_dict = edge_attr
            
            # ===== 新增：加载原始复数矩阵（用于验证） =====
            self.A_complex_dict = {}  # 存储原始复数 CSC 矩阵
            matrices_group = f['matrices']

            for freq_idx, freq_val in enumerate(self.selected_frequencies):
                freq_key = f"freq_{int(freq_val)}Hz"
                if freq_key in matrices_group:
                    # 读取 CSC 格式的复数矩阵数据
                    A_data_complex = matrices_group[freq_key]['A_data'][:]
                    A_indices = matrices_group[freq_key]['A_indices'][:]
                    A_indptr = matrices_group[freq_key]['A_indptr'][:]
                    A_shape = tuple(matrices_group[freq_key]['A_shape'][:])
                    frequency = matrices_group[freq_key].attrs["frequency"]
                    _log(f"正在加载频率 {frequency} Hz 的矩阵:")
                    
                    # 构建 SciPy 稀疏复数矩阵
                    A_complex = csc_matrix(
                        (A_data_complex, A_indices, A_indptr), 
                        shape=A_shape
                    )
                    
                    # 存储到字典（键为频率索引）
                    self.A_complex_dict[freq_idx] = A_complex
                    
                    
                    _log(f"  ✓ Idx [{freq_idx}] 加载复数矩阵 [{freq_key}]: 形状 {A_shape}, 非零元素 {A_complex.nnz}")
            
            # ===== 加载椭圆内边界节点掩码（若存在） =====
            # inner_boundary_mask: [N] bool，True 表示该节点在椭圆内边界上
            # 由 Ocean_Dataset_ellipse.py 生成的 HDF5 中可选地保存了椭圆参数；
            # 这里根据椭圆参数在运行时重建掩码。
            # ===== 读取域形状元数据 =====
            # domain_shape 由 Python Dataset 脚本自动推断写入 h5 attrs，
            # 无需用户手动指定。缺失时（旧数据集）用节点坐标自动检测。
            raw_shape = f.attrs.get('domain_shape', None)
            if raw_shape is not None:
                if isinstance(raw_shape, (bytes, np.bytes_)):
                    raw_shape = raw_shape.decode('utf-8')
                self.domain_shape = str(raw_shape)
            else:
                # 旧数据集无 domain_shape 属性，用节点坐标分布自动检测
                _nodes_np = f['mesh/nodes'][:]   # [2,N]
                x_n, y_n = _nodes_np[0], _nodes_np[1]
                xr = x_n.max() - x_n.min()
                yr = y_n.max() - y_n.min()
                if xr > 1e-8 and yr > 1e-8:
                    xn = ((x_n - x_n.min()) / xr).clip(0, 1)
                    yn = ((y_n - y_n.min()) / yr).clip(0, 1)
                    ix = np.clip((xn * 31).astype(int), 0, 31)
                    iy = np.clip((yn * 31).astype(int), 0, 31)
                    occ = np.zeros((32, 32), dtype=bool)
                    occ[ix, iy] = True
                    occ_ratio = float(occ.mean())
                    x_edges = np.linspace(0, 1, 17)
                    spans = []
                    for _bi in range(16):
                        mb = (xn >= x_edges[_bi]) & (xn < x_edges[_bi + 1])
                        if mb.sum() >= 6:
                            spans.append(float(yn[mb].max() - yn[mb].min()))
                    cv = float(np.std(spans) / max(np.mean(spans), 1e-6)) \
                         if len(spans) >= 4 else 1.0
                    self.domain_shape = 'rectangle' if (occ_ratio > 0.55 and cv < 0.35) \
                                        else 'wedge'
                    _log(f"  [domain 自动检测] 旧数据集无属性，"
                         f"occ={occ_ratio:.3f} cv={cv:.3f} → '{self.domain_shape}'")
                else:
                    self.domain_shape = 'rectangle'
                    _log("  [domain 自动检测] 节点范围过小，默认 'rectangle'")

            self.inner_boundary_mask = None   # 默认无内边界
            self.inner_boundary_node_indices = None
            self.ellipse_params = None          # 默认无内边界参数

            if f.attrs.get('use_ellipse_inner_boundary', 0):
                cx = float(f.attrs['ellipse_cx'])
                cy = float(f.attrs['ellipse_cy'])
                a  = float(f.attrs['ellipse_a'])
                b  = float(f.attrs['ellipse_b'])
                
                # 节点坐标 [2, N]
                nodes_np = f['mesh/nodes'][:]   # [2, N]
                X, Y = nodes_np[0, :], nodes_np[1, :]
                
                dist_sq = ((X - cx) / a) ** 2 + ((Y - cy) / b) ** 2

                # 椭圆内部及边界上的所有节点（dist_sq <= 1）
                # 物理上这些节点均在"潜艇"内部，压力应为零
                # 不再只标记边界环，而是包含全部内部节点
                interior_mask = dist_sq <= 1.0

                self.inner_boundary_mask = torch.from_numpy(interior_mask).bool()
                self.inner_boundary_node_indices = torch.where(self.inner_boundary_mask)[0]
                # 保存椭圆参数字典，供模型构建时使用
                self.ellipse_params = {'cx': cx, 'cy': cy, 'a': a, 'b': b}

                n_boundary = int((dist_sq <= 1.0).sum())
                _log(f"  ✓ 检测到椭圆内边界: 中心=({cx:.1f},{cy:.1f}), "
                      f"a={a:.1f} m, b={b:.1f} m")
                _log(f"  ✓ 椭圆内部+边界节点数（全部归零）: {n_boundary}")
            
        self.edge_index = edge_index
        self.edge_attr = edge_attr
        self.num_samples = len(self.source_vectors)
        
        _log(f"✓ 加载数据集: {os.path.basename(h5_path)}")
        _log(f"  样本数: {self.num_samples}")
        _log(f"  节点数: {self.num_nodes}")
        _log(f"  频率数: {self.num_frequencies}")
        _log(f"  频率: {self.selected_frequencies} Hz")
        _log(f"  域形状: {self.domain_shape}")

    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        return {
            'source_vector': self.source_vectors[idx],
            'fem_tl': self.fem_tl[idx],
            'fem_sol_vectors': self.fem_sol_vectors[idx],
            'analytical_tl': self.analytical_tl[idx],
            'analytical_vectors': self.analytical_vectors[idx],
            'source_position': self.source_positions[idx],
            'freq_index': self.frequency_indices[idx],
            'sample_idx': idx  # **新增**: 用于去重
        }
    
    def get_mesh(self):
        return self.nodes, self.elements
    
    def get_complex_matrix(self, freq_index):
        """
        获取指定频率的原始复数系统矩阵
        
        Args:
            freq_index: int, 频率索引 (0 到 num_frequencies-1)
        
        Returns:
            scipy.sparse.csc_matrix: 复数系统矩阵 A (N × N)
        """
        if freq_index not in self.A_complex_dict:
            raise KeyError(f"频率索引 {freq_index} 不存在，可用索引: {list(self.A_complex_dict.keys())}")
        return self.A_complex_dict[freq_index]

# ==================== 从稀疏矩阵构建图 ====================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def build_graph_from_h5(h5_path):
    """
    读取 HDF5 中所有频率的 CSC 复数矩阵,
    转换成 2N×2N 实矩阵,并生成图结构 (全部放入 GPU).
    
    Args:
        h5_path: str, HDF5 文件路径
        verify_realification: bool, 是否验证实化过程的正确性
    
    Returns:
        edge_index_dict: {0: edge_index (GPU), 1: edge_index, ...}
        edge_attr_dict : {0: edge_attr (GPU), 1: edge_attr, ...}
    """
    
    _log("\n" + "=" * 70)
    _log("构建图拓扑结构：从 HDF5 加载并实化系统矩阵")
    _log("=" * 70)
    
    edge_index_dict = {}
    edge_attr_dict  = {}
    
    with h5py.File(h5_path, 'r') as f:
        matrices_group = f['matrices']
        
        # -------------------------------------------------
        # 1. 收集并排序所有频率
        # -------------------------------------------------
        freq_key_list = []
        for freq_key in matrices_group.keys():
            freq = matrices_group[freq_key].attrs["frequency"]
            freq_key_list.append((freq, freq_key))
        
        freq_key_list.sort(key=lambda x: x[0])
        num_frequencies = len(freq_key_list)
        
        _log(f"发现 {num_frequencies} 个频率: {[f[0] for f in freq_key_list]} Hz")
        _log()
        
        # -------------------------------------------------
        # 2. 遍历所有频率，进行实化处理
        # -------------------------------------------------
        for idx, (freq, freq_key) in enumerate(tqdm(freq_key_list, desc="加载矩阵")):
            freq_group = matrices_group[freq_key]
            
            # 加载 CSC 格式数据
            A_data    = freq_group['A_data'][:]
            A_indices = freq_group['A_indices'][:]
            A_indptr  = freq_group['A_indptr'][:]
            A_shape   = tuple(freq_group['A_shape'][:])
            N = A_shape[0]
            
            # 构建复数 CSC 矩阵并实化为 2×2 块矩阵（纯 scipy，无 cupy）
            A_scipy_csr = csc_matrix((A_data, A_indices, A_indptr), shape=A_shape).tocsr()
            A_real = A_scipy_csr.real.tocsr()
            A_imag = A_scipy_csr.imag.tocsr()
            # 实化: [[Re, -Im], [Im, Re]] → 等价于原 cupy bmat 路径
            A_block = scipy.sparse.bmat(
                [[A_real, -A_imag], [A_imag, A_real]], format='coo')

            edge_index = torch.tensor(
                np.vstack([A_block.col, A_block.row]),
                dtype=torch.long
            ).unsqueeze(0).cuda()  # [1, 2, E]

            edge_attr = torch.from_numpy(
                A_block.data.copy()
            ).double().cuda()
            
            # 存储到字典
            edge_index_dict[idx] = edge_index
            edge_attr_dict[idx]  = edge_attr
    
    _log("\n" + "=" * 70)
    _log(f"✓ 成功加载 {num_frequencies} 个频率的实化矩阵")
    _log(f"  总 GPU 内存占用: ~{estimate_gpu_memory(edge_index_dict, edge_attr_dict):.2f} MB")
    _log("=" * 70)
    
    return edge_index_dict, edge_attr_dict

def estimate_gpu_memory(edge_index_dict, edge_attr_dict):
    """
    估算 GPU 内存占用 (MB)
    
    Args:
        edge_index_dict: dict of torch.Tensor
        edge_attr_dict: dict of torch.Tensor
    
    Returns:
        float: 估算的内存占用 (MB)
    """
    total_bytes = 0
    
    for idx in edge_index_dict:
        # edge_index: (2, E) long (8 bytes per element)
        total_bytes += edge_index_dict[idx].numel() * 8
        
        # edge_attr: (E,) float32 (4 bytes per element)
        total_bytes += edge_attr_dict[idx].numel() * 4
    
    return total_bytes / (1024 ** 2)  # 转换为 MB

# ==================== 压力转TL的辅助函数 ====================
def compute_tl_from_pressure_FEM(pressure, amp):
    """将压力场转换为传播损失(TL)，截断规则与 TL_MAX=200 dB 约定一致"""
    _TL_MAX = 200.0
    with np.errstate(divide='ignore', invalid='ignore'):
        TL = -20 * np.log10(amp / np.abs(pressure))
    TL = np.where(np.isneginf(TL), -_TL_MAX, TL)
    TL = np.where(np.isposinf(TL),     0.0,  TL)
    TL = np.where(np.isnan(TL),         0.0,  TL)
    return TL


# ==================== 内边界损失辅助函数 ====================
def build_inner_boundary_mask_complex(inner_boundary_node_indices, N, device):
    """
    将原始节点索引（长度为 M 的 1D 张量）扩展为实化向量的掩码。

    实化后向量布局: [u_real(0..N-1), u_imag(0..N-1)]，总长 2N。
    内边界节点 k 对应实化索引 k（实部）和 k+N（虚部）。

    Args:
        inner_boundary_node_indices: torch.Tensor, shape [M], 椭圆内边界节点索引
        N: int, 原始节点总数
        device: torch device

    Returns:
        mask: torch.BoolTensor, shape [2N]，内边界节点对应位置为 True
    """
    mask = torch.zeros(2 * N, dtype=torch.bool, device=device)
    idx = inner_boundary_node_indices.to(device)
    mask[idx] = True        # 实部
    mask[idx + N] = True    # 虚部
    return mask


# ==================== 训练器类 ====================
class AcousticTrainer:
    def __init__(self, model, train_loader, test_loader, dataset, 
                 edge_index, A_coo_data_dict, mask,
                 output_dir, device='cuda', rank=0, world_size=1,
                 loss_w_rel_mse=1.0e3,
                 loss_w_prior=1.0):
        """
        Args:
        """
        self.rank = rank
        self.world_size = world_size
        self.is_distributed = (world_size > 1)  # 判断是否真正分布式

        # 先给 log_file 一个默认值，避免在目录创建前调用 self.log() 时报错
        # 主进程在后面的 if rank == 0 块中会覆盖为真实路径
        self.log_file = None
        
        # 模型移到对应GPU
        self.device = device
        model = model.to(device)
        
        # **修改**: 只在真正分布式时使用DDP
        if self.is_distributed:
            self.model = DDP(
                model, 
                device_ids=[rank],
                output_device=rank,
                find_unused_parameters=True
            )
            if self.rank == 0:
                self.log(f"✓ 模型已包装为DDP (GPU {rank}/{world_size})")
        else:
            self.model = model
            if self.rank == 0:
                self.log(f"✓ 使用单GPU模式")
        
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.dataset = dataset
        self.p = self.dataset.nodes.T.cuda()
        self.output_dir = output_dir
        self.amplitude = dataset.amplitude
        self.edge_index = edge_index
        self.mask = mask.to(device)
        self.mask_complex = self.mask.repeat(2).to(device)
        self.mask_index = self.mask.repeat(2).squeeze().bool()
                     
        # edge_attr移到对应GPU
        self.A_coo_data_dict = {
            k: v.to(device).unsqueeze(1) for k, v in A_coo_data_dict.items()
        }
        self.cache = {}

        # ========== 内边界损失相关 ==========
        self.loss_w_rel_mse = float(loss_w_rel_mse)
        self.loss_w_prior = float(loss_w_prior)   # physics_prior vs true MSE 权重
        N = int(dataset.num_nodes)

        # ===== 统一硬边界掩码 bc_mask_full [1,2N]：椭圆内边界 + 海面 Dirichlet(p=0) =====
        # 三模型(proposed/deeponet/fno)共用同一掩码，在 train/eval 经
        # apply_inner_boundary_constraint 统一施加(pred * bc_mask_full)。
        self.bc_mask_full = torch.ones(1, 2 * N, device=device)

        # (a) 椭圆内边界：椭圆内部+边界节点处置 0(实/虚)
        if dataset.inner_boundary_mask is not None and dataset.inner_boundary_node_indices is not None:
            self.inner_bc_mask = build_inner_boundary_mask_complex(
                dataset.inner_boundary_node_indices, N, device
            )
            self.bc_mask_full[:, self.inner_bc_mask] = 0.0
            self.has_inner_bc = True
            if self.rank == 0:
                num_bc_nodes = dataset.inner_boundary_node_indices.shape[0]
                self.log(f"✓ 椭圆内边界硬约束: {num_bc_nodes} 个节点置零(p=0)")
        else:
            self.inner_bc_mask = None
            self.has_inner_bc = False
            if self.rank == 0:
                self.log("  (未检测到椭圆内边界)")

        # (b) 海面 Dirichlet(p=0)：约定原点左上、y 向下为深度，海面 = 最小 y(顶部)。
        #     取 y≈y_min 的节点，实部、虚部均置 0。
        _y = dataset.nodes[1]                                   # [N] 节点 y(深度), CPU
        _surf = (_y - _y.min()).abs() <= 1e-6                   # [N] bool
        self.surface_node_indices = torch.where(_surf)[0].to(device)
        n_surf = int(self.surface_node_indices.numel())
        if n_surf > 0:
            self.bc_mask_full[:, self.surface_node_indices]     = 0.0   # 实部
            self.bc_mask_full[:, self.surface_node_indices + N] = 0.0   # 虚部
        self.has_surface_bc = (n_surf > 0)
        # 只要有任一硬边界(椭圆或海面)，约束即生效
        self.has_inner_bc = self.has_inner_bc or self.has_surface_bc
        if self.rank == 0:
            self.log(f"✓ 海面 Dirichlet 硬约束: {n_surf} 个海面节点置零(p=0)")
        if self.rank == 0:
            self.log(
                f"  Loss weights: complex_mse={self.loss_w_rel_mse:.2e}, "
                f"prior={self.loss_w_prior:.2e}"
            )
        # ====================================

        # 只在主进程创建输出目录
        if self.rank == 0:
            self.model_dir = os.path.join(output_dir, 'models')
            self.log_dir = os.path.join(output_dir, 'logs')
            self.plot_dir = os.path.join(output_dir, 'plots')
            os.makedirs(self.model_dir, exist_ok=True)
            os.makedirs(self.log_dir, exist_ok=True)
            os.makedirs(self.plot_dir, exist_ok=True)

            # 复用 main 中已建立的统一日志文件（含执行命令+参数+前置输出）；
            # 若未建立（例如单独实例化 Trainer）则回退到独立文件。
            if _LOG_FILE_PATH is not None:
                self.log_file = _LOG_FILE_PATH
            else:
                self.log_file = os.path.join(
                    self.log_dir,
                    f'training_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
                )
        
        self.freq_list = self.dataset.selected_frequencies
        self.p_ref = []
        self.p_ref_imag = []
        self.p_ref_real = []
        self.amp = 1500.0
        
        for index in range(len(self.freq_list)):
            k = 2 * np.pi * self.freq_list[index] / 1500.0
            h0 = hankel1(0, k)
            p_ref = 1j * h0 / 4.0
            self.p_ref.append(p_ref)
            self.p_ref_real.append(p_ref.real)
            self.p_ref_imag.append(p_ref.imag)
        
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-3)
        # CosineAnnealingWarmRestarts：余弦退火 + 周期性重启，避免 StepLR 的
        # 阶跃衰减导致的训练不稳定，T_0=50 epoch 一个周期，T_mult=2 逐渐延长
        # self.scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
        #     self.optimizer, T_0=50, T_mult=2, eta_min=1e-5
        # )
        self.scheduler = torch.optim.lr_scheduler.ExponentialLR(
                self.optimizer, 
                gamma=0.995
            )

        # ── 近场加权亥姆霍兹残差（无独立网络，无伪影）──────────────────
        implicit_layer = (self.model.module.implicit_layer
                          if hasattr(self.model, 'module')
                          else self.model.implicit_layer)
        self._implicit_layer = implicit_layer
        self.nf_optimizer = None   # 无独立优化器
        self._has_nf = (
            hasattr(implicit_layer, '_nf_node_weight_2n') and
            implicit_layer._nf_node_weight_2n is not None and
            implicit_layer._nf_node_weight_2n.max().item() > 1.0
        )
        if rank == 0 and self._has_nf:
            n_nf = int((implicit_layer._nf_node_weight_2n > 1.0).sum().item() // 2)
            w_max = implicit_layer._nf_node_weight_2n.max().item()
            self.log(f"  ✓ 近场加权 Helmholtz: {n_nf} 个 NF Box 节点, "
                     f"权重 {w_max:.1f}x，无独立网络无伪影")
        # ─────────────────────────────────────────────────────────────
        self.train_losses = []
        self.test_losses = []

        # ── per-frequency EMA 误差图（节点级自适应权重）─────────────────
        # 形状 [2N]，记录每个节点的历史平均误差（指数移动平均）
        # 每个 train batch 后更新；下一个同频率 batch 用它计算 [1,2] 权重
        # α=0.1：慢速更新，平滑噪声；初始全1（各节点均等）
        _2N = dataset.num_nodes * 2
        self._ema_alpha = 0.1
        self._ema_error = {
            i: torch.ones(_2N, dtype=torch.float32, device=device)
            for i in range(len(self.freq_list))
        }
        # ─────────────────────────────────────────────────────────────
        
        # 按频率分组的损失记录
        self.train_losses_per_freq = {int(freq): [] for freq in self.freq_list}
        self.test_losses_per_freq = {int(freq): [] for freq in self.freq_list}
        
        # 各项误差指标记录
        self.test_fem_errors = []
        self.test_sol_errors = []
        self.test_fem_ana_errors = []
        # 训练集各项误差指标记录
        self.train_fem_errors = []
        self.train_sol_errors = []
        self.train_fem_ana_errors = []

        # 按频率分组的训练集各项误差
        self.train_fem_errors_per_freq = {int(freq): [] for freq in self.freq_list}
        self.train_sol_errors_per_freq = {int(freq): [] for freq in self.freq_list}
        self.train_fem_ana_errors_per_freq = {int(freq): [] for freq in self.freq_list}
        
        # 按频率分组的各项误差
        self.test_fem_errors_per_freq = {int(freq): [] for freq in self.freq_list}
        self.test_sol_errors_per_freq = {int(freq): [] for freq in self.freq_list}
        self.test_fem_ana_errors_per_freq = {int(freq): [] for freq in self.freq_list}
        
        # 推理时间记录
        self.train_time_per_epoch = []
        self.test_time_per_epoch = []
        self.train_time_per_sample = []
        self.test_time_per_sample = []
        
        # 按频率的推理时间
        self.test_time_per_freq = {int(freq): [] for freq in self.freq_list}
        self.train_time_per_freq = {int(freq): [] for freq in self.freq_list}
        
        # 最佳模型跟踪
        self.best_test_loss = float('inf')
        self.best_epoch = 0

    # ==================== 新增：内边界损失计算 ====================
    def apply_inner_boundary_constraint(self, pred):
        """
        硬约束：将硬边界节点上的预测值强制置零（Dirichlet p=0）。
        合并进 self.bc_mask_full 的两类硬边界：
          · 椭圆内边界(障碍物内部+边界)；
          · 海面 Dirichlet(y=0 顶部)。
        实部、虚部均置 0。掩码乘法(非 inplace)保持 autograd 可微，
        对 proposed/deeponet/fno 三模型一视同仁。

        Args:
            pred: torch.Tensor, shape [B, 2N]（前 N 实部、后 N 虚部）。
        Returns:
            pred_constrained: torch.Tensor, shape [B, 2N]（新张量，不破坏 autograd）。
        """
        if not self.has_inner_bc:
            return pred
        # 非 inplace: 掩码乘法保留 autograd 图
        return pred * self.bc_mask_full
    # =============================================================

    def compute_relative_complex_mse(self, target: torch.Tensor,
                                     pred: torch.Tensor,
                                     eps: float = 1e-8) -> torch.Tensor:
        """
        Primary complex-data loss (stable):
            plain complex MSE on [real, imag] concatenation.
        Kept function name for backward compatibility.
        """
        _ = eps  # compatibility
        mse = F.mse_loss(pred, target)
        if not torch.isfinite(mse):
            mse = torch.tensor(0.0, device=pred.device, dtype=pred.dtype)
        return mse

    def compute_log_amplitude_mse(self, target: torch.Tensor,
                                   pred: torch.Tensor,
                                   eps: float = 1e-8) -> torch.Tensor:
        """
        v10 新增 —— log-amplitude MSE。

        为什么需要这一项:
          MSE 对大幅值区过度敏感,对干涉节点 (|p| → 0 的区域) 权重几乎为零。
          但 TL = 20·log10(|p|/|p_ref|) 在低幅值区反而变化最剧烈 —— 这就是
          训练 `Sol vs 解析解` 做到 2.5e-4 但 `TL vs 解析解` 卡在 5 dB 的原因。
          log-amplitude MSE 把"相对误差"做等比监督,保证节点附近也有梯度。

        Args:
            target: [B, 2N] 解析解(前 N 实,后 N 虚)
            pred:   [B, 2N] 预测
            eps:    防 log(0) 的小量(对应 ~-80 dB 下溢门限)
        """
        N = target.shape[1] // 2
        # 复数幅值(不开 sqrt 避免二次方后又开根的数值浪费)
        tgt_mag_sq = target[:, :N]**2 + target[:, N:]**2
        prd_mag_sq = pred[:, :N]**2 + pred[:, N:]**2
        # log|p|² = 2·log|p|,常数不影响梯度
        lt = torch.log(tgt_mag_sq + eps)
        lp = torch.log(prd_mag_sq + eps)
        # 可选: 只在 target 量级足够大的节点上监督(避开数值噪声域)
        # 取 target 幅值的 5 分位作为软底,小于此的节点按 soft mask 衰减权重
        with torch.no_grad():
            low_floor = torch.quantile(tgt_mag_sq.flatten(), 0.05) + eps
        soft_w = torch.sigmoid(torch.log(tgt_mag_sq + eps) - torch.log(low_floor))
        return ((lp - lt)**2 * soft_w).mean()

    def compute_nearfield_weighted_loss(self, pred, target, source_position,
                                        freq_idx, nearfield_radius_wavelengths=2.0):
        """
        近场加权 MSE 损失。
        """
        N = pred.shape[1] // 2
        freq = self.freq_list[freq_idx]
        k = 2.0 * np.pi * freq / 1500.0
        wavelength = 2.0 * np.pi / k

        p_xy = self.p[:N, :].to(self.device)        # [N, 2]

        src = source_position.to(self.device)        # [B, 2]
        dist = torch.norm(
            p_xy.unsqueeze(0) - src.unsqueeze(1),    # [B, N, 2]
            dim=-1
        )                                             # [B, N]

        threshold = nearfield_radius_wavelengths * wavelength
        w_max = 5.0
        smooth_weight = 1.0 + (w_max - 1.0) * torch.sigmoid(
            (threshold - dist) / (0.2 * threshold + 1e-6)
        )                                             # [B, N]

        weight_2n = torch.cat([smooth_weight, smooth_weight], dim=1)  # [B, 2N]

        sq_err = (pred - target) ** 2                # [B, 2N]
        weighted_loss = (sq_err * weight_2n).mean()

        if not torch.isfinite(weighted_loss):
            weighted_loss = F.mse_loss(pred, target)

        return weighted_loss

    def compute_magnitude_phase_mse(self, pred, target, weight=None):
        """
        计算幅值MSE和相位MSE的组合损失（终极稳定版 - 避免所有NaN）
        """
        N = pred.shape[1] // 2

        def _wmean(x, w):
            if w is None:
                return x.mean()
            return (x * w).mean()

        w_N = weight[:N].unsqueeze(0) if weight is not None else None

        pred   = torch.nan_to_num(pred,   nan=0.0, posinf=1e6, neginf=-1e6)
        target = torch.nan_to_num(target, nan=0.0, posinf=1e6, neginf=-1e6)

        pred_real   = pred[:, :N];  pred_imag   = pred[:, N:]
        target_real = target[:, :N]; target_imag = target[:, N:]

        eps = 1e-6
        pred_mag   = torch.sqrt(pred_real**2   + pred_imag**2   + eps)
        target_mag = torch.sqrt(target_real**2 + target_imag**2 + eps)
        pred_mag   = torch.clamp(pred_mag,   min=eps, max=1e6)
        target_mag = torch.clamp(target_mag, min=eps, max=1e6)

        try:
            magnitude_mse = _wmean((pred_mag - target_mag) ** 2, w_N)
            if not torch.isfinite(magnitude_mse):
                magnitude_mse = torch.tensor(1e-6, device=pred.device, dtype=pred.dtype)
        except Exception as e:
            self.log(f"[错误] 幅值MSE计算失败: {e}")
            magnitude_mse = torch.tensor(1e-6, device=pred.device, dtype=pred.dtype)

        pred_norm_real  = torch.clamp(pred_real   / pred_mag,   -1.0, 1.0)
        pred_norm_imag  = torch.clamp(pred_imag   / pred_mag,   -1.0, 1.0)
        target_norm_real = torch.clamp(target_real / target_mag, -1.0, 1.0)
        target_norm_imag = torch.clamp(target_imag / target_mag, -1.0, 1.0)

        cos_delta = torch.clamp(
            pred_norm_real * target_norm_real + pred_norm_imag * target_norm_imag,
            -1.0 + 1e-6, 1.0 - 1e-6)
        phase_angle_diff = torch.acos(cos_delta)   # [B, N]

        mag_threshold = torch.median(target_mag) * 0.01
        valid_mask = (target_mag > mag_threshold) & (pred_mag > mag_threshold)
        num_valid  = valid_mask.sum().item()

        if num_valid > 50:
            try:
                if w_N is not None:
                    w_expanded = w_N.expand_as(phase_angle_diff)
                    w_valid = w_expanded[valid_mask]
                else:
                    w_valid = None
                phase_mse = _wmean(phase_angle_diff[valid_mask], w_valid)
                phase_mse = torch.clamp(phase_mse, 0.0, np.pi)
                if not torch.isfinite(phase_mse):
                    phase_mse = torch.tensor(0.0, device=pred.device, dtype=pred.dtype)
            except Exception as e:
                self.log(f"[错误] 相位MAE计算失败: {e}")
                phase_mse = torch.tensor(0.0, device=pred.device, dtype=pred.dtype)
        else:
            phase_mse = torch.tensor(0.0, device=pred.device, dtype=pred.dtype)

        phase_weight = 0.15
        total_mse = magnitude_mse + phase_weight * phase_mse

        if not torch.isfinite(total_mse):
            self.log(f"[警告] total_mse不是有限值，回退到纯幅值MSE")
            self.log(f"  magnitude_mse: {magnitude_mse.item() if torch.isfinite(magnitude_mse) else 'NaN'}")
            self.log(f"  phase_mse: {phase_mse.item() if torch.isfinite(phase_mse) else 'NaN'}")
            total_mse     = torch.tensor(1e-6, device=pred.device, dtype=pred.dtype)
            magnitude_mse = torch.tensor(1e-6, device=pred.device, dtype=pred.dtype)
            phase_mse     = torch.tensor(0.0,  device=pred.device, dtype=pred.dtype)

        return total_mse
     
    def log(self, message):
        """只在主进程输出日志"""
        if self.rank == 0:
            print(message)
            if self.log_file is not None:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(message + '\n')

    def compute_tl_loss(self, pred_tl, target_tl):
        """计算TL的MSE损失"""
        return torch.mean((pred_tl - target_tl) ** 2)
        
    def get_batch_edge_attr(self, freq_index):
        """
        由于batch内频率相同,只需要传入单个频率索引
        freq_index: 标量tensor或int
        """
        if isinstance(freq_index, torch.Tensor):
            freq_index = freq_index.item()

        return self.A_coo_data_dict[freq_index]
        
    def train_epoch(self, epoch):
        """训练一个epoch - 优化多卡数据收集"""
        self.model.train()

        epoch_start_time = time.time()

        local_total_loss = 0.0
        local_total_loss_rel = 0.0
        local_total_loss_prior = 0.0   # physics_prior vs true MSE
        local_total_fem_error = 0.0
        local_total_sol_error = 0.0
        local_total_fem_ana_error = 0.0
        local_num_samples = 0

        local_freq_losses = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_fem_errors = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_sol_errors = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_fem_ana_errors = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_counts = {int(freq): 0 for freq in self.freq_list}
        local_freq_times = {int(freq): [] for freq in self.freq_list}
        
        local_freq_sol_mae = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_tl_mae_vs_analytical = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_tl_mae_vs_fem = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_tl_mae_analytical_vs_fem = {int(freq): 0.0 for freq in self.freq_list}
        
        sample_times = []
        
        if self.is_distributed and hasattr(self.train_loader.batch_sampler, 'set_epoch'):
            self.train_loader.batch_sampler.set_epoch(epoch)
        
        sampler = self.train_loader.batch_sampler
        if hasattr(sampler, '_current_batch_idx'):
            sampler._current_batch_idx = 0
        
        pbar = tqdm(self.train_loader, desc=f"Training Epoch {epoch}") if self.rank == 0 else self.train_loader
        
        for batch in pbar:
            batch_start_time = time.time()
            
            source_vector = batch['source_vector'].to(self.device)
            source_location = batch['source_position'].to(self.device)
            fem_tl = batch['fem_tl'].to(self.device)
            fem_sol = batch['fem_sol_vectors'].to(self.device)
            sol = batch['analytical_vectors'].to(self.device)
            analytical_tl = batch['analytical_tl'].to(self.device)
            freq_indices = batch['freq_index'].to(self.device)
            
            assert torch.all(freq_indices == freq_indices[0]), "Batch内频率不一致!"
            freq_idx = freq_indices[0].item()
            freq_value = int(self.freq_list[freq_idx])
            
            edge_attr = self.get_batch_edge_attr(freq_idx)
            
            self.optimizer.zero_grad()
            
            source_input = source_vector.permute(0, 2, 1)
            B = source_input.shape[0]
            N = source_input.shape[1]
            real = source_input[:, :, 0]
            imag = source_input[:, :, 1]
            source_input = torch.cat([real, imag], dim=1)
            
            if len(source_input.shape) == 2:
                source_input = source_input.unsqueeze(-1)
            if len(edge_attr.shape) == 2:
                edge_attr = edge_attr.unsqueeze(0)
            
            mask_complex = (source_input.squeeze(-1) != 0).float()
            pred, x_dep_o, x_dep, residual = self.model(
                source_input, edge_attr, freq_idx, 
                self.p_ref[freq_idx], source_location, 
                fem_sol, mask_complex
            )
            
            pred = pred.squeeze(-1)
            x_dep = x_dep.squeeze(-1)
            x_dep_o = x_dep_o.squeeze(-1)
            # ===== 内边界硬约束(椭圆内 p=0): 模型调用后立即统一施加 =====
            # 对 proposed/deeponet/fno 一视同仁，且在 TL/loss 之前；
            # proposed 内部虽已置零，此处再乘掩码为幂等，数值不变。
            pred  = self.apply_inner_boundary_constraint(pred)
            x_dep = self.apply_inner_boundary_constraint(x_dep)
            # ==========================================================
            pred_real = pred[:, :N]
            pred_imag = pred[:, N:]
            x_dep_real = x_dep[:, :N]
            x_dep_imag = x_dep[:, N:]
            sol_real = sol[:, :N]
            sol_imag = sol[:, N:]
            
            analytical_tl = tl_computation_autograd(
                sol_real, sol_imag, self.p_ref[freq_idx]
            )
            pred_tl = tl_computation_autograd(
                pred_real, pred_imag, self.p_ref[freq_idx]
            )

            t_mask = torch.isnan(sol) | torch.isinf(sol)
            if t_mask.any():
                indices = torch.where(t_mask.any(dim=tuple(range(1, sol.ndim))))[0]
                raise ValueError(f"发现NAN/INF,第一维索引: {indices.tolist()} 源点坐标:{source_location[indices].tolist()}")

            batch_size = pred_tl.shape[0]

            rel_complex_mse = self.compute_relative_complex_mse(sol, pred)
            loss_rel_term = self.loss_w_rel_mse * rel_complex_mse
            # physics_prior vs true solution MSE
            loss_prior_term = self.loss_w_prior * F.mse_loss(x_dep, sol)
            tl_loss = loss_rel_term + loss_prior_term
            loss = tl_loss * batch_size
            
            sampler = self.train_loader.batch_sampler
            if hasattr(sampler, 'is_current_batch_real'):
                is_real = sampler.is_current_batch_real()
            else:
                is_real = True
            
            with torch.no_grad():
                # 诊断量与 loss 项严格对齐（去权重后完全相等）：
                #   非修正解 vs COMSOL (fem_error) ≡ loss_prior 原始 MSE = MSE(x_dep, sol)
                #   sol vs COMSOL       (sol_error) ≡ loss_complex 原始 MSE = MSE(pred, sol)
                # 均使用施加内边界约束后的 x_dep/pred，target 用 sol（与 loss 同源）。
                fem_error = F.mse_loss(x_dep, sol)
                sol_error = F.mse_loss(pred, sol)
                fem_ana_error = F.mse_loss(sol, fem_sol)
                
                tl_mae_vs_analytical = torch.mean(torch.abs(pred_tl - analytical_tl)).item()
                tl_mae_vs_fem = torch.mean(torch.abs(pred_tl - fem_tl)).item()
                tl_mae_analytical_vs_fem = torch.mean(torch.abs(analytical_tl - fem_tl)).item()
                
                if is_real:
                    local_total_fem_error += fem_error.item() * batch_size
                    local_total_sol_error += sol_error.item() * batch_size
                    local_total_fem_ana_error += fem_ana_error.item() * batch_size

                    local_freq_fem_errors[freq_value] += fem_error.item() * batch_size
                    local_freq_sol_errors[freq_value] += sol_error.item() * batch_size
                    local_freq_fem_ana_errors[freq_value] += fem_ana_error.item() * batch_size
                    local_freq_tl_mae_vs_analytical[freq_value] += tl_mae_vs_analytical * batch_size
                    local_freq_tl_mae_vs_fem[freq_value] += tl_mae_vs_fem * batch_size
                    local_freq_tl_mae_analytical_vs_fem[freq_value] += tl_mae_analytical_vs_fem * batch_size
            
            loss.backward()
            self.optimizer.step()

            # ── EMA 误差图更新（detach，不参与梯度）───────────────────
            with torch.no_grad():
                cur_err = (pred - sol).detach() ** 2          # [B, 2N]
                cur_err_mean = cur_err.mean(dim=0).float()     # [2N]，batch均值
                α = self._ema_alpha
                self._ema_error[freq_idx] = (
                    (1 - α) * self._ema_error[freq_idx] + α * cur_err_mean
                )
            # ──────────────────────────────────────────────────────────
            
            batch_time = time.time() - batch_start_time
            sample_time = batch_time / batch_size
            sample_times.append(sample_time)
            local_freq_times[freq_value].append(sample_time)
            
            if is_real:
                local_total_loss += loss.item()
                local_total_loss_rel += loss_rel_term.item() * batch_size
                local_total_loss_prior += loss_prior_term.item() * batch_size
                local_num_samples += batch_size
                local_freq_losses[freq_value] += loss.item()
                local_freq_counts[freq_value] += batch_size
            
            if self.rank == 0:
                pbar.set_postfix({
                    'loss': f'{loss.item():.4e}',
                    'freq': f'{freq_value}Hz',
                    'time': f'{batch_time:.3f}s'
                })
        
        epoch_time = time.time() - epoch_start_time

        # ========== 跨GPU同步 ==========
        if self.is_distributed:
            metrics_to_sync = [
                local_total_loss,
                local_total_loss_rel,
                local_total_loss_prior,
                local_total_fem_error,
                local_total_sol_error,
                local_total_fem_ana_error,
                float(local_num_samples)
            ]

            for freq in sorted(local_freq_losses.keys()):
                metrics_to_sync.extend([
                    local_freq_losses[freq],
                    local_freq_fem_errors[freq],
                    local_freq_sol_errors[freq],
                    local_freq_fem_ana_errors[freq],
                    local_freq_tl_mae_vs_analytical[freq],
                    local_freq_tl_mae_vs_fem[freq],
                    local_freq_tl_mae_analytical_vs_fem[freq],
                    float(local_freq_counts[freq])
                ])

            metrics = torch.tensor(metrics_to_sync, device=self.device)
            dist.all_reduce(metrics, op=dist.ReduceOp.SUM)

            total_loss           = metrics[0].item()
            total_loss_rel       = metrics[1].item()
            total_loss_prior     = metrics[2].item()
            total_fem_error      = metrics[3].item()
            total_sol_error      = metrics[4].item()
            total_fem_ana_error  = metrics[5].item()
            total_num_samples    = int(metrics[6].item())

            freq_losses = {}
            freq_fem_errors = {}
            freq_sol_errors = {}
            freq_fem_ana_errors = {}
            freq_tl_mae_vs_analytical = {}
            freq_tl_mae_vs_fem = {}
            freq_tl_mae_analytical_vs_fem = {}
            freq_counts = {}

            idx = 7
            for freq in sorted(local_freq_losses.keys()):
                freq_losses[freq]                       = metrics[idx].item()
                freq_fem_errors[freq]                   = metrics[idx + 1].item()
                freq_sol_errors[freq]                   = metrics[idx + 2].item()
                freq_fem_ana_errors[freq]               = metrics[idx + 3].item()
                freq_tl_mae_vs_analytical[freq]         = metrics[idx + 4].item()
                freq_tl_mae_vs_fem[freq]                = metrics[idx + 5].item()
                freq_tl_mae_analytical_vs_fem[freq]     = metrics[idx + 6].item()
                freq_counts[freq]                       = int(metrics[idx + 7].item())
                idx += 8

            time_metrics = torch.tensor([epoch_time, np.mean(sample_times) if sample_times else 0.0], 
                                        device=self.device)
            dist.all_reduce(time_metrics, op=dist.ReduceOp.SUM)
            epoch_time = time_metrics[0].item() / self.world_size
            avg_sample_time = time_metrics[1].item() / self.world_size
            
            freq_avg_times = {}
            freq_time_list = []
            freq_count_list = []
            for freq in sorted(local_freq_times.keys()):
                if local_freq_times[freq]:
                    freq_time_list.append(np.mean(local_freq_times[freq]))
                    freq_count_list.append(1.0)
                else:
                    freq_time_list.append(0.0)
                    freq_count_list.append(0.0)
            
            if freq_time_list:
                freq_time_tensor = torch.tensor(freq_time_list, device=self.device)
                dist.all_reduce(freq_time_tensor, op=dist.ReduceOp.SUM)
                freq_count_tensor = torch.tensor(freq_count_list, device=self.device)
                dist.all_reduce(freq_count_tensor, op=dist.ReduceOp.SUM)
                for i, freq in enumerate(sorted(local_freq_times.keys())):
                    if freq_count_tensor[i] > 0:
                        freq_avg_times[freq] = freq_time_tensor[i].item() / freq_count_tensor[i].item()
                    else:
                        freq_avg_times[freq] = 0.0
            else:
                for freq in sorted(local_freq_times.keys()):
                    freq_avg_times[freq] = 0.0
        else:
            total_loss           = local_total_loss
            total_loss_rel       = local_total_loss_rel
            total_loss_prior     = local_total_loss_prior
            total_fem_error      = local_total_fem_error
            total_sol_error      = local_total_sol_error
            total_fem_ana_error  = local_total_fem_ana_error
            total_num_samples    = local_num_samples

            freq_losses                   = local_freq_losses
            freq_fem_errors               = local_freq_fem_errors
            freq_sol_errors               = local_freq_sol_errors
            freq_fem_ana_errors           = local_freq_fem_ana_errors
            freq_tl_mae_vs_analytical     = local_freq_tl_mae_vs_analytical
            freq_tl_mae_vs_fem            = local_freq_tl_mae_vs_fem
            freq_tl_mae_analytical_vs_fem = local_freq_tl_mae_analytical_vs_fem
            freq_counts                   = local_freq_counts
            avg_sample_time = np.mean(sample_times) if sample_times else 0.0
            freq_avg_times = {}
            for freq in sorted(local_freq_times.keys()):
                freq_avg_times[freq] = np.mean(local_freq_times[freq]) if local_freq_times[freq] else 0.0

        # ========== 计算平均值并记录 ==========
        avg_loss           = total_loss / total_num_samples if total_num_samples > 0 else 0.0
        avg_loss_rel       = total_loss_rel / total_num_samples if total_num_samples > 0 else 0.0
        avg_loss_prior     = total_loss_prior / total_num_samples if total_num_samples > 0 else 0.0
        avg_fem_error      = total_fem_error / total_num_samples if total_num_samples > 0 else 0.0
        avg_sol_error      = total_sol_error / total_num_samples if total_num_samples > 0 else 0.0
        avg_fem_ana_error  = total_fem_ana_error / total_num_samples if total_num_samples > 0 else 0.0

        self.train_losses.append(avg_loss)
        self.train_fem_errors.append(avg_fem_error)
        self.train_sol_errors.append(avg_sol_error)
        self.train_fem_ana_errors.append(avg_fem_ana_error)
        
        self.train_time_per_epoch.append(epoch_time)
        self.train_time_per_sample.append(avg_sample_time)
        
        freq_avg_losses = {}
        freq_avg_fem_errors = {}
        freq_avg_sol_errors = {}
        freq_avg_fem_ana_errors = {}
        freq_avg_tl_mae_vs_analytical = {}
        freq_avg_tl_mae_vs_fem = {}
        freq_avg_tl_mae_analytical_vs_fem = {}
        
        for freq in sorted(freq_losses.keys()):
            if freq_counts[freq] > 0:
                freq_avg_losses[freq]                   = freq_losses[freq] / freq_counts[freq]
                freq_avg_fem_errors[freq]               = freq_fem_errors[freq] / freq_counts[freq]
                freq_avg_sol_errors[freq]               = freq_sol_errors[freq] / freq_counts[freq]
                freq_avg_fem_ana_errors[freq]           = freq_fem_ana_errors[freq] / freq_counts[freq]
                freq_avg_tl_mae_vs_analytical[freq]     = freq_tl_mae_vs_analytical[freq] / freq_counts[freq]
                freq_avg_tl_mae_vs_fem[freq]            = freq_tl_mae_vs_fem[freq] / freq_counts[freq]
                freq_avg_tl_mae_analytical_vs_fem[freq] = freq_tl_mae_analytical_vs_fem[freq] / freq_counts[freq]
                
                self.train_losses_per_freq[freq].append(freq_avg_losses[freq])
                self.train_fem_errors_per_freq[freq].append(freq_avg_fem_errors[freq])
                self.train_sol_errors_per_freq[freq].append(freq_avg_sol_errors[freq])
                self.train_fem_ana_errors_per_freq[freq].append(freq_avg_fem_ana_errors[freq])
                self.train_time_per_freq[freq].append(freq_avg_times[freq])
            else:
                freq_avg_losses[freq]                   = 0.0
                freq_avg_fem_errors[freq]               = 0.0
                freq_avg_sol_errors[freq]               = 0.0
                freq_avg_fem_ana_errors[freq]           = 0.0
                freq_avg_tl_mae_vs_analytical[freq]     = 0.0
                freq_avg_tl_mae_vs_fem[freq]            = 0.0
                freq_avg_tl_mae_analytical_vs_fem[freq] = 0.0
                
                self.train_losses_per_freq[freq].append(0.0)
                self.train_fem_errors_per_freq[freq].append(0.0)
                self.train_sol_errors_per_freq[freq].append(0.0)
                self.train_fem_ana_errors_per_freq[freq].append(0.0)
                self.train_time_per_freq[freq].append(0.0)
        
        # ========== 打印统计表格 ==========
        if self.rank == 0:
            self.log(f"\n{'='*140}")
            self.log(f"训练 Epoch {epoch} 完成")
            self.log(f"{'='*140}")
            self.log(f"总体统计:")
            self.log(f"  总损失:                   {avg_loss:.6e}")
            self.log(
                f"  Loss Weights: rel_mse={self.loss_w_rel_mse:.2e}, "
                f"prior={self.loss_w_prior:.2e}"
            )
            self.log(f"  Loss-ComplexMSE (w={self.loss_w_rel_mse:.1e}):      {avg_loss_rel:.6e}")
            self.log(f"  Loss-Prior(prior_mse) (w={self.loss_w_prior:.1e}):  {avg_loss_prior:.6e}")
            self.log(f"  非修正解 vs COMSOL误差:      {avg_fem_error:.6e}")
            if self.has_inner_bc:
                self.log(f"  内边界约束: 硬约束已启用 (直接置零)")
            self.log(f"  总样本数:                 {total_num_samples}")
            self.log(f"  总时间:                   {epoch_time:.2f}s")
            self.log(f"  样本时间:                 {avg_sample_time*1000:.2f}ms/sample")
            self.log(f"  吞吐量:                   {total_num_samples/epoch_time:.2f} samples/s")
            
            self.log(f"\n{'='*140}")
            self.log("按频率详细统计:")
            self.log(f"{'='*140}")
            
            header = f"{'频率(Hz)':<10} {'样本数':<8} {'损失':<15} " \
                     f"{'Sol vs COMSOL':<15} " \
                     f"{'TL vs COMSOL':<15} " \
                     f"{'时间(ms)':<10} {'占比':<8}"
            self.log(header)
            self.log(f"{'-'*140}")
            
            for freq in self.freq_list:
                freq_value = int(freq)
                
                if freq_counts[freq_value] == 0:
                    continue
                
                avg_time_ms = freq_avg_times[freq_value] * 1000
                num_samples_freq = freq_counts[freq_value]
                percentage = (num_samples_freq / total_num_samples) * 100
                
                row = f"{freq_value:<10} {num_samples_freq:<8} {freq_avg_losses[freq_value]:<15.6e} " \
                      f"{freq_avg_fem_errors[freq_value]:<15.6e} " \
                      f"{freq_avg_tl_mae_vs_fem[freq_value]:<15.6e} " \
                      f"{avg_time_ms:<10.2f} {percentage:<7.1f}%"
                self.log(row)
            
            self.log(f"{'='*140}")
            
            overall_time_ms = avg_sample_time * 1000
            overall_tl_mae_vs_analytical = sum(freq_tl_mae_vs_analytical.values()) / total_num_samples
            overall_tl_mae_vs_fem = sum(freq_tl_mae_vs_fem.values()) / total_num_samples
            overall_tl_mae_analytical_vs_fem = sum(freq_tl_mae_analytical_vs_fem.values()) / total_num_samples
            
            self.log(f"\n{'Overall':<10} {total_num_samples:<8} {avg_loss:<15.6e} "
                  f"{avg_fem_error:<15.6e} "
                  f"{overall_tl_mae_vs_fem:<15.6e} "
                  f"{overall_time_ms:<10.2f} {'100.0':<7}%")
            self.log("=" * 140 + "\n")
        
        return avg_loss
            
    def evaluate(self, epoch):
        """评估模型 - 优化版：智能采样+只同步统计指标"""        
        self.model.eval()

        eval_start_time = time.time()
        
        local_total_loss = 0.0
        local_total_loss_rel = 0.0
        local_total_loss_prior = 0.0
        local_total_fem_error = 0.0
        local_total_sol_error = 0.0
        local_total_fem_ana_error = 0.0
        local_num_samples = 0

        local_freq_losses = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_fem_errors = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_sol_errors = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_fem_ana_errors = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_counts = {int(freq): 0 for freq in self.freq_list}
        local_freq_times = {int(freq): [] for freq in self.freq_list}
        
        local_freq_tl_mae_vs_analytical = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_tl_mae_vs_fem = {int(freq): 0.0 for freq in self.freq_list}
        local_freq_tl_mae_analytical_vs_fem = {int(freq): 0.0 for freq in self.freq_list}
        
        samples_per_freq = 2
        local_sampled_results = {int(freq): [] for freq in self.freq_list}
        
        sample_times = []
        sampler = self.test_loader.batch_sampler
        if hasattr(sampler, '_current_batch_idx'):
            sampler._current_batch_idx = 0
        
        with torch.no_grad():
            for batch in tqdm(self.test_loader, desc="Evaluating", 
                            disable=not self.rank == 0):
                batch_start_time = time.time()
                
                source_vector = batch['source_vector'].to(self.device)
                fem_tl = batch['fem_tl'].to(self.device)
                source_location = batch['source_position'].to(self.device)
                sol = batch['analytical_vectors'].to(self.device)
                fem_sol = batch['fem_sol_vectors'].to(self.device)
                analytical_tl = batch['analytical_tl'].to(self.device)
                freq_indices = batch['freq_index'].to(self.device)
        
                assert torch.all(freq_indices == freq_indices[0]), "Batch内频率不一致!"
                freq_idx = freq_indices[0].item()
                freq_value = int(self.freq_list[freq_idx])
                
                edge_attr = self.get_batch_edge_attr(freq_idx)
        
                source_input = source_vector.permute(0, 2, 1)
                N = source_input.shape[1]
                real = source_input[:, :, 0]
                imag = source_input[:, :, 1]
                source_input = torch.cat([real, imag], dim=1)
                
                if len(source_input.shape) == 2:
                    source_input = source_input.unsqueeze(-1)
                if len(edge_attr.shape) == 2:
                    edge_attr = edge_attr.unsqueeze(0)
                
                mask_complex = (source_input.squeeze(-1) != 0).float()
                pred, x_dep_o, x_dep, residual = self.model(
                    source_input, edge_attr, freq_idx, 
                    self.p_ref[freq_idx], source_location, 
                    sol, mask_complex
                )
                
                pred = pred.squeeze(-1)
                x_dep = x_dep.squeeze(-1)
                x_dep_o = x_dep_o.squeeze(-1)
                # ===== 内边界硬约束(椭圆内 p=0): 与 train 一致，统一施加 =====
                pred  = self.apply_inner_boundary_constraint(pred)
                x_dep = self.apply_inner_boundary_constraint(x_dep)
                # ==========================================================
                pred_real = pred[:, :N]
                pred_imag = pred[:, N:]
                x_dep_real = x_dep[:, :N]
                x_dep_imag = x_dep[:, N:]
                sol_real = sol[:, :N]
                sol_imag = sol[:, N:]
                                
                analytical_tl = tl_computation_autograd(
                    sol_real, sol_imag, self.p_ref[freq_idx]
                )
                pred_tl = tl_computation_autograd(
                    pred_real, pred_imag, self.p_ref[freq_idx]
                )
                
                batch_size = pred_tl.shape[0]
                t_mask = torch.isnan(sol) | torch.isinf(sol)
                if t_mask.any():
                    indices = torch.where(t_mask.any(dim=tuple(range(1, sol.ndim))))[0]
                    raise ValueError(f"发现NAN/INF,第一维索引: {indices.tolist()} 源点坐标:{source_location[indices].tolist()}")
                
                # 诊断量与 loss 项严格对齐（去权重后完全相等）：
                #   非修正解 vs COMSOL (fem_error) ≡ loss_prior 原始 MSE = MSE(x_dep, sol)
                #   sol vs COMSOL       (sol_error) ≡ loss_complex 原始 MSE = MSE(pred, sol)
                fem_error = F.mse_loss(x_dep, sol)
                sol_error = F.mse_loss(pred, sol)
                fem_ana_error = F.mse_loss(sol, fem_sol)

                tl_mae_vs_analytical = torch.mean(torch.abs(pred_tl - analytical_tl)).item()
                tl_mae_vs_fem = torch.mean(torch.abs(pred_tl - fem_tl)).item()
                tl_mae_analytical_vs_fem = torch.mean(torch.abs(analytical_tl - fem_tl)).item()
                
                batch_time = time.time() - batch_start_time
                sample_time = batch_time / batch_size
                
                sample_times.append(sample_time)
                local_freq_times[freq_value].append(sample_time)
                
                sampler = self.test_loader.batch_sampler
                if hasattr(sampler, 'is_current_batch_real'):
                    is_real = sampler.is_current_batch_real()
                else:
                    is_real = True
                
                if is_real:
                    _rel_complex_mse = self.compute_relative_complex_mse(sol, pred).item()
                    _loss_rel_term = self.loss_w_rel_mse * _rel_complex_mse
                    _loss_prior_term = self.loss_w_prior * F.mse_loss(x_dep, sol).item()
                    # train/test 一致：total loss = rel + prior 两项
                    batch_loss_val = _loss_rel_term + _loss_prior_term
                    local_total_loss += batch_loss_val * batch_size
                    local_total_loss_rel += _loss_rel_term * batch_size
                    local_total_loss_prior += _loss_prior_term * batch_size
                    local_total_fem_error += fem_error.item() * batch_size
                    local_total_sol_error += sol_error.item() * batch_size
                    local_total_fem_ana_error += fem_ana_error.item() * batch_size
                    local_num_samples += batch_size

                    local_freq_losses[freq_value] += batch_loss_val * batch_size
                    local_freq_fem_errors[freq_value] += fem_error.item() * batch_size
                    local_freq_sol_errors[freq_value] += sol_error.item() * batch_size
                    local_freq_fem_ana_errors[freq_value] += fem_ana_error.item() * batch_size
                    local_freq_tl_mae_vs_analytical[freq_value] += tl_mae_vs_analytical * batch_size
                    local_freq_tl_mae_vs_fem[freq_value] += tl_mae_vs_fem * batch_size
                    local_freq_tl_mae_analytical_vs_fem[freq_value] += tl_mae_analytical_vs_fem * batch_size
                    local_freq_counts[freq_value] += batch_size
                
                if len(local_sampled_results[freq_value]) < samples_per_freq:
                    sample_idx = 0
                    local_sampled_results[freq_value].append({
                        'pred_tl': pred_tl[sample_idx:sample_idx+1].cpu(),
                        'fem_tl': fem_tl[sample_idx:sample_idx+1].cpu(),
                        'analytical_tl': analytical_tl[sample_idx:sample_idx+1].cpu(),
                        'source_pos': source_location[sample_idx:sample_idx+1].cpu(),
                        'freq_index': freq_indices[sample_idx:sample_idx+1].cpu(),
                        'sample_idx': batch['sample_idx'][sample_idx:sample_idx+1].cpu()
                    })
        
        eval_time = time.time() - eval_start_time
        
        # ========== 跨GPU聚合 ==========
        if self.is_distributed:
            metrics_to_sync = [
                local_total_loss,
                local_total_loss_rel,
                local_total_loss_prior,
                local_total_fem_error,
                local_total_sol_error,
                local_total_fem_ana_error,
                float(local_num_samples)
            ]

            for freq in sorted(local_freq_losses.keys()):
                metrics_to_sync.extend([
                    local_freq_losses[freq],
                    local_freq_fem_errors[freq],
                    local_freq_sol_errors[freq],
                    local_freq_fem_ana_errors[freq],
                    local_freq_tl_mae_vs_analytical[freq],
                    local_freq_tl_mae_vs_fem[freq],
                    local_freq_tl_mae_analytical_vs_fem[freq],
                    float(local_freq_counts[freq])
                ])

            metrics = torch.tensor(metrics_to_sync, device=self.device)
            dist.all_reduce(metrics, op=dist.ReduceOp.SUM)

            total_loss           = metrics[0].item()
            total_loss_rel       = metrics[1].item()
            total_loss_prior     = metrics[2].item()
            total_fem_error      = metrics[3].item()
            total_sol_error      = metrics[4].item()
            total_fem_ana_error  = metrics[5].item()
            total_num_samples    = int(metrics[6].item())

            freq_losses = {}
            freq_fem_errors = {}
            freq_sol_errors = {}
            freq_fem_ana_errors = {}
            freq_tl_mae_vs_analytical = {}
            freq_tl_mae_vs_fem = {}
            freq_tl_mae_analytical_vs_fem = {}
            freq_counts = {}

            idx = 7
            for freq in sorted(local_freq_losses.keys()):
                freq_losses[freq]                       = metrics[idx].item()
                freq_fem_errors[freq]                   = metrics[idx + 1].item()
                freq_sol_errors[freq]                   = metrics[idx + 2].item()
                freq_fem_ana_errors[freq]               = metrics[idx + 3].item()
                freq_tl_mae_vs_analytical[freq]         = metrics[idx + 4].item()
                freq_tl_mae_vs_fem[freq]                = metrics[idx + 5].item()
                freq_tl_mae_analytical_vs_fem[freq]     = metrics[idx + 6].item()
                freq_counts[freq]                       = int(metrics[idx + 7].item())
                idx += 8
            
            local_avg_sample_time = np.mean(sample_times) if sample_times else 0.0
            time_metrics = torch.tensor([eval_time, local_avg_sample_time], device=self.device)
            dist.all_reduce(time_metrics, op=dist.ReduceOp.SUM)
            eval_time = time_metrics[0].item() / self.world_size
            avg_sample_time = time_metrics[1].item() / self.world_size
            
            freq_avg_times = {}
            freq_time_list = []
            freq_count_list = []
            for freq in sorted(local_freq_times.keys()):
                if local_freq_times[freq]:
                    freq_time_list.append(np.mean(local_freq_times[freq]))
                    freq_count_list.append(1.0)
                else:
                    freq_time_list.append(0.0)
                    freq_count_list.append(0.0)
            
            if freq_time_list:
                freq_time_tensor = torch.tensor(freq_time_list, device=self.device)
                dist.all_reduce(freq_time_tensor, op=dist.ReduceOp.SUM)
                freq_count_tensor = torch.tensor(freq_count_list, device=self.device)
                dist.all_reduce(freq_count_tensor, op=dist.ReduceOp.SUM)
                for i, freq in enumerate(sorted(local_freq_times.keys())):
                    if freq_count_tensor[i] > 0:
                        freq_avg_times[freq] = freq_time_tensor[i].item() / freq_count_tensor[i].item()
                    else:
                        freq_avg_times[freq] = 0.0
            else:
                for freq in sorted(local_freq_times.keys()):
                    freq_avg_times[freq] = 0.0
            
            if self.rank == 0:
                gathered_sampled = [None] * self.world_size
                dist.gather_object(local_sampled_results, gathered_sampled, dst=0)
                
                results = []
                freq_sample_counts = {int(freq): 0 for freq in self.freq_list}
                
                for gpu_samples in gathered_sampled:
                    if gpu_samples is not None:
                        for freq_value in sorted(gpu_samples.keys()):
                            for sample in gpu_samples[freq_value]:
                                if freq_sample_counts[freq_value] < samples_per_freq:
                                    results.append({
                                        'pred_tl': sample['pred_tl'],
                                        'fem_tl': sample['fem_tl'],
                                        'analytical_tl': sample['analytical_tl'],
                                        'source_pos': sample['source_pos'],
                                        'freq_index': sample['freq_index']
                                    })
                                    freq_sample_counts[freq_value] += 1
                                
                                if all(count >= samples_per_freq for count in freq_sample_counts.values()):
                                    break
            else:
                dist.gather_object(local_sampled_results, dst=0)
                results = []
        else:
            total_loss           = local_total_loss
            total_loss_rel       = local_total_loss_rel
            total_loss_prior     = local_total_loss_prior
            total_fem_error      = local_total_fem_error
            total_sol_error      = local_total_sol_error
            total_fem_ana_error  = local_total_fem_ana_error
            total_num_samples    = local_num_samples

            freq_losses                   = local_freq_losses
            freq_fem_errors               = local_freq_fem_errors
            freq_sol_errors               = local_freq_sol_errors
            freq_fem_ana_errors           = local_freq_fem_ana_errors
            freq_tl_mae_vs_analytical     = local_freq_tl_mae_vs_analytical
            freq_tl_mae_vs_fem            = local_freq_tl_mae_vs_fem
            freq_tl_mae_analytical_vs_fem = local_freq_tl_mae_analytical_vs_fem
            freq_counts                   = local_freq_counts
            avg_sample_time = np.mean(sample_times) if sample_times else 0.0
            freq_avg_times = {}
            for freq in sorted(local_freq_times.keys()):
                freq_avg_times[freq] = np.mean(local_freq_times[freq]) if local_freq_times[freq] else 0.0
            
            results = []
            for freq_value in sorted(local_sampled_results.keys()):
                results.extend(local_sampled_results[freq_value])
        
        # ========== 计算平均值并记录 ==========
        avg_loss           = total_loss / total_num_samples if total_num_samples > 0 else 0.0
        avg_loss_rel       = total_loss_rel / total_num_samples if total_num_samples > 0 else 0.0
        avg_loss_prior     = total_loss_prior / total_num_samples if total_num_samples > 0 else 0.0
        avg_fem_error      = total_fem_error / total_num_samples if total_num_samples > 0 else 0.0
        avg_sol_error      = total_sol_error / total_num_samples if total_num_samples > 0 else 0.0
        avg_fem_ana_error  = total_fem_ana_error / total_num_samples if total_num_samples > 0 else 0.0

        self.test_losses.append(avg_loss)
        self.test_fem_errors.append(avg_fem_error)
        self.test_sol_errors.append(avg_sol_error)
        self.test_fem_ana_errors.append(avg_fem_ana_error)
        
        self.test_time_per_epoch.append(eval_time)
        self.test_time_per_sample.append(avg_sample_time)
        
        freq_avg_losses = {}
        freq_avg_fem_errors = {}
        freq_avg_sol_errors = {}
        freq_avg_fem_ana_errors = {}
        freq_avg_tl_mae_vs_analytical = {}
        freq_avg_tl_mae_vs_fem = {}
        freq_avg_tl_mae_analytical_vs_fem = {}
        
        for freq in sorted(freq_losses.keys()):
            if freq_counts[freq] > 0:
                freq_avg_losses[freq]                   = freq_losses[freq] / freq_counts[freq]
                freq_avg_fem_errors[freq]               = freq_fem_errors[freq] / freq_counts[freq]
                freq_avg_sol_errors[freq]               = freq_sol_errors[freq] / freq_counts[freq]
                freq_avg_fem_ana_errors[freq]           = freq_fem_ana_errors[freq] / freq_counts[freq]
                freq_avg_tl_mae_vs_analytical[freq]     = freq_tl_mae_vs_analytical[freq] / freq_counts[freq]
                freq_avg_tl_mae_vs_fem[freq]            = freq_tl_mae_vs_fem[freq] / freq_counts[freq]
                freq_avg_tl_mae_analytical_vs_fem[freq] = freq_tl_mae_analytical_vs_fem[freq] / freq_counts[freq]
                
                self.test_losses_per_freq[freq].append(freq_avg_losses[freq])
                self.test_fem_errors_per_freq[freq].append(freq_avg_fem_errors[freq])
                self.test_sol_errors_per_freq[freq].append(freq_avg_sol_errors[freq])
                self.test_fem_ana_errors_per_freq[freq].append(freq_avg_fem_ana_errors[freq])
                self.test_time_per_freq[freq].append(freq_avg_times[freq])
            else:
                freq_avg_losses[freq]                   = 0.0
                freq_avg_fem_errors[freq]               = 0.0
                freq_avg_sol_errors[freq]               = 0.0
                freq_avg_fem_ana_errors[freq]           = 0.0
                freq_avg_tl_mae_vs_analytical[freq]     = 0.0
                freq_avg_tl_mae_vs_fem[freq]            = 0.0
                freq_avg_tl_mae_analytical_vs_fem[freq] = 0.0
                
                self.test_losses_per_freq[freq].append(0.0)
                self.test_fem_errors_per_freq[freq].append(0.0)
                self.test_sol_errors_per_freq[freq].append(0.0)
                self.test_fem_ana_errors_per_freq[freq].append(0.0)
                self.test_time_per_freq[freq].append(0.0)
        
        # ========== 打印统计表格 ==========
        if self.rank == 0:
            self.log(f"\n{'='*140}")
            self.log(f"评估 Epoch {epoch} 完成")
            self.log(f"{'='*140}")
            self.log(f"总体统计:")
            self.log(f"  测试损失:                    {avg_loss:.6e}")
            self.log(
                f"  Loss Weights: rel_mse={self.loss_w_rel_mse:.2e}, "
                f"prior={self.loss_w_prior:.2e}"
            )
            self.log(f"  Loss-ComplexMSE (w={self.loss_w_rel_mse:.1e}):      {avg_loss_rel:.6e}")
            self.log(f"  Loss-Prior(prior_mse) (w={self.loss_w_prior:.1e}):  {avg_loss_prior:.6e}")
            self.log(f"  非修正解 vs COMSOL误差:         {avg_fem_error:.6e}")
            if self.has_inner_bc:
                self.log(f"  内边界约束: 硬约束已启用 (直接置零)")
            self.log(f"  总样本数:                    {total_num_samples}")
            self.log(f"  总时间:                      {eval_time:.2f}s")
            self.log(f"  样本时间:                    {avg_sample_time*1000:.2f}ms/sample")
            self.log(f"  吞吐量:                      {total_num_samples/eval_time:.2f} samples/s")
            self.log(f"  可视化样本数:                {len(results)} (每频率{samples_per_freq}个)")
            
            self.log("\n" + "=" * 140)
            self.log("按频率详细统计:")
            self.log("=" * 140)
            
            header = f"{'频率(Hz)':<10} {'样本数':<8} {'损失':<15} " \
                     f"{'Sol vs COMSOL':<15} " \
                     f"{'TL vs COMSOL':<15} " \
                     f"{'时间(ms)':<10} {'占比':<8}"
            self.log(header)
            self.log("-" * 140)
            
            for freq in self.freq_list:
                freq_value = int(freq)
                
                if freq_counts[freq_value] == 0:
                    continue
                
                avg_time_ms = freq_avg_times[freq_value] * 1000
                num_samples_freq = freq_counts[freq_value]
                percentage = (num_samples_freq / total_num_samples) * 100
                
                row = f"{freq_value:<10} {num_samples_freq:<8} {freq_avg_losses[freq_value]:<15.6e} " \
                      f"{freq_avg_fem_errors[freq_value]:<15.6e} " \
                      f"{freq_avg_tl_mae_vs_fem[freq_value]:<15.6e} " \
                      f"{avg_time_ms:<10.2f} {percentage:<7.1f}%"
                self.log(row)
            
            self.log("=" * 140)
            
            overall_time_ms = avg_sample_time * 1000
            overall_tl_mae_vs_analytical = sum(freq_tl_mae_vs_analytical.values()) / total_num_samples
            overall_tl_mae_vs_fem = sum(freq_tl_mae_vs_fem.values()) / total_num_samples
            overall_tl_mae_analytical_vs_fem = sum(freq_tl_mae_analytical_vs_fem.values()) / total_num_samples
            
            self.log(f"\n{'Overall':<10} {total_num_samples:<8} {avg_loss:<15.6e} "
                  f"{avg_fem_error:<15.6e} "
                  f"{overall_tl_mae_vs_fem:<15.6e} "
                  f"{overall_time_ms:<10.2f} {'100.0':<7}%")
            self.log("=" * 140 + "\n")
        
        return avg_loss, avg_fem_error, avg_sol_error, avg_fem_ana_error, results
    
    def save_detailed_statistics(self, epoch):
        """保存详细的统计数据到JSON和NPY文件"""
        if not self.rank == 0:
            return
        
        import json
        
        avg_train_time_per_sample_ms = float(np.mean(self.train_time_per_sample) * 1000) if self.train_time_per_sample else 0.0
        avg_test_time_per_sample_ms = float(np.mean(self.test_time_per_sample) * 1000) if self.test_time_per_sample else 0.0
        avg_train_time_per_epoch_s = float(np.mean(self.train_time_per_epoch)) if self.train_time_per_epoch else 0.0
        avg_test_time_per_epoch_s = float(np.mean(self.test_time_per_epoch)) if self.test_time_per_epoch else 0.0
        
        avg_train_time_per_freq = {}
        avg_test_time_per_freq = {}
        for freq in sorted([int(f) for f in self.freq_list]):
            avg_train_time_per_freq[freq] = float(np.mean(self.train_time_per_freq[freq]) * 1000) if self.train_time_per_freq[freq] else 0.0
            avg_test_time_per_freq[freq]  = float(np.mean(self.test_time_per_freq[freq])  * 1000) if self.test_time_per_freq[freq]  else 0.0
        
        stats = {
            'epoch': epoch,
            'overall': {
                'train_losses':           self.train_losses,
                'test_losses':            self.test_losses,
                'train_fem_errors':       self.train_fem_errors,
                'train_sol_errors':       self.train_sol_errors,
                'train_fem_ana_errors':   self.train_fem_ana_errors,
                'test_fem_errors':        self.test_fem_errors,
                'test_sol_errors':        self.test_sol_errors,
                'test_fem_ana_errors':    self.test_fem_ana_errors,
                'best_test_loss':         float(self.best_test_loss),
                'best_epoch':             int(self.best_epoch),
                'has_inner_bc':           bool(self.has_inner_bc),
            },
            'timing': {
                'train_time_per_epoch':         self.train_time_per_epoch,
                'test_time_per_epoch':          self.test_time_per_epoch,
                'train_time_per_sample':        self.train_time_per_sample,
                'test_time_per_sample':         self.test_time_per_sample,
                'avg_train_time_per_sample_ms': avg_train_time_per_sample_ms,
                'avg_test_time_per_sample_ms':  avg_test_time_per_sample_ms,
                'avg_train_time_per_epoch_s':   avg_train_time_per_epoch_s,
                'avg_test_time_per_epoch_s':    avg_test_time_per_epoch_s,
                'total_train_time_s':           float(np.sum(self.train_time_per_epoch)) if self.train_time_per_epoch else 0.0,
                'total_test_time_s':            float(np.sum(self.test_time_per_epoch))  if self.test_time_per_epoch  else 0.0,
                'last_train_time_per_sample_ms': float(self.train_time_per_sample[-1] * 1000) if self.train_time_per_sample else 0.0,
                'last_test_time_per_sample_ms':  float(self.test_time_per_sample[-1]  * 1000) if self.test_time_per_sample  else 0.0,
            },
            'per_frequency': {}
        }
        
        for freq in sorted([int(f) for f in self.freq_list]):
            stats['per_frequency'][str(freq)] = {
                'train_losses':       self.train_losses_per_freq[freq],
                'test_losses':        self.test_losses_per_freq[freq],
                'train_fem_errors':   self.train_fem_errors_per_freq[freq],
                'train_sol_errors':   self.train_sol_errors_per_freq[freq],
                'train_fem_ana_errors': self.train_fem_ana_errors_per_freq[freq],
                'test_fem_errors':    self.test_fem_errors_per_freq[freq],
                'test_sol_errors':    self.test_sol_errors_per_freq[freq],
                'test_fem_ana_errors': self.test_fem_ana_errors_per_freq[freq],
                'train_times':        self.train_time_per_freq[freq],
                'test_times':         self.test_time_per_freq[freq],
                'avg_train_time_ms':  avg_train_time_per_freq[freq],
                'avg_test_time_ms':   avg_test_time_per_freq[freq],
            }
        
        stats['timing_summary'] = {
            'description': 'Average inference times for quick reference',
            'train': {
                'per_sample_ms': avg_train_time_per_sample_ms,
                'per_epoch_s':   avg_train_time_per_epoch_s,
                'total_s':       float(np.sum(self.train_time_per_epoch)) if self.train_time_per_epoch else 0.0,
            },
            'test': {
                'per_sample_ms': avg_test_time_per_sample_ms,
                'per_epoch_s':   avg_test_time_per_epoch_s,
                'total_s':       float(np.sum(self.test_time_per_epoch)) if self.test_time_per_epoch else 0.0,
            },
            'per_frequency_train_ms': avg_train_time_per_freq,
            'per_frequency_test_ms':  avg_test_time_per_freq,
        }
        
        json_path = os.path.join(self.log_dir, f'statistics_epoch{epoch}.json')
        with open(json_path, 'w') as f:
            json.dump(stats, f, indent=2)
        
        npy_path = os.path.join(self.log_dir, f'statistics_epoch{epoch}.npy')
        np.save(npy_path, stats)
        
        self.log(f"✓ 保存统计数据: {json_path}")
        self.log(f"✓ 保存统计数组: {npy_path}")
        
        if epoch == len(self.train_losses):
            self.log("\n" + "=" * 90)
            self.log("推理时间统计摘要:")
            self.log("=" * 90)
            self.log(f"训练集:")
            self.log(f"  平均每样本时间: {avg_train_time_per_sample_ms:.2f} ms")
            self.log(f"  平均每epoch时间: {avg_train_time_per_epoch_s:.2f} s")
            self.log(f"  总训练时间: {float(np.sum(self.train_time_per_epoch)):.2f} s")
            self.log(f"\n测试集:")
            self.log(f"  平均每样本时间: {avg_test_time_per_sample_ms:.2f} ms")
            self.log(f"  平均每epoch时间: {avg_test_time_per_epoch_s:.2f} s")
            self.log(f"  总测试时间: {float(np.sum(self.test_time_per_epoch)):.2f} s")
            self.log(f"\n按频率统计 (训练集, ms/sample):")
            for freq in sorted([int(f) for f in self.freq_list]):
                self.log(f"  {freq} Hz: {avg_train_time_per_freq[freq]:.2f} ms")
            self.log(f"\n按频率统计 (测试集, ms/sample):")
            for freq in sorted([int(f) for f in self.freq_list]):
                self.log(f"  {freq} Hz: {avg_test_time_per_freq[freq]:.2f} ms")
            self.log("=" * 90)

    
    def visualize_train_test_split(self, train_indices, test_indices, prefix='split'):
        """按频率各画一张图，用不同颜色标出训练集/测试集的源点位置。

        便于用户直观判断数据划分（尤其是源点空间范围约束划分 train_max_x/y）是否符合预期。
        坐标约定与 visualize_results 一致：左上角(0,0)，x向右，y向下（海面 y=0 在顶部）。
        楔形时画斜底边界线；有椭圆障碍时画椭圆轮廓。每个频率输出一张 PNG 到 plot_dir。
        """
        if not self.rank == 0:
            return

        src_pos = self.dataset.source_positions.cpu().numpy()   # [N, 2] 物理坐标
        freq_idx_all = self.dataset.frequency_indices.cpu().numpy()  # [N]
        freqs = self.dataset.selected_frequencies

        nodes, _ = self.dataset.get_mesh()
        Lx_dom = float(nodes[0].numpy().max())
        Ly_dom = float(nodes[1].numpy().max())
        is_wedge = getattr(self.dataset, 'domain_shape', 'rectangle') \
                   in ('wedge', 'right_triangle')
        ep = self.dataset.ellipse_params

        train_set = set(int(i) for i in train_indices)
        test_set  = set(int(i) for i in test_indices)

        n_saved = 0
        for fi in range(len(freqs)):
            freq = int(freqs[fi])
            # 该频率下的样本索引
            samp_idx = np.where(freq_idx_all == fi)[0]
            tr_idx = [i for i in samp_idx if i in train_set]
            te_idx = [i for i in samp_idx if i in test_set]
            if len(tr_idx) == 0 and len(te_idx) == 0:
                continue

            fig, ax = plt.subplots(figsize=(8, 8 * Ly_dom / max(Lx_dom, 1e-6)))

            if tr_idx:
                ax.scatter(src_pos[tr_idx, 0], src_pos[tr_idx, 1],
                           c='#1f77b4', s=28, marker='o', alpha=0.75,
                           edgecolors='none', label=f'Train ({len(tr_idx)})')
            if te_idx:
                ax.scatter(src_pos[te_idx, 0], src_pos[te_idx, 1],
                           c='#d62728', s=28, marker='^', alpha=0.75,
                           edgecolors='none', label=f'Test ({len(te_idx)})')

            # 域边界
            if is_wedge:
                ax.plot([0, Lx_dom], [0, Ly_dom], 'k-', linewidth=1.5,
                        label='Rigid boundary')
                ax.plot([Lx_dom, Lx_dom], [0, Ly_dom], color='gray',
                        linewidth=1.0, linestyle='--')
            else:
                ax.plot([0, Lx_dom, Lx_dom, 0, 0],
                        [0, 0, Ly_dom, Ly_dom, 0],
                        color='gray', linewidth=1.0, linestyle='--')

            # 椭圆障碍轮廓
            if ep is not None:
                from matplotlib.patches import Ellipse as _MplEllipse
                ax.add_patch(_MplEllipse(
                    (ep['cx'], ep['cy']), width=2 * ep['a'], height=2 * ep['b'],
                    fill=False, edgecolor='k', linewidth=1.5, linestyle='-'))

            ax.set_xlabel('X / Range (m)', fontsize=11)
            ax.set_ylabel('Y / Depth (m)', fontsize=11)
            ax.set_title(f'Train/Test Source Split  (f={freq} Hz)',
                         fontsize=12, fontweight='bold')
            ax.set_xlim(0, Lx_dom)
            ax.set_ylim(Ly_dom, 0)   # y=0 在顶部
            ax.set_aspect('equal', adjustable='box')
            ax.legend(loc='best', fontsize=9)
            ax.grid(True, alpha=0.3, linestyle='--')

            save_path = os.path.join(self.plot_dir, f'{prefix}_f{freq}Hz.png')
            plt.tight_layout()
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            n_saved += 1
            self.log(f"✓ 保存划分示意图: {save_path} "
                     f"(训练 {len(tr_idx)} / 测试 {len(te_idx)})")

        if n_saved == 0:
            self.log("[警告] 划分示意图：无可绘制的样本")

    def visualize_results(self, results, epoch, prefix='', is_final=False):
        """可视化结果 - 每个频率生成2个样本
        坐标约定：左上角(0,0)，x向右，y向下（海面y=0在顶部，invert_yaxis保证正确显示）
        楔形时：海底斜底 y = (Ly/Lx)*x，从楔尖(0,0)到(Lx,Ly)；Robin 在右截断边 x=Lx；域外区域置NaN。
        """
        if not self.rank == 0:
            return

        if len(results) == 0:
            self.log("[警告] 没有可视化数据")
            return

        nodes, elements = self.dataset.get_mesh()
        x_coords = nodes[0].numpy()
        y_coords = nodes[1].numpy()
        Lx_dom = float(x_coords.max())
        Ly_dom = float(y_coords.max())

        # 判断域形状
        is_wedge = getattr(self.dataset, 'domain_shape', 'rectangle') \
                   in ('wedge', 'right_triangle')

        freq_samples = {}
        for result in results:
            freq_idx = result['freq_index'][0].item()
            if freq_idx not in freq_samples:
                freq_samples[freq_idx] = []
            if len(freq_samples[freq_idx]) < 2:
                freq_samples[freq_idx].append(result)
            if len(freq_samples) == len(self.dataset.selected_frequencies):
                if all(len(samples) == 2 for samples in freq_samples.values()):
                    break

        selected_results = []
        for freq_idx in sorted(freq_samples.keys()):
            selected_results.extend(freq_samples[freq_idx])

        num_samples_vis = len(selected_results)
        if num_samples_vis == 0:
            self.log("[警告] 没有选中的样本")
            return

        fig, axes = plt.subplots(num_samples_vis, 3,
                                 figsize=(18, 5 * num_samples_vis))
        if num_samples_vis == 1:
            axes = axes.reshape(1, -1)

        # 规则插值网格
        gx_lin = np.linspace(0, Lx_dom, 200)
        gy_lin = np.linspace(0, Ly_dom, 200)
        grid_x, grid_y = np.meshgrid(gx_lin, gy_lin)

        # 楔形域外 mask：海底斜底 y = (Ly/Lx)*x，域外（斜底以下 y > (Ly/Lx)*x）置NaN
        if is_wedge:
            # 楔形斜底：y = (Ly/Lx)*x，从左上角(0,0)到右下角(Lx,Ly)
            # 域外（斜底以下）：y > (Ly/Lx)*x
            wedge_outside = grid_y > (Ly_dom / Lx_dom) * grid_x
        else:
            wedge_outside = np.zeros_like(grid_x, dtype=bool)

        for i, result in enumerate(selected_results):
            pred_tl   = result['pred_tl'][0].numpy()
            fem_tl    = result['fem_tl'][0].numpy()
            source_pos = result['source_pos'][0].numpy()
            freq_idx  = result['freq_index'][0].item()
            freq      = self.dataset.selected_frequencies[freq_idx]

            grid_pred = griddata((x_coords, y_coords), pred_tl,
                                 (grid_x, grid_y), method='cubic')
            grid_fem  = griddata((x_coords, y_coords), fem_tl,
                                 (grid_x, grid_y), method='cubic')

            vmin, vmax = -60.0, 0.0

            # 椭圆障碍内部遮罩
            if self.dataset.ellipse_params is not None:
                ep = self.dataset.ellipse_params
                cx, cy, a, b = ep['cx'], ep['cy'], ep['a'], ep['b']
                inside_ell = ((grid_x - cx)/a)**2 + ((grid_y - cy)/b)**2 <= 1.0
                grid_pred[inside_ell] = np.nan
                grid_fem[inside_ell]  = np.nan

            # 楔形域外遮罩
            grid_pred[wedge_outside] = np.nan
            grid_fem[wedge_outside]  = np.nan

            grid_pred = np.clip(grid_pred, vmin, vmax)
            grid_fem  = np.clip(grid_fem,  vmin, vmax)
            gnn_error = np.abs(grid_pred - grid_fem)
            avg_gnn_error = float(np.nanmean(gnn_error))
            error_vmax = min(float(np.nanmax(gnn_error)) if np.any(np.isfinite(gnn_error)) else 10.0, 10.0)

            titles = [
                f'Ours TL (f={freq:.0f}Hz)\nSrc:({source_pos[0]:.1f},{source_pos[1]:.1f})',
                f'COMSOL TL (f={freq:.0f}Hz)',
                f'Error vs COMSOL | Avg:{avg_gnn_error:.2f} dB'
            ]
            data_list  = [grid_pred, grid_fem, gnn_error]
            cmap_list  = ['jet', 'jet', 'Reds']
            vmin_list  = [vmin, vmin, 0]
            vmax_list  = [vmax, vmax, error_vmax]

            extent = (0, Lx_dom, Ly_dom, 0)  # (left,right,bottom,top): bottom=Ly,top=0 -> 海面y=0在顶(修正上下翻转)

            for j, (data, title) in enumerate(zip(data_list, titles)):
                ax = axes[i, j]
                im = ax.imshow(data, extent=extent,
                               origin='upper',       # origin='upper': 矩阵[0,0]在左上→y=0在顶
                               cmap=cmap_list[j], aspect='equal',
                               vmin=vmin_list[j], vmax=vmax_list[j])

                # 楔形边界线
                if is_wedge:
                    # 斜底边：(0,0)→(Lx,Ly)，即 y=(Ly/Lx)*x
                    ax.plot([0, Lx_dom], [0, Ly_dom], 'k-', linewidth=1.5,
                            label='Rigid boundary')
                    # 右截断边 x=Lx（Robin/Nonreflecting）；左侧 x=0 为楔尖退化点，无边界
                    ax.plot([Lx_dom, Lx_dom], [0, Ly_dom], color='gray', linewidth=1.0,
                            linestyle='--')

                # 椭圆障碍内边界轮廓 (画出 p=0 硬约束的障碍边界,内部已遮罩为空白)
                if self.dataset.ellipse_params is not None:
                    from matplotlib.patches import Ellipse as _MplEllipse
                    ep = self.dataset.ellipse_params
                    ax.add_patch(_MplEllipse(
                        (ep['cx'], ep['cy']), width=2*ep['a'], height=2*ep['b'],
                        fill=False, edgecolor='k', linewidth=1.5, linestyle='-'))

                # 声源标注
                ax.plot(source_pos[0], source_pos[1], 'r*', markersize=10)

                ax.set_xlabel('X / Range (m)', fontsize=10)
                ax.set_ylabel('Y / Depth (m)', fontsize=10)
                ax.set_title(title, fontsize=10, fontweight='bold')
                # origin='upper' 已使 y=0 在顶部，无需 invert_yaxis
                ax.set_xlim(0, Lx_dom)
                ax.set_ylim(Ly_dom, 0)   # y 轴：0在顶，Ly在底

                cbar = plt.colorbar(im, ax=ax, fraction=0.035, pad=0.04, shrink=0.8)
                cbar.set_label('TL (dB)' if j < 2 else 'Error (dB)', fontsize=9)

                for spine in ax.spines.values():
                    spine.set_edgecolor('black')
                    spine.set_linewidth(1.5)

        domain_label = 'Wedge' if is_wedge else 'Rectangle'
        plt.suptitle(f'[{domain_label}] TL Field  Epoch {epoch}',
                     fontsize=12, fontweight='bold')
        # 大标题保留，并用 rect 给顶部留白，避免 suptitle 与子图标题重合
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        filename = f'{prefix}_tl_comparison_epoch{epoch}.pdf'
        save_path = os.path.join(self.plot_dir, filename)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()

        self.log(f"✓ 保存可视化结果: {save_path} "
                 f"(样本数: {num_samples_vis}, 覆盖频率: {len(freq_samples)})")

        # 末轮：额外保存本图的原始张量（插值前的节点级数据 + 网格 + 元信息），
        # 供 restore_tl_figure.py 离线复现图像，无需重跑训练。
        if is_final:
            self._save_plot_raw_tensors(selected_results, epoch, prefix,
                                        Lx_dom, Ly_dom, is_wedge)


    def _save_plot_raw_tensors(self, selected_results, epoch, prefix,
                               Lx_dom, Ly_dom, is_wedge):
        """末轮保存 TL 对比图的原始张量（插值前的节点级数据 + 网格 + 元信息）。

        保存为一个 .npz，供 restore_tl_figure.py 离线复现图像（无需重跑训练）。
        存的是节点级 pred_tl/fem_tl（未插值），还原脚本内部做 griddata 插值重建，
        与训练时绘图逻辑一致。
        """
        nodes, _ = self.dataset.get_mesh()
        x_coords = nodes[0].numpy()
        y_coords = nodes[1].numpy()

        n = len(selected_results)
        Nnode = x_coords.shape[0]
        pred_tl_all = np.zeros((n, Nnode), dtype=np.float64)
        fem_tl_all  = np.zeros((n, Nnode), dtype=np.float64)
        src_all     = np.zeros((n, 2), dtype=np.float64)
        freq_all    = np.zeros((n,), dtype=np.float64)
        for i, r in enumerate(selected_results):
            pred_tl_all[i] = r['pred_tl'][0].numpy()
            fem_tl_all[i]  = r['fem_tl'][0].numpy()
            src_all[i]     = r['source_pos'][0].numpy()
            fi             = r['freq_index'][0].item()
            freq_all[i]    = float(self.dataset.selected_frequencies[fi])

        ep = self.dataset.ellipse_params
        if ep is not None:
            ellipse = np.array([ep['cx'], ep['cy'], ep['a'], ep['b']],
                               dtype=np.float64)
        else:
            ellipse = np.array([], dtype=np.float64)   # 空 = 无椭圆

        save_path = os.path.join(self.plot_dir, f'{prefix}_tl_raw_epoch{epoch}.npz')
        np.savez_compressed(
            save_path,
            x_coords=x_coords, y_coords=y_coords,
            pred_tl=pred_tl_all, fem_tl=fem_tl_all,
            source_pos=src_all, freq=freq_all,
            Lx_dom=np.float64(Lx_dom), Ly_dom=np.float64(Ly_dom),
            is_wedge=np.bool_(is_wedge),
            ellipse=ellipse,
            vmin=np.float64(-60.0), vmax=np.float64(0.0),
            epoch=np.int64(epoch),
            domain_label=('Wedge' if is_wedge else 'Rectangle'),
        )
        self.log(f"✓ 保存绘图原始张量: {save_path} "
                 f"(样本 {n}, 节点 {Nnode}) —— 可用 restore_tl_figure.py 复现")


    def plot_loss_curves_enhanced(self, epoch):
        """增强版损失曲线绘制 - 包含总体和分频率曲线，以及内边界损失"""
        if not self.rank == 0:
            return
        
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
        
        nrows = 3

        fig = plt.figure(figsize=(20, 4 * nrows))
        gs = gridspec.GridSpec(nrows, 2, figure=fig, hspace=0.35, wspace=0.3)
        
        epochs = range(1, len(self.train_losses) + 1)
        
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(epochs, self.train_losses, 'b-', label='Train Loss', 
                 linewidth=2.5, marker='o', markersize=3, alpha=0.7)
        ax1.plot(epochs, self.test_losses, 'r-', label='Test Loss', 
                 linewidth=2.5, marker='s', markersize=3, alpha=0.7)
        
        if len(self.test_losses) > 0:
            best_epoch = np.argmin(self.test_losses) + 1
            best_loss = self.test_losses[best_epoch - 1]
            ax1.plot(best_epoch, best_loss, 'g*', markersize=15, 
                    label=f'Best: {best_loss:.4e} @ Epoch {best_epoch}')
        
        ax1.set_xlabel('Epoch', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Loss', fontsize=12, fontweight='bold')
        ax1.set_title('Overall Training and Test Loss', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10, loc='best')
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_yscale('log')
        
        ax2 = fig.add_subplot(gs[1, 0])
        colors = plt.cm.rainbow(np.linspace(0, 1, len(self.freq_list)))
        
        for idx, freq in enumerate(sorted([int(f) for f in self.freq_list])):
            if len(self.train_losses_per_freq[freq]) > 0:
                ax2.plot(epochs, self.train_losses_per_freq[freq], 
                        label=f'{freq} Hz', linewidth=2, 
                        marker='o', markersize=2, color=colors[idx], alpha=0.7)
        
        ax2.set_xlabel('Epoch', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Loss', fontsize=11, fontweight='bold')
        ax2.set_title('Training Loss by Frequency', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9, loc='best', ncol=2)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.set_yscale('log')
        
        ax3 = fig.add_subplot(gs[1, 1])
        
        for idx, freq in enumerate(sorted([int(f) for f in self.freq_list])):
            if len(self.test_losses_per_freq[freq]) > 0:
                ax3.plot(epochs, self.test_losses_per_freq[freq], 
                        label=f'{freq} Hz', linewidth=2, 
                        marker='s', markersize=2, color=colors[idx], alpha=0.7)
        
        ax3.set_xlabel('Epoch', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Loss', fontsize=11, fontweight='bold')
        ax3.set_title('Test Loss by Frequency', fontsize=12, fontweight='bold')
        ax3.legend(fontsize=9, loc='best', ncol=2)
        ax3.grid(True, alpha=0.3, linestyle='--')
        ax3.set_yscale('log')
        
        ax4 = fig.add_subplot(gs[2, 0])
        
        if len(self.train_sol_errors) > 0:
            ax4.plot(epochs, self.train_sol_errors, 'g-',
                    label='Solution vs COMSOL', linewidth=2, marker='o', markersize=3)
        if len(self.train_fem_errors) > 0:
            ax4.plot(epochs, self.train_fem_errors, 'b-',
                    label='Solution without Correction vs COMSOL', linewidth=2, marker='s', markersize=3)

        ax4.set_xlabel('Epoch', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Error', fontsize=11, fontweight='bold')
        ax4.set_title('Training Set Error Metrics Over Time', fontsize=12, fontweight='bold')
        ax4.legend(fontsize=9, loc='best')
        ax4.grid(True, alpha=0.3, linestyle='--')
        ax4.set_yscale('log')
        
        ax5 = fig.add_subplot(gs[2, 1])
        
        if len(self.test_sol_errors) > 0:
            ax5.plot(epochs, self.test_sol_errors, 'g-',
                    label='Solution vs COMSOL', linewidth=2, marker='o', markersize=3)
        if len(self.test_fem_errors) > 0:
            ax5.plot(epochs, self.test_fem_errors, 'b-',
                    label='Solution without Correction vs COMSOL', linewidth=2, marker='s', markersize=3)

        ax5.set_xlabel('Epoch', fontsize=11, fontweight='bold')
        ax5.set_ylabel('Error', fontsize=11, fontweight='bold')
        ax5.set_title('Test Set Error Metrics Over Time', fontsize=12, fontweight='bold')
        ax5.legend(fontsize=9, loc='best')
        ax5.grid(True, alpha=0.3, linestyle='--')
        ax5.set_yscale('log')

        save_path = os.path.join(self.plot_dir, f'metrics_dashboard_epoch{epoch}.pdf')
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.log(f"✓ 保存指标面板: {save_path}")
            
        
    def train(self, num_epochs):
        """完整训练流程 - 增强版"""
        if self.rank == 0:
            mode = "多GPU分布式" if self.is_distributed else "单GPU"
            self.log("=" * 90)
            self.log(f"开始训练 - {num_epochs} epochs ({mode}: {self.world_size}张卡)")
            self.log(f"训练集大小: {len(self.train_loader.dataset)}")
            self.log(f"测试集大小: {len(self.test_loader.dataset)}")
            self.log(f"频率: {self.dataset.selected_frequencies} Hz")
            if self.has_inner_bc:
                self.log(f"椭圆内边界约束: 硬约束已启用 (直接置零 p=0)")
            if self.is_distributed:
                self.log(f"数据聚合: 所有GPU数据将在主进程聚合统计")
            self.log("=" * 90)

        for epoch in range(1, num_epochs + 1):
            train_loss = self.train_epoch(epoch)
            
            if self.is_distributed:
                dist.barrier()
            
            test_loss, fem_error, sol_error, fem_ana_error, results = self.evaluate(epoch)
            self.scheduler.step()
            
            if self.rank == 0:
                if epoch % 25 == 0 or epoch == num_epochs:
                    self.log(f"\n[保存] 正在保存第 {epoch} epoch的统计数据和图表...")

                    _is_final = (epoch == num_epochs)
                    self.save_detailed_statistics(epoch)
                    self.plot_loss_curves_enhanced(epoch)
                    # 末轮额外保存绘图原始张量（供 restore_tl_figure.py 复现）
                    self.visualize_results(results, epoch, prefix='periodic',
                                           is_final=_is_final)
                
                if test_loss < self.best_test_loss:
                    self.best_test_loss = test_loss
                    self.best_epoch = epoch

                    # Bug fix: 每次刷新最佳即落盘，与 25 倍数的周期性存档解耦。
                    # 原逻辑仅在 epoch%25==0 时才 torch.save，导致最佳出现在非 25
                    # 倍数 epoch 时 best_model.pth 未更新（甚至保存的不是最佳模型）。
                    model_to_save = self.model.module if hasattr(self.model, 'module') else self.model

                    checkpoint = {
                        'epoch': epoch,
                        'model_state_dict': model_to_save.state_dict(),
                        'optimizer_state_dict': self.optimizer.state_dict(),
                        'scheduler_state_dict': self.scheduler.state_dict(),
                        'test_loss': test_loss,
                        'train_loss': train_loss,
                        'best_test_loss': self.best_test_loss,
                        'best_epoch': self.best_epoch,
                        'world_size': self.world_size,
                        'statistics': {
                            'train_losses': self.train_losses,
                            'test_losses': self.test_losses,
                            'train_losses_per_freq': self.train_losses_per_freq,
                            'test_losses_per_freq': self.test_losses_per_freq,
                        }
                    }

                    save_path = os.path.join(self.model_dir, 'best_model.pth')
                    torch.save(checkpoint, save_path)
                    self.log(f"✓ 保存最佳模型: {save_path} (Epoch {epoch}, Loss: {test_loss:.4e})")
        
        if self.rank == 0:
            self.save_detailed_statistics(num_epochs)
            self.plot_loss_curves_enhanced(num_epochs)
            
            self.log("\n" + "=" * 90)
            self.log(f"训练完成!")
            self.log(f"  最优测试损失: {self.best_test_loss:.4e} (Epoch {self.best_epoch})")
            self.log(f"  训练模式: {'多GPU分布式' if self.is_distributed else '单GPU'}")
            if self.is_distributed:
                self.log(f"  使用GPU数量: {self.world_size}")
            if self.has_inner_bc:
                self.log(f"  内边界约束: 硬约束 (直接置零 p=0)")
            self.log(f"  平均测试时间: {np.mean(self.test_time_per_sample)*1000:.2f} ms/sample")
            self.log("=" * 90)
            
# ==================== 主程序 ====================
def main(args):
    if args.distributed:
        try:
            rank, world_size, gpu = setup_distributed()
            device = f'cuda:{gpu}'
            is_distributed = (world_size > 1)
            
            if rank == 0:
                _log(f"\n{'='*70}")
                _log(f"分布式配置:")
                _log(f"  - 模式: {'多GPU分布式' if is_distributed else '单GPU'}")
                _log(f"  - GPU数量: {world_size}")
                _log(f"  - 当前GPU: {gpu}")
                _log(f"  - 全局Rank: {rank}")
                _log(f"{'='*70}\n")
        except Exception as e:
            _log(f"[警告] 分布式初始化失败: {e}")
            _log(f"[回退] 使用单GPU模式")
            rank = 0
            world_size = 1
            gpu = 0
            is_distributed = False
            device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    else:
        rank = 0
        world_size = 1
        gpu = 0
        is_distributed = False
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    seed = args.seed + rank
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    
    if rank == 0:
        _log(f"使用设备: {device}")
        _log(f"随机种子: {seed}")

    if rank == 0:
        _log("\n" + "=" * 70)
        _log("查找数据集文件")
        _log("=" * 70)
    
    dataset_dirs = sorted([
        os.path.join(args.data_dir, d)
        for d in os.listdir(args.data_dir)
        if os.path.isdir(os.path.join(args.data_dir, d)) and d.startswith(args.dataset_name)
    ])

    if not dataset_dirs:
        # 列出 data_dir 下所有子目录，方便定位命名差异
        try:
            all_subdirs = sorted([
                d for d in os.listdir(args.data_dir)
                if os.path.isdir(os.path.join(args.data_dir, d))
            ])
        except Exception:
            all_subdirs = []
        hint = (
            f"\n  可用子目录（共 {len(all_subdirs)} 个）:\n"
            + "\n".join(f"    {d}" for d in all_subdirs[:30])
            + ("\n    ..." if len(all_subdirs) > 30 else "")
            if all_subdirs else "\n  （data_dir 下无任何子目录）"
        )
        raise FileNotFoundError(
            f"在 {args.data_dir} 中找不到以 '{args.dataset_name}' 开头的目录。"
            f"{hint}"
            f"\n  请检查 --dataset_name 参数是否与目录名完全匹配。"
        )
    
    dataset_dir = dataset_dirs[0]
    h5_path = os.path.join(dataset_dir, "acoustic_dataset.h5")
    
    if not os.path.exists(h5_path):
        raise FileNotFoundError(f"找不到数据文件: {h5_path}")
    
    if rank == 0:
        _log(f"✓ 找到数据集: {dataset_dir}")

    if rank == 0:
        _log("\n" + "=" * 70)
        _log("构建图拓扑结构")
        _log("=" * 70)
    edge_index, edge_attr = build_graph_from_h5(h5_path)

    if rank == 0:
        _log("\n" + "=" * 70)
        _log("加载数据集")
        _log("=" * 70)
    dataset = AcousticDataset(h5_path, edge_index, edge_attr)

    if rank == 0:
        _log("\n" + "=" * 70)
        _log("划分训练集和测试集")
        _log("=" * 70)

    Y = dataset.frequency_indices.numpy()

    # ── 频率过滤校验（仅校验合法性，实际过滤在 split 之后）──────────────────
    if args.active_freqs is not None:
        available_freqs = [int(f) for f in dataset.selected_frequencies]
        invalid = [f for f in args.active_freqs if f not in available_freqs]
        if invalid:
            raise ValueError(
                f"--active_freqs 中包含数据集不支持的频率: {invalid}\n"
                f"可用频率: {available_freqs}"
            )

    # ── ★ output_dir：从 h5 元数据 + dataset 构建，与 Python Dataset v3 命名对齐 ──
    # 此处提前构建，使 split_file 可放在 output_dir 下（不污染数据目录）。
    # geometry_type 此时尚未由三方判别确定，用 h5 的 domain_shape 做路径标识；
    # 真正用于选择先验网络的 geometry_type 在模型构建前由三方判别确定。
    _h5_domain_for_path = getattr(dataset, 'domain_shape', 'rectangle')
    _dom_path = {'right_triangle': 'wedge', 'rectangle': 'rectangle',
                 'wedge': 'wedge'}.get(_h5_domain_for_path, _h5_domain_for_path)

    with h5py.File(h5_path, 'r') as _hf:
        _grid_x    = int(_hf.attrs.get('grid_size_x',           0))
        _grid_y    = int(_hf.attrs.get('grid_size_y',           0))
        _H_val     = float(_hf.attrs.get('grid_resolution_H',   0.0))
        _spf       = int(_hf.attrs.get('samples_per_frequency',  0))
        _freqs_raw = _hf.attrs.get('selected_frequencies',      [])
        _has_split   = int(_hf.attrs.get('has_split_info',       0))
        _split_ttest = int(_hf.attrs.get('split_train_test',     0))
        _tx        = float(_hf.attrs.get('train_max_x',          0.0))
        _ty        = float(_hf.attrs.get('train_max_y',          0.0))
        # 参考解类型：解析解数据集（reference_solution_type='analytic'）加 _analyticsol
        # 后缀，与 MATLAB/转换器目录命名对齐，避免与同网格 COMSOL 数据集实验目录互覆盖。
        _ref_sol_type = _hf.attrs.get('reference_solution_type', 'FEM')
        if isinstance(_ref_sol_type, bytes):
            _ref_sol_type = _ref_sol_type.decode('utf-8', 'ignore')
        _sol_tag = "_analyticsol" if str(_ref_sol_type).strip().lower() == 'analytic' else ""
        # 读取 MATLAB split_info：每频率的训练样本数 n_train。
        # 语义：数据集内每个频率块「先 n_train 个训练样本、随后 n_test 个测试样本」。
        # 用每频率相对量 n_train（而非绝对 train_start），对上游频率过滤/顺序压缩免疫。
        # 以【频率值 Hz】为对齐键（而非 freq_idx —— 后者是 MATLAB 原始索引，
        # 与 trainer 端 selected 重映射后的索引可能不一致）。
        _split_ntrain_by_hz = {}
        if 'split_info' in _hf:
            for _grp_name in _hf['split_info']:
                _a = _hf['split_info'][_grp_name].attrs
                try:
                    _hz = int(round(float(_a['freq'])))
                    _split_ntrain_by_hz[_hz] = int(_a['n_train'])
                except (KeyError, ValueError, TypeError):
                    continue

    # ── 回退：HDF5 未写 split 元数据时，从数据集目录名解析约束范围 ──────────
    # 场景：MATLAB 设了 split_train_test=true 但 manifest 缺 split_info（见
    # run_gpu0.log「⚠ manifest 中无 split_info」），导致 Python 端整段 split
    # 元数据未写入 HDF5（split_train_test/train_max_x/y 全缺）。此时目录名仍带
    # data_generate_comsol.m 生成的 _split<X>x<Y> 标记（如 _split128x48），
    # 据此恢复约束范围，用源点坐标法 (x≤X AND y≤Y) 强制启用域内划分。
    if not (_split_ttest == 1 and _tx > 0.0 and _ty > 0.0):
        import re as _re
        _m = _re.search(r'_split(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)',
                        os.path.basename(os.path.normpath(dataset_dir)))
        if _m:
            _tx = float(_m.group(1))
            _ty = float(_m.group(2))
            _split_ttest = 1
            if rank == 0:
                _log(f"⚠ HDF5 缺 split 元数据，但目录名含 split 标记 → "
                     f"从路径恢复约束范围 (train: x≤{_tx:.1f} AND y≤{_ty:.1f})，"
                     f"将用源点坐标法启用域内划分。")

    _freqs_sorted = sorted([int(f) for f in _freqs_raw])
    if args.active_freqs is not None:
        _freq_tag = "f" + "_".join(str(f) for f in sorted(args.active_freqs)) + "_active"
    else:
        _freq_tag = "f" + "_".join(str(f) for f in _freqs_sorted)
    # split_tag 判据必须与实际划分逻辑 (_need_region_split) 一致：
    # 仅当启用范围约束 (split_train_test=1) 且 train_max_x/y 有效时才带 _split 标记，
    # 避免「有 split_info 但未启用约束」误加标记、或「按约束划分却不加标记」丢失区分。
    _split_tag = (f"_split{_tx:.0f}x{_ty:.0f}"
                  if (_split_ttest == 1 and _tx > 0.0 and _ty > 0.0) else "")

    _data_tag = (
        f"{_dom_path}"
        f"_Lx{_grid_x}_Ly{_grid_y}_H{_H_val:.3f}"
        f"_{_freq_tag}_spf{_spf}{_split_tag}{_sol_tag}"
    )
    _train_tag = (
        f"ratio{args.train_ratio:.2f}"
        f"_bs{args.batch_size}"
        f"_mi{args.model_index}"
        f"_hc{args.hidden_channels}"
    )
    # ── 实验配置 Tag：区分性能/消融实验，避免覆盖 ──────────────────────────
    #   · 分辨率(H) / 频率(freq_tag) / 范围(Lx,Ly) / 域(rect/wedge) /
    #     源泛化(split_tag, 来自 train_max_x/y) / samples_per_freq
    #     已包含在 _data_tag 中，靠数据集区分的实验天然不会互相覆盖。
    #   · 这里只补 model_type(性能实验) 与 ablation(消融实验)：二者共用同一
    #     R1/W1 数据集，不打 tag 会互相覆盖。proposed+none 不加 tag，保持原
    #     路径不变（对应 Table 3 的 Reuse 语义：性能/消融的 Full/Proposed 行
    #     复用 Forward Solving 结果）。
    _exp_parts = []
    if getattr(args, "model_type", "proposed") != "proposed":
        _exp_parts.append(str(args.model_type))            # deeponet / fno / kno / cno
    if getattr(args, "ablation", "none") != "none":
        _exp_parts.append(str(args.ablation))              # no_prior / no_graph / no_data_loss / no_prior_loss
    _exp_tag = ("_" + "_".join(_exp_parts)) if _exp_parts else ""

    dir_name   = f"train_{_data_tag}__{_train_tag}{_exp_tag}_ddp"
    output_dir = os.path.join(args.output_dir, dir_name)

    if rank == 0:
        # 保存路径(output_dir = args.output_dir/dir_name)已存在则先清空其内容,
        # 避免旧 models/logs/plots/split 残留。只删这个具体实验文件夹,不碰上级。
        import shutil
        _abs_out  = os.path.abspath(output_dir)
        _abs_base = os.path.abspath(args.output_dir)
        # 安全校验:必须严格位于 args.output_dir 之下,且不等于上级目录本身
        _safe = (_abs_out.startswith(_abs_base + os.sep)
                 and _abs_out != _abs_base
                 and os.path.basename(_abs_out) == dir_name)
        if _safe and os.path.isdir(_abs_out):
            # 清空目录内容,但保留 train_test_split.pth (固定划分,供复现)
            for _name in os.listdir(_abs_out):
                if _name == 'train_test_split.pth':
                    continue
                _pth = os.path.join(_abs_out, _name)
                if os.path.isdir(_pth):
                    shutil.rmtree(_pth)
                else:
                    os.remove(_pth)
            _log(f"  [清理] 已清除旧保存目录内容(保留 train_test_split.pth): {_abs_out}")
        os.makedirs(output_dir, exist_ok=True)
        # 目录清理完成后立即建立统一日志文件：
        #   - 头部写入执行命令 + 全部参数 + 时间戳
        #   - 回放 Trainer 创建前的全部 _log 输出（分布式配置/设备/数据集加载等）
        #   - 此后 _log 与 Trainer.self.log 均追加写入同一文件
        _hdr = _build_run_header(_sys.argv)
        _hdr.append("命令行参数 (argparse):")
        for _k, _v in sorted(vars(args).items()):
            _hdr.append(f"  {_k} = {_v}")
        _hdr.append("=" * 70)
        _log_path = _setup_file_logging(output_dir, header_lines=_hdr)
        _log(f"  统一日志文件: {_log_path}")
        _log(f"  训练输出目录: {output_dir}")
    # 分布式:其他 rank 等 rank0 清理+重建完成,避免竞争
    if is_distributed:
        dist.barrier()

    # ── 数据集划分复用 (--reuse_split): 校验合法 → 复制到当前实验目录复用 ──────
    split_file_new = os.path.join(output_dir, 'train_test_split.pth')
    if args.reuse_split is not None:
        _bad = None
        _src = args.reuse_split
        if not os.path.isfile(_src):
            _bad = f"复用划分文件不存在: {_src}"
        else:
            try:
                _chk = torch.load(_src, map_location='cpu')
            except Exception as e:
                _chk = None; _bad = f"复用划分文件无法读取: {_src} ({e})"
            if _bad is None:
                if not (isinstance(_chk, dict)
                        and 'train_indices' in _chk and 'test_indices' in _chk):
                    _bad = f"复用划分文件缺少 train_indices/test_indices: {_src}"
                else:
                    _all = list(_chk['train_indices']) + list(_chk['test_indices'])
                    _n = len(dataset)
                    if len(_all) == 0:
                        _bad = "复用划分索引为空"
                    elif min(_all) < 0 or max(_all) >= _n:
                        _bad = (f"复用划分索引越界(数据集大小 {_n}, "
                                f"索引范围 [{min(_all)},{max(_all)}]): {_src}")
        if _bad is not None:
            if rank == 0:
                _log(f"[错误] --reuse_split 校验失败: {_bad}")
            if is_distributed:
                dist.barrier()
            import sys; sys.exit(1)
        # 合法 → 复制到当前实验目录 (覆盖 split_file_new),后续加载逻辑自然复用
        if rank == 0:
            import shutil
            if os.path.abspath(_src) != os.path.abspath(split_file_new):
                shutil.copy(_src, split_file_new)
            _log(f"✓ 复用数据划分: {_src} → {split_file_new}")
        if is_distributed:
            dist.barrier()
        # 复用优先于 resplit: 既已指定合法复用,强制重划开关失效
        args.resplit = False

    # ── split_file 放在 output_dir 下（不同训练配置互不干扰）────────────────
    # 向后兼容：若旧版 split 文件在 dataset_dir 下也尝试读取
    split_file_old = os.path.join(dataset_dir, 'train_test_split.pth')

    # 数据集是否要求源点空间范围约束划分
    _need_region_split = (_split_ttest == 1 and _tx > 0.0 and _ty > 0.0)

    def _split_is_stale(si: dict) -> bool:
        """已有划分文件是否与数据集约束不符（需重新划分）。
        数据集要求范围约束，但缓存文件不是 source_region 模式（或范围不一致）→ 过期。
        """
        if not _need_region_split:
            return False
        # 兼容历史 'source_region' 及新的 'source_region_splitinfo'/'source_region_coord(_outmix)'
        _mode = str(si.get('split_mode', ''))
        if not _mode.startswith('source_region'):
            return True
        # 范围参数变化也视为过期
        if (abs(float(si.get('train_max_x', -1)) - _tx) > 1e-6 or
                abs(float(si.get('train_max_y', -1)) - _ty) > 1e-6):
            return True
        # outmix 路径：范围外抽样比例/种子变化，或缓存模式与当前 out_train_ratio 期望不符 → 过期
        _want_outmix = float(args.out_train_ratio) > 0.0
        _is_outmix   = (_mode == 'source_region_coord_outmix')
        if _want_outmix != _is_outmix:
            return True
        if _is_outmix:
            return (abs(float(si.get('out_train_ratio', -1)) - float(args.out_train_ratio)) > 1e-9 or
                    int(si.get('split_seed', -1)) != int(args.split_seed))
        return False

    _loaded_split = None
    if os.path.exists(split_file_new) and not args.resplit:
        _cand = torch.load(split_file_new)
        if _split_is_stale(_cand):
            if rank == 0:
                _log(f"⚠ 已有划分 {split_file_new} 与数据集范围约束不符 "
                     f"(需 source_region x≤{_tx:.1f} AND y≤{_ty:.1f})，将重新按约束划分。")
        else:
            _loaded_split = _cand
            if rank == 0:
                _log(f"✓ 加载已有数据划分: {split_file_new}")
    elif os.path.exists(split_file_old) and not args.resplit:
        _cand = torch.load(split_file_old)
        if _split_is_stale(_cand):
            if rank == 0:
                _log(f"⚠ 已有划分（旧路径）{split_file_old} 与数据集范围约束不符，"
                     f"将重新按约束划分。")
        else:
            _loaded_split = _cand
            if rank == 0:
                _log(f"✓ 加载已有数据划分（旧路径兼容）: {split_file_old}")

    if _loaded_split is not None:
        train_indices = _loaded_split['train_indices']
        test_indices  = _loaded_split['test_indices']
    elif _need_region_split:
        # ── 源点空间范围约束划分（来自数据集生成端 train_max_x/train_max_y）──
        # 这是源点空间外推泛化实验的核心约束，必须确定性划分，
        # 不能用 StratifiedShuffleSplit 随机划分（否则约束失效、训练/测试源点混叠）。
        #
        # 优先级 1（默认，范围外泛化划分）：坐标 outmix 路径。
        #   范围内 (x≤tx AND y≤ty) 全部训练；范围外按频率分层随机抽
        #   out_train_ratio (默认 10%) 补入训练、其余作测试。
        #   MATLAB split_info 是「每频率前 n_train 训练」的确定性排布，
        #   无法表达「范围外抽 10%」，故只要 out_train_ratio>0 就优先走坐标路径。
        # 优先级 2（out_train_ratio==0 时）：忠实采用 MATLAB split_info 的排布，
        #   即范围外 100% 作测试（旧行为）。split_info 不可用时回退坐标判定。
        _out_train_ratio = float(args.out_train_ratio)
        freq_idx_all = dataset.frequency_indices.cpu().numpy()
        selected_hz  = [int(round(float(f))) for f in dataset.selected_frequencies]
        use_split_info = (_out_train_ratio <= 0.0 and
                          len(_split_ntrain_by_hz) > 0 and
                          all(selected_hz[fi] in _split_ntrain_by_hz
                              for fi in np.unique(freq_idx_all)))
        train_indices, test_indices = [], []
        if use_split_info:
            for fi in np.unique(freq_idx_all):
                grp = np.where(freq_idx_all == fi)[0]   # 升序全局索引 = HDF5 顺序
                n_tr = int(_split_ntrain_by_hz[selected_hz[int(fi)]])
                n_tr = max(0, min(n_tr, len(grp)))       # 防越界
                train_indices.extend(grp[:n_tr].tolist())
                test_indices.extend(grp[n_tr:].tolist())
            _split_desc = "MATLAB split_info (每频率前 n_train 为训练)"
            _split_mode = 'source_region_splitinfo'
        else:
            # 源点范围外推泛化划分（含范围外少量训练样本）：
            #   · 范围内 (x≤tx AND y≤ty) 全部作训练集。
            #   · 范围外按频率分层随机抽取 out_train_ratio 补入训练集，其余作测试集，
            #     用于检验模型对范围外少量监督的泛化能力。
            #     (out_train_ratio=0 时范围外全部作测试，等价旧行为。)
            #   · 固定种子 (args.split_seed)，逐频率分层，保证可复现且频率间平衡。
            src_xy = dataset.source_positions.cpu().numpy()   # [N, 2] 物理坐标
            in_train_region = (src_xy[:, 0] <= _tx) & (src_xy[:, 1] <= _ty)

            train_indices = np.where(in_train_region)[0].tolist()   # 范围内全部训练
            rng = np.random.default_rng(args.split_seed)
            out_all = np.where(~in_train_region)[0]
            test_indices = []
            n_out_train = 0
            for fi in np.unique(freq_idx_all):
                out_fi = out_all[freq_idx_all[out_all] == fi]   # 该频率的范围外样本
                if len(out_fi) == 0:
                    continue
                k = int(round(len(out_fi) * _out_train_ratio))
                k = max(0, min(k, len(out_fi)))
                perm = rng.permutation(len(out_fi))
                sel_train = out_fi[perm[:k]]
                sel_test  = out_fi[perm[k:]]
                train_indices.extend(sel_train.tolist())
                test_indices.extend(sel_test.tolist())
                n_out_train += len(sel_train)
            train_indices = sorted(train_indices)
            test_indices  = sorted(test_indices)
            _split_desc = (f"源点坐标 范围内(x≤{_tx:.1f} AND y≤{_ty:.1f})全部训练 + "
                           f"范围外按频率分层随机 {_out_train_ratio:.0%} 补入训练"
                           f"(seed={args.split_seed}, 范围外补 {n_out_train} 训练)")
            _split_mode = 'source_region_coord_outmix'
        if rank == 0:
            _log(f"✓ 按源点空间范围约束划分 [{_split_desc}]: "
                 f"训练 {len(train_indices)} / 测试 {len(test_indices)} 样本")
            if len(train_indices) == 0 or len(test_indices) == 0:
                _log(f"  [警告] 范围约束划分后训练集或测试集为空，请检查 "
                     f"train_max_x/y ({_tx}/{_ty}) 或 split_info 是否与数据集匹配。")
            split_indices = {
                'train_indices': train_indices,
                'test_indices':  test_indices,
                'train_size':    len(train_indices),
                'test_size':     len(test_indices),
                'split_mode':    _split_mode,
                'train_max_x':   _tx,
                'train_max_y':   _ty,
            }
            if _split_mode == 'source_region_coord_outmix':
                split_indices['out_train_ratio'] = _out_train_ratio
                split_indices['split_seed']      = args.split_seed
            torch.save(split_indices, split_file_new)
            _log(f"✓ 保存新的数据划分（源点范围约束）: {split_file_new}")
    else:
        sss = StratifiedShuffleSplit(
            n_splits=1, test_size=1 - args.train_ratio,
            random_state=args.split_seed
        )
        train_indices, test_indices = next(
            sss.split(np.arange(len(dataset)), Y)
        )
        train_indices = train_indices.tolist()
        test_indices  = test_indices.tolist()
        if rank == 0:
            split_indices = {
                'train_indices': train_indices,
                'test_indices':  test_indices,
                'train_size':    len(train_indices),
                'test_size':     len(test_indices),
                'split_seed':    args.split_seed,
                'train_ratio':   args.train_ratio,
                'split_mode':    'random_stratified',
            }
            torch.save(split_indices, split_file_new)
            _log(f"✓ 保存新的数据划分: {split_file_new}")

    train_dataset = Subset(dataset, train_indices)
    test_dataset  = Subset(dataset, test_indices)

    # ── 频率过滤（调试开关，在 split 之后执行）──────────────────────────────
    if args.active_freqs is not None:
        active_freq_set = set(args.active_freqs)
        freq_idx_to_hz = {
            i: int(hz) for i, hz in enumerate(dataset.selected_frequencies)
        }

        def _filter_by_freq(indices):
            return [
                idx for idx in indices
                if freq_idx_to_hz[dataset.frequency_indices[idx].item()] in active_freq_set
            ]

        train_indices = _filter_by_freq(train_indices)
        test_indices  = _filter_by_freq(test_indices)
        train_dataset = Subset(dataset, train_indices)
        test_dataset  = Subset(dataset, test_indices)

        if rank == 0:
            _log(f"\n[调试] --active_freqs 频率过滤已启用")
            _log(f"  激活频率: {sorted(active_freq_set)} Hz")
            _log(f"  过滤后训练集: {len(train_indices)} 样本")
            _log(f"  过滤后测试集: {len(test_indices)} 样本")
            _log(f"  注意: 未激活频率的统计列仍会输出，但样本数为 0。")

    if rank == 0:
        _log(f"\n数据集统计:")
        _log(f"  总样本数: {len(dataset)}")
        _log(f"  训练集: {len(train_indices)} 样本")
        _log(f"  测试集: {len(test_indices)} 样本")

    if rank == 0:
        _log("\n" + "=" * 70)
        _log("创建按频率分组的分布式DataLoader")
        _log("=" * 70)
    
    batch_size = args.batch_size
    
    # train_indices / test_indices 已在频率过滤后更新，这两行无需修改
    train_freq_indices = [dataset.frequency_indices[i].item() for i in train_indices]
    test_freq_indices = [dataset.frequency_indices[i].item() for i in test_indices]
    
    if is_distributed:
        train_sampler = DistributedFrequencyGroupedSampler(
            train_freq_indices, batch_size, num_replicas=world_size,
            rank=rank, shuffle=False, seed=args.seed
        )
        test_sampler = DistributedFrequencyGroupedSampler(
            test_freq_indices, batch_size, num_replicas=world_size,
            rank=rank, shuffle=False, seed=args.seed
        )
    else:
        train_sampler = FrequencyGroupedSampler(train_freq_indices, batch_size, shuffle=False)
        test_sampler  = FrequencyGroupedSampler(test_freq_indices,  batch_size, shuffle=False)
    
    train_loader = DataLoader(train_dataset, batch_sampler=train_sampler,
                              num_workers=4, pin_memory=True)
    test_loader  = DataLoader(test_dataset,  batch_sampler=test_sampler,
                              num_workers=4, pin_memory=True)
    
    if rank == 0:
        _log(f"✓ 训练集batches: {len(train_loader)} (per GPU)")
        _log(f"✓ 测试集batches: {len(test_loader)} (per GPU)")

    if rank == 0:
        _log("\n" + "=" * 70)
        _log("创建模型")
        _log("=" * 70)

    p = dataset.nodes.repeat(1, 2).T.to(device)
    mask = create_fixed_mask(unique_xy_keep_order(p).shape[0]).to(device)

    # ══════════════════════════════════════════════════════════════
    # geometry_type 三方一致性校验
    # ══════════════════════════════════════════════════════════════
    _DOMAIN_TO_GEOM = {'right_triangle': 'wedge', 'rectangle': 'rectangle', 'wedge': 'wedge'}

    cli_geom = getattr(args, 'geometry_type', 'auto')
    geom_A   = cli_geom if cli_geom != 'auto' else None

    h5_domain = getattr(dataset, 'domain_shape', None)
    if h5_domain in _DOMAIN_TO_GEOM:
        geom_B = _DOMAIN_TO_GEOM[h5_domain]
    else:
        geom_B = None

    def _auto_detect_geometry(p_tensor: torch.Tensor) -> tuple:
        def _unique_xy(x):
            return torch.unique(x, dim=0)

        pxy = _unique_xy(p_tensor).detach().cpu().to(torch.float64)
        x, y = pxy[:, 0], pxy[:, 1]
        xr = float((x.max() - x.min()).item())
        yr = float((y.max() - y.min()).item())
        if xr <= 1e-8 or yr <= 1e-8:
            return "wedge", 0.0, 1.0

        xn = ((x - x.min()) / xr).clamp(0.0, 1.0)
        yn = ((y - y.min()) / yr).clamp(0.0, 1.0)
        ix = torch.clamp((xn * 31).long(), 0, 31)
        iy = torch.clamp((yn * 31).long(), 0, 31)
        occ = torch.zeros((32, 32), dtype=torch.bool)
        occ[ix, iy] = True
        occ_ratio = float(occ.to(torch.float64).mean().item())

        span_vals = []
        x_edges = torch.linspace(0.0, 1.0, steps=17, dtype=torch.float64)
        for bi in range(16):
            l, r = x_edges[bi], x_edges[bi + 1]
            mb = (xn >= l) & ((xn <= r) if bi == 15 else (xn < r))
            if torch.count_nonzero(mb) < 6:
                continue
            yb = yn[mb]
            span_vals.append(float((yb.max() - yb.min()).item()))
        if len(span_vals) >= 4:
            s   = torch.tensor(span_vals, dtype=torch.float64)
            cv  = float((s.std() / torch.clamp(s.mean(), min=1e-6)).item())
        else:
            cv  = 1.0
        result = "rectangle" if (occ_ratio > 0.55 and cv < 0.35) else "wedge"
        return result, occ_ratio, cv

    _p_nodes = p[:p.shape[0] // 2, :2]
    geom_C, _occ_ratio, _cv = _auto_detect_geometry(_p_nodes)

    _votes = {}
    if geom_A is not None:
        _votes['CLI (--geometry_type)']          = geom_A
    if geom_B is not None:
        _votes[f'h5 metadata (domain_shape={h5_domain!r})'] = geom_B
    _votes[f'auto-detect (occ={_occ_ratio:.3f}, cv={_cv:.3f})'] = geom_C

    _unique_votes = set(_votes.values())
    _consistent   = (len(_unique_votes) == 1)

    if rank == 0:
        _log("")
        _log("┌" + "─" * 62 + "┐")
        _log("│  域形状三方判别结果" + " " * 44 + "│")
        _log("├" + "─" * 62 + "┤")
        _h5_disp  = h5_domain if h5_domain else "N/A（属性缺失）"
        _cli_disp = cli_geom
        _log(f"│  [A] CLI --geometry_type : {_cli_disp:<36}│")
        _log(f"│  [B] h5 domain_shape     : {_h5_disp:<36}│")
        _geom_B_disp = geom_B if geom_B else "N/A（弃权）"
        _log(f"│      → 映射后            : {_geom_B_disp:<36}│")
        _log(f"│  [C] 内部自动检测        : {geom_C:<36}│")
        _log(f"│      occ_ratio={_occ_ratio:.3f}, cv={_cv:.3f}" + " " * 28 + "│")
        _log("├" + "─" * 62 + "┤")
        if _consistent:
            _final = next(iter(_unique_votes))
            _prior = "RectFieldNet" if _final == "rectangle" else "WedgeFieldNet"
            _log(f"│  ✓ 三方一致  →  geometry_type = {_final:<28}│")
            _log(f"│               prior network   = {_prior:<28}│")
        else:
            _log("│  ✗ 判别结果不一致，详见下方冲突列表" + " " * 26 + "│")
        _log("└" + "─" * 62 + "┘")
        _log("")

    if not _consistent:
        if rank == 0:
            _log("═" * 64)
            _log("  [错误] 域形状三方判别结果不一致，无法确定使用哪种先验网络。")
            _log("  冲突详情：")
            for _src, _val in _votes.items():
                _log(f"    {_src:<45} → {_val}")
            _log("")
            _log("  请通过以下方式解决冲突：")
            _log("  方案1（推荐）：不传 --geometry_type，让程序自动从 h5 元数据读取。")
            _log("  方案2：显式传入与 h5 元数据及数据分布一致的值：")
            _log("    --geometry_type wedge      （楔形域）")
            _log("    --geometry_type rectangle  （矩形域）")
            _log("  方案3：若 h5 元数据有误，用 --geometry_type 强制覆盖，")
            _log("          但需确认与实际数据域形状吻合。")
            _log("═" * 64)
        if is_distributed:
            dist.barrier()
        import sys
        sys.exit(1)

    geometry_type = next(iter(_unique_votes))

    # ===== 性能测试 / 消融实验：模型与 loss 选择 =====
    _use_prior = (args.ablation != 'no_prior')
    _use_graph = (args.ablation != 'no_graph')
    if args.ablation == 'no_data_loss':
        args.loss_w_rel_mse = 0.0
    elif args.ablation == 'no_prior_loss':
        args.loss_w_prior = 0.0

    if args.model_type == 'proposed':
        model = GNNModel_Forward(
            p=p,
            mask=mask,
            edge_index=edge_index,
            edge_attr=edge_attr,
            interm_channels=args.hidden_channels,
            in_channels=dataset.num_nodes * 2,
            model_index=args.model_index,
            k_list=dataset.selected_frequencies.tolist(),
            test_index=args.test_index,
            ellipse_params=dataset.ellipse_params,
            geometry_type=geometry_type,
            use_physics_prior=_use_prior,
            use_multi_scale_graph=_use_graph,
        )
    elif args.model_type == 'deeponet':
        model = DeepONetBaseline(
            p=p, k_list=dataset.selected_frequencies.tolist(),
            geometry_type=geometry_type, hidden=128, latent=128)
    elif args.model_type == 'fno':
        model = FNO2DBaseline(
            p=p, k_list=dataset.selected_frequencies.tolist(),
            geometry_type=geometry_type, grid=64, width=32, modes=16)
    elif args.model_type == 'kno':
        model = KNOBaseline(
            p=p, k_list=dataset.selected_frequencies.tolist(),
            geometry_type=geometry_type, grid=64, width=32, modes=16,
            koopman_steps=4)
    elif args.model_type == 'cno':
        model = CNOBaseline(
            p=p, k_list=dataset.selected_frequencies.tolist(),
            geometry_type=geometry_type, grid=64, width=32, n_levels=2)
    else:
        raise ValueError(f'未知 model_type: {args.model_type}')

    if rank == 0:
        _log(f'  [实验配置] model_type={args.model_type}, ablation={args.ablation}, '
             f'loss_w_rel_mse={args.loss_w_rel_mse}')

    if rank == 0:
        _log(f"  总参数量: {sum(p.numel() for p in model.parameters()):,}")
        _log(f"  可训练参数: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
        if dataset.ellipse_params is not None:
            ep = dataset.ellipse_params
            _log(f"  椭圆内边界: 中心=({ep['cx']:.1f},{ep['cy']:.1f}), "
                 f"a={ep['a']:.1f} m, b={ep['b']:.1f} m → 内边界硬约束已启用")

    if rank == 0:
        _log("\n" + "=" * 70)
        _log("开始训练")
        _log("=" * 70)
    
    trainer = AcousticTrainer(
        model=model,
        mask=mask,
        train_loader=train_loader,
        test_loader=test_loader,
        dataset=dataset,
        edge_index=edge_index,
        A_coo_data_dict=dataset.A_coo_data_dict,
        output_dir=output_dir,
        device=device,
        rank=rank,
        world_size=world_size,
        loss_w_rel_mse=args.loss_w_rel_mse,
        loss_w_prior=args.loss_w_prior,
    )

    # 训练前：按频率各画一张训练/测试源点划分示意图（不同颜色区分），
    # 输出到 output_dir/plots，方便用户判断数据划分是否符合预期。
    trainer.visualize_train_test_split(train_indices, test_indices)

    trainer.train(args.epochs)

    if args.distributed and is_distributed:
        cleanup_distributed()

# ==================== 命令行接口 ====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='训练多频率海洋声学GNN求解器(频率分组批次)'
    )
    
    parser.add_argument('--data_dir', type=str, required=True,
                        help='数据集根目录')
    parser.add_argument('--dataset_name', type=str, required=True,
                        help='数据集名称')
    parser.add_argument('--output_dir', type=str, 
                        default='./acoustic_training_results/Forward/',
                        help='输出目录路径')
    parser.add_argument('--epochs', type=int, default=200,
                        help='训练轮数')
    parser.add_argument('--batch_size', type=int, default=1, 
                        help='批大小')
    parser.add_argument('--train_ratio', type=float, default=0.9,
                        help='训练集比例')
    parser.add_argument('--split_seed', type=int, default=42,
                        help='数据划分随机种子')
    parser.add_argument('--out_train_ratio', type=float, default=0.10,
                        help='源点范围外推划分中,范围外样本随机补入训练集的比例 '
                             '(默认0.10,即范围外抽10%%作训练、90%%作测试)。'
                             '设为0则范围外全部作测试(旧行为)。仅在坐标划分路径生效。')
    parser.add_argument('--resplit', action='store_true',
                        help='强制重新划分数据集')
    parser.add_argument('--reuse_split', type=str, default=None,
                        help='复用已有数据划分文件路径 (.pth)。指定后将校验合法性,'
                             '合法则复制到当前实验目录复用;不合法则退出。默认 None(不启用)。')
    parser.add_argument('--model_index', type=int, default=4,
                        help='模型类型索引')
    parser.add_argument('--test_index', type=int, default=0,
                        help='测试类型索引')
    parser.add_argument('--hidden_channels', type=int, default=48,
                        help='隐藏层通道数')
    parser.add_argument('--seed', type=int, default=123,
                        help='全局随机种子')
    parser.add_argument('--distributed', action='store_true',
                        help='启用分布式训练（自动检测GPU数量）')
    parser.add_argument('--local_rank', type=int, default=0,
                        help='本地GPU编号（由torch.distributed.launch自动设置）')
    parser.add_argument('--loss_w_rel_mse', type=float, default=1.0e2,
                        help='相对复数 MSE 项权重（数据驱动主项）。与 --loss_w_prior '
                             '搭配的推荐平衡比例为 100:1，即 prior 权重为 1 时此项为 1e2。')
    parser.add_argument('--model_type', type=str, default='proposed',
                        choices=['proposed', 'deeponet', 'fno', 'kno', 'cno'],
                        help='性能测试模型: proposed=完整方法 | deeponet | fno | '
                             'kno=Koopman算子 | cno=卷积算子 '
                             '(COMSOL 为参考数据本身,无需此项)')
    parser.add_argument('--ablation', type=str, default='none',
                        choices=['none', 'no_prior', 'no_graph',
                                 'no_data_loss', 'no_prior_loss'],
                        help='消融: none=完整 | no_prior=去物理先验 | no_graph=去多尺度图 '
                             '| no_data_loss(=--loss_w_rel_mse 0) '
                             '| no_prior_loss(=--loss_w_prior 0)')
    parser.add_argument('--loss_w_prior', type=float, default=1.0,
                        help='physics_prior vs true solution MSE loss 权重（基准=1，'
                             '与 --loss_w_rel_mse=1e2 构成推荐平衡比例 100:1）')
    parser.add_argument(
        '--geometry_type', type=str, default='auto',
        choices=['auto', 'wedge', 'rectangle'],
        help=(
            '物理先验网络的几何类型。\n'
            '  auto      : 优先读取 h5 元数据 domain_shape，'
            '若缺失则由模型自动检测节点分布（默认）。\n'
            '  wedge     : 强制使用楔形先验 WedgeFieldNet。\n'
            '  rectangle : 强制使用矩形先验 RectFieldNet。\n'
            '优先级: --geometry_type (非auto) > h5 domain_shape > 自动检测。'
        ),
    )
    # ==================== 新增：频率过滤调试开关 ====================
    parser.add_argument(
        '--active_freqs', type=int, nargs='+', default=None,
        metavar='HZ',
        help=(
            '只使用指定频率的样本进行训练和评估（调试用）。\n'
            '可指定 1~4 个频率，例：\n'
            '  --active_freqs 25          （只用 25Hz）\n'
            '  --active_freqs 25 50       （只用 25Hz 和 50Hz）\n'
            '  --active_freqs 25 50 75 100（使用全部四个频率，等价于不传）\n'
            '不传此参数时使用数据集中全部频率（默认行为不变）。\n'
            '注意：划分文件 train_test_split.pth 保存的是全量索引，\n'
            '      频率过滤在加载后进行，不会污染划分文件。'
        ),
    )
    # =============================================================

    args = parser.parse_args()
    
    main(args)