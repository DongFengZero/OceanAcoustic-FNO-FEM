# Fig. 21/22 — 源位置外推场图 Fig 21/22

- 对象：`fig:gen-grid / fig:gen-grid-wedge`（Fig. 21/22）
- 结论：**PASS** — 54 通过 / 0 失败 / 0 警告，共 54 项
- 脚本：`ch4_validation/scripts/FIG21_22_gen_extrap.py`
- 生成：2026-07-28 21:42:33

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 两个 figure* 环境，各 2 个 subfloat |
| 成图脚本（权威） | `regen_gen_extrap_bigfont.py` | regen_gen_extrap_bigfont.py |
| 数据源 npz (Case 39 R9) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No39_R9/Case39_R9__TL原始数据_ep200.npz` | Raw_Experimental_Data/4.7，ep200 |
| 数据源 npz (Case 40 R10) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No40_R10/Case40_R10__TL原始数据_ep200.npz` | Raw_Experimental_Data/4.7，ep200 |
| 数据源 npz (Case 41 W9) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No41_W9/Case41_W9__TL原始数据_ep200.npz` | Raw_Experimental_Data/4.7，ep200 |
| 数据源 npz (Case 42 W10) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No42_W10/Case42_W10__TL原始数据_ep200.npz` | Raw_Experimental_Data/4.7，ep200 |

## 1. 源可追溯与口径防漂移

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本两份副本 md5 同源 | 权威 `f9d74d5c` / repo `f9d74d5c` | PASS |
| 脚本内 Src 为 1 位小数（全章统一口径） |  | PASS |
| Case 39 R9 npz 样本数 = 8 | 4 频率 x 2 样本，实得 8 | PASS |
| gen_extrap_R9.pdf 存在 | gen_extrap_R9.pdf | PASS |
| Case 40 R10 npz 样本数 = 8 | 4 频率 x 2 样本，实得 8 | PASS |
| gen_extrap_R10.pdf 存在 | gen_extrap_R10.pdf | PASS |
| Case 41 W9 npz 样本数 = 8 | 4 频率 x 2 样本，实得 8 | PASS |
| gen_extrap_W9.pdf 存在 | gen_extrap_W9.pdf | PASS |
| Case 42 W10 npz 样本数 = 8 | 4 频率 x 2 样本，实得 8 | PASS |
| gen_extrap_W10.pdf 存在 | gen_extrap_W10.pdf | PASS |

## 2. epoch 双侧判据

> 图取 ep200(last)，兄弟表 Table 19 取 best epoch，本是两套口径。故除『caption 含 last』外，还须断言『caption 未误写 best』。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:gen-grid caption 声明 last epoch |  | PASS |
| fig:gen-grid caption 未误写 best epoch |  | PASS |
| fig:gen-grid-wedge caption 声明 last epoch |  | PASS |
| fig:gen-grid-wedge caption 未误写 best epoch |  | PASS |
| Case 39 R9 npz epoch == 200 (last) | 实得 [200] | PASS |
| Case 39 best epoch 可读 | best=168, last=200, 相差 32 轮 | PASS |
| Case 40 R10 npz epoch == 200 (last) | 实得 [200] | PASS |
| Case 40 best epoch 可读 | best=168, last=200, 相差 32 轮 | PASS |
| Case 41 W9 npz epoch == 200 (last) | 实得 [200] | PASS |
| Case 41 best epoch 可读 | best=184, last=200, 相差 16 轮 | PASS |
| Case 42 W10 npz epoch == 200 (last) | 实得 [200] | PASS |
| Case 42 best epoch 可读 | best=197, last=200, 相差 3 轮 | PASS |

## 3. ★ 展示样本必须全部落在外推区内

> caption 称『on the held-out region』。若有任一展示样本的源坐标落在训练区内，整张图的论点（外推能力）就不成立——这是本组独有的约束，前面各组都没有。逐样本核 8 个源坐标的区域归属。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 39 R9 8 个样本全在外推区（depth > 96 m）内 | 全部合规 | PASS |
| Case 40 R10 8 个样本全在外推区（range > 96 m）内 | 全部合规 | PASS |
| Case 41 W9 8 个样本全在外推区（depth > 48 m）内 | 全部合规 | PASS |
| Case 42 W10 8 个样本全在外推区（range > 96 m）内 | 全部合规 | PASS |

