# Table 8 — 五方法深度线 TL（矩形 R1 y=56.1m 与楔形 W1 y=30.4m 并排）

- 对象：`tab:dl-cmp`（Table 8）
- 结论：**PASS** — 172 通过 / 0 失败 / 0 警告 / 2 豁免，共 174 项
- 脚本：`ch4_validation/scripts/T08_dl_cmp.py`
- 生成：2026-10-05 10:16:18

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{tab:dl-cmp}` 所在 tabular* |
| 成图/取数脚本（权威） | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/_depthline_core.py` | 组 `comparison_R1_model_advantage` / `comparison_W1_model_advantage` |
| 同一脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/legacy/advantage_depth_line.py` | md5 应与权威副本相同 |
| 脚本导出 MAE 表 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/cache/_mae_tables.json` | round 到 3 位，供正文取用 |
| 论文图件（矩形 R1） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/comparison_R1_model_advantage.pdf` | 成图脚本 out/ 下的纸面尺寸 PDF |
| 论文图件（楔形 W1） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/comparison_W1_model_advantage.pdf` | 成图脚本 out/ 下的纸面尺寸 PDF |

## 2. 源可追溯性与脚本同源

> 深度线的口径由 `Validation_Scripts/fig06_07_dl/_depthline_core.py` 承载，成图脚本 `fig06_07_dl.py` 直接加载它、不复制算法；`common/depthline.py` 又直接 import 同一份 core，故三者口径不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 权威脚本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/_depthline_core.py | PASS |
| repo 副本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/legacy/advantage_depth_line.py | PASS |
| MAE json 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/cache/_mae_tables.json | PASS |
| Case15_R1_Proposed 的 ep200 npz 存在 | Case15-24/Case15_R1_Proposed/Case15_R1_Proposed__TL原始数据_ep200.npz | PASS |
| Case16_R1_DeepONet 的 ep200 npz 存在 | Case15-24/Case16_R1_DeepONet/Case16_R1_DeepONet__TL原始数据_ep200.npz | PASS |
| Case17_R1_FNO 的 ep200 npz 存在 | Case15-24/Case17_R1_FNO/Case17_R1_FNO__TL原始数据_ep200.npz | PASS |
| Case18_R1_KNO 的 ep200 npz 存在 | Case15-24/Case18_R1_KNO/Case18_R1_KNO__TL原始数据_ep200.npz | PASS |
| Case19_R1_CNO 的 ep200 npz 存在 | Case15-24/Case19_R1_CNO/Case19_R1_CNO__TL原始数据_ep200.npz | PASS |
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
| [rect] 指定深度线 force_y = 56.1 | 脚本内 `56.1` | PASS |
| [rect] 数据目录 grpdir = 'Case15-24' | 脚本内 `'Case15-24'` | PASS |
| [rect] 域类型 = 'Rectangle' | 脚本内 `'Rectangle'` | PASS |
| [rect] 脚本方法顺序与 tex 行序一致 | Proposed (Ours) / DeepONet / FNO / KNO / CNO | PASS |
| [wedge] 指定深度线 force_y = 30.4 | 脚本内 `30.4` | PASS |
| [wedge] 数据目录 grpdir = 'Case15-24' | 脚本内 `'Case15-24'` | PASS |
| [wedge] 域类型 = 'Wedge' | 脚本内 `'Wedge'` | PASS |
| [wedge] 脚本方法顺序与 tex 行序一致 | Proposed (Ours) / DeepONet / FNO / KNO / CNO | PASS |

## 4. 全精度重算（复用脚本自身函数）

> [rect] 重算落在第 131 行，实际深度 y=56.080268 m；force_y=56.1 取最近行，caption 写 56.1 m 是其一位小数。

