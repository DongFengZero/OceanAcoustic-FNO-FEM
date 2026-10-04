# Fig. 10 — 网格无关性 TL 场图 Fig. 10

- 对象：`fig:mesh`（Fig. 10）
- 结论：**PASS** — 113 通过 / 0 失败 / 0 警告，共 113 项
- 脚本：`ch4_validation/scripts/FIG10_mesh.py`
- 生成：2026-10-04 13:27:13

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | 两个并列 minipage，各 3 个 subfloat |
| 成图脚本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py` | fig04_05_10_fields.py，按 INDEX.md 对应 Fig 4/5/10 |
| 复用比对 npz (Case 6 / 12) | `Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No06_R4/Case06_R4__TL原始数据_ep200.npz` | 4.3 节单频案例，用于确认 Case 33≡6、36≡12 |
| 数据源 npz (Case 33) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No33_R4/Case33_R4__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 34) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No34_R7/Case34_R7__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 35) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No35_R8/Case35_R8__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 36) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No36_W4/Case36_W4__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 37) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No37_W7/Case37_W7__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |
| 数据源 npz (Case 38) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No38_W8/Case38_W8__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200（last epoch） |

## 1. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py | PASS |
| Case 33 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No33_R4/Case33_R4__TL原始数据_ep200.npz | PASS |
| Case 34 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No34_R7/Case34_R7__TL原始数据_ep200.npz | PASS |
| Case 35 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No35_R8/Case35_R8__TL原始数据_ep200.npz | PASS |
| Case 36 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No36_W4/Case36_W4__TL原始数据_ep200.npz | PASS |
| Case 37 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No37_W7/Case37_W7__TL原始数据_ep200.npz | PASS |
| Case 38 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No38_W8/Case38_W8__TL原始数据_ep200.npz | PASS |
| 图件 Case33_R4_TL.pdf 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/Case33_R4_TL.pdf | PASS |
| 图件 Case34_R7_TL.pdf 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/Case34_R7_TL.pdf | PASS |
| 图件 Case35_R8_TL.pdf 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/Case35_R8_TL.pdf | PASS |
| 图件 Case36_W4_TL.pdf 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/Case36_W4_TL.pdf | PASS |
| 图件 Case37_W7_TL.pdf 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/Case37_W7_TL.pdf | PASS |
| 图件 Case38_W8_TL.pdf 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/Case38_W8_TL.pdf | PASS |

## 2. 成图脚本确实产出本图

> R1 起成图脚本按 CH4_RAWROOT/CH4_FIGDIR 参数化，逐字节副本比对已失效；能证明归属的是『脚本产出清单 == 本图的图件集合』。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本可读 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig04_05_10_fields/fig04_05_10_fields.py | PASS |
| 脚本含 Fig 10 的产出定义 `FIG9` | 与 Fig 4(FIG4)/Fig 5(FIG5) 同渲染器 | PASS |
| 脚本含 Case 33 的输出名 `case33_r4_tl` | FIG9 分支产出 case33_r4_tl.pdf | PASS |
| 脚本含 Case 34 的输出名 `case34_r7_tl` | FIG9 分支产出 case34_r7_tl.pdf | PASS |
| 脚本含 Case 35 的输出名 `case35_r8_tl` | FIG9 分支产出 case35_r8_tl.pdf | PASS |
| 脚本含 Case 36 的输出名 `case36_w4_tl` | FIG9 分支产出 case36_w4_tl.pdf | PASS |
| 脚本含 Case 37 的输出名 `case37_w7_tl` | FIG9 分支产出 case37_w7_tl.pdf | PASS |
| 脚本含 Case 38 的输出名 `case38_w8_tl` | FIG9 分支产出 case38_w8_tl.pdf | PASS |

## 3. 口径防漂移（脚本源码 vs 重算层）

> 重算层复刻脚本 fields() 的内层算法；脚本改了插值方式或网格分辨率而重算层没跟上，图与核验就会各算一套，此处当场报错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 可从源码解析 fields() 默认参数 | grid_res=200, method=cubic | PASS |
| 插值方式一致 | 脚本 `cubic` / 重算层 `cubic` | PASS |
| 网格分辨率一致 | 脚本 `200` / 重算层 `200` | PASS |
| 单频面板按 1 位小数印 Src（全章统一口径） | 源码含 rows_single() 的 `f = %d Hz,  Src (%.1f, %.1f)` | PASS |
| 脚本按 2 位小数印 Avg 标注 | 源码含 `"Avg %.2f dB" % avg` | PASS |

## 4. epoch 自证与 caption 声明

> 图取 ep200（last epoch），兄弟表 Table 12 取 best epoch。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 npz epoch=200 | 实得 200 | PASS |
| Case 34 npz epoch=200 | 实得 200 | PASS |
| Case 35 npz epoch=200 | 实得 200 | PASS |
| Case 36 npz epoch=200 | 实得 200 | PASS |
| Case 37 npz epoch=200 | 实得 200 | PASS |
| Case 38 npz epoch=200 | 实得 200 | PASS |
| fig:mesh caption 声明 last epoch | 含 `from the last epoch` | PASS |
| fig:mesh caption 未误写 best epoch | 图源自 ep200 npz，非 best-epoch 评估 | PASS |
| fig:mesh caption 标明 100 Hz | 含 `$f=100$\,Hz` | PASS |
| fig:mesh caption 写明子图分组 (a)-(c)/(d)-(f) | 矩形 (a)-(c)、楔形 (d)-(f) | PASS |
| Case 33 best epoch 可读 | best=192, last=200, 相差 8 轮 | PASS |
| Case 34 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 35 best epoch 可读 | best=167, last=200, 相差 33 轮 | PASS |
| Case 36 best epoch 可读 | best=195, last=200, 相差 5 轮 | PASS |
| Case 37 best epoch 可读 | best=199, last=200, 相差 1 轮 | PASS |
| Case 38 best epoch 可读 | best=194, last=200, 相差 6 轮 | PASS |

## 5. 逐样本 Avg 误差：npz 重算 vs 图上标注

> 图上每个 Error 面板标 `Avg x.xx dB`。从 Raw_Experimental_Data 的 npz 复刻算法重算，与 PDF 文本层标注逐个按 2 位小数比对——这是图件产自这批 npz 的直接证据。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 图内 Avg 标注数量 | PDF 2 个 / 重算 2 个 | PASS |
| Case 33 2 个 Avg 逐一吻合 | PDF ['0.25', '0.21'] / npz 重算 ['0.25', '0.21'] | PASS |
| Case 34 图内 Avg 标注数量 | PDF 2 个 / 重算 2 个 | PASS |
| Case 34 2 个 Avg 逐一吻合 | PDF ['0.22', '0.22'] / npz 重算 ['0.22', '0.22'] | PASS |
| Case 35 图内 Avg 标注数量 | PDF 2 个 / 重算 2 个 | PASS |
| Case 35 2 个 Avg 逐一吻合 | PDF ['0.35', '0.31'] / npz 重算 ['0.35', '0.31'] | PASS |
| Case 36 图内 Avg 标注数量 | PDF 2 个 / 重算 2 个 | PASS |
| Case 36 2 个 Avg 逐一吻合 | PDF ['0.25', '0.26'] / npz 重算 ['0.25', '0.26'] | PASS |
| Case 37 图内 Avg 标注数量 | PDF 2 个 / 重算 2 个 | PASS |
| Case 37 2 个 Avg 逐一吻合 | PDF ['0.17', '0.19'] / npz 重算 ['0.17', '0.19'] | PASS |
| Case 38 图内 Avg 标注数量 | PDF 2 个 / 重算 2 个 | PASS |
| Case 38 2 个 Avg 逐一吻合 | PDF ['0.32', '0.30'] / npz 重算 ['0.32', '0.30'] | PASS |

## 6. Src 坐标：npz 重算 vs 图上标注

> 坐标 1 位小数，与深度线图及 Tables 6/7/12 同口径。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 2 组 Src 坐标吻合 | PDF [('51.5', '106.1'), ('68.0', '113.4')] / npz [('51.5', '106.1'), ('68.0', '113.4')] | PASS |
| Case 33 Src 均为 1 位小数 | 全部合规 | PASS |
| Case 34 2 组 Src 坐标吻合 | PDF [('51.5', '106.1'), ('68.0', '113.4')] / npz [('51.5', '106.1'), ('68.0', '113.4')] | PASS |
| Case 34 Src 均为 1 位小数 | 全部合规 | PASS |
| Case 35 2 组 Src 坐标吻合 | PDF [('51.5', '106.1'), ('68.0', '113.4')] / npz [('51.5', '106.1'), ('68.0', '113.4')] | PASS |
| Case 35 Src 均为 1 位小数 | 全部合规 | PASS |
| Case 36 2 组 Src 坐标吻合 | PDF [('112.6', '14.9'), ('82.5', '10.5')] / npz [('112.6', '14.9'), ('82.5', '10.5')] | PASS |
| Case 36 Src 均为 1 位小数 | 全部合规 | PASS |
| Case 37 2 组 Src 坐标吻合 | PDF [('112.7', '14.9'), ('82.5', '10.5')] / npz [('112.7', '14.9'), ('82.5', '10.5')] | PASS |
| Case 37 Src 均为 1 位小数 | 全部合规 | PASS |
| Case 38 2 组 Src 坐标吻合 | PDF [('112.7', '14.8'), ('82.5', '10.5')] / npz [('112.7', '14.8'), ('82.5', '10.5')] | PASS |
| Case 38 Src 均为 1 位小数 | 全部合规 | PASS |

## 7. 图结构与子图引用

> 单频 npz 只含 2 个样本，故每子图 2 行；六个 subfloat 的 label 须在 aux 注册，并逐个核 subfloat 题注里的 Case/Dataset/Δ。

> ★ 已知排版缺陷：本图主 label 为 Fig. 10，但六个 subfloat 在 aux 里注册为 13a-13f（subtable 计数器未随 figure 计数器重排）。本图未使用 \subref，印出来仍是 Fig. 10 与 (a)-(f)，读者看不到错号；此处据实记录，不强行断言 10a-10f。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 npz 样本数 = 2 | 单频 case，实得 2 | PASS |
| Case 33 全部样本为 100 Hz | [100] | PASS |
| Case 34 npz 样本数 = 2 | 单频 case，实得 2 | PASS |
| Case 34 全部样本为 100 Hz | [100] | PASS |
| Case 35 npz 样本数 = 2 | 单频 case，实得 2 | PASS |
| Case 35 全部样本为 100 Hz | [100] | PASS |
| Case 36 npz 样本数 = 2 | 单频 case，实得 2 | PASS |
| Case 36 全部样本为 100 Hz | [100] | PASS |
| Case 37 npz 样本数 = 2 | 单频 case，实得 2 | PASS |
| Case 37 全部样本为 100 Hz | [100] | PASS |
| Case 38 npz 样本数 = 2 | 单频 case，实得 2 | PASS |
| Case 38 全部样本为 100 Hz | [100] | PASS |
| 主图 label `fig:mesh` 注册且编号为 10 | aux `10` | PASS |
| 子图 label `fig:mesh-a` 已注册 | 编号 `13a` | PASS |
| 子图 `fig:mesh-a` 题注标注 Case 33 / R4 | subfloat 题注含 `Case~33` 与 `R4` | PASS |
| 子图 `fig:mesh-a` 题注标注 Δ=1.00 m | subfloat 题注含 `$\Delta=1.00$\,m` | PASS |
| 子图 label `fig:mesh-b` 已注册 | 编号 `13b` | PASS |
| 子图 `fig:mesh-b` 题注标注 Case 34 / R7 | subfloat 题注含 `Case~34` 与 `R7` | PASS |
| 子图 `fig:mesh-b` 题注标注 Δ=0.50 m | subfloat 题注含 `$\Delta=0.50$\,m` | PASS |
| 子图 label `fig:mesh-c` 已注册 | 编号 `13c` | PASS |
| 子图 `fig:mesh-c` 题注标注 Case 35 / R8 | subfloat 题注含 `Case~35` 与 `R8` | PASS |
| 子图 `fig:mesh-c` 题注标注 Δ=0.25 m | subfloat 题注含 `$\Delta=0.25$\,m` | PASS |
| 子图 label `fig:mesh-d` 已注册 | 编号 `13d` | PASS |
| 子图 `fig:mesh-d` 题注标注 Case 36 / W4 | subfloat 题注含 `Case~36` 与 `W4` | PASS |
| 子图 `fig:mesh-d` 题注标注 Δ=1.00 m | subfloat 题注含 `$\Delta=1.00$\,m` | PASS |
| 子图 label `fig:mesh-e` 已注册 | 编号 `13e` | PASS |
| 子图 `fig:mesh-e` 题注标注 Case 37 / W7 | subfloat 题注含 `Case~37` 与 `W7` | PASS |
| 子图 `fig:mesh-e` 题注标注 Δ=0.50 m | subfloat 题注含 `$\Delta=0.50$\,m` | PASS |
| 子图 label `fig:mesh-f` 已注册 | 编号 `13f` | PASS |
| 子图 `fig:mesh-f` 题注标注 Case 38 / W8 | subfloat 题注含 `Case~38` 与 `W8` | PASS |
| 子图 `fig:mesh-f` 题注标注 Δ=0.25 m | subfloat 题注含 `$\Delta=0.25$\,m` | PASS |

## 8. 网格无关性：细化下误差保持同量级

> ★ 本组的论点是网格无关性，判据与场图族相反：不要求单调，而要求三种网格间距下误差**保持同一量级**（网格加密 4 倍、节点数增约 16 倍，若误差随之爆掉就说明模型依赖特定离散）。caption 已声明这是个别样本的 last-round 结果，故不与表的均值趋势强行对齐。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 矩形 R4/R7/R8 三种 Δ 下图误差同量级（极差 < 3x） | Δ=1.00m:0.25 / Δ=0.50m:0.22 / Δ=0.25m:0.35 → 1.55x | PASS |
| 矩形 R4/R7/R8 三种 Δ 下图误差均 < 1 dB | 最大 `0.35` dB | PASS |
| 楔形 W4/W7/W8 三种 Δ 下图误差同量级（极差 < 3x） | Δ=1.00m:0.26 / Δ=0.50m:0.19 / Δ=0.25m:0.32 → 1.68x | PASS |
| 楔形 W4/W7/W8 三种 Δ 下图误差均 < 1 dB | 最大 `0.32` dB | PASS |

## 9. 引用方式：正文/表注引用 + caption 交叉引用

> ★ R1 的 Table 12 已无 Fig. 列（合并后只有 Δ|No.R|Dataset|Sol|TL |No.W|Dataset|Sol|TL 九列），故旧稿的『逐行 Fig. 列指向子图』断言已不成立，改为核 caption 与正文的交叉引用。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文/表注引用 `fig:mesh` 至少 2 处 | 实得 2 处（4.6 节正文 + Table 12 caption） | PASS |
| 正文不含图区间引用（R1 已改逐张引用） | 全文无 `\ref{fig:..}--\ref{fig:..}` 形式 | PASS |
| 旧 label `fig:mesh-rect` / `fig:mesh-wedge` 已不存在 | R1 合并为单一 `fig:mesh` | PASS |
| Table 12 caption 写明行对应子图 (a)-(c)/(d)-(f) | caption 含 `panels (a)--(c) and (d)--(f)` | PASS |
| Table 12 caption 交叉引用 Fig. 10 |  | PASS |
| Table 12 数据行 3 行（三档 Δ） | 实得 3 | PASS |
| Table 12 每行 9 列（两几何并排，无 Fig. 列） | Δ | No.R | Dataset | Sol | TL || No.W | Dataset | Sol | TL | PASS |

## 10. caption 已声明『个别样本、非最优』的免责说明

> 图上名次可能与表的均值趋势不同。R1 的 caption 写明了这点，此处固化为断言防止日后被删。★ 注意 R1 的措辞是 `not best-case results`，旧稿的 `rather than the best result` 已不在文中。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 含 `Individual sampled examples from the last epoch` | 已声明个别样本/非最优/不必吻合表均值 | PASS |
| caption 含 `not best-case results` | 已声明个别样本/非最优/不必吻合表均值 | PASS |
| caption 含 `need not follow the averaged trend of the table` | 已声明个别样本/非最优/不必吻合表均值 | PASS |

## 11. 数据集复用（Table 3 的 Reuse 列）

> Case 33 复用 Case 6 的 R4 数据集、Case 36 复用 Case 12 的 W4。两侧 npz 须逐字节相同，否则『复用』的说法不成立。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 与 Case 6 的 npz 逐字节相同 | md5 `89c29fd520e4` vs `89c29fd520e4` | PASS |
| Case 36 与 Case 12 的 npz 逐字节相同 | md5 `d0d35725c8e2` vs `d0d35725c8e2` | PASS |

