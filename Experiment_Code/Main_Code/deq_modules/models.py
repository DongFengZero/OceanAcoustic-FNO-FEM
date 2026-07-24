"""
====================================================================
两阶段声场预测模型 (Physics Prior + FEM-Guided GNN + Fusion)
====================================================================

整体结构按三个机制组织,每个机制对应一个 Part:

    Part 1  物理先验网络 (Physics Prior)
            _FNOScatterField   FNO 直出先验 (全局谱算子)
            输入: 频率 + 声源坐标 (高斯图) + 网格坐标
            输出: 近似压力场 (实虚部拼接) [B, 2N]

    Part 2  有限元残差引导的图网络 (FEM-Guided GNN)
            GraphFeatureEncoder      节点+边编码器 (场值/坐标/edge_attr → 场修正)
            AdaptiveMultiScaleGraphConv   多尺度 (1/2/4/8 跳) FEM 图卷积
            FEMGuidedGraphNet        把上述两者串联,用 FEM 残差驱动更新
            输入: 物理先验场 + FEM 边权 (A) 与右端项 (B)
            输出: 经 FEM 残差修正后的场 [B, 2N]

    Part 3  先验-FEM 融合 (Prior-FEM Fusion)
            PriorFEMFusion   频率自适应 gate 融合两路场
            输出: 最终预测场

顶层装配:
    PhysicsFEMForwardLayer  把三部分按顺序接起来
    GNNModel_Forward        训练入口,trainer 直接构造的类

trainer 兼容接口:
    GNNModel_Forward(...).forward(...) -> (pred, pred, x_dep, residual)
    (residual 恒为 0 占位, FEM 残差诊断已废弃)
    model.implicit_layer._nf_node_weight_2n      # 椭圆障碍权重,日志用
"""

import math
import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import MessagePassing


# =============================================================================
# Section 0. 共用工具
# =============================================================================

def as_edge_index(edge_index: torch.Tensor) -> torch.Tensor:
    """把 edge_index 归一化为 [2, E] 形状。"""
    return edge_index.squeeze(0) if edge_index.dim() == 3 else edge_index


def as_edge_attr(edge_attr: torch.Tensor) -> torch.Tensor:
    """把 edge_attr 归一化为 [E] 形状。"""
    if edge_attr.dim() == 3:
        return edge_attr.squeeze(0).squeeze(-1)
    if edge_attr.dim() == 2:
        return edge_attr.squeeze(0) if edge_attr.shape[0] == 1 else edge_attr.squeeze(-1)
    return edge_attr


def zero_realified_interior(x: torch.Tensor, mask_n: torch.Tensor | None) -> torch.Tensor:
    """实虚拼接场 [B, 2N] 在 mask_n 标记的"障碍内部"节点置零。"""
    if mask_n is None:
        return x
    n = x.shape[1] // 2
    m = mask_n.to(x.device)
    x = x.clone()
    x[:, :n][:, m] = 0.0
    x[:, n:][:, m] = 0.0
    return x


# =============================================================================
#                                                                              #
#  Part 1.  Physics Prior Network (物理先验)                                   #
#                                                                              #
#  FNO 直出先验:看【声源高斯图 + 坐标 + 频率】,由全局谱算子直接产出一路      #
#  完整的近似声场,作为后续 FEM 引导图网络的初值。                             #
#                                                                              #
# =============================================================================


# -----------------------------------------------------------------------------
# 1.1  FNO 直出先验场
# -----------------------------------------------------------------------------

class _FNOScatterField(nn.Module):
    """FNO-2D 全局算子:作为 Stage-1 物理先验的直出网络 (forward_source)。

    FNO 是全局算子 (FFT 全场耦合),看【源高斯图 + 坐标 + 频率】直接输出全场
    压力先验 (实/虚)。PhysicsFEMForwardLayer.forward 调 forward_source 得到
    physics_prior,再送入 Stage-2 FEM 引导 GNN。

    forward_source 输入通道 (栅格化到 grid×grid): [源高斯图, 源高斯图, x, y, freq]。
    输出 [B,N,2] (实/虚),采样回节点 node_xy(=p_single)。
    复用 _SpectralConv2d (实数存复权重,规避 NCCL 复数广播)。

    注: 另有 forward(prior_real, prior_imag, freq) 接口 (输入已有场做散射修正),
    历史遗留自简正波方案,当前主路径只用 forward_source。
    """
    def __init__(self, node_xy: torch.Tensor, freq_list,
                 grid: int = 64, width: int = 32, modes: int = 16,
                 n_layers: int = 4, k_nn: int = 8):
        super().__init__()
        node_xy_t = node_xy.detach().to(dtype=torch.float64).cpu()[:, :2]
        self.N    = node_xy_t.shape[0]
        self.grid = int(grid)
        self.width = int(width)
        self.freq_list = sorted([float(f) for f in freq_list])

        x_min = float(node_xy_t[:, 0].min()); x_max = float(node_xy_t[:, 0].max())
        y_min = float(node_xy_t[:, 1].min()); y_max = float(node_xy_t[:, 1].max())
        Lx = max(x_max - x_min, 1e-6); Ly = max(y_max - y_min, 1e-6)
        gx = (node_xy_t[:, 0] - x_min) / Lx * 2 - 1
        gy = (node_xy_t[:, 1] - y_min) / Ly * 2 - 1
        self.register_buffer("_samp_grid_f32",
                             torch.stack([gx, gy], dim=-1).float().view(1, self.N, 1, 2))
        self.register_buffer("_xy_min", torch.tensor([x_min, y_min], dtype=torch.float64))
        self.register_buffer("_Lxy",    torch.tensor([Lx, Ly], dtype=torch.float64))
        ys, xs = torch.meshgrid(
            torch.linspace(0.0, 1.0, self.grid, dtype=torch.float64),
            torch.linspace(0.0, 1.0, self.grid, dtype=torch.float64), indexing="ij")
        self.register_buffer("_coord", torch.stack([xs, ys], dim=0))
        grid_xy = torch.stack([x_min + xs.reshape(-1) * Lx,
                               y_min + ys.reshape(-1) * Ly], dim=-1)  # [G,2]
        # 解析场 node→grid 栅格化 (kNN 反距离, gather+sum, 不用 sparse → DDP 安全)
        k_nn = min(int(k_nn), self.N)
        with torch.no_grad():
            d = torch.cdist(grid_xy, node_xy_t)
            knn_d, knn_i = torch.topk(d, k_nn, dim=1, largest=False)
            w = 1.0 / (knn_d + 1e-6)
            w = w / w.sum(dim=1, keepdim=True)
        self.register_buffer("_W_idx", knn_i.long())     # [G,k]
        self.register_buffer("_W_val", w.to(torch.float64))  # [G,k]

        self.lift  = nn.Linear(5, self.width).double()    # 解析实/虚 + x + y + 频率
        self.specs = nn.ModuleList([
            _SpectralConv2d(self.width, self.width, modes, modes)
            for _ in range(max(1, n_layers))]).double()
        self.ws    = nn.ModuleList([
            nn.Conv2d(self.width, self.width, 1) for _ in range(max(1, n_layers))]).double()
        self.proj1 = nn.Linear(self.width, 128).double()
        self.proj2 = nn.Linear(128, 2).double()
        # 全幅 FNO 路径: proj2 用小随机初始化 (非零),让 FNO 从起点即有可学信号;
        # 幅度由 fno_scale (可学,初值 0.3) + RMS 锚定 + max_frac 上限共同约束。
        nn.init.normal_(self.proj2.weight, std=1e-2)
        nn.init.zeros_(self.proj2.bias)
        self.fno_scale = nn.Parameter(torch.tensor(0.3, dtype=torch.float64))

    def _freq_hz(self, freq_hz) -> float:
        return float(freq_hz)

    def _spec_proj(self, inp):
        """grid 输入 [B,H,W,5] → FNO 谱算子 → 采样回节点 [B,N,2]。"""
        Bsz, dev = inp.shape[0], inp.device
        x = self.lift(inp).permute(0, 3, 1, 2).contiguous()
        for spc, w in zip(self.specs, self.ws):
            x = F.gelu(spc(x) + w(x))
        x = x.permute(0, 2, 3, 1)
        x = self.proj2(F.gelu(self.proj1(x)))                # [B,H,W,2]
        x = x.permute(0, 3, 1, 2).contiguous()               # [B,2,H,W]
        grid = self._samp_grid_f32.to(dev).expand(Bsz, -1, -1, -1).float()
        samp = F.grid_sample(x.float(), grid, mode="bilinear",
                             align_corners=True).squeeze(-1).double()  # [B,2,N]
        return samp.permute(0, 2, 1).contiguous()            # [B,N,2]

    def forward_source(self, source_xy, freq_hz):
        """纯 FNO 直出 (不用解析解): 输入 = [源高斯图, 源高斯图, x, y, 频率]。
        source_xy: [B,2] 物理坐标;返回 [B,N,2]。"""
        Bsz, dev = source_xy.shape[0], source_xy.device
        H = W = self.grid
        coord = self._coord.to(dev)
        xy_min = self._xy_min.to(dev); Lxy = self._Lxy.to(dev)
        xs = xy_min[0] + coord[0] * Lxy[0]
        ys = xy_min[1] + coord[1] * Lxy[1]
        sx = source_xy[:, 0].view(Bsz, 1, 1)
        sy = source_xy[:, 1].view(Bsz, 1, 1)
        sigma = 0.05 * float(max(Lxy[0].item(), Lxy[1].item()))
        gauss = torch.exp(-((xs - sx) ** 2 + (ys - sy) ** 2) / (2 * sigma ** 2))
        fhz = float(freq_hz) / 100.0
        fmap = torch.full((Bsz, H, W), fhz, device=dev, dtype=torch.float64)
        inp = torch.stack([gauss, gauss,
                           coord[0].expand(Bsz, H, W),
                           coord[1].expand(Bsz, H, W),
                           fmap], dim=-1)                     # [B,H,W,5]
        return self._spec_proj(inp)

    def forward(self, prior_real, prior_imag, freq_hz):
        """prior_real/imag: [B,N] 解析场;freq_hz: 频率(Hz);返回散射残差 [B,N,2] (未限幅)。"""
        Bsz, dev, dt = prior_real.shape[0], prior_real.device, prior_real.dtype
        H = W = self.grid
        coord = self._coord.to(dev)
        idx = self._W_idx.to(dev)
        val = self._W_val.to(device=dev, dtype=dt)
        Gg, kk = idx.shape[0], idx.shape[1]
        fi = idx.reshape(-1)
        gr = (prior_real[:, fi].reshape(Bsz, Gg, kk) * val).sum(-1).reshape(Bsz, H, W)
        gi = (prior_imag[:, fi].reshape(Bsz, Gg, kk) * val).sum(-1).reshape(Bsz, H, W)
        fhz = float(freq_hz) / 100.0
        fmap = torch.full((Bsz, H, W), fhz, device=dev, dtype=torch.float64)
        inp = torch.stack([gr, gi,
                           coord[0].expand(Bsz, H, W),
                           coord[1].expand(Bsz, H, W),
                           fmap], dim=-1)                     # [B,H,W,5]
        return self._spec_proj(inp)