> [wedge] 重算落在第 71 行，实际深度 y=30.394649 m；force_y=30.4 取最近行，caption 写 30.4 m 是其一位小数。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| [rect] 选中行深度舍入到 1 位 = 56.1 m | 实际 `56.080268` | PASS |
| [wedge] 选中行深度舍入到 1 位 = 30.4 m | 实际 `30.394649` | PASS |
| tex 表体可定位 | 长度 1155 | PASS |
| 表体为 tabular*（固定总宽） | is_star=True | PASS |
| caption 声明 rect 深度 y=56.1 m（与重算一致） | caption 含该值 | PASS |
| caption 声明 wedge 深度 y=30.4 m（与重算一致） | caption 含该值 | PASS |
| caption 声明 last epoch | 深度线由 ep200 npz 现场提取，非 best epoch 汇总 | PASS |
| caption 声明两组 Case 区间 15-19 / 20-24 |  | PASS |

## 5. json 与全精度重算一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| [rect] json y_line 与重算一致 | json `56.08` / 重算 `56.08` | PASS |
| [rect] 25Hz Proposed (Ours) json vs 重算 | json `0.469` / 重算 `0.469175680` | PASS |
| [rect] 25Hz DeepONet json vs 重算 | json `0.736` / 重算 `0.735865304` | PASS |
| [rect] 25Hz FNO json vs 重算 | json `0.582` / 重算 `0.581546268` | PASS |
| [rect] 25Hz KNO json vs 重算 | json `1.21` / 重算 `1.210452336` | PASS |
| [rect] 25Hz CNO json vs 重算 | json `1.697` / 重算 `1.697342557` | PASS |
| [rect] 50Hz Proposed (Ours) json vs 重算 | json `0.696` / 重算 `0.695958881` | PASS |
| [rect] 50Hz DeepONet json vs 重算 | json `3.57` / 重算 `3.570382602` | PASS |
| [rect] 50Hz FNO json vs 重算 | json `0.873` / 重算 `0.873428028` | PASS |
| [rect] 50Hz KNO json vs 重算 | json `2.477` / 重算 `2.477373820` | PASS |
| [rect] 50Hz CNO json vs 重算 | json `1.737` / 重算 `1.736770202` | PASS |
| [rect] 75Hz Proposed (Ours) json vs 重算 | json `0.579` / 重算 `0.579045624` | PASS |
| [rect] 75Hz DeepONet json vs 重算 | json `2.243` / 重算 `2.242879460` | PASS |
| [rect] 75Hz FNO json vs 重算 | json `0.916` / 重算 `0.916294399` | PASS |
| [rect] 75Hz KNO json vs 重算 | json `2.456` / 重算 `2.455826182` | PASS |
| [rect] 75Hz CNO json vs 重算 | json `1.84` / 重算 `1.840114785` | PASS |
| [rect] 100Hz Proposed (Ours) json vs 重算 | json `1.515` / 重算 `1.514983695` | PASS |
| [rect] 100Hz DeepONet json vs 重算 | json `5.479` / 重算 `5.478562120` | PASS |
| [rect] 100Hz FNO json vs 重算 | json `2.143` / 重算 `2.142983701` | PASS |
| [rect] 100Hz KNO json vs 重算 | json `2.965` / 重算 `2.964714688` | PASS |
| [rect] 100Hz CNO json vs 重算 | json `4.033` / 重算 `4.032862282` | PASS |
| [wedge] json y_line 与重算一致 | json `30.39` / 重算 `30.39` | PASS |
| [wedge] 25Hz Proposed (Ours) json vs 重算 | json `0.195` / 重算 `0.195135261` | PASS |
| [wedge] 25Hz DeepONet json vs 重算 | json `0.793` / 重算 `0.793083731` | PASS |
| [wedge] 25Hz FNO json vs 重算 | json `0.446` / 重算 `0.445601871` | PASS |
| [wedge] 25Hz KNO json vs 重算 | json `0.832` / 重算 `0.832132345` | PASS |
| [wedge] 25Hz CNO json vs 重算 | json `0.762` / 重算 `0.761761603` | PASS |
| [wedge] 50Hz Proposed (Ours) json vs 重算 | json `0.144` / 重算 `0.144001160` | PASS |
| [wedge] 50Hz DeepONet json vs 重算 | json `1.982` / 重算 `1.982488174` | PASS |
| [wedge] 50Hz FNO json vs 重算 | json `0.417` / 重算 `0.416556085` | PASS |
| [wedge] 50Hz KNO json vs 重算 | json `0.826` / 重算 `0.826277347` | PASS |
| [wedge] 50Hz CNO json vs 重算 | json `1.055` / 重算 `1.054709443` | PASS |
| [wedge] 75Hz Proposed (Ours) json vs 重算 | json `0.576` / 重算 `0.575567594` | PASS |
| [wedge] 75Hz DeepONet json vs 重算 | json `1.468` / 重算 `1.468247207` | PASS |
| [wedge] 75Hz FNO json vs 重算 | json `1.281` / 重算 `1.281330671` | PASS |
| [wedge] 75Hz KNO json vs 重算 | json `2.496` / 重算 `2.496269723` | PASS |
| [wedge] 75Hz CNO json vs 重算 | json `2.836` / 重算 `2.835756529` | PASS |
| [wedge] 100Hz Proposed (Ours) json vs 重算 | json `0.666` / 重算 `0.665838609` | PASS |
| [wedge] 100Hz DeepONet json vs 重算 | json `7.038` / 重算 `7.037914739` | PASS |
| [wedge] 100Hz FNO json vs 重算 | json `1.189` / 重算 `1.189325003` | PASS |
| [wedge] 100Hz KNO json vs 重算 | json `4.315` / 重算 `4.315449918` | PASS |
| [wedge] 100Hz CNO json vs 重算 | json `3.16` / 重算 `3.160087640` | PASS |

