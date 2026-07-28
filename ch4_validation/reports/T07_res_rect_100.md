# Table 7 — 100Hz 方形域 矩形 R4-R6

- 对象：`tab:res-rect-100`（Table 7）
- 结论：**PASS** — 80 通过 / 0 失败 / 0 警告，共 80 项
- 脚本：`ch4_validation/scripts/T07_res_rect_100.py`
- 生成：2026-07-28 21:50:26

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:res-rect-100}` 所在 minipage |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/Case3-14_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 6) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No06_R4/training_run/logs/full_run_20260710_224527.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 7) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No07_R5/training_run/logs/full_run_20260710_220509.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 8) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No08_R6/training_run/logs/full_run_20260710_024837.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/Case3-14_数据汇总.xlsx | PASS |
| Case 6 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No06_R4/training_run/logs/full_run_20260710_224527.log | PASS |
| Case 7 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No07_R5/training_run/logs/full_run_20260710_220509.log | PASS |
| Case 8 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No08_R6/training_run/logs/full_run_20260710_024837.log | PASS |
| tex 表格环境可定位且确实包住 label | 长度 789 | PASS |
| tex 数据行数 = 3 | 实得 3 | PASS |
| tex 行 No. 覆盖 Case 6-8 | [6, 7, 8] | PASS |

## 3. best epoch 一致性

> 三例 best epoch 各不相同（192/196/200），正说明取值是逐案例按各自最佳轮读的，不是一律取 ep200。

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 6 best epoch | xlsx `192` / log `192` | PASS |
| Case 6 日志含『评估 Epoch 192』块 | 轮次 192 | PASS |
| Case 7 best epoch | xlsx `196` / log `196` | PASS |
| Case 7 日志含『评估 Epoch 196』块 | 轮次 196 | PASS |
| Case 8 best epoch | xlsx `200` / log `200` | PASS |
| Case 8 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |

## 4. 双渠道交叉验证（xlsx vs log）

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 6 Overall SOL | `0.0577102506213123` / `0.057710250000000005` | PASS |
| Case 6 Overall TL | `0.4443021` / `0.4443021` | PASS |
| Case 6 100 SOL | `0.0577102506213123` / `0.057710252` | PASS |
| Case 6 100 TL | `0.4443021` / `0.4443021` | PASS |
| Case 7 Overall SOL | `1.23036066070199` / `1.230361` | PASS |
| Case 7 Overall TL | `1.216968` / `1.216968` | PASS |
| Case 7 100 SOL | `1.23036066070199` / `1.230361` | PASS |
| Case 7 100 TL | `1.216968` / `1.216968` | PASS |
| Case 8 Overall SOL | `10.42148969136178` / `10.42149` | PASS |
| Case 8 Overall TL | `3.852302` / `3.852302` | PASS |
| Case 8 100 SOL | `10.42148969136178` / `10.421491800000002` | PASS |
| Case 8 100 TL | `3.852302` / `3.852302` | PASS |

## 5. 单频自洽性

> 单频案例只在 100 Hz 上训练与评估，故 Overall 组必须等于 100Hz 组；25/50/75Hz 三块应为空（xlsx 记 `—`）。两者任一不成立，说明该行被误当多频案例填了数。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 6 Overall SOL == 100Hz SOL | `0.0577102506213123` == `0.0577102506213123` | PASS |
| Case 6 Overall TL == 100Hz TL | `0.4443021` == `0.4443021` | PASS |
| Case 6 25/50/75Hz 均为空 | 空的频率 [25, 50, 75] | PASS |
| Case 7 Overall SOL == 100Hz SOL | `1.23036066070199` == `1.23036066070199` | PASS |
| Case 7 Overall TL == 100Hz TL | `1.216968` == `1.216968` | PASS |
| Case 7 25/50/75Hz 均为空 | 空的频率 [25, 50, 75] | PASS |
| Case 8 Overall SOL == 100Hz SOL | `10.42148969136178` == `10.42148969136178` | PASS |
| Case 8 Overall TL == 100Hz TL | `3.852302` == `3.852302` | PASS |
| Case 8 25/50/75Hz 均为空 | 空的频率 [25, 50, 75] | PASS |

## 6. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Dataset, Fig., Lx×Ly, Sol, TL。几何尺寸另与 xlsx 的 Lx/Ly 列比对——尺寸写错会让整行读者对错案例。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 6 Dataset 名 | tex `R4` | PASS |
| Case 6 Lx×Ly 印刷值 | tex `128x128` / 期望 `128x128` | PASS |
| Case 6 Lx/Ly 与 xlsx 一致 | xlsx `128×128` | PASS |
| Case 6 SOL (xlsx) | 源 0.0577102506213123 → `0.058` / 印刷 `0.058` | PASS |
| Case 6 SOL (log) | 源 0.057710252 → `0.058` / 印刷 `0.058` | PASS |
| Case 6 TL (xlsx) | 源 0.4443021 → `0.444` / 印刷 `0.444` | PASS |
| Case 6 TL (log) | 源 0.4443021 → `0.444` / 印刷 `0.444` | PASS |
| Case 7 Dataset 名 | tex `R5` | PASS |
| Case 7 Lx×Ly 印刷值 | tex `256x256` / 期望 `256x256` | PASS |
| Case 7 Lx/Ly 与 xlsx 一致 | xlsx `256×256` | PASS |
| Case 7 SOL (xlsx) | 源 1.23036066070199 → `1.230` / 印刷 `1.230` | PASS |
| Case 7 SOL (log) | 源 1.230361 → `1.230` / 印刷 `1.230` | PASS |
| Case 7 TL (xlsx) | 源 1.216968 → `1.217` / 印刷 `1.217` | PASS |
| Case 7 TL (log) | 源 1.216968 → `1.217` / 印刷 `1.217` | PASS |
| Case 8 Dataset 名 | tex `R6` | PASS |
| Case 8 Lx×Ly 印刷值 | tex `512x512` / 期望 `512x512` | PASS |
| Case 8 Lx/Ly 与 xlsx 一致 | xlsx `512×512` | PASS |
| Case 8 SOL (xlsx) | 源 10.42148969136178 → `10.421` / 印刷 `10.421` | PASS |
| Case 8 SOL (log) | 源 10.421491800000002 → `10.421` / 印刷 `10.421` | PASS |
| Case 8 TL (xlsx) | 源 3.852302 → `3.852` / 印刷 `3.852` | PASS |
| Case 8 TL (log) | 源 3.852302 → `3.852` / 印刷 `3.852` | PASS |

## 7. Fig. 列引用正确性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 6 Fig. 列引用 | tex `\ref{fig:res-rect-100}\subref{fig:res-rect-100-4}` → ['fig:res-rect-100', 'fig:res-rect-100-4'] | PASS |
| label `fig:res-rect-100` 已在 aux 注册 | 编号 `8` | PASS |
| label `fig:res-rect-100-4` 已在 aux 注册 | 编号 `8a` | PASS |
| Case 7 Fig. 列引用 | tex `\ref{fig:res-rect-100}\subref{fig:res-rect-100-5}` → ['fig:res-rect-100', 'fig:res-rect-100-5'] | PASS |
| label `fig:res-rect-100` 已在 aux 注册 | 编号 `8` | PASS |
| label `fig:res-rect-100-5` 已在 aux 注册 | 编号 `8b` | PASS |
| Case 8 Fig. 列引用 | tex `\ref{fig:res-rect-100}\subref{fig:res-rect-100-6}` → ['fig:res-rect-100', 'fig:res-rect-100-6'] | PASS |
| label `fig:res-rect-100` 已在 aux 注册 | 编号 `8` | PASS |
| label `fig:res-rect-100-6` 已在 aux 注册 | 编号 `8c` | PASS |

## 8. caption 与表内脚注

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表取各案例最佳轮 | PASS |
| caption 标明单频 f=100 Hz |  | PASS |
| 单位声明未在 caption 与表内脚注重复 | caption 已写单位；表内另有脚注 `` | PASS |

## 9. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 6 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 10. 正文引用精确性（4.3 节）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 Case 6 Sol | 正文 `0.058` / 表格 `0.058` | PASS |
| 正文 Case 6 Sol ← xlsx 源 | 源 0.0577102506213123 → `0.058` / 印刷 `0.058` | PASS |
| 正文 Case 6 TL | 正文 `0.444` / 表格 `0.444` | PASS |
| 正文 Case 6 TL ← xlsx 源 | 源 0.4443021 → `0.444` / 印刷 `0.444` | PASS |
| 正文 Case 7 TL | 正文 `1.217` / 表格 `1.217` | PASS |
| 正文 Case 7 TL ← xlsx 源 | 源 1.216968 → `1.217` / 印刷 `1.217` | PASS |
| 正文 Case 8 TL | 正文 `3.852` / 表格 `3.852` | PASS |
| 正文 Case 8 TL ← xlsx 源 | 源 3.852302 → `3.852` / 印刷 `3.852` | PASS |

## 11. 正文派生倍数（印刷值口径）

> 倍数用表格印刷值相除。此处 3.852/0.444 = 8.6756… → 8.676；若改用全精度源值 3.852302/0.4443021 会得 8.670，与正文不符——这正是先前 8.676/8.670 之争的由来，口径必须固定为印刷值。

> 对照：全精度口径为 `8.670456` → `8.670`，与正文的 8.676 不同；正文采用印刷值口径，故以印刷值为准。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 100Hz 矩形 512m/128m TL 倍数 = 8.676 | 印刷值口径 `3.852`/`0.444` = `8.675676` → `8.676` | PASS |
| 正文该倍数可定位 | tex 行 778 | PASS |

## 12. 正文趋势断言

> 正文称单频方形域“最准的是 128×128”，且 TL 随域增大单调上升。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| TL 随域尺度单调上升 | 0.444 < 1.217 < 3.852 | PASS |
| Sol 随域尺度单调上升 | 0.058 < 1.230 < 10.421 | PASS |

