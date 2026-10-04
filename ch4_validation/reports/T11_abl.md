# Table 11 — 消融逐频结果，矩形与楔形分块同表

- 对象：`tab:abl`（Table 11）
- 结论：**PASS** — 343 通过 / 0 失败 / 1 警告，共 344 项
- 脚本：`ch4_validation/scripts/T11_abl.py`
- 生成：2026-10-04 23:07:15

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{tab:abl}` 所在环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/Case25-32_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 25) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No25_R1_Full/training_run/logs/full_run_20260712_150041.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 26) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No26_R1_no_prior/training_run/logs/full_run_20260713_025215.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 27) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No27_R1_no_graph/training_run/logs/full_run_20260712_193334.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 28) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No28_R1_no_prior_loss/training_run/logs/full_run_20260712_150158.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 29) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No29_W1_Full/training_run/logs/full_run_20260715_023150.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 30) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No30_W1_no_prior/training_run/logs/full_run_20260715_023311.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 31) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No31_W1_no_graph/training_run/logs/full_run_20260715_082131.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 32) | `Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No32_W1_no_prior_loss/training_run/logs/full_run_20260715_023318.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/Case25-32_数据汇总.xlsx | PASS |
| Case 25 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No25_R1_Full/training_run/logs/full_run_20260712_150041.log | PASS |
| Case 26 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No26_R1_no_prior/training_run/logs/full_run_20260713_025215.log | PASS |
| Case 27 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No27_R1_no_graph/training_run/logs/full_run_20260712_193334.log | PASS |
| Case 28 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No28_R1_no_prior_loss/training_run/logs/full_run_20260712_150158.log | PASS |
| Case 29 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No29_W1_Full/training_run/logs/full_run_20260715_023150.log | PASS |
| Case 30 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No30_W1_no_prior/training_run/logs/full_run_20260715_023311.log | PASS |
| Case 31 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No31_W1_no_graph/training_run/logs/full_run_20260715_082131.log | PASS |
| Case 32 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No32_W1_no_prior_loss/training_run/logs/full_run_20260715_023318.log | PASS |
| tex 表格环境可定位且确实包住 label | 长度 2296 | PASS |

## 1. 本表 tabular 的定位

> R1 把多张表绑进同一个 figure* 浮动体，`table_env()` 可能解析到邻居的 tabular；本表一律用 `table_body_of()` 取 label 自己的表体。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| label 之后可定位到本表 tabular | tabular*=True，长度 1736 | PASS |
| 数据行数 = 8（两几何各 4 行） | 实得 8 | PASS |
| 加粗掩码与数据行同形 | 8 / 8 | PASS |
| 两个 \multicolumn{12} 块头行（矩形 / 楔形） | 实得 2 | PASS |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 行 No. 覆盖 25-28 与 29-32 | [25, 26, 27, 28, 29, 30, 31, 32] | PASS |
| Case 25 落在矩形块且 Variant 名相符 | tex `Full model` / 期望 `Full model` | PASS |
| Case 26 落在矩形块且 Variant 名相符 | tex `w/o physics prior` / 期望 `w/o physics prior` | PASS |
| Case 27 落在矩形块且 Variant 名相符 | tex `w/o graph correction` / 期望 `w/o graph correction` | PASS |
| Case 28 落在矩形块且 Variant 名相符 | tex `w/o prior supervision` / 期望 `w/o prior supervision` | PASS |
| Case 29 落在楔形块且 Variant 名相符 | tex `Full model` / 期望 `Full model` | PASS |
| Case 30 落在楔形块且 Variant 名相符 | tex `w/o physics prior` / 期望 `w/o physics prior` | PASS |
| Case 31 落在楔形块且 Variant 名相符 | tex `w/o graph correction` / 期望 `w/o graph correction` | PASS |
| Case 32 落在楔形块且 Variant 名相符 | tex `w/o prior supervision` / 期望 `w/o prior supervision` | PASS |
| 行序为矩形块 25-28 后接楔形块 29-32 | [25, 26, 27, 28, 29, 30, 31, 32] | PASS |

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
| Case 29 best epoch | xlsx `197` / log `197` | PASS |
| Case 29 日志含『评估 Epoch 197』块 | 轮次 197 | PASS |
| Case 30 best epoch | xlsx `200` / log `200` | PASS |
| Case 30 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |
| Case 31 best epoch | xlsx `199` / log `199` | PASS |
| Case 31 日志含『评估 Epoch 199』块 | 轮次 199 | PASS |
| Case 32 best epoch | xlsx `199` / log `199` | PASS |
| Case 32 日志含『评估 Epoch 199』块 | 轮次 199 | PASS |

