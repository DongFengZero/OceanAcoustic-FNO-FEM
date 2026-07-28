# Fig. 14/15 — 五方法统一网格场图 Fig 14/15

- 对象：`fig:perf-rect / fig:perf-wedge`（Fig. 14/15）
- 结论：**PASS** — 60 通过 / 0 失败 / 0 警告，共 60 项
- 脚本：`ch4_validation/scripts/FIG14_15_perf_grid.py`
- 生成：2026-07-29 00:28:45

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 单个 figure* 内含两图 |
| 成图脚本（权威） | `regen_method_grid.py` | regen_method_grid.py |
| 成图脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/regen_method_grid.py` | md5 应与权威副本相同 |

## 1. 源可追溯与口径防漂移

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本两份副本 md5 同源 | 权威 `309abb27` / repo `309abb27` | PASS |
| GRID == 200 | 脚本内 `200` | PASS |
| 插值 METHOD == cubic | 脚本内 `cubic` | PASS |
| 每频率展示 2 个样本 | 脚本内 `2` | PASS |
| FREQS 一致 | `[25, 50, 75, 100]` | PASS |
| fig:perf-rect 方法顺序与表行序一致 | ['Proposed', 'DeepONet', 'FNO', 'KNO', 'CNO'] | PASS |
| fig:perf-rect 图件存在 | perf_grid_R1.pdf | PASS |
| fig:perf-wedge 方法顺序与表行序一致 | ['Proposed', 'DeepONet', 'FNO', 'KNO', 'CNO'] | PASS |
| fig:perf-wedge 图件存在 | perf_grid_W1.pdf | PASS |

## 2. epoch 双侧判据与 caption 声明

> 图取 ep200(last)，兄弟表 Tables 13/14 取 best epoch，本是两套口径。故除『caption 含 last』外，还须断言『caption 未误写 best』，并列出各 case 的 best 与 200 的差异佐证。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:perf-rect 全部 npz epoch == 200 (last) | 实得 [200]（5 份 npz） | PASS |
| fig:perf-rect caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:perf-rect caption 未误写 best epoch | 图源自 ep200 npz | PASS |
| fig:perf-rect caption 标明案例区间 15-19 |  | PASS |
| Case 15 best epoch 可读 | best=198, last=200, 相差 2 轮 | PASS |
| Case 16 best epoch 可读 | best=199, last=200, 相差 1 轮 | PASS |
| Case 17 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 18 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 19 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| fig:perf-wedge 全部 npz epoch == 200 (last) | 实得 [200]（5 份 npz） | PASS |
| fig:perf-wedge caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:perf-wedge caption 未误写 best epoch | 图源自 ep200 npz | PASS |
| fig:perf-wedge caption 标明案例区间 20-24 |  | PASS |
| Case 20 best epoch 可读 | best=181, last=200, 相差 19 轮 | PASS |
| Case 21 best epoch 可读 | best=195, last=200, 相差 5 轮 | PASS |
| Case 22 best epoch 可读 | best=194, last=200, 相差 6 轮 | PASS |
| Case 23 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 24 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |

## 3. 图内结构：行标签与列标题

> 本组图不标任何数值（无 Src、无 Avg），故锚点取图内文本：8 个行标签 `f = XX Hz (a/b)` 须与 pick_rows 的取样序一致；列标题须含 COMSOL(Ref) 与五个方法名。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:perf-rect 行数 = 8（4 频率 x 2 样本） | 实得 8 | PASS |
| fig:perf-rect 8 个行标签与取样序一致 | 图上 8 个，缺 无 | PASS |
| fig:perf-rect 样本索引按 0-7 顺序取 | [0, 1, 2, 3, 4, 5, 6, 7] | PASS |
| fig:perf-rect caption 写明取每频率前两个样本或明确继承 | 含 `the first two` | PASS |
| fig:perf-rect caption 未含混使用 representative | 索引顺序取样不应称 representative | PASS |
| fig:perf-rect 含 COMSOL 参考列 |  | PASS |
| fig:perf-rect 含方法 Proposed 的列标题 |  | PASS |
| fig:perf-rect 含方法 DeepONet 的列标题 |  | PASS |
| fig:perf-rect 含方法 FNO 的列标题 |  | PASS |
| fig:perf-rect 含方法 KNO 的列标题 |  | PASS |
| fig:perf-rect 含方法 CNO 的列标题 |  | PASS |
| fig:perf-rect 含 |Error| 列 |  | PASS |
| fig:perf-wedge 行数 = 8（4 频率 x 2 样本） | 实得 8 | PASS |
| fig:perf-wedge 8 个行标签与取样序一致 | 图上 8 个，缺 无 | PASS |
| fig:perf-wedge 样本索引按 0-7 顺序取 | [0, 1, 2, 3, 4, 5, 6, 7] | PASS |
| fig:perf-wedge caption 写明取每频率前两个样本或明确继承 | 以 Layout as in 继承 | PASS |
| fig:perf-wedge caption 未含混使用 representative | 索引顺序取样不应称 representative | PASS |
| fig:perf-wedge 含 COMSOL 参考列 |  | PASS |
| fig:perf-wedge 含方法 Proposed 的列标题 |  | PASS |
| fig:perf-wedge 含方法 DeepONet 的列标题 |  | PASS |
| fig:perf-wedge 含方法 FNO 的列标题 |  | PASS |
| fig:perf-wedge 含方法 KNO 的列标题 |  | PASS |
| fig:perf-wedge 含方法 CNO 的列标题 |  | PASS |
| fig:perf-wedge 含 |Error| 列 |  | PASS |
| 被继承的 fig:perf-rect caption 自身写明取样方式 | 含 `the first two` | PASS |

## 4. 图误差排序 vs 兄弟表 Avg TL 排序

> 图上 8 个展示样本的逐方法场误差均值，与表的全测试集 Avg TL 数值不同（样本集不同），但**排序必须同向**——若图里某方法看着最准而表里它最差，就是图表不同源的信号。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:perf-rect 图误差排序 == 表 TL 排序 | 图 ['Proposed', 'FNO', 'CNO', 'KNO', 'DeepONet'] / 表 ['Proposed', 'FNO', 'CNO', 'KNO', 'DeepONet'] | PASS |
| fig:perf-rect 图上本文法误差最小 | Proposed:0.761 < FNO:1.018 < CNO:2.234 < KNO:2.376 < DeepONet:2.846 | PASS |
| fig:perf-wedge 图误差排序 == 表 TL 排序 | 图 ['Proposed', 'FNO', 'KNO', 'CNO', 'DeepONet'] / 表 ['Proposed', 'FNO', 'KNO', 'CNO', 'DeepONet'] | PASS |
| fig:perf-wedge 图上本文法误差最小 | Proposed:0.485 < FNO:0.671 < KNO:1.545 < CNO:1.803 < DeepONet:2.537 | PASS |

## 5. 正文引用

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:perf-rect 编号为 14 | aux `14` | PASS |
| fig:perf-wedge 编号为 15 | aux `15` | PASS |
| Fig 14 被引用（含 Fig 15 caption 的 Layout 交叉引用） | `\ref{fig:perf-rect}` 出现 4 处 | PASS |
| 兄弟表 Table 13 在正文被引 | tex 行 900 | PASS |

