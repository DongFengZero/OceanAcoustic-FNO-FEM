# Table 9 — 消融深度线 TL（矩形 y=71.9m 与楔形 y=33.4m 并排）

- 对象：`tab:dl-abl`（Table 9）
- 结论：**PASS** — 156 通过 / 0 失败 / 0 警告 / 1 豁免，共 157 项
- 脚本：`ch4_validation/scripts/T09_dl_abl.py`
- 生成：2026-10-04 12:47:36

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{tab:dl-abl}` 所在 tabular* |
| 成图/取数脚本（权威） | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/_depthline_core.py` | 组 `ablation_R1_module_advantage` / `ablation_W1_module_advantage` |
| 同一脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/legacy/advantage_depth_line.py` | 口径与权威副本同源 |
| 脚本导出 MAE 表 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/cache/_mae_tables.json` | round 到 3 位，供正文取用 |
| 论文图件（矩形 R1） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/ablation_R1_module_advantage.pdf` | 成图脚本 out/ 下的纸面尺寸 PDF |
| 论文图件（楔形 W1） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/ablation_W1_module_advantage.pdf` | 成图脚本 out/ 下的纸面尺寸 PDF |

## 2. 源可追溯性与脚本同源

> 深度线的口径由 `Validation_Scripts/fig06_07_dl/_depthline_core.py` 承载，成图脚本 `fig06_07_dl.py` 直接加载它、不复制算法；`common/depthline.py` 又直接 import 同一份 core，故三者口径不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 权威脚本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/_depthline_core.py | PASS |
| repo 副本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/legacy/advantage_depth_line.py | PASS |
| MAE json 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/cache/_mae_tables.json | PASS |
| Case25_R1_Full 的 ep200 npz 存在 | Case25-32/Case25_R1_Full/Case25_R1_Full__TL原始数据_ep200.npz | PASS |
| Case26_R1_no_prior 的 ep200 npz 存在 | Case25-32/Case26_R1_no_prior/Case26_R1_no_prior__TL原始数据_ep200.npz | PASS |
| Case27_R1_no_graph 的 ep200 npz 存在 | Case25-32/Case27_R1_no_graph/Case27_R1_no_graph__TL原始数据_ep200.npz | PASS |
| Case28_R1_no_prior_loss 的 ep200 npz 存在 | Case25-32/Case28_R1_no_prior_loss/Case28_R1_no_prior_loss__TL原始数据_ep200.npz | PASS |
| Case29_W1_Full 的 ep200 npz 存在 | Case25-32/Case29_W1_Full/Case29_W1_Full__TL原始数据_ep200.npz | PASS |
| Case30_W1_no_prior 的 ep200 npz 存在 | Case25-32/Case30_W1_no_prior/Case30_W1_no_prior__TL原始数据_ep200.npz | PASS |
| Case31_W1_no_graph 的 ep200 npz 存在 | Case25-32/Case31_W1_no_graph/Case31_W1_no_graph__TL原始数据_ep200.npz | PASS |
| Case32_W1_no_prior_loss 的 ep200 npz 存在 | Case25-32/Case32_W1_no_prior_loss/Case32_W1_no_prior_loss__TL原始数据_ep200.npz | PASS |

## 3. 提取口径防漂移

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 插值网格 GRID = 300 | 脚本内 `300` | PASS |
| 插值方式 METHOD = 'cubic' | 脚本内 `'cubic'` | PASS |
| 频率集 FREQS = (25, 50, 75, 100) | 脚本内 `(25, 50, 75, 100)` | PASS |
| [rect] 指定深度线 force_y = 71.9 | 脚本内 `71.9` | PASS |
| [rect] 数据目录 grpdir = 'Case25-32' | 脚本内 `'Case25-32'` | PASS |
| [rect] 域类型 = 'Rectangle' | 脚本内 `'Rectangle'` | PASS |
| [rect] 脚本变体顺序与 tex 行序一致 | Full (Ours) / w/o prior / w/o graph / w/o prior-sup. | PASS |
| [wedge] 指定深度线 force_y = 33.4 | 脚本内 `33.4` | PASS |
| [wedge] 数据目录 grpdir = 'Case25-32' | 脚本内 `'Case25-32'` | PASS |
| [wedge] 域类型 = 'Wedge' | 脚本内 `'Wedge'` | PASS |
| [wedge] 脚本变体顺序与 tex 行序一致 | Full (Ours) / w/o prior / w/o graph / w/o prior-sup. | PASS |