## 4. 双渠道交叉验证（xlsx vs log）

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 25 25Hz SOL | `16.63692949805409` / `16.6369326` | PASS |
| Case 25 25Hz TL | `1.377714` / `1.377714` | PASS |
| Case 25 50Hz SOL | `0.5120271787745878` / `0.51202722` | PASS |
| Case 25 50Hz TL | `0.6034657` / `0.6034657` | PASS |
| Case 25 75Hz SOL | `10.12754489202052` / `10.1275455` | PASS |
| Case 25 75Hz TL | `1.990745` / `1.990745` | PASS |
| Case 25 100Hz SOL | `18.65477762185037` / `18.6547783` | PASS |
| Case 25 100Hz TL | `3.673548` / `3.673548` | PASS |
| Case 25 Avg. SOL | `11.48282000795007` / `11.48282` | PASS |
| Case 25 Avg. TL | `1.911368` / `1.911368` | PASS |
| Case 26 25Hz SOL | `1563.083946704865` / `1563.0834799999998` | PASS |
| Case 26 25Hz TL | `22.93166` / `22.93166` | PASS |
| Case 26 50Hz SOL | `479.50402945280075` / `479.50399300000004` | PASS |
| Case 26 50Hz TL | `32.71898` / `32.71898` | PASS |
| Case 26 75Hz SOL | `424.60011579096323` / `424.6001` | PASS |
| Case 26 75Hz TL | `46.46738` / `46.46738` | PASS |
| Case 26 100Hz SOL | `129.5851467177272` / `129.585123` | PASS |
| Case 26 100Hz TL | `53.08328` / `53.08328` | PASS |
| Case 26 Avg. SOL | `649.1932973265648` / `649.1932999999999` | PASS |
| Case 26 Avg. TL | `38.80033` / `38.80033` | PASS |
| Case 27 25Hz SOL | `10.36997995106504` / `10.369980199999999` | PASS |
| Case 27 25Hz TL | `1.087888` / `1.087888` | PASS |
| Case 27 50Hz SOL | `0.5764913483290002` / `0.576491387` | PASS |
| Case 27 50Hz TL | `0.630979` / `0.630979` | PASS |
| Case 27 75Hz SOL | `19.53623965382576` / `19.5362376` | PASS |
| Case 27 75Hz TL | `2.559839` / `2.559839` | PASS |
| Case 27 100Hz SOL | `22.92125532403589` / `22.921257500000003` | PASS |
| Case 27 100Hz TL | `4.544477` / `4.544477` | PASS |
| Case 27 Avg. SOL | `13.350991916377101` / `13.35099` | PASS |
| Case 27 Avg. TL | `2.205796` / `2.205796` | PASS |
| Case 28 25Hz SOL | `3.189601749181748` / `3.189602` | PASS |
| Case 28 25Hz TL | `0.7414964` / `0.7414964` | PASS |
| Case 28 50Hz SOL | `0.5421166773885489` / `0.5421167` | PASS |
| Case 28 50Hz TL | `0.629636` / `0.629636` | PASS |
| Case 28 75Hz SOL | `19.97445821762085` / `19.97446` | PASS |
| Case 28 75Hz TL | `2.609463` / `2.609463` | PASS |
| Case 28 100Hz SOL | `21.54092490673066` / `21.540919999999996` | PASS |
| Case 28 100Hz TL | `4.309467` / `4.309467` | PASS |
| Case 28 Avg. SOL | `11.31177544593811` / `11.31178` | PASS |
| Case 28 Avg. TL | `2.072516` / `2.072516` | PASS |
| Case 29 25Hz SOL | `33.35254043340683` / `33.3525412` | PASS |
| Case 29 25Hz TL | `1.291144` / `1.291144` | PASS |
| Case 29 50Hz SOL | `0.7033266650978476` / `0.7033267` | PASS |
| Case 29 50Hz TL | `0.7219688` / `0.7219688` | PASS |
| Case 29 75Hz SOL | `19.44934674538672` / `19.4493459` | PASS |
| Case 29 75Hz TL | `2.140294` / `2.140294` | PASS |
| Case 29 100Hz SOL | `33.0750647932291` / `33.0750678` | PASS |
| Case 29 100Hz TL | `3.590624` / `3.590624` | PASS |
| Case 29 Avg. SOL | `21.64506972767413` / `21.645069999999997` | PASS |
| Case 29 Avg. TL | `1.936008` / `1.936008` | PASS |
| Case 30 25Hz SOL | `9691.231346130371` / `9691.231` | PASS |
| Case 30 25Hz TL | `9.445384` / `9.445384` | PASS |
| Case 30 50Hz SOL | `1386.380329728127` / `1386.3802799999999` | PASS |
| Case 30 50Hz TL | `55.7952` / `55.7952` | PASS |
| Case 30 75Hz SOL | `685.3322699666023` / `685.3322770000001` | PASS |
| Case 30 75Hz TL | `83.00855` / `83.00855` | PASS |
| Case 30 100Hz SOL | `327.8753321617842` / `327.875372` | PASS |
| Case 30 100Hz TL | `46.9382` / `46.9382` | PASS |
| Case 30 Avg. SOL | `3022.704696655274` / `3022.705` | PASS |
| Case 30 Avg. TL | `48.79683` / `48.79683` | PASS |
| Case 31 25Hz SOL | `162.56497632712131` / `162.56494999999998` | PASS |
| Case 31 25Hz TL | `2.037057` / `2.037057` | PASS |
| Case 31 50Hz SOL | `1.3072183821350338` / `1.3072188200000001` | PASS |
| Case 31 50Hz TL | `0.8516294` / `0.8516294` | PASS |
| Case 31 75Hz SOL | `21.83450921438635` / `21.834504900000002` | PASS |
| Case 31 75Hz TL | `2.342786` / `2.342786` | PASS |
| Case 31 100Hz SOL | `55.65077951177954` / `55.650782199999995` | PASS |
| Case 31 100Hz TL | `4.540552` / `4.540552` | PASS |
| Case 31 Avg. SOL | `60.33936939202249` / `60.339369999999995` | PASS |
| Case 31 Avg. TL | `2.443006` / `2.443006` | PASS |
| Case 32 25Hz SOL | `57.36030340194702` / `57.360299999999995` | PASS |
| Case 32 25Hz TL | `1.577166` / `1.577166` | PASS |
| Case 32 50Hz SOL | `0.9959153831005096` / `0.9959154` | PASS |
| Case 32 50Hz TL | `0.7516175` / `0.7516175` | PASS |
| Case 32 75Hz SOL | `32.38130211830139` / `32.3813` | PASS |
| Case 32 75Hz TL | `2.753591` / `2.753591` | PASS |
| Case 32 100Hz SOL | `60.97644567489624` / `60.97645` | PASS |
| Case 32 100Hz TL | `5.050601` / `5.050601` | PASS |
| Case 32 Avg. SOL | `37.9284918308258` / `37.928490000000004` | PASS |
| Case 32 Avg. TL | `2.533244` / `2.533244` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Variant, 25Hz(Sol,TL), 50Hz, 75Hz, 100Hz, Avg.(Sol,TL)；Avg. 对应 xlsx/日志的 Overall 组。两几何共用一张表，故行内只有一组数值。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 25 25Hz SOL (xlsx) | 源 16.63692949805409 → `16.637` / 印刷 `16.637` | PASS |
| Case 25 25Hz SOL (log) | 源 16.6369326 → `16.637` / 印刷 `16.637` | PASS |
| Case 25 25Hz TL (xlsx) | 源 1.377714 → `1.378` / 印刷 `1.378` | PASS |
| Case 25 25Hz TL (log) | 源 1.377714 → `1.378` / 印刷 `1.378` | PASS |
| Case 25 50Hz SOL (xlsx) | 源 0.5120271787745878 → `0.512` / 印刷 `0.512` | PASS |
| Case 25 50Hz SOL (log) | 源 0.51202722 → `0.512` / 印刷 `0.512` | PASS |
| Case 25 50Hz TL (xlsx) | 源 0.6034657 → `0.603` / 印刷 `0.603` | PASS |
| Case 25 50Hz TL (log) | 源 0.6034657 → `0.603` / 印刷 `0.603` | PASS |
| Case 25 75Hz SOL (xlsx) | 源 10.12754489202052 → `10.128` / 印刷 `10.128` | PASS |
| Case 25 75Hz SOL (log) | 源 10.1275455 → `10.128` / 印刷 `10.128` | PASS |
| Case 25 75Hz TL (xlsx) | 源 1.990745 → `1.991` / 印刷 `1.991` | PASS |
| Case 25 75Hz TL (log) | 源 1.990745 → `1.991` / 印刷 `1.991` | PASS |
| Case 25 100Hz SOL (xlsx) | 源 18.65477762185037 → `18.655` / 印刷 `18.655` | PASS |
| Case 25 100Hz SOL (log) | 源 18.6547783 → `18.655` / 印刷 `18.655` | PASS |
| Case 25 100Hz TL (xlsx) | 源 3.673548 → `3.674` / 印刷 `3.674` | PASS |
| Case 25 100Hz TL (log) | 源 3.673548 → `3.674` / 印刷 `3.674` | PASS |
| Case 25 Avg. SOL (xlsx) | 源 11.48282000795007 → `11.483` / 印刷 `11.483` | PASS |
| Case 25 Avg. SOL (log) | 源 11.48282 → `11.483` / 印刷 `11.483` | PASS |
| Case 25 Avg. TL (xlsx) | 源 1.911368 → `1.911` / 印刷 `1.911` | PASS |
| Case 25 Avg. TL (log) | 源 1.911368 → `1.911` / 印刷 `1.911` | PASS |
| Case 26 25Hz SOL (xlsx) | 源 1563.083946704865 → `1563.084` / 印刷 `1563.084` | PASS |
| Case 26 25Hz SOL (log) | 源 1563.0834799999998 → `1563.083` / 印刷 `1563.084`（xlsx `1563.083946704865` → `1563.084`，两渠道全精度相差 2.99e-07，属 3 位进位边界） | WARN |
| Case 26 25Hz TL (xlsx) | 源 22.93166 → `22.932` / 印刷 `22.932` | PASS |
| Case 26 25Hz TL (log) | 源 22.93166 → `22.932` / 印刷 `22.932` | PASS |
| Case 26 50Hz SOL (xlsx) | 源 479.50402945280075 → `479.504` / 印刷 `479.504` | PASS |
| Case 26 50Hz SOL (log) | 源 479.50399300000004 → `479.504` / 印刷 `479.504` | PASS |
| Case 26 50Hz TL (xlsx) | 源 32.71898 → `32.719` / 印刷 `32.719` | PASS |
| Case 26 50Hz TL (log) | 源 32.71898 → `32.719` / 印刷 `32.719` | PASS |
| Case 26 75Hz SOL (xlsx) | 源 424.60011579096323 → `424.600` / 印刷 `424.600` | PASS |
| Case 26 75Hz SOL (log) | 源 424.6001 → `424.600` / 印刷 `424.600` | PASS |
| Case 26 75Hz TL (xlsx) | 源 46.46738 → `46.467` / 印刷 `46.467` | PASS |
| Case 26 75Hz TL (log) | 源 46.46738 → `46.467` / 印刷 `46.467` | PASS |
| Case 26 100Hz SOL (xlsx) | 源 129.5851467177272 → `129.585` / 印刷 `129.585` | PASS |
| Case 26 100Hz SOL (log) | 源 129.585123 → `129.585` / 印刷 `129.585` | PASS |
| Case 26 100Hz TL (xlsx) | 源 53.08328 → `53.083` / 印刷 `53.083` | PASS |
| Case 26 100Hz TL (log) | 源 53.08328 → `53.083` / 印刷 `53.083` | PASS |
| Case 26 Avg. SOL (xlsx) | 源 649.1932973265648 → `649.193` / 印刷 `649.193` | PASS |
| Case 26 Avg. SOL (log) | 源 649.1932999999999 → `649.193` / 印刷 `649.193` | PASS |
| Case 26 Avg. TL (xlsx) | 源 38.80033 → `38.800` / 印刷 `38.800` | PASS |
| Case 26 Avg. TL (log) | 源 38.80033 → `38.800` / 印刷 `38.800` | PASS |
| Case 27 25Hz SOL (xlsx) | 源 10.36997995106504 → `10.370` / 印刷 `10.370` | PASS |
| Case 27 25Hz SOL (log) | 源 10.369980199999999 → `10.370` / 印刷 `10.370` | PASS |
| Case 27 25Hz TL (xlsx) | 源 1.087888 → `1.088` / 印刷 `1.088` | PASS |
| Case 27 25Hz TL (log) | 源 1.087888 → `1.088` / 印刷 `1.088` | PASS |
| Case 27 50Hz SOL (xlsx) | 源 0.5764913483290002 → `0.576` / 印刷 `0.576` | PASS |
| Case 27 50Hz SOL (log) | 源 0.576491387 → `0.576` / 印刷 `0.576` | PASS |
| Case 27 50Hz TL (xlsx) | 源 0.630979 → `0.631` / 印刷 `0.631` | PASS |
| Case 27 50Hz TL (log) | 源 0.630979 → `0.631` / 印刷 `0.631` | PASS |
| Case 27 75Hz SOL (xlsx) | 源 19.53623965382576 → `19.536` / 印刷 `19.536` | PASS |
| Case 27 75Hz SOL (log) | 源 19.5362376 → `19.536` / 印刷 `19.536` | PASS |
| Case 27 75Hz TL (xlsx) | 源 2.559839 → `2.560` / 印刷 `2.560` | PASS |
| Case 27 75Hz TL (log) | 源 2.559839 → `2.560` / 印刷 `2.560` | PASS |
| Case 27 100Hz SOL (xlsx) | 源 22.92125532403589 → `22.921` / 印刷 `22.921` | PASS |
| Case 27 100Hz SOL (log) | 源 22.921257500000003 → `22.921` / 印刷 `22.921` | PASS |
| Case 27 100Hz TL (xlsx) | 源 4.544477 → `4.544` / 印刷 `4.544` | PASS |
| Case 27 100Hz TL (log) | 源 4.544477 → `4.544` / 印刷 `4.544` | PASS |
| Case 27 Avg. SOL (xlsx) | 源 13.350991916377101 → `13.351` / 印刷 `13.351` | PASS |
| Case 27 Avg. SOL (log) | 源 13.35099 → `13.351` / 印刷 `13.351` | PASS |
| Case 27 Avg. TL (xlsx) | 源 2.205796 → `2.206` / 印刷 `2.206` | PASS |
| Case 27 Avg. TL (log) | 源 2.205796 → `2.206` / 印刷 `2.206` | PASS |
| Case 28 25Hz SOL (xlsx) | 源 3.189601749181748 → `3.190` / 印刷 `3.190` | PASS |
| Case 28 25Hz SOL (log) | 源 3.189602 → `3.190` / 印刷 `3.190` | PASS |
| Case 28 25Hz TL (xlsx) | 源 0.7414964 → `0.741` / 印刷 `0.741` | PASS |
| Case 28 25Hz TL (log) | 源 0.7414964 → `0.741` / 印刷 `0.741` | PASS |
| Case 28 50Hz SOL (xlsx) | 源 0.5421166773885489 → `0.542` / 印刷 `0.542` | PASS |
| Case 28 50Hz SOL (log) | 源 0.5421167 → `0.542` / 印刷 `0.542` | PASS |
| Case 28 50Hz TL (xlsx) | 源 0.629636 → `0.630` / 印刷 `0.630` | PASS |
| Case 28 50Hz TL (log) | 源 0.629636 → `0.630` / 印刷 `0.630` | PASS |
| Case 28 75Hz SOL (xlsx) | 源 19.97445821762085 → `19.974` / 印刷 `19.974` | PASS |
| Case 28 75Hz SOL (log) | 源 19.97446 → `19.974` / 印刷 `19.974` | PASS |
| Case 28 75Hz TL (xlsx) | 源 2.609463 → `2.609` / 印刷 `2.609` | PASS |
| Case 28 75Hz TL (log) | 源 2.609463 → `2.609` / 印刷 `2.609` | PASS |
| Case 28 100Hz SOL (xlsx) | 源 21.54092490673066 → `21.541` / 印刷 `21.541` | PASS |
| Case 28 100Hz SOL (log) | 源 21.540919999999996 → `21.541` / 印刷 `21.541` | PASS |
| Case 28 100Hz TL (xlsx) | 源 4.309467 → `4.309` / 印刷 `4.309` | PASS |
| Case 28 100Hz TL (log) | 源 4.309467 → `4.309` / 印刷 `4.309` | PASS |
| Case 28 Avg. SOL (xlsx) | 源 11.31177544593811 → `11.312` / 印刷 `11.312` | PASS |
| Case 28 Avg. SOL (log) | 源 11.31178 → `11.312` / 印刷 `11.312` | PASS |
| Case 28 Avg. TL (xlsx) | 源 2.072516 → `2.073` / 印刷 `2.073` | PASS |
| Case 28 Avg. TL (log) | 源 2.072516 → `2.073` / 印刷 `2.073` | PASS |
| Case 29 25Hz SOL (xlsx) | 源 33.35254043340683 → `33.353` / 印刷 `33.353` | PASS |
| Case 29 25Hz SOL (log) | 源 33.3525412 → `33.353` / 印刷 `33.353` | PASS |
| Case 29 25Hz TL (xlsx) | 源 1.291144 → `1.291` / 印刷 `1.291` | PASS |
| Case 29 25Hz TL (log) | 源 1.291144 → `1.291` / 印刷 `1.291` | PASS |
| Case 29 50Hz SOL (xlsx) | 源 0.7033266650978476 → `0.703` / 印刷 `0.703` | PASS |
| Case 29 50Hz SOL (log) | 源 0.7033267 → `0.703` / 印刷 `0.703` | PASS |
| Case 29 50Hz TL (xlsx) | 源 0.7219688 → `0.722` / 印刷 `0.722` | PASS |
| Case 29 50Hz TL (log) | 源 0.7219688 → `0.722` / 印刷 `0.722` | PASS |
| Case 29 75Hz SOL (xlsx) | 源 19.44934674538672 → `19.449` / 印刷 `19.449` | PASS |
| Case 29 75Hz SOL (log) | 源 19.4493459 → `19.449` / 印刷 `19.449` | PASS |
| Case 29 75Hz TL (xlsx) | 源 2.140294 → `2.140` / 印刷 `2.140` | PASS |
| Case 29 75Hz TL (log) | 源 2.140294 → `2.140` / 印刷 `2.140` | PASS |
| Case 29 100Hz SOL (xlsx) | 源 33.0750647932291 → `33.075` / 印刷 `33.075` | PASS |
| Case 29 100Hz SOL (log) | 源 33.0750678 → `33.075` / 印刷 `33.075` | PASS |
| Case 29 100Hz TL (xlsx) | 源 3.590624 → `3.591` / 印刷 `3.591` | PASS |
| Case 29 100Hz TL (log) | 源 3.590624 → `3.591` / 印刷 `3.591` | PASS |
| Case 29 Avg. SOL (xlsx) | 源 21.64506972767413 → `21.645` / 印刷 `21.645` | PASS |
| Case 29 Avg. SOL (log) | 源 21.645069999999997 → `21.645` / 印刷 `21.645` | PASS |
| Case 29 Avg. TL (xlsx) | 源 1.936008 → `1.936` / 印刷 `1.936` | PASS |
| Case 29 Avg. TL (log) | 源 1.936008 → `1.936` / 印刷 `1.936` | PASS |
| Case 30 25Hz SOL (xlsx) | 源 9691.231346130371 → `9691.231` / 印刷 `9691.231` | PASS |
| Case 30 25Hz SOL (log) | 源 9691.231 → `9691.231` / 印刷 `9691.231` | PASS |
| Case 30 25Hz TL (xlsx) | 源 9.445384 → `9.445` / 印刷 `9.445` | PASS |
| Case 30 25Hz TL (log) | 源 9.445384 → `9.445` / 印刷 `9.445` | PASS |
| Case 30 50Hz SOL (xlsx) | 源 1386.380329728127 → `1386.380` / 印刷 `1386.380` | PASS |
| Case 30 50Hz SOL (log) | 源 1386.3802799999999 → `1386.380` / 印刷 `1386.380` | PASS |
| Case 30 50Hz TL (xlsx) | 源 55.7952 → `55.795` / 印刷 `55.795` | PASS |
| Case 30 50Hz TL (log) | 源 55.7952 → `55.795` / 印刷 `55.795` | PASS |
| Case 30 75Hz SOL (xlsx) | 源 685.3322699666023 → `685.332` / 印刷 `685.332` | PASS |
| Case 30 75Hz SOL (log) | 源 685.3322770000001 → `685.332` / 印刷 `685.332` | PASS |
| Case 30 75Hz TL (xlsx) | 源 83.00855 → `83.009` / 印刷 `83.009` | PASS |
| Case 30 75Hz TL (log) | 源 83.00855 → `83.009` / 印刷 `83.009` | PASS |
| Case 30 100Hz SOL (xlsx) | 源 327.8753321617842 → `327.875` / 印刷 `327.875` | PASS |
| Case 30 100Hz SOL (log) | 源 327.875372 → `327.875` / 印刷 `327.875` | PASS |
| Case 30 100Hz TL (xlsx) | 源 46.9382 → `46.938` / 印刷 `46.938` | PASS |
| Case 30 100Hz TL (log) | 源 46.9382 → `46.938` / 印刷 `46.938` | PASS |
| Case 30 Avg. SOL (xlsx) | 源 3022.704696655274 → `3022.705` / 印刷 `3022.705` | PASS |
| Case 30 Avg. SOL (log) | 源 3022.705 → `3022.705` / 印刷 `3022.705` | PASS |
| Case 30 Avg. TL (xlsx) | 源 48.79683 → `48.797` / 印刷 `48.797` | PASS |
| Case 30 Avg. TL (log) | 源 48.79683 → `48.797` / 印刷 `48.797` | PASS |
| Case 31 25Hz SOL (xlsx) | 源 162.56497632712131 → `162.565` / 印刷 `162.565` | PASS |
| Case 31 25Hz SOL (log) | 源 162.56494999999998 → `162.565` / 印刷 `162.565` | PASS |
| Case 31 25Hz TL (xlsx) | 源 2.037057 → `2.037` / 印刷 `2.037` | PASS |
| Case 31 25Hz TL (log) | 源 2.037057 → `2.037` / 印刷 `2.037` | PASS |
| Case 31 50Hz SOL (xlsx) | 源 1.3072183821350338 → `1.307` / 印刷 `1.307` | PASS |
| Case 31 50Hz SOL (log) | 源 1.3072188200000001 → `1.307` / 印刷 `1.307` | PASS |
| Case 31 50Hz TL (xlsx) | 源 0.8516294 → `0.852` / 印刷 `0.852` | PASS |
| Case 31 50Hz TL (log) | 源 0.8516294 → `0.852` / 印刷 `0.852` | PASS |
| Case 31 75Hz SOL (xlsx) | 源 21.83450921438635 → `21.835` / 印刷 `21.835` | PASS |
| Case 31 75Hz SOL (log) | 源 21.834504900000002 → `21.835` / 印刷 `21.835` | PASS |
| Case 31 75Hz TL (xlsx) | 源 2.342786 → `2.343` / 印刷 `2.343` | PASS |
| Case 31 75Hz TL (log) | 源 2.342786 → `2.343` / 印刷 `2.343` | PASS |
| Case 31 100Hz SOL (xlsx) | 源 55.65077951177954 → `55.651` / 印刷 `55.651` | PASS |
| Case 31 100Hz SOL (log) | 源 55.650782199999995 → `55.651` / 印刷 `55.651` | PASS |
| Case 31 100Hz TL (xlsx) | 源 4.540552 → `4.541` / 印刷 `4.541` | PASS |
| Case 31 100Hz TL (log) | 源 4.540552 → `4.541` / 印刷 `4.541` | PASS |
| Case 31 Avg. SOL (xlsx) | 源 60.33936939202249 → `60.339` / 印刷 `60.339` | PASS |
| Case 31 Avg. SOL (log) | 源 60.339369999999995 → `60.339` / 印刷 `60.339` | PASS |
| Case 31 Avg. TL (xlsx) | 源 2.443006 → `2.443` / 印刷 `2.443` | PASS |
| Case 31 Avg. TL (log) | 源 2.443006 → `2.443` / 印刷 `2.443` | PASS |
| Case 32 25Hz SOL (xlsx) | 源 57.36030340194702 → `57.360` / 印刷 `57.360` | PASS |
| Case 32 25Hz SOL (log) | 源 57.360299999999995 → `57.360` / 印刷 `57.360` | PASS |
| Case 32 25Hz TL (xlsx) | 源 1.577166 → `1.577` / 印刷 `1.577` | PASS |
| Case 32 25Hz TL (log) | 源 1.577166 → `1.577` / 印刷 `1.577` | PASS |
| Case 32 50Hz SOL (xlsx) | 源 0.9959153831005096 → `0.996` / 印刷 `0.996` | PASS |
| Case 32 50Hz SOL (log) | 源 0.9959154 → `0.996` / 印刷 `0.996` | PASS |
| Case 32 50Hz TL (xlsx) | 源 0.7516175 → `0.752` / 印刷 `0.752` | PASS |
| Case 32 50Hz TL (log) | 源 0.7516175 → `0.752` / 印刷 `0.752` | PASS |
| Case 32 75Hz SOL (xlsx) | 源 32.38130211830139 → `32.381` / 印刷 `32.381` | PASS |
| Case 32 75Hz SOL (log) | 源 32.3813 → `32.381` / 印刷 `32.381` | PASS |
| Case 32 75Hz TL (xlsx) | 源 2.753591 → `2.754` / 印刷 `2.754` | PASS |
| Case 32 75Hz TL (log) | 源 2.753591 → `2.754` / 印刷 `2.754` | PASS |
| Case 32 100Hz SOL (xlsx) | 源 60.97644567489624 → `60.976` / 印刷 `60.976` | PASS |
| Case 32 100Hz SOL (log) | 源 60.97645 → `60.976` / 印刷 `60.976` | PASS |
| Case 32 100Hz TL (xlsx) | 源 5.050601 → `5.051` / 印刷 `5.051` | PASS |
| Case 32 100Hz TL (log) | 源 5.050601 → `5.051` / 印刷 `5.051` | PASS |
| Case 32 Avg. SOL (xlsx) | 源 37.9284918308258 → `37.928` / 印刷 `37.928` | PASS |
| Case 32 Avg. SOL (log) | 源 37.928490000000004 → `37.928` / 印刷 `37.928` | PASS |
| Case 32 Avg. TL (xlsx) | 源 2.533244 → `2.533` / 印刷 `2.533` | PASS |
| Case 32 Avg. TL (log) | 源 2.533244 → `2.533` / 印刷 `2.533` | PASS |

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
| 全部 80 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 8. 加粗判据（每列在各几何块内的最小值）

