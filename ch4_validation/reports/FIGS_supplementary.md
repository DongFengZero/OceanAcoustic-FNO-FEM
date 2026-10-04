# Fig. S1-S7 — 补充材料 Figs. S1-S7（跨文件核验）

- 对象：`Figs. S1-S7`（Fig. S1-S7）
- 结论：**PASS** — 61 通过 / 0 失败 / 0 警告，共 61 项
- 脚本：`ch4_validation/scripts/FIGS_supplementary.py`
- 生成：2026-10-04 13:28:22

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 补充材料 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_supplementary.tex` | 图题与正文编号 |
| 正文 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | S 引用 |
| 回复信 tex | `../JASA/OE/OE_Revision_R1_Submission/Response_to_Reviewers.tex` | 附录 B 映射 |
| 成图脚本 | `OceanAcoustic-FNO-FEM_github/Validation_Scripts/figS_supplementary/figS_supplementary.py` | 渲染器复用正文 Fig. 4/8/12 |

## 1. 图上数值 ↔ npz（ep200，成图脚本同一插值）

> 场图：每行『Src (x, y)』与『Avg e dB』；网格图：每行『f Hz (x, y)』与各变体 |Err| 平均。取样与正文 Fig. 4/8 相同：每频率前两个留出样本。

| 检查项 | 重算 / 图上 | 结论 |
|---|---|---|
| S1 图件 `figS1_case04_r2.pdf` 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS1_case04_r2.pdf | PASS |
| S1 `figS1_case04_r2.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S1 `figS1_case04_r2.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S1 Case04：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S2 图件 `figS2_case10_w2.pdf` 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS2_case10_w2.pdf | PASS |
| S2 `figS2_case10_w2.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S2 `figS2_case10_w2.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S2 Case10：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S3 图件 `figS3_case05_r3.pdf` 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS3_case05_r3.pdf | PASS |
| S3 `figS3_case05_r3.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S3 `figS3_case05_r3.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S3 Case05：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S4 图件 `figS4_case11_w3.pdf` 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS4_case11_w3.pdf | PASS |
| S4 `figS4_case11_w3.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S4 `figS4_case11_w3.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S4 Case11：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S5 图件 `figS5_abl_r1.pdf` 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS5_abl_r1.pdf | PASS |
| S5 `figS5_abl_r1.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S5 `figS5_abl_r1.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S5 消融网格：8 行声源与 32 个平均误差与重算一致 | 全部一致 | PASS |
| S6 图件 `figS6_abl_w1.pdf` 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS6_abl_w1.pdf | PASS |
| S6 `figS6_abl_w1.pdf` 宽度不超过版心 494.5 pt | 491.5 pt | PASS |
| S6 `figS6_abl_w1.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S6 消融网格：8 行声源与 32 个平均误差与重算一致 | 全部一致 | PASS |
| S7 图件 `figS7a_gen_extrap_w9.pdf` 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS7a_gen_extrap_w9.pdf | PASS |
| S7 `figS7a_gen_extrap_w9.pdf` 宽度不超过版心 494.5 pt | 225.0 pt | PASS |
| S7 `figS7a_gen_extrap_w9.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S7 图件 `figS7b_gen_extrap_w10.pdf` 存在 | ../JASA/OE/OE_Revision_R1_Submission/Figures/supplementary/figS7b_gen_extrap_w10.pdf | PASS |
| S7 `figS7b_gen_extrap_w10.pdf` 宽度不超过版心 494.5 pt | 225.0 pt | PASS |
| S7 `figS7b_gen_extrap_w10.pdf` 最小字号 ≥ 6 pt | 6.00 pt | PASS |
| S7 Case41：8 行声源与平均误差与重算一致 | 全部一致 | PASS |
| S7 Case42：8 行声源与平均误差与重算一致 | 全部一致 | PASS |

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
| 补充材料写 `Table~6` ↔ 正文 `tab:res-rect-mf` = 6 |  | PASS |
| 补充材料写 `Fig.~8` ↔ 正文 `fig:perf-cmp-r` = 8 |  | PASS |
| 补充材料写 `Table~11` ↔ 正文 `tab:abl` = 11 |  | PASS |
| 补充材料写 `Fig.~12` ↔ 正文 `fig:gen-grid` = 12 |  | PASS |
| 补充材料写 `Table~13` ↔ 正文 `tab:gen-overall` = 13 |  | PASS |
| 补充材料一览表含 `Sec.~4.3`（sec:forward） |  | PASS |
| 补充材料一览表含 `Sec.~4.5`（sec:ablation） |  | PASS |
| 补充材料一览表含 `Sec.~4.7`（sec:generalization） |  | PASS |

## 3. 回复信附录 B ↔ 补充材料

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 附录 B：原图 6 + 7 → S1--S4 |  | PASS |
| 补充材料一览表 S1 原图号 `6(a)` ∈ 附录 B 的 `6 + 7` |  | PASS |
| 补充材料一览表 S2 原图号 `6(b)` ∈ 附录 B 的 `6 + 7` |  | PASS |
| 补充材料一览表 S3 原图号 `7(a)` ∈ 附录 B 的 `6 + 7` |  | PASS |
| 补充材料一览表 S4 原图号 `7(b)` ∈ 附录 B 的 `6 + 7` |  | PASS |
| 附录 B：原图 16 + 17 → S5--S6 |  | PASS |
| 补充材料一览表 S5 原图号 `16` ∈ 附录 B 的 `16 + 17` |  | PASS |
| 补充材料一览表 S6 原图号 `17` ∈ 附录 B 的 `16 + 17` |  | PASS |
| 附录 B：原图 22 → S7 |  | PASS |
| 补充材料一览表 S7 原图号 `22` ∈ 附录 B 的 `22` |  | PASS |
| 回复信以 `Figs.~S1--S7` 指称补充材料 |  | PASS |