## 4. 逐样本 Avg 误差：npz 重算 vs 图上标注

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 39 R9 8 个 Avg 逐一吻合 | PDF ['1.91', '1.58', '4.20', '2.78', '5.92', '3.42', '5.96', '5.26'] / npz 重算 ['1.91', '1.58', '4.20', '2.78', '5.92', '3.42', '5.96', '5.26'] | PASS |
| Case 40 R10 8 个 Avg 逐一吻合 | PDF ['0.81', '4.25', '3.97', '2.23', '3.80', '1.39', '3.62', '0.76'] / npz 重算 ['0.81', '4.25', '3.97', '2.23', '3.80', '1.39', '3.62', '0.76'] | PASS |
| Case 41 W9 8 个 Avg 逐一吻合 | PDF ['1.68', '3.31', '7.48', '6.33', '2.30', '3.06', '6.67', '6.17'] / npz 重算 ['1.68', '3.31', '7.48', '6.33', '2.30', '3.06', '6.67', '6.17'] | PASS |
| Case 42 W10 8 个 Avg 逐一吻合 | PDF ['1.09', '10.57', '3.61', '1.79', '6.68', '1.32', '5.79', '6.29'] / npz 重算 ['1.09', '10.57', '3.61', '1.79', '6.68', '1.32', '5.79', '6.29'] | PASS |

## 5. 子图 label 与外推类型/阈值对应

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:gen-grid 编号为 21 | aux `21` | PASS |
| 子图 `fig:gen-r9` 编号为 21a/21b 之一 | aux `21a` | PASS |
| 子图 `fig:gen-r9` 题注含数据集名 R9 |  | PASS |
| 子图 `fig:gen-r9` 题注标明 deep extrapolation | tex 用 `deep`，Table 19 同一划分记作 `depth` | PASS |
| 子图 `fig:gen-r9` 题注标明阈值 96 m |  | PASS |
| 子图 `fig:gen-r10` 编号为 21a/21b 之一 | aux `21b` | PASS |
| 子图 `fig:gen-r10` 题注含数据集名 R10 |  | PASS |
| 子图 `fig:gen-r10` 题注标明 range extrapolation | tex 用 `range`，Table 19 同一划分记作 `range` | PASS |
| 子图 `fig:gen-r10` 题注标明阈值 96 m |  | PASS |
| fig:gen-grid-wedge 编号为 22 | aux `22` | PASS |
| 子图 `fig:gen-w9` 编号为 22a/22b 之一 | aux `22a` | PASS |
| 子图 `fig:gen-w9` 题注含数据集名 W9 |  | PASS |
| 子图 `fig:gen-w9` 题注标明 deep extrapolation | tex 用 `deep`，Table 19 同一划分记作 `depth` | PASS |
| 子图 `fig:gen-w9` 题注标明阈值 48 m |  | PASS |
| 子图 `fig:gen-w10` 编号为 22a/22b 之一 | aux `22b` | PASS |
| 子图 `fig:gen-w10` 题注含数据集名 W10 |  | PASS |
| 子图 `fig:gen-w10` 题注标明 range extrapolation | tex 用 `range`，Table 19 同一划分记作 `range` | PASS |
| 子图 `fig:gen-w10` 题注标明阈值 96 m |  | PASS |

## 5b. caption 的取样措辞与实际机制相符

> 本组按索引顺序取每频率前 2 个样本（非择优），故 caption 应写 the first two，不应含混称 representative。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:gen-grid caption 写明取样方式或明确继承 | 含 `the first two` | PASS |
| fig:gen-grid caption 未含混使用 representative |  | PASS |
| fig:gen-grid-wedge caption 写明取样方式或明确继承 | 以 Layout as in 继承 | PASS |
| fig:gen-grid-wedge caption 未含混使用 representative |  | PASS |

## 6. 正文引用

> 正文 4.7 节以 `Figs.~\ref{fig:gen-grid} and \ref{fig:gen-grid-wedge}` 并列引用两张图，非区间引用。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文并列引用 Fig 21 与 Fig 22 | 含 `Figs.~\ref{fig:gen-grid} and \ref{fig:gen-grid-wedge}` | PASS |
| 正文描述该组图的内容 | tex 行 1154 | PASS |