## 4. 全精度重算（复用脚本自身函数）

> [rect] 重算落在第 168 行，实际深度 y=71.919732 m；force_y=71.9 取最近行，caption 写 71.9 m 是其一位小数。

> [wedge] 重算落在第 78 行，实际深度 y=33.391304 m；force_y=33.4 取最近行，caption 写 33.4 m 是其一位小数。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| [rect] 选中行深度舍入到 1 位 = 71.9 m | 实际 `71.919732` | PASS |
| [wedge] 选中行深度舍入到 1 位 = 33.4 m | 实际 `33.391304` | PASS |
| tex 表体可定位 | 长度 1133 | PASS |
| 表体为 tabular*（固定总宽） | is_star=True | PASS |
| caption 声明 rect 深度 y=71.9 m（与重算一致） | caption 含该值 | PASS |
| caption 声明 rect 的 Cases~25--28 |  | PASS |
| caption 声明 wedge 深度 y=33.4 m（与重算一致） | caption 含该值 | PASS |
| caption 声明 wedge 的 Cases~29--32 |  | PASS |
| caption 以 Table 8 交代 header/emphasis/epoch 约定（含 epoch） | 故本表不再重复 last epoch 字样 | PASS |

## 5. json 与全精度重算一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| [rect] json y_line 与重算一致 | json `71.92` / 重算 `71.92` | PASS |
| [rect] 25Hz Full (Ours) json vs 重算 | json `1.092` / 重算 `1.092168347` | PASS |
| [rect] 25Hz w/o prior json vs 重算 | json `26.344` / 重算 `26.343610194` | PASS |
| [rect] 25Hz w/o graph json vs 重算 | json `0.968` / 重算 `0.968006704` | PASS |
| [rect] 25Hz w/o prior-sup. json vs 重算 | json `0.54` / 重算 `0.540375313` | PASS |
| [rect] 50Hz Full (Ours) json vs 重算 | json `0.533` / 重算 `0.532955990` | PASS |
| [rect] 50Hz w/o prior json vs 重算 | json `30.274` / 重算 `30.274313204` | PASS |
| [rect] 50Hz w/o graph json vs 重算 | json `0.547` / 重算 `0.546991315` | PASS |
| [rect] 50Hz w/o prior-sup. json vs 重算 | json `0.649` / 重算 `0.649440036` | PASS |
| [rect] 75Hz Full (Ours) json vs 重算 | json `1.547` / 重算 `1.547306137` | PASS |
| [rect] 75Hz w/o prior json vs 重算 | json `34.122` / 重算 `34.121951553` | PASS |
| [rect] 75Hz w/o graph json vs 重算 | json `2.903` / 重算 `2.903096185` | PASS |
| [rect] 75Hz w/o prior-sup. json vs 重算 | json `3.003` / 重算 `3.002957203` | PASS |
| [rect] 100Hz Full (Ours) json vs 重算 | json `3.174` / 重算 `3.174377784` | PASS |
| [rect] 100Hz w/o prior json vs 重算 | json `35.063` / 重算 `35.062962102` | PASS |
| [rect] 100Hz w/o graph json vs 重算 | json `5.008` / 重算 `5.007778557` | PASS |
| [rect] 100Hz w/o prior-sup. json vs 重算 | json `5.244` / 重算 `5.244146412` | PASS |
| [wedge] json y_line 与重算一致 | json `33.39` / 重算 `33.39` | PASS |
| [wedge] 25Hz Full (Ours) json vs 重算 | json `0.545` / 重算 `0.545448316` | PASS |
| [wedge] 25Hz w/o prior json vs 重算 | json `8.733` / 重算 `8.732524553` | PASS |
| [wedge] 25Hz w/o graph json vs 重算 | json `1.44` / 重算 `1.439754998` | PASS |
| [wedge] 25Hz w/o prior-sup. json vs 重算 | json `1.008` / 重算 `1.007677660` | PASS |
| [wedge] 50Hz Full (Ours) json vs 重算 | json `0.205` / 重算 `0.205193785` | PASS |
| [wedge] 50Hz w/o prior json vs 重算 | json `32.909` / 重算 `32.908629110` | PASS |
| [wedge] 50Hz w/o graph json vs 重算 | json `0.306` / 重算 `0.306454512` | PASS |
| [wedge] 50Hz w/o prior-sup. json vs 重算 | json `0.425` / 重算 `0.425215799` | PASS |
| [wedge] 75Hz Full (Ours) json vs 重算 | json `1.417` / 重算 `1.417487228` | PASS |
| [wedge] 75Hz w/o prior json vs 重算 | json `40.582` / 重算 `40.581971256` | PASS |
| [wedge] 75Hz w/o graph json vs 重算 | json `2.289` / 重算 `2.289158269` | PASS |
| [wedge] 75Hz w/o prior-sup. json vs 重算 | json `2.21` / 重算 `2.210329951` | PASS |
| [wedge] 100Hz Full (Ours) json vs 重算 | json `4.094` / 重算 `4.093890783` | PASS |
| [wedge] 100Hz w/o prior json vs 重算 | json `34.329` / 重算 `34.329034211` | PASS |
| [wedge] 100Hz w/o graph json vs 重算 | json `4.623` / 重算 `4.623336897` | PASS |
| [wedge] 100Hz w/o prior-sup. json vs 重算 | json `4.219` / 重算 `4.218932819` | PASS |

