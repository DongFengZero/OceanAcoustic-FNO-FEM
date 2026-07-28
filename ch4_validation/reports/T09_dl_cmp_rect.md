# Table 9 — 五方法深度线 TL @R1 y=56.1m

- 对象：`tab:dl-cmp-rect`（Table 9）
- 结论：**PASS** — 97 通过 / 0 失败 / 0 警告 / 1 豁免，共 98 项
- 脚本：`ch4_validation/scripts/T09_dl_cmp_rect.py`
- 生成：2026-07-28 21:38:26

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:dl-cmp-rect}` 所在 minipage |
| 成图/取数脚本（权威） | `advantage_depth_line.py` | 组 `comparison_R1_model_advantage` |
| 同一脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/advantage_depth_line.py` | md5 应与权威副本相同 |
| 脚本导出 MAE 表 | `重绘结果/advantage_depthline_MAE_bigfont/_mae_tables.json` | round 到 3 位，供正文取用 |
| 论文图件 | `../JASA/OE/els-cas-templates/Figures/results/comparison_R1_model_advantage.pdf` | Fig.~\ref{fig:dl-cmp-rect}，应与脚本产物逐字节相同 |

## 2. 源可追溯性与脚本同源

> 脚本用 `ROOT = dirname(__file__)` 定位数据与产物，只有位于 `D:\Data` 下才能同时命中 `ROOT/Case15-24` 与 `ROOT/重绘结果`；repo 内 `Validation_Scripts/` 那份是副本，md5 相同但路径不通。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 权威脚本存在 | advantage_depth_line.py | PASS |
| repo 副本与权威副本 md5 相同 | `0eb5636754e20cf348fc581ecfac0216` | PASS |
| MAE json 存在 | 重绘结果/advantage_depthline_MAE_bigfont/_mae_tables.json | PASS |
| Case15_R1_Proposed 的 ep200 npz 存在 | Case15-24/Case15_R1_Proposed/Case15_R1_Proposed__TL原始数据_ep200.npz | PASS |
| Case16_R1_DeepONet 的 ep200 npz 存在 | Case15-24/Case16_R1_DeepONet/Case16_R1_DeepONet__TL原始数据_ep200.npz | PASS |
| Case17_R1_FNO 的 ep200 npz 存在 | Case15-24/Case17_R1_FNO/Case17_R1_FNO__TL原始数据_ep200.npz | PASS |
| Case18_R1_KNO 的 ep200 npz 存在 | Case15-24/Case18_R1_KNO/Case18_R1_KNO__TL原始数据_ep200.npz | PASS |
| Case19_R1_CNO 的 ep200 npz 存在 | Case15-24/Case19_R1_CNO/Case19_R1_CNO__TL原始数据_ep200.npz | PASS |

## 3. 提取口径防漂移

> 口径直接从脚本对象读出再断言，脚本改了这里立刻失败，不会出现『核验脚本按旧口径算、论文按新口径印』的错位。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 插值网格 GRID = 300 | 脚本内 `300` | PASS |
| 插值方式 METHOD = 'cubic' | 脚本内 `'cubic'` | PASS |
| 频率集 FREQS = (25, 50, 75, 100) | 脚本内 `(25, 50, 75, 100)` | PASS |
| 指定深度线 force_y = 56.1 | 脚本内 `56.1` | PASS |
| 数据目录 grpdir = 'Case15-24' | 脚本内 `'Case15-24'` | PASS |
| 域类型 = 'Rectangle' | 脚本内 `'Rectangle'` | PASS |
| 脚本方法顺序与 tex 行序一致 | Proposed (Ours) / DeepONet / FNO / KNO / CNO | PASS |

## 4. 全精度重算（复用脚本自身函数）

> 重算落在第 131 行，实际深度 y=56.080268 m；force_y=56.1 取最近行，caption 写 56.1 m 是其一位小数。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 选中行深度舍入到 1 位 = 56.1 m | 实际 `56.080268` | PASS |
| caption 深度值与重算一致 | caption 含 `y=56.1\,m` | PASS |
| caption 声明 last epoch | 深度线由 ep200 npz 现场提取，非 best epoch 汇总 | PASS |

