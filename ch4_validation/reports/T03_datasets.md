# tab:datasets — 数据集总表 No.1-50（结构性，非测量值）

- 对象：`tab:datasets`（tab:datasets）
- 结论：**PASS** — 303 通过 / 0 失败 / 0 警告，共 303 项
- 脚本：`ch4_validation/scripts/T03_datasets.py`
- 生成：2026-07-28 20:29:23

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | Table None 环境 |
| Dataset 目录 | `Data_and_Code_Availability/Dataset` | 22 个数据集配置 |

## 1. tex 表格结构

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 表格环境可定位且确实包住 label | `tab:datasets`，长度 8477 | PASS |
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

