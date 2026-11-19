# Table — — 4.8 节离线成本与盈亏点（日志 ↔ 正文）

- 对象：`prose (Sec. 4.8 cost paragraph)`（Table —）
- 结论：**PASS** — 23 通过 / 0 失败 / 0 警告，共 23 项
- 脚本：`ch4_validation/scripts/PROSE_cost.py`
- 生成：2026-11-19 23:50:10

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE期刊/paper_R2/OE_submission.tex` | Sec. 4.8 末段 |
| COMSOL 生成日志 | `Data_and_Code_Availability/Dataset/R1/rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000/run_rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000_20260622_155328.log` | R1 数据集，全局统计块 |
| 训练统计 JSON | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No15_R1_Proposed/training_run/logs/statistics_epoch200.json` | Case 15，timing_summary.train.total_s |
| 训练日志 | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No15_R1_Proposed/training_run/logs/full_run_20260710_221657.log` | Case 15，使用GPU数量 |
| 单卡推理日志 | `Data_and_Code_Availability/Raw_Experimental_Data/4.8_Performance/No43_R1/training_run/logs/gpu1_full_run_20260721_111502.log` | Case 43，测试集平均每样本时间 |

## 1. 源日志可解析

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 4.8 节成本段可定位 | 起句 `A comparison of this kind is complete…` | PASS |
| COMSOL 生成日志含全局统计块 | {'n': 8000.0, 'mean_ms': 873.1, 'median_ms': 871.4, 'p95_ms': 973.2, 'total_s': 6984.4} | PASS |
| Case 15 statistics_epoch200.json 含训练墙钟 | total_s=22351.81516236067 epoch=200 | PASS |
| Case 15 日志含卡数 | n_gpu=8 | PASS |
| Case 43 单卡日志含测试集每样本时间 | 17.08 ms | PASS |

## 2. 正文字面量 ↔ 源值（按印刷位数舍入）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 8000 个参考解 = 日志总样本数 | `$8000$ reference solutions` | PASS |
| 数据生成 1.94 h = 求解总计/3600 | `$1.94$\,h` | PASS |
| 均值 873.1 ms | `$873.1$\,ms per solve` | PASS |
| 中位数 871.4 ms | `median of $871.4$\,ms` | PASS |
| P95 973.2 ms | `95th percentile of $973.2$\,ms` | PASS |
| 训练 6.21 h = total_s/3600 | `$6.21$\,h on eight accelerators` | PASS |
| 49.7 卡时 = 6.21 h × 8 | `$49.7$ GPU-hours` | PASS |
| 训练 22352 s（取整） | `$22352$\,s of training` | PASS |
| 数据生成 6984 s（取整） | `$6984$\,s of data generation` | PASS |
| 推理 17.08 ms（Case 43 单卡） | `$17.08$\,ms in Case~43` | PASS |
| COMSOL 873.1 ms（同一均值） | `$873.1$\,ms for COMSOL` | PASS |
| 卡数 8 ↔ 正文 eight accelerators | 日志 8 | PASS |

## 3. 推导量（用正文印刷值现场重算）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 每次查询节省 0.856 s = (873.1 − 17.08)/1000 | `0.8560` | PASS |
| 离线总计 29336 s = 22352 + 6984 |  | PASS |
| 盈亏点 N* = 29336/0.856 = 34271 → 3.4×10^4 | `N^{*}\approx3.4\times10^{4}` | PASS |
| N*/8000 = 4.28 → "about four times" |  | PASS |

## 4. 口径句

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 口径：训练 8 卡墙钟 + 单卡推理 |  | PASS |
| 训练归 Case 15、推理归 Case 43 |  | PASS |