## 6. 印刷值比对（全精度舍入到 3 位 vs tex）

> 判定用全精度值，不用 json —— json 已是 round(...,3)，拿它比对等于自证，无法识别补 0（如 KNO@25Hz 印 `1.210`，全精度 1.210xxx 才是真值来源）。行以方法名为键，矩形块占列 1-4、楔形块占列 5-8。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| tex 数据行数 = 5 | 实得 5 | PASS |
| 行以方法名为键且顺序一致 | Proposed / DeepONet / FNO / KNO / CNO | PASS |
| 行 `Proposed` 存在 |  | PASS |
| Proposed rect 25Hz | 源 0.46917567989763087 → `0.469` / 印刷 `0.469` | PASS |
| Proposed rect 50Hz | 源 0.6959588808704593 → `0.696` / 印刷 `0.696` | PASS |
| Proposed rect 75Hz | 源 0.5790456239901534 → `0.579` / 印刷 `0.579` | PASS |
| Proposed rect 100Hz | 源 1.5149836953267912 → `1.515` / 印刷 `1.515` | PASS |
| Proposed wedge 25Hz | 源 0.19513526059996544 → `0.195` / 印刷 `0.195` | PASS |
| Proposed wedge 50Hz | 源 0.14400115992252566 → `0.144` / 印刷 `0.144` | PASS |
| Proposed wedge 75Hz | 源 0.5755675939157606 → `0.576` / 印刷 `0.576` | PASS |
| Proposed wedge 100Hz | 源 0.6658386092081794 → `0.666` / 印刷 `0.666` | PASS |
| 行 `DeepONet` 存在 |  | PASS |
| DeepONet rect 25Hz | 源 0.7358653037284757 → `0.736` / 印刷 `0.736` | PASS |
| DeepONet rect 50Hz | 源 3.570382602400896 → `3.570` / 印刷 `3.570` | PASS |
| DeepONet rect 75Hz | 源 2.242879460338406 → `2.243` / 印刷 `2.243` | PASS |
| DeepONet rect 100Hz | 源 5.478562120157732 → `5.479` / 印刷 `5.479` | PASS |
| DeepONet wedge 25Hz | 源 0.7930837308184404 → `0.793` / 印刷 `0.793` | PASS |
| DeepONet wedge 50Hz | 源 1.9824881738837865 → `1.982` / 印刷 `1.982` | PASS |
| DeepONet wedge 75Hz | 源 1.468247206544106 → `1.468` / 印刷 `1.468` | PASS |
| DeepONet wedge 100Hz | 源 7.037914739452272 → `7.038` / 印刷 `7.038` | PASS |
| 行 `FNO` 存在 |  | PASS |
| FNO rect 25Hz | 源 0.5815462679933076 → `0.582` / 印刷 `0.582` | PASS |
| FNO rect 50Hz | 源 0.8734280283414905 → `0.873` / 印刷 `0.873` | PASS |
| FNO rect 75Hz | 源 0.916294399448016 → `0.916` / 印刷 `0.916` | PASS |
| FNO rect 100Hz | 源 2.1429837005185997 → `2.143` / 印刷 `2.143` | PASS |
| FNO wedge 25Hz | 源 0.4456018707193328 → `0.446` / 印刷 `0.446` | PASS |
| FNO wedge 50Hz | 源 0.4165560846200631 → `0.417` / 印刷 `0.417` | PASS |
| FNO wedge 75Hz | 源 1.2813306714744437 → `1.281` / 印刷 `1.281` | PASS |
| FNO wedge 100Hz | 源 1.1893250031379634 → `1.189` / 印刷 `1.189` | PASS |
| 行 `KNO` 存在 |  | PASS |
| KNO rect 25Hz | 源 1.2104523356989585 → `1.210` / 印刷 `1.210` | PASS |
| KNO rect 50Hz | 源 2.4773738198511013 → `2.477` / 印刷 `2.477` | PASS |
| KNO rect 75Hz | 源 2.455826181522053 → `2.456` / 印刷 `2.456` | PASS |
| KNO rect 100Hz | 源 2.9647146883368984 → `2.965` / 印刷 `2.965` | PASS |
| KNO wedge 25Hz | 源 0.8321323449956286 → `0.832` / 印刷 `0.832` | PASS |
| KNO wedge 50Hz | 源 0.8262773465953761 → `0.826` / 印刷 `0.826` | PASS |
| KNO wedge 75Hz | 源 2.4962697229327806 → `2.496` / 印刷 `2.496` | PASS |
| KNO wedge 100Hz | 源 4.3154499175979115 → `4.315` / 印刷 `4.315` | PASS |
| 行 `CNO` 存在 |  | PASS |
| CNO rect 25Hz | 源 1.6973425568136546 → `1.697` / 印刷 `1.697` | PASS |
| CNO rect 50Hz | 源 1.7367702015589492 → `1.737` / 印刷 `1.737` | PASS |
| CNO rect 75Hz | 源 1.8401147846834267 → `1.840` / 印刷 `1.840` | PASS |
| CNO rect 100Hz | 源 4.032862281813081 → `4.033` / 印刷 `4.033` | PASS |
| CNO wedge 25Hz | 源 0.7617616030071812 → `0.762` / 印刷 `0.762` | PASS |
| CNO wedge 50Hz | 源 1.0547094429258645 → `1.055` / 印刷 `1.055` | PASS |
| CNO wedge 75Hz | 源 2.835756529075116 → `2.836` / 印刷 `2.836` | PASS |
| CNO wedge 100Hz | 源 3.1600876402200573 → `3.160` / 印刷 `3.160` | PASS |

