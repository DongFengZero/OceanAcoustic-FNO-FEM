# Table 12 — 消融深度线 TL @W1 y=33.4m

- 对象：`tab:dl-abl-wedge`（Table 12）
- 结论：**PASS** — 85 通过 / 0 失败 / 0 警告，共 85 项
- 脚本：`ch4_validation/scripts/T12_dl_abl_wedge.py`
- 生成：2026-07-28 21:38:48

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:dl-abl-wedge}` 所在 minipage |
| 成图/取数脚本（权威） | `advantage_depth_line.py` | 组 `ablation_W1_module_advantage` |
| 同一脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/advantage_depth_line.py` | md5 应与权威副本相同 |
| 脚本导出 MAE 表 | `重绘结果/advantage_depthline_MAE_bigfont/_mae_tables.json` | round 到 3 位，供正文取用 |
| 论文图件 | `../JASA/OE/els-cas-templates/Figures/results/ablation_W1_module_advantage.pdf` | Fig.~\ref{fig:dl-abl-wedge}，应与脚本产物逐字节相同 |

## 2. 源可追溯性与脚本同源

> 脚本用 `ROOT = dirname(__file__)` 定位数据与产物，只有位于 `D:\Data` 下才能同时命中 `ROOT/Case25-32` 与 `ROOT/重绘结果`；repo 内 `Validation_Scripts/` 那份是副本，md5 相同但路径不通。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 权威脚本存在 | advantage_depth_line.py | PASS |
| repo 副本与权威副本 md5 相同 | `0eb5636754e20cf348fc581ecfac0216` | PASS |
| MAE json 存在 | 重绘结果/advantage_depthline_MAE_bigfont/_mae_tables.json | PASS |
| Case29_W1_Full 的 ep200 npz 存在 | Case25-32/Case29_W1_Full/Case29_W1_Full__TL原始数据_ep200.npz | PASS |
| Case30_W1_no_prior 的 ep200 npz 存在 | Case25-32/Case30_W1_no_prior/Case30_W1_no_prior__TL原始数据_ep200.npz | PASS |
| Case31_W1_no_graph 的 ep200 npz 存在 | Case25-32/Case31_W1_no_graph/Case31_W1_no_graph__TL原始数据_ep200.npz | PASS |
| Case32_W1_no_prior_loss 的 ep200 npz 存在 | Case25-32/Case32_W1_no_prior_loss/Case32_W1_no_prior_loss__TL原始数据_ep200.npz | PASS |

## 3. 提取口径防漂移

> 口径直接从脚本对象读出再断言，脚本改了这里立刻失败，不会出现『核验脚本按旧口径算、论文按新口径印』的错位。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 插值网格 GRID = 300 | 脚本内 `300` | PASS |
| 插值方式 METHOD = 'cubic' | 脚本内 `'cubic'` | PASS |
| 频率集 FREQS = (25, 50, 75, 100) | 脚本内 `(25, 50, 75, 100)` | PASS |
| 指定深度线 force_y = 33.4 | 脚本内 `33.4` | PASS |
| 数据目录 grpdir = 'Case25-32' | 脚本内 `'Case25-32'` | PASS |
| 域类型 = 'Wedge' | 脚本内 `'Wedge'` | PASS |
| 脚本方法顺序与 tex 行序一致 | Full (Ours) / w/o prior / w/o graph / w/o prior-sup. | PASS |

## 4. 全精度重算（复用脚本自身函数）

> 重算落在第 78 行，实际深度 y=33.391304 m；force_y=33.4 取最近行，caption 写 33.4 m 是其一位小数。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 选中行深度舍入到 1 位 = 33.4 m | 实际 `33.391304` | PASS |
| caption 深度值与重算一致 | caption 含 `y=33.4\,m` | PASS |
| caption 声明 last epoch | 深度线由 ep200 npz 现场提取，非 best epoch 汇总 | PASS |