## 6. 印刷值比对（全精度舍入到 3 位 vs tex）

> 判定用全精度值，不用 json —— json 已是 round(...,3)。本表含大量两位整数级 MAE（去先验后 26-40 dB），末位 0 的格子尤须回溯全精度确认第 3 位真的是 0。行以变体名为键，矩形块占列 1-4、楔形块占列 5-8。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 数据行数 = 4 | 实得 4 | PASS |
| 行以变体名为键且顺序一致 | Full model / w/o physics prior / w/o graph correction / w/o prior supervision | PASS |
| 行 `Full model` 存在 |  | PASS |
| Full model rect 25Hz | 源 1.092168346691922 → `1.092` / 印刷 `1.092` | PASS |
| Full model rect 50Hz | 源 0.5329559900137699 → `0.533` / 印刷 `0.533` | PASS |
| Full model rect 75Hz | 源 1.5473061373714823 → `1.547` / 印刷 `1.547` | PASS |
| Full model rect 100Hz | 源 3.1743777836681213 → `3.174` / 印刷 `3.174` | PASS |
| Full model wedge 25Hz | 源 0.5454483164813005 → `0.545` / 印刷 `0.545` | PASS |
| Full model wedge 50Hz | 源 0.205193784828277 → `0.205` / 印刷 `0.205` | PASS |
| Full model wedge 75Hz | 源 1.417487228217092 → `1.417` / 印刷 `1.417` | PASS |
| Full model wedge 100Hz | 源 4.093890782681291 → `4.094` / 印刷 `4.094` | PASS |
| 行 `w/o physics prior` 存在 |  | PASS |
| w/o physics prior rect 25Hz | 源 26.343610194470056 → `26.344` / 印刷 `26.344` | PASS |
| w/o physics prior rect 50Hz | 源 30.27431320444456 → `30.274` / 印刷 `30.274` | PASS |
| w/o physics prior rect 75Hz | 源 34.121951553211204 → `34.122` / 印刷 `34.122` | PASS |
| w/o physics prior rect 100Hz | 源 35.06296210235836 → `35.063` / 印刷 `35.063` | PASS |
| w/o physics prior wedge 25Hz | 源 8.732524553217452 → `8.733` / 印刷 `8.733` | PASS |
| w/o physics prior wedge 50Hz | 源 32.90862910998996 → `32.909` / 印刷 `32.909` | PASS |
| w/o physics prior wedge 75Hz | 源 40.58197125552458 → `40.582` / 印刷 `40.582` | PASS |
| w/o physics prior wedge 100Hz | 源 34.32903421065514 → `34.329` / 印刷 `34.329` | PASS |
| 行 `w/o graph correction` 存在 |  | PASS |
| w/o graph correction rect 25Hz | 源 0.9680067037698834 → `0.968` / 印刷 `0.968` | PASS |
| w/o graph correction rect 50Hz | 源 0.5469913147202249 → `0.547` / 印刷 `0.547` | PASS |
| w/o graph correction rect 75Hz | 源 2.9030961846184775 → `2.903` / 印刷 `2.903` | PASS |
| w/o graph correction rect 100Hz | 源 5.007778557240541 → `5.008` / 印刷 `5.008` | PASS |
| w/o graph correction wedge 25Hz | 源 1.439754998410447 → `1.440` / 印刷 `1.440` | PASS |
| w/o graph correction wedge 50Hz | 源 0.3064545123013916 → `0.306` / 印刷 `0.306` | PASS |
| w/o graph correction wedge 75Hz | 源 2.2891582692879773 → `2.289` / 印刷 `2.289` | PASS |
| w/o graph correction wedge 100Hz | 源 4.623336897004174 → `4.623` / 印刷 `4.623` | PASS |
| 行 `w/o prior supervision` 存在 |  | PASS |
| w/o prior supervision rect 25Hz | 源 0.5403753127041657 → `0.540` / 印刷 `0.540` | PASS |
| w/o prior supervision rect 50Hz | 源 0.6494400364717936 → `0.649` / 印刷 `0.649` | PASS |
| w/o prior supervision rect 75Hz | 源 3.0029572026769444 → `3.003` / 印刷 `3.003` | PASS |
| w/o prior supervision rect 100Hz | 源 5.244146412380103 → `5.244` / 印刷 `5.244` | PASS |
| w/o prior supervision wedge 25Hz | 源 1.0076776599015047 → `1.008` / 印刷 `1.008` | PASS |
| w/o prior supervision wedge 50Hz | 源 0.4252157986505235 → `0.425` / 印刷 `0.425` | PASS |
| w/o prior supervision wedge 75Hz | 源 2.2103299510185797 → `2.210` / 印刷 `2.210` | PASS |
| w/o prior supervision wedge 100Hz | 源 4.218932818512776 → `4.219` / 印刷 `4.219` | PASS |