## 7. 末位为 0 的单元格：真值还是补 0

> 凡印刷值末位为 0 的格，单看数字无法排除『2 位补 1 个 0』，逐个回溯全精度源值确认第 3 位确实是 0 或由进位得到。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| DeepONet rect 50Hz 末位 0 可由全精度复现 | 全精度 3.570382602 → `3.570` | PASS |
| KNO rect 25Hz 末位 0 可由全精度复现 | 全精度 1.210452336 → `1.210` | PASS |
| CNO rect 75Hz 末位 0 可由全精度复现 | 全精度 1.840114785 → `1.840` | PASS |
| CNO wedge 100Hz 末位 0 可由全精度复现 | 全精度 3.160087640 → `3.160` | PASS |
| 末位为 0 的格子共 4 个，全部回溯完毕 |  | PASS |

## 8. 表头源坐标与所选样本一致（两块各 4 个）

> 表头每频率标 $(x,y)$（`\srcxy`），须等于该频率**实际选中样本**的 source_pos；选线算法逐频独立挑样本，八个坐标互不相同，写错不会报编译错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 表头解析到 8 组源坐标（4 矩形 + 4 楔形） | [(44.5, 21.9), (25.9, 49.5), (120.7, 89.5), (77.5, 103.0), (80.7, 72.7), (117.6, 43.4), (113.4, 64.0), (88.0, 78.9)] | PASS |
| rect 25Hz 源坐标 | tex `(44.5, 21.9)` / 样本 0 实际 (44.50021, 21.86243) → `(44.5, 21.9)` | PASS |
| rect 50Hz 源坐标 | tex `(25.9, 49.5)` / 样本 2 实际 (25.88422, 49.48544) → `(25.9, 49.5)` | PASS |
| rect 75Hz 源坐标 | tex `(120.7, 89.5)` / 样本 4 实际 (120.71240, 89.50000) → `(120.7, 89.5)` | PASS |
| rect 100Hz 源坐标 | tex `(77.5, 103.0)` / 样本 7 实际 (77.49264, 102.95834) → `(77.5, 103.0)` | PASS |
| wedge 25Hz 源坐标 | tex `(80.7, 72.7)` / 样本 1 实际 (80.73742, 72.72114) → `(80.7, 72.7)` | PASS |
| wedge 50Hz 源坐标 | tex `(117.6, 43.4)` / 样本 2 实际 (117.61148, 43.44483) → `(117.6, 43.4)` | PASS |
| wedge 75Hz 源坐标 | tex `(113.4, 64.0)` / 样本 5 实际 (113.42506, 63.99967) → `(113.4, 64.0)` | PASS |
| wedge 100Hz 源坐标 | tex `(88.0, 78.9)` / 样本 6 实际 (88.02824, 78.86678) → `(88.0, 78.9)` | PASS |

