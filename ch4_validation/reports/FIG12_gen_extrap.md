# Fig. 12 — 源位置外推场图 Fig 12（矩形 R9/R10）

- 对象：`fig:gen-grid`（Fig. 12）
- 结论：**PASS** — 54 通过 / 0 失败 / 0 警告 / 3 豁免，共 57 项
- 脚本：`ch4_validation/scripts/FIG12_gen_extrap.py`
- 生成：2026-10-04 13:27:37

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{fig:gen-grid}` 所在 figure*，含 2 个 subfloat（R9 | R10） |
| 成图脚本（矩形两幅） | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py` | fig04_05_10_fields.py 的 FIG11 列表生成 gen_extrap_r9/r10 |
| 兄弟表 | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{tab:gen-overall}` = Table 13（best epoch） |
| 数据源 npz (Case 39 R9) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No39_R9/Case39_R9__TL原始数据_ep200.npz` | Raw_Experimental_Data/4.7，ep200 |
| 数据源 npz (Case 40 R10) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No40_R10/Case40_R10__TL原始数据_ep200.npz` | Raw_Experimental_Data/4.7，ep200 |

## 2. 源可追溯与样本数

> ★ 本组成图脚本有两处，格式不同：R9/R10（正文 Fig 12）由 fig04_05_10_fields.py 生成，行标题 `f = 25 Hz (a),  Src (78.5, 122.3)` 且平均误差排在同一行（`Avg 1.91 dB`）；W9/W10（已从正文删除）由 fig12_gen_extrap.py 生成，行标题拆三行（`(f=25Hz, a)` / `Src (121.5, 68.0)` / `(Avg 1.68 dB)`）。两处的 regex 不能混用。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本（矩形两幅）已入库 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py | PASS |
| 成图脚本（楔形两幅）已入库（图已从正文删除，脚本留档） | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig12_gen_extrap/fig12_gen_extrap.py | PASS |
| 脚本内 R9/R10 行标题格式为 `f = NN Hz (a/b),  Src (x.x, y.y)` |  | PASS |
| 脚本内平均误差标注为 `Avg %.2f dB`（2 位小数） |  | PASS |
| Case 39 R9 npz 样本数 = 8 | 4 频率 x 2 样本，实得 8 | PASS |
| gen_extrap_R9.pdf 存在 | gen_extrap_R9.pdf | PASS |
| Case 40 R10 npz 样本数 = 8 | 4 频率 x 2 样本，实得 8 | PASS |
| gen_extrap_R10.pdf 存在 | gen_extrap_R10.pdf | PASS |

## 3. epoch 双侧判据与 caption 声明

> 图取 ep200(last)，兄弟表 Table 13 取 best epoch，本是两套口径。故除『caption 含 last』外，还须断言『caption 未误写 best』。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 last epoch |  | PASS |
| caption 未误写 best epoch |  | PASS |
| Case 39 R9 npz epoch == 200 (last) | 实得 [200] | PASS |
| Case 39 best epoch 可读 | best=168, last=200, 相差 32 轮 | PASS |
| Case 40 R10 npz epoch == 200 (last) | 实得 [200] | PASS |
| Case 40 best epoch 可读 | best=168, last=200, 相差 32 轮 | PASS |

## 4. ★ 展示样本必须全部落在外推区内

> caption 称『on the held-out region』。若有任一展示样本的源坐标落在训练区内，整张图的论点（外推能力）就不成立——这是本组独有的约束，前面各组都没有。逐样本核 8 个源坐标的区域归属。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 13 解析到 4 行（R9/R10/W9/W10） | 实得 4 | PASS |
| Case 39 R9 8 个样本全在外推区（depth > 96 m）内 | 全部合规 | PASS |
| Table 13 含 Case 39 行 |  | PASS |
| Table 13 的 R9 阈值与图一致（96 m） | 表列 `depth ($y>96\mathrmm$)` / 图 depth > 96 | PASS |
| Case 40 R10 8 个样本全在外推区（range > 96 m）内 | 全部合规 | PASS |
| Table 13 含 Case 40 行 |  | PASS |
| Table 13 的 R10 阈值与图一致（96 m） | 表列 `range ($x>96\mathrmm$)` / 图 range > 96 | PASS |

## 5. 逐样本 Avg 误差：npz 重算 vs 图上标注

> R9/R10 的 `Avg x.xx dB` 与频率/声源同排一行；重算给全精度，判定用舍入到 2 位的印刷值。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 39 R9 8 个 Avg 逐一吻合 | 全部吻合 | PASS |
| Case 39 R9 图上解析到 8 个 Avg 标注 | 实得 8 | PASS |
| Case 39 R9 8 个 Src 坐标吻合 | PDF [('78.5', '122.3'), ('110.0', '119.9'), ('122.3', '115.5'), ('56.5', '112.6'), ('15.2', '112.2'), ('13.0', '101.0'), ('54.0', '103.7'), ('65.0', '116.7')] / npz [('78.5', '122.3'), ('110.0', '119.9'), ('122.3', '115.5'), ('56.5', '112.6'), ('15.2', '112.2'), ('13.0', '101.0'), ('54.0', '103.7'), ('65.0', '116.7')] | PASS |
| Case 39 R9 8 行频率序 = 每频率 2 样本 | 图上 `[('25', 'a'), ('25', 'b'), ('50', 'a'), ('50', 'b'), ('75', 'a'), ('75', 'b'), ('100', 'a'), ('100', 'b')]` | PASS |
| Case 39 R9 行标签的样本字母为 a/b 交替 | 每频率两个样本标 (a)/(b) | PASS |
| Case 40 R10 8 个 Avg 逐一吻合 | 全部吻合 | PASS |
| Case 40 R10 图上解析到 8 个 Avg 标注 | 实得 8 | PASS |
| Case 40 R10 8 个 Src 坐标吻合 | PDF [('109.4', '85.5'), ('108.5', '122.3'), ('122.3', '115.5'), ('101.3', '63.5'), ('114.3', '13.6'), ('97.5', '15.4'), ('117.5', '45.5'), ('96.6', '78.0')] / npz [('109.4', '85.5'), ('108.5', '122.3'), ('122.3', '115.5'), ('101.3', '63.5'), ('114.3', '13.6'), ('97.5', '15.4'), ('117.5', '45.5'), ('96.6', '78.0')] | PASS |
| Case 40 R10 8 行频率序 = 每频率 2 样本 | 图上 `[('25', 'a'), ('25', 'b'), ('50', 'a'), ('50', 'b'), ('75', 'a'), ('75', 'b'), ('100', 'a'), ('100', 'b')]` | PASS |
| Case 40 R10 行标签的样本字母为 a/b 交替 | 每频率两个样本标 (a)/(b) | PASS |

## 6. 子图 label 与数据集名 / 外推类型 / 阈值对应

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 子图 `fig:gen-r9` 编号前缀为 12 | aux `12a` | PASS |
| 子图 `fig:gen-r9` 是 Fig. 12a | aux `12a` | PASS |
| 子图 `fig:gen-r9` 题注含数据集名 R9 | 题注 `R9, rectangular, deep extrapolation (y>96\mathrm{m})` | PASS |
| 子图 `fig:gen-r9` 题注标明 deep extrapolation | 题注 `R9, rectangular, deep extrapolation (y>96\mathrm{m})`；tex 用 `deep`，Table 13 同一划分记作 `depth` | PASS |
| 子图 `fig:gen-r9` 题注标明阈值 96 m | 题注 `R9, rectangular, deep extrapolation (y>96\mathrm{m})` | PASS |
| 子图 `fig:gen-r10` 编号前缀为 12 | aux `12b` | PASS |
| 子图 `fig:gen-r10` 是 Fig. 12b | aux `12b` | PASS |
| 子图 `fig:gen-r10` 题注含数据集名 R10 | 题注 `R10, rectangular, range extrapolation (x>96\mathrm{m})` | PASS |
| 子图 `fig:gen-r10` 题注标明 range extrapolation | 题注 `R10, rectangular, range extrapolation (x>96\mathrm{m})`；tex 用 `range`，Table 13 同一划分记作 `range` | PASS |
| 子图 `fig:gen-r10` 题注标明阈值 96 m | 题注 `R10, rectangular, range extrapolation (x>96\mathrm{m})` | PASS |

## 7. caption 的取样措辞与实际机制相符

> 本组按索引顺序取每频率前 2 个样本（非择优），故 caption 应写 the first two，不应含混称 representative。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 写明取每频率前两个样本 | 含 `the first two held-out samples` | PASS |
| caption 未含混使用 representative |  | PASS |
| caption 说明行以 a/b 标样本 |  | PASS |
| caption 声明矩形几何 |  | PASS |

## 8. R1 版式变动：楔形两幅已从正文删除

> ★ R1 把 W9/W10 两幅（旧 fig:gen-grid-wedge = Fig 22）从正文删除，正文以 `Fig.~S5` 引用。故 main text 只剩矩形一张；相关核验项（旧 Fig 22 编号、gen-w9/gen-w10 子图号、wedge caption 的 last epoch）在 R1 已无对象，逐条豁免如下。W9/W10 的 PDF 与其脚本仍在仓库内，供回溯核对。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| `fig:gen-grid-wedge` 已不在正文（aux 无登记） | R1 已从正文删除 | PASS |
| `fig:gen-w9` 已不在正文（aux 无登记） | R1 已从正文删除 | PASS |
| `fig:gen-w10` 已不在正文（aux 无登记） | R1 已从正文删除 | PASS |
| 旧 Fig 22（fig:gen-grid-wedge）编号 == 22 | 该浮动体在 R1 已整段注释从正文删除，aux 无登记 | 豁免 |
| 子图 fig:gen-w9 / fig:gen-w10 编号为 22a/22b | 两幅随楔形图从正文删除，main text 不再引用其 label | 豁免 |
| 删除的楔形浮动体以注释形式留在 tex 中（可回溯） | tex 内含注释掉的 \label{fig:gen-grid-wedge} | PASS |
| 已删图件 gen_extrap_W9.pdf 仍在 Figures/results/ | W9 | PASS |
| 已删图件 gen_extrap_W10.pdf 仍在 Figures/results/ | W10 | PASS |

## 9. 正文引用

> 正文 4.7 节以 `Fig.~\ref{fig:gen-grid} and Fig.~S5` 并列引用矩形（正文）与楔形（补充）两张图，非区间引用，且第二张已改为硬写的 （R1 已改为只引用矩形图）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文引用 Fig. 12 |  | PASS |
| 正文以 `Fig.~\ref{fig:gen-grid} and Fig.~S7` 并列引用矩形与楔形外推图 | 楔形 W9/W10 在补充材料 Fig. S7 | PASS |
| 正文并列引用 Fig 21 与 Fig 22（`\ref{{fig:gen-grid}} and \ref{{fig:gen-grid-wedge}}`） | R1 的楔形图已从正文删除，正文改写为 `Fig.~S5` 硬引用，不再有 fig:gen-grid-wedge 的 \ref | 豁免 |
| 正文描述该组图的内容 | tex 行 1126 | PASS |

