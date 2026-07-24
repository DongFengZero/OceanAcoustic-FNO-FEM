# Experiment Code — FNO–FEM Ocean Acoustic Field Solver

本目录包含论文全部实验的**数据生成**与**训练/推理**代码。整体流程分两步：
MATLAB/COMSOL 生成物理数据 → Python 转换为 HDF5 并训练模型。

```
Experiment_Code/
├── Data_Generate/                     数据生成 (MATLAB + COMSOL)
│   ├── data_generate_comsol.m         带椭圆障碍的矩形/楔形波导 → COMSOL 数值解 (训练目标)
│   └── data_generate_comsol_analytic.m 无障碍规范波导 → 解析解 (ground truth) + COMSOL 验证
└── Main_Code/                         数据转换 + 模型训练 (Python)
    ├── Ocean_Dataset_barrier_comsol.py .mat → acoustic_dataset.h5 转换器
    ├── ocean_trainer_forward_b.py      训练/推理主程序 (单卡 + 多卡 DDP)
    └── deq_modules/
        └── models.py                   模型定义 (本文方法 + 4 个基线)
```

---

## 端到端流程

```
[1] MATLAB + COMSOL            [2] Python 转换               [3] Python 训练/推理
data_generate_comsol*.m   →   Ocean_Dataset_barrier_    →   ocean_trainer_forward_b.py
(comsol_mesh*.mat +           comsol.py                     (acoustic_dataset.h5 → 模型 + 指标 + 图)
 comsol_batch_manifest*.mat)  (→ acoustic_dataset.h5)
```

---

## [1] 数据生成 — `Data_Generate/`

| 脚本 | 用途 | 对应论文 |
|---|---|---|
| `data_generate_comsol.m` | 矩形/楔形波导 + 椭圆障碍，用 **COMSOL** 求 Helmholtz 数值解作训练目标 | 前向/对比/消融/网格/泛化 (No.3–50) |
| `data_generate_comsol_analytic.m` | 无障碍规范波导，用**解析解**作 ground truth，COMSOL 仅抽样验证 | 解析验证 (No.1–2) |

关键参数（脚本顶部可调）：`Lx/Ly`（域尺寸）、`H_grid`（网格分辨率 Δ）、
`freqs`（频率）、`samples_per_freq`、`domain`（`rectangle`/`wedge`）、
`use_ellipse` 及椭圆几何、`split_train_test`+`train_max_x/y`（按源坐标划分训练/测试）。

坐标约定（矩形）：x=range，y=depth，海面 y=0 为 Dirichlet(p=0)，海底 y=Ly 为 Rigid(Neumann)。
楔形：顶点在原点，海面 θ=0，斜底 θ=θ₀=atan(Ly/Lx) 为 Rigid，右边为 Robin ABC。

**输出**（`export_dir` 名称自动嵌入参数，避免不同配置互盖）：
```
rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000[_split64x64]/
  ├── comsol_mesh_Lx128_Ly128_H1.000.mat            网格
  ├── comsol_batch_Lx128_..._f25Hz.mat …            各频率批次解
  └── comsol_batch_manifest_Lx128_..._f25_50_75_100.mat  清单(源点/频率索引/split_info)
```

源点映射用确定性的**多近邻贪心唯一映射**（`snap_knn_unique`），不依赖随机种子，结果可复现。

---

## [2] 数据转换 — `Ocean_Dataset_barrier_comsol.py`

把 MATLAB `.mat` 读入，组装并写出下游训练用的 **`acoustic_dataset.h5`**，
另存 `source_positions_physical_*.npy`、`timing_statistics.json` 和每样本 TL 对比图。

**HDF5 主要字段**：`matrices/freq_*Hz`（Helmholtz 稀疏矩阵 A，CSC 格式）、
`source_positions*`、`frequency_indices`、`final_vectors`（FEM 解，实虚部拼接）、
`fem_tl`（传播损失）、`source_vectors`（载荷）、`split_info`（训练/测试划分）。