## 9. 表与图同源（Table 8 ↔ Fig. 的两块）

> MAE 表和深度线图是同一次选线/选样本的两个产物。比对论文图件与成图脚本 out/ 下同名 PDF：内容逐字节相同（仅嵌入时间戳不同，比对前抹掉），则『表里的数』与『图里的线』必定来自同一次计算，不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| [rect] 脚本产出 PDF 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out/comparison_R1_model_advantage.pdf | PASS |
| [rect] 论文图件存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/comparison_R1_model_advantage.pdf | PASS |
| [rect] 论文图件与脚本产物同源（抹时间戳后同 md5） | md5(no-ts) `1e9e55abb341f31ba8347037c81d04d6` | PASS |
| [wedge] 脚本产出 PDF 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out/comparison_W1_model_advantage.pdf | PASS |
| [wedge] 论文图件存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/comparison_W1_model_advantage.pdf | PASS |
| [wedge] 论文图件与脚本产物同源（抹时间戳后同 md5） | md5(no-ts) `10fc09d7ac4d7de742726c0f3857ffbb` | PASS |
| PDF 逐字节 md5 相同 | matplotlib 每次运行写入 CreationDate（本机实测 D:2026…），逐字节比对必然不等；已改为抹掉时间戳后比对，同源判定不受影响。 | 豁免 |

## 10. 加粗正确性（Best in bold，两块各自取列最小）

