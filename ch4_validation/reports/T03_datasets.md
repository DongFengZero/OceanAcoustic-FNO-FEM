# tab:datasets — 数据集总表 No.1-50（结构性，非测量值）

- 对象：`tab:datasets`（tab:datasets）
- 结论：**PASS** — 423 通过 / 0 失败 / 0 警告，共 423 项
- 脚本：`ch4_validation/scripts/T03_datasets.py`
- 生成：2026-10-04 12:46:59

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | Table None 环境 |
| Dataset 目录 | `Data_and_Code_Availability/Dataset` | 22 个数据集配置 |

## 1. tex 表格结构

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 表格环境可定位且确实包住 label | `tab:datasets`，长度 8203 | PASS |
| tex 数据行数 = 50 | 实得 50 | PASS |
| tex 行 No. 覆盖 1-50 | 实得 [1, 2, 3, 4, 5]...[46, 47, 48, 49, 50] | PASS |

## 2. Dataset ID 一致性

> 与 Dataset 目录中的 22 个数据集标签比对。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 1 Dataset ID | tex `R0` / 预期 `R0` | PASS |
| Case 2 Dataset ID | tex `W0` / 预期 `W0` | PASS |
| Case 3 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 4 Dataset ID | tex `R2` / 预期 `R2` | PASS |
| Case 5 Dataset ID | tex `R3` / 预期 `R3` | PASS |
| Case 6 Dataset ID | tex `R4` / 预期 `R4` | PASS |
| Case 7 Dataset ID | tex `R5` / 预期 `R5` | PASS |
| Case 8 Dataset ID | tex `R6` / 预期 `R6` | PASS |
| Case 9 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 10 Dataset ID | tex `W2` / 预期 `W2` | PASS |
| Case 11 Dataset ID | tex `W3` / 预期 `W3` | PASS |
| Case 12 Dataset ID | tex `W4` / 预期 `W4` | PASS |
| Case 13 Dataset ID | tex `W5` / 预期 `W5` | PASS |
| Case 14 Dataset ID | tex `W6` / 预期 `W6` | PASS |
| Case 15 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 16 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 17 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 18 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 19 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 20 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 21 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 22 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 23 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 24 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 25 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 26 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 27 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 28 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 29 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 30 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 31 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 32 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 33 Dataset ID | tex `R4` / 预期 `R4` | PASS |
| Case 34 Dataset ID | tex `R7` / 预期 `R7` | PASS |
| Case 35 Dataset ID | tex `R8` / 预期 `R8` | PASS |
| Case 36 Dataset ID | tex `W4` / 预期 `W4` | PASS |
| Case 37 Dataset ID | tex `W7` / 预期 `W7` | PASS |
| Case 38 Dataset ID | tex `W8` / 预期 `W8` | PASS |
| Case 39 Dataset ID | tex `R9` / 预期 `R9` | PASS |
| Case 40 Dataset ID | tex `R10` / 预期 `R10` | PASS |
| Case 41 Dataset ID | tex `W9` / 预期 `W9` | PASS |
| Case 42 Dataset ID | tex `W10` / 预期 `W10` | PASS |
| Case 43 Dataset ID | tex `R1` / 预期 `R1` | PASS |
| Case 44 Dataset ID | tex `W1` / 预期 `W1` | PASS |
| Case 45 Dataset ID | tex `R4` / 预期 `R4` | PASS |
| Case 46 Dataset ID | tex `R5` / 预期 `R5` | PASS |
| Case 47 Dataset ID | tex `R6` / 预期 `R6` | PASS |
| Case 48 Dataset ID | tex `W4` / 预期 `W4` | PASS |
| Case 49 Dataset ID | tex `W5` / 预期 `W5` | PASS |
| Case 50 Dataset ID | tex `W6` / 预期 `W6` | PASS |

## 3. 几何类型一致性

