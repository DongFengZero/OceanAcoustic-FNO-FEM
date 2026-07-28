# Table 8 — 100Hz 方形域 楔形 W4-W6

- 对象：`tab:res-wedge-100`（Table 8）
- 结论：**PASS** — 90 通过 / 0 失败 / 0 警告，共 90 项
- 脚本：`ch4_validation/scripts/T08_res_wedge_100.py`
- 生成：2026-07-29 00:25:43

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:res-wedge-100}` 所在 minipage |
| 渠道1 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/Case3-14_数据汇总.xlsx` | 工作表1，best epoch 全测试集 |
| 渠道2 log (Case 12) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No12_W4/training_run/logs/full_run_20260710_150948.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 13) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No13_W5/training_run/logs/full_run_20260710_122002.log` | 训练日志同轮『评估』块 |
| 渠道2 log (Case 14) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No14_W6/training_run/logs/full_run_20260710_024405.log` | 训练日志同轮『评估』块 |
| 复用比对 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/Case33-38_数据汇总.xlsx` | 4.6 节汇总，用于确认 Case 36≡12 |

## 2. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| xlsx 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/Case3-14_数据汇总.xlsx | PASS |
| Case 12 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No12_W4/training_run/logs/full_run_20260710_150948.log | PASS |
| Case 13 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No13_W5/training_run/logs/full_run_20260710_122002.log | PASS |
| Case 14 日志存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No14_W6/training_run/logs/full_run_20260710_024405.log | PASS |
| tex 表格环境可定位且确实包住 label | 长度 798 | PASS |
| tex 数据行数 = 3 | 实得 3 | PASS |
| tex 行 No. 覆盖 Case 12-14 | [12, 13, 14] | PASS |

## 3. best epoch 一致性

> 本组 best epoch 为 {12: 195, 13: 193, 14: 129}。Case 14 的 129 明显早于另两例，是该次训练的验证损失确实在 129 轮触底（日志自证一致），不是漏取或截断；记此一笔以免后人误判。

| 案例 | xlsx / 日志自证 | 结论 |
|---|---|---|
| Case 12 best epoch | xlsx `195` / log `195` | PASS |
| Case 12 日志含『评估 Epoch 195』块 | 轮次 195 | PASS |
| Case 13 best epoch | xlsx `193` / log `193` | PASS |
| Case 13 日志含『评估 Epoch 193』块 | 轮次 193 | PASS |
| Case 14 best epoch | xlsx `129` / log `129` | PASS |
| Case 14 日志含『评估 Epoch 129』块 | 轮次 129 | PASS |
| 三例 best epoch 均落在 1–200 合法区间 | [129, 193, 195] | PASS |

## 4. 双渠道交叉验证（xlsx vs log）

| 量 | xlsx / log | 结论 |
|---|---|---|
| Case 12 Overall SOL | `0.10030982230091469` / `0.10030979999999999` | PASS |
| Case 12 Overall TL | `0.6095095` / `0.6095095` | PASS |
| Case 12 100 SOL | `0.10030982230091469` / `0.10030979000000001` | PASS |
| Case 12 100 TL | `0.6095095` / `0.6095095` | PASS |
| Case 13 Overall SOL | `1.225514244288206` / `1.225515` | PASS |
| Case 13 Overall TL | `0.9301047` / `0.9301047` | PASS |
| Case 13 100 SOL | `1.225514244288206` / `1.225515` | PASS |
| Case 13 100 TL | `0.9301047` / `0.9301047` | PASS |
| Case 14 Overall SOL | `16.11375892534852` / `16.113760000000003` | PASS |
| Case 14 Overall TL | `3.407047` / `3.407047` | PASS |
| Case 14 100 SOL | `16.11375892534852` / `16.1137559` | PASS |
| Case 14 100 TL | `3.407047` / `3.407047` | PASS |

## 5. 单频自洽性

> 单频案例 Overall 组须等于 100Hz 组，且 25/50/75Hz 为空。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 12 Overall SOL == 100Hz SOL | `0.10030982230091469` == `0.10030982230091469` | PASS |
| Case 12 Overall TL == 100Hz TL | `0.6095095` == `0.6095095` | PASS |
| Case 12 25/50/75Hz 均为空 | 空的频率 [25, 50, 75] | PASS |
| Case 13 Overall SOL == 100Hz SOL | `1.225514244288206` == `1.225514244288206` | PASS |
| Case 13 Overall TL == 100Hz TL | `0.9301047` == `0.9301047` | PASS |
| Case 13 25/50/75Hz 均为空 | 空的频率 [25, 50, 75] | PASS |
| Case 14 Overall SOL == 100Hz SOL | `16.11375892534852` == `16.11375892534852` | PASS |
| Case 14 Overall TL == 100Hz TL | `3.407047` == `3.407047` | PASS |
| Case 14 25/50/75Hz 均为空 | 空的频率 [25, 50, 75] | PASS |

## 6. 印刷值比对（源值舍入到 3 位 vs tex）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 12 Dataset 名 | tex `W4` | PASS |
| Case 12 Lx×Ly 印刷值 | tex `128x128` / 期望 `128x128` | PASS |
| Case 12 Lx/Ly 与 xlsx 一致 | xlsx `128×128` | PASS |
| Case 12 SOL (xlsx) | 源 0.10030982230091469 → `0.100` / 印刷 `0.100` | PASS |
| Case 12 SOL (log) | 源 0.10030979000000001 → `0.100` / 印刷 `0.100` | PASS |
| Case 12 TL (xlsx) | 源 0.6095095 → `0.610` / 印刷 `0.610` | PASS |
| Case 12 TL (log) | 源 0.6095095 → `0.610` / 印刷 `0.610` | PASS |
| Case 13 Dataset 名 | tex `W5` | PASS |
| Case 13 Lx×Ly 印刷值 | tex `256x256` / 期望 `256x256` | PASS |
| Case 13 Lx/Ly 与 xlsx 一致 | xlsx `256×256` | PASS |
| Case 13 SOL (xlsx) | 源 1.225514244288206 → `1.226` / 印刷 `1.226` | PASS |
| Case 13 SOL (log) | 源 1.225515 → `1.226` / 印刷 `1.226` | PASS |
| Case 13 TL (xlsx) | 源 0.9301047 → `0.930` / 印刷 `0.930` | PASS |
| Case 13 TL (log) | 源 0.9301047 → `0.930` / 印刷 `0.930` | PASS |
| Case 14 Dataset 名 | tex `W6` | PASS |
| Case 14 Lx×Ly 印刷值 | tex `512x512` / 期望 `512x512` | PASS |
| Case 14 Lx/Ly 与 xlsx 一致 | xlsx `512×512` | PASS |
| Case 14 SOL (xlsx) | 源 16.11375892534852 → `16.114` / 印刷 `16.114` | PASS |
| Case 14 SOL (log) | 源 16.1137559 → `16.114` / 印刷 `16.114` | PASS |
| Case 14 TL (xlsx) | 源 3.407047 → `3.407` / 印刷 `3.407` | PASS |
| Case 14 TL (log) | 源 3.407047 → `3.407` / 印刷 `3.407` | PASS |

## 7. Fig. 列引用正确性

> 楔形三行须各自指向 `fig:res-wedge-100` 的 -10/-11/-12 子图；子图后缀沿用案例序号而非 1/2/3，错配不会报编译错，只能靠比对发现。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 12 Fig. 列引用 | tex `\ref{fig:res-wedge-100}\subref{fig:res-wedge-100-10}` → ['fig:res-wedge-100', 'fig:res-wedge-100-10'] | PASS |
| label `fig:res-wedge-100` 已在 aux 注册 | 编号 `9` | PASS |
| label `fig:res-wedge-100-10` 已在 aux 注册 | 编号 `9a` | PASS |
| Case 13 Fig. 列引用 | tex `\ref{fig:res-wedge-100}\subref{fig:res-wedge-100-11}` → ['fig:res-wedge-100', 'fig:res-wedge-100-11'] | PASS |
| label `fig:res-wedge-100` 已在 aux 注册 | 编号 `9` | PASS |
| label `fig:res-wedge-100-11` 已在 aux 注册 | 编号 `9b` | PASS |
| Case 14 Fig. 列引用 | tex `\ref{fig:res-wedge-100}\subref{fig:res-wedge-100-12}` → ['fig:res-wedge-100', 'fig:res-wedge-100-12'] | PASS |
| label `fig:res-wedge-100` 已在 aux 注册 | 编号 `9` | PASS |
| label `fig:res-wedge-100-12` 已在 aux 注册 | 编号 `9c` | PASS |

## 8. 与 Table 7 的版式一致性

> Table 7/8 并列在同一 `table*` 的左右 minipage 内，列定义与表头必须逐字符相同，否则两表不等宽、无法左右对读。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 列定义 (tabular preamble)与 Table 7 相同 | Table 8 `@{}ll c ccc@{}` / Table 7 `@{}ll c ccc@{}` | PASS |
| 表头行与 Table 7 相同 | Table 8 `No. & Dataset & Fig. & $L_x\times L_y$\,(m) & Sol & TL\,(dB) \\` / Table 7 `No. & Dataset & Fig. & $L_x\times L_y$\,(m) & Sol & TL\,(dB) \\` | PASS |
| 两表同用 \TABstyle |  | PASS |
| Table 8 表内无与 caption 重复的单位脚注 | 已于 2026-07-28 删除 | PASS |
| Table 7 表内无与 caption 重复的单位脚注 | 已于 2026-07-28 删除 | PASS |

## 9. 与 4.6 节的复用关系

> 4.6 网格研究的最粗一档就是本节的单频案例：Case 36 复用 Case 12、Case 33 复用 Case 6。判定不看三位小数是否相同（那可能是巧合），而要求 best epoch 与全精度值都一致，才算同一次运行。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 36 与 Case 12 best epoch 相同 | `195` == `195` | PASS |
| Case 36 与 Case 12 SOL 全精度相同 | `0.10030982230091469` == `0.10030982230091469` | PASS |
| Case 36 与 Case 12 TL 全精度相同 | `0.6095095` == `0.6095095` | PASS |
| Case 33 与 Case 6 best epoch 相同 | `192` == `192` | PASS |
| Case 33 与 Case 6 SOL 全精度相同 | `0.0577102506213123` == `0.0577102506213123` | PASS |
| Case 33 与 Case 6 TL 全精度相同 | `0.4443021` == `0.4443021` | PASS |

## 10. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 6 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 11. 正文引用精确性（4.3 节）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 Case 12 Sol | 正文 `0.100` / 表格 `0.100` | PASS |
| 正文 Case 12 Sol ← xlsx 源 | 源 0.10030982230091469 → `0.100` / 印刷 `0.100` | PASS |
| 正文 Case 12 TL | 正文 `0.610` / 表格 `0.610` | PASS |
| 正文 Case 12 TL ← xlsx 源 | 源 0.6095095 → `0.610` / 印刷 `0.610` | PASS |
| 正文 Case 13 TL | 正文 `0.930` / 表格 `0.930` | PASS |
| 正文 Case 13 TL ← xlsx 源 | 源 0.9301047 → `0.930` / 印刷 `0.930` | PASS |
| 正文 Case 14 TL | 正文 `3.407` / 表格 `3.407` | PASS |
| 正文 Case 14 TL ← xlsx 源 | 源 3.407047 → `3.407` / 印刷 `3.407` | PASS |

## 12. 正文趋势断言

> 正文列出楔形单频 TL 递增序列 0.610 → 0.930 → 3.407，并称 128m 单频两例是全体中最准的。

> 『单频 128m 最准』是跨表断言：需在 4.3 全部 12 例中比较，而不只是本表 3 例。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| TL 随域尺度单调上升 | 0.610 < 0.930 < 3.407 | PASS |
| Sol 随域尺度单调上升 | 0.100 < 1.226 < 16.114 | PASS |
| 正文递增序列可定位 | tex 行 811 | PASS |
| Cases 6/12 的 TL 是 12 例中最小的两个 | 最小 Case 6 (`0.444`)、次小 Case 12 (`0.610`) | PASS |

## X. Caption epoch 声明核验

> 本表数据来自 best epoch（从 log 读取），caption 应声明 'best epoch'。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 best epoch | 本表源自 log 的 best epoch，非 last epoch | PASS |