## 7. 末位为 0 的单元格：真值还是补 0

> 凡印刷值末位为 0 的格，单看数字无法排除『2 位补 1 个 0』，逐个回溯全精度源值确认第 3 位确实是 0 或由进位得到。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| w/o graph correction wedge 25Hz 末位 0 可由全精度复现 | 全精度 1.439754998 → `1.440` | PASS |
| w/o prior supervision rect 25Hz 末位 0 可由全精度复现 | 全精度 0.540375313 → `0.540` | PASS |
| w/o prior supervision wedge 75Hz 末位 0 可由全精度复现 | 全精度 2.210329951 → `2.210` | PASS |
| 末位为 0 的格子共 3 个，全部回溯完毕 |  | PASS |

## 8. 表头源坐标与所选样本一致（两块各 4 个）

> 表头每频率标 $(x,y)$（`\srcxy`），须等于该频率**实际选中样本**的 source_pos；八个坐标互不相同，写错不会报编译错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 表头解析到 8 组源坐标（4 矩形 + 4 楔形） | [(44.5, 21.9), (25.9, 49.5), (51.5, 5.7), (62.8, 85.3), (92.7, 58.9), (117.6, 43.4), (56.7, 33.8), (45.5, 29.5)] | PASS |
| rect 25Hz 源坐标 | tex `(44.5, 21.9)` / 样本 0 实际 (44.50021, 21.86243) → `(44.5, 21.9)` | PASS |
| rect 50Hz 源坐标 | tex `(25.9, 49.5)` / 样本 2 实际 (25.88422, 49.48544) → `(25.9, 49.5)` | PASS |
| rect 75Hz 源坐标 | tex `(51.5, 5.7)` / 样本 5 实际 (51.50000, 5.66814) → `(51.5, 5.7)` | PASS |
| rect 100Hz 源坐标 | tex `(62.8, 85.3)` / 样本 6 实际 (62.75945, 85.33403) → `(62.8, 85.3)` | PASS |
| wedge 25Hz 源坐标 | tex `(92.7, 58.9)` / 样本 0 实际 (92.73300, 58.85380) → `(92.7, 58.9)` | PASS |
| wedge 50Hz 源坐标 | tex `(117.6, 43.4)` / 样本 2 实际 (117.61148, 43.44483) → `(117.6, 43.4)` | PASS |
| wedge 75Hz 源坐标 | tex `(56.7, 33.8)` / 样本 4 实际 (56.67198, 33.82414) → `(56.7, 33.8)` | PASS |
| wedge 100Hz 源坐标 | tex `(45.5, 29.5)` / 样本 7 实际 (45.49694, 29.46439) → `(45.5, 29.5)` | PASS |

