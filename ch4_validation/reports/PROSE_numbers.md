# Table — — 正文每个小数的出处（表格印刷值 / 推导量 / 配置）

- 对象：`prose (abstract + Sec. 4-5)`（Table —）
- 结论：**PASS** — 108 通过 / 0 失败 / 0 警告 / 1 豁免，共 109 项
- 脚本：`ch4_validation/scripts/PROSE_numbers.py`
- 生成：2026-10-05 10:15:40

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | 摘要与第 4-5 章正文、全部表格 |
| 训练代码 | `OceanAcoustic-FNO-FEM_github/Experiment_Code/Main_Code/ocean_trainer_forward_b.py` | 配置参数默认值 |

## 1. 正文每个小数的出处

> 表格印刷值须出自本小节正文 \ref 到的表（逐字符）；推导量用印刷值当场重算；门槛验证论断本身；配置对照代码。任一数不属上述三类即 FAIL。

> 共核 109 个正文小数。

| 数值 @ 节 | 依据 | 结论 |
|---|---|---|
| `0.995` @ sec:setup | γ（ExponentialLR）↔ 训练代码  | PASS |
| `1.0` @ sec:setup | λ_p ↔ 训练代码 --loss_w_prior 默认值 default=1.0 | PASS |
| `6.4` @ sec:setup | COMSOL 软件版本号（作者确认），非数据，无法由归档数据核实 | 豁免 |
| `2.090` @ sec:ideal | 印刷于本节所引 ['tab:ideal-overall'] | PASS |
| `3.383` @ sec:ideal | 印刷于本节所引 ['tab:ideal-overall'] | PASS |
| `0.509` @ sec:ideal | 印刷于本节所引 ['tab:ideal-overall'] | PASS |
| `0.514` @ sec:ideal | 印刷于本节所引 ['tab:ideal-overall'] | PASS |
| `1.688` @ sec:forward → Case 3 | 出自 ['tab:res-rect-mf'] 的 Case 3 行 | PASS |
| `2.121` @ sec:forward → Case 9 | 出自 ['tab:res-rect-mf'] 的 Case 9 行 | PASS |
| `0.951` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `0.899` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `0.058` @ sec:forward → Case 6 | 出自 ['tab:sq100'] 的 Case 6 行 | PASS |
| `0.100` @ sec:forward → Case 12 | 出自 ['tab:sq100'] 的 Case 12 行 | PASS |
| `0.444` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `0.610` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `1.688` @ sec:forward → Case 3 | 出自 ['tab:res-rect-mf'] 的 Case 3 行 | PASS |
| `3.773` @ sec:forward → Case 4 | 出自 ['tab:res-rect-mf'] 的 Case 4 行 | PASS |
| `13.164` @ sec:forward → Case 5 | 出自 ['tab:res-rect-mf'] 的 Case 5 行 | PASS |
| `0.951` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `1.369` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `2.157` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `2.121` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `10.797` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `0.899` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `1.852` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `0.444` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `1.217` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `3.852` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `0.610` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `0.930` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `3.407` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `2.268` @ sec:forward | R3/R1 多频 TL 倍数 = Table 6 印刷值相除 2.157/0.951 | PASS |
| `0.951` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `2.157` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `8.676` @ sec:forward | R6/R4 单频 TL 倍数 = Table 7 印刷值相除 3.852/0.444 | PASS |
| `0.444` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `3.852` @ sec:forward | 印刷于本节所引 ['tab:sq100'] | PASS |
| `0.516` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `1.094` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `1.490` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `1.265` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `10.797` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `13.164` @ sec:forward | 印刷于本节所引 ['tab:res-rect-mf'] | PASS |
| `1.688` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `0.951` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `3.730` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `1.305` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `2.6` @ sec:performance | 门槛：Table 10 中 DeepONet/KNO/CNO 矩形 Avg. TL 均 > 2.6 dB  | PASS |
| `2.121` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `0.899` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `3.179` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `1.090` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `1.265` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `5.512` @ sec:performance | 印刷于本节所引 ['tab:perf-cmp'] | PASS |
| `56.1` @ sec:performance | 印刷于本节所引 ['tab:dl-cmp'] | PASS |
| `30.4` @ sec:performance | 印刷于本节所引 ['tab:dl-cmp'] | PASS |
| `1.515` @ sec:performance | 印刷于本节所引 ['tab:dl-cmp'] | PASS |
| `0.666` @ sec:performance | 印刷于本节所引 ['tab:dl-cmp'] | PASS |
| `11.483` @ sec:ablation | 印刷于本节所引 ['tab:abl'] | PASS |
| `649.193` @ sec:ablation | 印刷于本节所引 ['tab:abl'] | PASS |
| `21.645` @ sec:ablation | 印刷于本节所引 ['tab:abl'] | PASS |
| `3022.705` @ sec:ablation | 印刷于本节所引 ['tab:abl'] | PASS |
| `1.911` @ sec:ablation | 印刷于本节所引 ['tab:abl'] | PASS |
| `38.800` @ sec:ablation | 印刷于本节所引 ['tab:abl'] | PASS |
| `1.936` @ sec:ablation | 印刷于本节所引 ['tab:abl'] | PASS |
| `48.797` @ sec:ablation | 印刷于本节所引 ['tab:abl'] | PASS |
| `1.356` @ sec:ablation | Table 9：w/o graph − Full @75 Hz（印刷值相减）  | PASS |
| `1.834` @ sec:ablation | Table 9：w/o graph − Full @100 Hz（印刷值相减）  | PASS |
| `1.00` @ sec:mesh | 网格分辨率 Δ ∈ Table 12 Δ 列  | PASS |
| `0.50` @ sec:mesh | 网格分辨率 Δ ∈ Table 12 Δ 列  | PASS |
| `0.25` @ sec:mesh | 网格分辨率 Δ ∈ Table 12 Δ 列  | PASS |
| `1.00` @ sec:mesh | 网格分辨率 Δ ∈ Table 12 Δ 列  | PASS |
| `0.25` @ sec:mesh | 网格分辨率 Δ ∈ Table 12 Δ 列  | PASS |
| `0.65` @ sec:mesh | 门槛：Table 12 全部 TL < 0.65 dB max TL = 0.61 | PASS |
| `0.058` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `0.287` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `0.100` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `0.326` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `0.444` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `0.384` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `0.393` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `0.610` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `0.361` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `0.311` @ sec:mesh | 印刷于本节所引 ['tab:mesh'] | PASS |
| `3.642` @ sec:generalization | 印刷于本节所引 ['tab:gen-overall'] | PASS |
| `2.966` @ sec:generalization | 印刷于本节所引 ['tab:gen-overall'] | PASS |
| `4.347` @ sec:generalization | 印刷于本节所引 ['tab:gen-overall'] | PASS |
| `4.437` @ sec:generalization | 印刷于本节所引 ['tab:gen-overall'] | PASS |
| `17.08` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `14.04` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `873.10` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `503.00` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `45.93` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `31.37` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `17.08` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `52.82` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `142.42` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `106.42` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `21{,}737` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `337{,}351` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `10{,}680` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `165{,}034` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `47.53` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `251.39` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `40.57` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `133.09` @ sec:runtime | 印刷于本节所引 ['tab:runtime'] | PASS |
| `337{,}351` @ sec:cons | 印刷于本节所引 ['tab:runtime'] | PASS |
| `5.9` @ sec:cons | 48²×16²（PROSE_derived 回源核）  | PASS |
| `9.4` @ sec:cons | 48²×16³（PROSE_derived 回源核）  | PASS |

