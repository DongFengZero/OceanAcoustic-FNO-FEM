# Fig. 18/19 — 网格独立性场图 Fig 18/19

- 对象：`fig:mesh-rect / fig:mesh-wedge`（Fig. 18/19）
- 结论：**PASS** — 106 通过 / 0 失败 / 0 警告，共 106 项
- 脚本：`ch4_validation/scripts/FIG18_19_mesh.py`
- 生成：2026-07-30 00:07:07

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 两个并列 minipage，各 3 个 subfloat |
| 成图脚本（权威） | `regen_results_bigfont.py` | regen_results_bigfont.py |
| 成图脚本 repo 副本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/regen_results_bigfont.py` | md5 应与权威副本相同 |
| 数据源 npz (Case 33) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No33_R4/Case33_R4__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200 |
| 数据源 npz (Case 34) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No34_R7/Case34_R7__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200 |
| 数据源 npz (Case 35) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No35_R8/Case35_R8__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200 |
| 数据源 npz (Case 36) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No36_W4/Case36_W4__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200 |
| 数据源 npz (Case 37) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No37_W7/Case37_W7__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200 |
| 数据源 npz (Case 38) | `Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No38_W8/Case38_W8__TL原始数据_ep200.npz` | Raw_Experimental_Data，ep200 |

## 1. 源可追溯性

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No33_R4/Case33_R4__TL原始数据_ep200.npz | PASS |
| Case 34 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No34_R7/Case34_R7__TL原始数据_ep200.npz | PASS |
| Case 35 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No35_R8/Case35_R8__TL原始数据_ep200.npz | PASS |
| Case 36 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No36_W4/Case36_W4__TL原始数据_ep200.npz | PASS |
| Case 37 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No37_W7/Case37_W7__TL原始数据_ep200.npz | PASS |
| Case 38 npz 存在 | Data_and_Code_Availability/Raw_Experimental_Data/4.6_Mesh/No38_W8/Case38_W8__TL原始数据_ep200.npz | PASS |
| 成图脚本两份副本均存在 |  | PASS |
| 两份成图脚本 md5 同源 | 6f8f8c47d10457cc… | PASS |
| 图件 Case33_R4_TL.pdf 存在 | ../JASA/OE/els-cas-templates/Figures/results/Case33_R4_TL.pdf | PASS |
| 图件 Case34_R7_TL.pdf 存在 | ../JASA/OE/els-cas-templates/Figures/results/Case34_R7_TL.pdf | PASS |
| 图件 Case35_R8_TL.pdf 存在 | ../JASA/OE/els-cas-templates/Figures/results/Case35_R8_TL.pdf | PASS |
| 图件 Case36_W4_TL.pdf 存在 | ../JASA/OE/els-cas-templates/Figures/results/Case36_W4_TL.pdf | PASS |
| 图件 Case37_W7_TL.pdf 存在 | ../JASA/OE/els-cas-templates/Figures/results/Case37_W7_TL.pdf | PASS |
| 图件 Case38_W8_TL.pdf 存在 | ../JASA/OE/els-cas-templates/Figures/results/Case38_W8_TL.pdf | PASS |

## 2. 口径防漂移（从成图脚本源码读取）

> 重算层 _recompute_field 复刻 render() 的算法，其 method/grid_res 必须与成图脚本签名默认值一致；脚本改了而重算没跟上，此处报错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| render() 签名可解析 |  | PASS |
| 插值方法一致 | 脚本 `cubic` / 重算层 `cubic` | PASS |
| 网格分辨率一致 | 脚本 `200` / 重算层 `200` | PASS |
| Src 标注为 1 位小数（全章统一口径） | 源码含 `Src:({src[0]:.1f},...` | PASS |

## 3. epoch 自证与 caption 声明

> 单频 case 的 best epoch 多不等于 200（Case 14 的 best=129），而图取 ep200，故 caption 必须声明 last epoch。

> 图取 ep200(last)，兄弟表 Tables 17/18 取 best epoch。二者本是不同轮。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 npz epoch=200 | 实得 200 | PASS |
| Case 34 npz epoch=200 | 实得 200 | PASS |
| Case 35 npz epoch=200 | 实得 200 | PASS |
| Case 36 npz epoch=200 | 实得 200 | PASS |
| Case 37 npz epoch=200 | 实得 200 | PASS |
| Case 38 npz epoch=200 | 实得 200 | PASS |
| fig:mesh-rect caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:mesh-rect caption 未误写 best epoch | 图源自 ep200 npz，非 best-epoch 评估 | PASS |
| fig:mesh-rect caption 标明 100 Hz | 含 `f=100` | PASS |
| fig:mesh-wedge caption 声明 last epoch | 含 `Fields are from the last epoch.` | PASS |
| fig:mesh-wedge caption 未误写 best epoch | 图源自 ep200 npz，非 best-epoch 评估 | PASS |
| fig:mesh-wedge caption 标明 100 Hz | 含 `f=100` | PASS |
| Case 33 best epoch 可读 | best=192, last=200, 相差 8 轮 | PASS |
| Case 34 best epoch 可读 | best=200, last=200, 相等（巧合） | PASS |
| Case 35 best epoch 可读 | best=167, last=200, 相差 33 轮 | PASS |
| Case 36 best epoch 可读 | best=195, last=200, 相差 5 轮 | PASS |
| Case 37 best epoch 可读 | best=199, last=200, 相差 1 轮 | PASS |
| Case 38 best epoch 可读 | best=194, last=200, 相差 6 轮 | PASS |

## 4. 逐样本 Avg 误差：npz 重算 vs 图上标注

> 图上每个 Error 面板标 `Avg:x.xx dB`。从 Raw_Experimental_Data 的 npz 复刻算法重算，与 PDF 文本层标注逐个按 2 位小数比对——这是图件产自这批 npz 的直接证据。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 2 个 Avg 逐一吻合 | PDF ['0.25', '0.21'] / npz 重算 ['0.25', '0.21'] | PASS |
| Case 34 2 个 Avg 逐一吻合 | PDF ['0.22', '0.22'] / npz 重算 ['0.22', '0.22'] | PASS |
| Case 35 2 个 Avg 逐一吻合 | PDF ['0.35', '0.31'] / npz 重算 ['0.35', '0.31'] | PASS |
| Case 36 2 个 Avg 逐一吻合 | PDF ['0.25', '0.26'] / npz 重算 ['0.25', '0.26'] | PASS |
| Case 37 2 个 Avg 逐一吻合 | PDF ['0.17', '0.19'] / npz 重算 ['0.17', '0.19'] | PASS |
| Case 38 2 个 Avg 逐一吻合 | PDF ['0.32', '0.30'] / npz 重算 ['0.32', '0.30'] | PASS |

## 5. Src 坐标：npz 重算 vs 图上标注

> 坐标 1 位小数，与深度线图及 Tables 5/9-12 同口径。

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

## 6. 图结构与子图引用

> 单频 npz 只含 2 个样本，故每子图 2 行；三个 subfloat 的 label 须在 aux 注册且编号为 8a/8b/8c、9a/9b/9c。

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
| 主图 label `fig:mesh-rect` 已注册 | 编号 `18` | PASS |
| 子图 label `fig:mesh-rect-a` 已注册 | 编号 `18a` | PASS |
| 子图 `fig:mesh-rect-a` 标注 Case 33 / R4 | subfloat 题注含 `Case~33` 与 `R4` | PASS |
| 子图 label `fig:mesh-rect-b` 已注册 | 编号 `18b` | PASS |
| 子图 `fig:mesh-rect-b` 标注 Case 34 / R7 | subfloat 题注含 `Case~34` 与 `R7` | PASS |
| 子图 label `fig:mesh-rect-c` 已注册 | 编号 `18c` | PASS |
| 子图 `fig:mesh-rect-c` 标注 Case 35 / R8 | subfloat 题注含 `Case~35` 与 `R8` | PASS |
| 主图 label `fig:mesh-wedge` 已注册 | 编号 `19` | PASS |
| 子图 label `fig:mesh-wedge-a` 已注册 | 编号 `19a` | PASS |
| 子图 `fig:mesh-wedge-a` 标注 Case 36 / W4 | subfloat 题注含 `Case~36` 与 `W4` | PASS |
| 子图 label `fig:mesh-wedge-b` 已注册 | 编号 `19b` | PASS |
| 子图 `fig:mesh-wedge-b` 标注 Case 37 / W7 | subfloat 题注含 `Case~37` 与 `W7` | PASS |
| 子图 label `fig:mesh-wedge-c` 已注册 | 编号 `19c` | PASS |
| 子图 `fig:mesh-wedge-c` 标注 Case 38 / W8 | subfloat 题注含 `Case~38` 与 `W8` | PASS |

## 7. 网格独立性：细化下误差保持同量级

> ★ 本组的论点是网格无关性，判据与场图族相反：不要求单调，而要求三种网格间距下误差**保持同一量级**（网格加密 4 倍、节点数增约 16 倍，若误差随之爆掉就说明模型依赖特定离散）。caption 已声明这是个别样本的 last-round 结果，故不与表的均值趋势强行对齐。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:mesh-rect 三种 Δ 下图误差同量级（极差 < 3x） | Δ=1.00m:0.25 / Δ=0.50m:0.22 / Δ=0.25m:0.35 → 1.55x | PASS |
| fig:mesh-rect 三种 Δ 下图误差均 < 1 dB | 最大 `0.35` dB | PASS |
| fig:mesh-wedge 三种 Δ 下图误差同量级（极差 < 3x） | Δ=1.00m:0.26 / Δ=0.50m:0.19 / Δ=0.25m:0.32 → 1.68x | PASS |
| fig:mesh-wedge 三种 Δ 下图误差均 < 1 dB | 最大 `0.32` dB | PASS |

## 8. 引用方式：经 Tables 17/18 的 Fig. 列逐行引用

> ★ 本组的被引方式与前几组都不同：既非散文区间引用，也非单点引用，而是由兄弟表每一行的 Fig. 列指向自己的子图 （`\ref{fig:mesh-rect}\subref{fig:mesh-rect-a}` 等），故须逐行核对『第 N 行的子图引用确指第 N 个 Δ』，错配读者会看错图。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:mesh-rect 编号为 18/19 之一 | aux `18` | PASS |
| Case 33 (Δ=1.00m) 的 Fig. 列引用指向 fig:mesh-rect-a | tex 含 `\ref{fig:mesh-rect}\subref{fig:mesh-rect-a}` | PASS |
| 子图 label `fig:mesh-rect-a` 已在 aux 注册 | 编号 `18a` | PASS |
| Case 34 (Δ=0.50m) 的 Fig. 列引用指向 fig:mesh-rect-b | tex 含 `\ref{fig:mesh-rect}\subref{fig:mesh-rect-b}` | PASS |
| 子图 label `fig:mesh-rect-b` 已在 aux 注册 | 编号 `18b` | PASS |
| Case 35 (Δ=0.25m) 的 Fig. 列引用指向 fig:mesh-rect-c | tex 含 `\ref{fig:mesh-rect}\subref{fig:mesh-rect-c}` | PASS |
| 子图 label `fig:mesh-rect-c` 已在 aux 注册 | 编号 `18c` | PASS |
| fig:mesh-wedge 编号为 18/19 之一 | aux `19` | PASS |
| Case 36 (Δ=1.00m) 的 Fig. 列引用指向 fig:mesh-wedge-a | tex 含 `\ref{fig:mesh-wedge}\subref{fig:mesh-wedge-a}` | PASS |
| 子图 label `fig:mesh-wedge-a` 已在 aux 注册 | 编号 `19a` | PASS |
| Case 37 (Δ=0.50m) 的 Fig. 列引用指向 fig:mesh-wedge-b | tex 含 `\ref{fig:mesh-wedge}\subref{fig:mesh-wedge-b}` | PASS |
| 子图 label `fig:mesh-wedge-b` 已在 aux 注册 | 编号 `19b` | PASS |
| Case 38 (Δ=0.25m) 的 Fig. 列引用指向 fig:mesh-wedge-c | tex 含 `\ref{fig:mesh-wedge}\subref{fig:mesh-wedge-c}` | PASS |
| 子图 label `fig:mesh-wedge-c` 已在 aux 注册 | 编号 `19c` | PASS |

## 9. caption 已声明『个别样本、非最优』的免责说明

> 图上名次可能与表的均值趋势不同（与 Fig 16/17 同类问题）。本组 caption 原本就写明了这点，此处固化为断言防止日后被删。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:mesh-rect caption 声明为个别样本 | 含 `individual sampled examples` | PASS |
| fig:mesh-rect caption 声明非最优轮次 | 含 `rather than the best result` | PASS |
| fig:mesh-rect caption 说明不必吻合表的均值趋势 | 含 `need not follow the averaged trend` | PASS |
| fig:mesh-wedge caption 声明为个别样本 | 含 `individual sampled examples` | PASS |
| fig:mesh-wedge caption 声明非最优轮次 | 含 `rather than the best result` | PASS |
| fig:mesh-wedge caption 说明不必吻合表的均值趋势 | 含 `need not follow the averaged trend` | PASS |

## 10. 数据集复用（Table 3 的 Reuse 列）

> Case 33 复用 Case 6 的 R4 数据集、Case 36 复用 Case 12 的 W4。两侧 npz 须逐字节相同，否则『复用』的说法不成立。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Case 33 与 Case 6 的 npz 逐字节相同 | md5 `89c29fd520e4` vs `89c29fd520e4` | PASS |
| Case 36 与 Case 12 的 npz 逐字节相同 | md5 `d0d35725c8e2` vs `d0d35725c8e2` | PASS |

