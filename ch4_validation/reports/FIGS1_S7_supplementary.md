# Fig. S1-S7 — 补充材料 Figs. S1-S7（跨文件核验）

- 对象：`Figs. S1-S7`（Fig. S1-S7）
- 结论：**PASS** — 81 通过 / 0 失败 / 2 警告，共 83 项
- 脚本：`ch4_validation/scripts/FIGS1_S7_supplementary.py`
- 生成：2026-11-19 23:54:10

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 补充材料 tex | `../JASA/OE期刊/paper_R2/OE_supplementary.tex` | 图题与正文编号 |
| 正文 tex | `../JASA/OE期刊/paper_R2/OE_submission.tex` | S 引用 |
| 成图脚本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/figS1_S7_supplementary/figS1_S7_supplementary.py` | 渲染器复用正文 Fig. 4/8/12 |

## 1. 图上数值 ↔ npz（ep200，成图脚本同一插值）

> 场图：每行『Src (x, y)』与『Avg e dB』；网格图：每行『f Hz (x, y)』与各变体 |Err| 平均。取样与正文 Fig. 4/8 相同：每频率前两个留出样本。

| 检查项 | 重算 / 图上 | 结论 |
|---|---|---|
| S1 图件 `figS1_case04_r2.pdf` 存在 | ../JASA/OE期刊/paper_R2/Figures/supplementary/figS1_case04_r2.pdf | PASS |
| S1 `figS1_case04_r2.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S1 `figS1_case04_r2.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S1 Case04：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S2 图件 `figS2_case10_w2.pdf` 存在 | ../JASA/OE期刊/paper_R2/Figures/supplementary/figS2_case10_w2.pdf | PASS |
| S2 `figS2_case10_w2.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S2 `figS2_case10_w2.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S2 Case10：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S3 图件 `figS3_case05_r3.pdf` 存在 | ../JASA/OE期刊/paper_R2/Figures/supplementary/figS3_case05_r3.pdf | PASS |
| S3 `figS3_case05_r3.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S3 `figS3_case05_r3.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S3 Case05：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S4 图件 `figS4_case11_w3.pdf` 存在 | ../JASA/OE期刊/paper_R2/Figures/supplementary/figS4_case11_w3.pdf | PASS |
| S4 `figS4_case11_w3.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S4 `figS4_case11_w3.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S4 Case11：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S5 图件 `figS5_abl_r1.pdf` 存在 | ../JASA/OE期刊/paper_R2/Figures/supplementary/figS5_abl_r1.pdf | PASS |
| S5 `figS5_abl_r1.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S5 `figS5_abl_r1.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S5 消融网格：8 行声源与 32 个平均误差与重算一致 | 全部一致 | PASS |
| S6 图件 `figS6_abl_w1.pdf` 存在 | ../JASA/OE期刊/paper_R2/Figures/supplementary/figS6_abl_w1.pdf | PASS |
| S6 `figS6_abl_w1.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S6 `figS6_abl_w1.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S6 消融网格：8 行声源与 32 个平均误差与重算一致 | 全部一致 | PASS |
| S7 图件 `figS7a_gen_extrap_r10.pdf` 存在 | ../JASA/OE期刊/paper_R2/Figures/supplementary/figS7a_gen_extrap_r10.pdf | PASS |
| S7 `figS7a_gen_extrap_r10.pdf` 宽度不超过版心 494.5 pt | 225.0 pt | PASS |
| S7 `figS7a_gen_extrap_r10.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S7 图件 `figS7b_gen_extrap_w9.pdf` 存在 | ../JASA/OE期刊/paper_R2/Figures/supplementary/figS7b_gen_extrap_w9.pdf | PASS |
| S7 `figS7b_gen_extrap_w9.pdf` 宽度不超过版心 494.5 pt | 225.0 pt | PASS |
| S7 `figS7b_gen_extrap_w9.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S7 Case40：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S7 Case41：8 行声源与平均误差与重算一致 | 全部一致 | PASS |

## 2. 正文 ↔ 补充材料

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文引用的 S 编号恰为 S1-S7（无遗漏、无越界） | 引用 [1, 2, 3, 4, 5, 6, 7] | PASS |
| 补充材料恰有 7 个 figure 环境 | 7 | PASS |
| S1 在 sec:forward（4.3 节）被引用 | 实际出现于 ['sec:forward'] | PASS |
| S2 在 sec:forward（4.3 节）被引用 | 实际出现于 ['sec:forward'] | PASS |
| S3 在 sec:forward（4.3 节）被引用 | 实际出现于 ['sec:forward'] | PASS |
| S4 在 sec:forward（4.3 节）被引用 | 实际出现于 ['sec:forward'] | PASS |
| S5 在 sec:ablation（4.5 节）被引用 | 实际出现于 ['sec:ablation', 'sec:performance'] | PASS |
| S6 在 sec:ablation（4.5 节）被引用 | 实际出现于 ['sec:ablation', 'sec:performance'] | PASS |
| S7 在 sec:generalization（4.7 节）被引用 | 实际出现于 ['sec:generalization'] | PASS |
| 补充材料写 `Fig.~4` ↔ 正文 `fig:res-128` = 4 |  | PASS |
| 补充材料写 `Table~5` ↔ 正文 `tab:res-rect-mf` = 5 |  | PASS |
| 补充材料写 `Fig.~8` ↔ 正文 `fig:perf-cmp-r` = 8 |  | PASS |
| 补充材料写 `Table~10` ↔ 正文 `tab:abl` = 10 |  | PASS |
| 补充材料写 `Fig.~12` ↔ 正文 `fig:gen-grid` = 12 |  | PASS |
| 补充材料写 `Table~12` ↔ 正文 `tab:gen-overall` = 12 |  | PASS |
| 补充材料不含改号前的正文表号（6/11/13/14） | 无 | PASS |
| 补充材料一览表含 `Sec.~4.3`（sec:forward） |  | PASS |
| 补充材料一览表含 `Sec.~4.5`（sec:ablation） |  | PASS |
| 补充材料一览表含 `Sec.~4.7`（sec:generalization） |  | PASS |

## 3. 补充材料为独立文件 / 一览表 ↔ 图题、登记算例、正文编号

> 补充材料只用修订后的编号体系，不出现修订前图号或修订过程措辞；首页一览表的每一行按内容关键词、算例号、节号与表号逐项核对。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 补充材料正文不含修订前图号或修订过程措辞 | 无 | PASS |
| 一览表不含『Original figure』列 |  | PASS |
| 一览表恰列出 S1-S7 | [1, 2, 3, 4, 5, 6, 7] | PASS |
| 一览表 S1『256』出现在 S1 图题中 | $256\times128$\,m, rectangular | PASS |
| 一览表 S1『rectangular』出现在 S1 图题中 | $256\times128$\,m, rectangular | PASS |
| 一览表 S1 算例 `4 (R2)` ↔ 登记 [4] |  | PASS |
| 一览表 S1 引用 `Sec.~4.3, Table~5` ↔ aux sec:forward=4.3, tab:res-rect-mf=5 |  | PASS |
| 一览表 S2『256』出现在 S2 图题中 | $256\times128$\,m, wedge | PASS |
| 一览表 S2『wedge』出现在 S2 图题中 | $256\times128$\,m, wedge | PASS |
| 一览表 S2 算例 `10 (W2)` ↔ 登记 [10] |  | PASS |
| 一览表 S2 引用 `Sec.~4.3, Table~5` ↔ aux sec:forward=4.3, tab:res-rect-mf=5 |  | PASS |
| 一览表 S3『512』出现在 S3 图题中 | $512\times128$\,m, rectangular | PASS |
| 一览表 S3『rectangular』出现在 S3 图题中 | $512\times128$\,m, rectangular | PASS |
| 一览表 S3 算例 `5 (R3)` ↔ 登记 [5] |  | PASS |
| 一览表 S3 引用 `Sec.~4.3, Table~5` ↔ aux sec:forward=4.3, tab:res-rect-mf=5 |  | PASS |
| 一览表 S4『512』出现在 S4 图题中 | $512\times128$\,m, wedge | PASS |
| 一览表 S4『wedge』出现在 S4 图题中 | $512\times128$\,m, wedge | PASS |
| 一览表 S4 算例 `11 (W3)` ↔ 登记 [11] |  | PASS |
| 一览表 S4 引用 `Sec.~4.3, Table~5` ↔ aux sec:forward=4.3, tab:res-rect-mf=5 |  | PASS |
| 一览表 S5『rectangular』出现在 S5 图题中 | Ablation variants, rectangular | PASS |
| 一览表 S5『ablation』出现在 S5 图题中 | Ablation variants, rectangular | PASS |
| 一览表 S5 算例 `25--28 (R1)` ↔ 登记 [25, 26, 27, 28] |  | PASS |
| 一览表 S5 引用 `Sec.~4.5, Table~10` ↔ aux sec:ablation=4.5, tab:abl=10 |  | PASS |
| 一览表 S6『wedge』出现在 S6 图题中 | Ablation variants, wedge | PASS |
| 一览表 S6『ablation』出现在 S6 图题中 | Ablation variants, wedge | PASS |
| 一览表 S6 算例 `29--32 (W1)` ↔ 登记 [29, 30, 31, 32] |  | PASS |
| 一览表 S6 引用 `Sec.~4.5, Table~10` ↔ aux sec:ablation=4.5, tab:abl=10 |  | PASS |
| 一览表 S7『extrapolation』出现在 S7 图题中 | Source extrapolation, remaining splits | PASS |
| 一览表 S7 算例 `40--41 (R10, W9)` ↔ 登记 [40, 41] |  | PASS |
| 一览表 S7 引用 `Sec.~4.7, Table~12` ↔ aux sec:generalization=4.7, tab:gen-overall=12 |  | PASS |
| S5 图上变体名与 Table 10 的『w/o FNO prior』一致 | 图上仍印 R1 的『w/o physics prior』（表格 R2 已改名，图件未重绘） | WARN |
| S6 图上变体名与 Table 10 的『w/o FNO prior』一致 | 图上仍印 R1 的『w/o physics prior』（表格 R2 已改名，图件未重绘） | WARN |

