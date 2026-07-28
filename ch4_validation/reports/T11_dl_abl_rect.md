# Table 11 — 消融深度线 TL @R1 y=71.9m

- 对象：`tab:dl-abl-rect`（Table 11）
- 结论：**PASS** — 85 通过 / 0 失败 / 0 警告，共 85 项
- 脚本：`ch4_validation/scripts/T11_dl_abl_rect.py`
- 生成：2026-07-29 00:55:27

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:dl-abl-rect}` 所在 minipage |
| 成图/取数脚本（权威） | `advantage_depth_line.py` | 组 `ablation_R1_module_advantage` |
| 同一脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/advantage_depth_line.py` | md5 应与权威副本相同 |
| 脚本导出 MAE 表 | `重绘结果/advantage_depthline_MAE_bigfont/_mae_tables.json` | round 到 3 位，供正文取用 |
| 论文图件 | `../JASA/OE/els-cas-templates/Figures/results/ablation_R1_module_advantage.pdf` | Fig.~\ref{fig:dl-abl-rect}，应与脚本产物逐字节相同 |

## 2. 源可追溯性与脚本同源

> 脚本用 `ROOT = dirname(__file__)` 定位数据与产物，只有位于 `D:\Data` 下才能同时命中 `ROOT/Case25-32` 与 `ROOT/重绘结果`；repo 内 `Validation_Scripts/` 那份是副本，md5 相同但路径不通。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 权威脚本存在 | advantage_depth_line.py | PASS |
| repo 副本与权威副本 md5 相同 | `0eb5636754e20cf348fc581ecfac0216` | PASS |
| MAE json 存在 | 重绘结果/advantage_depthline_MAE_bigfont/_mae_tables.json | PASS |
| Case25_R1_Full 的 ep200 npz 存在 | Case25-32/Case25_R1_Full/Case25_R1_Full__TL原始数据_ep200.npz | PASS |
| Case26_R1_no_prior 的 ep200 npz 存在 | Case25-32/Case26_R1_no_prior/Case26_R1_no_prior__TL原始数据_ep200.npz | PASS |
| Case27_R1_no_graph 的 ep200 npz 存在 | Case25-32/Case27_R1_no_graph/Case27_R1_no_graph__TL原始数据_ep200.npz | PASS |
| Case28_R1_no_prior_loss 的 ep200 npz 存在 | Case25-32/Case28_R1_no_prior_loss/Case28_R1_no_prior_loss__TL原始数据_ep200.npz | PASS |

## 3. 提取口径防漂移

> 口径直接从脚本对象读出再断言，脚本改了这里立刻失败，不会出现『核验脚本按旧口径算、论文按新口径印』的错位。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 插值网格 GRID = 300 | 脚本内 `300` | PASS |
| 插值方式 METHOD = 'cubic' | 脚本内 `'cubic'` | PASS |
| 频率集 FREQS = (25, 50, 75, 100) | 脚本内 `(25, 50, 75, 100)` | PASS |
| 指定深度线 force_y = 71.9 | 脚本内 `71.9` | PASS |
| 数据目录 grpdir = 'Case25-32' | 脚本内 `'Case25-32'` | PASS |
| 域类型 = 'Rectangle' | 脚本内 `'Rectangle'` | PASS |
| 脚本方法顺序与 tex 行序一致 | Full (Ours) / w/o prior / w/o graph / w/o prior-sup. | PASS |

## 4. 全精度重算（复用脚本自身函数）

> 重算落在第 168 行，实际深度 y=71.919732 m；force_y=71.9 取最近行，caption 写 71.9 m 是其一位小数。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 选中行深度舍入到 1 位 = 71.9 m | 实际 `71.919732` | PASS |
| caption 深度值与重算一致 | caption 含 `y=71.9\,m` | PASS |
| caption 声明 last epoch | 深度线由 ep200 npz 现场提取，非 best epoch 汇总 | PASS |

