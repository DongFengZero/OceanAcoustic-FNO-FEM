# Table 5 — 解析解深度线 MAE @y=44.7m

- 对象：`tab:ideal-depthline`（Table 5）
- 结论：**PASS** — 42 通过 / 0 失败 / 0 警告，共 42 项
- 脚本：`ch4_validation/scripts/T05_ideal_depthline.py`
- 生成：2026-07-28 21:50:24

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:ideal-depthline}` 所在 minipage |
| 提取口径 脚本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/regen_ideal_panels.py` | 每频率取 y=44.7m 行 MAE 最小样本；成图与表值同一算法 |
| 数据源 npz (Case 1) | `Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No01_R0/Case01_R0__TL原始数据_ep200.npz` | ep200 TL 原始数据（last epoch） |
| 数据源 npz (Case 2) | `Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No02_W0/Case02_W0__TL原始数据_ep200.npz` | ep200 TL 原始数据（last epoch） |

## 2. 源可追溯性

> 成图脚本硬编码 `CASE_ROOT = D:\Data\Case1-2`，与注册表用的 `Raw_Experimental_Data/4.2_Validation/` 是两处副本，故校验 md5 确认同源——不同源则图与表的数据基础就不一致。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/regen_ideal_panels.py | PASS |
| Case 1 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No01_R0/Case01_R0__TL原始数据_ep200.npz | PASS |
| Case 2 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No02_W0/Case02_W0__TL原始数据_ep200.npz | PASS |
| Case 1 两处 npz 同源 | md5 `399d8e5e035e…` == `399d8e5e035e…` | PASS |
| Case 2 两处 npz 同源 | md5 `2361cff6159b…` == `2361cff6159b…` | PASS |
| tex 数据行数 = 2 | 实得 2 | PASS |
| tex 行 No. 覆盖 Case 1-2 | [1, 2] | PASS |

## 3. 提取口径与成图脚本一致（防漂移）

> 本脚本复刻了成图脚本的提取算法。若成图脚本的常量被改动而这里没跟上，表值就会与图脱钩，故直接从脚本源码解析常量做断言。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 常量 GRID | 脚本 `220` / 复刻 `220` | PASS |
| 常量 METHOD | 脚本 `cubic` / 复刻 `cubic` | PASS |
| 常量 Y_LINE | 脚本 `44.7` / 复刻 `44.7` | PASS |

## 4. 从 npz 独立复现（MAE 与源位 vs 印刷值）

> 列序：No., Dataset, 25Hz(TL,Src), 50Hz, 75Hz, 100Hz。Src 印刷为 1 位小数对，与图面板标题及场图同口径，故按 1 位比对。

> 采用 1 位而非整数：整数口径下 `39.50081`→40 与 `49.49999679`→49 进位方向相反、且把 39.5 与 40.0 混为一谈，无法回溯到具体样本；1 位小数保留了半整数网格信息（39.5/49.5/87.5 等）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 1 Dataset 名 | tex `R0 (rect.)` | PASS |
| Case 1 25Hz TL-MAE | 源 0.15101540210759823 → `0.151` / 印刷 `0.151` | PASS |
| Case 1 25Hz Src | npz 样本#1 `(39.500812,36.442653)` → `(39.5,36.4)` / 印刷 `(39.5,36.4)` | PASS |
| Case 1 25Hz 取样行贴近 y=44.7 | 实际 y=`44.42` m | PASS |
| Case 1 50Hz TL-MAE | 源 0.12963766470401805 → `0.130` / 印刷 `0.130` | PASS |
| Case 1 50Hz Src | npz 样本#3 `(49.499997,38.057485)` → `(49.5,38.1)` / 印刷 `(49.5,38.1)` | PASS |
| Case 1 50Hz 取样行贴近 y=44.7 | 实际 y=`44.42` m | PASS |
| Case 1 75Hz TL-MAE | 源 0.34054601590912176 → `0.341` / 印刷 `0.341` | PASS |
| Case 1 75Hz Src | npz 样本#4 `(87.500000,107.756656)` → `(87.5,107.8)` / 印刷 `(87.5,107.8)` | PASS |
| Case 1 75Hz 取样行贴近 y=44.7 | 实际 y=`44.42` m | PASS |
| Case 1 100Hz TL-MAE | 源 0.42963256233696384 → `0.430` / 印刷 `0.430` | PASS |
| Case 1 100Hz Src | npz 样本#7 `(22.672545,54.000000)` → `(22.7,54.0)` / 印刷 `(22.7,54.0)` | PASS |
| Case 1 100Hz 取样行贴近 y=44.7 | 实际 y=`44.42` m | PASS |
| Case 2 Dataset 名 | tex `W0 (wedge)` | PASS |
| Case 2 25Hz TL-MAE | 源 0.11350975583848255 → `0.114` / 印刷 `0.114` | PASS |
| Case 2 25Hz Src | npz 样本#1 `(63.500000,13.765474)` → `(63.5,13.8)` / 印刷 `(63.5,13.8)` | PASS |
| Case 2 25Hz 取样行贴近 y=44.7 | 实际 y=`44.42` m | PASS |
| Case 2 50Hz TL-MAE | 源 0.06932651460388556 → `0.069` / 印刷 `0.069` | PASS |
| Case 2 50Hz Src | npz 样本#2 `(83.046054,55.561680)` → `(83.0,55.6)` / 印刷 `(83.0,55.6)` | PASS |
| Case 2 50Hz 取样行贴近 y=44.7 | 实际 y=`44.42` m | PASS |
| Case 2 75Hz TL-MAE | 源 0.449343338669986 → `0.449` / 印刷 `0.449` | PASS |
| Case 2 75Hz Src | npz 样本#4 `(92.299326,53.374688)` → `(92.3,53.4)` / 印刷 `(92.3,53.4)` | PASS |
| Case 2 75Hz 取样行贴近 y=44.7 | 实际 y=`44.42` m | PASS |
| Case 2 100Hz TL-MAE | 源 1.2346670375372324 → `1.235` / 印刷 `1.235` | PASS |
| Case 2 100Hz Src | npz 样本#7 `(120.712396,58.500000)` → `(120.7,58.5)` / 印刷 `(120.7,58.5)` | PASS |
| Case 2 100Hz 取样行贴近 y=44.7 | 实际 y=`44.42` m | PASS |

## 5. 同表小数位一致性

> 要求：TL 列一律 3 位小数；Src 两个分量一律 1 位小数（与图面板标题及场图统一口径，不允许整数或 2 位混排）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 8 个 TL 单元格均 3 位小数、8 个 Src 均 1 位小数对 | 全部合规 | PASS |

## 6. caption 与口径自洽

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 标注的深度线位置 = 脚本 Y_LINE | caption 含 `y=44.7`：是 | PASS |
| caption 声明 last epoch | 本表源自 ep200 npz，非 best epoch | PASS |
| caption 说明取样规则 | 应交代“每频率取最匹配样本” | PASS |

## 7. 正文断言与表值一致（4.2 节）

> 4.2 正文未直接引用本表数字，只作趋势断言：“The error is largest at 75 and 100 Hz on the wedge”。趋势断言同样须由表值支持，否则是无据之言。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 楔形 W0 误差最大的两个频率 = 75/100Hz | 降序 100Hz(1.235) > 75Hz(0.449) > 25Hz(0.114) > 50Hz(0.069) | PASS |
| 正文该断言可定位 | tex 行 686 | PASS |

