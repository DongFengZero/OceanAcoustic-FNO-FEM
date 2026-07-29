# Table 17 — 网格无关性 矩形

- 对象：`tab:mesh-rect`（Table 17）
- 结论：**PASS** — 55 通过 / 0 失败 / 0 警告，共 55 项
- 脚本：`ch4_validation/scripts/T17_mesh_rect.py`
- 生成：2026-07-30 00:04:11

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:mesh-rect}` 所在 table* 环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/Case33-38_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 33) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No33_R4/training_run/logs/full_run_20260710_224527.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 34) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No34_R7/training_run/logs/full_run_20260710_220203.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 35) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No35_R8/training_run/logs/full_run_20260710_025319.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/Case33-38_数据汇总.xlsx | PASS |
| Case 33 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No33_R4/training_run/logs/full_run_20260710_224527.log | PASS |
| Case 34 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No34_R7/training_run/logs/full_run_20260710_220203.log | PASS |
| Case 35 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No35_R8/training_run/logs/full_run_20260710_025319.log | PASS |
| tex 表格环境可定位且确实包住 label | `tab:mesh-rect`，长度 786 | PASS |
| tex 数据行数 = 3 | 实得 3 | PASS |
| tex 行 No. 覆盖 33-35 | [33, 34, 35] | PASS |

## 3. best epoch 一致性

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 33 best epoch | xlsx `192` / log `192` | PASS |
| Case 33 日志含『评估 Epoch 192』块 | 轮次 192 | PASS |
| Case 34 best epoch | xlsx `200` / log `200` | PASS |
| Case 34 日志含『评估 Epoch 200』块 | 轮次 200 | PASS |
| Case 35 best epoch | xlsx `167` / log `167` | PASS |
| Case 35 日志含『评估 Epoch 167』块 | 轮次 167 | PASS |

## 4. 双渠道交叉验证（xlsx vs log，同一 best epoch）

> 日志侧取『评估 Epoch N 完成』块（测试集），非『训练』块；Sol 由 `(损失 − w_prior×prior)/w_rel` 现场算，权重逐轮解析。

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 33 100Hz SOL | `0.0577102506213123` / `0.057710252` | PASS |
| Case 33 100Hz TL | `0.4443021` / `0.4443021` | PASS |
| Case 34 100Hz SOL | `0.13098313575028442` / `0.130983092` | PASS |
| Case 34 100Hz TL | `0.3843261` / `0.3843261` | PASS |
| Case 35 100Hz SOL | `0.2871782717193128` / `0.287178317` | PASS |
| Case 35 100Hz TL | `0.3925595` / `0.3925595` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Dataset, Δ, Fig., Sol, TL。本表只有 100 Hz。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 Dataset 名 | tex `R4` | PASS |
| Case 33 100Hz SOL (xlsx) | 源 0.0577102506213123 → `0.058` / 印刷 `0.058` | PASS |
| Case 33 100Hz SOL (log) | 源 0.057710252 → `0.058` / 印刷 `0.058` | PASS |
| Case 33 100Hz TL (xlsx) | 源 0.4443021 → `0.444` / 印刷 `0.444` | PASS |
| Case 33 100Hz TL (log) | 源 0.4443021 → `0.444` / 印刷 `0.444` | PASS |
| Case 34 Dataset 名 | tex `R7` | PASS |
| Case 34 100Hz SOL (xlsx) | 源 0.13098313575028442 → `0.131` / 印刷 `0.131` | PASS |
| Case 34 100Hz SOL (log) | 源 0.130983092 → `0.131` / 印刷 `0.131` | PASS |
| Case 34 100Hz TL (xlsx) | 源 0.3843261 → `0.384` / 印刷 `0.384` | PASS |
| Case 34 100Hz TL (log) | 源 0.3843261 → `0.384` / 印刷 `0.384` | PASS |
| Case 35 Dataset 名 | tex `R8` | PASS |
| Case 35 100Hz SOL (xlsx) | 源 0.2871782717193128 → `0.287` / 印刷 `0.287` | PASS |
| Case 35 100Hz SOL (log) | 源 0.287178317 → `0.287` / 印刷 `0.287` | PASS |
| Case 35 100Hz TL (xlsx) | 源 0.3925595 → `0.393` / 印刷 `0.393` | PASS |
| Case 35 100Hz TL (log) | 源 0.3925595 → `0.393` / 印刷 `0.393` | PASS |

## 6. Fig. 列引用正确性

> 每行的图号必须指向该案例自己的图与子图。同时确认被引 label 在 aux 里存在（否则排出 `??`）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 Fig. 列引用 | tex `\ref{fig:mesh-rect}\subref{fig:mesh-rect-a}` → ['fig:mesh-rect', 'fig:mesh-rect-a']，应为 `[fig:mesh-rect, fig:mesh-rect-a]` | PASS |
| label `fig:mesh-rect` 已在 aux 注册 | 编号 `18` | PASS |
| label `fig:mesh-rect-a` 已在 aux 注册 | 编号 `18a` | PASS |
| Case 34 Fig. 列引用 | tex `\ref{fig:mesh-rect}\subref{fig:mesh-rect-b}` → ['fig:mesh-rect', 'fig:mesh-rect-b']，应为 `[fig:mesh-rect, fig:mesh-rect-b]` | PASS |
| label `fig:mesh-rect` 已在 aux 注册 | 编号 `18` | PASS |
| label `fig:mesh-rect-b` 已在 aux 注册 | 编号 `18b` | PASS |
| Case 35 Fig. 列引用 | tex `\ref{fig:mesh-rect}\subref{fig:mesh-rect-c}` → ['fig:mesh-rect', 'fig:mesh-rect-c']，应为 `[fig:mesh-rect, fig:mesh-rect-c]` | PASS |
| label `fig:mesh-rect` 已在 aux 注册 | 编号 `18` | PASS |
| label `fig:mesh-rect-c` 已在 aux 注册 | 编号 `18c` | PASS |

## 7. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 6 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 7. 正文引用精确性（4.6 节）

> 验证正文段落中引用的数值与表格/源数据一致。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 (Δ=1.00) Sol | 正文 `0.058` / 表格 `0.058` | PASS |
| Case 33 (Δ=1.00) Sol <- xlsx 源 | 源 0.0577102506213123 → `0.058` / 印刷 `0.058` | PASS |
| Case 35 (Δ=0.25) Sol | 正文 `0.287` / 表格 `0.287` | PASS |
| Case 35 (Δ=0.25) Sol <- xlsx 源 | 源 0.2871782717193128 → `0.287` / 印刷 `0.287` | PASS |
| Case 33 (Δ=1.00) TL | 正文 `0.444` / 表格 `0.444` | PASS |
| Case 33 (Δ=1.00) TL <- xlsx 源 | 源 0.4443021 → `0.444` / 印刷 `0.444` | PASS |
| Case 34 (Δ=0.50) TL | 正文 `0.384` / 表格 `0.384` | PASS |
| Case 34 (Δ=0.50) TL <- xlsx 源 | 源 0.3843261 → `0.384` / 印刷 `0.384` | PASS |
| Case 35 (Δ=0.25) TL | 正文 `0.393` / 表格 `0.393` | PASS |
| Case 35 (Δ=0.25) TL <- xlsx 源 | 源 0.3925595 → `0.393` / 印刷 `0.393` | PASS |

## X. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

