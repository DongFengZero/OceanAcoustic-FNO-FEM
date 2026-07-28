# Table 18 — 网格无关性 楔形

- 对象：`tab:mesh-wedge`（Table 18）
- 结论：**PASS** — 55 通过 / 0 失败 / 0 警告，共 55 项
- 脚本：`ch4_validation/scripts/T18_mesh_wedge.py`
- 生成：2026-07-28 20:30:09

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:mesh-wedge}` 所在 table* 环境 |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/Case33-38_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 36) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No36_W4/training_run/logs/full_run_20260710_150948.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 37) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No37_W7/training_run/logs/full_run_20260710_123333.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 38) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No38_W8/training_run/logs/full_run_20260710_030023.log` | 训练日志同轮『评估』块 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/Case33-38_数据汇总.xlsx | PASS |
| Case 36 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No36_W4/training_run/logs/full_run_20260710_150948.log | PASS |
| Case 37 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No37_W7/training_run/logs/full_run_20260710_123333.log | PASS |
| Case 38 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No38_W8/training_run/logs/full_run_20260710_030023.log | PASS |
| tex 表格环境可定位且确实包住 label | `tab:mesh-wedge`，长度 787 | PASS |
| tex 数据行数 = 3 | 实得 3 | PASS |
| tex 行 No. 覆盖 36-38 | [36, 37, 38] | PASS |

## 3. best epoch 一致性

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 36 best epoch | xlsx `195` / log `195` | PASS |
| Case 36 日志含『评估 Epoch 195』块 | 轮次 195 | PASS |
| Case 37 best epoch | xlsx `199` / log `199` | PASS |
| Case 37 日志含『评估 Epoch 199』块 | 轮次 199 | PASS |
| Case 38 best epoch | xlsx `194` / log `194` | PASS |
| Case 38 日志含『评估 Epoch 194』块 | 轮次 194 | PASS |

## 4. 双渠道交叉验证（xlsx vs log，同一 best epoch）

> 日志侧取『评估 Epoch N 完成』块（测试集），非『训练』块；Sol 由 `(损失 − w_prior×prior)/w_rel` 现场算，权重逐轮解析。

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 36 100Hz SOL | `0.10030982230091469` / `0.10030979000000001` | PASS |
| Case 36 100Hz TL | `0.6095095` / `0.6095095` | PASS |
| Case 37 100Hz SOL | `0.19601167878136042` / `0.19601165` | PASS |
| Case 37 100Hz TL | `0.3608499` / `0.3608499` | PASS |
| Case 38 100Hz SOL | `0.3259683660871815` / `0.32596840000000005` | PASS |
| Case 38 100Hz TL | `0.3113609` / `0.3113609` | PASS |

## 5. 印刷值比对（源值舍入到 3 位 vs tex）

> 列序：No., Dataset, Δ, Fig., Sol, TL。本表只有 100 Hz。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 36 Dataset 名 | tex `W4` | PASS |
| Case 36 100Hz SOL (xlsx) | 源 0.10030982230091469 → `0.100` / 印刷 `0.100` | PASS |
| Case 36 100Hz SOL (log) | 源 0.10030979000000001 → `0.100` / 印刷 `0.100` | PASS |
| Case 36 100Hz TL (xlsx) | 源 0.6095095 → `0.610` / 印刷 `0.610` | PASS |
| Case 36 100Hz TL (log) | 源 0.6095095 → `0.610` / 印刷 `0.610` | PASS |
| Case 37 Dataset 名 | tex `W7` | PASS |
| Case 37 100Hz SOL (xlsx) | 源 0.19601167878136042 → `0.196` / 印刷 `0.196` | PASS |
| Case 37 100Hz SOL (log) | 源 0.19601165 → `0.196` / 印刷 `0.196` | PASS |
| Case 37 100Hz TL (xlsx) | 源 0.3608499 → `0.361` / 印刷 `0.361` | PASS |
| Case 37 100Hz TL (log) | 源 0.3608499 → `0.361` / 印刷 `0.361` | PASS |
| Case 38 Dataset 名 | tex `W8` | PASS |
| Case 38 100Hz SOL (xlsx) | 源 0.3259683660871815 → `0.326` / 印刷 `0.326` | PASS |
| Case 38 100Hz SOL (log) | 源 0.32596840000000005 → `0.326` / 印刷 `0.326` | PASS |
| Case 38 100Hz TL (xlsx) | 源 0.3113609 → `0.311` / 印刷 `0.311` | PASS |
| Case 38 100Hz TL (log) | 源 0.3113609 → `0.311` / 印刷 `0.311` | PASS |

## 6. Fig. 列引用正确性

> 每行的图号必须指向该案例自己的图与子图。同时确认被引 label 在 aux 里存在（否则排出 `??`）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 36 Fig. 列引用 | tex `\ref{fig:mesh-wedge}\subref{fig:mesh-wedge-a}` → ['fig:mesh-wedge', 'fig:mesh-wedge-a']，应为 `[fig:mesh-wedge, fig:mesh-wedge-a]` | PASS |
| label `fig:mesh-wedge` 已在 aux 注册 | 编号 `19` | PASS |
| label `fig:mesh-wedge-a` 已在 aux 注册 | 编号 `19a` | PASS |
| Case 37 Fig. 列引用 | tex `\ref{fig:mesh-wedge}\subref{fig:mesh-wedge-b}` → ['fig:mesh-wedge', 'fig:mesh-wedge-b']，应为 `[fig:mesh-wedge, fig:mesh-wedge-b]` | PASS |
| label `fig:mesh-wedge` 已在 aux 注册 | 编号 `19` | PASS |
| label `fig:mesh-wedge-b` 已在 aux 注册 | 编号 `19b` | PASS |
| Case 38 Fig. 列引用 | tex `\ref{fig:mesh-wedge}\subref{fig:mesh-wedge-c}` → ['fig:mesh-wedge', 'fig:mesh-wedge-c']，应为 `[fig:mesh-wedge, fig:mesh-wedge-c]` | PASS |
| label `fig:mesh-wedge` 已在 aux 注册 | 编号 `19` | PASS |
| label `fig:mesh-wedge-c` 已在 aux 注册 | 编号 `19c` | PASS |

## 7. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 6 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 7. 正文引用精确性（4.6 节）

> 验证正文段落中引用的数值与表格/源数据一致。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 36 (Δ=1.00) Sol | 正文 `0.100` / 表格 `0.100` | PASS |
| Case 36 (Δ=1.00) Sol <- xlsx 源 | 源 0.10030982230091469 → `0.100` / 印刷 `0.100` | PASS |
| Case 38 (Δ=0.25) Sol | 正文 `0.326` / 表格 `0.326` | PASS |
| Case 38 (Δ=0.25) Sol <- xlsx 源 | 源 0.3259683660871815 → `0.326` / 印刷 `0.326` | PASS |
| Case 36 (Δ=1.00) TL | 正文 `0.610` / 表格 `0.610` | PASS |
| Case 36 (Δ=1.00) TL <- xlsx 源 | 源 0.6095095 → `0.610` / 印刷 `0.610` | PASS |
| Case 37 (Δ=0.50) TL | 正文 `0.361` / 表格 `0.361` | PASS |
| Case 37 (Δ=0.50) TL <- xlsx 源 | 源 0.3608499 → `0.361` / 印刷 `0.361` | PASS |
| Case 38 (Δ=0.25) TL | 正文 `0.311` / 表格 `0.311` | PASS |
| Case 38 (Δ=0.25) TL <- xlsx 源 | 源 0.3113609 → `0.311` / 印刷 `0.311` | PASS |

## X. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

