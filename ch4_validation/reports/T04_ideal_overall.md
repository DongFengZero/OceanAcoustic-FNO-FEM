# Table 4 — 解析解场精度 R0/W0

- 对象：`tab:ideal-overall`（Table 4）
- 结论：**PASS** — 87 通过 / 0 失败 / 0 警告，共 87 项
- 脚本：`ch4_validation/scripts/T04_ideal_overall.py`
- 生成：2026-07-28 21:38:07

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:ideal-overall}` 所在 minipage |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/Case1-2_数据汇总.xlsx` | 工作表1『Case1-2 汇总』，best epoch 全测试集 |
| 渠道2 log (Case 1) | `Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No01_R0/train_rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000_analyticsol__ratio0.90_bs1_mi4_hc48_ddp/logs/full_run_20260719_221907.log` | 训练日志 best epoch 原始块 |
| 渠道2 log (Case 2) | `Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No02_W0/train_wedge_Lx128_Ly128_H1.000_f25_50_75_100_spf2000_analyticsol__ratio0.90_bs1_mi4_hc48_ddp/logs/full_run_20260720_031249.log` | 训练日志 best epoch 原始块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 存在 | ../JASA/OE/els-cas-templates/OE_submission.tex | PASS |
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/Case1-2_数据汇总.xlsx | PASS |
| Case 1 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No01_R0/train_rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000_analyticsol__ratio0.90_bs1_mi4_hc48_ddp/logs/full_run_20260719_221907.log | PASS |
| Case 2 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No02_W0/train_wedge_Lx128_Ly128_H1.000_f25_50_75_100_spf2000_analyticsol__ratio0.90_bs1_mi4_hc48_ddp/logs/full_run_20260720_031249.log | PASS |
| tex 表格环境可定位 | `tab:ideal-overall` | PASS |
| tex 数据行数 = 2 | 实得 2 | PASS |
| tex 行 No. 覆盖 Case 1-2 | [1, 2] | PASS |

## 3. best epoch 一致性

> xlsx 的 Best Epoch 列与日志里最后一次“保存最佳模型 (Epoch N)”必须同值；两者不一致则后续所有取值都在比不同轮次。

| 案例 | xlsx Best Epoch / 日志自证 | 结论 |
|---|---|---|
| Case 1 best epoch | xlsx `200` / log `200` | PASS |
| Case 1 日志含 Epoch 200 统计块 | 轮次 200 | PASS |
| Case 2 best epoch | xlsx `199` / log `199` | PASS |
| Case 2 日志含 Epoch 199 统计块 | 轮次 199 | PASS |

## 4. 双渠道交叉验证（xlsx vs log，同一 best epoch）

> 日志侧 Sol 由 `(总损失 − w_prior×prior)/w_rel` 现场计算，权重从该轮 `Loss Weights:` 行解析，不假定为常数。

> Case 1 解析到的损失权重：rel_mse=1.00e+02, prior=1.00e+00

