# Table 14 — 五方法逐频精度 W1

- 对象：`tab:perf-wedge`（Table 14）
- 结论：**PASS** — 198 通过 / 0 失败 / 0 警告，共 198 项
- 脚本：`ch4_validation/scripts/T14_perf_wedge.py`
- 生成：2026-07-29 00:55:34

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:perf-wedge}` 所在 table* 环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/Case15-24_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 20) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No20_W1_Proposed/training_run/logs/full_run_20260710_152228.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 21) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No21_W1_DeepONet/training_run/logs/full_run_20260710_162410.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 22) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No22_W1_FNO/training_run/logs/full_run_20260710_172139.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 23) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No23_W1_KNO/training_run/logs/full_run_20260710_202430.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 24) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No24_W1_CNO/training_run/logs/full_run_20260710_184721.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/Case15-24_数据汇总.xlsx | PASS |
| Case 20 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No20_W1_Proposed/training_run/logs/full_run_20260710_152228.log | PASS |
| Case 21 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No21_W1_DeepONet/training_run/logs/full_run_20260710_162410.log | PASS |
| Case 22 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No22_W1_FNO/training_run/logs/full_run_20260710_172139.log | PASS |
| Case 23 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No23_W1_KNO/training_run/logs/full_run_20260710_202430.log | PASS |
| Case 24 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No24_W1_CNO/training_run/logs/full_run_20260710_184721.log | PASS |
| tex 表格环境可定位且确实包住 label | `tab:perf-wedge`，长度 1550 | PASS |
| tex 数据行数 = 5 | 实得 5 | PASS |
| tex 行 No. 覆盖 20-24 | [20, 21, 22, 23, 24] | PASS |

## 3. best epoch 一致性

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 20 best epoch | xlsx `181` / log `181` | PASS |
| Case 20 日志含『评估 Epoch 181』块 | 轮次 181 | PASS |
| Case 21 best epoch | xlsx `195` / log `195` | PASS |
| Case 21 日志含『评估 Epoch 195』块 | 轮次 195 | PASS |
| Case 22 best epoch | xlsx `194` / log `194` | PASS |
| Case 22 日志含『评估 Epoch 194』块 | 轮次 194 | PASS |
| Case 23 best epoch | xlsx `200` / log `200` | PASS |
| Case 23 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |
| Case 24 best epoch | xlsx `200` / log `200` | PASS |
| Case 24 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |

## 4. 双渠道交叉验证（xlsx vs log，同一 best epoch）

> 日志侧取『评估 Epoch N 完成』块（测试集），非『训练』块；Sol 由 `(损失 − w_prior×prior)/w_rel` 现场算，权重逐轮解析。

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 20 Overall SOL | `2.1209166909102346` / `2.120917` | PASS |
| Case 20 Overall TL | `0.899286` / `0.899286` | PASS |
| Case 20 25 SOL | `3.958929784130305` / `3.9589297199999995` | PASS |
| Case 20 25 TL | `0.7091513` / `0.7091513` | PASS |
| Case 20 50 SOL | `0.26640543073881423` / `0.266405447` | PASS |
| Case 20 50 TL | `0.6107074` / `0.6107074` | PASS |
| Case 20 75 SOL | `1.9178623508196322` / `1.9178620900000003` | PASS |
| Case 20 75 TL | `1.011998` / `1.011998` | PASS |
| Case 20 100 SOL | `2.340470429044217` / `2.3404708999999997` | PASS |
| Case 20 100 TL | `1.265287` / `1.265287` | PASS |
| Case 21 Overall SOL | `52.41673775017262` / `52.41674` | PASS |
| Case 21 Overall TL | `2.750098` / `2.750098` | PASS |
| Case 21 25 SOL | `23.320367420092218` / `23.3203663` | PASS |
| Case 21 25 TL | `1.301132` / `1.301132` | PASS |
| Case 21 50 SOL | `12.677953671664001` / `12.677950500000003` | PASS |
| Case 21 50 TL | `1.381942` / `1.381942` | PASS |
| Case 21 75 SOL | `45.68477077409625` / `45.6847723` | PASS |
| Case 21 75 TL | `2.805426` / `2.805426` | PASS |
| Case 21 100 SOL | `127.983848657459` / `127.983862` | PASS |
| Case 21 100 TL | `5.511891` / `5.511891` | PASS |
| Case 22 Overall SOL | `3.179383306996897` / `3.179383` | PASS |
| Case 22 Overall TL | `1.090027` / `1.090027` | PASS |
| Case 22 25 SOL | `5.422724352683872` / `5.42272475` | PASS |
| Case 22 25 TL | `0.8951543` / `0.8951543` | PASS |
| Case 22 50 SOL | `0.40133751172106713` / `0.401337525` | PASS |
| Case 22 50 TL | `0.668` / `0.668` | PASS |
| Case 22 75 SOL | `2.328076647245325` / `2.32807623` | PASS |
| Case 22 75 TL | `1.159577` / `1.159577` | PASS |
| Case 22 100 SOL | `4.565394896781072` / `4.56539505` | PASS |
| Case 22 100 TL | `1.637377` / `1.637377` | PASS |
| Case 23 Overall SOL | `26.13350008614361` / `26.1335` | PASS |
| Case 23 Overall TL | `1.976894` / `1.976894` | PASS |
| Case 23 25 SOL | `46.23470031656326` / `46.234703` | PASS |
| Case 23 25 TL | `1.346344` / `1.346344` | PASS |
| Case 23 50 SOL | `5.179396871244535` / `5.17939703` | PASS |
| Case 23 50 TL | `1.216249` / `1.216249` | PASS |
| Case 23 75 SOL | `24.48505545035005` / `24.485059399999997` | PASS |
| Case 23 75 TL | `2.334058` / `2.334058` | PASS |
| Case 23 100 SOL | `28.634844440966837` / `28.634841599999998` | PASS |
| Case 23 100 TL | `3.010926` / `3.010926` | PASS |
| Case 24 Overall SOL | `47.00651261955499` / `47.00651` | PASS |
| Case 24 Overall TL | `2.375095` / `2.375095` | PASS |
| Case 24 25 SOL | `57.71513618528843` / `57.715138599999996` | PASS |
| Case 24 25 TL | `1.33072` / `1.33072` | PASS |
| Case 24 50 SOL | `6.5668119001202285` / `6.56681187` | PASS |
| Case 24 50 TL | `1.214305` / `1.214305` | PASS |
| Case 24 75 SOL | `53.3690960612148` / `53.36909910000001` | PASS |
| Case 24 75 TL | `2.831276` / `2.831276` | PASS |
| Case 24 100 SOL | `70.37499751895666` / `70.37499999999999` | PASS |
| Case 24 100 TL | `4.124078` / `4.124078` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Method, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。Avg. 对应 xlsx/日志的 Overall 组。本表无 Fig. 列。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 20 Method 名 | tex `Proposed` | PASS |
| Case 20 25Hz SOL (xlsx) | 源 3.958929784130305 → `3.959` / 印刷 `3.959` | PASS |
| Case 20 25Hz SOL (log) | 源 3.9589297199999995 → `3.959` / 印刷 `3.959` | PASS |
| Case 20 25Hz TL (xlsx) | 源 0.7091513 → `0.709` / 印刷 `0.709` | PASS |
| Case 20 25Hz TL (log) | 源 0.7091513 → `0.709` / 印刷 `0.709` | PASS |
| Case 20 50Hz SOL (xlsx) | 源 0.26640543073881423 → `0.266` / 印刷 `0.266` | PASS |
| Case 20 50Hz SOL (log) | 源 0.266405447 → `0.266` / 印刷 `0.266` | PASS |
| Case 20 50Hz TL (xlsx) | 源 0.6107074 → `0.611` / 印刷 `0.611` | PASS |
| Case 20 50Hz TL (log) | 源 0.6107074 → `0.611` / 印刷 `0.611` | PASS |
| Case 20 75Hz SOL (xlsx) | 源 1.9178623508196322 → `1.918` / 印刷 `1.918` | PASS |
| Case 20 75Hz SOL (log) | 源 1.9178620900000003 → `1.918` / 印刷 `1.918` | PASS |
| Case 20 75Hz TL (xlsx) | 源 1.011998 → `1.012` / 印刷 `1.012` | PASS |
| Case 20 75Hz TL (log) | 源 1.011998 → `1.012` / 印刷 `1.012` | PASS |
| Case 20 100Hz SOL (xlsx) | 源 2.340470429044217 → `2.340` / 印刷 `2.340` | PASS |
| Case 20 100Hz SOL (log) | 源 2.3404708999999997 → `2.340` / 印刷 `2.340` | PASS |
| Case 20 100Hz TL (xlsx) | 源 1.265287 → `1.265` / 印刷 `1.265` | PASS |
| Case 20 100Hz TL (log) | 源 1.265287 → `1.265` / 印刷 `1.265` | PASS |
| Case 20 Avg. SOL (xlsx) | 源 2.1209166909102346 → `2.121` / 印刷 `2.121` | PASS |
| Case 20 Avg. SOL (log) | 源 2.120917 → `2.121` / 印刷 `2.121` | PASS |
| Case 20 Avg. TL (xlsx) | 源 0.899286 → `0.899` / 印刷 `0.899` | PASS |
| Case 20 Avg. TL (log) | 源 0.899286 → `0.899` / 印刷 `0.899` | PASS |
| Case 21 Method 名 | tex `DeepONet` | PASS |
| Case 21 25Hz SOL (xlsx) | 源 23.320367420092218 → `23.320` / 印刷 `23.320` | PASS |
| Case 21 25Hz SOL (log) | 源 23.3203663 → `23.320` / 印刷 `23.320` | PASS |
| Case 21 25Hz TL (xlsx) | 源 1.301132 → `1.301` / 印刷 `1.301` | PASS |
| Case 21 25Hz TL (log) | 源 1.301132 → `1.301` / 印刷 `1.301` | PASS |
| Case 21 50Hz SOL (xlsx) | 源 12.677953671664001 → `12.678` / 印刷 `12.678` | PASS |
| Case 21 50Hz SOL (log) | 源 12.677950500000003 → `12.678` / 印刷 `12.678` | PASS |
| Case 21 50Hz TL (xlsx) | 源 1.381942 → `1.382` / 印刷 `1.382` | PASS |
| Case 21 50Hz TL (log) | 源 1.381942 → `1.382` / 印刷 `1.382` | PASS |
| Case 21 75Hz SOL (xlsx) | 源 45.68477077409625 → `45.685` / 印刷 `45.685` | PASS |
| Case 21 75Hz SOL (log) | 源 45.6847723 → `45.685` / 印刷 `45.685` | PASS |
| Case 21 75Hz TL (xlsx) | 源 2.805426 → `2.805` / 印刷 `2.805` | PASS |
| Case 21 75Hz TL (log) | 源 2.805426 → `2.805` / 印刷 `2.805` | PASS |
| Case 21 100Hz SOL (xlsx) | 源 127.983848657459 → `127.984` / 印刷 `127.984` | PASS |
| Case 21 100Hz SOL (log) | 源 127.983862 → `127.984` / 印刷 `127.984` | PASS |
| Case 21 100Hz TL (xlsx) | 源 5.511891 → `5.512` / 印刷 `5.512` | PASS |
| Case 21 100Hz TL (log) | 源 5.511891 → `5.512` / 印刷 `5.512` | PASS |
| Case 21 Avg. SOL (xlsx) | 源 52.41673775017262 → `52.417` / 印刷 `52.417` | PASS |
| Case 21 Avg. SOL (log) | 源 52.41674 → `52.417` / 印刷 `52.417` | PASS |
| Case 21 Avg. TL (xlsx) | 源 2.750098 → `2.750` / 印刷 `2.750` | PASS |
| Case 21 Avg. TL (log) | 源 2.750098 → `2.750` / 印刷 `2.750` | PASS |
| Case 22 Method 名 | tex `FNO` | PASS |
| Case 22 25Hz SOL (xlsx) | 源 5.422724352683872 → `5.423` / 印刷 `5.423` | PASS |
| Case 22 25Hz SOL (log) | 源 5.42272475 → `5.423` / 印刷 `5.423` | PASS |
| Case 22 25Hz TL (xlsx) | 源 0.8951543 → `0.895` / 印刷 `0.895` | PASS |
| Case 22 25Hz TL (log) | 源 0.8951543 → `0.895` / 印刷 `0.895` | PASS |
| Case 22 50Hz SOL (xlsx) | 源 0.40133751172106713 → `0.401` / 印刷 `0.401` | PASS |
| Case 22 50Hz SOL (log) | 源 0.401337525 → `0.401` / 印刷 `0.401` | PASS |
| Case 22 50Hz TL (xlsx) | 源 0.668 → `0.668` / 印刷 `0.668` | PASS |
| Case 22 50Hz TL (log) | 源 0.668 → `0.668` / 印刷 `0.668` | PASS |
| Case 22 75Hz SOL (xlsx) | 源 2.328076647245325 → `2.328` / 印刷 `2.328` | PASS |
| Case 22 75Hz SOL (log) | 源 2.32807623 → `2.328` / 印刷 `2.328` | PASS |
| Case 22 75Hz TL (xlsx) | 源 1.159577 → `1.160` / 印刷 `1.160` | PASS |
| Case 22 75Hz TL (log) | 源 1.159577 → `1.160` / 印刷 `1.160` | PASS |
| Case 22 100Hz SOL (xlsx) | 源 4.565394896781072 → `4.565` / 印刷 `4.565` | PASS |
| Case 22 100Hz SOL (log) | 源 4.56539505 → `4.565` / 印刷 `4.565` | PASS |
| Case 22 100Hz TL (xlsx) | 源 1.637377 → `1.637` / 印刷 `1.637` | PASS |
| Case 22 100Hz TL (log) | 源 1.637377 → `1.637` / 印刷 `1.637` | PASS |
| Case 22 Avg. SOL (xlsx) | 源 3.179383306996897 → `3.179` / 印刷 `3.179` | PASS |
| Case 22 Avg. SOL (log) | 源 3.179383 → `3.179` / 印刷 `3.179` | PASS |
| Case 22 Avg. TL (xlsx) | 源 1.090027 → `1.090` / 印刷 `1.090` | PASS |
| Case 22 Avg. TL (log) | 源 1.090027 → `1.090` / 印刷 `1.090` | PASS |
| Case 23 Method 名 | tex `KNO` | PASS |
| Case 23 25Hz SOL (xlsx) | 源 46.23470031656326 → `46.235` / 印刷 `46.235` | PASS |
| Case 23 25Hz SOL (log) | 源 46.234703 → `46.235` / 印刷 `46.235` | PASS |
| Case 23 25Hz TL (xlsx) | 源 1.346344 → `1.346` / 印刷 `1.346` | PASS |
| Case 23 25Hz TL (log) | 源 1.346344 → `1.346` / 印刷 `1.346` | PASS |
| Case 23 50Hz SOL (xlsx) | 源 5.179396871244535 → `5.179` / 印刷 `5.179` | PASS |
| Case 23 50Hz SOL (log) | 源 5.17939703 → `5.179` / 印刷 `5.179` | PASS |
| Case 23 50Hz TL (xlsx) | 源 1.216249 → `1.216` / 印刷 `1.216` | PASS |
| Case 23 50Hz TL (log) | 源 1.216249 → `1.216` / 印刷 `1.216` | PASS |
| Case 23 75Hz SOL (xlsx) | 源 24.48505545035005 → `24.485` / 印刷 `24.485` | PASS |
| Case 23 75Hz SOL (log) | 源 24.485059399999997 → `24.485` / 印刷 `24.485` | PASS |
| Case 23 75Hz TL (xlsx) | 源 2.334058 → `2.334` / 印刷 `2.334` | PASS |
| Case 23 75Hz TL (log) | 源 2.334058 → `2.334` / 印刷 `2.334` | PASS |
| Case 23 100Hz SOL (xlsx) | 源 28.634844440966837 → `28.635` / 印刷 `28.635` | PASS |
| Case 23 100Hz SOL (log) | 源 28.634841599999998 → `28.635` / 印刷 `28.635` | PASS |
| Case 23 100Hz TL (xlsx) | 源 3.010926 → `3.011` / 印刷 `3.011` | PASS |
| Case 23 100Hz TL (log) | 源 3.010926 → `3.011` / 印刷 `3.011` | PASS |
| Case 23 Avg. SOL (xlsx) | 源 26.13350008614361 → `26.134` / 印刷 `26.134` | PASS |
| Case 23 Avg. SOL (log) | 源 26.1335 → `26.134` / 印刷 `26.134` | PASS |
| Case 23 Avg. TL (xlsx) | 源 1.976894 → `1.977` / 印刷 `1.977` | PASS |
| Case 23 Avg. TL (log) | 源 1.976894 → `1.977` / 印刷 `1.977` | PASS |
| Case 24 Method 名 | tex `CNO` | PASS |
| Case 24 25Hz SOL (xlsx) | 源 57.71513618528843 → `57.715` / 印刷 `57.715` | PASS |
| Case 24 25Hz SOL (log) | 源 57.715138599999996 → `57.715` / 印刷 `57.715` | PASS |
| Case 24 25Hz TL (xlsx) | 源 1.33072 → `1.331` / 印刷 `1.331` | PASS |
| Case 24 25Hz TL (log) | 源 1.33072 → `1.331` / 印刷 `1.331` | PASS |
| Case 24 50Hz SOL (xlsx) | 源 6.5668119001202285 → `6.567` / 印刷 `6.567` | PASS |
| Case 24 50Hz SOL (log) | 源 6.56681187 → `6.567` / 印刷 `6.567` | PASS |
| Case 24 50Hz TL (xlsx) | 源 1.214305 → `1.214` / 印刷 `1.214` | PASS |
| Case 24 50Hz TL (log) | 源 1.214305 → `1.214` / 印刷 `1.214` | PASS |
| Case 24 75Hz SOL (xlsx) | 源 53.3690960612148 → `53.369` / 印刷 `53.369` | PASS |
| Case 24 75Hz SOL (log) | 源 53.36909910000001 → `53.369` / 印刷 `53.369` | PASS |
| Case 24 75Hz TL (xlsx) | 源 2.831276 → `2.831` / 印刷 `2.831` | PASS |
| Case 24 75Hz TL (log) | 源 2.831276 → `2.831` / 印刷 `2.831` | PASS |
| Case 24 100Hz SOL (xlsx) | 源 70.37499751895666 → `70.375` / 印刷 `70.375` | PASS |
| Case 24 100Hz SOL (log) | 源 70.37499999999999 → `70.375` / 印刷 `70.375` | PASS |
| Case 24 100Hz TL (xlsx) | 源 4.124078 → `4.124` / 印刷 `4.124` | PASS |
| Case 24 100Hz TL (log) | 源 4.124078 → `4.124` / 印刷 `4.124` | PASS |
| Case 24 Avg. SOL (xlsx) | 源 47.00651261955499 → `47.007` / 印刷 `47.007` | PASS |
| Case 24 Avg. SOL (log) | 源 47.00651 → `47.007` / 印刷 `47.007` | PASS |
| Case 24 Avg. TL (xlsx) | 源 2.375095 → `2.375` / 印刷 `2.375` | PASS |
| Case 24 Avg. TL (log) | 源 2.375095 → `2.375` / 印刷 `2.375` | PASS |

## 6. Avg. 列与四频均值自洽

> caption 声明 Avg. 为四频均值；四频样本数相等，故等权均值应等于 Overall 组。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 20 Avg. SOL = 四频均值 | 均值 `2.12092` / Overall `2.12092` | PASS |
| Case 20 Avg. TL = 四频均值 | 均值 `0.899286` / Overall `0.899286` | PASS |
| Case 21 Avg. SOL = 四频均值 | 均值 `52.4167` / Overall `52.4167` | PASS |
| Case 21 Avg. TL = 四频均值 | 均值 `2.7501` / Overall `2.7501` | PASS |
| Case 22 Avg. SOL = 四频均值 | 均值 `3.17938` / Overall `3.17938` | PASS |
| Case 22 Avg. TL = 四频均值 | 均值 `1.09003` / Overall `1.09003` | PASS |
| Case 23 Avg. SOL = 四频均值 | 均值 `26.1335` / Overall `26.1335` | PASS |
| Case 23 Avg. TL = 四频均值 | 均值 `1.97689` / Overall `1.97689` | PASS |
| Case 24 Avg. SOL = 四频均值 | 均值 `47.0065` / Overall `47.0065` | PASS |
| Case 24 Avg. TL = 四频均值 | 均值 `2.37509` / Overall `2.37509` | PASS |

## 7. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 50 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 8. 正文引用精确性（4.4 节）

> 每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。只查①会漏掉正文与表格一起错的情形。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 Case 20 Proposed 频均 Sol | 正文 `2.121` / 表格 `2.121` | PASS |
| 正文 Case 20 Proposed 频均 Sol <- xlsx 源 | 源 2.1209166909102346 → `2.121` / 印刷 `2.121` | PASS |
| 正文 Case 20 Proposed 频均 TL | 正文 `0.899` / 表格 `0.899` | PASS |
| 正文 Case 20 Proposed 频均 TL <- xlsx 源 | 源 0.899286 → `0.899` / 印刷 `0.899` | PASS |
| 正文 Case 22 FNO 频均 Sol | 正文 `3.179` / 表格 `3.179` | PASS |
| 正文 Case 22 FNO 频均 Sol <- xlsx 源 | 源 3.179383306996897 → `3.179` / 印刷 `3.179` | PASS |
| 正文 Case 22 FNO 频均 TL | 正文 `1.090` / 表格 `1.090` | PASS |
| 正文 Case 22 FNO 频均 TL <- xlsx 源 | 源 1.090027 → `1.090` / 印刷 `1.090` | PASS |
| 正文 Case 20 @100Hz TL | 正文 `1.265` / 表格 `1.265` | PASS |
| 正文 Case 20 @100Hz TL <- xlsx 源 | 源 1.265287 → `1.265` / 印刷 `1.265` | PASS |
| 正文 Case 21 DeepONet @100Hz TL | 正文 `5.512` / 表格 `5.512` | PASS |
| 正文 Case 21 DeepONet @100Hz TL <- xlsx 源 | 源 5.511891 → `5.512` / 印刷 `5.512` | PASS |

## X. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

