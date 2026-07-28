# Fig. ideal-wedge — Fig. 4 楔形理想波导解析验证（W0, Case 2）

- 对象：`fig:ideal-wedge`（Fig. ideal-wedge）
- 结论：**PASS** — 31 通过 / 0 失败 / 0 警告，共 31 项
- 脚本：`ch4_validation/scripts/FIG04_ideal_wedge.py`
- 生成：2026-07-28 20:30:34

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|

## 1. 数据源与绘图脚本

> 验证 npz 文件存在、绘图脚本可导入、口径防漂移（函数签名不变）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| npz 文件存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No02_W0/Case02_W0__TL原始数据_ep200.npz | PASS |
| 绘图脚本取数目录与 Raw_Experimental_Data 同源 | md5 相同（Case1-2/Case02_W0/Case02_W0__TL原始数据_ep200.npz） | PASS |
| 绘图脚本存在 | D:\Data\OceanAcoustic-FNO-FEM_github\Validation_Scripts\regen_ideal_panels.py | PASS |
| load 函数可导入 | 口径防漂移 | PASS |
| pick_sample 函数可导入 | 口径防漂移 | PASS |
| FREQS 常量可导入 | [25, 50, 75, 100] | PASS |

## 2. Epoch 自证（npz metadata）

> 验证 npz 内的 epoch 字段与 caption 声明一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| npz epoch 字段 | epoch=200, 预期 200 (last) | PASS |
| xlsx 记录 Case 2 的 best epoch | best=199 | PASS |
| Case 2 best(199) 与 last(200) 确不相同 | 相差 1 轮 —— caption 写 best 即为错 | PASS |
| caption 未误写 best epoch | 图源自 ep200 npz，非 best-epoch 评估 | PASS |
| Caption 声明 epoch | 声明 'last epoch' | PASS |

## 3. 深度线 MAE 反向验证（与 Table 5 对齐）

> 从 npz 全精度重算 MAE，舍入 3 位后与 Table 5 印刷值比对

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25 Hz TL MAE (idx=1) | npz全精度 0.113509756 → 3dp 0.114 / 表印 0.114 | PASS |
| 50 Hz TL MAE (idx=2) | npz全精度 0.069326515 → 3dp 0.069 / 表印 0.069 | PASS |
| 75 Hz TL MAE (idx=4) | npz全精度 0.449343339 → 3dp 0.449 / 表印 0.449 | PASS |
| 100 Hz TL MAE (idx=7) | npz全精度 1.234667038 → 3dp 1.235 / 表印 1.235 | PASS |

## 4. Source 坐标反向验证（与 Table 5 / 图标题对齐）

> 从 npz source_pos 舍入 1 位后与 Table 5 Src 列、图面板标题比对。全章坐标统一 1 位小数（深度线与场图同口径）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25 Hz Src 坐标 (idx=1) | npz全精度 (63.500000,13.765474) → 1dp (63.5,13.8) / 表印 (63.5, 13.8) | PASS |
| 50 Hz Src 坐标 (idx=2) | npz全精度 (83.046054,55.561680) → 1dp (83.0,55.6) / 表印 (83.0, 55.6) | PASS |
| 75 Hz Src 坐标 (idx=4) | npz全精度 (92.299326,53.374688) → 1dp (92.3,53.4) / 表印 (92.3, 53.4) | PASS |
| 100 Hz Src 坐标 (idx=7) | npz全精度 (120.712396,58.500000) → 1dp (120.7,58.5) / 表印 (120.7, 58.5) | PASS |

## 5. 图文件存在性

> 验证论文引用的 PDF 文件存在

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 图片文件存在 | Figures/results/Case02_W0_grid2.pdf | PASS |

## 6. 样本选择一致性

> 确认 pick_sample 返回的样本索引与预期一致（4频率8样本中MAE最小者）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25 Hz 样本索引 | idx=1, 预期=1 | PASS |
| 50 Hz 样本索引 | idx=2, 预期=2 | PASS |
| 75 Hz 样本索引 | idx=4, 预期=4 | PASS |
| 100 Hz 样本索引 | idx=7, 预期=7 | PASS |

## 6. 正文引用：被引 + 说明与图内容相符

> 正文断言『每个频率两个留出样本』。npz 共 8 个样本、4 个频率，每频率恰 2 个；图按 pick_two 排两列(a/b)，与该断言一致。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文（4.2 节）引用本图 | tex 行 686 | PASS |
| 正文该断言可定位 | 含 `Two held-out samples at every frequency` | PASS |
| npz 每频率恰 2 个样本 | 频率计数 {25: 2, 50: 2, 75: 2, 100: 2} | PASS |
| 25 Hz 图上取 2 个不同样本 | idx=[1, 0] | PASS |
| 50 Hz 图上取 2 个不同样本 | idx=[2, 3] | PASS |
| 75 Hz 图上取 2 个不同样本 | idx=[4, 5] | PASS |
| 100 Hz 图上取 2 个不同样本 | idx=[7, 6] | PASS |