> Rect. / Wedge 与 Dataset ID 前缀（R/W）一致。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 1 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 2 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 3 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 4 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 5 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 6 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 7 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 8 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 9 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 10 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 11 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 12 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 13 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 14 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 15 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 16 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 17 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 18 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 19 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 20 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 21 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 22 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 23 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 24 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 25 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 26 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 27 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 28 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 29 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 30 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 31 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 32 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 33 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 34 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 35 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 36 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 37 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 38 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 39 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 40 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 41 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 42 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 43 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 44 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 45 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 46 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 47 Geom. | tex `Rect.` / 预期 `Rect.` | PASS |
| Case 48 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 49 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |
| Case 50 Geom. | tex `Wedge` / 预期 `Wedge` | PASS |

## 4. 配置参数验证（Lx, Ly, Δ, Obstacle）

> 从 Dataset 目录读取 mesh 和 manifest 文件，验证印刷值。

> 成功加载 22/22 个数据集配置。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 1 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 1 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 1 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 1 Obstacle (无) | 印刷 `--` | PASS |
| Case 2 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 2 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 2 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 2 Obstacle (无) | 印刷 `--` | PASS |
| Case 3 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 3 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 3 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 3 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 4 Lx | 源 256.0 / 印刷 `256` | PASS |
| Case 4 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 4 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 4 Obstacle | 源 (128,64,32,8) / 印刷 `(128,64,32,8)` | PASS |
| Case 5 Lx | 源 512.0 / 印刷 `512` | PASS |
| Case 5 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 5 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 5 Obstacle | 源 (256,64,64,8) / 印刷 `(256,64,64,8)` | PASS |
| Case 6 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 6 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 6 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 6 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 7 Lx | 源 256.0 / 印刷 `256` | PASS |
| Case 7 Ly | 源 256.0 / 印刷 `256` | PASS |
| Case 7 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 7 Obstacle | 源 (128,128,32,16) / 印刷 `(128,128,32,16)` | PASS |
| Case 8 Lx | 源 512.0 / 印刷 `512` | PASS |
| Case 8 Ly | 源 512.0 / 印刷 `512` | PASS |
| Case 8 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 8 Obstacle | 源 (256,256,64,32) / 印刷 `(256,256,64,32)` | PASS |
| Case 9 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 9 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 9 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 9 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 10 Lx | 源 256.0 / 印刷 `256` | PASS |
| Case 10 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 10 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 10 Obstacle | 源 (192,32,32,8) / 印刷 `(192,32,32,8)` | PASS |
| Case 11 Lx | 源 512.0 / 印刷 `512` | PASS |
| Case 11 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 11 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 11 Obstacle | 源 (384,32,64,8) / 印刷 `(384,32,64,8)` | PASS |
| Case 12 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 12 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 12 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 12 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 13 Lx | 源 256.0 / 印刷 `256` | PASS |
| Case 13 Ly | 源 256.0 / 印刷 `256` | PASS |
| Case 13 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 13 Obstacle | 源 (192,64,32,16) / 印刷 `(192,64,32,16)` | PASS |
| Case 14 Lx | 源 512.0 / 印刷 `512` | PASS |
| Case 14 Ly | 源 512.0 / 印刷 `512` | PASS |
| Case 14 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 14 Obstacle | 源 (384,128,64,32) / 印刷 `(384,128,64,32)` | PASS |
| Case 15 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 15 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 15 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 15 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 16 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 16 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 16 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 16 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 17 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 17 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 17 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 17 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 18 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 18 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 18 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 18 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 19 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 19 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 19 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 19 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 20 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 20 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 20 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 20 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 21 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 21 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 21 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 21 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 22 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 22 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 22 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 22 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 23 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 23 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 23 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 23 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 24 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 24 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 24 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 24 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 25 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 25 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 25 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 25 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 26 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 26 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 26 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 26 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 27 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 27 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 27 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 27 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 28 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 28 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 28 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 28 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 29 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 29 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 29 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 29 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 30 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 30 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 30 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 30 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 31 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 31 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 31 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 31 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 32 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 32 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 32 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 32 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 33 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 33 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 33 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 33 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 34 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 34 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 34 Δ | 源 0.5 → `0.50` / 印刷 `0.50` | PASS |
| Case 34 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 35 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 35 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 35 Δ | 源 0.25 → `0.25` / 印刷 `0.25` | PASS |
| Case 35 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 36 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 36 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 36 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 36 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 37 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 37 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 37 Δ | 源 0.5 → `0.50` / 印刷 `0.50` | PASS |
| Case 37 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 38 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 38 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 38 Δ | 源 0.25 → `0.25` / 印刷 `0.25` | PASS |
| Case 38 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 39 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 39 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 39 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 39 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 40 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 40 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 40 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 40 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 41 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 41 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 41 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 41 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 42 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 42 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 42 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 42 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 43 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 43 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 43 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 43 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 44 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 44 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 44 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 44 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 45 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 45 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 45 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 45 Obstacle | 源 (64,64,16,8) / 印刷 `(64,64,16,8)` | PASS |
| Case 46 Lx | 源 256.0 / 印刷 `256` | PASS |
| Case 46 Ly | 源 256.0 / 印刷 `256` | PASS |
| Case 46 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 46 Obstacle | 源 (128,128,32,16) / 印刷 `(128,128,32,16)` | PASS |
| Case 47 Lx | 源 512.0 / 印刷 `512` | PASS |
| Case 47 Ly | 源 512.0 / 印刷 `512` | PASS |
| Case 47 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 47 Obstacle | 源 (256,256,64,32) / 印刷 `(256,256,64,32)` | PASS |
| Case 48 Lx | 源 128.0 / 印刷 `128` | PASS |
| Case 48 Ly | 源 128.0 / 印刷 `128` | PASS |
| Case 48 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 48 Obstacle | 源 (96,32,16,8) / 印刷 `(96,32,16,8)` | PASS |
| Case 49 Lx | 源 256.0 / 印刷 `256` | PASS |
| Case 49 Ly | 源 256.0 / 印刷 `256` | PASS |
| Case 49 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 49 Obstacle | 源 (192,64,32,16) / 印刷 `(192,64,32,16)` | PASS |
| Case 50 Lx | 源 512.0 / 印刷 `512` | PASS |
| Case 50 Ly | 源 512.0 / 印刷 `512` | PASS |
| Case 50 Δ | 源 1.0 → `1.00` / 印刷 `1.00` | PASS |
| Case 50 Obstacle | 源 (384,128,64,32) / 印刷 `(384,128,64,32)` | PASS |

