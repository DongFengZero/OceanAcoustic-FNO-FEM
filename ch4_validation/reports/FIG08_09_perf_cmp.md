# Fig. 8/9 — 五方法统一网格场图 Fig 8/9

- 对象：`fig:perf-cmp-r / fig:perf-cmp-w`（Fig. 8/9）
- 结论：**PASS** — 89 通过 / 0 失败 / 0 警告 / 2 豁免，共 91 项
- 脚本：`ch4_validation/scripts/FIG08_09_perf_cmp.py`
- 生成：2026-10-05 21:29:47

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | 两个独立 figure* 环境，各含一张整页图 |
| 成图脚本（权威） | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig08_09_perf_grid/fig08_09_perf_grid.py` | fig08_09_perf_grid.py（R1 起入库；旧 regen_method_grid.py 已废弃） |
| 论文图件（Fig 8） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/perf_grid_R1.pdf` | 成图脚本 out/ 下的整页 PDF |
| 论文图件（Fig 9） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/perf_grid_W1.pdf` | 成图脚本 out/ 下的整页 PDF |

## 2. 源可追溯与口径防漂移

> R1 把成图脚本收入仓库（Validation_Scripts/fig08_09_perf_grid/），旧路径 D:\Data\regen_method_grid.py 与其 repo 副本已不存在，故『两份副本 md5 同源』这一判据在 R1 已无对象——改为核入库脚本确实存在。

> 该脚本不设 GRID / METHOD / N_SAMPLE 模块常量：插值格数与方式（grid_res=200, method="cubic"）是 interp() 的形参默认值，取样序由模块常量 ROWS_2S 给出。故本节的防漂移断言按脚本真实表面写，不照搬场图族其他脚本的常量名。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本已入库 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig08_09_perf_grid/fig08_09_perf_grid.py | PASS |
| 成图脚本两份副本 md5 同源 | 旧权威路径 D:\Data\regen_method_grid.py 与 repo 副本均已不存在；R1 的成图脚本只有入库的这一份，无副本可比 | 豁免 |
| 插值网格 grid_res == 200 | `200` | PASS |
| 插值方式 method == cubic | `cubic` | PASS |
| 五方法列序与表行序一致 | ['Proposed', 'DeepONet', 'FNO', 'KNO', 'CNO'] | PASS |
| FREQS / N_SAMPLE 模块常量 == 期望值 | 脚本无这两个常量；取样序由 ROWS_2S 给出，频率集由 npz 的 freq 数组给出，已在第 4 节按 ROWS_2S 逐行核过 | 豁免 |
| 取样序 ROWS_2S = 每频率前 2 个样本（索引 0-7 顺序） | 行标题频率须与之逐一对应 | PASS |
| Fig 8 取 ep200 npz | Case15_R1_Proposed__TL原始数据_ep200.npz | PASS |
| Fig 8 图件存在 | perf_grid_R1.pdf | PASS |
| Fig 8 数据源 npz 存在 | Case15_R1_Proposed | PASS |
| Fig 8 数据源 npz 存在 | Case16_R1_DeepONet | PASS |
| Fig 8 数据源 npz 存在 | Case17_R1_FNO | PASS |
| Fig 8 数据源 npz 存在 | Case18_R1_KNO | PASS |
| Fig 8 数据源 npz 存在 | Case19_R1_CNO | PASS |
| Fig 9 取 ep200 npz | Case20_W1_Proposed__TL原始数据_ep200.npz | PASS |
| Fig 9 图件存在 | perf_grid_W1.pdf | PASS |
| Fig 9 数据源 npz 存在 | Case20_W1_Proposed | PASS |
| Fig 9 数据源 npz 存在 | Case21_W1_DeepONet | PASS |
| Fig 9 数据源 npz 存在 | Case22_W1_FNO | PASS |
| Fig 9 数据源 npz 存在 | Case23_W1_KNO | PASS |
| Fig 9 数据源 npz 存在 | Case24_W1_CNO | PASS |

## 3. epoch 双侧判据与 caption 声明

> 图取 ep200(last)，兄弟表 Table 9 取 best epoch，本是两套口径。故除『caption 含 last』外，还须断言『caption 未误写 best』，并列出各 case 的 best 与 200 的差异佐证。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Fig 8 全部 npz epoch == 200 (last) | 实得 [200]（5 份 npz） | PASS |
| Fig 8 caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| Fig 8 caption 未误写 best epoch | 图源自 ep200 npz | PASS |
| Fig 8 caption 标明案例区间 Cases~15--19 |  | PASS |
| Case 15 best epoch 可读 | best=198, last=200, 相差 2 轮 | PASS |
| Case 16 best epoch 可读 | best=199, last=200, 相差 1 轮 | PASS |
| Case 17 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 18 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 19 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Fig 9 全部 npz epoch == 200 (last) | 实得 [200]（5 份 npz） | PASS |
| Fig 9 caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| Fig 9 caption 未误写 best epoch | 图源自 ep200 npz | PASS |
| Fig 9 caption 标明案例区间 Cases~20--24 |  | PASS |
| Case 20 best epoch 可读 | best=181, last=200, 相差 19 轮 | PASS |
| Case 21 best epoch 可读 | best=195, last=200, 相差 5 轮 | PASS |
| Case 22 best epoch 可读 | best=194, last=200, 相差 6 轮 | PASS |
| Case 23 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 24 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |

## 4. 图内结构：行标题与列标题

> 本组图不标任何 Src/Avg 之外的内容，故锚点取图内文本。R1 的行标题格式为 `NN Hz (x, y)`——频率 + 该行样本的源坐标（1 位小数），**没有** a/b 标签，也**没有** `f = ` 前缀（旧版格式已废弃）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Fig 8 行数 = 8（4 频率 x 2 样本） | 实得 8 | PASS |
| Fig 8 8 个行标题与取样序的坐标一致 | 图上 8 个 / 期望 8 个 | PASS |
| Fig 8 样本索引按 0-7 顺序取 | [0, 1, 2, 3, 4, 5, 6, 7] | PASS |
| Fig 8 caption 写明取每频率前两个样本（非择优） | 含 `the first two held-out samples` | PASS |
| Fig 8 caption 未含混使用 representative | 索引顺序取样不应称 representative | PASS |
| Fig 8 含列标题 COMSOL |  | PASS |
| Fig 8 含列标题 Reference |  | PASS |
| Fig 8 含列标题 Pred. |  | PASS |
| Fig 8 含列标题 |Err| |  | PASS |
| Fig 8 含方法 Proposed 的列标题 |  | PASS |
| Fig 8 含方法 DeepONet 的列标题 |  | PASS |
| Fig 8 含方法 FNO 的列标题 |  | PASS |
| Fig 8 含方法 KNO 的列标题 |  | PASS |
| Fig 8 含方法 CNO 的列标题 |  | PASS |
| Fig 8 含两条色条的标签 |  | PASS |
| Fig 9 行数 = 8（4 频率 x 2 样本） | 实得 8 | PASS |
| Fig 9 8 个行标题与取样序的坐标一致 | 图上 8 个 / 期望 8 个 | PASS |
| Fig 9 样本索引按 0-7 顺序取 | [0, 1, 2, 3, 4, 5, 6, 7] | PASS |
| Fig 9 caption 写明取每频率前两个样本（非择优） | 含 `the first two held-out samples` | PASS |
| Fig 9 caption 未含混使用 representative | 索引顺序取样不应称 representative | PASS |
| Fig 9 含列标题 COMSOL |  | PASS |
| Fig 9 含列标题 Reference |  | PASS |
| Fig 9 含列标题 Pred. |  | PASS |
| Fig 9 含列标题 |Err| |  | PASS |
| Fig 9 含方法 Proposed 的列标题 |  | PASS |
| Fig 9 含方法 DeepONet 的列标题 |  | PASS |
| Fig 9 含方法 FNO 的列标题 |  | PASS |
| Fig 9 含方法 KNO 的列标题 |  | PASS |
| Fig 9 含方法 CNO 的列标题 |  | PASS |
| Fig 9 含两条色条的标签 |  | PASS |

## 5. |Err| 上方的区域平均误差：npz 重算 vs 图上标注

> 本组图唯一的数值标注是每个 |Err| 面板上方的区域平均误差（2 位小数），共 8 行 x 5 方法 = 40 个。逐方法与 npz 全精度重算比对——图上取整到2 位，重算给全精度，判定用舍入后的 2 位值。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Fig 8 图上解析到 40 个平均误差标注 | 实得 40 | PASS |
| Fig 8 40 个平均误差逐一吻合 npz 重算 | 全部吻合 | PASS |
| Fig 9 图上解析到 40 个平均误差标注 | 实得 40 | PASS |
| Fig 9 40 个平均误差逐一吻合 npz 重算 | 全部吻合 | PASS |

## 6. 图误差排序 vs 兄弟表 Table 9 的 Avg TL 排序

> 图上展示样本的逐方法场误差均值，与表的全测试集 Avg TL 数值不同（样本集不同），但**排序必须同向**——若图里某方法看着最准而表里它最差，就是图表不同源的信号。表侧取 Table 9 各自几何块的行。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Fig 8 图误差排序 == Table 9 TL 排序 | 图 ['Proposed', 'FNO', 'CNO', 'KNO', 'DeepONet'] / 表 ['Proposed', 'FNO', 'CNO', 'KNO', 'DeepONet'] | PASS |
| Fig 8 图上本文法误差最小 | Proposed:0.761 < FNO:1.018 < CNO:2.234 < KNO:2.376 < DeepONet:2.846 | PASS |
| Fig 9 图误差排序 == Table 9 TL 排序 | 图 ['Proposed', 'FNO', 'KNO', 'CNO', 'DeepONet'] / 表 ['Proposed', 'FNO', 'KNO', 'CNO', 'DeepONet'] | PASS |
| Fig 9 图上本文法误差最小 | Proposed:0.485 < FNO:0.671 < KNO:1.545 < CNO:1.803 < DeepONet:2.537 | PASS |

## 7. caption 与图表交叉引用

> R1 两张图各自独立成页，Fig 9 的 caption 以 `Layout as in Fig.~\ref{fig:perf-cmp-r}` 继承布局与取样说明，但**自身也写明**the first two，故两图的取样判据都直接可核，不靠继承兜底。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 被继承的 Fig 8 caption 自身写明取样方式 | 含 `the first two` | PASS |
| Fig 8 caption 说明行标题含源坐标 |  | PASS |
| Fig 8 caption 说明 |Error| 的域平均标注 |  | PASS |
| Fig 9 caption 以 Layout as in Fig.~\ref{fig:perf-cmp-r} 继承布局 | 含该交叉引用 | PASS |
| Fig 9 caption 的继承链指向 Fig 8 |  | PASS |
| Fig 8 caption 以 Table~\ref{tab:dl-cmp} 交代与表的对应 | 含 `these include the sources of Table~\ref{tab:dl-cmp}`；★ 被引的是 Table 7（深度线表）而非兄弟表 Table 9——本组图的 40 个展示样本里，每频率恰有一个就是 Table 7 的深度线声源，caption 指的是这个事实 | PASS |
| Fig 9 caption 以 Table~\ref{tab:dl-cmp} 交代与表的对应 | 含 `these include the sources of Table~\ref{tab:dl-cmp}`；★ 被引的是 Table 7（深度线表）而非兄弟表 Table 9——本组图的 40 个展示样本里，每频率恰有一个就是 Table 7 的深度线声源，caption 指的是这个事实 | PASS |
| Table 7 表头解析到 8 个深度线声源 | [('113.4', '64.0'), ('117.6', '43.4'), ('120.7', '89.5'), ('25.9', '49.5'), ('44.5', '21.9'), ('77.5', '103.0'), ('80.7', '72.7'), ('88.0', '78.9')] | PASS |
| Fig 8 每个频率各有一个展示样本是 Table 7 的深度线声源 | 交集 [('120.7', '89.5'), ('25.9', '49.5'), ('44.5', '21.9'), ('77.5', '103.0')]（每频率 1 个 = 4 个，与 caption 的 `these include the sources of Table~\ref{tab:dl-cmp}` 相符；该判决由坐标事实而非 \ref 字符串给出） | PASS |
| Fig 9 每个频率各有一个展示样本是 Table 7 的深度线声源 | 交集 [('113.4', '64.0'), ('117.6', '43.4'), ('80.7', '72.7'), ('88.0', '78.9')]（每频率 1 个 = 4 个，与 caption 的 `these include the sources of Table~\ref{tab:dl-cmp}` 相符；该判决由坐标事实而非 \ref 字符串给出） | PASS |

## 8. 正文引用

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:perf-cmp-r 编号为 8 | aux `8` | PASS |
| fig:perf-cmp-w 编号为 9 | aux `9` | PASS |
| 正文并列引用 Fig 8 与 Fig 9 | 含 `Figs.~\ref{fig:perf-cmp-r} and~\ref{fig:perf-cmp-w}` | PASS |
| 兄弟表 Table 9 在正文被引 | tex 行 876 | PASS |

