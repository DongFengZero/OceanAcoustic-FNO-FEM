# Data and Code Availability — Manifest

按实验类型(第四章小节)分文件夹，每案例一子目录，内含该案例全部输出文件及其训练运行目录 `training_run/`(logs / config / metrics / plots / 模型权重)。

```
Raw_Experimental_Data/
  4.2_Validation/  4.3_Forward/  4.4_Comparison/  4.5_Ablation/
  4.6_Mesh/  4.7_Generalization/  4.8_Performance/
Validation_Scripts/
```

## 案例清单

| No. | 小节 | 子目录 | 输出文件数 | 训练目录 | 备注 |
|----:|:-----|:-------|:----------:|:---------|:-----|
| 1 | 4.2_Validation | No01_R0 | 8 | train:none | ideal; 训练日志见 dataset 仓库 |
| 2 | 4.2_Validation | No02_W0 | 8 | train:none | ideal; 训练日志见 dataset 仓库 |
| 3 | 4.3_Forward | No03_R1 | 7 | train_OK(40f) |  |
| 4 | 4.3_Forward | No04_R2 | 7 | train_OK(40f) |  |
| 5 | 4.3_Forward | No05_R3 | 7 | train_OK(40f) |  |
| 6 | 4.3_Forward | No06_R4 | 4 | train_OK(37f) |  |
| 7 | 4.3_Forward | No07_R5 | 4 | train_OK(37f) |  |
| 8 | 4.3_Forward | No08_R6 | 4 | train_OK(37f) |  |
| 9 | 4.3_Forward | No09_W1 | 7 | train_OK(40f) |  |
| 10 | 4.3_Forward | No10_W2 | 7 | train_OK(40f) |  |
| 11 | 4.3_Forward | No11_W3 | 7 | train_OK(45f) |  |
| 12 | 4.3_Forward | No12_W4 | 4 | train_OK(38f) |  |
| 13 | 4.3_Forward | No13_W5 | 4 | train_OK(37f) |  |
| 14 | 4.3_Forward | No14_W6 | 4 | train_OK(37f) |  |
| 15 | 4.4_Comparison | No15_R1_Proposed | 7 | train_OK(40f) | reuse No.3 |
| 16 | 4.4_Comparison | No16_R1_DeepONet | 7 | train_OK(40f) |  |
| 17 | 4.4_Comparison | No17_R1_FNO | 7 | train_OK(40f) |  |
| 18 | 4.4_Comparison | No18_R1_KNO | 7 | train_OK(40f) |  |
| 19 | 4.4_Comparison | No19_R1_CNO | 7 | train_OK(40f) |  |
| 20 | 4.4_Comparison | No20_W1_Proposed | 7 | train_OK(40f) | reuse No.9 |
| 21 | 4.4_Comparison | No21_W1_DeepONet | 7 | train_OK(40f) |  |
| 22 | 4.4_Comparison | No22_W1_FNO | 7 | train_OK(41f) |  |
| 23 | 4.4_Comparison | No23_W1_KNO | 7 | train_OK(40f) |  |
| 24 | 4.4_Comparison | No24_W1_CNO | 7 | train_OK(40f) |  |
| 25 | 4.5_Ablation | No25_R1_Full | 7 | train_OK(56f) | A800 re-run |
| 26 | 4.5_Ablation | No26_R1_no_prior | 7 | train_OK(40f) |  |
| 27 | 4.5_Ablation | No27_R1_no_graph | 7 | train_OK(41f) |  |
| 28 | 4.5_Ablation | No28_R1_no_prior_loss | 7 | train_OK(41f) |  |
| 29 | 4.5_Ablation | No29_W1_Full | 7 | train_OK(49f) | A800 re-run |
| 30 | 4.5_Ablation | No30_W1_no_prior | 7 | train_OK(40f) |  |
| 31 | 4.5_Ablation | No31_W1_no_graph | 7 | train_OK(40f) |  |
| 32 | 4.5_Ablation | No32_W1_no_prior_loss | 7 | train_OK(40f) |  |
| 33 | 4.6_Mesh | No33_R4 | 4 | train_OK(37f) | reuse No.6 |
| 34 | 4.6_Mesh | No34_R7 | 4 | train_OK(37f) |  |
| 35 | 4.6_Mesh | No35_R8 | 4 | train_OK(37f) |  |
| 36 | 4.6_Mesh | No36_W4 | 4 | train_OK(38f) | reuse No.12 |
| 37 | 4.6_Mesh | No37_W7 | 4 | train_OK(38f) |  |
| 38 | 4.6_Mesh | No38_W8 | 4 | train_OK(39f) |  |
| 39 | 4.7_Generalization | No39_R9 | 7 | train:none | extrap split; 训练日志见 code 仓库 |
| 40 | 4.7_Generalization | No40_R10 | 7 | train:none | extrap split; 训练日志见 code 仓库 |
| 41 | 4.7_Generalization | No41_W9 | 7 | train:none | extrap split; 训练日志见 code 仓库 |
| 42 | 4.7_Generalization | No42_W10 | 7 | train:none | extrap split; 训练日志见 code 仓库 |
| 43 | 4.8_Performance | No43_R1 | 0 | train:none | runtime 基准; 数据在性能分析 xlsx |
| 44 | 4.8_Performance | No44_W1 | 0 | train:none | runtime 基准; 数据在性能分析 xlsx |
| 45 | 4.8_Performance | No45_R4 | 0 | train_OK(37f) | reuse No.6 |
| 46 | 4.8_Performance | No46_R5 | 0 | train_OK(37f) | reuse No.7 |
| 47 | 4.8_Performance | No47_R6 | 0 | train_OK(37f) | reuse No.8 |
| 48 | 4.8_Performance | No48_W4 | 0 | train_OK(38f) | reuse No.12 |
| 49 | 4.8_Performance | No49_W5 | 0 | train_OK(37f) | reuse No.13 |
| 50 | 4.8_Performance | No50_W6 | 0 | train_OK(37f) | reuse No.14 |

## 验证脚本

- `regen_ideal_panels.py`
- `regen_results_bigfont.py`
- `regen_wide_fields.py`
- `advantage_depth_line.py`
- `scan_depth_lines.py`
- `regen_method_grid.py`
- `regen_gen_extrap_bigfont.py`
- `build_perf.py`
- `restore_tl_figure.py`
- `redraw_tl_figures.py`

## 说明

- 每案例 `training_run/` 为该配置的训练运行完整目录(含 `logs/full_run_*.log`、`statistics_epoch*.json`、`models/best_model.pth`、`plots/`)。
- No.1-2(理想解析)与 No.39-42(泛化外推)按不同 split 训练，其运行目录随 code/dataset 仓库发布，此处仅含案例输出。
- No.15/20(对比 Proposed)与 No.33/36、45-50 复用早期训练(见备注)，train 目录同源。
- No.43-44 运行时基准数据见 `4.8_Performance/Case43-50_推理时间性能分析.xlsx`。