# Fig. 4 — 多频前向 TL 场图 Fig. 4（128x128 m）

- 对象：`fig:res-128`（Fig. 4）
- 结论：**PASS** — 51 通过 / 0 失败 / 0 警告，共 51 项
- 脚本：`ch4_validation/scripts/FIG04_res_128.py`
- 生成：2026-10-05 21:28:27

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | figure* 环境，两个 subfloat |
| 成图脚本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py` | fig04_05_10_fields.py，按 INDEX.md 对应 Fig 4/5/10 |
| 数据源 npz (Case 3) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No03_R1/Case03_R1__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 9) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No09_W1/Case09_W1__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |

## 1. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py | PASS |
| tex 含 `\label{fig:res-128}` | figure* 环境 | PASS |
| Case 3 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No03_R1/Case03_R1__TL原始数据_ep200.npz | PASS |
| Case 9 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No09_W1/Case09_W1__TL原始数据_ep200.npz | PASS |
| Case 3 图件存在 | Case03_R1_TL.pdf | PASS |
| Case 9 图件存在 | Case09_W1_TL.pdf | PASS |

## 2. 成图脚本确实产出本图

> R1 的成图脚本已参数化路径（_figpaths.py 解析 CH4_RAWROOT/CH4_FIGDIR），与本机另一份副本逐字节比对已无意义；能证明归属的是『脚本的产出清单 == 本图的图件集合』。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本可读 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py | PASS |
| 脚本含 Case Case03 的输出名 `case03_r1_tl` | main() 的 FIG4 分支产出 case03_r1_tl.pdf | PASS |
| 脚本含 Case Case09 的输出名 `case09_w1_tl` | main() 的 FIG4 分支产出 case09_w1_tl.pdf | PASS |
| 脚本输出清单覆盖 Case 3 / Case 9 | 实得 [(3, 'r1'), (6, 'r4'), (7, 'r5'), (8, 'r6'), (9, 'w1'), (12, 'w4')]…（共 14 项） | PASS |
| 脚本含 Fig 4 的产出分支 `FIG4` | 同渲染器服务三张场图，与 INDEX.md 一致 | PASS |
| 脚本含 Fig 5 的产出分支 `FIG5` | 同渲染器服务三张场图，与 INDEX.md 一致 | PASS |
| 脚本含 Fig 10 的产出分支 `FIG9` | 同渲染器服务三张场图，与 INDEX.md 一致 | PASS |

## 3. 口径防漂移（脚本源码 vs 重算层）

> 重算层复刻脚本 fields() 的内层算法（griddata + 椭圆/楔形遮罩 + clip + nanmean）。脚本若改了插值方式或网格分辨率而重算层没跟上，图与核验就会各算一套，这条断言当场报错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 可从源码解析 fields() 默认参数 | grid_res=200, method=cubic | PASS |
| 插值方式一致 | 脚本 `cubic` / 重算层 `cubic` | PASS |
| 网格分辨率一致 | 脚本 `200` / 重算层 `200` | PASS |
| 脚本按 2 位小数印 Avg 标注 | 源码含 `"Avg %.2f dB" % avg`，与 PDF 文本层格式一致 | PASS |
| 脚本按 1 位小数印 Src 坐标 | 源码含 `f = %d Hz%s,  Src (%.1f, %.1f)` | PASS |
| 椭圆内以 NaN 硬掩膜（与重算层同法） | 源码含 `gp[inside] = np.nan` | PASS |

## 4. epoch 自证与 caption 声明

> 场图取 ep200（last epoch）；兄弟表 Table 5 取各案例 best epoch，两者本是不同轮，故两处 epoch 措辞不同是正确的，不可强行统一。

> 图取 ep200(last)，兄弟表 Table 5 取 best epoch。下表列出两者差异，说明 caption 必须写 last —— 若写 best，数值就该换成另一轮的评估值。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 npz epoch = 200 | epoch=200 | PASS |
| Case 9 npz epoch = 200 | epoch=200 | PASS |
| fig:res-128 caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:res-128 caption 未误写 best epoch | 图源自 ep200 npz，非 best-epoch 评估 | PASS |
| fig:res-128 caption 标明尺度 128x128 | 含 `128` | PASS |
| fig:res-128 caption 标明两个案例 | 含 `Case~3` 与 `Case~9` | PASS |
| Case 3 best epoch 可读 | best=198, last=200, 相差 2 轮 | PASS |
| Case 9 best epoch 可读 | best=181, last=200, 相差 19 轮 | PASS |

## 5. 逐样本 Avg 误差：npz 重算 vs 图上标注

> 图上每个 Error 面板的行小标题标 `Avg x.xx dB`，是该样本的场误差均值。从 Raw_Experimental_Data 的 npz 复刻算法重算，与 PDF 文本层标注逐个按 2 位小数比对——这是图与原始数据同源的直接证据。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 图内 Avg 标注数量 | PDF 8 个 / 重算 8 个 | PASS |
| Case 3 8 个 Avg 值逐一吻合 | PDF ['0.42', '1.09', '0.21', '0.26', '0.71', '0.72', '1.44', '1.23'] / 重算 ['0.42', '1.09', '0.21', '0.26', '0.71', '0.72', '1.44', '1.23'] | PASS |
| Case 9 图内 Avg 标注数量 | PDF 8 个 / 重算 8 个 | PASS |
| Case 9 8 个 Avg 值逐一吻合 | PDF ['0.43', '0.29', '0.30', '0.20', '0.44', '0.63', '0.81', '0.77'] / 重算 ['0.43', '0.29', '0.30', '0.20', '0.44', '0.63', '0.81', '0.77'] | PASS |

## 6. Src 坐标：图上标注 vs npz source_pos

> 脚本按 `:.1f` 印 Src；此处按同口径比对。两行标题在同一文本行内（`f = .. Hz, Src (x, y) Avg .. dB`），一次正则同时取出两者。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 8 组 Src 坐标吻合 | PDF 8 组，与 npz source_pos 一致 | PASS |
| Case 9 8 组 Src 坐标吻合 | PDF 8 组，与 npz source_pos 一致 | PASS |

## 7. 图结构：4 频率 × 2 样本

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 样本数 = 8 | n=8 | PASS |
| Case 3 频率排布为每频率 2 行 | [25, 25, 50, 50, 75, 75, 100, 100] | PASS |
| Case 9 样本数 = 8 | n=8 | PASS |
| Case 9 频率排布为每频率 2 行 | [25, 25, 50, 50, 75, 75, 100, 100] | PASS |

## 8. 图与表的关系（趋势同向，不可互算）

> 图上 Avg 是单样本场误差，Table 5 的 TL 是全测试集平均，量纲相同但统计口径不同，**不可互相反算**；可核验的是二者趋势必须同向：高频误差大于低频。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 3 图内 25Hz 误差 < 100Hz 误差 | `1.09` < `1.44` dB | PASS |
| Case 9 图内 25Hz 误差 < 100Hz 误差 | `0.43` < `0.81` dB | PASS |

## 9. 引用完整性（label 已在 aux 注册）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 主图 label `fig:res-128` 注册且编号为 4 | aux `4` | PASS |
| 子图 label `fig:res-128-r` 注册且编号为 4a | aux `4a` | PASS |
| 子图 label `fig:res-128-w` 注册且编号为 4b | aux `4b` | PASS |

## 10. 正文引用：逐张引用（R1 无区间引用）

> R1 已取消旧稿的 `Figs.~\ref{fig:res-128}--\ref{fig:res-wedge-100}` 区间写法，改为逐张引用；256/512 m 两张同族图已从正文删除，其精度数据保留在 Table 5，正文与 aux 均不再有它们的 label。

> 正文称『误差集中在低幅零点与源附近，而非弥散全场』且『障碍物后阴影区清晰、内部掩膜精确置零』。掩膜发生在绘图插值网格上（gp[inside]=NaN），故在 200x200 网格上核验。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文引用 `fig:res-128` 至少 1 处 | 实得 4 处：入口段 + 结论段 | PASS |
| 正文不含覆盖 Fig 4/5 的区间引用（R1 已改逐张引用） | 全文无 `\ref{fig:..}--\ref{fig:..}` 形式的图区间 | PASS |
| Table 5 不再以 `\subref` 交叉引用 Fig. 4 子图（Fig. 列已删） |  | PASS |
| 同族 256/512 m 场图由正文指向补充材料 `Figs.~S1--S4` |  | PASS |
| 子图 label `fig:res-128-r` 仍在 aux 注册 | 编号 `4a` | PASS |
| 子图 label `fig:res-128-w` 仍在 aux 注册 | 编号 `4b` | PASS |
| `fig:res-256` / `fig:res-512` 已不在 aux 注册 | 两张图 R1 已删除，正文不再排版它们 | PASS |
| Case 3 椭圆内在插值网格上被硬掩膜 | 椭圆内 960 格，掩膜后有限值 0（应 0） | PASS |
| Case 9 椭圆内在插值网格上被硬掩膜 | 椭圆内 972 格，掩膜后有限值 0（应 0） | PASS |