> **样本顺序：严格保持 manifest 原始顺序，不打乱。**
> 源顺序直接取自 manifest 的 `all_freq_indices`（仅布尔筛选未选频率，保序）；
> 全脚本无任何 shuffle/permutation；多卡 DDP 按 `i % world_size` 分工，但每样本
> 携带全局索引 `global_idx` 写回预分配数组原位，输出与单卡逐样本一致。
> 训练/测试划分不靠打乱，而由 manifest 的 `split_info`（按源坐标区域）决定。

运行示例：
```bash
python Ocean_Dataset_barrier_comsol.py \
    --data_dir  "./comsol_dataset_export/rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000" \
    --output_dir "../Ocean" \
    --grid_x 128 --grid_y 128 --H 1.000 \
    --frequencies 25 50 75 100 --samples_per_freq 2000
```
（给定 `--data_dir` 后会自动定位 `comsol_mesh*.mat` 与 `comsol_batch_manifest*.mat`。）

---

## [3] 训练/推理 — `ocean_trainer_forward_b.py`

从 `acoustic_dataset.h5` 训练模型，输出权重、逐轮指标（`statistics_epoch*.json`）、
训练日志（`full_run_*.log`）和周期性 TL 对比图（即 `Raw_Experimental_Data/*/training_run/`）。

主要参数：

| 参数 | 说明 | 默认 |
|---|---|---|
| `--data_dir` | 含 h5 子目录的父目录 (**必填**) | — |
| `--dataset_name` | h5 子目录名前缀 (**必填**) | — |
| `--epochs` | 训练轮数 | 200 |
| `--batch_size` | 批大小 | 1 |
| `--train_ratio` | 训练集比例 | 0.9 |
| `--split_seed` | 划分随机种子 | 42 |
| `--model_type` | `proposed`/`deeponet`/`fno`/`kno`/`cno` | proposed |
| `--ablation` | `none`/`no_prior`/`no_graph`/`no_data_loss`/`no_prior_loss` | none |
| `--distributed` | 启用多卡 DDP | off |
| `--seed` | 全局随机种子 | 123 |

运行示例：
```bash
# 单卡 — 本文完整方法
python ocean_trainer_forward_b.py \
    --data_dir ../Ocean --dataset_name rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000 \
    --epochs 200 --model_type proposed

# 多卡 DDP (4 GPU)
torchrun --nproc_per_node=4 ocean_trainer_forward_b.py \
    --data_dir ../Ocean --dataset_name rectangle_..._spf2000 --distributed --epochs 200

# 基线对比 (如 FNO) / 消融 (如去物理先验)
python ocean_trainer_forward_b.py ... --model_type fno
python ocean_trainer_forward_b.py ... --model_type proposed --ablation no_prior
```

> DataLoader 用 `FrequencyGroupedSampler`（按频率分组，`shuffle=False`），
> 保证同批同频率；训练/测试划分由种子确定，复现一致。

---

## 模型结构 — `deq_modules/models.py`

本文方法 `GNNModel_Forward`（trainer 入口）由三部分串联：

1. **物理先验网络** `_FNOScatterField` — FNO 全局谱算子，输入频率+源坐标+网格坐标，直出近似压力场。
2. **FEM 残差引导图网络** `FEMGuidedGraphNet` — 用 FEM 边权(A)与右端项(B)驱动的多尺度(1/2/4/8 跳)图卷积修正先验场。
3. **先验-FEM 融合** `PriorFEMFusion` — 频率自适应 gate 融合两路场，得最终预测。

基线模型（用于论文对比）：`DeepONetBaseline`、`FNO2DBaseline`、`KNOBaseline`、`CNOBaseline`。

---

## 案例 ↔ 配置对应

各案例的数据集配置见论文 Table 3 与 `../MANIFEST.md`；每案例的训练运行完整目录
（日志/指标/权重/图）见 `../Raw_Experimental_Data/<实验类型>/No*/training_run/`。

---

## 依赖环境

- **数据生成**：MATLAB + COMSOL Multiphysics（LiveLink for MATLAB）
- **转换/训练**：Python 3.11，`torch`、`torch_geometric`、`h5py`、`numpy`、`scipy`、
  `scikit-learn`、`matplotlib`、`tqdm`；多卡需 `torch.distributed`（`torchrun`）。