## 9. 表与图同源（Table 9 ↔ Fig. 的两块）

> MAE 表和深度线图是同一次选线/选样本的两个产物。比对论文图件与成图脚本 out/ 下同名 PDF：内容逐字节相同（仅嵌入时间戳不同，比对前抹掉），则『表里的数』与『图里的线』必定来自同一次计算。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| [rect] 脚本产出 PDF 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out/ablation_R1_module_advantage.pdf | PASS |
| [rect] 论文图件存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/ablation_R1_module_advantage.pdf | PASS |
| [rect] 论文图件与脚本产物同源（抹时间戳后同 md5） | md5(no-ts) `42f638c60615d8900e98aadba3fa585d` | PASS |
| [wedge] 脚本产出 PDF 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out/ablation_W1_module_advantage.pdf | PASS |
| [wedge] 论文图件存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/ablation_W1_module_advantage.pdf | PASS |
| [wedge] 论文图件与脚本产物同源（抹时间戳后同 md5） | md5(no-ts) `abcd13e24b0b4f3aa06a69f1a891c073` | PASS |
| PDF 逐字节 md5 相同 | matplotlib 每次运行写入 CreationDate（本机实测 D:2026…），逐字节比对必然不等；已改为抹掉时间戳后比对，同源判定不受影响。 | 豁免 |

## 10. 加粗正确性（Best in bold，两块各自取列最小）

> caption 声明『emphasis as in Table 8』，即每列最优加粗；并排后每列分属不同几何，最小值必须在各自块内取。**本表矩形 25 Hz 的最小值落在 w/o prior supervision（0.540）而非 Full model**，加粗须跟着数走。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| rect 25Hz 加粗落在最小值行 | 加粗 ['w/o prior supervision'] / 最小值 w/o prior supervision (`0.540`) | PASS |
| rect 50Hz 加粗落在最小值行 | 加粗 ['Full model'] / 最小值 Full model (`0.533`) | PASS |
| rect 75Hz 加粗落在最小值行 | 加粗 ['Full model'] / 最小值 Full model (`1.547`) | PASS |
| rect 100Hz 加粗落在最小值行 | 加粗 ['Full model'] / 最小值 Full model (`3.174`) | PASS |
| wedge 25Hz 加粗落在最小值行 | 加粗 ['Full model'] / 最小值 Full model (`0.545`) | PASS |
| wedge 50Hz 加粗落在最小值行 | 加粗 ['Full model'] / 最小值 Full model (`0.205`) | PASS |
| wedge 75Hz 加粗落在最小值行 | 加粗 ['Full model'] / 最小值 Full model (`1.417`) | PASS |
| wedge 100Hz 加粗落在最小值行 | 加粗 ['Full model'] / 最小值 Full model (`4.094`) | PASS |

## 11. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 32 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 12. 与 Table 8 的版式一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 8 表体可定位 | 长度 1155 | PASS |
| Table 8 亦为 tabular* | is_star=True | PASS |
| 两表列定义可解析 | Table 9 `@{\extracolsep{\fill}}A EEEE EEEE@{}` / Table 8 `@{\extracolsep{\fill}}M EEEE EEEE@{}` | PASS |
| Table 9 列类型序列为 `A EEEE EEEE` | `@{\extracolsep{\fill}}A EEEE EEEE@{}` | PASS |
| Table 8 列类型序列为 `M EEEE EEEE`（首列标签列类型名不同，宽度同） | `@{\extracolsep{\fill}}M EEEE EEEE@{}` | PASS |
| Table 9 用 \extracolsep{\fill} 均分列间余量 | `@{\extracolsep{\fill}}A EEEE EEEE@{}` | PASS |
| Table 8 用 \extracolsep{\fill} 均分列间余量 | `@{\extracolsep{\fill}}M EEEE EEEE@{}` | PASS |
| 两表同用 \TABstyleDL（整表紧凑列距） |  | PASS |
| 两表的 tabular* 总宽参数一致（等宽并排） | dl-abl=`\linewidth` / dl-cmp=`\linewidth` | PASS |