## 5. json 与全精度重算一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| json y_line 与重算一致 | json `56.08` / 重算 `56.08` | PASS |
| 25Hz Proposed (Ours) json vs 重算 | json `0.469` / 重算 `0.469175680` | PASS |
| 25Hz DeepONet json vs 重算 | json `0.736` / 重算 `0.735865304` | PASS |
| 25Hz FNO json vs 重算 | json `0.582` / 重算 `0.581546268` | PASS |
| 25Hz KNO json vs 重算 | json `1.21` / 重算 `1.210452336` | PASS |
| 25Hz CNO json vs 重算 | json `1.697` / 重算 `1.697342557` | PASS |
| 50Hz Proposed (Ours) json vs 重算 | json `0.696` / 重算 `0.695958881` | PASS |
| 50Hz DeepONet json vs 重算 | json `3.57` / 重算 `3.570382602` | PASS |
| 50Hz FNO json vs 重算 | json `0.873` / 重算 `0.873428028` | PASS |
| 50Hz KNO json vs 重算 | json `2.477` / 重算 `2.477373820` | PASS |
| 50Hz CNO json vs 重算 | json `1.737` / 重算 `1.736770202` | PASS |
| 75Hz Proposed (Ours) json vs 重算 | json `0.579` / 重算 `0.579045624` | PASS |
| 75Hz DeepONet json vs 重算 | json `2.243` / 重算 `2.242879460` | PASS |
| 75Hz FNO json vs 重算 | json `0.916` / 重算 `0.916294399` | PASS |
| 75Hz KNO json vs 重算 | json `2.456` / 重算 `2.455826182` | PASS |
| 75Hz CNO json vs 重算 | json `1.84` / 重算 `1.840114785` | PASS |
| 100Hz Proposed (Ours) json vs 重算 | json `1.515` / 重算 `1.514983695` | PASS |
| 100Hz DeepONet json vs 重算 | json `5.479` / 重算 `5.478562120` | PASS |
| 100Hz FNO json vs 重算 | json `2.143` / 重算 `2.142983701` | PASS |
| 100Hz KNO json vs 重算 | json `2.965` / 重算 `2.964714688` | PASS |
| 100Hz CNO json vs 重算 | json `4.033` / 重算 `4.032862282` | PASS |

## 6. 印刷值比对（全精度舍入到 3 位 vs tex）

> 判定用全精度值，不用 json —— json 已是 round(...,3)，拿它比对等于自证，无法识别补 0（如 KNO@25Hz 印 `1.210`，全精度 1.210452336 才是真值来源）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 表格环境可定位 | 长度 1358 | PASS |
| tex 数据行数 = 5 | 实得 5 | PASS |
| 行 No. 覆盖 Case 15-19 | [15, 16, 17, 18, 19] | PASS |
| Case 15 Method 名 | tex `Proposed` | PASS |
| Case 15 25Hz | 源 0.46917567989763087 → `0.469` / 印刷 `0.469` | PASS |
| Case 15 50Hz | 源 0.6959588808704593 → `0.696` / 印刷 `0.696` | PASS |
| Case 15 75Hz | 源 0.5790456239901534 → `0.579` / 印刷 `0.579` | PASS |
| Case 15 100Hz | 源 1.5149836953267912 → `1.515` / 印刷 `1.515` | PASS |
| Case 16 Method 名 | tex `DeepONet` | PASS |
| Case 16 25Hz | 源 0.7358653037284757 → `0.736` / 印刷 `0.736` | PASS |
| Case 16 50Hz | 源 3.570382602400896 → `3.570` / 印刷 `3.570` | PASS |
| Case 16 75Hz | 源 2.242879460338406 → `2.243` / 印刷 `2.243` | PASS |
| Case 16 100Hz | 源 5.478562120157732 → `5.479` / 印刷 `5.479` | PASS |
| Case 17 Method 名 | tex `FNO` | PASS |
| Case 17 25Hz | 源 0.5815462679933076 → `0.582` / 印刷 `0.582` | PASS |
| Case 17 50Hz | 源 0.8734280283414905 → `0.873` / 印刷 `0.873` | PASS |
| Case 17 75Hz | 源 0.916294399448016 → `0.916` / 印刷 `0.916` | PASS |
| Case 17 100Hz | 源 2.1429837005185997 → `2.143` / 印刷 `2.143` | PASS |
| Case 18 Method 名 | tex `KNO` | PASS |
| Case 18 25Hz | 源 1.2104523356989585 → `1.210` / 印刷 `1.210` | PASS |
| Case 18 50Hz | 源 2.4773738198511013 → `2.477` / 印刷 `2.477` | PASS |
| Case 18 75Hz | 源 2.455826181522053 → `2.456` / 印刷 `2.456` | PASS |
| Case 18 100Hz | 源 2.9647146883368984 → `2.965` / 印刷 `2.965` | PASS |
| Case 19 Method 名 | tex `CNO` | PASS |
| Case 19 25Hz | 源 1.6973425568136546 → `1.697` / 印刷 `1.697` | PASS |
| Case 19 50Hz | 源 1.7367702015589492 → `1.737` / 印刷 `1.737` | PASS |
| Case 19 75Hz | 源 1.8401147846834267 → `1.840` / 印刷 `1.840` | PASS |
| Case 19 100Hz | 源 4.032862281813081 → `4.033` / 印刷 `4.033` | PASS |