## 5. json 与全精度重算一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| json y_line 与重算一致 | json `71.92` / 重算 `71.92` | PASS |
| 25Hz Full (Ours) json vs 重算 | json `1.092` / 重算 `1.092168347` | PASS |
| 25Hz w/o prior json vs 重算 | json `26.344` / 重算 `26.343610194` | PASS |
| 25Hz w/o graph json vs 重算 | json `0.968` / 重算 `0.968006704` | PASS |
| 25Hz w/o prior-sup. json vs 重算 | json `0.54` / 重算 `0.540375313` | PASS |
| 50Hz Full (Ours) json vs 重算 | json `0.533` / 重算 `0.532955990` | PASS |
| 50Hz w/o prior json vs 重算 | json `30.274` / 重算 `30.274313204` | PASS |
| 50Hz w/o graph json vs 重算 | json `0.547` / 重算 `0.546991315` | PASS |
| 50Hz w/o prior-sup. json vs 重算 | json `0.649` / 重算 `0.649440036` | PASS |
| 75Hz Full (Ours) json vs 重算 | json `1.547` / 重算 `1.547306137` | PASS |
| 75Hz w/o prior json vs 重算 | json `34.122` / 重算 `34.121951553` | PASS |
| 75Hz w/o graph json vs 重算 | json `2.903` / 重算 `2.903096185` | PASS |
| 75Hz w/o prior-sup. json vs 重算 | json `3.003` / 重算 `3.002957203` | PASS |
| 100Hz Full (Ours) json vs 重算 | json `3.174` / 重算 `3.174377784` | PASS |
| 100Hz w/o prior json vs 重算 | json `35.063` / 重算 `35.062962102` | PASS |
| 100Hz w/o graph json vs 重算 | json `5.008` / 重算 `5.007778557` | PASS |
| 100Hz w/o prior-sup. json vs 重算 | json `5.244` / 重算 `5.244146412` | PASS |

## 6. 印刷值比对（全精度舍入到 3 位 vs tex）

> 判定用全精度值，不用 json —— json 已是 round(...,3)，拿它比对等于自证，无法识别补 0（如 w/o prior-sup.@25Hz 印 `0.540`，全精度 0.540375313 才是真值来源）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 表格环境可定位 | 长度 1419 | PASS |
| tex 数据行数 = 4 | 实得 4 | PASS |
| 行 No. 覆盖 Case 25-28 | [25, 26, 27, 28] | PASS |
| Case 25 Method 名 | tex `Full model` | PASS |
| Case 25 25Hz | 源 1.092168346691922 → `1.092` / 印刷 `1.092` | PASS |
| Case 25 50Hz | 源 0.5329559900137699 → `0.533` / 印刷 `0.533` | PASS |
| Case 25 75Hz | 源 1.5473061373714823 → `1.547` / 印刷 `1.547` | PASS |
| Case 25 100Hz | 源 3.1743777836681213 → `3.174` / 印刷 `3.174` | PASS |
| Case 26 Method 名 | tex `w/o physics prior` | PASS |
| Case 26 25Hz | 源 26.343610194470056 → `26.344` / 印刷 `26.344` | PASS |
| Case 26 50Hz | 源 30.27431320444456 → `30.274` / 印刷 `30.274` | PASS |
| Case 26 75Hz | 源 34.121951553211204 → `34.122` / 印刷 `34.122` | PASS |
| Case 26 100Hz | 源 35.06296210235836 → `35.063` / 印刷 `35.063` | PASS |
| Case 27 Method 名 | tex `w/o graph correction` | PASS |
| Case 27 25Hz | 源 0.9680067037698834 → `0.968` / 印刷 `0.968` | PASS |
| Case 27 50Hz | 源 0.5469913147202249 → `0.547` / 印刷 `0.547` | PASS |
| Case 27 75Hz | 源 2.9030961846184775 → `2.903` / 印刷 `2.903` | PASS |
| Case 27 100Hz | 源 5.007778557240541 → `5.008` / 印刷 `5.008` | PASS |
| Case 28 Method 名 | tex `w/o prior supervision` | PASS |
| Case 28 25Hz | 源 0.5403753127041657 → `0.540` / 印刷 `0.540` | PASS |
| Case 28 50Hz | 源 0.6494400364717936 → `0.649` / 印刷 `0.649` | PASS |
| Case 28 75Hz | 源 3.0029572026769444 → `3.003` / 印刷 `3.003` | PASS |
| Case 28 100Hz | 源 5.244146412380103 → `5.244` / 印刷 `5.244` | PASS |

## 7. 末位为 0 的单元格：真值还是补 0

> 凡印刷值末位为 0 的格，单看数字无法排除『2 位补 1 个 0』，逐个回溯全精度源值确认第 3 位确实是 0 或由进位得到。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 28 25Hz 末位 0 可由全精度复现 | 全精度 0.540375313 → `0.540` | PASS |

## 8. 表头源坐标与所选样本一致