## 13. 正文引用精确性（4.5 节）

> 正文：`the graph correction provides particularly strong improvements at the higher frequencies, reducing the TL by $1.356$\,dB at $75$\,Hz and $1.834$\,dB at $100$\,Hz`（矩形块）。这两数是 w/o graph 与 Full model 之差。★ 须注意正文是按**表中印出的 3 位值**相减，与全精度相减在第 3 位可能差 1；两者分别核验，不混为一谈。

> 口径：正文的派生量按**表中印出的 3 位值**计算，与 4.3 节的 8.676 同源（3.852/0.444 用印刷值，全精度会得 8.670）。故此处以印刷值口径为准；全精度差值一并列出，若有第 3 位差异，读者能在报告里看到它来自口径而非数据。

> 75Hz：全精度相减得 `1.355790047` → `1.356`；与正文同

> 100Hz：全精度相减得 `1.833400774` → `1.833`；与正文的 1.834 差在末位，源于印刷值四舍五入，非数据出入

> 4.5 节正文未以低位数复述本表单点深度线数值，故不设正文数值比对；正文的 `tens of decibels` 已由『去先验后 26-41 dB』的列值印证。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文 1.356 dB @75Hz 由表中印刷值复现（正文口径） | `2.903 − 1.547 = 1.356` | PASS |
| 正文 1.834 dB @100Hz 由表中印刷值复现（正文口径） | `5.008 − 3.174 = 1.834` | PASS |
| 深度线深度 y=71.9 m 在文中声明且与脚本 force_y 一致 | tex 行 946 | PASS |
| 深度线深度 y=33.4 m 在文中声明且与脚本 force_y 一致 | tex 行 946 | PASS |
| 正文『raises the depth-line TL to tens of decibels』成立 | w/o prior 最小 `8.733` dB（全部频率、两几何） | PASS |

## 14. 消融方向性（去掉模块应变差）

> 物理先验是主导项：去掉后误差应显著变差。楔形块 Full 四频全胜，矩形块 50-100 Hz Full 领先、25 Hz 由 w/o prior supervision 略胜——两处方向都必须由表内值直接印证，不套用结论。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| rect 25Hz 去掉物理先验后误差 >5× Full | w/o prior `26.344` vs Full `1.092` (24.1×) | PASS |
| rect 50Hz 去掉物理先验后误差 >5× Full | w/o prior `30.274` vs Full `0.533` (56.8×) | PASS |
| rect 75Hz 去掉物理先验后误差 >5× Full | w/o prior `34.122` vs Full `1.547` (22.1×) | PASS |
| rect 100Hz 去掉物理先验后误差 >5× Full | w/o prior `35.063` vs Full `3.174` (11.0×) | PASS |
| wedge 25Hz 去掉物理先验后误差 >5× Full | w/o prior `8.733` vs Full `0.545` (16.0×) | PASS |
| wedge 50Hz 去掉物理先验后误差 >5× Full | w/o prior `32.909` vs Full `0.205` (160.4×) | PASS |
| wedge 75Hz 去掉物理先验后误差 >5× Full | w/o prior `40.582` vs Full `1.417` (28.6×) | PASS |
| wedge 100Hz 去掉物理先验后误差 >5× Full | w/o prior `34.329` vs Full `4.094` (8.4×) | PASS |
| 楔形块 Full 在 4 个频率中全部占优 | 占优频率数 4 | PASS |
| 矩形块 Full 在 4 个频率中占优 3 个（25 Hz 除外） | 占优频率数 3 | PASS |
| 正文『the full model leading from 50 to 100 Hz』与矩形块 3/4 一致 | 25 Hz 另由 w/o prior supervision 略胜 | PASS |