## 7. 末位为 0 的单元格：真值还是补 0

> 凡印刷值末位为 0 的格，单看数字无法排除『2 位补 1 个 0』，逐个回溯全精度源值确认第 3 位确实是 0 或由进位得到。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 16 50Hz 末位 0 可由全精度复现 | 全精度 3.570382602 → `3.570` | PASS |
| Case 18 25Hz 末位 0 可由全精度复现 | 全精度 1.210452336 → `1.210` | PASS |
| Case 19 75Hz 末位 0 可由全精度复现 | 全精度 1.840114785 → `1.840` | PASS |

## 8. 表头源坐标与所选样本一致

> 表头每频率标 $(x,y)$，须等于该频率**实际选中样本**的 source_pos；选线算法逐频独立挑样本，四个坐标互不相同，写错不会报编译错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 表头解析到 4 组源坐标 | [(44.5, 21.9), (25.9, 49.5), (120.7, 89.5), (77.5, 103.0)] | PASS |
| 25Hz 源坐标 | tex `(44.5, 21.9)` / 样本 0 实际 (44.50021, 21.86243) → `(44.5, 21.9)` | PASS |
| 50Hz 源坐标 | tex `(25.9, 49.5)` / 样本 2 实际 (25.88422, 49.48544) → `(25.9, 49.5)` | PASS |
| 75Hz 源坐标 | tex `(120.7, 89.5)` / 样本 4 实际 (120.71240, 89.50000) → `(120.7, 89.5)` | PASS |
| 100Hz 源坐标 | tex `(77.5, 103.0)` / 样本 7 实际 (77.49264, 102.95834) → `(77.5, 103.0)` | PASS |

## 9. 表与图同源（Table 9 ↔ Fig. 12）

> MAE 表和深度线图是同一次 build_group 的两个产物。比对论文图件与脚本输出目录下同名 PDF 的 md5：相同则『表里的数』与『图里的线』必定来自同一次计算，不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 脚本产出 PDF 存在 | 重绘结果/advantage_depthline_MAE_bigfont/comparison_R1_model_advantage.pdf | PASS |
| 论文图件存在 | ../JASA/OE/els-cas-templates/Figures/results/comparison_R1_model_advantage.pdf | PASS |
| 两者逐字节相同 | md5 `e98b21f1c17c436932acf38c3190572a` | PASS |
| `fig:dl-cmp-rect` 已在 aux 注册 | 编号 `10` | PASS |
| 图注深度与表一致 | 图注含 `y=56.1\,m` | PASS |
| 图注声明 last epoch |  | PASS |

## 10. 加粗正确性（Best in bold）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25Hz 加粗落在最小值行 | 加粗 [15] / 最小值 Case 15 (`0.469`) | PASS |
| 50Hz 加粗落在最小值行 | 加粗 [15] / 最小值 Case 15 (`0.696`) | PASS |
| 75Hz 加粗落在最小值行 | 加粗 [15] / 最小值 Case 15 (`0.579`) | PASS |
| 100Hz 加粗落在最小值行 | 加粗 [15] / 最小值 Case 15 (`1.515`) | PASS |

## 11. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 20 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 12. 与 Table 10 的版式一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 列定义与 Table 10 相同 | Table 9 `@{}QM EEEE@{}` / Table 10 `@{}QM EEEE@{}` | PASS |
| 列定义为深度线族专用 `@{}QM EEEE@{}` | `@{}QM EEEE@{}` | PASS |
| 两表同用 \TABstyle |  | PASS |

## 13. 正文引用精确性（4.4 节）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文『at or below 1.515 dB』= 本文法最大值 | 四频 ['0.469', '0.696', '0.579', '1.515'] → 最大 `1.515` | PASS |
| 正文 1.515 ← 全精度源 | 源 1.5149836953267912 → `1.515` / 印刷 `1.515` | PASS |
| 正文声明的深度线 y=56.1 m 与脚本 force_y 一致 | tex 行 873 | PASS |
| 正文『DeepONet exceeds 5 dB』成立（阈值断言，不指某格） | DeepONet 最大 `5.479` > 5 | PASS |
| 正文 `$5$\,dB` 不作字面比对 | 该数是阈值表述（exceeds 5 dB），非某单元格的印刷值 | 豁免 |

## 14. 本文法逐频占优

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25Hz Proposed 为最小 | Proposed `0.469` vs 次优 `0.582` | PASS |
| 50Hz Proposed 为最小 | Proposed `0.696` vs 次优 `0.873` | PASS |
| 75Hz Proposed 为最小 | Proposed `0.579` vs 次优 `0.916` | PASS |
| 100Hz Proposed 为最小 | Proposed `1.515` vs 次优 `2.143` | PASS |