# =============================================================================
#                                                                              #
#  Part 2.  FEM-Guided Graph Network (有限元残差引导的图网络)                  #
#                                                                              #
#  阶段 1 已经给出近似 (但带有 FEM 离散误差、椭圆散射等不理想效应) 的场;       #
#  本部分把这个场作为初值,通过 FEM 系统矩阵 (A,B) 计算残差 r = B-Au,然后      #
#  在 FEM 邻接图上做多尺度图卷积,把残差转换为对场的修正。                     #
#                                                                              #
# =============================================================================


# -----------------------------------------------------------------------------
# 2.1  多尺度 FEM 图卷积
# -----------------------------------------------------------------------------

class AdaptiveMultiScaleGraphConv(nn.Module):
    """1/2/4/8 跳邻接的 FEM 图卷积,长程跳数由 (FEM 邻接矩阵)^k 预计算并稀疏化。

    每个分支对 (聚合-自身) 残差做线性投影 + GELU + 残差,再以可学频率敏感
    权重 alpha 加权求和。长程聚合做了入度归一化(与 1-hop 对齐)。
    """
    def __init__(self, feat_dim: int, n_branches: int = 4,
                 hidden_dim: int = 64, power_keys: list | None = None,
                 sparsify_topk: int = 16):
        super().__init__()
        self.feat_dim      = feat_dim
        self.n_branches    = n_branches
        self.sparsify_topk = sparsify_topk
        hd = hidden_dim

        if power_keys is None:
            power_keys = [2, 4, 8]
        assert len(power_keys) == n_branches - 1
        self.power_keys = power_keys

        self._power_edges:   dict = {}      # 长程边 (src, dst, weight)
        self._power_deg_inv: dict = {}      # 长程入度逆

        self.branch_proj = nn.ModuleList([nn.Linear(feat_dim, hd) for _ in range(n_branches)])
        self.branch_norm = nn.ModuleList([nn.LayerNorm(hd) for _ in range(n_branches)])
        self.dil_proj    = nn.ModuleList([nn.Linear(hd, hd, bias=False) for _ in range(n_branches)])
        self.back_proj   = nn.ModuleList([
            nn.Linear(hd, feat_dim, bias=False) for _ in range(n_branches - 1)])
        self.branch_logits = nn.Parameter(torch.zeros(n_branches, dtype=torch.float64))
        self.final_proj    = nn.Linear(hd, feat_dim)

        self._deg_inv: torch.Tensor | None = None    # 1-hop 入度逆
        self._cached_n: int = -1

        for mod in (self.branch_proj, self.branch_norm,
                    self.dil_proj, self.back_proj, self.final_proj):
            mod.to(torch.float64)

    @staticmethod
    def _build_power_edges(src_np, dst_np, ea_np, k, n_nodes, topk):
        """计算 A^k 后按每行 top-k 稀疏化。"""
        import scipy.sparse as sp
        A = sp.csr_matrix(
            (ea_np.astype(np.float32), (dst_np, src_np)),
            shape=(n_nodes, n_nodes))
        row_sum = np.array(A.sum(axis=1)).flatten()
        row_sum = np.where(row_sum > 0, row_sum, 1.0)
        A_norm  = sp.diags(1.0 / row_sum) @ A
        Ak = A_norm
        for _ in range(k - 1):
            Ak = Ak @ A_norm
        Ak = Ak.tocsr()
        rows_out, cols_out, vals_out = [], [], []
        for row in range(n_nodes):
            s, e = Ak.indptr[row], Ak.indptr[row + 1]
            if s == e: continue
            ci = Ak.indices[s:e]; vi = Ak.data[s:e]
            if len(vi) > topk:
                top_pos = np.argpartition(np.abs(vi), -topk)[-topk:]
                ci, vi  = ci[top_pos], vi[top_pos]
            rows_out.append(np.full(len(ci), row, dtype=np.int64))
            cols_out.append(ci.astype(np.int64))
            vals_out.append(vi.astype(np.float64))
        if not rows_out:
            return (torch.zeros(0, dtype=torch.int64),
                    torch.zeros(0, dtype=torch.int64),
                    torch.zeros(0, dtype=torch.float64))
        return (torch.from_numpy(np.concatenate(cols_out)),
                torch.from_numpy(np.concatenate(rows_out)),
                torch.from_numpy(np.concatenate(vals_out)))

    def set_graph(self, src, dst, ea, n_nodes):
        """构造所有 power_keys 的长程边 + 度归一化,在 __init__ 之后调用一次。"""
        src_np = src.cpu().numpy()
        dst_np = dst.cpu().numpy()
        ea_np  = ea.cpu().float().numpy()

        for k in self.power_keys:
            ps, pd, pa = self._build_power_edges(
                src_np, dst_np, ea_np, k, n_nodes, self.sparsify_topk)
            self._power_edges[k] = (ps, pd, pa)
            if pd.shape[0] > 0:
                deg_k = np.zeros(n_nodes, dtype=np.float64)
                np.add.at(deg_k, pd.numpy(), np.abs(pa.numpy()))
                deg_k = np.where(deg_k > 0, deg_k, 1.0)
                self._power_deg_inv[k] = torch.from_numpy(1.0 / deg_k)
            else:
                self._power_deg_inv[k] = torch.ones(n_nodes, dtype=torch.float64)

        ea_abs = np.abs(ea_np).astype(np.float64)
        deg    = np.zeros(n_nodes, dtype=np.float64)
        np.add.at(deg, dst_np, ea_abs)
        deg = np.where(deg > 0, deg, 1.0)
        self._deg_inv  = torch.from_numpy(1.0 / deg)
        self._cached_n = n_nodes

    def _precompute_deg(self, dst, ea, n):
        """退化路径:set_graph 未调用时的 1-hop 度归一化兜底。"""
        ea_1d = ea.abs() if ea.dim() == 1 else ea.abs().mean(0)
        deg   = ea_1d.new_zeros(n)
        deg.scatter_add_(0, dst, ea_1d)
        self._deg_inv  = 1.0 / deg.clamp(min=1.0)
        self._cached_n = n

    @staticmethod
    def _scatter_agg(x, src, dst, ea, deg_inv, n_nodes):
        """1-hop scatter: out[j] = Σ_i ea[i→j] · x[i],再按入度归一化。"""
        B        = x.shape[0]
        src_vals = x[:, src]
        weighted = ea.unsqueeze(0) * src_vals if ea.dim() == 1 else ea * src_vals
        out = torch.zeros(B, n_nodes, dtype=x.dtype, device=x.device)
        out.scatter_add_(1, dst.unsqueeze(0).expand(B, -1), weighted)
        return out * deg_inv.unsqueeze(0)

    def forward(self, x, src, dst, ea, alpha_bias=None):
        n, dev = x.shape[1], x.device
        if self._deg_inv is None or self._cached_n != n:
            self._precompute_deg(dst, ea, n)
        deg_inv = self._deg_inv.to(dev)

        # 分支权重 (可加频率自适应偏置)
        if alpha_bias is None:
            alphas, alpha_mode = torch.softmax(self.branch_logits, dim=0), "global"
        elif alpha_bias.dim() == 1:
            alphas, alpha_mode = torch.softmax(
                self.branch_logits + alpha_bias.to(dev), dim=0), "global"
        else:
            alphas, alpha_mode = torch.softmax(
                self.branch_logits.unsqueeze(0) + alpha_bias.to(dev), dim=1), "batch"

        branch_outs = []
        cumulative  = torch.zeros_like(x)
        for i in range(self.n_branches):
            z_i = x + cumulative

            if i == 0:
                # 1-hop 分支: (Az - z) = 用邻居均值替换自身的偏差
                A1z   = self._scatter_agg(z_i, src, dst, ea, deg_inv, n)
                agg_i = A1z - z_i
            else:
                # k-hop 分支: 同样取相对偏差 (A^k z - Az)
                k          = self.power_keys[i - 1]
                ps, pd, pa = self._power_edges[k]
                ps, pd, pa = ps.to(dev), pd.to(dev), pa.to(dev)
                B_ = z_i.shape[0]
                agg_k = torch.zeros(B_, n, dtype=z_i.dtype, device=dev)
                agg_k.scatter_add_(
                    1, pd.unsqueeze(0).expand(B_, -1), pa.unsqueeze(0) * z_i[:, ps])
                agg_k = agg_k * self._power_deg_inv[k].to(dev).unsqueeze(0)
                A1z_i = self._scatter_agg(z_i, src, dst, ea, deg_inv, n)
                agg_i = agg_k - A1z_i

            y_i   = F.gelu(self.branch_norm[i](self.branch_proj[i](agg_i + z_i)))
            out_i = y_i + self.dil_proj[i](y_i)
            branch_outs.append(
                alphas[i] * out_i if alpha_mode == "global"
                else alphas[:, i].unsqueeze(1) * out_i)
            if i < self.n_branches - 1:
                cumulative = cumulative + self.back_proj[i](out_i)

        return self.final_proj(sum(branch_outs))


# -----------------------------------------------------------------------------
# 2.2  FEM 残差引导的图网络主体
# -----------------------------------------------------------------------------

