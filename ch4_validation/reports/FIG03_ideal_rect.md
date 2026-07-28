# Fig. ideal-rect — Fig. 3 矩形理想波导解析验证（R0, Case 1）

- 对象：`fig:ideal-rect`（Fig. ideal-rect）
- 结论：**PASS** — 37 通过 / 0 失败 / 0 警告，共 37 项
- 脚本：`ch4_validation/scripts/FIG03_ideal_rect.py`
- 生成：2026-07-28 21:51:29

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|

## 1. 数据源与绘图脚本

> 验证 npz 文件存在、绘图脚本可导入、口径防漂移（函数签名不变）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| npz 文件存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.2_Validation/No01_R0/Case01_R0__TL原始数据_ep200.npz | PASS |
| 绘图脚本取数目录与 Raw_Experimental_Data 同源 | md5 相同（Case1-2/Case01_R0/Case01_R0__TL原始数据_ep200.npz） | PASS |
| 绘图脚本存在 | D:\Data\OceanAcoustic-FNO-FEM_github\Validation_Scripts\regen_ideal_panels.py | PASS |
| load 函数可导入 | 口径防漂移 | PASS |
| pick_sample 函数可导入 | 口径防漂移 | PASS |
| FREQS 常量可导入 | [25, 50, 75, 100] | PASS |

## 2. Epoch 自证（npz metadata）

> 验证 npz 内的 epoch 字段与 caption 声明一致

> Case 1: best epoch=200，图取 last=200。二者恰好相等（巧合），但 caption 仍应按数据来源写 last。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| npz epoch 字段 | epoch=200, 预期 200 (last) | PASS |
| xlsx 记录 Case 1 的 best epoch | best=200 | PASS |
| caption 未误写 best epoch | 图源自 ep200 npz，非 best-epoch 评估 | PASS |
| Caption 声明 epoch | 声明 'last epoch' | PASS |

## 3. 深度线 MAE 反向验证（与 Table 5 对齐）

> 从 npz 全精度重算 MAE，舍入 3 位后与 Table 5 印刷值比对

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25 Hz TL MAE (idx=1) | npz全精度 0.151015402 → 3dp 0.151 / 表印 0.151 | PASS |
| 50 Hz TL MAE (idx=3) | npz全精度 0.129637665 → 3dp 0.130 / 表印 0.130 | PASS |
| 75 Hz TL MAE (idx=4) | npz全精度 0.340546016 → 3dp 0.341 / 表印 0.341 | PASS |
| 100 Hz TL MAE (idx=7) | npz全精度 0.429632562 → 3dp 0.430 / 表印 0.430 | PASS |

## 4. Source 坐标反向验证（与 Table 5 / 图标题对齐）

> 从 npz source_pos 舍入 1 位后与 Table 5 Src 列、图面板标题比对。全章坐标统一 1 位小数（深度线与场图同口径）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25 Hz Src 坐标 (idx=1) | npz全精度 (39.500812,36.442653) → 1dp (39.5,36.4) / 表印 (39.5, 36.4) | PASS |
| 50 Hz Src 坐标 (idx=3) | npz全精度 (49.499997,38.057485) → 1dp (49.5,38.1) / 表印 (49.5, 38.1) | PASS |
| 75 Hz Src 坐标 (idx=4) | npz全精度 (87.500000,107.756656) → 1dp (87.5,107.8) / 表印 (87.5, 107.8) | PASS |
| 100 Hz Src 坐标 (idx=7) | npz全精度 (22.672545,54.000000) → 1dp (22.7,54.0) / 表印 (22.7, 54.0) | PASS |

## 5. 图文件存在性

> 验证论文引用的 PDF 文件存在

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 图片文件存在 | Figures/results/Case01_R0_grid2.pdf | PASS |

## 6. 样本选择一致性

> 确认 pick_sample 返回的样本索引与预期一致（4频率8样本中MAE最小者）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25 Hz 样本索引 | idx=1, 预期=1 | PASS |
| 50 Hz 样本索引 | idx=3, 预期=3 | PASS |
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
| 50 Hz 图上取 2 个不同样本 | idx=[3, 2] | PASS |
| 75 Hz 图上取 2 个不同样本 | idx=[4, 5] | PASS |
| 100 Hz 图上取 2 个不同样本 | idx=[7, 6] | PASS |

## 7. caption 的取样措辞与实际机制相符

> 本图用 pick_two：按 y=Y_LINE 行的 MAE 升序取前 2 个，是**择优**取样。caption 若含混称 representative，读者会以为是随机抽样，故要求写明 best-matching 与排序依据。（场图族用 pick_rows 按索引顺序取前 2 个，措辞是 the first two，两者不可混用。）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 写明 best-matching |  | PASS |
| caption 写明排序依据为深度线 MAE |  | PASS |
| caption 未含混使用 representative | 择优取样不应称 representative | PASS |
| 25 Hz a 列即 MAE 最优样本 | pick_two 首个 idx=1，pick_sample idx=1，MAE=0.151015 | PASS |
| 50 Hz a 列即 MAE 最优样本 | pick_two 首个 idx=3，pick_sample idx=3，MAE=0.129638 | PASS |
| 75 Hz a 列即 MAE 最优样本 | pick_two 首个 idx=4，pick_sample idx=4，MAE=0.340546 | PASS |
| 100 Hz a 列即 MAE 最优样本 | pick_two 首个 idx=7，pick_sample idx=7，MAE=0.429633 | PASS |

