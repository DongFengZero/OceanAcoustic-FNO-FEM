# Table 6 — 多频前向精度 R1-R3/W1-W3

- 对象：`tab:res-rect-mf`（Table 6）
- 结论：**PASS** — 277 通过 / 0 失败 / 0 警告，共 277 项
- 脚本：`ch4_validation/scripts/T06_res_rect_mf.py`
- 生成：2026-07-28 20:29:30

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:res-rect-mf}` 所在 table* 环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/Case3-14_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 3) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No03_R1/training_run/logs/full_run_20260710_221657.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 4) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No04_R2/training_run/logs/full_run_20260710_214148.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 5) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No05_R3/training_run/logs/full_run_20260710_024112.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 9) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No09_W1/training_run/logs/full_run_20260710_152228.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 10) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No10_W2/training_run/logs/full_run_20260710_123954.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 11) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No11_W3/training_run/logs/full_run_20260710_022039.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/Case3-14_数据汇总.xlsx | PASS |
| Case 3 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No03_R1/training_run/logs/full_run_20260710_221657.log | PASS |
| Case 4 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No04_R2/training_run/logs/full_run_20260710_214148.log | PASS |
| Case 5 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No05_R3/training_run/logs/full_run_20260710_024112.log | PASS |
| Case 9 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No09_W1/training_run/logs/full_run_20260710_152228.log | PASS |
| Case 10 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No10_W2/training_run/logs/full_run_20260710_123954.log | PASS |
| Case 11 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No11_W3/training_run/logs/full_run_20260710_022039.log | PASS |
| tex 表格环境可定位且确实包住 label | `tab:res-rect-mf`，长度 1964 | PASS |
| tex 数据行数 = 6 | 实得 6 | PASS |
| tex 行 No. 覆盖 3-5 与 9-11 | [3, 4, 5, 9, 10, 11] | PASS |

## 3. best epoch 一致性

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 3 best epoch | xlsx `198` / log `198` | PASS |
| Case 3 日志含『评估 Epoch 198』块 | 轮次 198 | PASS |
| Case 4 best epoch | xlsx `200` / log `200` | PASS |
| Case 4 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |
| Case 5 best epoch | xlsx `200` / log `200` | PASS |
| Case 5 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |
| Case 9 best epoch | xlsx `181` / log `181` | PASS |
| Case 9 日志含『评估 Epoch 181』块 | 轮次 181 | PASS |
| Case 10 best epoch | xlsx `192` / log `192` | PASS |
| Case 10 日志含『评估 Epoch 192』块 | 轮次 192 | PASS |
| Case 11 best epoch | xlsx `200` / log `200` | PASS |
| Case 11 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |

## 4. 双渠道交叉验证（xlsx vs log，同一 best epoch）

> 日志侧取『评估 Epoch N 完成』块（测试集），非『训练』块；Sol 由 `(损失 − w_prior×prior)/w_rel` 现场算，权重逐轮解析。

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 3 Overall SOL | `1.6882909461855888` / `1.6882910000000002` | PASS |
| Case 3 Overall TL | `0.9511941` / `0.9511941` | PASS |
| Case 3 25 SOL | `2.475624985527247` / `2.4756253` | PASS |
| Case 3 25 TL | `0.7047694` / `0.7047694` | PASS |
| Case 3 50 SOL | `0.266019553237129` / `0.26601958000000003` | PASS |
| Case 3 50 TL | `0.516494` / `0.516494` | PASS |
| Case 3 75 SOL | `2.156675141304732` / `2.15667489` | PASS |
| Case 3 75 TL | `1.093897` / `1.093897` | PASS |
| Case 3 100 SOL | `1.854844175977632` / `1.85484438` | PASS |
| Case 3 100 TL | `1.489616` / `1.489616` | PASS |
| Case 4 Overall SOL | `3.773339698091149` / `3.7733390000000004` | PASS |
| Case 4 Overall TL | `1.36862` / `1.36862` | PASS |
| Case 4 25 SOL | `3.005988581571728` / `3.0059886400000004` | PASS |
| Case 4 25 TL | `0.7880404` / `0.7880404` | PASS |
| Case 4 50 SOL | `1.096274408337194` / `1.0962745` | PASS |
| Case 4 50 TL | `0.6626845` / `0.6626845` | PASS |
| Case 4 75 SOL | `4.015348758548498` / `4.015348` | PASS |
| Case 4 75 TL | `1.421382` / `1.421382` | PASS |
| Case 4 100 SOL | `6.975745828822255` / `6.975745699999999` | PASS |
| Case 4 100 TL | `2.602374` / `2.602374` | PASS |
| Case 5 Overall SOL | `13.163763936609032` / `13.16376` | PASS |
| Case 5 Overall TL | `2.157118` / `2.157118` | PASS |
| Case 5 25 SOL | `3.9512569957878436` / `3.9512571000000003` | PASS |
| Case 5 25 TL | `0.88342` / `0.88342` | PASS |
| Case 5 50 SOL | `6.623950600624084` / `6.623950599999999` | PASS |
| Case 5 50 TL | `1.143559` / `1.143559` | PASS |
| Case 5 75 SOL | `15.971385035663841` / `15.971386000000003` | PASS |
| Case 5 75 TL | `2.565011` / `2.565011` | PASS |
| Case 5 100 SOL | `26.10846422612667` / `26.10846` | PASS |
| Case 5 100 TL | `4.036483` / `4.036483` | PASS |
| Case 9 Overall SOL | `2.1209166909102346` / `2.120917` | PASS |
| Case 9 Overall TL | `0.899286` / `0.899286` | PASS |
| Case 9 25 SOL | `3.958929784130305` / `3.9589297199999995` | PASS |
| Case 9 25 TL | `0.7091513` / `0.7091513` | PASS |
| Case 9 50 SOL | `0.26640543073881423` / `0.266405447` | PASS |
| Case 9 50 TL | `0.6107074` / `0.6107074` | PASS |
| Case 9 75 SOL | `1.9178623508196322` / `1.9178620900000003` | PASS |
| Case 9 75 TL | `1.011998` / `1.011998` | PASS |
| Case 9 100 SOL | `2.340470429044217` / `2.3404708999999997` | PASS |
| Case 9 100 TL | `1.265287` / `1.265287` | PASS |
| Case 10 Overall SOL | `3.377542411908507` / `3.377543` | PASS |
| Case 10 Overall TL | `1.178464` / `1.178464` | PASS |
| Case 10 25 SOL | `2.151557384058833` / `2.15155723` | PASS |
| Case 10 25 TL | `0.9517106` / `0.9517106` | PASS |
| Case 10 50 SOL | `1.093047365429811` / `1.09304735` | PASS |
| Case 10 50 TL | `0.7252787` / `0.7252787` | PASS |
| Case 10 75 SOL | `5.118295981083064` / `5.118296` | PASS |
| Case 10 75 TL | `1.409486` / `1.409486` | PASS |
| Case 10 100 SOL | `5.147270672023296` / `5.147271000000001` | PASS |
| Case 10 100 TL | `1.627381` / `1.627381` | PASS |
| Case 11 Overall SOL | `10.79732421785593` / `10.79733` | PASS |
| Case 11 Overall TL | `1.85227` / `1.85227` | PASS |
| Case 11 25 SOL | `5.667485436424613` / `5.66748593` | PASS |
| Case 11 25 TL | `1.996354` / `1.996354` | PASS |
| Case 11 50 SOL | `5.145914969034493` / `5.145914500000001` | PASS |
| Case 11 50 TL | `1.076485` / `1.076485` | PASS |
| Case 11 75 SOL | `12.25881576538086` / `12.258818999999999` | PASS |
| Case 11 75 TL | `1.765749` / `1.765749` | PASS |
| Case 11 100 SOL | `20.117080397903912` / `20.117077000000002` | PASS |
| Case 11 100 TL | `2.570491` / `2.570491` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Dataset, Fig., 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。Avg. 对应 xlsx/日志的 Overall 组。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 Dataset 名 | tex `R1` | PASS |
| Case 3 25Hz SOL (xlsx) | 源 2.475624985527247 → `2.476` / 印刷 `2.476` | PASS |
| Case 3 25Hz SOL (log) | 源 2.4756253 → `2.476` / 印刷 `2.476` | PASS |
| Case 3 25Hz TL (xlsx) | 源 0.7047694 → `0.705` / 印刷 `0.705` | PASS |
| Case 3 25Hz TL (log) | 源 0.7047694 → `0.705` / 印刷 `0.705` | PASS |
| Case 3 50Hz SOL (xlsx) | 源 0.266019553237129 → `0.266` / 印刷 `0.266` | PASS |
| Case 3 50Hz SOL (log) | 源 0.26601958000000003 → `0.266` / 印刷 `0.266` | PASS |
| Case 3 50Hz TL (xlsx) | 源 0.516494 → `0.516` / 印刷 `0.516` | PASS |
| Case 3 50Hz TL (log) | 源 0.516494 → `0.516` / 印刷 `0.516` | PASS |
| Case 3 75Hz SOL (xlsx) | 源 2.156675141304732 → `2.157` / 印刷 `2.157` | PASS |
| Case 3 75Hz SOL (log) | 源 2.15667489 → `2.157` / 印刷 `2.157` | PASS |
| Case 3 75Hz TL (xlsx) | 源 1.093897 → `1.094` / 印刷 `1.094` | PASS |
| Case 3 75Hz TL (log) | 源 1.093897 → `1.094` / 印刷 `1.094` | PASS |
| Case 3 100Hz SOL (xlsx) | 源 1.854844175977632 → `1.855` / 印刷 `1.855` | PASS |
| Case 3 100Hz SOL (log) | 源 1.85484438 → `1.855` / 印刷 `1.855` | PASS |
| Case 3 100Hz TL (xlsx) | 源 1.489616 → `1.490` / 印刷 `1.490` | PASS |
| Case 3 100Hz TL (log) | 源 1.489616 → `1.490` / 印刷 `1.490` | PASS |
| Case 3 Avg. SOL (xlsx) | 源 1.6882909461855888 → `1.688` / 印刷 `1.688` | PASS |
| Case 3 Avg. SOL (log) | 源 1.6882910000000002 → `1.688` / 印刷 `1.688` | PASS |
| Case 3 Avg. TL (xlsx) | 源 0.9511941 → `0.951` / 印刷 `0.951` | PASS |
| Case 3 Avg. TL (log) | 源 0.9511941 → `0.951` / 印刷 `0.951` | PASS |
| Case 4 Dataset 名 | tex `R2` | PASS |
| Case 4 25Hz SOL (xlsx) | 源 3.005988581571728 → `3.006` / 印刷 `3.006` | PASS |
| Case 4 25Hz SOL (log) | 源 3.0059886400000004 → `3.006` / 印刷 `3.006` | PASS |
| Case 4 25Hz TL (xlsx) | 源 0.7880404 → `0.788` / 印刷 `0.788` | PASS |
| Case 4 25Hz TL (log) | 源 0.7880404 → `0.788` / 印刷 `0.788` | PASS |
| Case 4 50Hz SOL (xlsx) | 源 1.096274408337194 → `1.096` / 印刷 `1.096` | PASS |
| Case 4 50Hz SOL (log) | 源 1.0962745 → `1.096` / 印刷 `1.096` | PASS |
| Case 4 50Hz TL (xlsx) | 源 0.6626845 → `0.663` / 印刷 `0.663` | PASS |
| Case 4 50Hz TL (log) | 源 0.6626845 → `0.663` / 印刷 `0.663` | PASS |
| Case 4 75Hz SOL (xlsx) | 源 4.015348758548498 → `4.015` / 印刷 `4.015` | PASS |
| Case 4 75Hz SOL (log) | 源 4.015348 → `4.015` / 印刷 `4.015` | PASS |
| Case 4 75Hz TL (xlsx) | 源 1.421382 → `1.421` / 印刷 `1.421` | PASS |
| Case 4 75Hz TL (log) | 源 1.421382 → `1.421` / 印刷 `1.421` | PASS |
| Case 4 100Hz SOL (xlsx) | 源 6.975745828822255 → `6.976` / 印刷 `6.976` | PASS |
| Case 4 100Hz SOL (log) | 源 6.975745699999999 → `6.976` / 印刷 `6.976` | PASS |
| Case 4 100Hz TL (xlsx) | 源 2.602374 → `2.602` / 印刷 `2.602` | PASS |
| Case 4 100Hz TL (log) | 源 2.602374 → `2.602` / 印刷 `2.602` | PASS |
| Case 4 Avg. SOL (xlsx) | 源 3.773339698091149 → `3.773` / 印刷 `3.773` | PASS |
| Case 4 Avg. SOL (log) | 源 3.7733390000000004 → `3.773` / 印刷 `3.773` | PASS |
| Case 4 Avg. TL (xlsx) | 源 1.36862 → `1.369` / 印刷 `1.369` | PASS |
| Case 4 Avg. TL (log) | 源 1.36862 → `1.369` / 印刷 `1.369` | PASS |
| Case 5 Dataset 名 | tex `R3` | PASS |
| Case 5 25Hz SOL (xlsx) | 源 3.9512569957878436 → `3.951` / 印刷 `3.951` | PASS |
| Case 5 25Hz SOL (log) | 源 3.9512571000000003 → `3.951` / 印刷 `3.951` | PASS |
| Case 5 25Hz TL (xlsx) | 源 0.88342 → `0.883` / 印刷 `0.883` | PASS |
| Case 5 25Hz TL (log) | 源 0.88342 → `0.883` / 印刷 `0.883` | PASS |
| Case 5 50Hz SOL (xlsx) | 源 6.623950600624084 → `6.624` / 印刷 `6.624` | PASS |
| Case 5 50Hz SOL (log) | 源 6.623950599999999 → `6.624` / 印刷 `6.624` | PASS |
| Case 5 50Hz TL (xlsx) | 源 1.143559 → `1.144` / 印刷 `1.144` | PASS |
| Case 5 50Hz TL (log) | 源 1.143559 → `1.144` / 印刷 `1.144` | PASS |
| Case 5 75Hz SOL (xlsx) | 源 15.971385035663841 → `15.971` / 印刷 `15.971` | PASS |
| Case 5 75Hz SOL (log) | 源 15.971386000000003 → `15.971` / 印刷 `15.971` | PASS |
| Case 5 75Hz TL (xlsx) | 源 2.565011 → `2.565` / 印刷 `2.565` | PASS |
| Case 5 75Hz TL (log) | 源 2.565011 → `2.565` / 印刷 `2.565` | PASS |
| Case 5 100Hz SOL (xlsx) | 源 26.10846422612667 → `26.108` / 印刷 `26.108` | PASS |
| Case 5 100Hz SOL (log) | 源 26.10846 → `26.108` / 印刷 `26.108` | PASS |
| Case 5 100Hz TL (xlsx) | 源 4.036483 → `4.036` / 印刷 `4.036` | PASS |
| Case 5 100Hz TL (log) | 源 4.036483 → `4.036` / 印刷 `4.036` | PASS |
| Case 5 Avg. SOL (xlsx) | 源 13.163763936609032 → `13.164` / 印刷 `13.164` | PASS |
| Case 5 Avg. SOL (log) | 源 13.16376 → `13.164` / 印刷 `13.164` | PASS |
| Case 5 Avg. TL (xlsx) | 源 2.157118 → `2.157` / 印刷 `2.157` | PASS |
| Case 5 Avg. TL (log) | 源 2.157118 → `2.157` / 印刷 `2.157` | PASS |
| Case 9 Dataset 名 | tex `W1` | PASS |
| Case 9 25Hz SOL (xlsx) | 源 3.958929784130305 → `3.959` / 印刷 `3.959` | PASS |
| Case 9 25Hz SOL (log) | 源 3.9589297199999995 → `3.959` / 印刷 `3.959` | PASS |
| Case 9 25Hz TL (xlsx) | 源 0.7091513 → `0.709` / 印刷 `0.709` | PASS |
| Case 9 25Hz TL (log) | 源 0.7091513 → `0.709` / 印刷 `0.709` | PASS |
| Case 9 50Hz SOL (xlsx) | 源 0.26640543073881423 → `0.266` / 印刷 `0.266` | PASS |
| Case 9 50Hz SOL (log) | 源 0.266405447 → `0.266` / 印刷 `0.266` | PASS |
| Case 9 50Hz TL (xlsx) | 源 0.6107074 → `0.611` / 印刷 `0.611` | PASS |
| Case 9 50Hz TL (log) | 源 0.6107074 → `0.611` / 印刷 `0.611` | PASS |
| Case 9 75Hz SOL (xlsx) | 源 1.9178623508196322 → `1.918` / 印刷 `1.918` | PASS |
| Case 9 75Hz SOL (log) | 源 1.9178620900000003 → `1.918` / 印刷 `1.918` | PASS |
| Case 9 75Hz TL (xlsx) | 源 1.011998 → `1.012` / 印刷 `1.012` | PASS |
| Case 9 75Hz TL (log) | 源 1.011998 → `1.012` / 印刷 `1.012` | PASS |
| Case 9 100Hz SOL (xlsx) | 源 2.340470429044217 → `2.340` / 印刷 `2.340` | PASS |
| Case 9 100Hz SOL (log) | 源 2.3404708999999997 → `2.340` / 印刷 `2.340` | PASS |
| Case 9 100Hz TL (xlsx) | 源 1.265287 → `1.265` / 印刷 `1.265` | PASS |
| Case 9 100Hz TL (log) | 源 1.265287 → `1.265` / 印刷 `1.265` | PASS |
| Case 9 Avg. SOL (xlsx) | 源 2.1209166909102346 → `2.121` / 印刷 `2.121` | PASS |
| Case 9 Avg. SOL (log) | 源 2.120917 → `2.121` / 印刷 `2.121` | PASS |
| Case 9 Avg. TL (xlsx) | 源 0.899286 → `0.899` / 印刷 `0.899` | PASS |
| Case 9 Avg. TL (log) | 源 0.899286 → `0.899` / 印刷 `0.899` | PASS |
| Case 10 Dataset 名 | tex `W2` | PASS |
| Case 10 25Hz SOL (xlsx) | 源 2.151557384058833 → `2.152` / 印刷 `2.152` | PASS |
| Case 10 25Hz SOL (log) | 源 2.15155723 → `2.152` / 印刷 `2.152` | PASS |
| Case 10 25Hz TL (xlsx) | 源 0.9517106 → `0.952` / 印刷 `0.952` | PASS |
| Case 10 25Hz TL (log) | 源 0.9517106 → `0.952` / 印刷 `0.952` | PASS |
| Case 10 50Hz SOL (xlsx) | 源 1.093047365429811 → `1.093` / 印刷 `1.093` | PASS |
| Case 10 50Hz SOL (log) | 源 1.09304735 → `1.093` / 印刷 `1.093` | PASS |
| Case 10 50Hz TL (xlsx) | 源 0.7252787 → `0.725` / 印刷 `0.725` | PASS |
| Case 10 50Hz TL (log) | 源 0.7252787 → `0.725` / 印刷 `0.725` | PASS |
| Case 10 75Hz SOL (xlsx) | 源 5.118295981083064 → `5.118` / 印刷 `5.118` | PASS |
| Case 10 75Hz SOL (log) | 源 5.118296 → `5.118` / 印刷 `5.118` | PASS |
| Case 10 75Hz TL (xlsx) | 源 1.409486 → `1.409` / 印刷 `1.409` | PASS |
| Case 10 75Hz TL (log) | 源 1.409486 → `1.409` / 印刷 `1.409` | PASS |
| Case 10 100Hz SOL (xlsx) | 源 5.147270672023296 → `5.147` / 印刷 `5.147` | PASS |
| Case 10 100Hz SOL (log) | 源 5.147271000000001 → `5.147` / 印刷 `5.147` | PASS |
| Case 10 100Hz TL (xlsx) | 源 1.627381 → `1.627` / 印刷 `1.627` | PASS |
| Case 10 100Hz TL (log) | 源 1.627381 → `1.627` / 印刷 `1.627` | PASS |
| Case 10 Avg. SOL (xlsx) | 源 3.377542411908507 → `3.378` / 印刷 `3.378` | PASS |
| Case 10 Avg. SOL (log) | 源 3.377543 → `3.378` / 印刷 `3.378` | PASS |
| Case 10 Avg. TL (xlsx) | 源 1.178464 → `1.178` / 印刷 `1.178` | PASS |
| Case 10 Avg. TL (log) | 源 1.178464 → `1.178` / 印刷 `1.178` | PASS |
| Case 11 Dataset 名 | tex `W3` | PASS |
| Case 11 25Hz SOL (xlsx) | 源 5.667485436424613 → `5.667` / 印刷 `5.667` | PASS |
| Case 11 25Hz SOL (log) | 源 5.66748593 → `5.667` / 印刷 `5.667` | PASS |
| Case 11 25Hz TL (xlsx) | 源 1.996354 → `1.996` / 印刷 `1.996` | PASS |
| Case 11 25Hz TL (log) | 源 1.996354 → `1.996` / 印刷 `1.996` | PASS |
| Case 11 50Hz SOL (xlsx) | 源 5.145914969034493 → `5.146` / 印刷 `5.146` | PASS |
| Case 11 50Hz SOL (log) | 源 5.145914500000001 → `5.146` / 印刷 `5.146` | PASS |
| Case 11 50Hz TL (xlsx) | 源 1.076485 → `1.076` / 印刷 `1.076` | PASS |
| Case 11 50Hz TL (log) | 源 1.076485 → `1.076` / 印刷 `1.076` | PASS |
| Case 11 75Hz SOL (xlsx) | 源 12.25881576538086 → `12.259` / 印刷 `12.259` | PASS |
| Case 11 75Hz SOL (log) | 源 12.258818999999999 → `12.259` / 印刷 `12.259` | PASS |
| Case 11 75Hz TL (xlsx) | 源 1.765749 → `1.766` / 印刷 `1.766` | PASS |
| Case 11 75Hz TL (log) | 源 1.765749 → `1.766` / 印刷 `1.766` | PASS |
| Case 11 100Hz SOL (xlsx) | 源 20.117080397903912 → `20.117` / 印刷 `20.117` | PASS |
| Case 11 100Hz SOL (log) | 源 20.117077000000002 → `20.117` / 印刷 `20.117` | PASS |
| Case 11 100Hz TL (xlsx) | 源 2.570491 → `2.570` / 印刷 `2.570` | PASS |
| Case 11 100Hz TL (log) | 源 2.570491 → `2.570` / 印刷 `2.570` | PASS |
| Case 11 Avg. SOL (xlsx) | 源 10.79732421785593 → `10.797` / 印刷 `10.797` | PASS |
| Case 11 Avg. SOL (log) | 源 10.79733 → `10.797` / 印刷 `10.797` | PASS |
| Case 11 Avg. TL (xlsx) | 源 1.85227 → `1.852` / 印刷 `1.852` | PASS |
| Case 11 Avg. TL (log) | 源 1.85227 → `1.852` / 印刷 `1.852` | PASS |

## 6. Fig. 列引用正确性

> 每行的图号必须指向该案例自己的图与子图；同一尺度下矩形取 `-r` 子图、楔形取 `-w`，错配读者会看错图。同时确认被引 label 在 aux 里存在（否则排出 `??`）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 Fig. 列引用 | tex `\ref{fig:res-128}\subref{fig:res-128-r}` → ['fig:res-128', 'fig:res-128-r']，应为 `[fig:res-128, fig:res-128-r]` | PASS |
| label `fig:res-128` 已在 aux 注册 | 编号 `5` | PASS |
| label `fig:res-128-r` 已在 aux 注册 | 编号 `5a` | PASS |
| Case 4 Fig. 列引用 | tex `\ref{fig:res-256}\subref{fig:res-256-r}` → ['fig:res-256', 'fig:res-256-r']，应为 `[fig:res-256, fig:res-256-r]` | PASS |
| label `fig:res-256` 已在 aux 注册 | 编号 `6` | PASS |
| label `fig:res-256-r` 已在 aux 注册 | 编号 `6a` | PASS |
| Case 5 Fig. 列引用 | tex `\ref{fig:res-512}\subref{fig:res-512-r}` → ['fig:res-512', 'fig:res-512-r']，应为 `[fig:res-512, fig:res-512-r]` | PASS |
| label `fig:res-512` 已在 aux 注册 | 编号 `7` | PASS |
| label `fig:res-512-r` 已在 aux 注册 | 编号 `7a` | PASS |
| Case 9 Fig. 列引用 | tex `\ref{fig:res-128}\subref{fig:res-128-w}` → ['fig:res-128', 'fig:res-128-w']，应为 `[fig:res-128, fig:res-128-w]` | PASS |
| label `fig:res-128` 已在 aux 注册 | 编号 `5` | PASS |
| label `fig:res-128-w` 已在 aux 注册 | 编号 `5b` | PASS |
| Case 10 Fig. 列引用 | tex `\ref{fig:res-256}\subref{fig:res-256-w}` → ['fig:res-256', 'fig:res-256-w']，应为 `[fig:res-256, fig:res-256-w]` | PASS |
| label `fig:res-256` 已在 aux 注册 | 编号 `6` | PASS |
| label `fig:res-256-w` 已在 aux 注册 | 编号 `6b` | PASS |
| Case 11 Fig. 列引用 | tex `\ref{fig:res-512}\subref{fig:res-512-w}` → ['fig:res-512', 'fig:res-512-w']，应为 `[fig:res-512, fig:res-512-w]` | PASS |
| label `fig:res-512` 已在 aux 注册 | 编号 `7` | PASS |
| label `fig:res-512-w` 已在 aux 注册 | 编号 `7b` | PASS |

## 7. 几何分组小标题行

> 表内用两行 `\multicolumn{13}` 小标题分隔矩形/楔形；它们不是数据行（会被 ncol 过滤掉），但缺失会让 6 行混为一体。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 小标题行 `Rectangular waveguide` 存在 |  | PASS |
| `Rectangular waveguide` 组下辖案例 | 实得 [3, 4, 5]，应为 [3, 4, 5] | PASS |
| 小标题行 `Wedge waveguide` 存在 |  | PASS |
| `Wedge waveguide` 组下辖案例 | 实得 [9, 10, 11]，应为 [9, 10, 11] | PASS |

## 8. Avg. 列与四频均值自洽

> caption 声明 Avg. 为四频均值；四频样本数相等，故等权均值应等于 Overall 组。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 Avg. SOL = 四频均值 | 均值 `1.68829` / Overall `1.68829` | PASS |
| Case 3 Avg. TL = 四频均值 | 均值 `0.951194` / Overall `0.951194` | PASS |
| Case 4 Avg. SOL = 四频均值 | 均值 `3.77334` / Overall `3.77334` | PASS |
| Case 4 Avg. TL = 四频均值 | 均值 `1.36862` / Overall `1.36862` | PASS |
| Case 5 Avg. SOL = 四频均值 | 均值 `13.1638` / Overall `13.1638` | PASS |
| Case 5 Avg. TL = 四频均值 | 均值 `2.15712` / Overall `2.15712` | PASS |
| Case 9 Avg. SOL = 四频均值 | 均值 `2.12092` / Overall `2.12092` | PASS |
| Case 9 Avg. TL = 四频均值 | 均值 `0.899286` / Overall `0.899286` | PASS |
| Case 10 Avg. SOL = 四频均值 | 均值 `3.37754` / Overall `3.37754` | PASS |
| Case 10 Avg. TL = 四频均值 | 均值 `1.17846` / Overall `1.17846` | PASS |
| Case 11 Avg. SOL = 四频均值 | 均值 `10.7973` / Overall `10.7973` | PASS |
| Case 11 Avg. TL = 四频均值 | 均值 `1.85227` / Overall `1.85227` | PASS |

## 9. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 60 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 10. 正文引用精确性（4.3 节）

> 每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。只查①会漏掉正文与表格一起错的情形。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 Case 3 频均 Sol | 正文 `1.688` / 表格 `1.688` | PASS |
| 正文 Case 3 频均 Sol ← xlsx 源 | 源 1.6882909461855888 → `1.688` / 印刷 `1.688` | PASS |
| 正文 Case 9 频均 Sol | 正文 `2.121` / 表格 `2.121` | PASS |
| 正文 Case 9 频均 Sol ← xlsx 源 | 源 2.1209166909102346 → `2.121` / 印刷 `2.121` | PASS |
| 正文 Case 3 频均 TL | 正文 `0.951` / 表格 `0.951` | PASS |
| 正文 Case 3 频均 TL ← xlsx 源 | 源 0.9511941 → `0.951` / 印刷 `0.951` | PASS |
| 正文 Case 9 频均 TL | 正文 `0.899` / 表格 `0.899` | PASS |
| 正文 Case 9 频均 TL ← xlsx 源 | 源 0.899286 → `0.899` / 印刷 `0.899` | PASS |
| 正文 Case 4 频均 Sol | 正文 `3.773` / 表格 `3.773` | PASS |
| 正文 Case 4 频均 Sol ← xlsx 源 | 源 3.773339698091149 → `3.773` / 印刷 `3.773` | PASS |
| 正文 Case 5 频均 Sol | 正文 `13.164` / 表格 `13.164` | PASS |
| 正文 Case 5 频均 Sol ← xlsx 源 | 源 13.163763936609032 → `13.164` / 印刷 `13.164` | PASS |
| 正文 Case 4 频均 TL | 正文 `1.369` / 表格 `1.369` | PASS |
| 正文 Case 4 频均 TL ← xlsx 源 | 源 1.36862 → `1.369` / 印刷 `1.369` | PASS |
| 正文 Case 5 频均 TL | 正文 `2.157` / 表格 `2.157` | PASS |
| 正文 Case 5 频均 TL ← xlsx 源 | 源 2.157118 → `2.157` / 印刷 `2.157` | PASS |
| 正文 Case 11 频均 Sol | 正文 `10.797` / 表格 `10.797` | PASS |
| 正文 Case 11 频均 Sol ← xlsx 源 | 源 10.79732421785593 → `10.797` / 印刷 `10.797` | PASS |
| 正文 Case 11 频均 TL | 正文 `1.852` / 表格 `1.852` | PASS |
| 正文 Case 11 频均 TL ← xlsx 源 | 源 1.85227 → `1.852` / 印刷 `1.852` | PASS |
| 正文 Case 3 @50Hz TL | 正文 `0.516` / 表格 `0.516` | PASS |
| 正文 Case 3 @50Hz TL ← xlsx 源 | 源 0.516494 → `0.516` / 印刷 `0.516` | PASS |
| 正文 Case 3 @75Hz TL | 正文 `1.094` / 表格 `1.094` | PASS |
| 正文 Case 3 @75Hz TL ← xlsx 源 | 源 1.093897 → `1.094` / 印刷 `1.094` | PASS |
| 正文 Case 3 @100Hz TL | 正文 `1.490` / 表格 `1.490` | PASS |
| 正文 Case 3 @100Hz TL ← xlsx 源 | 源 1.489616 → `1.490` / 印刷 `1.490` | PASS |
| 正文 Case 9 @100Hz TL | 正文 `1.265` / 表格 `1.265` | PASS |
| 正文 Case 9 @100Hz TL ← xlsx 源 | 源 1.265287 → `1.265` / 印刷 `1.265` | PASS |

## 11. 正文派生倍数（印刷值口径）

> 派生倍数一律用**表格印刷值**相除，读者才能直接复算。用全精度源值回算会得到另一个数（如 2.268 变 2.267），此前 8.676/8.670 就是这么错的。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 矩形多频 512m/128m TL 倍数 = 2.268 | `2.157`/`0.951` = `2.268139` → `2.268` | PASS |
| 正文该倍数可定位 | tex 行 778 | PASS |

## 12. 正文趋势断言

> 正文断言“楔形在最大range反而略优”，须由表值支持。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 512m 处楔形 Sol < 矩形 Sol | W3 `10.797` < R3 `13.164` | PASS |
| 正文对比值 10.797 (Case 11) | 表格 `10.797` | PASS |
| 正文对比值 13.164 (Case 5) | 表格 `13.164` | PASS |

## X. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