## 5. json 与全精度重算一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| json y_line 与重算一致 | json `33.39` / 重算 `33.39` | PASS |
| 25Hz Full (Ours) json vs 重算 | json `0.545` / 重算 `0.545448316` | PASS |
| 25Hz w/o prior json vs 重算 | json `8.733` / 重算 `8.732524553` | PASS |
| 25Hz w/o graph json vs 重算 | json `1.44` / 重算 `1.439754998` | PASS |
| 25Hz w/o prior-sup. json vs 重算 | json `1.008` / 重算 `1.007677660` | PASS |
| 50Hz Full (Ours) json vs 重算 | json `0.205` / 重算 `0.205193785` | PASS |
| 50Hz w/o prior json vs 重算 | json `32.909` / 重算 `32.908629110` | PASS |
| 50Hz w/o graph json vs 重算 | json `0.306` / 重算 `0.306454512` | PASS |
| 50Hz w/o prior-sup. json vs 重算 | json `0.425` / 重算 `0.425215799` | PASS |
| 75Hz Full (Ours) json vs 重算 | json `1.417` / 重算 `1.417487228` | PASS |
| 75Hz w/o prior json vs 重算 | json `40.582` / 重算 `40.581971256` | PASS |
| 75Hz w/o graph json vs 重算 | json `2.289` / 重算 `2.289158269` | PASS |
| 75Hz w/o prior-sup. json vs 重算 | json `2.21` / 重算 `2.210329951` | PASS |
| 100Hz Full (Ours) json vs 重算 | json `4.094` / 重算 `4.093890783` | PASS |
| 100Hz w/o prior json vs 重算 | json `34.329` / 重算 `34.329034211` | PASS |
| 100Hz w/o graph json vs 重算 | json `4.623` / 重算 `4.623336897` | PASS |
| 100Hz w/o prior-sup. json vs 重算 | json `4.219` / 重算 `4.218932819` | PASS |

## 6. 印刷值比对（全精度舍入到 3 位 vs tex）

> 判定用全精度值，不用 json —— json 已是 round(...,3)，拿它比对等于自证，无法识别补 0（如 w/o graph@25Hz 印 `1.440`，全精度须确认第 3 位真是 0）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 表格环境可定位 | 长度 1382 | PASS |
| tex 数据行数 = 4 | 实得 4 | PASS |
| 行 No. 覆盖 Case 29-32 | [29, 30, 31, 32] | PASS |
| Case 29 Method 名 | tex `Full model` | PASS |
| Case 29 25Hz | 源 0.5454483164813005 → `0.545` / 印刷 `0.545` | PASS |
| Case 29 50Hz | 源 0.205193784828277 → `0.205` / 印刷 `0.205` | PASS |
| Case 29 75Hz | 源 1.417487228217092 → `1.417` / 印刷 `1.417` | PASS |
| Case 29 100Hz | 源 4.093890782681291 → `4.094` / 印刷 `4.094` | PASS |
| Case 30 Method 名 | tex `w/o physics prior` | PASS |
| Case 30 25Hz | 源 8.732524553217452 → `8.733` / 印刷 `8.733` | PASS |
| Case 30 50Hz | 源 32.90862910998996 → `32.909` / 印刷 `32.909` | PASS |
| Case 30 75Hz | 源 40.58197125552458 → `40.582` / 印刷 `40.582` | PASS |
| Case 30 100Hz | 源 34.32903421065514 → `34.329` / 印刷 `34.329` | PASS |
| Case 31 Method 名 | tex `w/o graph correction` | PASS |
| Case 31 25Hz | 源 1.439754998410447 → `1.440` / 印刷 `1.440` | PASS |
| Case 31 50Hz | 源 0.3064545123013916 → `0.306` / 印刷 `0.306` | PASS |
| Case 31 75Hz | 源 2.2891582692879773 → `2.289` / 印刷 `2.289` | PASS |
| Case 31 100Hz | 源 4.623336897004174 → `4.623` / 印刷 `4.623` | PASS |
| Case 32 Method 名 | tex `w/o prior supervision` | PASS |
| Case 32 25Hz | 源 1.0076776599015047 → `1.008` / 印刷 `1.008` | PASS |
| Case 32 50Hz | 源 0.4252157986505235 → `0.425` / 印刷 `0.425` | PASS |
| Case 32 75Hz | 源 2.2103299510185797 → `2.210` / 印刷 `2.210` | PASS |
| Case 32 100Hz | 源 4.218932818512776 → `4.219` / 印刷 `4.219` | PASS |

## 7. 末位为 0 的单元格：真值还是补 0

> 凡印刷值末位为 0 的格，单看数字无法排除『2 位补 1 个 0』，逐个回溯全精度源值确认第 3 位确实是 0 或由进位得到。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 31 25Hz 末位 0 可由全精度复现 | 全精度 1.439754998 → `1.440` | PASS |
| Case 32 75Hz 末位 0 可由全精度复现 | 全精度 2.210329951 → `2.210` | PASS |