> 表头每频率标 $(x,y)$，须等于该频率**实际选中样本**的 source_pos；选线算法逐频独立挑样本，四个坐标互不相同，写错不会报编译错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 表头解析到 4 组源坐标 | [(44.5, 21.9), (25.9, 49.5), (51.5, 5.7), (62.8, 85.3)] | PASS |
| 25Hz 源坐标 | tex `(44.5, 21.9)` / 样本 0 实际 (44.50021, 21.86243) → `(44.5, 21.9)` | PASS |
| 50Hz 源坐标 | tex `(25.9, 49.5)` / 样本 2 实际 (25.88422, 49.48544) → `(25.9, 49.5)` | PASS |
| 75Hz 源坐标 | tex `(51.5, 5.7)` / 样本 5 实际 (51.50000, 5.66814) → `(51.5, 5.7)` | PASS |
| 100Hz 源坐标 | tex `(62.8, 85.3)` / 样本 6 实际 (62.75945, 85.33403) → `(62.8, 85.3)` | PASS |

## 9. 表与图同源（Table 11 ↔ Fig. 12）

> MAE 表和深度线图是同一次 build_group 的两个产物。比对论文图件与脚本输出目录下同名 PDF 的 md5：相同则『表里的数』与『图里的线』必定来自同一次计算，不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 脚本产出 PDF 存在 | 重绘结果/advantage_depthline_MAE_bigfont/ablation_R1_module_advantage.pdf | PASS |
| 论文图件存在 | ../JASA/OE/els-cas-templates/Figures/results/ablation_R1_module_advantage.pdf | PASS |
| 两者逐字节相同 | md5 `9d0df8af47d1b1bb78566520bdb02f1f` | PASS |
| `fig:dl-abl-rect` 已在 aux 注册 | 编号 `12` | PASS |
| 图注深度与表一致 | 图注含 `y=71.9\,m` | PASS |
| 图注声明 last epoch |  | PASS |

## 10. 加粗正确性（Best in bold）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25Hz 加粗落在最小值行 | 加粗 [28] / 最小值 Case 28 (`0.540`) | PASS |
| 50Hz 加粗落在最小值行 | 加粗 [25] / 最小值 Case 25 (`0.533`) | PASS |
| 75Hz 加粗落在最小值行 | 加粗 [25] / 最小值 Case 25 (`1.547`) | PASS |
| 100Hz 加粗落在最小值行 | 加粗 [25] / 最小值 Case 25 (`3.174`) | PASS |

## 11. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 16 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 12. 与 Table 12 的版式一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 列定义与 Table 12 相同 | Table 11 `@{\extracolsep{\fill}}QA EEEE@{}` / Table 12 `@{\extracolsep{\fill}}QA EEEE@{}` | PASS |
| 列类型序列为消融深度线族专用 `QA EEEE` | `@{\extracolsep{\fill}}QA EEEE@{}` | PASS |
| 用 \extracolsep{\fill} 均分列间余量（tabular* 等宽所需） | `@{\extracolsep{\fill}}QA EEEE@{}` | PASS |
| 两表同用 \TABstyleDL（整表 \scriptsize + 紧凑列距） |  | PASS |

## 13. 正文引用精确性（4.5 节）

> 4.5 节正文以 Tables 15/16 的全测试集误差为论述依据，未直接引用本表的单点深度线数值；故本节只核验『表内值未被正文以低位数复述』。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文未以 2 位小数复述本表数值 | 无低位数复述 | PASS |
| 深度线深度 y=71.9 m 在 caption 中声明且与脚本 force_y 一致 | tex 行 955 | PASS |

## 14. 消融结论方向性（去掉模块应变差）

> 消融表不要求 Full 逐频最优：25 Hz 最小值落在 w/o prior-sup.（0.540），这是真实结果，加粗已按列最小值标注。此处只断言物理先验是主导项。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25Hz 去掉物理先验后误差 >5× Full | w/o prior `26.344` vs Full `1.092` (24.1×) | PASS |
| 50Hz 去掉物理先验后误差 >5× Full | w/o prior `30.274` vs Full `0.533` (56.8×) | PASS |
| 75Hz 去掉物理先验后误差 >5× Full | w/o prior `34.122` vs Full `1.547` (22.1×) | PASS |
| 100Hz 去掉物理先验后误差 >5× Full | w/o prior `35.063` vs Full `3.174` (11.0×) | PASS |
| Full 在 4 个频率中占优 3 个（25 Hz 除外） | 占优频率数 3 | PASS |