class FEMGuidedGraphNet(MessagePassing):
    """阶段 2 主网络。把"节点/边编码器 + 1-hop 图卷积 + FEM 残差"按下式串联:

        net_x  = net(x)                          # 节点/边编码器先给出修正方向
        x_proc = x - net_x
        ms_agg = ms_conv(x_proc, A)              # 1-hop 图聚合
        out    = x_proc + 0.01 * (B - ms_agg)    # FEM 残差驱动一步更新
        return out + net(out)                    # 节点/边编码器精修
    """
    def __init__(self, edge_index, p, interm_channels, freq_list):
        super().__init__(aggr="add")
        self.edge_index_all  = edge_index
        self.freq_list       = freq_list
        self.p               = p
        self.interm_channels = interm_channels
        self._interior_mask  = None

        feat_dim = p.shape[0]
        # 恢复 1/2/4/8 四跳多尺度分支
        self.ms_conv = AdaptiveMultiScaleGraphConv(
            feat_dim=feat_dim, n_branches=1, hidden_dim=interm_channels,
            power_keys=[], sparsify_topk=16,
        )
        # 每个频率一份分支偏置 (零初始) → 让不同频率自适应使用不同跳数尺度
        self.freq_branch_alpha = nn.Embedding(
            num_embeddings=max(1, len(self.freq_list)),
            embedding_dim=self.ms_conv.n_branches,
        ).to(torch.float64)
        nn.init.zeros_(self.freq_branch_alpha.weight)
        # 注: ms_conv.set_graph 在外层 PhysicsFEMForwardLayer.__init__ 末尾调用,
        #     因为只有在那里才能拿到带正确维度的 edge_attr[0]。

    def set_interior_mask(self, mask_2n: torch.Tensor | None):
        if mask_2n is None:
            self._interior_mask = None
        else:
            self._interior_mask = mask_2n[: mask_2n.shape[0] // 2].cpu()

    def _zero(self, x: torch.Tensor) -> torch.Tensor:
        return zero_realified_interior(x, self._interior_mask)

    def _call_net(self, x, net, index, src, dst, ea):
        """调用节点/边编码器时兼容多种签名,避免上游接口耦合死。"""
        try:
            return net(x, freq_idx=index, src=src, dst=dst, edge_attr=ea)
        except TypeError:
            try:
                return net(x, index, src, dst, ea)
            except TypeError:
                return net(x)

    def forward(self, x, index, B, A, x_dep, net, opt=0):
        x   = self._zero(x)
        ei  = as_edge_index(self.edge_index_all[index])
        ea  = as_edge_attr(A)
        src, dst = ei[0], ei[1]

        # Step 1: 节点/边编码器给出修正方向
        net_x  = self._call_net(x, net, index, src, dst, ea)
        x_proc = x - net_x

        # Step 2: 1-hop 图聚合 + FEM 残差驱动一步更新
        idx_t      = torch.tensor(int(index), dtype=torch.long, device=x.device)
        alpha_bias = self.freq_branch_alpha(idx_t)
        ms_agg     = self.ms_conv(x_proc, src, dst, ea, alpha_bias=alpha_bias)
        residual   = B - ms_agg
        out        = x_proc + 1e-2 * residual

        # Step 3: 节点/边编码器再做一次精修
        net_out = self._call_net(out, net, index, src, dst, ea)
        return self._zero(out + net_out)

    # PyG 接口 (父类要求,但本类 forward 不调用 propagate)
    def message(self, x_j, edge_attr):
        return edge_attr * x_j

    def update(self, aggr_out, x, B):
        residual = B - aggr_out
        return (x.transpose(0, 1) + 1e-2 * residual.transpose(0, 1)).transpose(0, 1)


# =============================================================================
#                                                                              #
#  Part 3.  Prior-FEM Fusion (融合)                                            #
#                                                                              #
#  阶段 1 输出 physics_prior (物理上正确但 FEM 系统残差大);                    #
#  阶段 2 输出 gnn_out      (FEM 残差小但近场可能过冲);                        #
#  融合层用频率自适应 gate + 残差幅度门控混合两者,起点偏向 prior 保持稳定,    #
#  训练中根据频率/场量级动态调整。                                            #
#                                                                              #
# =============================================================================

class PriorFEMFusion(nn.Module):
    """频率/场量级自适应融合:
        out = gate·prior + (1-gate)·(prior + scale_eff · (gnn - prior))
        gate     = σ(freq_to_gate(f_emb) + field_to_gate(field_stats))
        scale_eff = tanh(freq_to_scale + field_to_scale) · exp(intensity · |log_scale_max|)

    field_stats: [prior_mean, gnn_mean, prior_std, gnn_std, residual_std]
    所有 head 零初始化 → 起点 gate≈0.38、scale_eff≈0.1·1.0,以 prior 为锚。
    """
    def __init__(self, n_freq: int, embed_dim: int = 8):
        super().__init__()
        self.freq_embed = nn.Embedding(n_freq, embed_dim)
        nn.init.normal_(self.freq_embed.weight, std=0.01)

        self.freq_to_gate = nn.Linear(embed_dim, 1)
        nn.init.zeros_(self.freq_to_gate.weight)
        nn.init.constant_(self.freq_to_gate.bias, -0.5)   # 初始 gate ≈ 0.38

        self.field_to_gate = nn.Linear(5, 1)
        nn.init.zeros_(self.field_to_gate.weight)
        nn.init.zeros_(self.field_to_gate.bias)

        self.field_to_scale = nn.Linear(5, 1)
        nn.init.zeros_(self.field_to_scale.weight)
        nn.init.zeros_(self.field_to_scale.bias)

        self.freq_to_scale = nn.Linear(embed_dim, 1)
        nn.init.zeros_(self.freq_to_scale.weight)
        nn.init.constant_(self.freq_to_scale.bias, 0.1)

        self.freq_to_intensity = nn.Linear(embed_dim, 1)
        nn.init.zeros_(self.freq_to_intensity.weight)
        nn.init.zeros_(self.freq_to_intensity.bias)

        self.log_scale_max = nn.Parameter(torch.tensor(1.0, dtype=torch.float64))

        for m in (self.freq_embed, self.freq_to_gate, self.field_to_gate,
                  self.field_to_scale, self.freq_to_scale, self.freq_to_intensity):
            m.to(torch.float64)

    def forward(self, physics, gnn, freq_idx: int):
        B     = physics.shape[0]
        f_idx = torch.tensor(freq_idx, dtype=torch.long, device=physics.device)
        f_emb = self.freq_embed(f_idx).unsqueeze(0).expand(B, -1)

        # 场量级统计 (mean/std + residual std)
        p_mean = physics.mean(dim=1, keepdim=True)
        g_mean = gnn.mean(dim=1, keepdim=True)
        p_std  = physics.std(dim=1, keepdim=True, unbiased=False)
        g_std  = gnn.std(dim=1, keepdim=True, unbiased=False)
        r_std  = (gnn - physics).std(dim=1, keepdim=True, unbiased=False)
        field_feat = torch.cat([p_mean, g_mean, p_std, g_std, r_std], dim=1)

        gate  = torch.sigmoid(
            self.freq_to_gate(f_emb) + self.field_to_gate(field_feat))
        scale = torch.tanh(
            self.freq_to_scale(f_emb).squeeze(-1).unsqueeze(1)
            + self.field_to_scale(field_feat))

        # 频率自适应残差放大: 高频时 intensity→1 → 残差幅度被放大
        intensity  = torch.sigmoid(
            self.freq_to_intensity(f_emb).squeeze(-1)).unsqueeze(1)
        amp_factor = torch.exp(intensity * torch.abs(self.log_scale_max))
        scale_eff  = scale * amp_factor

        residual = gnn - physics
        return gate * physics + (1.0 - gate) * (physics + scale_eff * residual)


# =============================================================================
#                                                                              #
#  Top-Level. PhysicsFEMForwardLayer (三阶段装配) + GNNModel_Forward (训练入口)
#                                                                              #
# =============================================================================


class PhysicsFEMForwardLayer(nn.Module):
    """把三个阶段按顺序串起来的核心层。forward 主流程见 forward() 末尾。

    构造时自动:
      - 推断几何类型 (auto: 楔形 vs 矩形)
      - 按最高频率自适应模态数 n_modes_rect / n_modes_wedge
      - 构造椭圆障碍 mask (若有) 与近场配点 / 近场权重
      - 构造 Jacobi 对角逆 (跨频率缓存,先验配点 loss 用)
      - 把 ms_conv 的长程边预计算好

    forward (index, B, A, ..., net) → dict{output, x_dep, residual}
    """
    def __init__(
        self,
        in_channels, interm_channels, out_channels, input_scale,
        edge_attr, edge_index, p, k_list, model_index, mask,
        partition=5,
        ellipse_params: dict | None = None,
        geometry_type: str = "auto",
        rect_params: dict | None = None,
        use_physics_prior: bool = True,
        use_multi_scale_graph: bool = True,
        use_fno_scatter: bool = True,
        **kwargs,
    ):
        super().__init__()
        self.use_physics_prior     = bool(use_physics_prior)
        self.use_multi_scale_graph = bool(use_multi_scale_graph)
        self.use_fno_scatter       = bool(use_fno_scatter)
        self.in_channels     = in_channels
        self.interm_channels = interm_channels
        self.mask            = mask
        self.freq_list       = k_list
        self.edge_attr       = edge_attr
        self.edge_index      = edge_index
        self.model_index     = model_index
        self.p               = p
        self.p_single        = self._unique_xy_keep_order(self.p)
        self.geometry_type   = self._infer_geometry_type(geometry_type)
        self.freq_list.sort()

        # ---- 阶段 1: 物理先验 (纯 FNO 直出) --------------------------------
        # 简正波解析先验已移除，先验一律由 FNO (_FNOScatterField) 直出。
        import os as _os
        if _os.environ.get("RANK", "0") == "0":
            domain_size  = float(torch.max(self.p[:, 0]).cpu())
            domain_depth = float((torch.max(self.p[:, 1]) - torch.min(self.p[:, 1])).cpu())
            print(f"[two-stage] FNO 直出先验 "
                  f"(geom={self.geometry_type}, max_freq={max(self.freq_list)}Hz, "
                  f"Lx≈{domain_size:.1f}m, D≈{domain_depth:.1f}m)")
        self._ellipse_params = ellipse_params

        # ---- 椭圆障碍相关 mask / 配点 -------------------------------------
        self._interior_mask_2n  = self._build_interior_mask_2n(ellipse_params)
        self._nf_node_weight_2n = self._build_nf_node_weight_2n(
            ellipse_params, margin=1.5, w_nf=5.0)
        self._diag_inv = {}

        # ---- 阶段 2: FEM 引导 GNN ----------------------------------------
        self.message_passing = FEMGuidedGraphNet(
            edge_index=self.edge_index, p=p,
            interm_channels=interm_channels, freq_list=self.freq_list)
        self.message_passing.set_interior_mask(self._interior_mask_2n)

        # 给 ms_conv 预构造长程边 (1/2/4/8 跳)
        _ei0 = as_edge_index(self.edge_index[0])
        _ea0 = as_edge_attr(self.edge_attr[0])
        self.message_passing.ms_conv.set_graph(
            src=_ei0[0].cpu(), dst=_ei0[1].cpu(),
            ea=_ea0.cpu(), n_nodes=p.shape[0])

        # ---- 阶段 3: 融合 ----------------------------------------------
        self.skip_fusion = PriorFEMFusion(
            n_freq=len(self.freq_list), embed_dim=8)

        # ---- 方案 C: FNO 独立全场修正路 (理想解析解 + FNO修正,加权加法拼接) ----
        # FNO 看【理想解析场 + 坐标 + 频率】,独立产一路完整修正场;
        # 与理想解析解加权相加: physics_prior = w_a·analytic + w_f·FNO修正。
        # w_f = tanh(fno_blend_logit) (可学,初值非零让 FNO 较快参与)。
        if self.use_fno_scatter:
            self.fno_corr = _FNOScatterField(
                node_xy=self.p_single, freq_list=self.freq_list,
                grid=64, width=max(16, self.interm_channels), modes=16).double()
            self.fno_blend_logit = nn.Parameter(torch.tensor(0.5, dtype=torch.float64))
        else:
            self.fno_corr = None

    # ==================================================================
    # 主 forward
    # ==================================================================
    def forward(self, index, B, A, x_fem, source_info, mask, net,
                skip_solver=False, verbose=False):
        # 计时探针 (PIKF_PROFILE=1 时启用): 用 cuda.synchronize 测各 Stage 墙钟耗时
        import os as _os, time as _time
        _prof = _os.environ.get("PIKF_PROFILE", "0") == "1"
        def _t():
            if _prof and torch.cuda.is_available():
                torch.cuda.synchronize()
            return _time.perf_counter()
        _tmark = {}
        _t0 = _t()
        # ---- Stage 1: 纯 FNO 直出先验 (简正波先验已移除) ----
        if self.use_physics_prior:
            if self.fno_corr is None:
                raise RuntimeError(
                    "简正波解析先验已移除，物理先验必须由 FNO 提供；"
                    "请确保 use_fno_scatter=True。")
            _ta = _t()
            # 纯 FNO: 输入仅 [源高斯图, 坐标, 频率]。
            corr = self.fno_corr.forward_source(
                source_info[:, :2].to(self.p.dtype),
                float(self.freq_list[index]))             # [B,N,2]
            physics_prior = torch.cat([corr[..., 0], corr[..., 1]], dim=1)  # [B,2N]
            prior_physics_data = physics_prior
            _tmark["s1_fno"] = _t() - _ta
        else:
            # 消融[w/o physics-prior network]: 用零场作初值，让 GNN 从零学起（不调用先验网络）
            physics_prior = torch.zeros(
                source_info.shape[0], self.p.shape[0],
                dtype=self.p.dtype, device=B.device)
            prior_physics_data = physics_prior
        x_dep = self._apply_interior_zero(physics_prior)

        # 首次见此 freq_idx 时缓存 Jacobi 对角逆 (NF helmholtz loss 用)
        if index not in self._diag_inv:
            ea_flat = as_edge_attr(self.edge_attr[index])
            self.precompute_diag_inv(index, self.edge_index[index],
                                     ea_flat, physics_prior.shape[1])

        # ---- Stage 2: FEM 引导 GNN ----
        _ts2 = _t()
        if self.use_multi_scale_graph:
            gnn_out = self.message_passing(
                x_dep, index, B.squeeze(-1), A.squeeze(-1), x_dep, net
            ).reshape_as(x_dep)
            gnn_out = self._apply_interior_zero(gnn_out)
        else:
            # 消融[w/o multi-scale graph]: 跳过图卷积修正，直接用先验场
            gnn_out = x_dep
        _tmark["s2_graph"] = _t() - _ts2

        # ---- Stage 3: 频率自适应融合 ----
        # 注: FNO 散射修正已嵌入 Stage-1 先验内部 (接管 scatter_net),此处不变。
        _ts3 = _t()
        output = self.skip_fusion(physics_prior, gnn_out, freq_idx=index)
        output = self._apply_interior_zero(output)

        if self._interior_mask_2n is not None:
            m = self._interior_mask_2n.to(output.device)
            physics_prior = physics_prior.clone(); physics_prior[:, m] = 0.0
            output        = output.clone();        output[:, m]        = 0.0

        _tmark["s3_fusion"] = _t() - _ts3

        if _prof and _os.environ.get("RANK", "0") == "0":
            _msg = "  ".join(f"{k}={v*1000:.2f}ms" for k, v in _tmark.items())
            print(f"[profile] {_msg}  | total={(_t()-_t0)*1000:.2f}ms")

        return {
            "output":   output,
            "x_dep":    physics_prior,
            # FEM 残差项已废弃（不再参与 loss 或诊断），返回 0 占位保持接口稳定
            "residual": torch.zeros((), dtype=output.dtype, device=output.device),
        }

    # ==================================================================
    # 椭圆障碍相关辅助 (trainer 通过 _has_nf 判断这些字段是否启用)
    # ==================================================================






    def _build_nf_node_weight_2n(self, ellipse_params, margin=1.5, w_nf=5.0):
        """近场加权 mask: 椭圆附近 box 内权重=w_nf,椭圆内=0,其他=1。"""
        if ellipse_params is None:
            return torch.ones(2 * self.p_single.shape[0], dtype=torch.float64)
        cx, cy = ellipse_params['cx'], ellipse_params['cy']
        a,  b  = ellipse_params['a'],  ellipse_params['b']
        r  = max(a, b)
        xy = self.p_single
        x, y = xy[:, 0], xy[:, 1]
        in_nf = ((x >= cx - r - margin) & (x <= cx + r + margin) &
                 (y >= cy - r - margin) & (y <= cy + r + margin))
        interior = ((x - cx) / a) ** 2 + ((y - cy) / b) ** 2 <= 1.0
        w = torch.ones(x.shape[0], dtype=torch.float64)
        w[in_nf] = w_nf
        w[interior] = 0.0
        return torch.cat([w, w], dim=0)



    def _build_interior_mask_2n(self, ellipse_params):
        """椭圆内部节点 mask (供 _apply_interior_zero 用)。"""
        if ellipse_params is None:
            return None
        cx, cy = ellipse_params['cx'], ellipse_params['cy']
        a,  b  = ellipse_params['a'],  ellipse_params['b']
        xy = self.p_single
        interior = ((xy[:, 0] - cx) / a) ** 2 + ((xy[:, 1] - cy) / b) ** 2 <= 1.0
        N = interior.shape[0]
        mask = torch.zeros(2 * N, dtype=torch.bool)
        mask[:N] = interior; mask[N:] = interior
        return mask

    def _apply_interior_zero(self, u):
        if self._interior_mask_2n is None:
            return u
        m = self._interior_mask_2n.to(u.device)
        if not m.any():
            return u
        u = u.clone(); u[:, m] = 0.0
        return u

    def precompute_diag_inv(self, freq_idx, edge_index, edge_attr, n2):
        """缓存 FEM 系统的对角逆 (Jacobi 预条件用)。"""
        if freq_idx in self._diag_inv:
            return
        ei = as_edge_index(edge_index)
        dst, src = ei[1], ei[0]
        diag_mask = (dst == src)
        diag      = torch.zeros(n2, dtype=edge_attr.dtype, device=edge_attr.device)
        if diag_mask.any():
            diag.scatter_add_(0, dst[diag_mask], edge_attr[diag_mask])
        abs_diag  = diag.abs()
        safe_mask = abs_diag > abs_diag.mean() * 1e-4
        self._diag_inv[freq_idx] = torch.where(
            safe_mask, 1.0 / (diag + 1e-30), torch.zeros_like(diag))

    # ==================================================================
    # 几何推断与坐标变换
    # ==================================================================

    @staticmethod
    def _unique_xy_keep_order(x_vals):
        if x_vals.dim() != 2 or x_vals.size(1) != 2:
            raise ValueError("输入张量必须是 [N, 2] 形状。")
        # Fix Bug 2: torch.unique 按字典序排列，破坏 FEM 节点编号顺序，导致
        # physics_prior 的列与 GNN edge_index 的节点编号对不上（图传播读错邻居）。
        # p 由 trainer 以 dataset.nodes.repeat(1,2).T 构造，前 N 行与后 N 行是
        # 同一批 FEM 节点坐标的拷贝，直接取前半段即可保留原始 FEM 节点顺序。
        half = x_vals.shape[0] // 2
        if half > 0 and torch.allclose(x_vals[:half], x_vals[half:], atol=1e-8):
            return x_vals[:half]
        # fallback：非标准双拷贝结构时退回 unique（顺序不保证，但不崩溃）
        return torch.unique(x_vals, dim=0)

    # 保持旧名兼容 (内部一致使用 _unique_xy_keep_order)
    unique_xy_keep_order = _unique_xy_keep_order

    def _infer_geometry_type(self, geometry_type: str) -> str:
        """auto: 通过节点占空比 + y 跨度变异系数判定 rectangle vs wedge。"""
        import os as _os
        _rank0 = (_os.environ.get("RANK", "0") == "0")
        if geometry_type != "auto":
            if geometry_type not in {"wedge", "rectangle"}:
                raise ValueError(f"Unsupported geometry_type: {geometry_type!r}. "
                                 "Choose from: 'wedge', 'rectangle', 'auto'.")
            if _rank0:
                print(f"[PhysicsFEMForwardLayer] geometry_type={geometry_type!r} "
                      f"(explicitly provided)")
            return geometry_type

        pxy = self._unique_xy_keep_order(self.p).detach().cpu().to(torch.float64)
        x, y = pxy[:, 0], pxy[:, 1]
        xr = float((torch.max(x) - torch.min(x)).item())
        yr = float((torch.max(y) - torch.min(y)).item())
        if xr <= 1e-8 or yr <= 1e-8:
            return "wedge"

        xn = ((x - torch.min(x)) / xr).clamp(0.0, 1.0)
        yn = ((y - torch.min(y)) / yr).clamp(0.0, 1.0)
        # 32×32 占用栅格 → 占空比
        ix = torch.clamp((xn * 31).long(), 0, 31)
        iy = torch.clamp((yn * 31).long(), 0, 31)
        occ = torch.zeros((32, 32), dtype=torch.bool)
        occ[ix, iy] = True
        occ_ratio = float(occ.to(torch.float64).mean().item())

        # 各 x 列的 y 跨度变异系数 → 矩形为常数 (cv 小),楔形随 x 变化 (cv 大)
        span_vals = []
        x_edges = torch.linspace(0.0, 1.0, steps=17, dtype=torch.float64)
        for bi in range(16):
            l, r = x_edges[bi], x_edges[bi + 1]
            mb = (xn >= l) & ((xn <= r) if bi == 15 else (xn < r))
            if torch.count_nonzero(mb) < 6: continue
            yb = yn[mb]
            span_vals.append(float((torch.max(yb) - torch.min(yb)).item()))
        if len(span_vals) >= 4:
            span_t  = torch.tensor(span_vals, dtype=torch.float64)
            span_cv = float((torch.std(span_t)
                             / torch.clamp(torch.mean(span_t), min=1e-6)).item())
        else:
            span_cv = 1.0

        result = "rectangle" if (occ_ratio > 0.55 and span_cv < 0.35) else "wedge"
        if _rank0:
            print(f"[PhysicsFEMForwardLayer] auto-detect: "
                  f"occ_ratio={occ_ratio:.3f}, cv={span_cv:.3f} "
                  f"→ geometry_type={result!r} "
                  f"(thresholds: occ>0.55 and cv<0.35 → rectangle)")
        return result


class GraphFeatureEncoder(nn.Module):
    """节点 + 边编码器（A/B 边编码，服务 1-hop 图卷积）。

    GNNModel_Forward 的预处理网络。本类做:
      · 节点编码: [场值, 节点坐标] → hidden
      · 边编码:   edge_attr (FEM 系统矩阵 A 的边权) → hidden 权重
      · 1-hop 聚合: agg[dst] += edge_enc · node_enc[src]
      · 解码回场域修正 [B,2N] (decode 末层零初始化 → 起步≈0)
    在 2N 实化节点空间操作 (与 ms_conv 一致)。签名兼容 _call_net。
    """
    def __init__(self, in_out_dim: int, hidden: int, node_xy: torch.Tensor,
                 freq_list=None, c0: float = 1500.0, **kwargs):
        super().__init__()
        self.in_out_dim = int(in_out_dim)
        N = self.in_out_dim // 2
        h = max(16, int(hidden))
        # 实化 2N 节点坐标 (前 N 与后 N 同坐标:实部/虚部共享物理位置)
        xy = node_xy.detach().to(dtype=torch.float64).cpu()[:, :2]
        if xy.shape[0] < N:
            xy = torch.cat([xy, xy[-1:].repeat(N - xy.shape[0], 1)], dim=0)
        else:
            xy = xy[:N]
        xy2 = torch.cat([xy, xy], dim=0)                      # [2N,2]
        # 坐标归一化到 ~[-1,1]
        mn = xy2.min(0, keepdim=True).values
        rng = (xy2.max(0, keepdim=True).values - mn).clamp(min=1e-6)
        self.register_buffer("_node_xy", (xy2 - mn) / rng * 2 - 1)  # [2N,2]
        self.node_enc = nn.Sequential(
            nn.Linear(3, h), nn.SiLU(), nn.Linear(h, h)).double()   # [场值,x,y]→h
        self.edge_enc = nn.Sequential(
            nn.Linear(1, h), nn.SiLU(), nn.Linear(h, h)).double()   # edge_attr→h
        self.decode = nn.Linear(h, 1).double()
        nn.init.zeros_(self.decode.weight); nn.init.zeros_(self.decode.bias)

    def forward(self, x, freq_idx=None, src=None, dst=None, edge_attr=None):
        # x: [B,2N];退化(无图)时返回零修正
        B, M = x.shape
        if src is None or dst is None or edge_attr is None:
            return torch.zeros_like(x)
        dev, dt = x.device, x.dtype
        xy = self._node_xy.to(device=dev, dtype=dt)           # [2N,2]
        nf = torch.cat([x.unsqueeze(-1),
                        xy.unsqueeze(0).expand(B, -1, -1)], dim=-1)  # [B,2N,3]
        n_enc = self.node_enc(nf)                              # [B,2N,h]
        # edge_attr 对齐到 [E]: 兼容 [E]/[E,1]/[B,E]/[1,E] (系统矩阵 batch 间共享)
        E = src.shape[0]
        ea = edge_attr.to(dt).reshape(-1)
        if ea.numel() != E:
            ea = ea[:E] if ea.numel() > E else ea.reshape(-1)[:E]
        e_enc = self.edge_enc(ea.view(E, 1))                  # [E,h]
        msg = n_enc[:, src, :] * e_enc.unsqueeze(0)          # [B,E,h]
        agg = torch.zeros(B, M, n_enc.shape[-1], dtype=dt, device=dev)
        agg.scatter_add_(1, dst.view(1, -1, 1).expand(B, -1, agg.shape[-1]), msg)
        out = self.decode(F.silu(n_enc + agg)).squeeze(-1)    # [B,2N]
        return out


# =============================================================================
# Public training wrapper
# =============================================================================

class GNNModel_Forward(nn.Module):
    """trainer 直接构造的顶层类。

    forward(B, A, freq_idx, amp, source_location, sol, mask)
        -> (pred, pred, x_dep, residual)
       pred     最终预测的实虚拼接场 [B, 2N]
       x_dep    阶段 1 物理先验场 (用于 trainer 的 fem_error 监控)
       residual 标量,Helmholtz 残差均方值
    """
    def __init__(self, edge_index, mask, edge_attr, p, model_index,
                 test_index, k_list, partition=5, interm_channels=32,
                 in_channels=1, pre_layer_flag=False,
                 ellipse_params: dict | None = None,
                 geometry_type: str = "auto",
                 rect_params: dict | None = None,
                 use_physics_prior: bool = True,
                 use_multi_scale_graph: bool = True,
                 use_fno_scatter: bool = True):
        super().__init__()
        del pre_layer_flag  # 旧参数，向后兼容签名保留但不使用
        self.edge_index      = edge_index
        self.edge_attr       = edge_attr
        self.mask            = mask
        self.test_index      = test_index
        self.in_channels     = in_channels
        self.interm_channels = interm_channels
        self.p               = p
        self.N               = self.p.shape[0] // 2
        self.freq_list       = k_list
        # 预处理网络: 节点 + 边编码器 (替代复基底预条件器)
        self.net = GraphFeatureEncoder(
            in_out_dim=self.p.shape[0],
            hidden=self.interm_channels,
            node_xy=self.p[:self.N, :2],
            freq_list=sorted(self.freq_list),
            c0=1500.0,
        ).double()
        # 三阶段装配
        self.implicit_layer = PhysicsFEMForwardLayer(
            in_channels=in_channels,
            interm_channels=interm_channels,
            out_channels=1,
            input_scale=64,
            edge_attr=edge_attr,
            edge_index=edge_index,
            p=p,
            k_list=k_list,
            model_index=model_index,
            mask=mask,
            partition=partition,
            ellipse_params=ellipse_params,
            geometry_type=geometry_type,
            rect_params=rect_params,
            use_physics_prior=use_physics_prior,
            use_multi_scale_graph=use_multi_scale_graph,
            use_fno_scatter=use_fno_scatter,
        )

    def forward(self, B, A, freq_idx, amp, source_location, sol, mask,
                area_max=1 / 6.0):
        if A.shape[0] == 1:
            A = A.repeat(B.shape[0], 1, 1)

        result = self.implicit_layer(
            freq_idx, B, A, sol, source_location, mask, self.net)
        output = result["output"].double().reshape((B.shape[0], self.p.shape[0]))

        il = self.implicit_layer
        if il._interior_mask_2n is not None:
            m = il._interior_mask_2n.to(output.device)
            output = output.clone(); output[:, m] = 0.0

        # trainer 期待 4 元组 (pred, x_dep_o, x_dep, residual)
        # x_dep_o 返回物理先验场（修正前），trainer 用它计算 "without correction" 误差曲线；
        # x_dep_o == pred 会使两条误差曲线完全重合，此处修正。
        prior = result["x_dep"].double().reshape_as(output)
        if il._interior_mask_2n is not None:
            prior = prior.clone(); prior[:, m] = 0.0
        return output, prior, prior, result["residual"]


# =====================================================================
#  性能对比 Baseline 模型（纯数据驱动算子，无 FEM 物理残差）
#  —— 与 GNNModel_Forward 同 forward 接口，trainer 可直接 drop-in：
#       forward(B, A, freq_idx, amp, source_location, sol, mask)
#         -> (pred, pred, pred, residual)
#  · 不使用 sol（监督目标），只用 source_location + 频率预测场 [B, 2N]
#    （前 N 实部、后 N 虚部，列序与节点序一致）
#  · residual 恒为 0 标量；trainer 在选用 baseline 时会自动把
#    loss_w_residual 置 0（纯数据驱动对比）
#  · 自带 implicit_layer 占位，避免 trainer.__init__ 读取
#    implicit_layer._nf_node_weight_2n 时报错（属性为 None 即短路）
#  · COMSOL baseline 不在此处：它就是数据集生成时输出的 FEM 参考解本身，
#    无需训练模型。
# =====================================================================

class _BaselineShim:
    """trainer.__init__ 会无条件访问 model.implicit_layer 的若干属性；
    baseline 没有真正的 implicit layer，用此占位（全 None 即短路相关逻辑）。"""
    _nf_node_weight_2n    = None
    _interior_mask_2n     = None


class DeepONetBaseline(nn.Module):
    """DeepONet baseline（性能测试用，纯数据驱动）。

    branch: coarse_grid×coarse_grid 声源高斯图 + 归一化频率 → 实/虚两套系数 [B, 2L]
    trunk : (x/Lx, y/Ly, sin/cos(kx), sin/cos(ky), f_norm) → 实/虚两套有界基函数 [N, 2L]

    改进说明
    --------
    Fix-A  branch 输入从 3 个坐标标量改为 coarse_grid² 高斯声源图 + 频率：
           FNO 拿到 64×64 源图，原 DeepONet 只有 3 个标量，信息量差 ~4000 倍，
           这是收敛速度差两个数量级的根本原因。高斯图的 sigma = λ/4 匹配声学尺度。
    Fix-B  trunk 加入波数位置编码 sin/cos(k·x), sin/cos(k·y)：
           让基函数天然携带频率相关的振荡结构，加速学习格林函数的空间衰减/干涉模式。
    Fix-C  trunk 末层 tanh（有界基函数）。
    Fix-D  内积除以 √L + 可学 out_scale（初值 0.1）消除量级暴胀。
    Fix-E  频率归一化按实际范围 [f_min, f_max]。
    """
    def __init__(self, p, k_list, geometry_type="auto",
                 hidden=128, latent=128, coarse_grid=16, **kwargs):
        super().__init__()
        N = p.shape[0] // 2
        self.N = N
        self.latent = latent
        self.coarse_grid = int(coarse_grid)
        self.freq_list = sorted([float(f) for f in k_list])
        node_xy = p[:N, :2].double().clone()
        self.register_buffer("node_xy", node_xy)
        Lx = float(node_xy[:, 0].max().clamp(min=1.0))
        Ly = float(node_xy[:, 1].max().clamp(min=1.0))
        self.register_buffer("_Lxy", torch.tensor([Lx, Ly], dtype=torch.float64))
        # _scale 保留供向后兼容
        self.register_buffer("_scale", torch.tensor([Lx, Ly], dtype=torch.float64))

        # Fix-E: 按实际频率范围归一化
        f_min = float(min(self.freq_list))
        f_max = float(max(self.freq_list))
        self.register_buffer("_f_min", torch.tensor(f_min, dtype=torch.float64))
        self.register_buffer("_f_range",
                             torch.tensor(max(f_max - f_min, 1.0), dtype=torch.float64))

        # Fix-A: coarse grid 坐标缓存，用于生成声源高斯图
        ys_g, xs_g = torch.meshgrid(
            torch.linspace(0.0, 1.0, coarse_grid, dtype=torch.float64),
            torch.linspace(0.0, 1.0, coarse_grid, dtype=torch.float64),
            indexing="ij")
        self.register_buffer("_grid_xs", xs_g)   # [G, G] 归一化坐标
        self.register_buffer("_grid_ys", ys_g)

        # Fix-A: branch = Gaussian 声源图(G²) + 归一化频率 → 2L 系数（无末层激活）
        branch_in = coarse_grid * coarse_grid + 1
        def _branch_mlp():
            return nn.Sequential(
                nn.Linear(branch_in, hidden), nn.GELU(),
                nn.Linear(hidden, hidden),     nn.GELU(),
                nn.Linear(hidden, hidden),     nn.GELU(),
                nn.Linear(hidden, 2 * latent),          # 无最终激活
            ).double()

        # Fix-B: trunk = [x/Lx, y/Ly, sin(kx), cos(kx), sin(ky), cos(ky), f_norm] → 2L (tanh)
        trunk_in = 7
        def _trunk_mlp():
            return nn.Sequential(
                nn.Linear(trunk_in, hidden), nn.GELU(),
                nn.Linear(hidden, hidden),   nn.GELU(),
                nn.Linear(hidden, hidden),   nn.GELU(),
                nn.Linear(hidden, 2 * latent),
                nn.Tanh(),                              # Fix-C: 基函数有界
            ).double()

        self.branch = _branch_mlp()
        self.trunk  = _trunk_mlp()
        self.bias      = nn.Parameter(torch.zeros(2, dtype=torch.float64))
        self.out_scale = nn.Parameter(torch.tensor(0.1, dtype=torch.float64))  # Fix-D
        self.implicit_layer = _BaselineShim()

    def _freq_hz(self, freq_idx):
        return self.freq_list[int(freq_idx)]

    def _norm_freq(self, freq_hz, dev):
        """频率归一化到 [0, 1]（Fix-E）。"""
        f = torch.tensor(float(freq_hz), dtype=torch.float64, device=dev)
        return ((f - self._f_min.to(dev)) / self._f_range.to(dev)).clamp(0.0, 1.0)

    def _make_gauss_map(self, source_location, freq_hz, dev):
        """在 coarse_grid×coarse_grid 规则网格上生成声源高斯图 [B, G*G]。
        sigma = λ/4，保证高斯斑与声学尺度匹配；最小取域宽的 2%。
        """
        Bsz = source_location.shape[0]
        Lxy = self._Lxy.to(dev)
        xs = self._grid_xs.to(dev) * Lxy[0]   # [G,G] 物理坐标
        ys = self._grid_ys.to(dev) * Lxy[1]
        sx = source_location[:, 0].double().view(Bsz, 1, 1)
        sy = source_location[:, 1].double().view(Bsz, 1, 1)
        lam   = 1500.0 / max(float(freq_hz), 1.0)
        sigma = max(lam * 0.25, 0.02 * float(Lxy[0].item()))
        gauss = torch.exp(-((xs - sx) ** 2 + (ys - sy) ** 2) / (2 * sigma ** 2))
        return gauss.reshape(Bsz, -1)          # [B, G*G]

    def forward(self, B, A, freq_idx, amp, source_location, sol, mask,
                area_max=1 / 6.0):
        dev  = source_location.device
        Bsz  = source_location.shape[0]
        fhz  = self._freq_hz(freq_idx)
        fhz_norm = float(self._norm_freq(fhz, dev).item())

        # Fix-A: branch — Gaussian 声源图 + 归一化频率
        gauss_map = self._make_gauss_map(source_location, fhz, dev)   # [B, G*G]
        fb  = torch.full((Bsz, 1), fhz_norm, dtype=torch.float64, device=dev)
        br  = self.branch(torch.cat([gauss_map, fb], dim=1))          # [B, 2L]

        # Fix-B: trunk — 坐标 + 波数位置编码 + 归一化频率
        Lxy = self._Lxy.to(dev)
        xy  = self.node_xy.to(dev)                                     # [N, 2]
        xn  = (xy[:, 0] / Lxy[0]).view(self.N, 1)
        yn  = (xy[:, 1] / Lxy[1]).view(self.N, 1)
        k   = 2.0 * math.pi * fhz / 1500.0
        kx  = (xy[:, 0] * k).view(self.N, 1)
        ky  = (xy[:, 1] * k).view(self.N, 1)
        ft  = torch.full((self.N, 1), fhz_norm, dtype=torch.float64, device=dev)
        trunk_in = torch.cat([xn, yn,
                              torch.sin(kx), torch.cos(kx),
                              torch.sin(ky), torch.cos(ky),
                              ft], dim=1)                              # [N, 7]
        tr  = self.trunk(trunk_in)                                     # [N, 2L] (tanh)

        L = self.latent
        scale_eff = torch.abs(self.out_scale) / math.sqrt(float(L))   # Fix-D
        real = (br[:, :L] @ tr[:, :L].t()) * scale_eff + self.bias[0] # [B, N]
        imag = (br[:, L:] @ tr[:, L:].t()) * scale_eff + self.bias[1] # [B, N]

        pred = torch.cat([real, imag], dim=1)                          # [B, 2N]
        residual = torch.zeros((), dtype=pred.dtype, device=dev)
        return pred, pred, pred, residual


class _SpectralConv2d(nn.Module):
    """FNO 的 2D 谱卷积层（截断低频 modes 做复数线性变换）。"""
    def __init__(self, in_c, out_c, m1, m2):
        super().__init__()
        self.m1, self.m2 = m1, m2
        s = 1.0 / (in_c * out_c)
        # 实数参数存复权重(末维2=实/虚)；复数 Parameter 会触发 DDP/NCCL 广播失败
        # (TypeError: ... not supported for NCCL process group: ComplexFloat)
        self.w1 = nn.Parameter(s * torch.rand(in_c, out_c, m1, m2, 2))
        self.w2 = nn.Parameter(s * torch.rand(in_c, out_c, m1, m2, 2))

    @staticmethod
    def _mul(x, w):
        # w: 实数 [in,out,h,w,2] -> 复数; x: 复数 [B,in,h,w]
        wc = torch.complex(w[..., 0], w[..., 1])
        return torch.einsum("bixy,ioxy->boxy", x, wc)

    def forward(self, x):
        Bsz, _, H, W = x.shape
        xft = torch.fft.rfft2(x)
        out = torch.zeros(Bsz, self.w1.shape[1], H, W // 2 + 1,
                          dtype=xft.dtype, device=x.device)
        m1 = min(self.m1, H // 2)
        m2 = min(self.m2, W // 2 + 1)
        out[:, :, :m1, :m2]  = self._mul(xft[:, :, :m1, :m2],  self.w1[:, :, :m1, :m2])
        out[:, :, -m1:, :m2] = self._mul(xft[:, :, -m1:, :m2], self.w2[:, :, :m1, :m2])
        return torch.fft.irfft2(out, s=(H, W))


class FNO2DBaseline(nn.Module):
    """FNO-2D baseline（性能测试用，纯数据驱动）。

    把节点坐标光栅化到 grid×grid 规则网格，输入通道 [源高斯图, x, y, 频率]，
    经 n_layers 个 Fourier 层得到 [实, 虚] 两通道，再 bilinear 采样回节点 -> [B, 2N]。
    内部用 float32（FNO 惯例），输出转回 double 供 trainer 使用。
    （矩形域为规则网格、最自然；楔形域域外区域由 trainer 的内边界/域外 mask 处理。）
    """
    def __init__(self, p, k_list, geometry_type="auto",
                 grid=64, width=32, modes=16, n_layers=4, **kwargs):
        super().__init__()
        N = p.shape[0] // 2
        self.N = N
        self.grid = grid
        self.width = width
        self.freq_list = sorted([float(f) for f in k_list])
        node_xy = p[:N, :2].double().clone()
        self.register_buffer("node_xy", node_xy)
        Lx = float(node_xy[:, 0].max().clamp(min=1.0))
        Ly = float(node_xy[:, 1].max().clamp(min=1.0))
        self.register_buffer("_Lxy", torch.tensor([Lx, Ly], dtype=torch.float64))
        # 节点归一化到 [-1,1]（grid_sample 用；x=宽 维, y=高 维）
        gx = (node_xy[:, 0] / Lx) * 2 - 1
        gy = (node_xy[:, 1] / Ly) * 2 - 1
        self.register_buffer("_samp_grid", torch.stack([gx, gy], dim=-1).float())
        # 规则网格归一化坐标通道 [2,H,W]（与约定一致：x 向右, y 向下）
        ys, xs = torch.meshgrid(
            torch.linspace(0, 1, grid), torch.linspace(0, 1, grid), indexing="ij")
        self.register_buffer("_coord", torch.stack([xs, ys], dim=0).float())
        self.lift  = nn.Linear(4, width)
        self.specs = nn.ModuleList([_SpectralConv2d(width, width, modes, modes)
                                    for _ in range(n_layers)])
        self.ws    = nn.ModuleList([nn.Conv2d(width, width, 1) for _ in range(n_layers)])
        self.proj1 = nn.Linear(width, 128)
        self.proj2 = nn.Linear(128, 2)
        self.implicit_layer = _BaselineShim()

    def _freq_hz(self, freq_idx):
        return self.freq_list[int(freq_idx)]

    def forward(self, B, A, freq_idx, amp, source_location, sol, mask,
                area_max=1 / 6.0):
        dev = source_location.device
        Bsz = source_location.shape[0]
        Hh = Ww = self.grid
        Lx, Ly = float(self._Lxy[0]), float(self._Lxy[1])
        coord = self._coord.to(dev)                              # [2,H,W]
        xs = coord[0] * Lx
        ys = coord[1] * Ly
        # 源点高斯图（每个 batch 一张）
        sx = source_location[:, 0].float().view(Bsz, 1, 1)
        sy = source_location[:, 1].float().view(Bsz, 1, 1)
        sigma = 0.05 * max(Lx, Ly)
        gauss = torch.exp(-((xs - sx) ** 2 + (ys - sy) ** 2) / (2 * sigma ** 2))  # [B,H,W]
        fhz = self._freq_hz(freq_idx) / 100.0
        fmap = torch.full((Bsz, Hh, Ww), fhz, device=dev)
        inp = torch.stack([gauss,
                           coord[0].expand(Bsz, Hh, Ww),
                           coord[1].expand(Bsz, Hh, Ww),
                           fmap], dim=-1)                          # [B,H,W,4]
        x = self.lift(inp).permute(0, 3, 1, 2).contiguous()        # [B,width,H,W]
        for spc, w in zip(self.specs, self.ws):
            x = F.gelu(spc(x) + w(x))
        x = x.permute(0, 2, 3, 1)                                  # [B,H,W,width]
        x = self.proj2(F.gelu(self.proj1(x)))                      # [B,H,W,2]
        x = x.permute(0, 3, 1, 2).contiguous()                     # [B,2,H,W]
        # 采样回节点坐标
        grid = self._samp_grid.to(dev).view(1, self.N, 1, 2).expand(Bsz, -1, -1, -1)
        samp = F.grid_sample(x, grid, mode="bilinear", align_corners=True)  # [B,2,N,1]
        samp = samp.squeeze(-1)                                    # [B,2,N]
        pred = torch.cat([samp[:, 0], samp[:, 1]], dim=1).double()  # [B,2N]
        residual = torch.zeros((), dtype=pred.dtype, device=dev)
        return pred, pred, pred, residual


# =====================================================================
#  KNOBaseline — Koopman Neural Operator baseline
# =====================================================================

class KNOBaseline(nn.Module):
    """Koopman Neural Operator baseline（性能测试用，纯数据驱动）。

    标准 grid-based KNO（Xiong et al., 2023, "Koopman Neural Operator ..."）：
        1. Encoder：把网格输入 [源高斯图, x, y, 频率编码] 逐点提升到 width 维观测量 v。
        2. 傅里叶截断：对 v 做 rfft2，保留低频 modes（带限观测子空间）。
        3. Koopman 线性演化：在低频模态上用【同一个】可学复线性算子 K 迭代 T 步
           ĥ ← K·ĥ，模拟可观测量空间中的线性动力系统（这是 KNO 区别于 FNO 的核心：
           FNO 每层独立谱权重，KNO 用共享算子 K 重复作用，学 Koopman 算子的谱）。
        4. irfft2 还原 + 逐点局部路径残差 + Decoder 投影到 [实, 虚] 两通道。
        5. bilinear 采样回节点 → [B, 2N]。

    与本仓库 FNO/CNO 一致：grid 光栅化 + 复权重用实数张量存储（DDP/NCCL 安全）。
    内部 float32，输出转回 double 供 trainer 使用。
    """
    def __init__(self, p, k_list, geometry_type="auto",
                 grid=64, width=32, modes=16, koopman_steps=4,
                 n_freq_bands=4, **kwargs):
        super().__init__()
        N = p.shape[0] // 2
        self.N = N
        self.grid  = grid
        self.width = width
        self.modes = modes
        self.koopman_steps = int(koopman_steps)
        self.n_freq_bands  = int(n_freq_bands)
        self.freq_list = sorted([float(f) for f in k_list])

        node_xy = p[:N, :2].double().clone()
        self.register_buffer("node_xy", node_xy)
        Lx = float(node_xy[:, 0].max().clamp(min=1.0))
        Ly = float(node_xy[:, 1].max().clamp(min=1.0))
        self.register_buffer("_Lxy", torch.tensor([Lx, Ly], dtype=torch.float64))

        f_min = float(min(self.freq_list)); f_max = float(max(self.freq_list))
        self.register_buffer("_f_min",   torch.tensor(f_min, dtype=torch.float64))
        self.register_buffer("_f_range", torch.tensor(max(f_max - f_min, 1.0),
                                                       dtype=torch.float64))

        gx = (node_xy[:, 0] / Lx) * 2 - 1
        gy = (node_xy[:, 1] / Ly) * 2 - 1
        self.register_buffer("_samp_grid", torch.stack([gx, gy], dim=-1).float())
        ys_g, xs_g = torch.meshgrid(
            torch.linspace(0.0, 1.0, grid),
            torch.linspace(0.0, 1.0, grid), indexing="ij")
        self.register_buffer("_coord", torch.stack([xs_g, ys_g], dim=0))  # [2,H,W]

        # Encoder：输入通道 gauss(1)+坐标(2)+波数编码(4)+频率正弦编码(2*bands) → width
        in_ch = 1 + 2 + 4 + 2 * self.n_freq_bands
        self.encoder = nn.Sequential(
            nn.Linear(in_ch, width), nn.GELU(),
            nn.Linear(width, width))

        # Koopman 线性算子 K：在低频模态上作用的【共享】复线性变换（实数存复权重）。
        # KNO 本质是「共享算子重复作用」；但纯线性迭代 K^T 会退化成单次线性变换、
        # 且深度不足（表达力远弱于 FNO 的多谱层）。因此每次 Koopman 作用后接
        # 局部线性旁路 + GELU 非线性，使 T 步迭代成为 T 层深度算子（保留共享 K
        # 的 KNO 特征，同时对齐 FNO 的有效深度）。
        s = 1.0 / (width * width)
        w = s * torch.rand(width, width, modes, modes, 2)
        eye = torch.zeros(width, width, modes, modes, 2)
        idx = torch.arange(width)
        eye[idx, idx, :, :, 0] = 1.0          # 对角实部 ≈ 恒等，稳定起步
        self.koopman_w = nn.Parameter(eye + 0.01 * w)

        # 每个 Koopman 迭代步共享一份局部旁路（W·x），迭代间插非线性
        self.local_w = nn.Conv2d(width, width, 1)

        # Decoder：width → 128 → [实, 虚]
        self.dec1 = nn.Conv2d(width, 128, 1)
        self.dec2 = nn.Conv2d(128, 2, 1)
        self.out_scale = nn.Parameter(torch.tensor(0.1))
        self.implicit_layer = _BaselineShim()

    def _freq_hz(self, freq_idx):
        return self.freq_list[int(freq_idx)]

    def _freq_encoding(self, freq_hz, dev):
        f_norm = (float(freq_hz) - float(self._f_min)) / float(self._f_range)
        f_norm = min(max(f_norm, 0.0), 1.0)
        bands = torch.arange(1, self.n_freq_bands + 1, device=dev,
                             dtype=torch.float32)
        ang = math.pi * f_norm * bands
        return torch.cat([torch.sin(ang), torch.cos(ang)])   # [2*bands]

    def _koopman_apply(self, h_ft):
        """在低频模态上作用共享复线性算子 K 一次。h_ft: 复数 [B,width,m1,m2]。"""
        wc = torch.complex(self.koopman_w[..., 0], self.koopman_w[..., 1])
        m1 = min(self.modes, h_ft.shape[-2])
        m2 = min(self.modes, h_ft.shape[-1])
        out = h_ft.clone()
        out[:, :, :m1, :m2] = torch.einsum(
            "bixy,ioxy->boxy", h_ft[:, :, :m1, :m2], wc[:, :, :m1, :m2])
        return out

    def forward(self, B, A, freq_idx, amp, source_location, sol, mask,
                area_max=1 / 6.0):
        dev = source_location.device
        Bsz = source_location.shape[0]
        Hh = Ww = self.grid
        Lx, Ly = float(self._Lxy[0]), float(self._Lxy[1])
        coord = self._coord.to(dev)
        xs = coord[0] * Lx; ys = coord[1] * Ly

        fhz = self._freq_hz(freq_idx)
        sx = source_location[:, 0].float().view(Bsz, 1, 1)
        sy = source_location[:, 1].float().view(Bsz, 1, 1)
        lam   = 1500.0 / max(float(fhz), 1.0)
        sigma = max(lam * 0.25, 0.03 * max(Lx, Ly))
        gauss = torch.exp(-((xs - sx) ** 2 + (ys - sy) ** 2) / (2 * sigma ** 2))

        k  = 2.0 * math.pi * float(fhz) / 1500.0
        kx = xs * k; ky = ys * k
        skx = torch.sin(kx).expand(Bsz, Hh, Ww); ckx = torch.cos(kx).expand(Bsz, Hh, Ww)
        sky = torch.sin(ky).expand(Bsz, Hh, Ww); cky = torch.cos(ky).expand(Bsz, Hh, Ww)
        fenc = self._freq_encoding(fhz, dev)
        fmaps = [fenc[i].view(1, 1, 1).expand(Bsz, Hh, Ww) for i in range(fenc.shape[0])]

        chans = [gauss,
                 coord[0].expand(Bsz, Hh, Ww), coord[1].expand(Bsz, Hh, Ww),
                 skx, ckx, sky, cky, *fmaps]
        inp = torch.stack(chans, dim=-1)                     # [B,H,W,in_ch]

        # Encoder（逐点提升）
        v = self.encoder(inp).permute(0, 3, 1, 2).contiguous()   # [B,width,H,W]

        # Koopman 迭代演化：每步 = 共享算子 K 在傅里叶域作用 + 局部旁路 + GELU。
        # 迭代 T 步构成 T 层深度算子（共享同一 K，这是 KNO 的核心特征），
        # 迭代间的非线性避免 K^T 退化为单次线性变换、并对齐 FNO 的有效深度。
        for _ in range(self.koopman_steps):
            h_ft = torch.fft.rfft2(v)
            h_ft = self._koopman_apply(h_ft)
            h    = torch.fft.irfft2(h_ft, s=(Hh, Ww))            # [B,width,H,W]
            v    = F.gelu(h + self.local_w(v))                   # 谱路径 + 局部旁路

        # Decoder
        v = self.dec2(F.gelu(self.dec1(v)))                      # [B,2,H,W]
        v = v * torch.abs(self.out_scale)

        grid = self._samp_grid.to(dev).view(1, self.N, 1, 2).expand(Bsz, -1, -1, -1)
        samp = F.grid_sample(v, grid, mode="bilinear", align_corners=True)
        samp = samp.squeeze(-1)                                  # [B,2,N]
        pred = torch.cat([samp[:, 0], samp[:, 1]], dim=1).double()
        residual = torch.zeros((), dtype=pred.dtype, device=dev)
        return pred, pred, pred, residual


# =====================================================================
#  CNOBaseline — Convolutional Neural Operator baseline
# =====================================================================

class _CNOBlock(nn.Module):
    """CNO 基本块：带限（反走样）卷积 + 残差 + (可选)上/下采样 + 激活。

    CNO 的核心思想是把算子学习限制在带限函数空间：在每次非线性激活前后做
    低通滤波（这里用反走样的 up/down 采样近似）来保持连续-离散一致性。
    改进点（相对初版）：
      · 双层卷积 + 组归一化 + 残差连接（same 模式），缓解深层梯度衰减；
      · same 模式下用 dilation 扩大感受野（声场是全局现象，需要长程耦合）。
    """
    def __init__(self, in_c, out_c, mode="same", dilation=1):
        super().__init__()
        self.mode = mode
        pad = dilation
        self.conv1 = nn.Conv2d(in_c, out_c, 3, padding=pad, dilation=dilation)
        self.norm1 = nn.GroupNorm(min(8, out_c), out_c)
        self.conv2 = nn.Conv2d(out_c, out_c, 3, padding=1)
        self.norm2 = nn.GroupNorm(min(8, out_c), out_c)
        self.act   = nn.GELU()
        # 残差捷径（in_c != out_c 时用 1x1 对齐通道）
        self.skip  = (nn.Identity() if in_c == out_c
                      else nn.Conv2d(in_c, out_c, 1))

    def forward(self, x):
        h = self.act(self.norm1(self.conv1(x)))
        h = self.norm2(self.conv2(h))
        h = self.act(h + self.skip(x))          # 残差
        if self.mode == "down":
            h = F.avg_pool2d(h, kernel_size=2, stride=2)   # 反走样下采样
        elif self.mode == "up":
            h = F.interpolate(h, scale_factor=2, mode="bilinear",
                              align_corners=False)
        return h


class CNOBaseline(nn.Module):
    """Convolutional Neural Operator baseline（性能测试用，纯数据驱动）。

    把节点坐标光栅化到 grid×grid 规则网格，输入通道
    [源高斯图, x, y, sin(kx), cos(kx), sin(ky), cos(ky), freq正弦编码...]，
    经 U 型 CNO（下采样编码 + 膨胀卷积中间层 + 上采样解码 + skip 连接）得到
    [实, 虚] 两通道，再 bilinear 采样回节点 → [B, 2N]。

    相对初版的关键改进（初版卡在高误差不降的原因）：
      · 感受野：中间层用多个 dilation 逐级放大的 _CNOBlock，让局部卷积也能
        建立长程耦合（声场是全局波动现象，纯 3×3 局部卷积传不到远场）。
      · 输入编码：加入波数位置编码 sin/cos(k·x,y) + 正弦频率编码，避免
        fhz/100 后各频率数值过近而被淹没。
      · 每块残差连接 + GroupNorm，缓解深层梯度衰减。
      · 高斯源 sigma 与波长挂钩（λ/4），匹配声学尺度。
      · 可学 out_scale（初值 0.1）稳定初期输出量级。
    内部用 float32，输出转回 double 供 trainer 使用。
    """
    def __init__(self, p, k_list, geometry_type="auto",
                 grid=64, width=48, n_levels=2, n_freq_bands=4, **kwargs):
        super().__init__()
        N = p.shape[0] // 2
        self.N = N
        self.grid  = grid
        self.width = width
        self.n_levels = int(n_levels)
        self.n_freq_bands = int(n_freq_bands)
        self.freq_list = sorted([float(f) for f in k_list])

        node_xy = p[:N, :2].double().clone()
        self.register_buffer("node_xy", node_xy)
        Lx = float(node_xy[:, 0].max().clamp(min=1.0))
        Ly = float(node_xy[:, 1].max().clamp(min=1.0))
        self.register_buffer("_Lxy", torch.tensor([Lx, Ly], dtype=torch.float64))

        f_min = float(min(self.freq_list)); f_max = float(max(self.freq_list))
        self.register_buffer("_f_min",   torch.tensor(f_min, dtype=torch.float64))
        self.register_buffer("_f_range", torch.tensor(max(f_max - f_min, 1.0),
                                                       dtype=torch.float64))

        gx = (node_xy[:, 0] / Lx) * 2 - 1
        gy = (node_xy[:, 1] / Ly) * 2 - 1
        self.register_buffer("_samp_grid", torch.stack([gx, gy], dim=-1).float())

        ys_g, xs_g = torch.meshgrid(
            torch.linspace(0.0, 1.0, grid),
            torch.linspace(0.0, 1.0, grid), indexing="ij")
        self.register_buffer("_coord", torch.stack([xs_g, ys_g], dim=0))  # [2,H,W]

        # 输入通道：gauss(1) + 归一化坐标(2) + 波数编码(4) + 频率正弦编码(2*bands)
        in_ch = 1 + 2 + 4 + 2 * self.n_freq_bands
        self.lift = nn.Conv2d(in_ch, width, 1)

        # U 型编码器（下采样）/ 解码器（上采样），带 skip
        self.enc = nn.ModuleList([
            _CNOBlock(width, width, mode="down") for _ in range(self.n_levels)])
        # 中间层：dilation 逐级放大 (1,2,4,8) 扩大感受野，建立长程耦合
        self.mid = nn.ModuleList([
            _CNOBlock(width, width, mode="same", dilation=d)
            for d in (1, 2, 4, 8)])
        self.dec = nn.ModuleList([
            _CNOBlock(width * 2, width, mode="up") for _ in range(self.n_levels)])

        self.proj1 = nn.Conv2d(width, 128, 1)
        self.proj2 = nn.Conv2d(128, 2, 1)
        self.out_scale = nn.Parameter(torch.tensor(0.1))
        self.implicit_layer = _BaselineShim()

    def _freq_hz(self, freq_idx):
        return self.freq_list[int(freq_idx)]

    def _freq_encoding(self, freq_hz, dev):
        """正弦频率编码 [2*bands]：归一化频率的多频带 sin/cos。"""
        f_norm = ((float(freq_hz) - float(self._f_min)) /
                  float(self._f_range))
        f_norm = min(max(f_norm, 0.0), 1.0)
        bands = torch.arange(1, self.n_freq_bands + 1, device=dev,
                             dtype=torch.float32)
        ang = math.pi * f_norm * bands
        return torch.cat([torch.sin(ang), torch.cos(ang)])   # [2*bands]

    def forward(self, B, A, freq_idx, amp, source_location, sol, mask,
                area_max=1 / 6.0):
        dev = source_location.device
        Bsz = source_location.shape[0]
        Hh = Ww = self.grid
        Lx, Ly = float(self._Lxy[0]), float(self._Lxy[1])
        coord = self._coord.to(dev)                              # [2,H,W]
        xs = coord[0] * Lx
        ys = coord[1] * Ly

        # 源点高斯图（sigma = λ/4，与波长挂钩）
        fhz = self._freq_hz(freq_idx)
        sx = source_location[:, 0].float().view(Bsz, 1, 1)
        sy = source_location[:, 1].float().view(Bsz, 1, 1)
        lam   = 1500.0 / max(float(fhz), 1.0)
        sigma = max(lam * 0.25, 0.03 * max(Lx, Ly))
        gauss = torch.exp(-((xs - sx) ** 2 + (ys - sy) ** 2) / (2 * sigma ** 2))  # [B,H,W]

        # 波数位置编码 sin/cos(k·x), sin/cos(k·y)
        k  = 2.0 * math.pi * float(fhz) / 1500.0
        kx = (xs * k); ky = (ys * k)                             # [B,H,W] / [H,W]
        skx = torch.sin(kx).expand(Bsz, Hh, Ww)
        ckx = torch.cos(kx).expand(Bsz, Hh, Ww)
        sky = torch.sin(ky).expand(Bsz, Hh, Ww)
        cky = torch.cos(ky).expand(Bsz, Hh, Ww)

        # 频率正弦编码（广播成通道图）
        fenc = self._freq_encoding(fhz, dev)                     # [2*bands]
        fmaps = [fenc[i].view(1, 1, 1).expand(Bsz, Hh, Ww)
                 for i in range(fenc.shape[0])]

        chans = [gauss,
                 coord[0].expand(Bsz, Hh, Ww),
                 coord[1].expand(Bsz, Hh, Ww),
                 skx, ckx, sky, cky, *fmaps]
        inp = torch.stack(chans, dim=1)                          # [B, in_ch, H, W]
        x = self.lift(inp)                                       # [B,width,H,W]

        # U 型：编码下采样并缓存 skip
        skips = []
        for blk in self.enc:
            skips.append(x)
            x = blk(x)
        # 中间膨胀卷积堆叠（残差已在块内）
        for blk in self.mid:
            x = blk(x)
        # 解码上采样并拼接 skip
        for blk in self.dec:
            skip = skips.pop()
            if x.shape[-2:] != skip.shape[-2:]:
                x = F.interpolate(x, size=skip.shape[-2:], mode="bilinear",
                                  align_corners=False)
            x = blk(torch.cat([x, skip], dim=1))
        if x.shape[-2:] != (Hh, Ww):
            x = F.interpolate(x, size=(Hh, Ww), mode="bilinear",
                              align_corners=False)

        x = self.proj2(F.gelu(self.proj1(x)))                    # [B,2,H,W]
        x = x * torch.abs(self.out_scale)                        # 可学输出缩放
        grid = self._samp_grid.to(dev).view(1, self.N, 1, 2).expand(Bsz, -1, -1, -1)
        samp = F.grid_sample(x, grid, mode="bilinear", align_corners=True)
        samp = samp.squeeze(-1)                                  # [B,2,N]
        pred = torch.cat([samp[:, 0], samp[:, 1]], dim=1).double()  # [B,2N]
        residual = torch.zeros((), dtype=pred.dtype, device=dev)
        return pred, pred, pred, residual