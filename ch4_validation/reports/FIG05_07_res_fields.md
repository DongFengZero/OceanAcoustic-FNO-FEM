# Fig. 5/6/7 — 前向求解 TL 场图 Fig 5/6/7

- 对象：`fig:res-128/256/512`（Fig. 5/6/7）
- 结论：**PASS** — 94 通过 / 0 失败 / 0 警告，共 94 项
- 脚本：`ch4_validation/scripts/FIG05_07_res_fields.py`
- 生成：2026-07-29 00:27:31

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 三个 figure* 环境 |
| 成图脚本（权威） | `regen_results_bigfont.py` | ROOT 在 D:/Data，可命中 results/ |
| 成图脚本（repo 副本） | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/regen_results_bigfont.py` | md5 应与权威副本相同 |
| 数据源 npz (Case 3) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No03_R1/Case03_R1__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 9) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No09_W1/Case09_W1__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 4) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No04_R2/Case04_R2__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 10) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No10_W2/Case10_W2__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 5) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No05_R3/Case05_R3__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 11) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No11_W3/Case11_W3__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |

## 1. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 权威成图脚本存在 | D:\Data\regen_results_bigfont.py | PASS |
| repo 副本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/regen_results_bigfont.py | PASS |
| 两份成图脚本 md5 同源 | 6f8f8c47d10457cc… | PASS |
| Case 3 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No03_R1/Case03_R1__TL原始数据_ep200.npz | PASS |
| Case 9 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No09_W1/Case09_W1__TL原始数据_ep200.npz | PASS |
| Case 4 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No04_R2/Case04_R2__TL原始数据_ep200.npz | PASS |
| Case 10 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No10_W2/Case10_W2__TL原始数据_ep200.npz | PASS |
| Case 5 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No05_R3/Case05_R3__TL原始数据_ep200.npz | PASS |
| Case 11 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No11_W3/Case11_W3__TL原始数据_ep200.npz | PASS |
| Case 3 图件存在 | Case03_R1_TL.pdf | PASS |
| Case 9 图件存在 | Case09_W1_TL.pdf | PASS |
| Case 4 图件存在 | Case04_R2_TL.pdf | PASS |
| Case 10 图件存在 | Case10_W2_TL.pdf | PASS |
| Case 5 图件存在 | Case05_R3_TL.pdf | PASS |
| Case 11 图件存在 | Case11_W3_TL.pdf | PASS |

## 2. 口径防漂移（脚本源码 vs 重算层）

> 重算层复刻 render() 的算法；若脚本改了插值方式或网格分辨率而重算层没跟上，图与核验就会各算一套，这条断言当场报错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 可从源码解析 render() 默认参数 | method=cubic, grid_res=200 | PASS |
| 插值方式一致 | 脚本 `cubic` / 重算层 `cubic` | PASS |
| 网格分辨率一致 | 脚本 `200` / 重算层 `200` | PASS |

## 3. epoch 自证与 caption 声明

> 场图取 ep200（last epoch）；而 Table 6 取各案例 best epoch，Case 3/9/10 的 best 分别为 198/181/192，与 200 不同轮，故两处 epoch 措辞不同是正确的，不可强行统一。

> 图取 ep200(last)，兄弟表 Table 6 取 best epoch。下表列出两者差异，说明 caption 必须写 last —— 若写 best，数值就该换成另一轮的评估值。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 npz epoch = 200 | epoch=200 | PASS |
| Case 9 npz epoch = 200 | epoch=200 | PASS |
| Case 4 npz epoch = 200 | epoch=200 | PASS |
| Case 10 npz epoch = 200 | epoch=200 | PASS |
| Case 5 npz epoch = 200 | epoch=200 | PASS |
| Case 11 npz epoch = 200 | epoch=200 | PASS |
| fig:res-128 caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:res-128 caption 未误写 best epoch | 图源自 ep200 npz，非 best-epoch 评估 | PASS |
| fig:res-128 caption 标明尺度 128x128 | 含 `128` | PASS |
| fig:res-256 caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:res-256 caption 未误写 best epoch | 图源自 ep200 npz，非 best-epoch 评估 | PASS |
| fig:res-256 caption 标明尺度 256x128 | 含 `256` | PASS |
| fig:res-512 caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:res-512 caption 未误写 best epoch | 图源自 ep200 npz，非 best-epoch 评估 | PASS |
| fig:res-512 caption 标明尺度 512x128 | 含 `512` | PASS |
| Case 3 best epoch 可读 | best=198, last=200, 相差 2 轮 | PASS |
| Case 9 best epoch 可读 | best=181, last=200, 相差 19 轮 | PASS |
| Case 4 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 10 best epoch 可读 | best=192, last=200, 相差 8 轮 | PASS |
| Case 5 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 11 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |

## 4. 逐样本 Avg 误差：npz 重算 vs 图上标注

> 图上每个 Error 面板标 `Avg:x.xx dB`，是该样本的场误差均值。从 Raw_Experimental_Data 的 npz 复刻算法重算，与 PDF 内标注逐个按 2 位小数比对——这是图与原始数据同源的直接证据。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 图内 Avg 标注数量 | PDF 8 个 / 重算 8 个 | PASS |
| Case 3 8 个 Avg 值逐一吻合 | PDF ['0.42', '1.09', '0.21', '0.26', '0.71', '0.72', '1.44', '1.23'] / 重算 ['0.42', '1.09', '0.21', '0.26', '0.71', '0.72', '1.44', '1.23'] | PASS |
| Case 9 图内 Avg 标注数量 | PDF 8 个 / 重算 8 个 | PASS |
| Case 9 8 个 Avg 值逐一吻合 | PDF ['0.43', '0.29', '0.30', '0.20', '0.44', '0.63', '0.81', '0.77'] / 重算 ['0.43', '0.29', '0.30', '0.20', '0.44', '0.63', '0.81', '0.77'] | PASS |
| Case 4 图内 Avg 标注数量 | PDF 8 个 / 重算 8 个 | PASS |
| Case 4 8 个 Avg 值逐一吻合 | PDF ['0.45', '0.36', '0.32', '0.49', '1.18', '1.23', '2.60', '2.27'] / 重算 ['0.45', '0.36', '0.32', '0.49', '1.18', '1.23', '2.60', '2.27'] | PASS |
| Case 10 图内 Avg 标注数量 | PDF 8 个 / 重算 8 个 | PASS |
| Case 10 8 个 Avg 值逐一吻合 | PDF ['0.41', '0.59', '0.26', '0.34', '0.92', '0.84', '1.30', '1.39'] / 重算 ['0.41', '0.59', '0.26', '0.34', '0.92', '0.84', '1.30', '1.39'] | PASS |
| Case 5 图内 Avg 标注数量 | PDF 8 个 / 重算 8 个 | PASS |
| Case 5 8 个 Avg 值逐一吻合 | PDF ['0.53', '0.91', '0.80', '0.85', '2.06', '1.69', '4.79', '3.58'] / 重算 ['0.53', '0.91', '0.80', '0.85', '2.06', '1.69', '4.79', '3.58'] | PASS |
| Case 11 图内 Avg 标注数量 | PDF 8 个 / 重算 8 个 | PASS |
| Case 11 8 个 Avg 值逐一吻合 | PDF ['0.75', '0.90', '0.49', '0.55', '1.74', '1.52', '2.55', '2.75'] / 重算 ['0.75', '0.90', '0.49', '0.55', '1.74', '1.52', '2.55', '2.75'] | PASS |

## 5. Src 坐标：图上标注 vs npz source_pos

> 脚本按 `:.1f` 印 Src；此处按同口径比对。注：Fig 3/4 的深度线图已统一为 2 位小数，场图仍为 1 位，两类图的标注口径不同但各自与其脚本一致。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 8 组 Src 坐标吻合 | PDF 8 组，与 npz source_pos 一致 | PASS |
| Case 9 8 组 Src 坐标吻合 | PDF 8 组，与 npz source_pos 一致 | PASS |
| Case 4 8 组 Src 坐标吻合 | PDF 8 组，与 npz source_pos 一致 | PASS |
| Case 10 8 组 Src 坐标吻合 | PDF 8 组，与 npz source_pos 一致 | PASS |
| Case 5 8 组 Src 坐标吻合 | PDF 8 组，与 npz source_pos 一致 | PASS |
| Case 11 8 组 Src 坐标吻合 | PDF 8 组，与 npz source_pos 一致 | PASS |

## 6. 图结构：4 频率 × 2 样本

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 样本数 = 8 | n=8 | PASS |
| Case 3 频率排布为每频率 2 行 | [25, 25, 50, 50, 75, 75, 100, 100] | PASS |
| Case 9 样本数 = 8 | n=8 | PASS |
| Case 9 频率排布为每频率 2 行 | [25, 25, 50, 50, 75, 75, 100, 100] | PASS |
| Case 4 样本数 = 8 | n=8 | PASS |
| Case 4 频率排布为每频率 2 行 | [25, 25, 50, 50, 75, 75, 100, 100] | PASS |
| Case 10 样本数 = 8 | n=8 | PASS |
| Case 10 频率排布为每频率 2 行 | [25, 25, 50, 50, 75, 75, 100, 100] | PASS |
| Case 5 样本数 = 8 | n=8 | PASS |
| Case 5 频率排布为每频率 2 行 | [25, 25, 50, 50, 75, 75, 100, 100] | PASS |
| Case 11 样本数 = 8 | n=8 | PASS |
| Case 11 频率排布为每频率 2 行 | [25, 25, 50, 50, 75, 75, 100, 100] | PASS |

## 7. 图与表的关系（趋势同向，不可互算）

> 图上 Avg 是单样本场误差，Table 6 的 TL 是全测试集平均，量纲相同但统计口径不同，**不可互相反算**；可核验的是二者趋势必须同向：高频误差大于低频。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 图内 25Hz 误差 < 100Hz 误差 | `1.09` < `1.44` dB | PASS |
| Case 3 表内 25Hz TL < 100Hz TL | 表 `0.705` < `1.490` | PASS |
| Case 9 图内 25Hz 误差 < 100Hz 误差 | `0.43` < `0.81` dB | PASS |
| Case 9 表内 25Hz TL < 100Hz TL | 表 `0.709` < `1.265` | PASS |
| Case 4 图内 25Hz 误差 < 100Hz 误差 | `0.45` < `2.60` dB | PASS |
| Case 4 表内 25Hz TL < 100Hz TL | 表 `0.788` < `2.602` | PASS |
| Case 10 图内 25Hz 误差 < 100Hz 误差 | `0.59` < `1.39` dB | PASS |
| Case 10 表内 25Hz TL < 100Hz TL | 表 `0.952` < `1.627` | PASS |
| Case 5 图内 25Hz 误差 < 100Hz 误差 | `0.91` < `4.79` dB | PASS |
| Case 5 表内 25Hz TL < 100Hz TL | 表 `0.883` < `4.036` | PASS |
| Case 11 图内 25Hz 误差 < 100Hz 误差 | `0.90` < `2.75` dB | PASS |
| Case 11 表内 25Hz TL < 100Hz TL | 表 `1.996` < `2.570` | PASS |

## 8. 引用完整性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| label `fig:res-128` 已在 aux 注册 | 编号 `5` | PASS |
| label `fig:res-128-r` 已在 aux 注册 | 编号 `5a` | PASS |
| label `fig:res-128-w` 已在 aux 注册 | 编号 `5b` | PASS |
| label `fig:res-256` 已在 aux 注册 | 编号 `6` | PASS |
| label `fig:res-256-r` 已在 aux 注册 | 编号 `6a` | PASS |
| label `fig:res-256-w` 已在 aux 注册 | 编号 `6b` | PASS |
| label `fig:res-512` 已在 aux 注册 | 编号 `7` | PASS |
| label `fig:res-512-r` 已在 aux 注册 | 编号 `7a` | PASS |
| label `fig:res-512-w` 已在 aux 注册 | 编号 `7b` | PASS |

## 9. 正文引用：被引 + 说明与图内容相符

> Fig 5-9 编号连续，正文用区间引用 `Figs.~\ref{fig:res-128}--\ref{fig:res-wedge-100}` 一次覆盖五张，故单张的 \ref 计数可能为 0，须按区间端点判定『是否被引』。

> 正文称『误差集中在低幅零点与源附近，而非弥散全场』且『障碍物后阴影区清晰、内部掩膜精确置零』。掩膜发生在绘图插值网格上（gp[inside_ell]=NaN），故在 200x200 网格上核验。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文存在覆盖 Fig 5-9 的区间引用 | `Figs.~\ref{fig:res-128}--\ref{fig:res-wedge-100}` | PASS |
| L783 段以该区间引用图证实趋势 | tex 行 816 | PASS |
| Case 3 椭圆内在插值网格上被硬掩膜 | 椭圆内 960 格，掩膜后有限值 0（应 0） | PASS |
| Case 9 椭圆内在插值网格上被硬掩膜 | 椭圆内 972 格，掩膜后有限值 0（应 0） | PASS |

