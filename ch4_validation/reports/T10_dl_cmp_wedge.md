# Table 10 — 五方法深度线 TL @W1 y=30.4m

- 对象：`tab:dl-cmp-wedge`（Table 10）
- 结论：**PASS** — 96 通过 / 0 失败 / 0 警告 / 1 豁免，共 97 项
- 脚本：`ch4_validation/scripts/T10_dl_cmp_wedge.py`
- 生成：2026-07-30 00:03:54

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | `\label{tab:dl-cmp-wedge}` 所在 minipage |
| 成图/取数脚本（权威） | `advantage_depth_line.py` | 组 `comparison_W1_model_advantage` |
| 同一脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/advantage_depth_line.py` | md5 应与权威副本相同 |
| 脚本导出 MAE 表 | `重绘结果/advantage_depthline_MAE_bigfont/_mae_tables.json` | round 到 3 位，供正文取用 |
| 论文图件 | `../JASA/OE/els-cas-templates/Figures/results/comparison_W1_model_advantage.pdf` | Fig.~\ref{fig:dl-cmp-wedge}，应与脚本产物逐字节相同 |

## 2. 源可追溯性与脚本同源

> 脚本用 `ROOT = dirname(__file__)` 定位数据与产物，只有位于 `D:\Data` 下才能同时命中 `ROOT/Case15-24` 与 `ROOT/重绘结果`；repo 内 `Validation_Scripts/` 那份是副本，md5 相同但路径不通。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 权威脚本存在 | advantage_depth_line.py | PASS |
| repo 副本与权威副本 md5 相同 | `0eb5636754e20cf348fc581ecfac0216` | PASS |
| MAE json 存在 | 重绘结果/advantage_depthline_MAE_bigfont/_mae_tables.json | PASS |
| Case20_W1_Proposed 的 ep200 npz 存在 | Case15-24/Case20_W1_Proposed/Case20_W1_Proposed__TL原始数据_ep200.npz | PASS |
| Case21_W1_DeepONet 的 ep200 npz 存在 | Case15-24/Case21_W1_DeepONet/Case21_W1_DeepONet__TL原始数据_ep200.npz | PASS |
| Case22_W1_FNO 的 ep200 npz 存在 | Case15-24/Case22_W1_FNO/Case22_W1_FNO__TL原始数据_ep200.npz | PASS |
| Case23_W1_KNO 的 ep200 npz 存在 | Case15-24/Case23_W1_KNO/Case23_W1_KNO__TL原始数据_ep200.npz | PASS |
| Case24_W1_CNO 的 ep200 npz 存在 | Case15-24/Case24_W1_CNO/Case24_W1_CNO__TL原始数据_ep200.npz | PASS |

## 3. 提取口径防漂移

> 口径直接从脚本对象读出再断言，脚本改了这里立刻失败，不会出现『核验脚本按旧口径算、论文按新口径印』的错位。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 插值网格 GRID = 300 | 脚本内 `300` | PASS |
| 插值方式 METHOD = 'cubic' | 脚本内 `'cubic'` | PASS |
| 频率集 FREQS = (25, 50, 75, 100) | 脚本内 `(25, 50, 75, 100)` | PASS |
| 指定深度线 force_y = 30.4 | 脚本内 `30.4` | PASS |
| 数据目录 grpdir = 'Case15-24' | 脚本内 `'Case15-24'` | PASS |
| 域类型 = 'Wedge' | 脚本内 `'Wedge'` | PASS |
| 脚本方法顺序与 tex 行序一致 | Proposed (Ours) / DeepONet / FNO / KNO / CNO | PASS |

## 4. 全精度重算（复用脚本自身函数）

> 重算落在第 71 行，实际深度 y=30.394649 m；force_y=30.4 取最近行，caption 写 30.4 m 是其一位小数。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 选中行深度舍入到 1 位 = 30.4 m | 实际 `30.394649` | PASS |
| caption 深度值与重算一致 | caption 含 `y=30.4\,m` | PASS |
| caption 声明 last epoch | 深度线由 ep200 npz 现场提取，非 best epoch 汇总 | PASS |

## 5. json 与全精度重算一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| json y_line 与重算一致 | json `30.39` / 重算 `30.39` | PASS |
| 25Hz Proposed (Ours) json vs 重算 | json `0.195` / 重算 `0.195135261` | PASS |
| 25Hz DeepONet json vs 重算 | json `0.793` / 重算 `0.793083731` | PASS |
| 25Hz FNO json vs 重算 | json `0.446` / 重算 `0.445601871` | PASS |
| 25Hz KNO json vs 重算 | json `0.832` / 重算 `0.832132345` | PASS |
| 25Hz CNO json vs 重算 | json `0.762` / 重算 `0.761761603` | PASS |
| 50Hz Proposed (Ours) json vs 重算 | json `0.144` / 重算 `0.144001160` | PASS |
| 50Hz DeepONet json vs 重算 | json `1.982` / 重算 `1.982488174` | PASS |
| 50Hz FNO json vs 重算 | json `0.417` / 重算 `0.416556085` | PASS |
| 50Hz KNO json vs 重算 | json `0.826` / 重算 `0.826277347` | PASS |
| 50Hz CNO json vs 重算 | json `1.055` / 重算 `1.054709443` | PASS |
| 75Hz Proposed (Ours) json vs 重算 | json `0.576` / 重算 `0.575567594` | PASS |
| 75Hz DeepONet json vs 重算 | json `1.468` / 重算 `1.468247207` | PASS |
| 75Hz FNO json vs 重算 | json `1.281` / 重算 `1.281330671` | PASS |
| 75Hz KNO json vs 重算 | json `2.496` / 重算 `2.496269723` | PASS |
| 75Hz CNO json vs 重算 | json `2.836` / 重算 `2.835756529` | PASS |
| 100Hz Proposed (Ours) json vs 重算 | json `0.666` / 重算 `0.665838609` | PASS |
| 100Hz DeepONet json vs 重算 | json `7.038` / 重算 `7.037914739` | PASS |
| 100Hz FNO json vs 重算 | json `1.189` / 重算 `1.189325003` | PASS |
| 100Hz KNO json vs 重算 | json `4.315` / 重算 `4.315449918` | PASS |
| 100Hz CNO json vs 重算 | json `3.16` / 重算 `3.160087640` | PASS |

## 6. 印刷值比对（全精度舍入到 3 位 vs tex）

> 判定用全精度值，不用 json —— json 已是 round(...,3)，拿它比对等于自证，无法识别补 0（如 KNO@25Hz 印 `1.210`，全精度 1.210452336 才是真值来源）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 表格环境可定位 | 长度 1405 | PASS |
| tex 数据行数 = 5 | 实得 5 | PASS |
| 行 No. 覆盖 Case 20-19 | [20, 21, 22, 23, 24] | PASS |
| Case 20 Method 名 | tex `Proposed` | PASS |
| Case 20 25Hz | 源 0.19513526059996544 → `0.195` / 印刷 `0.195` | PASS |
| Case 20 50Hz | 源 0.14400115992252566 → `0.144` / 印刷 `0.144` | PASS |
| Case 20 75Hz | 源 0.5755675939157606 → `0.576` / 印刷 `0.576` | PASS |
| Case 20 100Hz | 源 0.6658386092081794 → `0.666` / 印刷 `0.666` | PASS |
| Case 21 Method 名 | tex `DeepONet` | PASS |
| Case 21 25Hz | 源 0.7930837308184404 → `0.793` / 印刷 `0.793` | PASS |
| Case 21 50Hz | 源 1.9824881738837865 → `1.982` / 印刷 `1.982` | PASS |
| Case 21 75Hz | 源 1.468247206544106 → `1.468` / 印刷 `1.468` | PASS |
| Case 21 100Hz | 源 7.037914739452272 → `7.038` / 印刷 `7.038` | PASS |
| Case 22 Method 名 | tex `FNO` | PASS |
| Case 22 25Hz | 源 0.4456018707193328 → `0.446` / 印刷 `0.446` | PASS |
| Case 22 50Hz | 源 0.4165560846200631 → `0.417` / 印刷 `0.417` | PASS |
| Case 22 75Hz | 源 1.2813306714744437 → `1.281` / 印刷 `1.281` | PASS |
| Case 22 100Hz | 源 1.1893250031379634 → `1.189` / 印刷 `1.189` | PASS |
| Case 23 Method 名 | tex `KNO` | PASS |
| Case 23 25Hz | 源 0.8321323449956286 → `0.832` / 印刷 `0.832` | PASS |
| Case 23 50Hz | 源 0.8262773465953761 → `0.826` / 印刷 `0.826` | PASS |
| Case 23 75Hz | 源 2.4962697229327806 → `2.496` / 印刷 `2.496` | PASS |
| Case 23 100Hz | 源 4.3154499175979115 → `4.315` / 印刷 `4.315` | PASS |
| Case 24 Method 名 | tex `CNO` | PASS |
| Case 24 25Hz | 源 0.7617616030071812 → `0.762` / 印刷 `0.762` | PASS |
| Case 24 50Hz | 源 1.0547094429258645 → `1.055` / 印刷 `1.055` | PASS |
| Case 24 75Hz | 源 2.835756529075116 → `2.836` / 印刷 `2.836` | PASS |
| Case 24 100Hz | 源 3.1600876402200573 → `3.160` / 印刷 `3.160` | PASS |

## 7. 末位为 0 的单元格：真值还是补 0

> 凡印刷值末位为 0 的格，单看数字无法排除『2 位补 1 个 0』，逐个回溯全精度源值确认第 3 位确实是 0 或由进位得到。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 24 100Hz 末位 0 可由全精度复现 | 全精度 3.160087640 → `3.160` | PASS |

## 8. 表头源坐标与所选样本一致

> 表头每频率标 $(x,y)$，须等于该频率**实际选中样本**的 source_pos；选线算法逐频独立挑样本，四个坐标互不相同，写错不会报编译错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 表头解析到 4 组源坐标 | [(80.7, 72.7), (117.6, 43.4), (113.4, 64.0), (88.0, 78.9)] | PASS |
| 25Hz 源坐标 | tex `(80.7, 72.7)` / 样本 1 实际 (80.73742, 72.72114) → `(80.7, 72.7)` | PASS |
| 50Hz 源坐标 | tex `(117.6, 43.4)` / 样本 2 实际 (117.61148, 43.44483) → `(117.6, 43.4)` | PASS |
| 75Hz 源坐标 | tex `(113.4, 64.0)` / 样本 5 实际 (113.42506, 63.99967) → `(113.4, 64.0)` | PASS |
| 100Hz 源坐标 | tex `(88.0, 78.9)` / 样本 6 实际 (88.02824, 78.86678) → `(88.0, 78.9)` | PASS |

## 9. 表与图同源（Table 9 ↔ Fig. 12）

> MAE 表和深度线图是同一次 build_group 的两个产物。比对论文图件与脚本输出目录下同名 PDF 的 md5：相同则『表里的数』与『图里的线』必定来自同一次计算，不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 脚本产出 PDF 存在 | 重绘结果/advantage_depthline_MAE_bigfont/comparison_W1_model_advantage.pdf | PASS |
| 论文图件存在 | ../JASA/OE/els-cas-templates/Figures/results/comparison_W1_model_advantage.pdf | PASS |
| 两者逐字节相同 | md5 `67fba98d9555cec3d95add51dc87105a` | PASS |
| `fig:dl-cmp-wedge` 已在 aux 注册 | 编号 `11` | PASS |
| 图注深度与表一致 | 图注含 `y=30.4\,m` | PASS |
| 图注声明 last epoch |  | PASS |

## 10. 加粗正确性（Best in bold）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25Hz 加粗落在最小值行 | 加粗 [20] / 最小值 Case 20 (`0.195`) | PASS |
| 50Hz 加粗落在最小值行 | 加粗 [20] / 最小值 Case 20 (`0.144`) | PASS |
| 75Hz 加粗落在最小值行 | 加粗 [20] / 最小值 Case 20 (`0.576`) | PASS |
| 100Hz 加粗落在最小值行 | 加粗 [20] / 最小值 Case 20 (`0.666`) | PASS |

## 11. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 20 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 12. 与 Table 10 的版式一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 列定义与 Table 10 相同 | Table 9 `@{\extracolsep{\fill}}QM EEEE@{}` / Table 10 `@{\extracolsep{\fill}}QM EEEE@{}` | PASS |
| 列类型序列为深度线族专用 `QM EEEE` | `@{\extracolsep{\fill}}QM EEEE@{}` | PASS |
| 用 \extracolsep{\fill} 均分列间余量（tabular* 等宽所需） | `@{\extracolsep{\fill}}QM EEEE@{}` | PASS |
| 两表同用 \TABstyleDL（整表 \scriptsize + 紧凑列距） |  | PASS |

## 13. 正文引用精确性（4.4 节）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文『at or below 0.666 dB』= 本文法最大值 | 四频 ['0.195', '0.144', '0.576', '0.666'] → 最大 `0.666` | PASS |
| 正文 0.666 ← 全精度源 | 源 0.6658386092081794 → `0.666` / 印刷 `0.666` | PASS |
| 正文声明的深度线 y=30.4 m 与脚本 force_y 一致 | tex 行 906 | PASS |
| 正文『DeepONet exceeds 5 dB』成立（阈值断言，不指某格） | DeepONet 最大 `7.038` > 5 | PASS |
| 正文 `$5$\,dB` 不作字面比对 | 该数是阈值表述（exceeds 5 dB），非某单元格的印刷值 | 豁免 |

## 14. 本文法逐频占优

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 25Hz Proposed 为最小 | Proposed `0.195` vs 次优 `0.446` | PASS |
| 50Hz Proposed 为最小 | Proposed `0.144` vs 次优 `0.417` | PASS |
| 75Hz Proposed 为最小 | Proposed `0.576` vs 次优 `1.281` | PASS |
| 100Hz Proposed 为最小 | Proposed `0.666` vs 次优 `1.189` | PASS |

