# Fig. 12 — 源位置外推场图 Fig 12（矩形 R9 深区 + 楔形 W10 远区）

- 对象：`fig:gen-grid`（Fig. 12）
- 结论：**PASS** — 58 通过 / 0 失败 / 0 警告，共 58 项
- 脚本：`ch4_validation/scripts/FIG12_gen_extrap.py`
- 生成：2026-10-06 00:29:11

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{fig:gen-grid}` 所在 figure*，含 2 个 subfloat（R9 | W10） |
| 成图脚本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py` | fig04_05_10_fields.py 的 FIG12 列表生成 gen_extrap_r9/w10 |
| 兄弟表 | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{tab:gen-overall}` = Table 12（best epoch） |
| 数据源 npz (Case 39 R9) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No39_R9/Case39_R9__TL原始数据_ep200.npz` | Raw_Experimental_Data/4.7，ep200 |
| 数据源 npz (Case 42 W10) | `Data_and_Code_Availability/Raw_Experimental_Data/4.7_Generalization/No42_W10/Case42_W10__TL原始数据_ep200.npz` | Raw_Experimental_Data/4.7，ep200 |

## 2. 源可追溯与样本数

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本已入库 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py | PASS |
| 脚本 FIG12 列表 = Case39→gen_extrap_r9, Case42→gen_extrap_w10 |  | PASS |
| 脚本内行标题格式为 `f = NN Hz (a/b),  Src (x.x, y.y)` |  | PASS |
| 脚本内平均误差标注为 `Avg %.2f dB`（2 位小数） |  | PASS |
| Case 39 R9 npz 样本数 = 8 | 4 频率 x 2 样本，实得 8 | PASS |
| gen_extrap_R9.pdf 存在 | gen_extrap_R9.pdf | PASS |
| Case 42 W10 npz 样本数 = 8 | 4 频率 x 2 样本，实得 8 | PASS |
| gen_extrap_W10.pdf 存在 | gen_extrap_W10.pdf | PASS |

## 3. epoch 双侧判据与 caption 声明

> 图取 ep200(last)，兄弟表 Table 12 取 best epoch，本是两套口径。故除『caption 含 last』外，还须断言『caption 未误写 best』。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 声明 last epoch |  | PASS |
| caption 未误写 best epoch |  | PASS |
| Case 39 R9 npz epoch == 200 (last) | 实得 [200] | PASS |
| Case 39 best epoch 可读 | best=168, last=200, 相差 32 轮 | PASS |
| Case 42 W10 npz epoch == 200 (last) | 实得 [200] | PASS |
| Case 42 best epoch 可读 | best=197, last=200, 相差 3 轮 | PASS |

## 4. ★ 展示样本必须全部落在外推区内

> caption 称『on the held-out region』。若有任一展示样本的源坐标落在训练区内，整张图的论点（外推能力）就不成立。逐样本核 8 个源坐标的区域归属。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 12 解析到 4 行（R9/R10/W9/W10） | 实得 4 | PASS |
| Case 39 R9 8 个样本全在外推区（depth > 96 m）内 | 全部合规 | PASS |
| Table 12 含 Case 39 行 |  | PASS |
| Table 12 的 R9 阈值与图一致（96 m） | 表列 `depth ($y>96\mathrmm$)` / 图 depth > 96 | PASS |
| Case 42 W10 8 个样本全在外推区（range > 96 m）内 | 全部合规 | PASS |
| Table 12 含 Case 42 行 |  | PASS |
| Table 12 的 W10 阈值与图一致（96 m） | 表列 `range ($x>96\mathrmm$)` / 图 range > 96 | PASS |

## 5. 逐样本 Avg 误差：npz 重算 vs 图上标注

> `Avg x.xx dB` 与频率/声源同排一行；重算给全精度，判定用舍入到 2 位的印刷值。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 39 R9 8 个 Avg 逐一吻合 | 全部吻合 | PASS |
| Case 39 R9 图上解析到 8 个 Avg 标注 | 实得 8 | PASS |
| Case 39 R9 8 个 Src 坐标吻合 | PDF [('78.5', '122.3'), ('110.0', '119.9'), ('122.3', '115.5'), ('56.5', '112.6'), ('15.2', '112.2'), ('13.0', '101.0'), ('54.0', '103.7'), ('65.0', '116.7')] / npz [('78.5', '122.3'), ('110.0', '119.9'), ('122.3', '115.5'), ('56.5', '112.6'), ('15.2', '112.2'), ('13.0', '101.0'), ('54.0', '103.7'), ('65.0', '116.7')] | PASS |
| Case 39 R9 8 行频率序 = 每频率 2 样本 | 图上 `[('25', 'a'), ('25', 'b'), ('50', 'a'), ('50', 'b'), ('75', 'a'), ('75', 'b'), ('100', 'a'), ('100', 'b')]` | PASS |
| Case 39 R9 行标签的样本字母为 a/b 交替 | 每频率两个样本标 (a)/(b) | PASS |
| Case 42 W10 8 个 Avg 逐一吻合 | 全部吻合 | PASS |
| Case 42 W10 图上解析到 8 个 Avg 标注 | 实得 8 | PASS |
| Case 42 W10 8 个 Src 坐标吻合 | PDF [('102.2', '78.1'), ('112.1', '102.9'), ('118.3', '109.3'), ('100.5', '59.9'), ('111.5', '10.5'), ('97.5', '14.4'), ('119.2', '43.5'), ('119.1', '56.5')] / npz [('102.2', '78.1'), ('112.1', '102.9'), ('118.3', '109.3'), ('100.5', '59.9'), ('111.5', '10.5'), ('97.5', '14.4'), ('119.2', '43.5'), ('119.1', '56.5')] | PASS |
| Case 42 W10 8 行频率序 = 每频率 2 样本 | 图上 `[('25', 'a'), ('25', 'b'), ('50', 'a'), ('50', 'b'), ('75', 'a'), ('75', 'b'), ('100', 'a'), ('100', 'b')]` | PASS |
| Case 42 W10 行标签的样本字母为 a/b 交替 | 每频率两个样本标 (a)/(b) | PASS |