## 5. Freq. 与 N (N/f) 列 ↔ 训练日志

> 每行回到该算例自己的训练日志，读『样本数: N』与『发现 k 个频率: [...]』；Reuse 列非空的行（复用他例数据与模型）取被复用算例的日志。N/f 应等于 N/k。此前这两列未被断言，Cases 43/44 曾误印为 2000 (2000)。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 1 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No01_R0/train_rectangle_Lx128_Ly128_H1.000_f25_50_75_100_spf2000_analyticsol__ratio0.90_bs1_mi4_hc48_ddp/logs/full_run_20260719_221907.log） | PASS |
| Case 1 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 2 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No02_W0/train_wedge_Lx128_Ly128_H1.000_f25_50_75_100_spf2000_analyticsol__ratio0.90_bs1_mi4_hc48_ddp/logs/full_run_20260720_031249.log） | PASS |
| Case 2 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 3 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No03_R1/training_run/logs/full_run_20260710_221657.log） | PASS |
| Case 3 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 4 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No04_R2/training_run/logs/full_run_20260710_214148.log） | PASS |
| Case 4 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 5 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No05_R3/training_run/logs/full_run_20260710_024112.log） | PASS |
| Case 5 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 6 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No06_R4/training_run/logs/full_run_20260710_224527.log） | PASS |
| Case 6 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 7 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No07_R5/training_run/logs/full_run_20260710_220509.log） | PASS |
| Case 7 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 8 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No08_R6/training_run/logs/full_run_20260710_024837.log） | PASS |
| Case 8 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 9 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No09_W1/training_run/logs/full_run_20260710_152228.log） | PASS |
| Case 9 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 10 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No10_W2/training_run/logs/full_run_20260710_123954.log） | PASS |
| Case 10 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 11 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No11_W3/training_run/logs/full_run_20260710_022039.log） | PASS |
| Case 11 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 12 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No12_W4/training_run/logs/full_run_20260710_150948.log） | PASS |
| Case 12 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 13 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No13_W5/training_run/logs/full_run_20260710_122002.log） | PASS |
| Case 13 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 14 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No14_W6/training_run/logs/full_run_20260710_024405.log） | PASS |
| Case 14 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 15 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No03_R1/training_run/logs/full_run_20260710_221657.log） | PASS |
| Case 15 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 16 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No16_R1_DeepONet/training_run/logs/full_run_20260711_003124.log） | PASS |
| Case 16 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 17 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No17_R1_FNO/training_run/logs/full_run_20260711_004949.log） | PASS |
| Case 17 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 18 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No18_R1_KNO/training_run/logs/full_run_20260711_013721.log） | PASS |
| Case 18 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 19 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No19_R1_CNO/training_run/logs/full_run_20260711_022215.log） | PASS |
| Case 19 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 20 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No09_W1/training_run/logs/full_run_20260710_152228.log） | PASS |
| Case 20 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 21 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No21_W1_DeepONet/training_run/logs/full_run_20260710_162410.log） | PASS |
| Case 21 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 22 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No22_W1_FNO/training_run/logs/full_run_20260710_172139.log） | PASS |
| Case 22 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 23 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No23_W1_KNO/training_run/logs/full_run_20260710_202430.log） | PASS |
| Case 23 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 24 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/No24_W1_CNO/training_run/logs/full_run_20260710_184721.log） | PASS |
| Case 24 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 25 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No25_R1_Full/training_run/logs/full_run_20260712_150041.log） | PASS |
| Case 25 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 26 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No26_R1_no_prior/training_run/logs/full_run_20260713_025215.log） | PASS |
| Case 26 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 27 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No27_R1_no_graph/training_run/logs/full_run_20260712_193334.log） | PASS |
| Case 27 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 28 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No28_R1_no_prior_loss/training_run/logs/full_run_20260712_150158.log） | PASS |
| Case 28 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 29 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No29_W1_Full/training_run/logs/full_run_20260715_023150.log） | PASS |
| Case 29 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 30 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No30_W1_no_prior/training_run/logs/full_run_20260715_023311.log） | PASS |
| Case 30 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 31 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No31_W1_no_graph/training_run/logs/full_run_20260715_082131.log） | PASS |
| Case 31 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 32 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.5_Ablation/No32_W1_no_prior_loss/training_run/logs/full_run_20260715_023318.log） | PASS |
| Case 32 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 33 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No06_R4/training_run/logs/full_run_20260710_224527.log） | PASS |
| Case 33 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 34 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No34_R7/training_run/logs/full_run_20260710_220203.log） | PASS |
| Case 34 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 35 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No35_R8/training_run/logs/full_run_20260710_025319.log） | PASS |
| Case 35 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 36 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No12_W4/training_run/logs/full_run_20260710_150948.log） | PASS |
| Case 36 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 37 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No37_W7/training_run/logs/full_run_20260710_123333.log） | PASS |
| Case 37 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 38 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No38_W8/training_run/logs/full_run_20260710_030023.log） | PASS |
| Case 38 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 39 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No39_R9/training_run/logs/full_run_20260720_153827.log） | PASS |
| Case 39 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 40 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No40_R10/training_run/logs/full_run_20260720_103428.log） | PASS |
| Case 40 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 41 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No41_W9/training_run/logs/full_run_20260720_204724.log） | PASS |
| Case 41 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 42 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No42_W10/training_run/logs/full_run_20260721_011504.log） | PASS |
| Case 42 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 43 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.8_Performance/No43_R1/training_run/logs/gpu1_full_run_20260721_111502.log） | PASS |
| Case 43 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 44 Freq. | 日志 `25,50,75,100` / 印刷 `25,50,75,100`（Data_and_Code_Availability/Raw_Experimental_Data/4.8_Performance/No44_W1/training_run/logs/gpu1_full_run_20260721_113657.log） | PASS |
| Case 44 N (N/f) | 日志 样本数 8000、4 频 → `8000 (2000)` / 印刷 `8000(2000)` | PASS |
| Case 45 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No06_R4/training_run/logs/full_run_20260710_224527.log） | PASS |
| Case 45 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 46 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No07_R5/training_run/logs/full_run_20260710_220509.log） | PASS |
| Case 46 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 47 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No08_R6/training_run/logs/full_run_20260710_024837.log） | PASS |
| Case 47 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 48 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No12_W4/training_run/logs/full_run_20260710_150948.log） | PASS |
| Case 48 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 49 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No13_W5/training_run/logs/full_run_20260710_122002.log） | PASS |
| Case 49 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |
| Case 50 Freq. | 日志 `100` / 印刷 `100`（Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No14_W6/training_run/logs/full_run_20260710_024405.log） | PASS |
| Case 50 N (N/f) | 日志 样本数 2000、1 频 → `2000 (2000)` / 印刷 `2000(2000)` | PASS |