> Case 2 解析到的损失权重：rel_mse=1.00e+02, prior=1.00e+00

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 1 Overall SOL | `2.090045413933694` / `2.090045` | PASS |
| Case 1 Overall TL | `0.5088705` / `0.5088705` | PASS |
| Case 1 25 SOL | `2.9437884426442906` / `2.9437885699999997` | PASS |
| Case 1 25 TL | `0.4107766` / `0.4107766` | PASS |
| Case 1 50 SOL | `0.9853098075836898` / `0.9853102600000001` | PASS |
| Case 1 50 TL | `0.1313123` / `0.1313123` | PASS |
| Case 1 75 SOL | `2.919280910282396` / `2.91928079` | PASS |
| Case 1 75 TL | `0.7279129` / `0.7279129` | PASS |
| Case 1 100 SOL | `1.511802599998191` / `1.51180265` | PASS |
| Case 1 100 TL | `0.76548` / `0.76548` | PASS |
| Case 2 Overall SOL | `3.382503363536671` / `3.382504` | PASS |
| Case 2 Overall TL | `0.5140532` / `0.5140532` | PASS |
| Case 2 25 SOL | `6.115809269249438` / `6.1158089` | PASS |
| Case 2 25 TL | `0.3612889` / `0.3612889` | PASS |
| Case 2 50 SOL | `0.4623499284207355` / `0.4623499280000001` | PASS |
| Case 2 50 TL | `0.1491131` / `0.1491131` | PASS |
| Case 2 75 SOL | `2.773482297197916` / `2.77348229` | PASS |
| Case 2 75 TL | `0.589117` / `0.589117` | PASS |
| Case 2 100 SOL | `4.178372432943434` / `4.17837285` | PASS |
| Case 2 100 TL | `0.956694` / `0.956694` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Dataset, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。Avg. 对应 xlsx/日志的 Overall 组。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 1 Dataset 名 | tex `R0 (rect.)` | PASS |
| Case 1 25Hz SOL (xlsx) | 源 2.9437884426442906 → `2.944` / 印刷 `2.944` | PASS |
| Case 1 25Hz SOL (log) | 源 2.9437885699999997 → `2.944` / 印刷 `2.944` | PASS |
| Case 1 25Hz TL (xlsx) | 源 0.4107766 → `0.411` / 印刷 `0.411` | PASS |
| Case 1 25Hz TL (log) | 源 0.4107766 → `0.411` / 印刷 `0.411` | PASS |
| Case 1 50Hz SOL (xlsx) | 源 0.9853098075836898 → `0.985` / 印刷 `0.985` | PASS |
| Case 1 50Hz SOL (log) | 源 0.9853102600000001 → `0.985` / 印刷 `0.985` | PASS |
| Case 1 50Hz TL (xlsx) | 源 0.1313123 → `0.131` / 印刷 `0.131` | PASS |
| Case 1 50Hz TL (log) | 源 0.1313123 → `0.131` / 印刷 `0.131` | PASS |
| Case 1 75Hz SOL (xlsx) | 源 2.919280910282396 → `2.919` / 印刷 `2.919` | PASS |
| Case 1 75Hz SOL (log) | 源 2.91928079 → `2.919` / 印刷 `2.919` | PASS |
| Case 1 75Hz TL (xlsx) | 源 0.7279129 → `0.728` / 印刷 `0.728` | PASS |
| Case 1 75Hz TL (log) | 源 0.7279129 → `0.728` / 印刷 `0.728` | PASS |
| Case 1 100Hz SOL (xlsx) | 源 1.511802599998191 → `1.512` / 印刷 `1.512` | PASS |
| Case 1 100Hz SOL (log) | 源 1.51180265 → `1.512` / 印刷 `1.512` | PASS |
| Case 1 100Hz TL (xlsx) | 源 0.76548 → `0.765` / 印刷 `0.765` | PASS |
| Case 1 100Hz TL (log) | 源 0.76548 → `0.765` / 印刷 `0.765` | PASS |
| Case 1 Avg. SOL (xlsx) | 源 2.090045413933694 → `2.090` / 印刷 `2.090` | PASS |
| Case 1 Avg. SOL (log) | 源 2.090045 → `2.090` / 印刷 `2.090` | PASS |
| Case 1 Avg. TL (xlsx) | 源 0.5088705 → `0.509` / 印刷 `0.509` | PASS |
| Case 1 Avg. TL (log) | 源 0.5088705 → `0.509` / 印刷 `0.509` | PASS |
| Case 2 Dataset 名 | tex `W0 (wedge)` | PASS |
| Case 2 25Hz SOL (xlsx) | 源 6.115809269249438 → `6.116` / 印刷 `6.116` | PASS |
| Case 2 25Hz SOL (log) | 源 6.1158089 → `6.116` / 印刷 `6.116` | PASS |
| Case 2 25Hz TL (xlsx) | 源 0.3612889 → `0.361` / 印刷 `0.361` | PASS |
| Case 2 25Hz TL (log) | 源 0.3612889 → `0.361` / 印刷 `0.361` | PASS |
| Case 2 50Hz SOL (xlsx) | 源 0.4623499284207355 → `0.462` / 印刷 `0.462` | PASS |
| Case 2 50Hz SOL (log) | 源 0.4623499280000001 → `0.462` / 印刷 `0.462` | PASS |
| Case 2 50Hz TL (xlsx) | 源 0.1491131 → `0.149` / 印刷 `0.149` | PASS |
| Case 2 50Hz TL (log) | 源 0.1491131 → `0.149` / 印刷 `0.149` | PASS |
| Case 2 75Hz SOL (xlsx) | 源 2.773482297197916 → `2.773` / 印刷 `2.773` | PASS |
| Case 2 75Hz SOL (log) | 源 2.77348229 → `2.773` / 印刷 `2.773` | PASS |
| Case 2 75Hz TL (xlsx) | 源 0.589117 → `0.589` / 印刷 `0.589` | PASS |
| Case 2 75Hz TL (log) | 源 0.589117 → `0.589` / 印刷 `0.589` | PASS |
| Case 2 100Hz SOL (xlsx) | 源 4.178372432943434 → `4.178` / 印刷 `4.178` | PASS |
| Case 2 100Hz SOL (log) | 源 4.17837285 → `4.178` / 印刷 `4.178` | PASS |
| Case 2 100Hz TL (xlsx) | 源 0.956694 → `0.957` / 印刷 `0.957` | PASS |
| Case 2 100Hz TL (log) | 源 0.956694 → `0.957` / 印刷 `0.957` | PASS |
| Case 2 Avg. SOL (xlsx) | 源 3.382503363536671 → `3.383` / 印刷 `3.383` | PASS |
| Case 2 Avg. SOL (log) | 源 3.382504 → `3.383` / 印刷 `3.383` | PASS |
| Case 2 Avg. TL (xlsx) | 源 0.5140532 → `0.514` / 印刷 `0.514` | PASS |
| Case 2 Avg. TL (log) | 源 0.5140532 → `0.514` / 印刷 `0.514` | PASS |

