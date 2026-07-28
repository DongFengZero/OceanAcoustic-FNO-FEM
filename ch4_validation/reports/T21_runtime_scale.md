# tab:runtime-scale — 跨域尺度推理耗时

- 对象：`tab:runtime-scale`（tab:runtime-scale）
- 结论：**PASS** — 41 通过 / 0 失败 / 0 警告，共 41 项
- 脚本：`ch4_validation/scripts/T21_runtime_scale.py`
- 生成：2026-07-29 00:26:22

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | Table None 环境 |
| xlsx 源 | `Data_and_Code_Availability/Raw_Experimental_Data/4.8_Performance/Case43-50_推理时间性能分析.xlsx` | Cases 45–50 域尺度缩放数据 |

## 1. 源数据完整性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 45 存在于 xlsx | 是 | PASS |
| Case 46 存在于 xlsx | 是 | PASS |
| Case 47 存在于 xlsx | 是 | PASS |
| Case 48 存在于 xlsx | 是 | PASS |
| Case 49 存在于 xlsx | 是 | PASS |
| Case 50 存在于 xlsx | 是 | PASS |

## 2. tex 表格结构

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 表格环境可定位且确实包住 label | `tab:runtime-scale`，长度 697 | PASS |
| tex 数据行数 = 6 | 实得 6 | PASS |
| tex 行 No. 覆盖 45-50 | [45, 46, 47, 48, 49, 50] | PASS |

## 3. 印刷值比对（源值舍入到 2 位 vs tex）

> 列：Case, Dataset, Lx(m), N(节点数), Time(ms)。Time 精度 2 位。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 45 Dataset 名 | tex `R4` | PASS |
| Case 45 Lx | 源 128 / 印刷 `128` | PASS |
| Case 45 N | 源 21737 → `21,737` / 印刷 `21,737` | PASS |
| Case 45 Time | 源 47.02 → `47.02` / 印刷 `47.02` | PASS |
| Case 46 Dataset 名 | tex `R5` | PASS |
| Case 46 Lx | 源 256 / 印刷 `256` | PASS |
| Case 46 N | 源 85353 → `85,353` / 印刷 `85,353` | PASS |
| Case 46 Time | 源 85.86 → `85.86` / 印刷 `85.86` | PASS |
| Case 47 Dataset 名 | tex `R6` | PASS |
| Case 47 Lx | 源 512 / 印刷 `512` | PASS |
| Case 47 N | 源 337351 → `337,351` / 印刷 `337,351` | PASS |
| Case 47 Time | 源 249.53 → `249.53` / 印刷 `249.53` | PASS |
| Case 48 Dataset 名 | tex `W4` | PASS |
| Case 48 Lx | 源 128 / 印刷 `128` | PASS |
| Case 48 N | 源 10680 → `10,680` / 印刷 `10,680` | PASS |
| Case 48 Time | 源 40.1 → `40.10` / 印刷 `40.10` | PASS |
| Case 49 Dataset 名 | tex `W5` | PASS |
| Case 49 Lx | 源 256 / 印刷 `256` | PASS |
| Case 49 N | 源 41633 → `41,633` / 印刷 `41,633` | PASS |
| Case 49 Time | 源 58.24 → `58.24` / 印刷 `58.24` | PASS |
| Case 50 Dataset 名 | tex `W6` | PASS |
| Case 50 Lx | 源 512 / 印刷 `512` | PASS |
| Case 50 N | 源 165034 → `165,034` / 印刷 `165,034` | PASS |
| Case 50 Time | 源 132.41 → `132.41` / 印刷 `132.41` | PASS |

## 4. 正文引用精确性（4.8 节）

> 验证正文段落中引用的数值与表格/源数据一致。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 45 (R4) N | 源 21737 → `21,737` / 正文 `21,737` | PASS |
| Case 47 (R6) N | 源 337351 → `337,351` / 正文 `337,351` | PASS |
| Case 48 (W4) N | 源 10680 → `10,680` / 正文 `10,680` | PASS |
| Case 50 (W6) N | 源 165034 → `165,034` / 正文 `165,034` | PASS |
| Case 45 (R4) Time | 源 47.02 → `47.02` / 印刷 `47.02` | PASS |
| Case 47 (R6) Time | 源 249.53 → `249.53` / 印刷 `249.53` | PASS |
| Case 48 (W4) Time | 源 40.1 → `40.10` / 印刷 `40.10` | PASS |
| Case 50 (W6) Time | 源 132.41 → `132.41` / 印刷 `132.41` | PASS |

