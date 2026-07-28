# Table 16 — 消融逐频结果 W1

- 对象：`tab:abl-wedge`（Table 16）
- 结论：**PASS** — 118 通过 / 0 失败 / 0 警告，共 118 项
- 脚本：`ch4_validation/scripts/T16_abl_wedge.py`
- 生成：2026-07-29 01:07:00

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:abl-wedge}` 所在 table* 环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/Case25-32_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 29) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No29_W1_Full/training_run/logs/full_run_20260715_023150.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 30) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No30_W1_no_prior/training_run/logs/full_run_20260715_023311.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 31) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No31_W1_no_graph/training_run/logs/full_run_20260715_082131.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 32) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No32_W1_no_prior_loss/training_run/logs/full_run_20260715_023318.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/Case25-32_数据汇总.xlsx | PASS |
| Case 29 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No29_W1_Full/training_run/logs/full_run_20260715_023150.log | PASS |
| Case 30 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No30_W1_no_prior/training_run/logs/full_run_20260715_023311.log | PASS |
| Case 31 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No31_W1_no_graph/training_run/logs/full_run_20260715_082131.log | PASS |
| Case 32 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No32_W1_no_prior_loss/training_run/logs/full_run_20260715_023318.log | PASS |
| tex 表格环境可定位且确实包住 label | `tab:abl-wedge`，长度 1519 | PASS |
| tex 数据行数 = 4 | 实得 4 | PASS |
| tex 行 No. 覆盖 15-19 | [29, 30, 31, 32] | PASS |

## 3. best epoch 一致性

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 29 best epoch | xlsx `197` / log `197` | PASS |
| Case 29 日志含『评估 Epoch 197』块 | 轮次 197 | PASS |
| Case 30 best epoch | xlsx `200` / log `200` | PASS |
| Case 30 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |
| Case 31 best epoch | xlsx `199` / log `199` | PASS |
| Case 31 日志含『评估 Epoch 199』块 | 轮次 199 | PASS |
| Case 32 best epoch | xlsx `199` / log `199` | PASS |
| Case 32 日志含『评估 Epoch 199』块 | 轮次 199 | PASS |

## 4. 双渠道交叉验证（xlsx vs log，同一 best epoch）

> 日志侧取『评估 Epoch N 完成』块（测试集），非『训练』块；Sol 由 `(损失 − w_prior×prior)/w_rel` 现场算，权重逐轮解析。

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 29 Overall SOL | `21.64506972767413` / `21.645069999999997` | PASS |
| Case 29 Overall TL | `1.936008` / `1.936008` | PASS |
| Case 29 25 SOL | `33.35254043340683` / `33.3525412` | PASS |
| Case 29 25 TL | `1.291144` / `1.291144` | PASS |
| Case 29 50 SOL | `0.7033266650978476` / `0.7033267` | PASS |
| Case 29 50 TL | `0.7219688` / `0.7219688` | PASS |
| Case 29 75 SOL | `19.44934674538672` / `19.4493459` | PASS |
| Case 29 75 TL | `2.140294` / `2.140294` | PASS |
| Case 29 100 SOL | `33.0750647932291` / `33.0750678` | PASS |
| Case 29 100 TL | `3.590624` / `3.590624` | PASS |
| Case 30 Overall SOL | `3022.704696655274` / `3022.705` | PASS |
| Case 30 Overall TL | `48.79683` / `48.79683` | PASS |
| Case 30 25 SOL | `9691.231346130371` / `9691.231` | PASS |
| Case 30 25 TL | `9.445384` / `9.445384` | PASS |
| Case 30 50 SOL | `1386.380329728127` / `1386.3802799999999` | PASS |
| Case 30 50 TL | `55.7952` / `55.7952` | PASS |
| Case 30 75 SOL | `685.3322699666023` / `685.3322770000001` | PASS |
| Case 30 75 TL | `83.00855` / `83.00855` | PASS |
| Case 30 100 SOL | `327.8753321617842` / `327.875372` | PASS |
| Case 30 100 TL | `46.9382` / `46.9382` | PASS |
| Case 31 Overall SOL | `60.33936939202249` / `60.339369999999995` | PASS |
| Case 31 Overall TL | `2.443006` / `2.443006` | PASS |
| Case 31 25 SOL | `162.56497632712131` / `162.56494999999998` | PASS |
| Case 31 25 TL | `2.037057` / `2.037057` | PASS |
| Case 31 50 SOL | `1.3072183821350338` / `1.3072188200000001` | PASS |
| Case 31 50 TL | `0.8516294` / `0.8516294` | PASS |
| Case 31 75 SOL | `21.83450921438635` / `21.834504900000002` | PASS |
| Case 31 75 TL | `2.342786` / `2.342786` | PASS |
| Case 31 100 SOL | `55.65077951177954` / `55.650782199999995` | PASS |
| Case 31 100 TL | `4.540552` / `4.540552` | PASS |
| Case 32 Overall SOL | `37.9284918308258` / `37.928490000000004` | PASS |
| Case 32 Overall TL | `2.533244` / `2.533244` | PASS |
| Case 32 25 SOL | `57.36030340194702` / `57.360299999999995` | PASS |
| Case 32 25 TL | `1.577166` / `1.577166` | PASS |
| Case 32 50 SOL | `0.9959153831005096` / `0.9959154` | PASS |
| Case 32 50 TL | `0.7516175` / `0.7516175` | PASS |
| Case 32 75 SOL | `32.38130211830139` / `32.3813` | PASS |
| Case 32 75 TL | `2.753591` / `2.753591` | PASS |
| Case 32 100 SOL | `60.97644567489624` / `60.97645` | PASS |
| Case 32 100 TL | `5.050601` / `5.050601` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Variant, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)。Avg. 对应 xlsx/日志的 Overall 组。本表无 Fig. 列。日志渠道的一致性已在第 4 节双渠道验证中确认，此处仅比对 xlsx。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 29 Variant 名 | tex `Full model` | PASS |
| Case 29 25Hz SOL (xlsx) | 源 33.35254043340683 → `33.353` / 印刷 `33.353` | PASS |
| Case 29 25Hz TL (xlsx) | 源 1.291144 → `1.291` / 印刷 `1.291` | PASS |
| Case 29 50Hz SOL (xlsx) | 源 0.7033266650978476 → `0.703` / 印刷 `0.703` | PASS |
| Case 29 50Hz TL (xlsx) | 源 0.7219688 → `0.722` / 印刷 `0.722` | PASS |
| Case 29 75Hz SOL (xlsx) | 源 19.44934674538672 → `19.449` / 印刷 `19.449` | PASS |
| Case 29 75Hz TL (xlsx) | 源 2.140294 → `2.140` / 印刷 `2.140` | PASS |
| Case 29 100Hz SOL (xlsx) | 源 33.0750647932291 → `33.075` / 印刷 `33.075` | PASS |
| Case 29 100Hz TL (xlsx) | 源 3.590624 → `3.591` / 印刷 `3.591` | PASS |
| Case 29 Avg. SOL (xlsx) | 源 21.64506972767413 → `21.645` / 印刷 `21.645` | PASS |
| Case 29 Avg. TL (xlsx) | 源 1.936008 → `1.936` / 印刷 `1.936` | PASS |
| Case 30 Variant 名 | tex `w/o physics prior` | PASS |
| Case 30 25Hz SOL (xlsx) | 源 9691.231346130371 → `9691.231` / 印刷 `9691.231` | PASS |
| Case 30 25Hz TL (xlsx) | 源 9.445384 → `9.445` / 印刷 `9.445` | PASS |
| Case 30 50Hz SOL (xlsx) | 源 1386.380329728127 → `1386.380` / 印刷 `1386.380` | PASS |
| Case 30 50Hz TL (xlsx) | 源 55.7952 → `55.795` / 印刷 `55.795` | PASS |
| Case 30 75Hz SOL (xlsx) | 源 685.3322699666023 → `685.332` / 印刷 `685.332` | PASS |
| Case 30 75Hz TL (xlsx) | 源 83.00855 → `83.009` / 印刷 `83.009` | PASS |
| Case 30 100Hz SOL (xlsx) | 源 327.8753321617842 → `327.875` / 印刷 `327.875` | PASS |
| Case 30 100Hz TL (xlsx) | 源 46.9382 → `46.938` / 印刷 `46.938` | PASS |
| Case 30 Avg. SOL (xlsx) | 源 3022.704696655274 → `3022.705` / 印刷 `3022.705` | PASS |
| Case 30 Avg. TL (xlsx) | 源 48.79683 → `48.797` / 印刷 `48.797` | PASS |
| Case 31 Variant 名 | tex `w/o graph correction` | PASS |
| Case 31 25Hz SOL (xlsx) | 源 162.56497632712131 → `162.565` / 印刷 `162.565` | PASS |
| Case 31 25Hz TL (xlsx) | 源 2.037057 → `2.037` / 印刷 `2.037` | PASS |
| Case 31 50Hz SOL (xlsx) | 源 1.3072183821350338 → `1.307` / 印刷 `1.307` | PASS |
| Case 31 50Hz TL (xlsx) | 源 0.8516294 → `0.852` / 印刷 `0.852` | PASS |
| Case 31 75Hz SOL (xlsx) | 源 21.83450921438635 → `21.835` / 印刷 `21.835` | PASS |
| Case 31 75Hz TL (xlsx) | 源 2.342786 → `2.343` / 印刷 `2.343` | PASS |
| Case 31 100Hz SOL (xlsx) | 源 55.65077951177954 → `55.651` / 印刷 `55.651` | PASS |
| Case 31 100Hz TL (xlsx) | 源 4.540552 → `4.541` / 印刷 `4.541` | PASS |
| Case 31 Avg. SOL (xlsx) | 源 60.33936939202249 → `60.339` / 印刷 `60.339` | PASS |
| Case 31 Avg. TL (xlsx) | 源 2.443006 → `2.443` / 印刷 `2.443` | PASS |
| Case 32 Variant 名 | tex `w/o prior supervision` | PASS |
| Case 32 25Hz SOL (xlsx) | 源 57.36030340194702 → `57.360` / 印刷 `57.360` | PASS |
| Case 32 25Hz TL (xlsx) | 源 1.577166 → `1.577` / 印刷 `1.577` | PASS |
| Case 32 50Hz SOL (xlsx) | 源 0.9959153831005096 → `0.996` / 印刷 `0.996` | PASS |
| Case 32 50Hz TL (xlsx) | 源 0.7516175 → `0.752` / 印刷 `0.752` | PASS |
| Case 32 75Hz SOL (xlsx) | 源 32.38130211830139 → `32.381` / 印刷 `32.381` | PASS |
| Case 32 75Hz TL (xlsx) | 源 2.753591 → `2.754` / 印刷 `2.754` | PASS |
| Case 32 100Hz SOL (xlsx) | 源 60.97644567489624 → `60.976` / 印刷 `60.976` | PASS |
| Case 32 100Hz TL (xlsx) | 源 5.050601 → `5.051` / 印刷 `5.051` | PASS |
| Case 32 Avg. SOL (xlsx) | 源 37.9284918308258 → `37.928` / 印刷 `37.928` | PASS |
| Case 32 Avg. TL (xlsx) | 源 2.533244 → `2.533` / 印刷 `2.533` | PASS |

## 6. Avg. 列与四频均值自洽

> caption 声明 Avg. 为四频均值；四频样本数相等，故等权均值应等于 Overall 组。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 29 Avg. SOL = 四频均值 | 均值 `21.6451` / Overall `21.6451` | PASS |
| Case 29 Avg. TL = 四频均值 | 均值 `1.93601` / Overall `1.93601` | PASS |
| Case 30 Avg. SOL = 四频均值 | 均值 `3022.7` / Overall `3022.7` | PASS |
| Case 30 Avg. TL = 四频均值 | 均值 `48.7968` / Overall `48.7968` | PASS |
| Case 31 Avg. SOL = 四频均值 | 均值 `60.3394` / Overall `60.3394` | PASS |
| Case 31 Avg. TL = 四频均值 | 均值 `2.44301` / Overall `2.44301` | PASS |
| Case 32 Avg. SOL = 四频均值 | 均值 `37.9285` / Overall `37.9285` | PASS |
| Case 32 Avg. TL = 四频均值 | 均值 `2.53324` / Overall `2.53324` | PASS |

## 7. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 40 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 8. 正文引用精确性（4.5 节）

> 每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。只查①会漏掉正文与表格一起错的情形。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 Case 29 Full model 频均 Sol | 正文 `21.645` / 表格 `21.645` | PASS |
| 正文 Case 29 Full model 频均 Sol <- xlsx 源 | 源 21.64506972767413 → `21.645` / 印刷 `21.645` | PASS |
| 正文 Case 29 Full model 频均 TL | 正文 `1.936` / 表格 `1.936` | PASS |
| 正文 Case 29 Full model 频均 TL <- xlsx 源 | 源 1.936008 → `1.936` / 印刷 `1.936` | PASS |
| 正文 Case 30 w/o prior 频均 Sol | 正文 `3022.705` / 表格 `3022.705` | PASS |
| 正文 Case 30 w/o prior 频均 Sol <- xlsx 源 | 源 3022.704696655274 → `3022.705` / 印刷 `3022.705` | PASS |
| 正文 Case 30 w/o prior 频均 TL | 正文 `48.797` / 表格 `48.797` | PASS |
| 正文 Case 30 w/o prior 频均 TL <- xlsx 源 | 源 48.79683 → `48.797` / 印刷 `48.797` | PASS |

## X. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

