# Fig. 23 — 推理性能图 Fig 23

- 对象：`fig:perf`（Fig. 23）
- 结论：**PASS** — 54 通过 / 0 失败 / 0 警告，共 54 项
- 脚本：`ch4_validation/scripts/FIG23_perf.py`
- 生成：2026-07-29 01:10:27

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 单个 figure* 环境 |
| 运行时 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.8_Performance/Case43-50_推理时间性能分析.xlsx` | 两个 sheet，Tables 20/21 同源 |

## 1. 图件与已知缺口

> 成图脚本原先不在仓库内（build_perf.py 只产 xlsx 不画图），现已收入 Validation_Scripts/build_perf_figure.py。该脚本把数值**硬编码**在源码里而非从 xlsx 读取，所以真正的风险不是『图与脚本不一致』，而是『脚本里的常量与表值脱钩』——下一节直接解析源码常量与 xlsx 比对，正是针对这一点。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 图件存在 | perf_merged.pdf | PASS |
| 成图脚本已入库 | Validation_Scripts/build_perf_figure.py | PASS |
| PDF 文本层可读 | 484 字符 | PASS |

## 2. 子图(a)(b) 标注 vs Table 20

> 图上标注取整，表值保留小数。逐点核『图标注 == round(表值)』。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 20 含 6 行 GPU 数据（R1/W1 各 1/2/4 卡） | 实得 6 | PASS |
| 图(a) 第1点吞吐 53 == round(52.82) | 表 `52.82` → `53` | PASS |
| 图(b) 第1点加速 46x == round(45.9) | 表 `45.9` → `46` | PASS |
| 图(a) 标注 `53` 见于 PDF |  | PASS |
| 图(b) 标注 `46` 见于 PDF |  | PASS |
| 图(a) 第2点吞吐 98 == round(98.22) | 表 `98.22` → `98` | PASS |
| 图(b) 第2点加速 85x == round(85.4) | 表 `85.4` → `85` | PASS |
| 图(a) 标注 `98` 见于 PDF |  | PASS |
| 图(b) 标注 `85` 见于 PDF |  | PASS |
| 图(a) 第3点吞吐 164 == round(163.78) | 表 `163.78` → `164` | PASS |
| 图(b) 第3点加速 142x == round(142.4) | 表 `142.4` → `142` | PASS |
| 图(a) 标注 `164` 见于 PDF |  | PASS |
| 图(b) 标注 `142` 见于 PDF |  | PASS |
| 图(a) 第4点吞吐 62 == round(62.42) | 表 `62.42` → `62` | PASS |
| 图(b) 第4点加速 31x == round(31.4) | 表 `31.4` → `31` | PASS |
| 图(a) 标注 `62` 见于 PDF |  | PASS |
| 图(b) 标注 `31` 见于 PDF |  | PASS |
| 图(a) 第5点吞吐 120 == round(120.35) | 表 `120.35` → `120` | PASS |
| 图(b) 第5点加速 60x == round(60.5) | 表 `60.5` → `60` | PASS |
| 图(a) 标注 `120` 见于 PDF |  | PASS |
| 图(b) 标注 `60` 见于 PDF |  | PASS |
| 图(a) 第6点吞吐 212 == round(211.77) | 表 `211.77` → `212` | PASS |
| 图(b) 第6点加速 106x == round(106.4) | 表 `106.4` → `106` | PASS |
| 图(a) 标注 `212` 见于 PDF |  | PASS |
| 图(b) 标注 `106` 见于 PDF |  | PASS |

## 3. 子图(c) 标注 vs Table 21

> 子图(c) 只在数据点旁标域边长，不标数值；核标注齐全且与 Table 21 的 Lx 列一致（三种尺度各出现于矩形与楔形两条曲线）。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 21 的 Lx 取值 = 128/256/512 | [128, 256, 512] | PASS |
| 子图(c) 标注域边长 128 m（矩形+楔形两条曲线各一次） | PDF 内出现 2 次 | PASS |
| 子图(c) 标注域边长 256 m（矩形+楔形两条曲线各一次） | PDF 内出现 2 次 | PASS |
| 子图(c) 标注域边长 512 m（矩形+楔形两条曲线各一次） | PDF 内出现 2 次 | PASS |

## 3b. 成图脚本硬编码常量 vs xlsx 表值

> 脚本里 thr/spd/nodes/time 四组常量是手抄进去的，一旦表值更新而常量未同步，图就会静默过期。此处用 ast 解析源码取出常量，与 xlsx 逐值比对——这是比『图上标注 vs 表值』更靠前的一道闸。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 脚本 thr[R1] 与 Table 20 一致 | 脚本 [52.82, 98.22, 163.78] / xlsx [52.82, 98.22, 163.78] | PASS |
| 脚本 spd[R1] 与 Table 20 一致 | 脚本 [45.9, 85.4, 142.4] / xlsx [45.9, 85.4, 142.4] | PASS |
| 脚本 thr[W1] 与 Table 20 一致 | 脚本 [62.42, 120.35, 211.77] / xlsx [62.42, 120.35, 211.77] | PASS |
| 脚本 spd[W1] 与 Table 20 一致 | 脚本 [31.4, 60.5, 106.4] / xlsx [31.4, 60.5, 106.4] | PASS |
| 脚本 nodes_R 与 Table 21 一致 | 脚本 [21737, 85353, 337351] / xlsx [21737, 85353, 337351] | PASS |
| 脚本 time_R 与 Table 21 一致 | 脚本 [47.02, 85.86, 249.53] / xlsx [47.02, 85.86, 249.53] | PASS |
| 脚本 nodes_W 与 Table 21 一致 | 脚本 [10680, 41633, 165034] / xlsx [10680, 41633, 165034] | PASS |
| 脚本 time_W 与 Table 21 一致 | 脚本 [40.1, 58.24, 132.41] / xlsx [40.1, 58.24, 132.41] | PASS |
| 脚本 edge 标注 = 128/256/512 | [128, 256, 512] | PASS |

## 4. caption 与正文引用

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| caption 不含 epoch 声明（推理耗时与训练轮次无关，正确） |  | PASS |
| caption 说明子图 (a) |  | PASS |
| caption 说明子图 (b) |  | PASS |
| caption 说明子图 (c) |  | PASS |
| caption 标明 GPU 型号 A800 |  | PASS |
| caption 标明子图(c) 用单 DCU |  | PASS |
| caption 标明子图(c) 案例区间 45-50 | 含 `Cases~45--50` | PASS |
| caption 说明子图(b) 的基准是 COMSOL |  | PASS |
| 编号为 23 | aux `23` | PASS |
| 正文以 `Fig.~\ref{fig:perf}(a,b)` 引用多 GPU 部分 |  | PASS |
| 正文以 `Fig.~\ref{fig:perf}(c)` 引用域缩放部分 |  | PASS |
| 兄弟表 `tab:runtime` 在正文被引 | tex 行 1232 | PASS |
| 兄弟表 `tab:runtime-scale` 在正文被引 | tex 行 1262 | PASS |