> caption：'The best value in each column, within each geometry, is in bold'。两几何是上下两块、行集合互不相干，故最小值必须**分块**取；若误按全表取，楔形块会出现 4 行全不加粗而隐形漏检。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 两几何块 × 10 列 = 20 处加粗均指向块内最小值 | 全部合规 | PASS |

## 9. 正文引用精确性（4.5 节）

> 每处引用查两件事：① 与表格印刷值同值同位数；② 该值确由 xlsx 源支持。只查①会漏掉正文与表格一起错的情形。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 4.5 节正文窗口可定位 | 起句 `The physics prior is by far the most imp…` | PASS |
| 正文 Case 25 频均 Sol | 正文 `11.483` / 表格 `11.483` | PASS |
| 正文 Case 25 频均 Sol <- xlsx 源 | 源 11.48282000795007 → `11.483` / 印刷 `11.483` | PASS |
| 正文 Case 25 频均 Sol 可定位 | 窗口内行 2 | PASS |
| 正文 Case 26 频均 Sol | 正文 `649.193` / 表格 `649.193` | PASS |
| 正文 Case 26 频均 Sol <- xlsx 源 | 源 649.1932973265648 → `649.193` / 印刷 `649.193` | PASS |
| 正文 Case 26 频均 Sol 可定位 | 窗口内行 2 | PASS |
| 正文 Case 25 频均 TL | 正文 `1.911` / 表格 `1.911` | PASS |
| 正文 Case 25 频均 TL <- xlsx 源 | 源 1.911368 → `1.911` / 印刷 `1.911` | PASS |
| 正文 Case 25 频均 TL 可定位 | 窗口内行 3 | PASS |
| 正文 Case 26 频均 TL | 正文 `38.800` / 表格 `38.800` | PASS |
| 正文 Case 26 频均 TL <- xlsx 源 | 源 38.80033 → `38.800` / 印刷 `38.800` | PASS |
| 正文 Case 26 频均 TL 可定位 | 窗口内行 3 | PASS |
| 正文 Case 29 频均 Sol | 正文 `21.645` / 表格 `21.645` | PASS |
| 正文 Case 29 频均 Sol <- xlsx 源 | 源 21.64506972767413 → `21.645` / 印刷 `21.645` | PASS |
| 正文 Case 29 频均 Sol 可定位 | 窗口内行 3 | PASS |
| 正文 Case 30 频均 Sol | 正文 `3022.705` / 表格 `3022.705` | PASS |
| 正文 Case 30 频均 Sol <- xlsx 源 | 源 3022.704696655274 → `3022.705` / 印刷 `3022.705` | PASS |
| 正文 Case 30 频均 Sol 可定位 | 窗口内行 3 | PASS |
| 正文 Case 29 频均 TL | 正文 `1.936` / 表格 `1.936` | PASS |
| 正文 Case 29 频均 TL <- xlsx 源 | 源 1.936008 → `1.936` / 印刷 `1.936` | PASS |
| 正文 Case 29 频均 TL 可定位 | 窗口内行 7 | PASS |
| 正文 Case 30 频均 TL | 正文 `48.797` / 表格 `48.797` | PASS |
| 正文 Case 30 频均 TL <- xlsx 源 | 源 48.79683 → `48.797` / 印刷 `48.797` | PASS |
| 正文 Case 30 频均 TL 可定位 | 窗口内行 7 | PASS |