## 6. Reuse 列 ↔ 训练日志 md5

> Reuse 声明『本行与第 k 行共用数据与已训练模型』。判据：本行目录下的训练日志与第 k 行的训练日志逐字节相同（md5），且两行 Dataset 与 Freq. 一致。R1 前 Cases 15/20/33/36 的 Reuse 曾误印为 1/7/4/10（各小 2，源于表首插入 Cases 1-2 后未顺延），已改为 3/9/6/12。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 15 → Reuse 3：Dataset/Freq. 一致 | R1/25,50,75,100 vs R1/25,50,75,100 | PASS |
| Case 15 → Reuse 3：训练日志 md5 相同 | `7b7a1bfe12` / `7b7a1bfe12` | PASS |
| Case 20 → Reuse 9：Dataset/Freq. 一致 | W1/25,50,75,100 vs W1/25,50,75,100 | PASS |
| Case 20 → Reuse 9：训练日志 md5 相同 | `7f1dde4cbe` / `7f1dde4cbe` | PASS |
| Case 33 → Reuse 6：Dataset/Freq. 一致 | R4/100 vs R4/100 | PASS |
| Case 33 → Reuse 6：训练日志 md5 相同 | `a1917a0b42` / `a1917a0b42` | PASS |
| Case 36 → Reuse 12：Dataset/Freq. 一致 | W4/100 vs W4/100 | PASS |
| Case 36 → Reuse 12：训练日志 md5 相同 | `ff4a9d9c4b` / `ff4a9d9c4b` | PASS |
| Case 45 → Reuse 6：Dataset/Freq. 一致 | R4/100 vs R4/100 | PASS |
| Case 45 → Reuse 6：训练日志 md5 相同 | `a1917a0b42` / `a1917a0b42` | PASS |
| Case 46 → Reuse 7：Dataset/Freq. 一致 | R5/100 vs R5/100 | PASS |
| Case 46 → Reuse 7：训练日志 md5 相同 | `b1eadb401b` / `b1eadb401b` | PASS |
| Case 47 → Reuse 8：Dataset/Freq. 一致 | R6/100 vs R6/100 | PASS |
| Case 47 → Reuse 8：训练日志 md5 相同 | `7625980c68` / `7625980c68` | PASS |
| Case 48 → Reuse 12：Dataset/Freq. 一致 | W4/100 vs W4/100 | PASS |
| Case 48 → Reuse 12：训练日志 md5 相同 | `ff4a9d9c4b` / `ff4a9d9c4b` | PASS |
| Case 49 → Reuse 13：Dataset/Freq. 一致 | W5/100 vs W5/100 | PASS |
| Case 49 → Reuse 13：训练日志 md5 相同 | `17a6ce7519` / `17a6ce7519` | PASS |
| Case 50 → Reuse 14：Dataset/Freq. 一致 | W6/100 vs W6/100 | PASS |
| Case 50 → Reuse 14：训练日志 md5 相同 | `b5277b4bf6` / `b5277b4bf6` | PASS |

