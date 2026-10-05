# Table 11 — 网格无关性，矩形与楔形并排

- 对象：`tab:mesh`（Table 11）
- 结论：**PASS** — 113 通过 / 0 失败 / 0 警告，共 113 项
- 脚本：`ch4_validation/scripts/T11_mesh.py`
- 生成：2026-10-06 00:26:11

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{tab:mesh}` 所在环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/Case33-38_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 33) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No33_R4/training_run/logs/full_run_20260710_224527.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 34) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No34_R7/training_run/logs/full_run_20260710_220203.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 35) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No35_R8/training_run/logs/full_run_20260710_025319.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 36) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No36_W4/training_run/logs/full_run_20260710_150948.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 37) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No37_W7/training_run/logs/full_run_20260710_123333.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 38) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No38_W8/training_run/logs/full_run_20260710_030023.log` | 训练日志同轮『评估』块 |
| 复用比对 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/Case3-14_数据汇总.xlsx` | 4.3 节汇总，用于确认 Case 33≡6、36≡12 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/Case33-38_数据汇总.xlsx | PASS |
| Case 33 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No33_R4/training_run/logs/full_run_20260710_224527.log | PASS |
| Case 34 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No34_R7/training_run/logs/full_run_20260710_220203.log | PASS |
| Case 35 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No35_R8/training_run/logs/full_run_20260710_025319.log | PASS |
| Case 36 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No36_W4/training_run/logs/full_run_20260710_150948.log | PASS |
| Case 37 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No37_W7/training_run/logs/full_run_20260710_123333.log | PASS |
| Case 38 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No38_W8/training_run/logs/full_run_20260710_030023.log | PASS |
| tex 表格环境可定位且确实包住 label | 长度 2334 | PASS |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 行 No. 覆盖 33-35 与 36-38 | [33, 34, 35, 36, 37, 38] | PASS |
| Case 33 落在矩形块 | 实得 矩形 | PASS |
| Case 34 落在矩形块 | 实得 矩形 | PASS |
| Case 35 落在矩形块 | 实得 矩形 | PASS |
| Case 36 落在楔形块 | 实得 楔形 | PASS |
| Case 37 落在楔形块 | 实得 楔形 | PASS |
| Case 38 落在楔形块 | 实得 楔形 | PASS |

## 3. best epoch 一致性

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 33 best epoch | xlsx `192` / log `192` | PASS |
| Case 33 日志含『评估 Epoch 192』块 | 轮次 192 | PASS |
| Case 34 best epoch | xlsx `200` / log `200` | PASS |
| Case 34 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |
| Case 35 best epoch | xlsx `167` / log `167` | PASS |
| Case 35 日志含『评估 Epoch 167』块 | 轮次 167 | PASS |
| Case 36 best epoch | xlsx `195` / log `195` | PASS |
| Case 36 日志含『评估 Epoch 195』块 | 轮次 195 | PASS |
| Case 37 best epoch | xlsx `199` / log `199` | PASS |
| Case 37 日志含『评估 Epoch 199』块 | 轮次 199 | PASS |
| Case 38 best epoch | xlsx `194` / log `194` | PASS |
| Case 38 日志含『评估 Epoch 194』块 | 轮次 194 | PASS |

## 4. 双渠道交叉验证（xlsx vs log）

> 本表只有 100 Hz 一档，故只核 100Hz 组。

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 33 100Hz SOL | `0.0577102506213123` / `0.057710252` | PASS |
| Case 33 100Hz TL | `0.4443021` / `0.4443021` | PASS |
| Case 34 100Hz SOL | `0.13098313575028442` / `0.130983092` | PASS |
| Case 34 100Hz TL | `0.3843261` / `0.3843261` | PASS |
| Case 35 100Hz SOL | `0.2871782717193128` / `0.287178317` | PASS |
| Case 35 100Hz TL | `0.3925595` / `0.3925595` | PASS |
| Case 36 100Hz SOL | `0.10030982230091469` / `0.10030979000000001` | PASS |
| Case 36 100Hz TL | `0.6095095` / `0.6095095` | PASS |
| Case 37 100Hz SOL | `0.19601167878136042` / `0.19601165` | PASS |
| Case 37 100Hz TL | `0.3608499` / `0.3608499` | PASS |
| Case 38 100Hz SOL | `0.3259683660871815` / `0.32596840000000005` | PASS |
| Case 38 100Hz TL | `0.3113609` / `0.3113609` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：Δ, No., Dataset, Sol, TL（矩形块）| No., Dataset, Sol, TL（楔形块）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 Dataset 名 | tex `R4` | PASS |
| Case 33 SOL (xlsx) | 源 0.0577102506213123 → `0.058` / 印刷 `0.058` | PASS |
| Case 33 SOL (log) | 源 0.057710252 → `0.058` / 印刷 `0.058` | PASS |
| Case 33 TL (xlsx) | 源 0.4443021 → `0.444` / 印刷 `0.444` | PASS |
| Case 33 TL (log) | 源 0.4443021 → `0.444` / 印刷 `0.444` | PASS |
| Case 34 Dataset 名 | tex `R7` | PASS |
| Case 34 SOL (xlsx) | 源 0.13098313575028442 → `0.131` / 印刷 `0.131` | PASS |
| Case 34 SOL (log) | 源 0.130983092 → `0.131` / 印刷 `0.131` | PASS |
| Case 34 TL (xlsx) | 源 0.3843261 → `0.384` / 印刷 `0.384` | PASS |
| Case 34 TL (log) | 源 0.3843261 → `0.384` / 印刷 `0.384` | PASS |
| Case 35 Dataset 名 | tex `R8` | PASS |
| Case 35 SOL (xlsx) | 源 0.2871782717193128 → `0.287` / 印刷 `0.287` | PASS |
| Case 35 SOL (log) | 源 0.287178317 → `0.287` / 印刷 `0.287` | PASS |
| Case 35 TL (xlsx) | 源 0.3925595 → `0.393` / 印刷 `0.393` | PASS |
| Case 35 TL (log) | 源 0.3925595 → `0.393` / 印刷 `0.393` | PASS |
| Case 36 Dataset 名 | tex `W4` | PASS |
| Case 36 SOL (xlsx) | 源 0.10030982230091469 → `0.100` / 印刷 `0.100` | PASS |
| Case 36 SOL (log) | 源 0.10030979000000001 → `0.100` / 印刷 `0.100` | PASS |
| Case 36 TL (xlsx) | 源 0.6095095 → `0.610` / 印刷 `0.610` | PASS |
| Case 36 TL (log) | 源 0.6095095 → `0.610` / 印刷 `0.610` | PASS |
| Case 37 Dataset 名 | tex `W7` | PASS |
| Case 37 SOL (xlsx) | 源 0.19601167878136042 → `0.196` / 印刷 `0.196` | PASS |
| Case 37 SOL (log) | 源 0.19601165 → `0.196` / 印刷 `0.196` | PASS |
| Case 37 TL (xlsx) | 源 0.3608499 → `0.361` / 印刷 `0.361` | PASS |
| Case 37 TL (log) | 源 0.3608499 → `0.361` / 印刷 `0.361` | PASS |
| Case 38 Dataset 名 | tex `W8` | PASS |
| Case 38 SOL (xlsx) | 源 0.3259683660871815 → `0.326` / 印刷 `0.326` | PASS |
| Case 38 SOL (log) | 源 0.32596840000000005 → `0.326` / 印刷 `0.326` | PASS |
| Case 38 TL (xlsx) | 源 0.3113609 → `0.311` / 印刷 `0.311` | PASS |
| Case 38 TL (log) | 源 0.3113609 → `0.311` / 印刷 `0.311` | PASS |

## 6. Δ 列与案例归属

> 行首的 Δ 标签同时被两个几何块共用；写错会让楔形行被读成矩形分辨率。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 Δ 标签 | tex `1.00` / 期望 `1.00` | PASS |
| Case 34 Δ 标签 | tex `0.50` / 期望 `0.50` | PASS |
| Case 35 Δ 标签 | tex `0.25` / 期望 `0.25` | PASS |
| Case 36 Δ 标签 | tex `1.00` / 期望 `1.00` | PASS |
| Case 37 Δ 标签 | tex `0.50` / 期望 `0.50` | PASS |
| Case 38 Δ 标签 | tex `0.25` / 期望 `0.25` | PASS |

## 6. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 24 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 8. 与 4.3 节的复用关系

> 4.6 网格研究的最粗一档就是 4.3 的单频案例：Case 33 复用 Case 6、Case 36 复用 Case 12。判定不看三位小数（那可能是巧合），而要求 best epoch 与全精度值都一致，才算同一次运行。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 与 Case 6 best epoch 相同 | `192` == `192` | PASS |
| Case 33 与 Case 6 SOL 全精度相同 | `0.0577102506213123` == `0.0577102506213123` | PASS |
| Case 33 与 Case 6 TL 全精度相同 | `0.4443021` == `0.4443021` | PASS |
| Case 36 与 Case 12 best epoch 相同 | `195` == `195` | PASS |
| Case 36 与 Case 12 SOL 全精度相同 | `0.10030982230091469` == `0.10030982230091469` | PASS |
| Case 36 与 Case 12 TL 全精度相同 | `0.6095095` == `0.6095095` | PASS |

## 9. 正文引用精确性（4.6 节）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 Case 33 (Δ=1.00) Sol | 正文 `0.058` / 表格 `0.058` | PASS |
| 正文 Case 33 (Δ=1.00) Sol ← xlsx 源 | 源 0.0577102506213123 → `0.058` / 印刷 `0.058` | PASS |
| 正文 Case 35 (Δ=0.25) Sol | 正文 `0.287` / 表格 `0.287` | PASS |
| 正文 Case 35 (Δ=0.25) Sol ← xlsx 源 | 源 0.2871782717193128 → `0.287` / 印刷 `0.287` | PASS |
| 正文 Case 36 (Δ=1.00) Sol | 正文 `0.100` / 表格 `0.100` | PASS |
| 正文 Case 36 (Δ=1.00) Sol ← xlsx 源 | 源 0.10030982230091469 → `0.100` / 印刷 `0.100` | PASS |
| 正文 Case 38 (Δ=0.25) Sol | 正文 `0.326` / 表格 `0.326` | PASS |
| 正文 Case 38 (Δ=0.25) Sol ← xlsx 源 | 源 0.3259683660871815 → `0.326` / 印刷 `0.326` | PASS |
| 正文 Case 33 (Δ=1.00) TL | 正文 `0.444` / 表格 `0.444` | PASS |
| 正文 Case 33 (Δ=1.00) TL ← xlsx 源 | 源 0.4443021 → `0.444` / 印刷 `0.444` | PASS |
| 正文 Case 34 (Δ=0.50) TL | 正文 `0.384` / 表格 `0.384` | PASS |
| 正文 Case 34 (Δ=0.50) TL ← xlsx 源 | 源 0.3843261 → `0.384` / 印刷 `0.384` | PASS |
| 正文 Case 35 (Δ=0.25) TL | 正文 `0.393` / 表格 `0.393` | PASS |
| 正文 Case 35 (Δ=0.25) TL ← xlsx 源 | 源 0.3925595 → `0.393` / 印刷 `0.393` | PASS |
| 正文 Case 36 (Δ=1.00) TL | 正文 `0.610` / 表格 `0.610` | PASS |
| 正文 Case 36 (Δ=1.00) TL ← xlsx 源 | 源 0.6095095 → `0.610` / 印刷 `0.610` | PASS |
| 正文 Case 37 (Δ=0.50) TL | 正文 `0.361` / 表格 `0.361` | PASS |
| 正文 Case 37 (Δ=0.50) TL ← xlsx 源 | 源 0.3608499 → `0.361` / 印刷 `0.361` | PASS |
| 正文 Case 38 (Δ=0.25) TL | 正文 `0.311` / 表格 `0.311` | PASS |
| 正文 Case 38 (Δ=0.25) TL ← xlsx 源 | 源 0.3113609 → `0.311` / 印刷 `0.311` | PASS |

## 10. 正文趋势断言

> 正文称解误差随细化温和上升，而 TL（物理相关量）不随细化变差。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 矩形 Sol 随细化上升 | 0.058 < 0.131 < 0.287 | PASS |
| 矩形 TL 全部低于 0.65 dB | 0.444 / 0.384 / 0.393 | PASS |
| 矩形 最细网格 TL 不劣于最粗 | `0.444` → `0.393` | PASS |
| 楔形 Sol 随细化上升 | 0.100 < 0.196 < 0.326 | PASS |
| 楔形 TL 全部低于 0.65 dB | 0.610 / 0.361 / 0.311 | PASS |
| 楔形 最细网格 TL 不劣于最粗 | `0.610` → `0.311` | PASS |

## 7. caption 声明核验

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 数据源确为该口径 | PASS |
| caption 未误写 last epoch | 口径唯一 | PASS |
| 表号为 11 | aux `11` | PASS |

## 12. caption 已写明行与子图的对应关系

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 写明行对应 (a)-(c)/(d)-(f) | caption 含 `panels (a)--(c) and (d)--(f)` | PASS |
| caption 交叉引用 Fig.\ref{fig:mesh} |  | PASS |

