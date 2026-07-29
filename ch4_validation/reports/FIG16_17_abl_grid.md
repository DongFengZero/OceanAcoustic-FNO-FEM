# Fig. 16/17 — 四变体消融场图 Fig 16/17

- 对象：`fig:abl-rect / fig:abl-wedge`（Fig. 16/17）
- 结论：**PASS** — 62 通过 / 0 失败 / 0 警告，共 62 项
- 脚本：`ch4_validation/scripts/FIG16_17_abl_grid.py`
- 生成：2026-07-30 00:06:40

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
| fig:abl-rect 方法顺序与表行序一致 | ['Full model', 'w/o prior', 'w/o graph', 'w/o prior-sup.'] | PASS |
| fig:abl-rect 图件存在 | abl_grid_R1.pdf | PASS |
| fig:abl-wedge 方法顺序与表行序一致 | ['Full model', 'w/o prior', 'w/o graph', 'w/o prior-sup.'] | PASS |
| fig:abl-wedge 图件存在 | abl_grid_W1.pdf | PASS |

## 2. epoch 双侧判据与 caption 声明

> 图取 ep200(last)，兄弟表 Tables 15/16 取 best epoch，本是两套口径。故除『caption 含 last』外，还须断言『caption 未误写 best』，并列出各 case 的 best 与 200 的差异佐证。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:abl-rect 全部 npz epoch == 200 (last) | 实得 [200]（4 份 npz） | PASS |
| fig:abl-rect caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:abl-rect caption 未误写 best epoch | 图源自 ep200 npz | PASS |
| fig:abl-rect caption 标明案例区间 25-28 |  | PASS |
| Case 25 best epoch 可读 | best=194, last=200, 相差 6 轮 | PASS |
| Case 26 best epoch 可读 | best=82, last=200, 相差 118 轮 | PASS |
| Case 27 best epoch 可读 | best=199, last=200, 相差 1 轮 | PASS |
| Case 28 best epoch 可读 | best=199, last=200, 相差 1 轮 | PASS |
| fig:abl-wedge 全部 npz epoch == 200 (last) | 实得 [200]（4 份 npz） | PASS |
| fig:abl-wedge caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:abl-wedge caption 未误写 best epoch | 图源自 ep200 npz | PASS |
| fig:abl-wedge caption 标明案例区间 29-32 |  | PASS |
| Case 29 best epoch 可读 | best=197, last=200, 相差 3 轮 | PASS |
| Case 30 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 31 best epoch 可读 | best=199, last=200, 相差 1 轮 | PASS |
| Case 32 best epoch 可读 | best=199, last=200, 相差 1 轮 | PASS |

## 3. 图内结构：行标签与列标题

> 本组图不标任何数值（无 Src、无 Avg），故锚点取图内文本：8 个行标签 `f = XX Hz (a/b)` 须与 pick_rows 的取样序一致；列标题须含 COMSOL(Ref) 与五个方法名。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:abl-rect 行数 = 8（4 频率 x 2 样本） | 实得 8 | PASS |
| fig:abl-rect 8 个行标签与取样序一致 | 图上 8 个，缺 无 | PASS |
| fig:abl-rect 样本索引按 0-7 顺序取 | [0, 1, 2, 3, 4, 5, 6, 7] | PASS |
| fig:abl-rect caption 写明取每频率前两个样本或明确继承 | 含 `the first two` | PASS |
| fig:abl-rect caption 未含混使用 representative | 索引顺序取样不应称 representative | PASS |
| fig:abl-rect 含 COMSOL 参考列 |  | PASS |
| fig:abl-rect 含方法 Full model 的列标题 |  | PASS |
| fig:abl-rect 含方法 w/o prior 的列标题 |  | PASS |
| fig:abl-rect 含方法 w/o graph 的列标题 |  | PASS |
| fig:abl-rect 含方法 w/o prior-sup. 的列标题 |  | PASS |
| fig:abl-rect 含 |Error| 列 |  | PASS |
| fig:abl-wedge 行数 = 8（4 频率 x 2 样本） | 实得 8 | PASS |
| fig:abl-wedge 8 个行标签与取样序一致 | 图上 8 个，缺 无 | PASS |
| fig:abl-wedge 样本索引按 0-7 顺序取 | [0, 1, 2, 3, 4, 5, 6, 7] | PASS |
| fig:abl-wedge caption 写明取每频率前两个样本或明确继承 | 以 Layout as in 继承 | PASS |
| fig:abl-wedge caption 未含混使用 representative | 索引顺序取样不应称 representative | PASS |
| fig:abl-wedge 含 COMSOL 参考列 |  | PASS |
| fig:abl-wedge 含方法 Full model 的列标题 |  | PASS |
| fig:abl-wedge 含方法 w/o prior 的列标题 |  | PASS |
| fig:abl-wedge 含方法 w/o graph 的列标题 |  | PASS |
| fig:abl-wedge 含方法 w/o prior-sup. 的列标题 |  | PASS |
| fig:abl-wedge 含 |Error| 列 |  | PASS |
| 被继承的 fig:abl-rect caption 自身写明取样方式 | 含 `the first two` | PASS |

