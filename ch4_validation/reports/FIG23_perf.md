# Fig. 23 — 推理性能图 Fig 23

- 对象：`fig:perf`（Fig. 23）
- 结论：**PASS** — 44 通过 / 0 失败 / 0 警告，共 44 项
- 脚本：`ch4_validation/scripts/FIG23_perf.py`
- 生成：2026-07-28 20:33:26

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 单个 figure* 环境 |
| 运行时 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.8_Performance/Case43-50_推理时间性能分析.xlsx` | 两个 sheet，Tables 20/21 同源 |

## 1. 图件与已知缺口

> ★ 仓库内没有生成本图的脚本：build_perf.py 只产 xlsx 不画图，全仓 grep `perf_merged` 无命中。因此本图无法做『脚本产物 vs 论文图件 md5 同源』的比对——这是全 21 张图中唯一缺此环节的一张。改以『图上标注 vs 表值』逐点核验替代（下两节），强度略低但仍能锁住图与数据的一致性。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 图件存在 | perf_merged.pdf | PASS |
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
| 兄弟表 `tab:runtime` 在正文被引 | tex 行 1199 | PASS |
| 兄弟表 `tab:runtime-scale` 在正文被引 | tex 行 1229 | PASS |

