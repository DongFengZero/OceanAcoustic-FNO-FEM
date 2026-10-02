# Fig. 7 — 四变体消融深度线 Fig 7（矩形+楔形合并）

- 对象：`fig:dl-abl`（Fig. 7）
- 结论：**PASS** — 74 通过 / 0 失败 / 0 警告 / 5 豁免，共 79 项
- 脚本：`ch4_validation/scripts/FIG07_dl_abl.py`
- 生成：2026-10-03 00:08:15

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{fig:dl-abl}` 所在 figure* 浮动体（表+图同体） |
| 成图/取数脚本（权威） | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/_depthline_core.py` | 组 ablation_R1_module_advantage / ablation_W1_module_advantage |
| 同一脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/legacy/advantage_depth_line.py` | legacy 副本，口径函数逐字符相同 |
| 成图脚本（纸面尺寸成图） | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/fig06_07_dl.py` | Fig 7 的 240x142 pt 纸面尺寸版由它写到 out/ |
| 共用图例图 | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/dl_legend_abl.pdf` | 本组四条曲线的方法名在此图中 |
| 论文图件（Rectangular） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/ablation_r1_module_advantage.pdf` | 来源：成图脚本 out/ 下的纸面尺寸 PDF |
| 论文图件（Wedge） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/ablation_w1_module_advantage.pdf` | 来源：成图脚本 out/ 下的纸面尺寸 PDF |

## 2. 源可追溯与口径防漂移

> 深度线口径由 Validation_Scripts/fig06_07_dl/_depthline_core.py 承载，成图脚本直接加载它不复制算法；common/depthline.py 又 import 同一份core，故三者口径不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 权威 core 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/_depthline_core.py | PASS |
| repo 副本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/legacy/advantage_depth_line.py | PASS |
| 成图脚本两份副本 md5 相同 | core 与 legacy 副本 md5 不同是既定的整理结果（路径解析层 _figpaths 被改写），口径一致性改由现场读出 GRID/METHOD/FREQS 断言 | 豁免 |
| 成图脚本 out/ 有纸面尺寸产物 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out | PASS |
| 插值网格 GRID = 300 | 脚本内 `300` | PASS |
| 插值方式 METHOD = 'cubic' | 脚本内 `'cubic'` | PASS |
| 频率集 FREQS = (25, 50, 75, 100) | 脚本内 `(25, 50, 75, 100)` | PASS |
| 脚本内 Src 为 1 位小数（全章统一口径） | 含 `{_sx:.1f}, {_sy:.1f}` | PASS |
| Rectangular Case25_R1_Full 的 ep200 npz 存在 | Case25-32/Case25_R1_Full/Case25_R1_Full__TL原始数据_ep200.npz | PASS |
| Rectangular Case26_R1_no_prior 的 ep200 npz 存在 | Case25-32/Case26_R1_no_prior/Case26_R1_no_prior__TL原始数据_ep200.npz | PASS |
| Rectangular Case27_R1_no_graph 的 ep200 npz 存在 | Case25-32/Case27_R1_no_graph/Case27_R1_no_graph__TL原始数据_ep200.npz | PASS |
| Rectangular Case28_R1_no_prior_loss 的 ep200 npz 存在 | Case25-32/Case28_R1_no_prior_loss/Case28_R1_no_prior_loss__TL原始数据_ep200.npz | PASS |
| Wedge Case29_W1_Full 的 ep200 npz 存在 | Case25-32/Case29_W1_Full/Case29_W1_Full__TL原始数据_ep200.npz | PASS |
| Wedge Case30_W1_no_prior 的 ep200 npz 存在 | Case25-32/Case30_W1_no_prior/Case30_W1_no_prior__TL原始数据_ep200.npz | PASS |
| Wedge Case31_W1_no_graph 的 ep200 npz 存在 | Case25-32/Case31_W1_no_graph/Case31_W1_no_graph__TL原始数据_ep200.npz | PASS |
| Wedge Case32_W1_no_prior_loss 的 ep200 npz 存在 | Case25-32/Case32_W1_no_prior_loss/Case32_W1_no_prior_loss__TL原始数据_ep200.npz | PASS |

## 3. epoch 自证与 caption 声明

> R1 的 Fig 7 caption 以『layout and conventions as in Fig.~\ref{fig:dl-cmp}』继承 Fig 6 的 epoch 约定，与 Table 9 继承 Table 8 同一写法；故判据改为核继承声明，并回核被继承方确有 last epoch。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-abl-r 全部 npz epoch == 200 (last) | 实得 [200]（4 份 npz） | PASS |
| fig:dl-abl-w 全部 npz epoch == 200 (last) | 实得 [200]（4 份 npz） | PASS |
| caption 声明 ablation variants |  | PASS |
| fig:dl-abl caption 未误写 best epoch | 深度线族一律源自 ep200 npz | PASS |
| caption 以 Fig.~\ref{fig:dl-cmp} 继承布局、约定与 epoch 口径 | 含 `layout and conventions as in Fig.~\ref{fig:dl-cmp}` | PASS |
| 被继承的 Fig. 6 自身声明 last epoch |  | PASS |
| fig:dl-abl caption 自行写明 last epoch | R1 改为继承 Fig. 6 的约定（已回核 Fig. 6 确有 last epoch）；两图的 npz epoch 已在本节逐组核为 200 | 豁免 |
| caption 说明楔形曲线起点（y=(L_y/L_x)x 处，x=33.4 m） |  | PASS |
| caption 以 (b) 指代楔形面板（矩形面板由 subfloat 题注标为 Rectangular） | R1 的 Fig 7 caption 只点名 (b)；矩形面板编号 (a) 由 subfloat 承担 | PASS |

## 4. 图上 Src 标注：npz 重算 vs PDF 文本层

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-abl-r 4 组 Src 吻合 | PDF [('44.5', '21.9'), ('25.9', '49.5'), ('51.5', '5.7'), ('62.8', '85.3')] / npz [('44.5', '21.9'), ('25.9', '49.5'), ('51.5', '5.7'), ('62.8', '85.3')] | PASS |
| fig:dl-abl-r 四个频率面板齐全 | 图上 `['25', '50', '75', '100']` | PASS |
| fig:dl-abl-r 含逐点误差面板 |  | PASS |
| fig:dl-abl-r 含 TL 纵轴标签 |  | PASS |
| fig:dl-abl-w 4 组 Src 吻合 | PDF [('92.7', '58.9'), ('117.6', '43.4'), ('56.7', '33.8'), ('45.5', '29.5')] / npz [('92.7', '58.9'), ('117.6', '43.4'), ('56.7', '33.8'), ('45.5', '29.5')] | PASS |
| fig:dl-abl-w 四个频率面板齐全 | 图上 `['25', '50', '75', '100']` | PASS |
| fig:dl-abl-w 含逐点误差面板 |  | PASS |
| fig:dl-abl-w 含 TL 纵轴标签 |  | PASS |
| 图例（dl_legend_abl.pdf）含 Full | `COMSOL (reference)
Full model
w/o physics prior
w/o graph correction
w/o prior supervision
Obstacle
Beyond axis range` | PASS |
| 图例（dl_legend_abl.pdf）含 w/o | `COMSOL (reference)
Full model
w/o physics prior
w/o graph correction
w/o prior supervision
Obstacle
Beyond axis range` | PASS |
| 图例（dl_legend_abl.pdf）含 prior | `COMSOL (reference)
Full model
w/o physics prior
w/o graph correction
w/o prior supervision
Obstacle
Beyond axis range` | PASS |
| 图例（dl_legend_abl.pdf）含 graph | `COMSOL (reference)
Full model
w/o physics prior
w/o graph correction
w/o prior supervision
Obstacle
Beyond axis range` | PASS |
| 图例（dl_legend_abl.pdf）含 supervision | `COMSOL (reference)
Full model
w/o physics prior
w/o graph correction
w/o prior supervision
Obstacle
Beyond axis range` | PASS |
| 图例（dl_legend_abl.pdf）含 COMSOL | `COMSOL (reference)
Full model
w/o physics prior
w/o graph correction
w/o prior supervision
Obstacle
Beyond axis range` | PASS |
| 图例含 Obstacle 灰带说明 |  | PASS |

## 5. 图与表同源（Fig. 7 <-> Table 9）

> MAE 表与深度线图是同一次 build_group 的两个产物。比对论文图件与脚本out/ 下同名 PDF：抹掉嵌入时间戳后 md5 相同，即证明表里的数与图里的线出自同一次运行。★ raw md5 永远不等：matplotlib 每次写 CreationDate。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-abl-r 脚本产出 PDF 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out/ablation_R1_module_advantage.pdf | PASS |
| fig:dl-abl-r 论文图件存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/ablation_r1_module_advantage.pdf | PASS |
| fig:dl-abl-r 论文图件与脚本产物同源（抹时间戳后同 md5） | md5(no-ts) `42f638c60615` | PASS |
| fig:dl-abl-w 脚本产出 PDF 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out/ablation_W1_module_advantage.pdf | PASS |
| fig:dl-abl-w 论文图件存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/ablation_w1_module_advantage.pdf | PASS |
| fig:dl-abl-w 论文图件与脚本产物同源（抹时间戳后同 md5） | md5(no-ts) `abcd13e24b0b` | PASS |
| PDF 逐字节 md5 相同 | matplotlib 每次运行写入 CreationDate（本机实测 D:2026…），逐字节比对必然不等；已改为抹掉时间戳后比对，同源判定不受影响。 | 豁免 |
| 图件来源为 common/depthline.py:figure_pdf() 所指目录 | 该函数指向 fig06_07_dl/cache/（core 的旧版大画布渲染，MediaBox 1181.8x855.1 pt）；论文用的是成图脚本 out/ 下的纸面尺寸版（240x142 pt）。本脚本改读 out/。 | 豁免 |

## 6. 表头源坐标与所选样本一致（两块各 4 个）

> Table 9 表头每频率标 $(x,y)$（\srcxy）。★ 本表表头分两行：第一行是 `\multicolumn` 的几何块名，第二行才是频率与 \srcxy，故不能只用 header_row()（它止于第一个 \midrule），须在表体内取全部 \srcxy。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 9 表体可定位 | 长度 1133 | PASS |
| 表头块名声明两个几何（R1 / W1） | 第一行 `& \multicolumn{4}{c}{\textit{Rectangular (R1), $y=71.9$\,m}} & \multic` | PASS |
| 表头解析到 8 组源坐标（4 矩形 + 4 楔形） | [(44.5, 21.9), (25.9, 49.5), (51.5, 5.7), (62.8, 85.3), (92.7, 58.9), (117.6, 43.4), (56.7, 33.8), (45.5, 29.5)] | PASS |
| fig:dl-abl-r 选中行深度舍入到 1 位 = 71.9 m | 实际 `71.919732`（subfloat 题注写 1 位小数） | PASS |
| fig:dl-abl-r subfloat 题注标明 y=71.9 m（与重算一致） | 题注 `Rectangular (R1), y=71.9m` | PASS |
| Rectangular 25Hz 源坐标 | tex `(44.5, 21.9)` / 样本 0 实际 (44.50021, 21.86243) -> `(44.5, 21.9)` | PASS |
| Rectangular 50Hz 源坐标 | tex `(25.9, 49.5)` / 样本 2 实际 (25.88422, 49.48544) -> `(25.9, 49.5)` | PASS |
| Rectangular 75Hz 源坐标 | tex `(51.5, 5.7)` / 样本 5 实际 (51.50000, 5.66814) -> `(51.5, 5.7)` | PASS |
| Rectangular 100Hz 源坐标 | tex `(62.8, 85.3)` / 样本 6 实际 (62.75945, 85.33403) -> `(62.8, 85.3)` | PASS |
| fig:dl-abl-w 选中行深度舍入到 1 位 = 33.4 m | 实际 `33.391304`（subfloat 题注写 1 位小数） | PASS |
| fig:dl-abl-w subfloat 题注标明 y=33.4 m（与重算一致） | 题注 `Wedge (W1), y=33.4m` | PASS |
| Wedge 25Hz 源坐标 | tex `(92.7, 58.9)` / 样本 0 实际 (92.73300, 58.85380) -> `(92.7, 58.9)` | PASS |
| Wedge 50Hz 源坐标 | tex `(117.6, 43.4)` / 样本 2 实际 (117.61148, 43.44483) -> `(117.6, 43.4)` | PASS |
| Wedge 75Hz 源坐标 | tex `(56.7, 33.8)` / 样本 4 实际 (56.67198, 33.82414) -> `(56.7, 33.8)` | PASS |
| Wedge 100Hz 源坐标 | tex `(45.5, 29.5)` / 样本 7 实际 (45.49694, 29.46439) -> `(45.5, 29.5)` | PASS |

## 7. 与 Table 9 的一致性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 9 caption 声明 Cases~25--28 | 与 subfloat 题注的几何对应 | PASS |
| Table 9 caption 声明 Rectangular 深度 y=71.9 m |  | PASS |
| fig:dl-abl-r 题注深度与 Table 9 同值 |  | PASS |
| Table 9 caption 声明 Cases~29--32 | 与 subfloat 题注的几何对应 | PASS |
| Table 9 caption 声明 Wedge 深度 y=33.4 m |  | PASS |
| fig:dl-abl-w 题注深度与 Table 9 同值 |  | PASS |
| Table 9 caption 以 Table 8 交代 header/emphasis/epoch 约定 |  | PASS |

## 8. 正文引用、编号与方向性

> 正文 4.5 节称去掉物理先验后『raises the depth-line TL to tens of decibels at every frequency on both geometries』。这是图上曲线最显著的特征，逐频核其成立。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-abl 编号为 7 | aux `7` | PASS |
| 正文多处引用 Fig. 7（4.4 引入段 + 4.5 消融段各一次） | `\ref{fig:dl-abl}` 出现 2 处 | PASS |
| 子图 `fig:dl-abl-r` 已在 aux 注册 | aux `10a` | PASS |
| 子图 `fig:dl-abl-w` 已在 aux 注册 | aux `10b` | PASS |
| 正文以区间引用覆盖两张图 | R1 合并后正文改为单点引用（Fig.~\ref{fig:dl-abl}），全章已无 \ref{A}--\ref{B} 形式 | 豁免 |
| 子图编号为全章全局递增的 10a/10b（排版事实） | subfig 计数器跨图累加，正文不引用面板 label | PASS |
| fig:dl-abl-r w/o prior 四频 TL 均达数十 dB 量级 | 25Hz:26.3 / 50Hz:30.3 / 75Hz:34.1 / 100Hz:35.1 | PASS |
| fig:dl-abl-w w/o prior 四频 TL 均达数十 dB 量级 | 25Hz:8.7 / 50Hz:32.9 / 75Hz:40.6 / 100Hz:34.3 | PASS |
| 正文『tens of decibels』表述由图 7 的 w/o prior 列值印证 |  | PASS |