## 6. Avg. 列与四频均值自洽

> caption 声明 “Avg. is the mean over the four frequencies”，四频样本数相等（各 1800），故等权均值应与 Overall 组一致。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 1 Avg. SOL = 四频均值 | 均值 `2.09005` / Overall `2.09005` | PASS |
| Case 1 Avg. TL = 四频均值 | 均值 `0.50887` / Overall `0.508871` | PASS |
| Case 2 Avg. SOL = 四频均值 | 均值 `3.3825` / Overall `3.3825` | PASS |
| Case 2 Avg. TL = 四频均值 | 均值 `0.514053` / Overall `0.514053` | PASS |

## 7. 同表小数位一致性

> 要求：同一表格内 Sol 与 TL 一律 3 位小数，不因数值大小变位数。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 20 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 8. 正文引用精确性（4.2 节）

> 判定不设容差：正文字面量须与表格印刷值逐字符相同，位数不足（如 `0.51` 之于 `0.509`）即判失败。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 R0 频均 Sol | 正文 `2.090` / 表格 `2.090` — tex 行 686 | PASS |
| 正文 R0 频均 Sol ← xlsx 源 | 源 2.090045413933694 → `2.090` / 印刷 `2.090` | PASS |
| 正文 W0 频均 Sol | 正文 `3.383` / 表格 `3.383` — tex 行 686 | PASS |
| 正文 W0 频均 Sol ← xlsx 源 | 源 3.382503363536671 → `3.383` / 印刷 `3.383` | PASS |
| 正文 R0 场 TL | 正文 `0.509` / 表格 `0.509` — tex 行 686 | PASS |
| 正文 R0 场 TL ← xlsx 源 | 源 0.5088705 → `0.509` / 印刷 `0.509` | PASS |
| 正文 W0 场 TL | 正文 `0.514` / 表格 `0.514` — tex 行 686 | PASS |
| 正文 W0 场 TL ← xlsx 源 | 源 0.5140532 → `0.514` / 印刷 `0.514` | PASS |

## 8. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