## 6. 子图 label 与数据集名 / 几何 / 外推类型 / 阈值对应

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 子图 `fig:gen-r9` 编号前缀为 12 | aux `12a` | PASS |
| 子图 `fig:gen-r9` 是 Fig. 12a | aux `12a` | PASS |
| 子图 `fig:gen-r9` 题注含数据集名 R9 | 题注 `R9, rectangular, deep extrapolation (y>96\mathrm{m})` | PASS |
| 子图 `fig:gen-r9` 题注标明几何 rectangular | 题注 `R9, rectangular, deep extrapolation (y>96\mathrm{m})` | PASS |
| 子图 `fig:gen-r9` 题注标明 deep extrapolation | 题注 `R9, rectangular, deep extrapolation (y>96\mathrm{m})`；tex 用 `deep`，Table 12 同一划分记作 `depth` | PASS |
| 子图 `fig:gen-r9` 题注标明阈值 96 m | 题注 `R9, rectangular, deep extrapolation (y>96\mathrm{m})` | PASS |
| 子图 `fig:gen-w10` 编号前缀为 12 | aux `12b` | PASS |
| 子图 `fig:gen-w10` 是 Fig. 12b | aux `12b` | PASS |
| 子图 `fig:gen-w10` 题注含数据集名 W10 | 题注 `W10, wedge, range extrapolation (x>96\mathrm{m})` | PASS |
| 子图 `fig:gen-w10` 题注标明几何 wedge | 题注 `W10, wedge, range extrapolation (x>96\mathrm{m})` | PASS |
| 子图 `fig:gen-w10` 题注标明 range extrapolation | 题注 `W10, wedge, range extrapolation (x>96\mathrm{m})`；tex 用 `range`，Table 12 同一划分记作 `range` | PASS |
| 子图 `fig:gen-w10` 题注标明阈值 96 m | 题注 `W10, wedge, range extrapolation (x>96\mathrm{m})` | PASS |

## 7. caption 的取样措辞与实际机制相符

> 本组按索引顺序取每频率前 2 个样本（非择优），故 caption 应写 the first two，不应含混称 representative；两幅分属两种几何，caption 须两者都点明，并指向 Fig. S7。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 写明取每频率前两个样本 | 含 `the first two held-out samples` | PASS |
| caption 未含混使用 representative |  | PASS |
| caption 说明行以 a/b 标样本 |  | PASS |
| caption 同时点明矩形与楔形 |  | PASS |
| caption 标出 R9 与 W10 |  | PASS |
| caption 指出余下两幅（R10, W9）在 Fig.~S7 |  | PASS |

## 8. 余下两个分割（R10/W9）在补充材料

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| `fig:gen-grid-wedge` 不在正文（aux 无登记） | R10/W9 两幅在补充材料 Fig. S7 | PASS |
| `fig:gen-r10` 不在正文（aux 无登记） | R10/W9 两幅在补充材料 Fig. S7 | PASS |
| `fig:gen-w9` 不在正文（aux 无登记） | R10/W9 两幅在补充材料 Fig. S7 | PASS |
| 旧楔形浮动体的注释残留已清除 |  | PASS |
| 补充材料图件 figS7a_gen_extrap_r10.pdf（Case 40 R10）存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS7a_gen_extrap_r10.pdf | PASS |
| 补充材料图件 figS7b_gen_extrap_w9.pdf（Case 41 W9）存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS7b_gen_extrap_w9.pdf | PASS |

## 9. 正文引用

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文引用 Fig. 12 |  | PASS |
| 正文 4.7 节把 Fig. 12（R9/W10）与 Fig. S7（R10/W9）并列引用 |  | PASS |
| 正文描述该组图的内容 | tex 行 1105 | PASS |