> caption 只声明『每列最优加粗』；两张表并排后每列分属不同几何，故最小值必须在各自块内取，不能用跨块的全局最小。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| rect 25Hz 加粗落在最小值行 | 加粗 ['Proposed'] / 最小值 Proposed (`0.469`) | PASS |
| rect 50Hz 加粗落在最小值行 | 加粗 ['Proposed'] / 最小值 Proposed (`0.696`) | PASS |
| rect 75Hz 加粗落在最小值行 | 加粗 ['Proposed'] / 最小值 Proposed (`0.579`) | PASS |
| rect 100Hz 加粗落在最小值行 | 加粗 ['Proposed'] / 最小值 Proposed (`1.515`) | PASS |
| wedge 25Hz 加粗落在最小值行 | 加粗 ['Proposed'] / 最小值 Proposed (`0.195`) | PASS |
| wedge 50Hz 加粗落在最小值行 | 加粗 ['Proposed'] / 最小值 Proposed (`0.144`) | PASS |
| wedge 75Hz 加粗落在最小值行 | 加粗 ['Proposed'] / 最小值 Proposed (`0.576`) | PASS |
| wedge 100Hz 加粗落在最小值行 | 加粗 ['Proposed'] / 最小值 Proposed (`0.666`) | PASS |

## 11. 同表小数位一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 40 个数值单元格均为 3 位小数 | 全部合规 | PASS |

## 12. 与 Table 9 的版式一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 9 表体可定位 | 长度 1133 | PASS |
| Table 9 亦为 tabular* | is_star=True | PASS |
| 两表列定义可解析 | Table 8 `@{\extracolsep{\fill}}M EEEE EEEE@{}` / Table 9 `@{\extracolsep{\fill}}A EEEE EEEE@{}` | PASS |
| Table 8 列类型序列为 `M EEEE EEEE` | `@{\extracolsep{\fill}}M EEEE EEEE@{}` | PASS |
| Table 9 列类型序列为 `A EEEE EEEE` | `@{\extracolsep{\fill}}A EEEE EEEE@{}` | PASS |
| Table 8 用 \extracolsep{\fill} 均分列间余量 | `@{\extracolsep{\fill}}M EEEE EEEE@{}` | PASS |
| Table 9 用 \extracolsep{\fill} 均分列间余量 | `@{\extracolsep{\fill}}A EEEE EEEE@{}` | PASS |
| 两表同用 \TABstyleDL（整表紧凑列距） |  | PASS |
| 两表的 tabular* 总宽参数一致（等宽并排） | dl-cmp=`\linewidth` / dl-abl=`\linewidth` | PASS |

## 13. 正文引用精确性（4.4 节）

> 正文 `$1.515$\,dB on the rectangular line and $0.666$\,dB on the wedge line` 是**分几何**的本文法最大值，不是跨块全局最大。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文『at or below 1.515 dB on the rectangular line』 | 矩形四频 ['0.469', '0.696', '0.579', '1.515'] → 最大 `1.515` | PASS |
| 正文『0.666 dB on the wedge line』 | 楔形四频 ['0.195', '0.144', '0.576', '0.666'] → 最大 `0.666` | PASS |
| 正文声明的深度线 y=56.1 m 与脚本 force_y 一致 | tex 行 905 | PASS |
| 正文声明的深度线 y=30.4 m 与脚本 force_y 一致 | tex 行 905 | PASS |
| 正文『DeepONet exceeds 5 dB』成立（阈值断言，不指某格） | DeepONet 最大 `7.038` > 5 | PASS |
| 正文 `$5$\,dB` 不作字面比对 | 该数是阈值表述（exceeds 5 dB），非某单元格的印刷值 | 豁免 |

## 14. 本文法逐频占优（两块分别）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| rect 25Hz Proposed 为最小 | Proposed `0.469` vs 次优 `0.582` | PASS |
| rect 50Hz Proposed 为最小 | Proposed `0.696` vs 次优 `0.873` | PASS |
| rect 75Hz Proposed 为最小 | Proposed `0.579` vs 次优 `0.916` | PASS |
| rect 100Hz Proposed 为最小 | Proposed `1.515` vs 次优 `2.143` | PASS |
| wedge 25Hz Proposed 为最小 | Proposed `0.195` vs 次优 `0.446` | PASS |
| wedge 50Hz Proposed 为最小 | Proposed `0.144` vs 次优 `0.417` | PASS |
| wedge 75Hz Proposed 为最小 | Proposed `0.576` vs 次优 `1.281` | PASS |
| wedge 100Hz Proposed 为最小 | Proposed `0.666` vs 次优 `1.189` | PASS |

