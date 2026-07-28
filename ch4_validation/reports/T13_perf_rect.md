# Table 13 — 五方法逐频精度 R1

- 对象：`tab:perf-rect`（Table 13）
- 结论：**PASS** — 194 通过 / 0 失败 / 0 警告，共 194 项
- 脚本：`ch4_validation/scripts/T13_perf_rect.py`
- 生成：2026-07-29 01:06:58

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:perf-rect}` 所在 table* 环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/Case15-24_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 15) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No15_R1_Proposed/training_run/logs/full_run_20260710_221657.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 16) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No16_R1_DeepONet/training_run/logs/full_run_20260711_003124.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 17) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No17_R1_FNO/training_run/logs/full_run_20260711_004949.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 18) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No18_R1_KNO/training_run/logs/full_run_20260711_013721.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 19) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No19_R1_CNO/training_run/logs/full_run_20260711_022215.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/Case15-24_数据汇总.xlsx | PASS |
| Case 15 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No15_R1_Proposed/training_run/logs/full_run_20260710_221657.log | PASS |
| Case 16 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No16_R1_DeepONet/training_run/logs/full_run_20260711_003124.log | PASS |
| Case 17 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No17_R1_FNO/training_run/logs/full_run_20260711_004949.log | PASS |
| Case 18 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No18_R1_KNO/training_run/logs/full_run_20260711_013721.log | PASS |
| Case 19 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No19_R1_CNO/training_run/logs/full_run_20260711_022215.log | PASS |
| tex 表格环境可定位且确实包住 label | `tab:perf-rect`，长度 1554 | PASS |
| tex 数据行数 = 5 | 实得 5 | PASS |
| tex 行 No. 覆盖 15-19 | [15, 16, 17, 18, 19] | PASS |

## 3. best epoch 一致性

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 15 best epoch | xlsx `198` / log `198` | PASS |
| Case 15 日志含『评估 Epoch 198』块 | 轮次 198 | PASS |
| Case 16 best epoch | xlsx `199` / log `199` | PASS |
| Case 16 日志含『评估 Epoch 199』块 | 轮次 199 | PASS |
| Case 17 best epoch | xlsx `200` / log `200` | PASS |
| Case 17 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |
| Case 18 best epoch | xlsx `200` / log `200` | PASS |
| Case 18 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |
| Case 19 best epoch | xlsx `200` / log `200` | PASS |
| Case 19 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |

## 4. 双渠道交叉验证（xlsx vs log，同一 best epoch）

> 日志侧取『评估 Epoch N 完成』块（测试集），非『训练』块；Sol 由 `(损失 − w_prior×prior)/w_rel` 现场算，权重逐轮解析。

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 15 Overall SOL | `1.6882909461855888` / `1.6882910000000002` | PASS |
| Case 15 Overall TL | `0.9511941` / `0.9511941` | PASS |
| Case 15 25 SOL | `2.475624985527247` / `2.4756253` | PASS |
| Case 15 25 TL | `0.7047694` / `0.7047694` | PASS |
| Case 15 50 SOL | `0.266019553237129` / `0.26601958000000003` | PASS |
| Case 15 50 TL | `0.516494` / `0.516494` | PASS |
| Case 15 75 SOL | `2.156675141304732` / `2.15667489` | PASS |
| Case 15 75 TL | `1.093897` / `1.093897` | PASS |
| Case 15 100 SOL | `1.854844175977632` / `1.85484438` | PASS |
| Case 15 100 TL | `1.489616` / `1.489616` | PASS |
| Case 16 Overall SOL | `46.28393617458641` / `46.28394` | PASS |
| Case 16 Overall TL | `3.483583` / `3.483583` | PASS |
| Case 16 25 SOL | `32.02167481649667` / `32.021673299999996` | PASS |
| Case 16 25 TL | `1.507518` / `1.507518` | PASS |
| Case 16 50 SOL | `18.3700246270746` / `18.3700197` | PASS |
| Case 16 50 TL | `1.869137` / `1.869137` | PASS |
| Case 16 75 SOL | `53.54775651358068` / `53.5477524` | PASS |
| Case 16 75 TL | `3.490569` / `3.490569` | PASS |
| Case 16 100 SOL | `81.19629761204123` / `81.1962971` | PASS |
| Case 16 100 TL | `7.067107` / `7.067107` | PASS |
| Case 17 Overall SOL | `3.729538974585012` / `3.729539` | PASS |
| Case 17 Overall TL | `1.305029` / `1.305029` | PASS |
| Case 17 25 SOL | `4.016159859020265` / `4.0161594` | PASS |
| Case 17 25 TL | `0.8294734` / `0.8294734` | PASS |
| Case 17 50 SOL | `0.4407965883729048` / `0.44079663399999996` | PASS |
| Case 17 50 TL | `0.6063695` / `0.6063695` | PASS |
| Case 17 75 SOL | `4.748221815680154` / `4.748221780000001` | PASS |
| Case 17 75 TL | `1.528673` / `1.528673` | PASS |
| Case 17 100 SOL | `5.712977214716375` / `5.712977230000001` | PASS |
| Case 17 100 TL | `2.255599` / `2.255599` | PASS |
| Case 18 Overall SOL | `28.46832028590143` / `28.468329999999998` | PASS |
| Case 18 Overall TL | `2.738437` / `2.738437` | PASS |
| Case 18 25 SOL | `37.509433086961515` / `37.5094356` | PASS |
| Case 18 25 TL | `1.758901` / `1.758901` | PASS |
| Case 18 50 SOL | `12.21692649414763` / `12.2169307` | PASS |
| Case 18 50 TL | `1.911753` / `1.911753` | PASS |
| Case 18 75 SOL | `29.49299784377217` / `29.493000000000002` | PASS |
| Case 18 75 TL | `3.001591` / `3.001591` | PASS |
| Case 18 100 SOL | `34.6539280610159` / `34.6539308` | PASS |
| Case 18 100 TL | `4.281503` / `4.281503` | PASS |
| Case 19 Overall SOL | `27.011267002671957` / `27.01127` | PASS |
| Case 19 Overall TL | `2.634112` / `2.634112` | PASS |
| Case 19 25 SOL | `35.926640615798526` / `35.926643600000006` | PASS |
| Case 19 25 TL | `1.832511` / `1.832511` | PASS |
| Case 19 50 SOL | `4.9055928422603765` / `4.90559308` | PASS |
| Case 19 50 TL | `1.345858` / `1.345858` | PASS |
| Case 19 75 SOL | `34.554940043017275` / `34.554940599999995` | PASS |
| Case 19 75 TL | `2.869022` / `2.869022` | PASS |
| Case 19 100 SOL | `32.65789831057191` / `32.657901` | PASS |
| Case 19 100 TL | `4.489058` / `4.489058` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Method, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。Avg. 对应 xlsx/日志的 Overall 组。本表无 Fig. 列。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 15 Method 名 | tex `Proposed` | PASS |
| Case 15 25Hz SOL (xlsx) | 源 2.475624985527247 → `2.476` / 印刷 `2.476` | PASS |
| Case 15 25Hz SOL (log) | 源 2.4756253 → `2.476` / 印刷 `2.476` | PASS |
| Case 15 25Hz TL (xlsx) | 源 0.7047694 → `0.705` / 印刷 `0.705` | PASS |
| Case 15 25Hz TL (log) | 源 0.7047694 → `0.705` / 印刷 `0.705` | PASS |
| Case 15 50Hz SOL (xlsx) | 源 0.266019553237129 → `0.266` / 印刷 `0.266` | PASS |
| Case 15 50Hz SOL (log) | 源 0.26601958000000003 → `0.266` / 印刷 `0.266` | PASS |
| Case 15 50Hz TL (xlsx) | 源 0.516494 → `0.516` / 印刷 `0.516` | PASS |
| Case 15 50Hz TL (log) | 源 0.516494 → `0.516` / 印刷 `0.516` | PASS |
| Case 15 75Hz SOL (xlsx) | 源 2.156675141304732 → `2.157` / 印刷 `2.157` | PASS |
| Case 15 75Hz SOL (log) | 源 2.15667489 → `2.157` / 印刷 `2.157` | PASS |
| Case 15 75Hz TL (xlsx) | 源 1.093897 → `1.094` / 印刷 `1.094` | PASS |
| Case 15 75Hz TL (log) | 源 1.093897 → `1.094` / 印刷 `1.094` | PASS |
| Case 15 100Hz SOL (xlsx) | 源 1.854844175977632 → `1.855` / 印刷 `1.855` | PASS |
| Case 15 100Hz SOL (log) | 源 1.85484438 → `1.855` / 印刷 `1.855` | PASS |
| Case 15 100Hz TL (xlsx) | 源 1.489616 → `1.490` / 印刷 `1.490` | PASS |
| Case 15 100Hz TL (log) | 源 1.489616 → `1.490` / 印刷 `1.490` | PASS |
| Case 15 Avg. SOL (xlsx) | 源 1.6882909461855888 → `1.688` / 印刷 `1.688` | PASS |
| Case 15 Avg. SOL (log) | 源 1.6882910000000002 → `1.688` / 印刷 `1.688` | PASS |
| Case 15 Avg. TL (xlsx) | 源 0.9511941 → `0.951` / 印刷 `0.951` | PASS |
| Case 15 Avg. TL (log) | 源 0.9511941 → `0.951` / 印刷 `0.951` | PASS |
| Case 16 Method 名 | tex `DeepONet` | PASS |
| Case 16 25Hz SOL (xlsx) | 源 32.02167481649667 → `32.022` / 印刷 `32.022` | PASS |
| Case 16 25Hz SOL (log) | 源 32.021673299999996 → `32.022` / 印刷 `32.022` | PASS |
| Case 16 25Hz TL (xlsx) | 源 1.507518 → `1.508` / 印刷 `1.508` | PASS |
| Case 16 25Hz TL (log) | 源 1.507518 → `1.508` / 印刷 `1.508` | PASS |
| Case 16 50Hz SOL (xlsx) | 源 18.3700246270746 → `18.370` / 印刷 `18.370` | PASS |
| Case 16 50Hz SOL (log) | 源 18.3700197 → `18.370` / 印刷 `18.370` | PASS |
| Case 16 50Hz TL (xlsx) | 源 1.869137 → `1.869` / 印刷 `1.869` | PASS |
| Case 16 50Hz TL (log) | 源 1.869137 → `1.869` / 印刷 `1.869` | PASS |
| Case 16 75Hz SOL (xlsx) | 源 53.54775651358068 → `53.548` / 印刷 `53.548` | PASS |
| Case 16 75Hz SOL (log) | 源 53.5477524 → `53.548` / 印刷 `53.548` | PASS |
| Case 16 75Hz TL (xlsx) | 源 3.490569 → `3.491` / 印刷 `3.491` | PASS |
| Case 16 75Hz TL (log) | 源 3.490569 → `3.491` / 印刷 `3.491` | PASS |
| Case 16 100Hz SOL (xlsx) | 源 81.19629761204123 → `81.196` / 印刷 `81.196` | PASS |
| Case 16 100Hz SOL (log) | 源 81.1962971 → `81.196` / 印刷 `81.196` | PASS |
| Case 16 100Hz TL (xlsx) | 源 7.067107 → `7.067` / 印刷 `7.067` | PASS |
| Case 16 100Hz TL (log) | 源 7.067107 → `7.067` / 印刷 `7.067` | PASS |
| Case 16 Avg. SOL (xlsx) | 源 46.28393617458641 → `46.284` / 印刷 `46.284` | PASS |
| Case 16 Avg. SOL (log) | 源 46.28394 → `46.284` / 印刷 `46.284` | PASS |
| Case 16 Avg. TL (xlsx) | 源 3.483583 → `3.484` / 印刷 `3.484` | PASS |
| Case 16 Avg. TL (log) | 源 3.483583 → `3.484` / 印刷 `3.484` | PASS |
| Case 17 Method 名 | tex `FNO` | PASS |
| Case 17 25Hz SOL (xlsx) | 源 4.016159859020265 → `4.016` / 印刷 `4.016` | PASS |
| Case 17 25Hz SOL (log) | 源 4.0161594 → `4.016` / 印刷 `4.016` | PASS |
| Case 17 25Hz TL (xlsx) | 源 0.8294734 → `0.829` / 印刷 `0.829` | PASS |
| Case 17 25Hz TL (log) | 源 0.8294734 → `0.829` / 印刷 `0.829` | PASS |
| Case 17 50Hz SOL (xlsx) | 源 0.4407965883729048 → `0.441` / 印刷 `0.441` | PASS |
| Case 17 50Hz SOL (log) | 源 0.44079663399999996 → `0.441` / 印刷 `0.441` | PASS |
| Case 17 50Hz TL (xlsx) | 源 0.6063695 → `0.606` / 印刷 `0.606` | PASS |
| Case 17 50Hz TL (log) | 源 0.6063695 → `0.606` / 印刷 `0.606` | PASS |
| Case 17 75Hz SOL (xlsx) | 源 4.748221815680154 → `4.748` / 印刷 `4.748` | PASS |
| Case 17 75Hz SOL (log) | 源 4.748221780000001 → `4.748` / 印刷 `4.748` | PASS |
| Case 17 75Hz TL (xlsx) | 源 1.528673 → `1.529` / 印刷 `1.529` | PASS |
| Case 17 75Hz TL (log) | 源 1.528673 → `1.529` / 印刷 `1.529` | PASS |
| Case 17 100Hz SOL (xlsx) | 源 5.712977214716375 → `5.713` / 印刷 `5.713` | PASS |
| Case 17 100Hz SOL (log) | 源 5.712977230000001 → `5.713` / 印刷 `5.713` | PASS |
| Case 17 100Hz TL (xlsx) | 源 2.255599 → `2.256` / 印刷 `2.256` | PASS |
| Case 17 100Hz TL (log) | 源 2.255599 → `2.256` / 印刷 `2.256` | PASS |
| Case 17 Avg. SOL (xlsx) | 源 3.729538974585012 → `3.730` / 印刷 `3.730` | PASS |
| Case 17 Avg. SOL (log) | 源 3.729539 → `3.730` / 印刷 `3.730` | PASS |
| Case 17 Avg. TL (xlsx) | 源 1.305029 → `1.305` / 印刷 `1.305` | PASS |
| Case 17 Avg. TL (log) | 源 1.305029 → `1.305` / 印刷 `1.305` | PASS |
| Case 18 Method 名 | tex `KNO` | PASS |
| Case 18 25Hz SOL (xlsx) | 源 37.509433086961515 → `37.509` / 印刷 `37.509` | PASS |
| Case 18 25Hz SOL (log) | 源 37.5094356 → `37.509` / 印刷 `37.509` | PASS |
| Case 18 25Hz TL (xlsx) | 源 1.758901 → `1.759` / 印刷 `1.759` | PASS |
| Case 18 25Hz TL (log) | 源 1.758901 → `1.759` / 印刷 `1.759` | PASS |
| Case 18 50Hz SOL (xlsx) | 源 12.21692649414763 → `12.217` / 印刷 `12.217` | PASS |
| Case 18 50Hz SOL (log) | 源 12.2169307 → `12.217` / 印刷 `12.217` | PASS |
| Case 18 50Hz TL (xlsx) | 源 1.911753 → `1.912` / 印刷 `1.912` | PASS |
| Case 18 50Hz TL (log) | 源 1.911753 → `1.912` / 印刷 `1.912` | PASS |
| Case 18 75Hz SOL (xlsx) | 源 29.49299784377217 → `29.493` / 印刷 `29.493` | PASS |
| Case 18 75Hz SOL (log) | 源 29.493000000000002 → `29.493` / 印刷 `29.493` | PASS |
| Case 18 75Hz TL (xlsx) | 源 3.001591 → `3.002` / 印刷 `3.002` | PASS |
| Case 18 75Hz TL (log) | 源 3.001591 → `3.002` / 印刷 `3.002` | PASS |
| Case 18 100Hz SOL (xlsx) | 源 34.6539280610159 → `34.654` / 印刷 `34.654` | PASS |
| Case 18 100Hz SOL (log) | 源 34.6539308 → `34.654` / 印刷 `34.654` | PASS |
| Case 18 100Hz TL (xlsx) | 源 4.281503 → `4.282` / 印刷 `4.282` | PASS |
| Case 18 100Hz TL (log) | 源 4.281503 → `4.282` / 印刷 `4.282` | PASS |
| Case 18 Avg. SOL (xlsx) | 源 28.46832028590143 → `28.468` / 印刷 `28.468` | PASS |
| Case 18 Avg. SOL (log) | 源 28.468329999999998 → `28.468` / 印刷 `28.468` | PASS |
| Case 18 Avg. TL (xlsx) | 源 2.738437 → `2.738` / 印刷 `2.738` | PASS |
| Case 18 Avg. TL (log) | 源 2.738437 → `2.738` / 印刷 `2.738` | PASS |
| Case 19 Method 名 | tex `CNO` | PASS |
| Case 19 25Hz SOL (xlsx) | 源 35.926640615798526 → `35.927` / 印刷 `35.927` | PASS |
| Case 19 25Hz SOL (log) | 源 35.926643600000006 → `35.927` / 印刷 `35.927` | PASS |
| Case 19 25Hz TL (xlsx) | 源 1.832511 → `1.833` / 印刷 `1.833` | PASS |
| Case 19 25Hz TL (log) | 源 1.832511 → `1.833` / 印刷 `1.833` | PASS |
| Case 19 50Hz SOL (xlsx) | 源 4.9055928422603765 → `4.906` / 印刷 `4.906` | PASS |
| Case 19 50Hz SOL (log) | 源 4.90559308 → `4.906` / 印刷 `4.906` | PASS |
| Case 19 50Hz TL (xlsx) | 源 1.345858 → `1.346` / 印刷 `1.346` | PASS |
| Case 19 50Hz TL (log) | 源 1.345858 → `1.346` / 印刷 `1.346` | PASS |
| Case 19 75Hz SOL (xlsx) | 源 34.554940043017275 → `34.555` / 印刷 `34.555` | PASS |
| Case 19 75Hz SOL (log) | 源 34.554940599999995 → `34.555` / 印刷 `34.555` | PASS |
| Case 19 75Hz TL (xlsx) | 源 2.869022 → `2.869` / 印刷 `2.869` | PASS |
| Case 19 75Hz TL (log) | 源 2.869022 → `2.869` / 印刷 `2.869` | PASS |
| Case 19 100Hz SOL (xlsx) | 源 32.65789831057191 → `32.658` / 印刷 `32.658` | PASS |
| Case 19 100Hz SOL (log) | 源 32.657901 → `32.658` / 印刷 `32.658` | PASS |
| Case 19 100Hz TL (xlsx) | 源 4.489058 → `4.489` / 印刷 `4.489` | PASS |
| Case 19 100Hz TL (log) | 源 4.489058 → `4.489` / 印刷 `4.489` | PASS |
| Case 19 Avg. SOL (xlsx) | 源 27.011267002671957 → `27.011` / 印刷 `27.011` | PASS |
| Case 19 Avg. SOL (log) | 源 27.01127 → `27.011` / 印刷 `27.011` | PASS |
| Case 19 Avg. TL (xlsx) | 源 2.634112 → `2.634` / 印刷 `2.634` | PASS |
| Case 19 Avg. TL (log) | 源 2.634112 → `2.634` / 印刷 `2.634` | PASS |

## 6. Avg. 列与四频均值自洽

> caption 声明 Avg. 为四频均值；四频样本数相等，故等权均值应等于 Overall 组。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 15 Avg. SOL = 四频均值 | 均值 `1.68829` / Overall `1.68829` | PASS |
| Case 15 Avg. TL = 四频均值 | 均值 `0.951194` / Overall `0.951194` | PASS |
| Case 16 Avg. SOL = 四频均值 | 均值 `46.2839` / Overall `46.2839` | PASS |
| Case 16 Avg. TL = 四频均值 | 均值 `3.48358` / Overall `3.48358` | PASS |
| Case 17 Avg. SOL = 四频均值 | 均值 `3.72954` / Overall `3.72954` | PASS |
| Case 17 Avg. TL = 四频均值 | 均值 `1.30503` / Overall `1.30503` | PASS |
| Case 18 Avg. SOL = 四频均值 | 均值 `28.4683` / Overall `28.4683` | PASS |
| Case 18 Avg. TL = 四频均值 | 均值 `2.73844` / Overall `2.73844` | PASS |
| Case 19 Avg. SOL = 四频均值 | 均值 `27.0113` / Overall `27.0113` | PASS |
| Case 19 Avg. TL = 四频均值 | 均值 `2.63411` / Overall `2.63411` | PASS |

## 7. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 50 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 8. 正文引用精确性（4.4 节）

> 每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。只查①会漏掉正文与表格一起错的情形。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 Case 15 Proposed 频均 Sol | 正文 `1.688` / 表格 `1.688` | PASS |
| 正文 Case 15 Proposed 频均 Sol <- xlsx 源 | 源 1.6882909461855888 → `1.688` / 印刷 `1.688` | PASS |
| 正文 Case 15 Proposed 频均 TL | 正文 `0.951` / 表格 `0.951` | PASS |
| 正文 Case 15 Proposed 频均 TL <- xlsx 源 | 源 0.9511941 → `0.951` / 印刷 `0.951` | PASS |
| 正文 Case 17 FNO 频均 Sol | 正文 `3.730` / 表格 `3.730` | PASS |
| 正文 Case 17 FNO 频均 Sol <- xlsx 源 | 源 3.729538974585012 → `3.730` / 印刷 `3.730` | PASS |
| 正文 Case 17 FNO 频均 TL | 正文 `1.305` / 表格 `1.305` | PASS |
| 正文 Case 17 FNO 频均 TL <- xlsx 源 | 源 1.305029 → `1.305` / 印刷 `1.305` | PASS |

## X. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

