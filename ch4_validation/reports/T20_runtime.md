# tab:runtime — 单轮计时与加速比

- 对象：`tab:runtime`（tab:runtime）
- 结论：**PASS** — 47 通过 / 0 失败 / 0 警告，共 47 项
- 脚本：`ch4_validation/scripts/T20_runtime.py`
- 生成：2026-07-29 01:07:03

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | Table None 环境 |
| xlsx 源 | `Data_and_Code_Availability/Raw_Experimental_Data/4.8_Performance/Case43-50_推理时间性能分析.xlsx` | Cases 43–44 运行时数据 |

## 1. 源数据完整性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 43 存在于 xlsx | 是 | PASS |
| Case 43 COMSOL 数据存在 | 是 | PASS |
| Case 43 1 GPU 数据存在 | 是 | PASS |
| Case 43 2 GPU 数据存在 | 是 | PASS |
| Case 43 4 GPU 数据存在 | 是 | PASS |
| Case 44 存在于 xlsx | 是 | PASS |
| Case 44 COMSOL 数据存在 | 是 | PASS |
| Case 44 1 GPU 数据存在 | 是 | PASS |
| Case 44 2 GPU 数据存在 | 是 | PASS |
| Case 44 4 GPU 数据存在 | 是 | PASS |

## 2. tex 表格结构

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 表格环境可定位且确实包住 label | `tab:runtime`，长度 1213 | PASS |
| tex 数据行数 = 8 | 实得 8 | PASS |

## 3. 印刷值比对（源值舍入到 2 位 vs tex）

> 运行时数据精度：Time(ms) 2 位、Thr.(samp/s) 2 位、Speed-up 2 位。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 43 COMSOL Time | 源 873.1 → `873.10` / 印刷 `873.10` | PASS |
| Case 43 COMSOL Thr. | 源 1.15 → `1.15` / 印刷 `1.15` | PASS |
| Case 43 COMSOL Speed-up = 1× | 印刷 `1$x$` | PASS |
| Case 43 1 GPU Time | 源 17.08 → `17.08` / 印刷 `17.08` | PASS |
| Case 43 1 GPU Thr. | 源 52.82 → `52.82` / 印刷 `52.82` | PASS |
| Case 43 1 GPU Speed-up | 源 45.9304347826087 → `45.93` / 印刷 `45.93` | PASS |
| Case 43 2 GPU Time | 源 17.64 → `17.64` / 印刷 `17.64` | PASS |
| Case 43 2 GPU Thr. | 源 98.22 → `98.22` / 印刷 `98.22` | PASS |
| Case 43 2 GPU Speed-up | 源 85.40869565217392 → `85.41` / 印刷 `85.41` | PASS |
| Case 43 4 GPU Time | 源 18.28 → `18.28` / 印刷 `18.28` | PASS |
| Case 43 4 GPU Thr. | 源 163.78 → `163.78` / 印刷 `163.78` | PASS |
| Case 43 4 GPU Speed-up | 源 142.41739130434783 → `142.42` / 印刷 `142.42` | PASS |
| Case 44 COMSOL Time | 源 503.0 → `503.00` / 印刷 `503.00` | PASS |
| Case 44 COMSOL Thr. | 源 1.99 → `1.99` / 印刷 `1.99` | PASS |
| Case 44 COMSOL Speed-up = 1× | 印刷 `1$x$` | PASS |
| Case 44 1 GPU Time | 源 14.04 → `14.04` / 印刷 `14.04` | PASS |
| Case 44 1 GPU Thr. | 源 62.42 → `62.42` / 印刷 `62.42` | PASS |
| Case 44 1 GPU Speed-up | 源 31.366834170854272 → `31.37` / 印刷 `31.37` | PASS |
| Case 44 2 GPU Time | 源 14.15 → `14.15` / 印刷 `14.15` | PASS |
| Case 44 2 GPU Thr. | 源 120.35 → `120.35` / 印刷 `120.35` | PASS |
| Case 44 2 GPU Speed-up | 源 60.47738693467336 → `60.48` / 印刷 `60.48` | PASS |
| Case 44 4 GPU Time | 源 14.74 → `14.74` / 印刷 `14.74` | PASS |
| Case 44 4 GPU Thr. | 源 211.77 → `211.77` / 印刷 `211.77` | PASS |
| Case 44 4 GPU Speed-up | 源 106.41708542713569 → `106.42` / 印刷 `106.42` | PASS |

## 4. 正文引用精确性（4.8 节）

> 验证正文段落中引用的数值与表格/源数据一致。Speed-up 为派生计算。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 43 1 GPU Time | 源 17.08 → `17.08` / 印刷 `17.08` | PASS |
| Case 44 1 GPU Time | 源 14.04 → `14.04` / 印刷 `14.04` | PASS |
| Case 43 COMSOL Time | 源 873.1 → `873.10` / 印刷 `873.10` | PASS |
| Case 44 COMSOL Time | 源 503.0 → `503.00` / 印刷 `503.00` | PASS |
| Case 43 1 GPU Speed-up | 源 45.9304347826087 → `45.93` / 印刷 `45.93` | PASS |
| Case 44 1 GPU Speed-up | 源 31.366834170854272 → `31.37` / 印刷 `31.37` | PASS |
| Case 43 1 GPU Thr. | 源 52.82 → `52.82` / 印刷 `52.82` | PASS |
| Case 43 2 GPU Thr. | 源 98.22 → `98.22` / 印刷 `98.22` | PASS |
| Case 43 4 GPU Thr. | 源 163.78 → `163.78` / 印刷 `163.78` | PASS |
| Case 43 4 GPU Speed-up | 源 142.41739130434783 → `142.42` / 印刷 `142.42` | PASS |
| Case 44 4 GPU Speed-up | 源 106.41708542713569 → `106.42` / 印刷 `106.42` | PASS |