## 10. 正文变体排序断言（印刷值口径）

> 正文：去掉物理先验后误差激增；楔形上全模型各频段最优，矩形上全模型在 50-100Hz 领先、25Hz 由 w/o prior supervision 略胜。这些是可复算的排序断言，用表格印刷值验证，不用源值。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 矩形 w/o prior 的频均 SOL 比全模型高一个数量级 | `649.193` vs `11.483` | PASS |
| 楔形 w/o prior 的频均 SOL 比全模型高一个数量级 | `3022.705` vs `21.645` | PASS |
| 矩形 w/o prior 的频均 TL 比全模型高一个数量级 | `38.800` vs `1.911` | PASS |
| 楔形 w/o prior 的频均 TL 比全模型高一个数量级 | `48.797` vs `1.936` | PASS |
| 楔形频均 SOL 最优为全模型 (Case 29) | 实得 [29] | PASS |
| 矩形 50Hz SOL 最优为全模型 (Case 25) | 全模型 `0.512` / 最小 `0.512` | PASS |
| 矩形 75Hz SOL 最优为全模型 (Case 25) | 全模型 `10.128` / 最小 `10.128` | PASS |
| 矩形 100Hz SOL 最优为全模型 (Case 25) | 全模型 `18.655` / 最小 `18.655` | PASS |
| 矩形 25Hz SOL 最优为 w/o prior supervision (Case 28) | Case 28 `3.190` / 最小 `3.190` | PASS |
| 楔形频均 TL 最优为全模型 (Case 29) | 实得 [29] | PASS |
| 矩形 50Hz TL 最优为全模型 (Case 25) | 全模型 `0.603` / 最小 `0.603` | PASS |
| 矩形 75Hz TL 最优为全模型 (Case 25) | 全模型 `1.991` / 最小 `1.991` | PASS |
| 矩形 100Hz TL 最优为全模型 (Case 25) | 全模型 `3.674` / 最小 `3.674` | PASS |
| 矩形 25Hz TL 最优为 w/o prior supervision (Case 28) | Case 28 `0.741` / 最小 `0.741` | PASS |

## 11. caption 声明核验

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 数据源确为该口径 | PASS |
| caption 未误写 last epoch | 口径唯一 | PASS |
| 表号为 11 | aux `11` | PASS |

## 12. caption 其余声明（按几何加粗 / 四频均值 / 案例号）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 写明加粗按几何分别判定 |  | PASS |
| caption 声明 Avg. 为四频均值 |  | PASS |
| caption 写明两块的案例号范围 |  | PASS |
| caption 声明变体数为 4 |  | PASS |