## 8. 表头源坐标与所选样本一致

> 表头每频率标 $(x,y)$，须等于该频率**实际选中样本**的 source_pos；选线算法逐频独立挑样本，四个坐标互不相同，写错不会报编译错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 表头解析到 4 组源坐标 | [(92.7, 58.9), (117.6, 43.4), (56.7, 33.8), (45.5, 29.5)] | PASS |
| 25Hz 源坐标 | tex `(92.7, 58.9)` / 样本 0 实际 (92.73300, 58.85380) → `(92.7, 58.9)` | PASS |
| 50Hz 源坐标 | tex `(117.6, 43.4)` / 样本 2 实际 (117.61148, 43.44483) → `(117.6, 43.4)` | PASS |
| 75Hz 源坐标 | tex `(56.7, 33.8)` / 样本 4 实际 (56.67198, 33.82414) → `(56.7, 33.8)` | PASS |
| 100Hz 源坐标 | tex `(45.5, 29.5)` / 样本 7 实际 (45.49694, 29.46439) → `(45.5, 29.5)` | PASS |

## 9. 表与图同源（Table 12 ↔ Fig. 13）

> MAE 表和深度线图是同一次 build_group 的两个产物。比对论文图件与脚本输出目录下同名 PDF 的 md5：相同则『表里的数』与『图里的线』必定来自同一次计算，不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 脚本产出 PDF 存在 | 重绘结果/advantage_depthline_MAE_bigfont/ablation_W1_module_advantage.pdf | PASS |
| 论文图件存在 | ../JASA/OE/els-cas-templates/Figures/results/ablation_W1_module_advantage.pdf | PASS |
| 两者逐字节相同 | md5 `6844ad600441185aa6e538503bfbd352` | PASS |
| `fig:dl-abl-wedge` 已在 aux 注册 | 编号 `13` | PASS |
| 图注深度与表一致 | 图注含 `y=33.4\,m` | PASS |
| 图注声明 last epoch |  | PASS |

## 10. 加粗正确性（Best in bold）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25Hz 加粗落在最小值行 | 加粗 [29] / 最小值 Case 29 (`0.545`) | PASS |
| 50Hz 加粗落在最小值行 | 加粗 [29] / 最小值 Case 29 (`0.205`) | PASS |
| 75Hz 加粗落在最小值行 | 加粗 [29] / 最小值 Case 29 (`1.417`) | PASS |
| 100Hz 加粗落在最小值行 | 加粗 [29] / 最小值 Case 29 (`4.094`) | PASS |

## 11. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 16 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 12. 与 Table 11 的版式一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 列定义与 Table 11 相同 | Table 12 `@{}QA EEEE@{}` / Table 11 `@{}QA EEEE@{}` | PASS |
| 列定义为消融深度线族专用 `@{}QA EEEE@{}` | `@{}QA EEEE@{}` | PASS |
| 两表同用 \TABstyle |  | PASS |

## 13. 正文引用精确性（4.5 节）

> 4.5 节正文以 Tables 15/16 的全测试集误差为论述依据，未直接引用本表的单点深度线数值；故本节只核验『表内值未被正文以低位数复述』。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文未以 2 位小数复述本表数值 | 无低位数复述 | PASS |
| 深度线深度 y=33.4 m 在 caption 中声明且与脚本 force_y 一致 | tex 行 942 | PASS |

## 14. 消融结论方向性（去掉模块应变差）

> 与 Table 11（R1）不同，本表 Full model 四个频率全部最小，故加粗全部落在 Case 29 行；此处断言物理先验是主导项，且 Full 的逐频占优是真实的。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25Hz 去掉物理先验后误差 >5× Full | w/o prior `8.733` vs Full `0.545` (16.0×) | PASS |
| 50Hz 去掉物理先验后误差 >5× Full | w/o prior `32.909` vs Full `0.205` (160.4×) | PASS |
| 75Hz 去掉物理先验后误差 >5× Full | w/o prior `40.582` vs Full `1.417` (28.6×) | PASS |
| 100Hz 去掉物理先验后误差 >5× Full | w/o prior `34.329` vs Full `4.094` (8.4×) | PASS |
| Full 在 4 个频率中全部占优（与 R1 表不同） | 占优频率数 4 | PASS |

