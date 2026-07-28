# Table 15 — 消融逐频结果 R1

- 对象：`tab:abl-rect`（Table 15）
- 结论：**PASS** — 118 通过 / 0 失败 / 0 警告，共 118 项
- 脚本：`ch4_validation/scripts/T15_abl_rect.py`
- 生成：2026-07-28 21:38:51

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:abl-rect}` 所在 table* 环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/Case25-32_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 25) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No25_R1_Full/training_run/logs/full_run_20260712_150041.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 26) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No26_R1_no_prior/training_run/logs/full_run_20260713_025215.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 27) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No27_R1_no_graph/training_run/logs/full_run_20260712_193334.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 28) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No28_R1_no_prior_loss/training_run/logs/full_run_20260712_150158.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/Case25-32_数据汇总.xlsx | PASS |
| Case 25 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No25_R1_Full/training_run/logs/full_run_20260712_150041.log | PASS |
| Case 26 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No26_R1_no_prior/training_run/logs/full_run_20260713_025215.log | PASS |
| Case 27 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No27_R1_no_graph/training_run/logs/full_run_20260712_193334.log | PASS |
| Case 28 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No28_R1_no_prior_loss/training_run/logs/full_run_20260712_150158.log | PASS |
| tex 表格环境可定位且确实包住 label | `tab:abl-rect`，长度 1520 | PASS |
| tex 数据行数 = 4 | 实得 4 | PASS |
| tex 行 No. 覆盖 15-19 | [25, 26, 27, 28] | PASS |

## 3. best epoch 一致性

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 25 best epoch | xlsx `194` / log `194` | PASS |
| Case 25 日志含『评估 Epoch 194』块 | 轮次 194 | PASS |
| Case 26 best epoch | xlsx `82` / log `82` | PASS |
| Case 26 日志含『评估 Epoch 82』块 | 轮次 82 | PASS |
| Case 27 best epoch | xlsx `199` / log `199` | PASS |
| Case 27 日志含『评估 Epoch 199』块 | 轮次 199 | PASS |
| Case 28 best epoch | xlsx `199` / log `199` | PASS |
| Case 28 日志含『评估 Epoch 199』块 | 轮次 199 | PASS |

## 4. 双渠道交叉验证（xlsx vs log，同一 best epoch）

> 日志侧取『评估 Epoch N 完成』块（测试集），非『训练』块；Sol 由 `(损失 − w_prior×prior)/w_rel` 现场算，权重逐轮解析。

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 25 Overall SOL | `11.48282000795007` / `11.48282` | PASS |
| Case 25 Overall TL | `1.911368` / `1.911368` | PASS |
| Case 25 25 SOL | `16.63692949805409` / `16.6369326` | PASS |
| Case 25 25 TL | `1.377714` / `1.377714` | PASS |
| Case 25 50 SOL | `0.5120271787745878` / `0.51202722` | PASS |
| Case 25 50 TL | `0.6034657` / `0.6034657` | PASS |
| Case 25 75 SOL | `10.12754489202052` / `10.1275455` | PASS |
| Case 25 75 TL | `1.990745` / `1.990745` | PASS |
| Case 25 100 SOL | `18.65477762185037` / `18.6547783` | PASS |
| Case 25 100 TL | `3.673548` / `3.673548` | PASS |
| Case 26 Overall SOL | `649.1932973265648` / `649.1932999999999` | PASS |
| Case 26 Overall TL | `38.80033` / `38.80033` | PASS |
| Case 26 25 SOL | `1563.083946704865` / `1563.0834799999998` | PASS |
| Case 26 25 TL | `22.93166` / `22.93166` | PASS |
| Case 26 50 SOL | `479.50402945280075` / `479.50399300000004` | PASS |
| Case 26 50 TL | `32.71898` / `32.71898` | PASS |
| Case 26 75 SOL | `424.60011579096323` / `424.6001` | PASS |
| Case 26 75 TL | `46.46738` / `46.46738` | PASS |
| Case 26 100 SOL | `129.5851467177272` / `129.585123` | PASS |
| Case 26 100 TL | `53.08328` / `53.08328` | PASS |
| Case 27 Overall SOL | `13.350991916377101` / `13.35099` | PASS |
| Case 27 Overall TL | `2.205796` / `2.205796` | PASS |
| Case 27 25 SOL | `10.36997995106504` / `10.369980199999999` | PASS |
| Case 27 25 TL | `1.087888` / `1.087888` | PASS |
| Case 27 50 SOL | `0.5764913483290002` / `0.576491387` | PASS |
| Case 27 50 TL | `0.630979` / `0.630979` | PASS |
| Case 27 75 SOL | `19.53623965382576` / `19.5362376` | PASS |
| Case 27 75 TL | `2.559839` / `2.559839` | PASS |
| Case 27 100 SOL | `22.92125532403589` / `22.921257500000003` | PASS |
| Case 27 100 TL | `4.544477` / `4.544477` | PASS |
| Case 28 Overall SOL | `11.31177544593811` / `11.31178` | PASS |
| Case 28 Overall TL | `2.072516` / `2.072516` | PASS |
| Case 28 25 SOL | `3.189601749181748` / `3.189602` | PASS |
| Case 28 25 TL | `0.7414964` / `0.7414964` | PASS |
| Case 28 50 SOL | `0.5421166773885489` / `0.5421167` | PASS |
| Case 28 50 TL | `0.629636` / `0.629636` | PASS |
| Case 28 75 SOL | `19.97445821762085` / `19.97446` | PASS |
| Case 28 75 TL | `2.609463` / `2.609463` | PASS |
| Case 28 100 SOL | `21.54092490673066` / `21.540919999999996` | PASS |
| Case 28 100 TL | `4.309467` / `4.309467` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Variant, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。Avg. 对应 xlsx/日志的 Overall 组。本表无 Fig. 列。日志渠道的一致性已在第 4 节双渠道验证中确认，此处仅比对 xlsx。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 25 Variant 名 | tex `Full model` | PASS |
| Case 25 25Hz SOL (xlsx) | 源 16.63692949805409 → `16.637` / 印刷 `16.637` | PASS |
| Case 25 25Hz TL (xlsx) | 源 1.377714 → `1.378` / 印刷 `1.378` | PASS |
| Case 25 50Hz SOL (xlsx) | 源 0.5120271787745878 → `0.512` / 印刷 `0.512` | PASS |
| Case 25 50Hz TL (xlsx) | 源 0.6034657 → `0.603` / 印刷 `0.603` | PASS |
| Case 25 75Hz SOL (xlsx) | 源 10.12754489202052 → `10.128` / 印刷 `10.128` | PASS |
| Case 25 75Hz TL (xlsx) | 源 1.990745 → `1.991` / 印刷 `1.991` | PASS |
| Case 25 100Hz SOL (xlsx) | 源 18.65477762185037 → `18.655` / 印刷 `18.655` | PASS |
| Case 25 100Hz TL (xlsx) | 源 3.673548 → `3.674` / 印刷 `3.674` | PASS |
| Case 25 Avg. SOL (xlsx) | 源 11.48282000795007 → `11.483` / 印刷 `11.483` | PASS |
| Case 25 Avg. TL (xlsx) | 源 1.911368 → `1.911` / 印刷 `1.911` | PASS |
| Case 26 Variant 名 | tex `w/o physics prior` | PASS |
| Case 26 25Hz SOL (xlsx) | 源 1563.083946704865 → `1563.084` / 印刷 `1563.084` | PASS |
| Case 26 25Hz TL (xlsx) | 源 22.93166 → `22.932` / 印刷 `22.932` | PASS |
| Case 26 50Hz SOL (xlsx) | 源 479.50402945280075 → `479.504` / 印刷 `479.504` | PASS |
| Case 26 50Hz TL (xlsx) | 源 32.71898 → `32.719` / 印刷 `32.719` | PASS |
| Case 26 75Hz SOL (xlsx) | 源 424.60011579096323 → `424.600` / 印刷 `424.600` | PASS |
| Case 26 75Hz TL (xlsx) | 源 46.46738 → `46.467` / 印刷 `46.467` | PASS |
| Case 26 100Hz SOL (xlsx) | 源 129.5851467177272 → `129.585` / 印刷 `129.585` | PASS |
| Case 26 100Hz TL (xlsx) | 源 53.08328 → `53.083` / 印刷 `53.083` | PASS |
| Case 26 Avg. SOL (xlsx) | 源 649.1932973265648 → `649.193` / 印刷 `649.193` | PASS |
| Case 26 Avg. TL (xlsx) | 源 38.80033 → `38.800` / 印刷 `38.800` | PASS |
| Case 27 Variant 名 | tex `w/o graph correction` | PASS |
| Case 27 25Hz SOL (xlsx) | 源 10.36997995106504 → `10.370` / 印刷 `10.370` | PASS |
| Case 27 25Hz TL (xlsx) | 源 1.087888 → `1.088` / 印刷 `1.088` | PASS |
| Case 27 50Hz SOL (xlsx) | 源 0.5764913483290002 → `0.576` / 印刷 `0.576` | PASS |
| Case 27 50Hz TL (xlsx) | 源 0.630979 → `0.631` / 印刷 `0.631` | PASS |
| Case 27 75Hz SOL (xlsx) | 源 19.53623965382576 → `19.536` / 印刷 `19.536` | PASS |
| Case 27 75Hz TL (xlsx) | 源 2.559839 → `2.560` / 印刷 `2.560` | PASS |
| Case 27 100Hz SOL (xlsx) | 源 22.92125532403589 → `22.921` / 印刷 `22.921` | PASS |
| Case 27 100Hz TL (xlsx) | 源 4.544477 → `4.544` / 印刷 `4.544` | PASS |
| Case 27 Avg. SOL (xlsx) | 源 13.350991916377101 → `13.351` / 印刷 `13.351` | PASS |
| Case 27 Avg. TL (xlsx) | 源 2.205796 → `2.206` / 印刷 `2.206` | PASS |
| Case 28 Variant 名 | tex `w/o prior supervision` | PASS |
| Case 28 25Hz SOL (xlsx) | 源 3.189601749181748 → `3.190` / 印刷 `3.190` | PASS |
| Case 28 25Hz TL (xlsx) | 源 0.7414964 → `0.741` / 印刷 `0.741` | PASS |
| Case 28 50Hz SOL (xlsx) | 源 0.5421166773885489 → `0.542` / 印刷 `0.542` | PASS |
| Case 28 50Hz TL (xlsx) | 源 0.629636 → `0.630` / 印刷 `0.630` | PASS |
| Case 28 75Hz SOL (xlsx) | 源 19.97445821762085 → `19.974` / 印刷 `19.974` | PASS |
| Case 28 75Hz TL (xlsx) | 源 2.609463 → `2.609` / 印刷 `2.609` | PASS |
| Case 28 100Hz SOL (xlsx) | 源 21.54092490673066 → `21.541` / 印刷 `21.541` | PASS |
| Case 28 100Hz TL (xlsx) | 源 4.309467 → `4.309` / 印刷 `4.309` | PASS |
| Case 28 Avg. SOL (xlsx) | 源 11.31177544593811 → `11.312` / 印刷 `11.312` | PASS |
| Case 28 Avg. TL (xlsx) | 源 2.072516 → `2.073` / 印刷 `2.073` | PASS |

## 6. Avg. 列与四频均值自洽

> caption 声明 Avg. 为四频均值；四频样本数相等，故等权均值应等于 Overall 组。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 25 Avg. SOL = 四频均值 | 均值 `11.4828` / Overall `11.4828` | PASS |
| Case 25 Avg. TL = 四频均值 | 均值 `1.91137` / Overall `1.91137` | PASS |
| Case 26 Avg. SOL = 四频均值 | 均值 `649.193` / Overall `649.193` | PASS |
| Case 26 Avg. TL = 四频均值 | 均值 `38.8003` / Overall `38.8003` | PASS |
| Case 27 Avg. SOL = 四频均值 | 均值 `13.351` / Overall `13.351` | PASS |
| Case 27 Avg. TL = 四频均值 | 均值 `2.2058` / Overall `2.2058` | PASS |
| Case 28 Avg. SOL = 四频均值 | 均值 `11.3118` / Overall `11.3118` | PASS |
| Case 28 Avg. TL = 四频均值 | 均值 `2.07252` / Overall `2.07252` | PASS |

## 7. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 40 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 8. 正文引用精确性（4.5 节）

> 每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。只查①会漏掉正文与表格一起错的情形。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 Case 25 Full model 频均 Sol | 正文 `11.483` / 表格 `11.483` | PASS |
| 正文 Case 25 Full model 频均 Sol <- xlsx 源 | 源 11.48282000795007 → `11.483` / 印刷 `11.483` | PASS |
| 正文 Case 25 Full model 频均 TL | 正文 `1.911` / 表格 `1.911` | PASS |
| 正文 Case 25 Full model 频均 TL <- xlsx 源 | 源 1.911368 → `1.911` / 印刷 `1.911` | PASS |
| 正文 Case 26 w/o prior 频均 Sol | 正文 `649.193` / 表格 `649.193` | PASS |
| 正文 Case 26 w/o prior 频均 Sol <- xlsx 源 | 源 649.1932973265648 → `649.193` / 印刷 `649.193` | PASS |
| 正文 Case 26 w/o prior 频均 TL | 正文 `38.800` / 表格 `38.800` | PASS |
| 正文 Case 26 w/o prior 频均 TL <- xlsx 源 | 源 38.80033 → `38.800` / 印刷 `38.800` | PASS |

## X. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