## 4. 图误差与兄弟表 Avg TL 的端点一致性

> ★ 本组判据比 Fig 14/15 弱一档，只核首末两端而非完整排序，原因是两侧聚合口径不同：图误差是 8 个展示样本的等权平均，表 Avg TL 是全测试集平均。w/o prior-sup. 在 25 Hz 显著优于 Full（图 0.502/0.536 vs 1.171/1.635），其余频率则劣于 Full；等权平均把它拉到 Full 之下，全测试集平均则 Full 胜出。两者各自自洽，中间名次本就可以互换——Table 11 里 25 Hz 的加粗落在 w/o prior-sup. 而非 Full，是同一现象。

> 　fig:abl-rect：图序 ['w/o prior-sup.', 'Full model', 'w/o graph', 'w/o prior'] 与表序 ['Full model', 'w/o prior-sup.', 'w/o graph', 'w/o prior'] 中段不同，系聚合口径差异，非图表不同源。

> 　fig:abl-wedge：图序 ['Full model', 'w/o prior-sup.', 'w/o graph', 'w/o prior'] 与表序 ['Full model', 'w/o graph', 'w/o prior-sup.', 'w/o prior'] 中段不同，系聚合口径差异，非图表不同源。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:abl-rect 图与表一致认定 w/o prior 最差 | 图末位 `w/o prior` / 表末位 `w/o prior` | PASS |
| fig:abl-rect 图上 w/o prior 误差碾压其余（>5x） | 29.76 vs 次差 2.00 | PASS |
| fig:abl-rect 图上最优为 Full 或 w/o prior-sup. | w/o prior-sup.:1.754 < Full model:1.808 < w/o graph:2.004 < w/o prior:29.765 | PASS |
| fig:abl-rect 表上最优为 Full model（全测试集口径） | Full model:1.911 < w/o prior-sup.:2.073 < w/o graph:2.206 < w/o prior:38.800 | PASS |
| fig:abl-rect caption 已就『图上名次≠全测试集名次』给出说明 | 含 per-sample vs split-averaged 的 caveat | PASS |
| fig:abl-wedge 图与表一致认定 w/o prior 最差 | 图末位 `w/o prior` / 表末位 `w/o prior` | PASS |
| fig:abl-wedge 图上 w/o prior 误差碾压其余（>5x） | 29.05 vs 次差 2.22 | PASS |
| fig:abl-wedge 图上最优为 Full 或 w/o prior-sup. | Full model:1.740 < w/o prior-sup.:1.949 < w/o graph:2.218 < w/o prior:29.048 | PASS |
| fig:abl-wedge 表上最优为 Full model（全测试集口径） | Full model:1.936 < w/o graph:2.443 < w/o prior-sup.:2.533 < w/o prior:48.797 | PASS |
| fig:abl-wedge caption 已就『图上名次≠全测试集名次』给出说明 | 含 per-sample vs split-averaged 的 caveat | PASS |

## 5. 正文引用

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:abl-rect 编号为 16 | aux `16` | PASS |
| fig:abl-wedge 编号为 17 | aux `17` | PASS |
| Fig 16 被引用（含 Fig 17 caption 的 Layout 交叉引用） | `\ref{fig:abl-rect}` 出现 3 处 | PASS |
| 兄弟表 Table 15 在正文被引 | tex 行 1052 | PASS |

