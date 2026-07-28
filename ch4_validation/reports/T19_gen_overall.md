# Table 19 — 泛化外推精度 R9/R10/W9/W10

- 对象：`tab:gen-overall`（Table 19）
- 结论：**PASS** — 118 通过 / 0 失败 / 0 警告，共 118 项
- 脚本：`ch4_validation/scripts/T19_gen_overall.py`
- 生成：2026-07-29 00:26:20

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:gen-overall}` 所在 table* 环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/Case39-42_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 39) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No39_R9/training_run/logs/full_run_20260720_153827.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 40) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No40_R10/training_run/logs/full_run_20260720_103428.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 41) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No41_W9/training_run/logs/full_run_20260720_204724.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 42) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No42_W10/training_run/logs/full_run_20260721_011504.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/Case39-42_数据汇总.xlsx | PASS |
| Case 39 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No39_R9/training_run/logs/full_run_20260720_153827.log | PASS |
| Case 40 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No40_R10/training_run/logs/full_run_20260720_103428.log | PASS |
| Case 41 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No41_W9/training_run/logs/full_run_20260720_204724.log | PASS |
| Case 42 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No42_W10/training_run/logs/full_run_20260721_011504.log | PASS |
| tex 表格环境可定位且确实包住 label | `tab:gen-overall`，长度 1725 | PASS |
| tex 数据行数 = 4 | 实得 4 | PASS |
| tex 行 No. 覆盖 39-42 | [39, 40, 41, 42] | PASS |

## 3. best epoch 一致性

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 39 best epoch | xlsx `168` / log `168` | PASS |
| Case 39 日志含『评估 Epoch 168』块 | 轮次 168 | PASS |
| Case 40 best epoch | xlsx `168` / log `168` | PASS |
| Case 40 日志含『评估 Epoch 168』块 | 轮次 168 | PASS |
| Case 41 best epoch | xlsx `184` / log `184` | PASS |
| Case 41 日志含『评估 Epoch 184』块 | 轮次 184 | PASS |
| Case 42 best epoch | xlsx `197` / log `197` | PASS |
| Case 42 日志含『评估 Epoch 197』块 | 轮次 197 | PASS |

## 4. 双渠道交叉验证（xlsx vs log，同一 best epoch）

> 日志侧取『评估 Epoch N 完成』块（测试集），非『训练』块；Sol 由 `(损失 − w_prior×prior)/w_rel` 现场算，权重逐轮解析。

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 39 Overall SOL | `62.751567715571994` / `62.75156` | PASS |
| Case 39 Overall TL | `3.642254` / `3.642254` | PASS |
| Case 39 25 SOL | `55.95634681069189` / `55.9563487` | PASS |
| Case 39 25 TL | `2.436003` / `2.436003` | PASS |
| Case 39 50 SOL | `48.89363205681245` / `48.8936364` | PASS |
| Case 39 50 TL | `3.349023` / `3.349023` | PASS |
| Case 39 75 SOL | `95.4765108310514` / `95.4765096` | PASS |
| Case 39 75 TL | `4.302736` / `4.302736` | PASS |
| Case 39 100 SOL | `50.67978468206194` / `50.679787600000004` | PASS |
| Case 39 100 TL | `4.481253` / `4.481253` | PASS |
| Case 40 Overall SOL | `51.73777799225516` / `51.73778` | PASS |
| Case 40 Overall TL | `2.966459` / `2.966459` | PASS |
| Case 40 25 SOL | `75.54511725902556` / `75.545114` | PASS |
| Case 40 25 TL | `2.027404` / `2.027404` | PASS |
| Case 40 50 SOL | `35.23553897523218` / `35.2355417` | PASS |
| Case 40 50 TL | `2.456988` / `2.456988` | PASS |
| Case 40 75 SOL | `66.9465112603373` / `66.9465138` | PASS |
| Case 40 75 TL | `3.629947` / `3.629947` | PASS |
| Case 40 100 SOL | `29.22393785168728` / `29.223934200000002` | PASS |
| Case 40 100 TL | `3.751497` / `3.751497` | PASS |
| Case 41 Overall SOL | `313.69290500879293` / `313.6929` | PASS |
| Case 41 Overall TL | `4.346686` / `4.346686` | PASS |
| Case 41 25 SOL | `686.2264954381518` / `686.226462` | PASS |
| Case 41 25 TL | `2.905493` / `2.905493` | PASS |
| Case 41 50 SOL | `205.5555416478051` / `205.555589` | PASS |
| Case 41 50 TL | `3.832826` / `3.832826` | PASS |
| Case 41 75 SOL | `213.9502320852545` / `213.950199` | PASS |
| Case 41 75 TL | `5.601251` / `5.601251` | PASS |
| Case 41 100 SOL | `149.0393105066485` / `149.039301` | PASS |
| Case 41 100 TL | `5.047175` / `5.047175` | PASS |
| Case 42 Overall SOL | `325.1775051984522` / `325.17749999999995` | PASS |
| Case 42 Overall TL | `4.437186` / `4.437186` | PASS |
| Case 42 25 SOL | `827.7104049921036` / `827.7104059999999` | PASS |
| Case 42 25 TL | `4.219337` / `4.219337` | PASS |
| Case 42 50 SOL | `178.5856323937575` / `178.585629` | PASS |
| Case 42 50 TL | `3.78341` / `3.78341` | PASS |
| Case 42 75 SOL | `172.925657282273` / `172.92570099999998` | PASS |
| Case 42 75 TL | `4.741251` / `4.741251` | PASS |
| Case 42 100 SOL | `121.4883125697573` / `121.48830600000001` | PASS |
| Case 42 100 TL | `5.004744` / `5.004744` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Data, Extrap.region, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。Avg. 对应 xlsx/日志的 Overall 组。日志渠道的一致性已在第 4 节双渠道验证中确认，此处仅比对 xlsx。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 39 Data 名 | tex `R9` | PASS |
| Case 39 25Hz SOL (xlsx) | 源 55.95634681069189 → `55.956` / 印刷 `55.956` | PASS |
| Case 39 25Hz TL (xlsx) | 源 2.436003 → `2.436` / 印刷 `2.436` | PASS |
| Case 39 50Hz SOL (xlsx) | 源 48.89363205681245 → `48.894` / 印刷 `48.894` | PASS |
| Case 39 50Hz TL (xlsx) | 源 3.349023 → `3.349` / 印刷 `3.349` | PASS |
| Case 39 75Hz SOL (xlsx) | 源 95.4765108310514 → `95.477` / 印刷 `95.477` | PASS |
| Case 39 75Hz TL (xlsx) | 源 4.302736 → `4.303` / 印刷 `4.303` | PASS |
| Case 39 100Hz SOL (xlsx) | 源 50.67978468206194 → `50.680` / 印刷 `50.680` | PASS |
| Case 39 100Hz TL (xlsx) | 源 4.481253 → `4.481` / 印刷 `4.481` | PASS |
| Case 39 Avg. SOL (xlsx) | 源 62.751567715571994 → `62.752` / 印刷 `62.752` | PASS |
| Case 39 Avg. TL (xlsx) | 源 3.642254 → `3.642` / 印刷 `3.642` | PASS |
| Case 40 Data 名 | tex `R10` | PASS |
| Case 40 25Hz SOL (xlsx) | 源 75.54511725902556 → `75.545` / 印刷 `75.545` | PASS |
| Case 40 25Hz TL (xlsx) | 源 2.027404 → `2.027` / 印刷 `2.027` | PASS |
| Case 40 50Hz SOL (xlsx) | 源 35.23553897523218 → `35.236` / 印刷 `35.236` | PASS |
| Case 40 50Hz TL (xlsx) | 源 2.456988 → `2.457` / 印刷 `2.457` | PASS |
| Case 40 75Hz SOL (xlsx) | 源 66.9465112603373 → `66.947` / 印刷 `66.947` | PASS |
| Case 40 75Hz TL (xlsx) | 源 3.629947 → `3.630` / 印刷 `3.630` | PASS |
| Case 40 100Hz SOL (xlsx) | 源 29.22393785168728 → `29.224` / 印刷 `29.224` | PASS |
| Case 40 100Hz TL (xlsx) | 源 3.751497 → `3.751` / 印刷 `3.751` | PASS |
| Case 40 Avg. SOL (xlsx) | 源 51.73777799225516 → `51.738` / 印刷 `51.738` | PASS |
| Case 40 Avg. TL (xlsx) | 源 2.966459 → `2.966` / 印刷 `2.966` | PASS |
| Case 41 Data 名 | tex `W9` | PASS |
| Case 41 25Hz SOL (xlsx) | 源 686.2264954381518 → `686.226` / 印刷 `686.226` | PASS |
| Case 41 25Hz TL (xlsx) | 源 2.905493 → `2.905` / 印刷 `2.905` | PASS |
| Case 41 50Hz SOL (xlsx) | 源 205.5555416478051 → `205.556` / 印刷 `205.556` | PASS |
| Case 41 50Hz TL (xlsx) | 源 3.832826 → `3.833` / 印刷 `3.833` | PASS |
| Case 41 75Hz SOL (xlsx) | 源 213.9502320852545 → `213.950` / 印刷 `213.950` | PASS |
| Case 41 75Hz TL (xlsx) | 源 5.601251 → `5.601` / 印刷 `5.601` | PASS |
| Case 41 100Hz SOL (xlsx) | 源 149.0393105066485 → `149.039` / 印刷 `149.039` | PASS |
| Case 41 100Hz TL (xlsx) | 源 5.047175 → `5.047` / 印刷 `5.047` | PASS |
| Case 41 Avg. SOL (xlsx) | 源 313.69290500879293 → `313.693` / 印刷 `313.693` | PASS |
| Case 41 Avg. TL (xlsx) | 源 4.346686 → `4.347` / 印刷 `4.347` | PASS |
| Case 42 Data 名 | tex `W10` | PASS |
| Case 42 25Hz SOL (xlsx) | 源 827.7104049921036 → `827.710` / 印刷 `827.710` | PASS |
| Case 42 25Hz TL (xlsx) | 源 4.219337 → `4.219` / 印刷 `4.219` | PASS |
| Case 42 50Hz SOL (xlsx) | 源 178.5856323937575 → `178.586` / 印刷 `178.586` | PASS |
| Case 42 50Hz TL (xlsx) | 源 3.78341 → `3.783` / 印刷 `3.783` | PASS |
| Case 42 75Hz SOL (xlsx) | 源 172.925657282273 → `172.926` / 印刷 `172.926` | PASS |
| Case 42 75Hz TL (xlsx) | 源 4.741251 → `4.741` / 印刷 `4.741` | PASS |
| Case 42 100Hz SOL (xlsx) | 源 121.4883125697573 → `121.488` / 印刷 `121.488` | PASS |
| Case 42 100Hz TL (xlsx) | 源 5.004744 → `5.005` / 印刷 `5.005` | PASS |
| Case 42 Avg. SOL (xlsx) | 源 325.1775051984522 → `325.178` / 印刷 `325.178` | PASS |
| Case 42 Avg. TL (xlsx) | 源 4.437186 → `4.437` / 印刷 `4.437` | PASS |

## 6. Avg. 列与四频均值自洽

> caption 声明 Avg. 为四频均值；四频样本数相等，故等权均值应等于 Overall 组。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 39 Avg. SOL = 四频均值 | 均值 `62.7516` / Overall `62.7516` | PASS |
| Case 39 Avg. TL = 四频均值 | 均值 `3.64225` / Overall `3.64225` | PASS |
| Case 40 Avg. SOL = 四频均值 | 均值 `51.7378` / Overall `51.7378` | PASS |
| Case 40 Avg. TL = 四频均值 | 均值 `2.96646` / Overall `2.96646` | PASS |
| Case 41 Avg. SOL = 四频均值 | 均值 `313.693` / Overall `313.693` | PASS |
| Case 41 Avg. TL = 四频均值 | 均值 `4.34669` / Overall `4.34669` | PASS |
| Case 42 Avg. SOL = 四频均值 | 均值 `325.178` / Overall `325.178` | PASS |
| Case 42 Avg. TL = 四频均值 | 均值 `4.43719` / Overall `4.43719` | PASS |

## 7. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 40 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 8. 正文引用精确性（4.7 节）

> 每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。只查①会漏掉正文与表格一起错的情形。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 R9 频均 TL | 正文 `3.642` / 表格 `3.642` | PASS |
| 正文 R9 频均 TL <- xlsx 源 | 源 3.642254 → `3.642` / 印刷 `3.642` | PASS |
| 正文 R10 频均 TL | 正文 `2.966` / 表格 `2.966` | PASS |
| 正文 R10 频均 TL <- xlsx 源 | 源 2.966459 → `2.966` / 印刷 `2.966` | PASS |
| 正文 W9 频均 TL | 正文 `4.347` / 表格 `4.347` | PASS |
| 正文 W9 频均 TL <- xlsx 源 | 源 4.346686 → `4.347` / 印刷 `4.347` | PASS |
| 正文 W10 频均 TL | 正文 `4.437` / 表格 `4.437` | PASS |
| 正文 W10 频均 TL <- xlsx 源 | 源 4.437186 → `4.437` / 印刷 `4.437` | PASS |

## X. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

