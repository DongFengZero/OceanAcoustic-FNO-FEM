# Table 10 — 五方法逐频精度，矩形与楔形分块同表

- 对象：`tab:perf-cmp`（Table 10）
- 结论：**PASS** — 408 通过 / 0 失败 / 0 警告，共 408 项
- 脚本：`ch4_validation/scripts/T10_perf_cmp.py`
- 生成：2026-10-05 10:16:32

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{tab:perf-cmp}` 所在环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/Case15-24_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 15) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No15_R1_Proposed/training_run/logs/full_run_20260710_221657.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 16) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No16_R1_DeepONet/training_run/logs/full_run_20260711_003124.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 17) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No17_R1_FNO/training_run/logs/full_run_20260711_004949.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 18) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No18_R1_KNO/training_run/logs/full_run_20260711_013721.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 19) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No19_R1_CNO/training_run/logs/full_run_20260711_022215.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 20) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No20_W1_Proposed/training_run/logs/full_run_20260710_152228.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 21) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No21_W1_DeepONet/training_run/logs/full_run_20260710_162410.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 22) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No22_W1_FNO/training_run/logs/full_run_20260710_172139.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 23) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No23_W1_KNO/training_run/logs/full_run_20260710_202430.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 24) | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No24_W1_CNO/training_run/logs/full_run_20260710_184721.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/Case15-24_数据汇总.xlsx | PASS |
| Case 15 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No15_R1_Proposed/training_run/logs/full_run_20260710_221657.log | PASS |
| Case 16 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No16_R1_DeepONet/training_run/logs/full_run_20260711_003124.log | PASS |
| Case 17 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No17_R1_FNO/training_run/logs/full_run_20260711_004949.log | PASS |
| Case 18 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No18_R1_KNO/training_run/logs/full_run_20260711_013721.log | PASS |
| Case 19 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No19_R1_CNO/training_run/logs/full_run_20260711_022215.log | PASS |
| Case 20 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No20_W1_Proposed/training_run/logs/full_run_20260710_152228.log | PASS |
| Case 21 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No21_W1_DeepONet/training_run/logs/full_run_20260710_162410.log | PASS |
| Case 22 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No22_W1_FNO/training_run/logs/full_run_20260710_172139.log | PASS |
| Case 23 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No23_W1_KNO/training_run/logs/full_run_20260710_202430.log | PASS |
| Case 24 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No24_W1_CNO/training_run/logs/full_run_20260710_184721.log | PASS |
| tex 表格环境可定位且确实包住 label | 长度 2372 | PASS |

## 1. 本表 tabular 的定位

> R1 把多张表绑进同一个 figure* 浮动体，`table_env()` 可能解析到邻居的 tabular；本表一律用 `table_body_of()` 取 label 自己的表体。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| label 之后可定位到本表 tabular | tabular*=True，长度 1804 | PASS |
| 数据行数 = 10（两几何各 5 行） | 实得 10 | PASS |
| 加粗掩码与数据行同形 | 10 / 10 | PASS |
| 两个 \multicolumn{12} 块头行（矩形 / 楔形） | 实得 2 | PASS |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 行 No. 覆盖 15-19 与 20-24 | [15, 16, 17, 18, 19, 20, 21, 22, 23, 24] | PASS |
| Case 15 落在矩形块且 Method 名相符 | tex `Proposed` / 期望 `Proposed` | PASS |
| Case 16 落在矩形块且 Method 名相符 | tex `DeepONet` / 期望 `DeepONet` | PASS |
| Case 17 落在矩形块且 Method 名相符 | tex `FNO` / 期望 `FNO` | PASS |
| Case 18 落在矩形块且 Method 名相符 | tex `KNO` / 期望 `KNO` | PASS |
| Case 19 落在矩形块且 Method 名相符 | tex `CNO` / 期望 `CNO` | PASS |
| Case 20 落在楔形块且 Method 名相符 | tex `Proposed` / 期望 `Proposed` | PASS |
| Case 21 落在楔形块且 Method 名相符 | tex `DeepONet` / 期望 `DeepONet` | PASS |
| Case 22 落在楔形块且 Method 名相符 | tex `FNO` / 期望 `FNO` | PASS |
| Case 23 落在楔形块且 Method 名相符 | tex `KNO` / 期望 `KNO` | PASS |
| Case 24 落在楔形块且 Method 名相符 | tex `CNO` / 期望 `CNO` | PASS |
| 行序为矩形块 15-19 后接楔形块 20-24 | [15, 16, 17, 18, 19, 20, 21, 22, 23, 24] | PASS |

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

## 4. 双渠道交叉验证（xlsx vs log）

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 15 25Hz SOL | `2.475624985527247` / `2.4756253` | PASS |
| Case 15 25Hz TL | `0.7047694` / `0.7047694` | PASS |
| Case 15 50Hz SOL | `0.266019553237129` / `0.26601958000000003` | PASS |
| Case 15 50Hz TL | `0.516494` / `0.516494` | PASS |
| Case 15 75Hz SOL | `2.156675141304732` / `2.15667489` | PASS |
| Case 15 75Hz TL | `1.093897` / `1.093897` | PASS |
| Case 15 100Hz SOL | `1.854844175977632` / `1.85484438` | PASS |
| Case 15 100Hz TL | `1.489616` / `1.489616` | PASS |
| Case 15 Avg. SOL | `1.6882909461855888` / `1.6882910000000002` | PASS |
| Case 15 Avg. TL | `0.9511941` / `0.9511941` | PASS |
| Case 16 25Hz SOL | `32.02167481649667` / `32.021673299999996` | PASS |
| Case 16 25Hz TL | `1.507518` / `1.507518` | PASS |
| Case 16 50Hz SOL | `18.3700246270746` / `18.3700197` | PASS |
| Case 16 50Hz TL | `1.869137` / `1.869137` | PASS |
| Case 16 75Hz SOL | `53.54775651358068` / `53.5477524` | PASS |
| Case 16 75Hz TL | `3.490569` / `3.490569` | PASS |
| Case 16 100Hz SOL | `81.19629761204123` / `81.1962971` | PASS |
| Case 16 100Hz TL | `7.067107` / `7.067107` | PASS |
| Case 16 Avg. SOL | `46.28393617458641` / `46.28394` | PASS |
| Case 16 Avg. TL | `3.483583` / `3.483583` | PASS |
| Case 17 25Hz SOL | `4.016159859020265` / `4.0161594` | PASS |
| Case 17 25Hz TL | `0.8294734` / `0.8294734` | PASS |
| Case 17 50Hz SOL | `0.4407965883729048` / `0.44079663399999996` | PASS |
| Case 17 50Hz TL | `0.6063695` / `0.6063695` | PASS |
| Case 17 75Hz SOL | `4.748221815680154` / `4.748221780000001` | PASS |
| Case 17 75Hz TL | `1.528673` / `1.528673` | PASS |
| Case 17 100Hz SOL | `5.712977214716375` / `5.712977230000001` | PASS |
| Case 17 100Hz TL | `2.255599` / `2.255599` | PASS |
| Case 17 Avg. SOL | `3.729538974585012` / `3.729539` | PASS |
| Case 17 Avg. TL | `1.305029` / `1.305029` | PASS |
| Case 18 25Hz SOL | `37.509433086961515` / `37.5094356` | PASS |
| Case 18 25Hz TL | `1.758901` / `1.758901` | PASS |
| Case 18 50Hz SOL | `12.21692649414763` / `12.2169307` | PASS |
| Case 18 50Hz TL | `1.911753` / `1.911753` | PASS |
| Case 18 75Hz SOL | `29.49299784377217` / `29.493000000000002` | PASS |
| Case 18 75Hz TL | `3.001591` / `3.001591` | PASS |
| Case 18 100Hz SOL | `34.6539280610159` / `34.6539308` | PASS |
| Case 18 100Hz TL | `4.281503` / `4.281503` | PASS |
| Case 18 Avg. SOL | `28.46832028590143` / `28.468329999999998` | PASS |
| Case 18 Avg. TL | `2.738437` / `2.738437` | PASS |
| Case 19 25Hz SOL | `35.926640615798526` / `35.926643600000006` | PASS |
| Case 19 25Hz TL | `1.832511` / `1.832511` | PASS |
| Case 19 50Hz SOL | `4.9055928422603765` / `4.90559308` | PASS |
| Case 19 50Hz TL | `1.345858` / `1.345858` | PASS |
| Case 19 75Hz SOL | `34.554940043017275` / `34.554940599999995` | PASS |
| Case 19 75Hz TL | `2.869022` / `2.869022` | PASS |
| Case 19 100Hz SOL | `32.65789831057191` / `32.657901` | PASS |
| Case 19 100Hz TL | `4.489058` / `4.489058` | PASS |
| Case 19 Avg. SOL | `27.011267002671957` / `27.01127` | PASS |
| Case 19 Avg. TL | `2.634112` / `2.634112` | PASS |
| Case 20 25Hz SOL | `3.958929784130305` / `3.9589297199999995` | PASS |
| Case 20 25Hz TL | `0.7091513` / `0.7091513` | PASS |
| Case 20 50Hz SOL | `0.26640543073881423` / `0.266405447` | PASS |
| Case 20 50Hz TL | `0.6107074` / `0.6107074` | PASS |
| Case 20 75Hz SOL | `1.9178623508196322` / `1.9178620900000003` | PASS |
| Case 20 75Hz TL | `1.011998` / `1.011998` | PASS |
| Case 20 100Hz SOL | `2.340470429044217` / `2.3404708999999997` | PASS |
| Case 20 100Hz TL | `1.265287` / `1.265287` | PASS |
| Case 20 Avg. SOL | `2.1209166909102346` / `2.120917` | PASS |
| Case 20 Avg. TL | `0.899286` / `0.899286` | PASS |
| Case 21 25Hz SOL | `23.320367420092218` / `23.3203663` | PASS |
| Case 21 25Hz TL | `1.301132` / `1.301132` | PASS |
| Case 21 50Hz SOL | `12.677953671664001` / `12.677950500000003` | PASS |
| Case 21 50Hz TL | `1.381942` / `1.381942` | PASS |
| Case 21 75Hz SOL | `45.68477077409625` / `45.6847723` | PASS |
| Case 21 75Hz TL | `2.805426` / `2.805426` | PASS |
| Case 21 100Hz SOL | `127.983848657459` / `127.983862` | PASS |
| Case 21 100Hz TL | `5.511891` / `5.511891` | PASS |
| Case 21 Avg. SOL | `52.41673775017262` / `52.41674` | PASS |
| Case 21 Avg. TL | `2.750098` / `2.750098` | PASS |
| Case 22 25Hz SOL | `5.422724352683872` / `5.42272475` | PASS |
| Case 22 25Hz TL | `0.8951543` / `0.8951543` | PASS |
| Case 22 50Hz SOL | `0.40133751172106713` / `0.401337525` | PASS |
| Case 22 50Hz TL | `0.668` / `0.668` | PASS |
| Case 22 75Hz SOL | `2.328076647245325` / `2.32807623` | PASS |
| Case 22 75Hz TL | `1.159577` / `1.159577` | PASS |
| Case 22 100Hz SOL | `4.565394896781072` / `4.56539505` | PASS |
| Case 22 100Hz TL | `1.637377` / `1.637377` | PASS |
| Case 22 Avg. SOL | `3.179383306996897` / `3.179383` | PASS |
| Case 22 Avg. TL | `1.090027` / `1.090027` | PASS |
| Case 23 25Hz SOL | `46.23470031656326` / `46.234703` | PASS |
| Case 23 25Hz TL | `1.346344` / `1.346344` | PASS |
| Case 23 50Hz SOL | `5.179396871244535` / `5.17939703` | PASS |
| Case 23 50Hz TL | `1.216249` / `1.216249` | PASS |
| Case 23 75Hz SOL | `24.48505545035005` / `24.485059399999997` | PASS |
| Case 23 75Hz TL | `2.334058` / `2.334058` | PASS |
| Case 23 100Hz SOL | `28.634844440966837` / `28.634841599999998` | PASS |
| Case 23 100Hz TL | `3.010926` / `3.010926` | PASS |
| Case 23 Avg. SOL | `26.13350008614361` / `26.1335` | PASS |
| Case 23 Avg. TL | `1.976894` / `1.976894` | PASS |
| Case 24 25Hz SOL | `57.71513618528843` / `57.715138599999996` | PASS |
| Case 24 25Hz TL | `1.33072` / `1.33072` | PASS |
| Case 24 50Hz SOL | `6.5668119001202285` / `6.56681187` | PASS |
| Case 24 50Hz TL | `1.214305` / `1.214305` | PASS |
| Case 24 75Hz SOL | `53.3690960612148` / `53.36909910000001` | PASS |
| Case 24 75Hz TL | `2.831276` / `2.831276` | PASS |
| Case 24 100Hz SOL | `70.37499751895666` / `70.37499999999999` | PASS |
| Case 24 100Hz TL | `4.124078` / `4.124078` | PASS |
| Case 24 Avg. SOL | `47.00651261955499` / `47.00651` | PASS |
| Case 24 Avg. TL | `2.375095` / `2.375095` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Method, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)；Avg. 对应 xlsx/日志的 Overall 组。两几何共用一张表，故行内只有一组数值。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
|  25Hz SOL (xlsx) | 源 2.475624985527247 → `2.476` / 印刷 `2.476` | PASS |
|  25Hz SOL (log) | 源 2.4756253 → `2.476` / 印刷 `2.476` | PASS |
|  25Hz TL (xlsx) | 源 0.7047694 → `0.705` / 印刷 `0.705` | PASS |
|  25Hz TL (log) | 源 0.7047694 → `0.705` / 印刷 `0.705` | PASS |
|  50Hz SOL (xlsx) | 源 0.266019553237129 → `0.266` / 印刷 `0.266` | PASS |
|  50Hz SOL (log) | 源 0.26601958000000003 → `0.266` / 印刷 `0.266` | PASS |
|  50Hz TL (xlsx) | 源 0.516494 → `0.516` / 印刷 `0.516` | PASS |
|  50Hz TL (log) | 源 0.516494 → `0.516` / 印刷 `0.516` | PASS |
|  75Hz SOL (xlsx) | 源 2.156675141304732 → `2.157` / 印刷 `2.157` | PASS |
|  75Hz SOL (log) | 源 2.15667489 → `2.157` / 印刷 `2.157` | PASS |
|  75Hz TL (xlsx) | 源 1.093897 → `1.094` / 印刷 `1.094` | PASS |
|  75Hz TL (log) | 源 1.093897 → `1.094` / 印刷 `1.094` | PASS |
|  100Hz SOL (xlsx) | 源 1.854844175977632 → `1.855` / 印刷 `1.855` | PASS |
|  100Hz SOL (log) | 源 1.85484438 → `1.855` / 印刷 `1.855` | PASS |
|  100Hz TL (xlsx) | 源 1.489616 → `1.490` / 印刷 `1.490` | PASS |
|  100Hz TL (log) | 源 1.489616 → `1.490` / 印刷 `1.490` | PASS |
|  Avg. SOL (xlsx) | 源 1.6882909461855888 → `1.688` / 印刷 `1.688` | PASS |
|  Avg. SOL (log) | 源 1.6882910000000002 → `1.688` / 印刷 `1.688` | PASS |
|  Avg. TL (xlsx) | 源 0.9511941 → `0.951` / 印刷 `0.951` | PASS |
|  Avg. TL (log) | 源 0.9511941 → `0.951` / 印刷 `0.951` | PASS |
|  25Hz SOL (xlsx) | 源 32.02167481649667 → `32.022` / 印刷 `32.022` | PASS |
|  25Hz SOL (log) | 源 32.021673299999996 → `32.022` / 印刷 `32.022` | PASS |
|  25Hz TL (xlsx) | 源 1.507518 → `1.508` / 印刷 `1.508` | PASS |
|  25Hz TL (log) | 源 1.507518 → `1.508` / 印刷 `1.508` | PASS |
|  50Hz SOL (xlsx) | 源 18.3700246270746 → `18.370` / 印刷 `18.370` | PASS |
|  50Hz SOL (log) | 源 18.3700197 → `18.370` / 印刷 `18.370` | PASS |
|  50Hz TL (xlsx) | 源 1.869137 → `1.869` / 印刷 `1.869` | PASS |
|  50Hz TL (log) | 源 1.869137 → `1.869` / 印刷 `1.869` | PASS |
|  75Hz SOL (xlsx) | 源 53.54775651358068 → `53.548` / 印刷 `53.548` | PASS |
|  75Hz SOL (log) | 源 53.5477524 → `53.548` / 印刷 `53.548` | PASS |
|  75Hz TL (xlsx) | 源 3.490569 → `3.491` / 印刷 `3.491` | PASS |
|  75Hz TL (log) | 源 3.490569 → `3.491` / 印刷 `3.491` | PASS |
|  100Hz SOL (xlsx) | 源 81.19629761204123 → `81.196` / 印刷 `81.196` | PASS |
|  100Hz SOL (log) | 源 81.1962971 → `81.196` / 印刷 `81.196` | PASS |
|  100Hz TL (xlsx) | 源 7.067107 → `7.067` / 印刷 `7.067` | PASS |
|  100Hz TL (log) | 源 7.067107 → `7.067` / 印刷 `7.067` | PASS |
|  Avg. SOL (xlsx) | 源 46.28393617458641 → `46.284` / 印刷 `46.284` | PASS |
|  Avg. SOL (log) | 源 46.28394 → `46.284` / 印刷 `46.284` | PASS |
|  Avg. TL (xlsx) | 源 3.483583 → `3.484` / 印刷 `3.484` | PASS |
|  Avg. TL (log) | 源 3.483583 → `3.484` / 印刷 `3.484` | PASS |
|  25Hz SOL (xlsx) | 源 4.016159859020265 → `4.016` / 印刷 `4.016` | PASS |
|  25Hz SOL (log) | 源 4.0161594 → `4.016` / 印刷 `4.016` | PASS |
|  25Hz TL (xlsx) | 源 0.8294734 → `0.829` / 印刷 `0.829` | PASS |
|  25Hz TL (log) | 源 0.8294734 → `0.829` / 印刷 `0.829` | PASS |
|  50Hz SOL (xlsx) | 源 0.4407965883729048 → `0.441` / 印刷 `0.441` | PASS |
|  50Hz SOL (log) | 源 0.44079663399999996 → `0.441` / 印刷 `0.441` | PASS |
|  50Hz TL (xlsx) | 源 0.6063695 → `0.606` / 印刷 `0.606` | PASS |
|  50Hz TL (log) | 源 0.6063695 → `0.606` / 印刷 `0.606` | PASS |
|  75Hz SOL (xlsx) | 源 4.748221815680154 → `4.748` / 印刷 `4.748` | PASS |
|  75Hz SOL (log) | 源 4.748221780000001 → `4.748` / 印刷 `4.748` | PASS |
|  75Hz TL (xlsx) | 源 1.528673 → `1.529` / 印刷 `1.529` | PASS |
|  75Hz TL (log) | 源 1.528673 → `1.529` / 印刷 `1.529` | PASS |
|  100Hz SOL (xlsx) | 源 5.712977214716375 → `5.713` / 印刷 `5.713` | PASS |
|  100Hz SOL (log) | 源 5.712977230000001 → `5.713` / 印刷 `5.713` | PASS |
|  100Hz TL (xlsx) | 源 2.255599 → `2.256` / 印刷 `2.256` | PASS |
|  100Hz TL (log) | 源 2.255599 → `2.256` / 印刷 `2.256` | PASS |
|  Avg. SOL (xlsx) | 源 3.729538974585012 → `3.730` / 印刷 `3.730` | PASS |
|  Avg. SOL (log) | 源 3.729539 → `3.730` / 印刷 `3.730` | PASS |
|  Avg. TL (xlsx) | 源 1.305029 → `1.305` / 印刷 `1.305` | PASS |
|  Avg. TL (log) | 源 1.305029 → `1.305` / 印刷 `1.305` | PASS |
|  25Hz SOL (xlsx) | 源 37.509433086961515 → `37.509` / 印刷 `37.509` | PASS |
|  25Hz SOL (log) | 源 37.5094356 → `37.509` / 印刷 `37.509` | PASS |
|  25Hz TL (xlsx) | 源 1.758901 → `1.759` / 印刷 `1.759` | PASS |
|  25Hz TL (log) | 源 1.758901 → `1.759` / 印刷 `1.759` | PASS |
|  50Hz SOL (xlsx) | 源 12.21692649414763 → `12.217` / 印刷 `12.217` | PASS |
|  50Hz SOL (log) | 源 12.2169307 → `12.217` / 印刷 `12.217` | PASS |
|  50Hz TL (xlsx) | 源 1.911753 → `1.912` / 印刷 `1.912` | PASS |
|  50Hz TL (log) | 源 1.911753 → `1.912` / 印刷 `1.912` | PASS |
|  75Hz SOL (xlsx) | 源 29.49299784377217 → `29.493` / 印刷 `29.493` | PASS |
|  75Hz SOL (log) | 源 29.493000000000002 → `29.493` / 印刷 `29.493` | PASS |
|  75Hz TL (xlsx) | 源 3.001591 → `3.002` / 印刷 `3.002` | PASS |
|  75Hz TL (log) | 源 3.001591 → `3.002` / 印刷 `3.002` | PASS |
|  100Hz SOL (xlsx) | 源 34.6539280610159 → `34.654` / 印刷 `34.654` | PASS |
|  100Hz SOL (log) | 源 34.6539308 → `34.654` / 印刷 `34.654` | PASS |
|  100Hz TL (xlsx) | 源 4.281503 → `4.282` / 印刷 `4.282` | PASS |
|  100Hz TL (log) | 源 4.281503 → `4.282` / 印刷 `4.282` | PASS |
|  Avg. SOL (xlsx) | 源 28.46832028590143 → `28.468` / 印刷 `28.468` | PASS |
|  Avg. SOL (log) | 源 28.468329999999998 → `28.468` / 印刷 `28.468` | PASS |
|  Avg. TL (xlsx) | 源 2.738437 → `2.738` / 印刷 `2.738` | PASS |
|  Avg. TL (log) | 源 2.738437 → `2.738` / 印刷 `2.738` | PASS |
|  25Hz SOL (xlsx) | 源 35.926640615798526 → `35.927` / 印刷 `35.927` | PASS |
|  25Hz SOL (log) | 源 35.926643600000006 → `35.927` / 印刷 `35.927` | PASS |
|  25Hz TL (xlsx) | 源 1.832511 → `1.833` / 印刷 `1.833` | PASS |
|  25Hz TL (log) | 源 1.832511 → `1.833` / 印刷 `1.833` | PASS |
|  50Hz SOL (xlsx) | 源 4.9055928422603765 → `4.906` / 印刷 `4.906` | PASS |
|  50Hz SOL (log) | 源 4.90559308 → `4.906` / 印刷 `4.906` | PASS |
|  50Hz TL (xlsx) | 源 1.345858 → `1.346` / 印刷 `1.346` | PASS |
|  50Hz TL (log) | 源 1.345858 → `1.346` / 印刷 `1.346` | PASS |
|  75Hz SOL (xlsx) | 源 34.554940043017275 → `34.555` / 印刷 `34.555` | PASS |
|  75Hz SOL (log) | 源 34.554940599999995 → `34.555` / 印刷 `34.555` | PASS |
|  75Hz TL (xlsx) | 源 2.869022 → `2.869` / 印刷 `2.869` | PASS |
|  75Hz TL (log) | 源 2.869022 → `2.869` / 印刷 `2.869` | PASS |
|  100Hz SOL (xlsx) | 源 32.65789831057191 → `32.658` / 印刷 `32.658` | PASS |
|  100Hz SOL (log) | 源 32.657901 → `32.658` / 印刷 `32.658` | PASS |
|  100Hz TL (xlsx) | 源 4.489058 → `4.489` / 印刷 `4.489` | PASS |
|  100Hz TL (log) | 源 4.489058 → `4.489` / 印刷 `4.489` | PASS |
|  Avg. SOL (xlsx) | 源 27.011267002671957 → `27.011` / 印刷 `27.011` | PASS |
|  Avg. SOL (log) | 源 27.01127 → `27.011` / 印刷 `27.011` | PASS |
|  Avg. TL (xlsx) | 源 2.634112 → `2.634` / 印刷 `2.634` | PASS |
|  Avg. TL (log) | 源 2.634112 → `2.634` / 印刷 `2.634` | PASS |
|  25Hz SOL (xlsx) | 源 3.958929784130305 → `3.959` / 印刷 `3.959` | PASS |
|  25Hz SOL (log) | 源 3.9589297199999995 → `3.959` / 印刷 `3.959` | PASS |
|  25Hz TL (xlsx) | 源 0.7091513 → `0.709` / 印刷 `0.709` | PASS |
|  25Hz TL (log) | 源 0.7091513 → `0.709` / 印刷 `0.709` | PASS |
|  50Hz SOL (xlsx) | 源 0.26640543073881423 → `0.266` / 印刷 `0.266` | PASS |
|  50Hz SOL (log) | 源 0.266405447 → `0.266` / 印刷 `0.266` | PASS |
|  50Hz TL (xlsx) | 源 0.6107074 → `0.611` / 印刷 `0.611` | PASS |
|  50Hz TL (log) | 源 0.6107074 → `0.611` / 印刷 `0.611` | PASS |
|  75Hz SOL (xlsx) | 源 1.9178623508196322 → `1.918` / 印刷 `1.918` | PASS |
|  75Hz SOL (log) | 源 1.9178620900000003 → `1.918` / 印刷 `1.918` | PASS |
|  75Hz TL (xlsx) | 源 1.011998 → `1.012` / 印刷 `1.012` | PASS |
|  75Hz TL (log) | 源 1.011998 → `1.012` / 印刷 `1.012` | PASS |
|  100Hz SOL (xlsx) | 源 2.340470429044217 → `2.340` / 印刷 `2.340` | PASS |
|  100Hz SOL (log) | 源 2.3404708999999997 → `2.340` / 印刷 `2.340` | PASS |
|  100Hz TL (xlsx) | 源 1.265287 → `1.265` / 印刷 `1.265` | PASS |
|  100Hz TL (log) | 源 1.265287 → `1.265` / 印刷 `1.265` | PASS |
|  Avg. SOL (xlsx) | 源 2.1209166909102346 → `2.121` / 印刷 `2.121` | PASS |
|  Avg. SOL (log) | 源 2.120917 → `2.121` / 印刷 `2.121` | PASS |
|  Avg. TL (xlsx) | 源 0.899286 → `0.899` / 印刷 `0.899` | PASS |
|  Avg. TL (log) | 源 0.899286 → `0.899` / 印刷 `0.899` | PASS |
|  25Hz SOL (xlsx) | 源 23.320367420092218 → `23.320` / 印刷 `23.320` | PASS |
|  25Hz SOL (log) | 源 23.3203663 → `23.320` / 印刷 `23.320` | PASS |
|  25Hz TL (xlsx) | 源 1.301132 → `1.301` / 印刷 `1.301` | PASS |
|  25Hz TL (log) | 源 1.301132 → `1.301` / 印刷 `1.301` | PASS |
|  50Hz SOL (xlsx) | 源 12.677953671664001 → `12.678` / 印刷 `12.678` | PASS |
|  50Hz SOL (log) | 源 12.677950500000003 → `12.678` / 印刷 `12.678` | PASS |
|  50Hz TL (xlsx) | 源 1.381942 → `1.382` / 印刷 `1.382` | PASS |
|  50Hz TL (log) | 源 1.381942 → `1.382` / 印刷 `1.382` | PASS |
|  75Hz SOL (xlsx) | 源 45.68477077409625 → `45.685` / 印刷 `45.685` | PASS |
|  75Hz SOL (log) | 源 45.6847723 → `45.685` / 印刷 `45.685` | PASS |
|  75Hz TL (xlsx) | 源 2.805426 → `2.805` / 印刷 `2.805` | PASS |
|  75Hz TL (log) | 源 2.805426 → `2.805` / 印刷 `2.805` | PASS |
|  100Hz SOL (xlsx) | 源 127.983848657459 → `127.984` / 印刷 `127.984` | PASS |
|  100Hz SOL (log) | 源 127.983862 → `127.984` / 印刷 `127.984` | PASS |
|  100Hz TL (xlsx) | 源 5.511891 → `5.512` / 印刷 `5.512` | PASS |
|  100Hz TL (log) | 源 5.511891 → `5.512` / 印刷 `5.512` | PASS |
|  Avg. SOL (xlsx) | 源 52.41673775017262 → `52.417` / 印刷 `52.417` | PASS |
|  Avg. SOL (log) | 源 52.41674 → `52.417` / 印刷 `52.417` | PASS |
|  Avg. TL (xlsx) | 源 2.750098 → `2.750` / 印刷 `2.750` | PASS |
|  Avg. TL (log) | 源 2.750098 → `2.750` / 印刷 `2.750` | PASS |
|  25Hz SOL (xlsx) | 源 5.422724352683872 → `5.423` / 印刷 `5.423` | PASS |
|  25Hz SOL (log) | 源 5.42272475 → `5.423` / 印刷 `5.423` | PASS |
|  25Hz TL (xlsx) | 源 0.8951543 → `0.895` / 印刷 `0.895` | PASS |
|  25Hz TL (log) | 源 0.8951543 → `0.895` / 印刷 `0.895` | PASS |
|  50Hz SOL (xlsx) | 源 0.40133751172106713 → `0.401` / 印刷 `0.401` | PASS |
|  50Hz SOL (log) | 源 0.401337525 → `0.401` / 印刷 `0.401` | PASS |
|  50Hz TL (xlsx) | 源 0.668 → `0.668` / 印刷 `0.668` | PASS |
|  50Hz TL (log) | 源 0.668 → `0.668` / 印刷 `0.668` | PASS |
|  75Hz SOL (xlsx) | 源 2.328076647245325 → `2.328` / 印刷 `2.328` | PASS |
|  75Hz SOL (log) | 源 2.32807623 → `2.328` / 印刷 `2.328` | PASS |
|  75Hz TL (xlsx) | 源 1.159577 → `1.160` / 印刷 `1.160` | PASS |
|  75Hz TL (log) | 源 1.159577 → `1.160` / 印刷 `1.160` | PASS |
|  100Hz SOL (xlsx) | 源 4.565394896781072 → `4.565` / 印刷 `4.565` | PASS |
|  100Hz SOL (log) | 源 4.56539505 → `4.565` / 印刷 `4.565` | PASS |
|  100Hz TL (xlsx) | 源 1.637377 → `1.637` / 印刷 `1.637` | PASS |
|  100Hz TL (log) | 源 1.637377 → `1.637` / 印刷 `1.637` | PASS |
|  Avg. SOL (xlsx) | 源 3.179383306996897 → `3.179` / 印刷 `3.179` | PASS |
|  Avg. SOL (log) | 源 3.179383 → `3.179` / 印刷 `3.179` | PASS |
|  Avg. TL (xlsx) | 源 1.090027 → `1.090` / 印刷 `1.090` | PASS |
|  Avg. TL (log) | 源 1.090027 → `1.090` / 印刷 `1.090` | PASS |
|  25Hz SOL (xlsx) | 源 46.23470031656326 → `46.235` / 印刷 `46.235` | PASS |
|  25Hz SOL (log) | 源 46.234703 → `46.235` / 印刷 `46.235` | PASS |
|  25Hz TL (xlsx) | 源 1.346344 → `1.346` / 印刷 `1.346` | PASS |
|  25Hz TL (log) | 源 1.346344 → `1.346` / 印刷 `1.346` | PASS |
|  50Hz SOL (xlsx) | 源 5.179396871244535 → `5.179` / 印刷 `5.179` | PASS |
|  50Hz SOL (log) | 源 5.17939703 → `5.179` / 印刷 `5.179` | PASS |
|  50Hz TL (xlsx) | 源 1.216249 → `1.216` / 印刷 `1.216` | PASS |
|  50Hz TL (log) | 源 1.216249 → `1.216` / 印刷 `1.216` | PASS |
|  75Hz SOL (xlsx) | 源 24.48505545035005 → `24.485` / 印刷 `24.485` | PASS |
|  75Hz SOL (log) | 源 24.485059399999997 → `24.485` / 印刷 `24.485` | PASS |
|  75Hz TL (xlsx) | 源 2.334058 → `2.334` / 印刷 `2.334` | PASS |
|  75Hz TL (log) | 源 2.334058 → `2.334` / 印刷 `2.334` | PASS |
|  100Hz SOL (xlsx) | 源 28.634844440966837 → `28.635` / 印刷 `28.635` | PASS |
|  100Hz SOL (log) | 源 28.634841599999998 → `28.635` / 印刷 `28.635` | PASS |
|  100Hz TL (xlsx) | 源 3.010926 → `3.011` / 印刷 `3.011` | PASS |
|  100Hz TL (log) | 源 3.010926 → `3.011` / 印刷 `3.011` | PASS |
|  Avg. SOL (xlsx) | 源 26.13350008614361 → `26.134` / 印刷 `26.134` | PASS |
|  Avg. SOL (log) | 源 26.1335 → `26.134` / 印刷 `26.134` | PASS |
|  Avg. TL (xlsx) | 源 1.976894 → `1.977` / 印刷 `1.977` | PASS |
|  Avg. TL (log) | 源 1.976894 → `1.977` / 印刷 `1.977` | PASS |
|  25Hz SOL (xlsx) | 源 57.71513618528843 → `57.715` / 印刷 `57.715` | PASS |
|  25Hz SOL (log) | 源 57.715138599999996 → `57.715` / 印刷 `57.715` | PASS |
|  25Hz TL (xlsx) | 源 1.33072 → `1.331` / 印刷 `1.331` | PASS |
|  25Hz TL (log) | 源 1.33072 → `1.331` / 印刷 `1.331` | PASS |
|  50Hz SOL (xlsx) | 源 6.5668119001202285 → `6.567` / 印刷 `6.567` | PASS |
|  50Hz SOL (log) | 源 6.56681187 → `6.567` / 印刷 `6.567` | PASS |
|  50Hz TL (xlsx) | 源 1.214305 → `1.214` / 印刷 `1.214` | PASS |
|  50Hz TL (log) | 源 1.214305 → `1.214` / 印刷 `1.214` | PASS |
|  75Hz SOL (xlsx) | 源 53.3690960612148 → `53.369` / 印刷 `53.369` | PASS |
|  75Hz SOL (log) | 源 53.36909910000001 → `53.369` / 印刷 `53.369` | PASS |
|  75Hz TL (xlsx) | 源 2.831276 → `2.831` / 印刷 `2.831` | PASS |
|  75Hz TL (log) | 源 2.831276 → `2.831` / 印刷 `2.831` | PASS |
|  100Hz SOL (xlsx) | 源 70.37499751895666 → `70.375` / 印刷 `70.375` | PASS |
|  100Hz SOL (log) | 源 70.37499999999999 → `70.375` / 印刷 `70.375` | PASS |
|  100Hz TL (xlsx) | 源 4.124078 → `4.124` / 印刷 `4.124` | PASS |
|  100Hz TL (log) | 源 4.124078 → `4.124` / 印刷 `4.124` | PASS |
|  Avg. SOL (xlsx) | 源 47.00651261955499 → `47.007` / 印刷 `47.007` | PASS |
|  Avg. SOL (log) | 源 47.00651 → `47.007` / 印刷 `47.007` | PASS |
|  Avg. TL (xlsx) | 源 2.375095 → `2.375` / 印刷 `2.375` | PASS |
|  Avg. TL (log) | 源 2.375095 → `2.375` / 印刷 `2.375` | PASS |

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
| 全部 100 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 8. 加粗判据（每列在各几何块内的最小值）

> caption：'The best value in each column, within each geometry, is in bold'。两几何是上下两块、行集合互不相干，故最小值必须**分块**取；若误按全表取，楔形块会出现 5 行全不加粗而隐形漏检。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 两几何块 × 10 列 = 20 处加粗均指向块内最小值 | 全部合规 | PASS |

## 9. 正文引用精确性（4.4 节）

> 每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。只查①会漏掉正文与表格一起错的情形。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 4.4 节正文窗口可定位 | 起句 `The proposed solver attains the lowest s…` | PASS |
| 正文 Case 15 频均 Sol | 正文 `1.688` / 表格 `1.688` | PASS |
| 正文 Case 15 频均 Sol <- xlsx 源 | 源 1.6882909461855888 → `1.688` / 印刷 `1.688` | PASS |
| 正文 Case 15 频均 Sol 可定位 | 窗口内行 3 | PASS |
| 正文 Case 15 频均 TL | 正文 `0.951` / 表格 `0.951` | PASS |
| 正文 Case 15 频均 TL <- xlsx 源 | 源 0.9511941 → `0.951` / 印刷 `0.951` | PASS |
| 正文 Case 15 频均 TL 可定位 | 窗口内行 7 | PASS |
| 正文 Case 17 频均 Sol | 正文 `3.730` / 表格 `3.730` | PASS |
| 正文 Case 17 频均 Sol <- xlsx 源 | 源 3.729538974585012 → `3.730` / 印刷 `3.730` | PASS |
| 正文 Case 17 频均 Sol 可定位 | 窗口内行 9 | PASS |
| 正文 Case 17 频均 TL | 正文 `1.305` / 表格 `1.305` | PASS |
| 正文 Case 17 频均 TL <- xlsx 源 | 源 1.305029 → `1.305` / 印刷 `1.305` | PASS |
| 正文 Case 17 频均 TL 可定位 | 窗口内行 10 | PASS |
| 正文 Case 20 频均 Sol | 正文 `2.121` / 表格 `2.121` | PASS |
| 正文 Case 20 频均 Sol <- xlsx 源 | 源 2.1209166909102346 → `2.121` / 印刷 `2.121` | PASS |
| 正文 Case 20 频均 Sol 可定位 | 窗口内行 16 | PASS |
| 正文 Case 20 频均 TL | 正文 `0.899` / 表格 `0.899` | PASS |
| 正文 Case 20 频均 TL <- xlsx 源 | 源 0.899286 → `0.899` / 印刷 `0.899` | PASS |
| 正文 Case 20 频均 TL 可定位 | 窗口内行 17 | PASS |
| 正文 Case 22 频均 Sol | 正文 `3.179` / 表格 `3.179` | PASS |
| 正文 Case 22 频均 Sol <- xlsx 源 | 源 3.179383306996897 → `3.179` / 印刷 `3.179` | PASS |
| 正文 Case 22 频均 Sol 可定位 | 窗口内行 17 | PASS |
| 正文 Case 22 频均 TL | 正文 `1.090` / 表格 `1.090` | PASS |
| 正文 Case 22 频均 TL <- xlsx 源 | 源 1.090027 → `1.090` / 印刷 `1.090` | PASS |
| 正文 Case 22 频均 TL 可定位 | 窗口内行 18 | PASS |
| 正文 Case 20 @100Hz TL | 正文 `1.265` / 表格 `1.265` | PASS |
| 正文 Case 20 @100Hz TL <- xlsx 源 | 源 1.265287 → `1.265` / 印刷 `1.265` | PASS |
| 正文 Case 20 @100Hz TL 可定位 | 窗口内行 26 | PASS |
| 正文 Case 21 @100Hz TL | 正文 `5.512` / 表格 `5.512` | PASS |
| 正文 Case 21 @100Hz TL <- xlsx 源 | 源 5.511891 → `5.512` / 印刷 `5.512` | PASS |
| 正文 Case 21 @100Hz TL 可定位 | 窗口内行 26 | PASS |

## 10. caption 声明核验

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 数据源确为该口径 | PASS |
| caption 未误写 last epoch | 口径唯一 | PASS |
| 表号为 10 | aux `10` | PASS |

## 11. caption 其余声明（按几何加粗 / 四频均值 / 案例号 / 图引用）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 写明加粗按几何分别判定 |  | PASS |
| caption 声明 Avg. 为四频均值 |  | PASS |
| caption 写明两块的案例号范围 |  | PASS |
| caption 交叉引用 Fig.\ref{fig:perf-cmp-r}/{-w} |  | PASS |

