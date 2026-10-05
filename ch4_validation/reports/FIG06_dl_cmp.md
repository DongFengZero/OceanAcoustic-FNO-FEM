# Fig. 6 — 五方法深度线对比 Fig 6（矩形+楔形合并）

- 对象：`fig:dl-cmp`（Fig. 6）
- 结论：**PASS** — 69 通过 / 0 失败 / 0 警告 / 5 豁免，共 74 项
- 脚本：`ch4_validation/scripts/FIG06_dl_cmp.py`
- 生成：2026-10-05 10:17:47

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | `\label{fig:dl-cmp}` 所在 figure* 浮动体（表+图同体） |
| 成图/取数脚本（权威） | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/_depthline_core.py` | 组 comparison_R1_model_advantage / comparison_W1_model_advantage |
| 同一脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/legacy/advantage_depth_line.py` | legacy 副本，口径函数逐字符相同 |
| 成图脚本（纸面尺寸成图） | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/fig06_07_dl.py` | Fig 6 的 240x142 pt 纸面尺寸版由它写到 out/ |
| 论文图件（Rectangular） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/comparison_r1_model_advantage.pdf` | 来源：成图脚本 out/ 下的纸面尺寸 PDF |
| 论文图件（Wedge） | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/comparison_w1_model_advantage.pdf` | 来源：成图脚本 out/ 下的纸面尺寸 PDF |
| 共用图例图 | `../JASA/OE/OE_Revision_R1_Submission/Figures/results/dl_legend_cmp.pdf` | 本组五条曲线的方法名在此图中 |

## 2. 源可追溯与口径防漂移

> 深度线的口径由 Validation_Scripts/fig06_07_dl/_depthline_core.py 承载，成图脚本 fig06_07_dl.py 直接加载它、不复制算法；common/depthline.py 又直接 import 同一份 core，故三者口径不可能各自漂移。

> 权威 core 与 legacy 副本 md5 不同，属预期：_depthline_core.py 是原 advantage_depth_line.py 整理进仓库时改过路径解析层（_figpaths）的版本，口径函数本身未改；两者的 GRID/METHOD/FREQS 由下一段从模块对象现场读出断言，不靠 md5 证明同源。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 权威 core 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/_depthline_core.py | PASS |
| repo 副本存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/legacy/advantage_depth_line.py | PASS |
| 成图脚本两份副本 md5 相同 | core 与 legacy 副本的 md5 不同是既定的整理结果（路径层被改写），口径一致性改由现场读出 GRID/METHOD/FREQS 断言 | 豁免 |
| 成图脚本 out/ 有纸面尺寸产物 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out | PASS |
| 插值网格 GRID = 300 | 脚本内 `300` | PASS |
| 插值方式 METHOD = 'cubic' | 脚本内 `'cubic'` | PASS |
| 频率集 FREQS = (25, 50, 75, 100) | 脚本内 `(25, 50, 75, 100)` | PASS |
| 脚本内 Src 为 1 位小数（全章统一口径） | 含 `{_sx:.1f}, {_sy:.1f}` | PASS |
| Rectangular Case15_R1_Proposed 的 ep200 npz 存在 | Case15-24/Case15_R1_Proposed/Case15_R1_Proposed__TL原始数据_ep200.npz | PASS |
| Rectangular Case16_R1_DeepONet 的 ep200 npz 存在 | Case15-24/Case16_R1_DeepONet/Case16_R1_DeepONet__TL原始数据_ep200.npz | PASS |
| Rectangular Case17_R1_FNO 的 ep200 npz 存在 | Case15-24/Case17_R1_FNO/Case17_R1_FNO__TL原始数据_ep200.npz | PASS |
| Rectangular Case18_R1_KNO 的 ep200 npz 存在 | Case15-24/Case18_R1_KNO/Case18_R1_KNO__TL原始数据_ep200.npz | PASS |
| Rectangular Case19_R1_CNO 的 ep200 npz 存在 | Case15-24/Case19_R1_CNO/Case19_R1_CNO__TL原始数据_ep200.npz | PASS |
| Wedge Case20_W1_Proposed 的 ep200 npz 存在 | Case15-24/Case20_W1_Proposed/Case20_W1_Proposed__TL原始数据_ep200.npz | PASS |
| Wedge Case21_W1_DeepONet 的 ep200 npz 存在 | Case15-24/Case21_W1_DeepONet/Case21_W1_DeepONet__TL原始数据_ep200.npz | PASS |
| Wedge Case22_W1_FNO 的 ep200 npz 存在 | Case15-24/Case22_W1_FNO/Case22_W1_FNO__TL原始数据_ep200.npz | PASS |
| Wedge Case23_W1_KNO 的 ep200 npz 存在 | Case15-24/Case23_W1_KNO/Case23_W1_KNO__TL原始数据_ep200.npz | PASS |
| Wedge Case24_W1_CNO 的 ep200 npz 存在 | Case15-24/Case24_W1_CNO/Case24_W1_CNO__TL原始数据_ep200.npz | PASS |

## 3. epoch 自证与 caption 声明

> R1 合并后，y=56.1 / y=30.4 由两个 subfloat 题注分别标明，不在大 caption 内；判据随之从 caption_of(图) 移到 subfloat 题注。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-cmp-r 全部 npz epoch == 200 (last) | 实得 [200]（5 份 npz） | PASS |
| fig:dl-cmp-w 全部 npz epoch == 200 (last) | 实得 [200]（5 份 npz） | PASS |
| fig:dl-cmp caption 声明 last epoch | 含 `Profiles are from the last epoch.` | PASS |
| fig:dl-cmp caption 未误写 best epoch | 深度线族一律源自 ep200 npz，非 best epoch 汇总 | PASS |
| caption 声明 five methods |  | PASS |
| caption 声明频率范围 25--100 Hz | 含 `$25$--$100$\,Hz` | PASS |
| caption 说明灰色障碍带与轴端虚线的含义 |  | PASS |
| 大 caption 内含 `y=56.1` / `y=30.4` | R1 改为由 subfloat 题注 `Rectangular (R1), $y=56.1$\,m` 标明，该值已在第 6 节逐块与重算深度比对 | 豁免 |

## 4. 图上 Src 标注：npz 重算 vs PDF 文本层

> 每个频率面板标题带该频率实际选中样本的 source_pos，逐频独立选样，四组坐标互不相同，写错不报编译错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-cmp-r 4 组 Src 吻合 | PDF [('44.5', '21.9'), ('25.9', '49.5'), ('120.7', '89.5'), ('77.5', '103.0')] / npz [('44.5', '21.9'), ('25.9', '49.5'), ('120.7', '89.5'), ('77.5', '103.0')] | PASS |
| fig:dl-cmp-r 四个频率面板齐全（标题形如 `25 Hz, Src (x, y) m`） | 图上 `['25', '50', '75', '100']` | PASS |
| fig:dl-cmp-r 含逐点误差面板 |  | PASS |
| fig:dl-cmp-r 含 TL 纵轴标签 |  | PASS |
| fig:dl-cmp-w 4 组 Src 吻合 | PDF [('80.7', '72.7'), ('117.6', '43.4'), ('113.4', '64.0'), ('88.0', '78.9')] / npz [('80.7', '72.7'), ('117.6', '43.4'), ('113.4', '64.0'), ('88.0', '78.9')] | PASS |
| fig:dl-cmp-w 四个频率面板齐全（标题形如 `25 Hz, Src (x, y) m`） | 图上 `['25', '50', '75', '100']` | PASS |
| fig:dl-cmp-w 含逐点误差面板 |  | PASS |
| fig:dl-cmp-w 含 TL 纵轴标签 |  | PASS |
| 图例（dl_legend_cmp.pdf）含 Proposed | `COMSOL (reference) Proposed DeepONet FNO KNO CNO Obstacle Beyond axis range` | PASS |
| 图例（dl_legend_cmp.pdf）含 DeepONet | `COMSOL (reference) Proposed DeepONet FNO KNO CNO Obstacle Beyond axis range` | PASS |
| 图例（dl_legend_cmp.pdf）含 FNO | `COMSOL (reference) Proposed DeepONet FNO KNO CNO Obstacle Beyond axis range` | PASS |
| 图例（dl_legend_cmp.pdf）含 KNO | `COMSOL (reference) Proposed DeepONet FNO KNO CNO Obstacle Beyond axis range` | PASS |
| 图例（dl_legend_cmp.pdf）含 CNO | `COMSOL (reference) Proposed DeepONet FNO KNO CNO Obstacle Beyond axis range` | PASS |
| 图例含 COMSOL 参考解 |  | PASS |

## 5. 图与表同源（Fig. 6 <-> Table 8）

> MAE 表与深度线图是同一次 build_group 的两个产物。比对论文图件与成图脚本 out/ 下同名 PDF：抹掉嵌入时间戳后 md5 相同，即证明表里的数与图里的线出自同一次运行，不可能各自漂移。★ 不能比 raw md5：matplotlib 每次都写 CreationDate。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-cmp-r 脚本产出 PDF 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out/comparison_R1_model_advantage.pdf | PASS |
| fig:dl-cmp-r 论文图件存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/comparison_r1_model_advantage.pdf | PASS |
| fig:dl-cmp-r 论文图件与脚本产物同源（抹时间戳后同 md5） | md5(no-ts) `1e9e55abb341` | PASS |
| fig:dl-cmp-w 脚本产出 PDF 存在 | OceanAcoustic-FNO-FEM_github/Validation_Scripts/fig06_07_dl/out/comparison_W1_model_advantage.pdf | PASS |
| fig:dl-cmp-w 论文图件存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/results/comparison_w1_model_advantage.pdf | PASS |
| fig:dl-cmp-w 论文图件与脚本产物同源（抹时间戳后同 md5） | md5(no-ts) `10fc09d7ac4d` | PASS |
| PDF 逐字节 md5 相同 | matplotlib 每次运行写入 CreationDate（本机实测 D:2026…），逐字节比对必然不等；已改为抹掉时间戳后比对，同源判定不受影响。 | 豁免 |
| 图件来源为 common/depthline.py:figure_pdf() 所指目录 | 该函数指向 fig06_07_dl/cache/，那里是 core 的旧版大画布渲染（MediaBox 1181.8x855.1 pt）；论文用的是成图脚本 out/ 下的纸面尺寸版（240x142 pt）。本脚本改读 out/。 | 豁免 |

## 6. 表头源坐标与所选样本一致（两块各 4 个）

> Table 8 表头每频率标 $(x,y)$（\srcxy），须等于该频率**实际选中样本**的 source_pos；八个坐标互不相同，写错不会报编译错。★ 图的 subfloat 题注深度也在此一并核：题注写 1 位小数，重算给全精度。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 8 表体可定位 | 长度 1155 | PASS |
| 表头解析到 8 组源坐标（4 矩形 + 4 楔形） | [(44.5, 21.9), (25.9, 49.5), (120.7, 89.5), (77.5, 103.0), (80.7, 72.7), (117.6, 43.4), (113.4, 64.0), (88.0, 78.9)] | PASS |
| fig:dl-cmp-r 选中行深度舍入到 1 位 = 56.1 m | 实际 `56.080268`（subfloat 题注写 1 位小数） | PASS |
| fig:dl-cmp-r subfloat 题注标明 y=56.1 m（与重算一致） | 题注 `Rectangular (R1), y=56.1m` | PASS |
| Rectangular 25Hz 源坐标 | tex `(44.5, 21.9)` / 样本 0 实际 (44.50021, 21.86243) -> `(44.5, 21.9)` | PASS |
| Rectangular 50Hz 源坐标 | tex `(25.9, 49.5)` / 样本 2 实际 (25.88422, 49.48544) -> `(25.9, 49.5)` | PASS |
| Rectangular 75Hz 源坐标 | tex `(120.7, 89.5)` / 样本 4 实际 (120.71240, 89.50000) -> `(120.7, 89.5)` | PASS |
| Rectangular 100Hz 源坐标 | tex `(77.5, 103.0)` / 样本 7 实际 (77.49264, 102.95834) -> `(77.5, 103.0)` | PASS |
| fig:dl-cmp-w 选中行深度舍入到 1 位 = 30.4 m | 实际 `30.394649`（subfloat 题注写 1 位小数） | PASS |
| fig:dl-cmp-w subfloat 题注标明 y=30.4 m（与重算一致） | 题注 `Wedge (W1), y=30.4m` | PASS |
| Wedge 25Hz 源坐标 | tex `(80.7, 72.7)` / 样本 1 实际 (80.73742, 72.72114) -> `(80.7, 72.7)` | PASS |
| Wedge 50Hz 源坐标 | tex `(117.6, 43.4)` / 样本 2 实际 (117.61148, 43.44483) -> `(117.6, 43.4)` | PASS |
| Wedge 75Hz 源坐标 | tex `(113.4, 64.0)` / 样本 5 实际 (113.42506, 63.99967) -> `(113.4, 64.0)` | PASS |
| Wedge 100Hz 源坐标 | tex `(88.0, 78.9)` / 样本 6 实际 (88.02824, 78.86678) -> `(88.0, 78.9)` | PASS |

## 7. 与 Table 8 的一致性（数与数同源）

> 图的 subfloat 题注声明的深度、案例区间必须与表 caption 同值；两者排在同一浮动体内并列同页，读者左右对读。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 8 caption 声明 Cases~15--19 | 与 subfloat 题注的几何对应 | PASS |
| Table 8 caption 声明 Rectangular 深度 y=56.1 m |  | PASS |
| fig:dl-cmp-r 题注深度与 Table 8 同值 |  | PASS |
| Table 8 caption 声明 Cases~20--24 | 与 subfloat 题注的几何对应 | PASS |
| Table 8 caption 声明 Wedge 深度 y=30.4 m |  | PASS |
| fig:dl-cmp-w 题注深度与 Table 8 同值 |  | PASS |

## 8. 正文引用与编号

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-cmp 编号为 6 | aux `6` | PASS |
| 正文多处引用 Fig. 6（4.4 引入段 + 4.5 消融段各一次） | `\ref{fig:dl-cmp}` 出现 2 处 | PASS |
| 子图 `fig:dl-cmp-r` 已在 aux 注册 | aux `9a` | PASS |
| 子图 `fig:dl-cmp-w` 已在 aux 注册 | aux `9b` | PASS |
| 正文以区间引用覆盖两张图 | R1 合并后正文改为单点引用（Fig.~\ref{fig:dl-cmp}），全章已无 \ref{A}--\ref{B} 形式（实测 0 处） | 豁免 |
| 子图编号为全章全局递增的 9a/9b（排版事实） | aux 9a/9b：subfig 计数器跨图累加，正文不引用面板 label | PASS |

