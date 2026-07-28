# Fig. 3-23 — 全章图件引用完整性

- 对象：`fig:* (Ch.4)`（Fig. 3-23）
- 结论：**PASS** — 66 通过 / 0 失败 / 0 警告，共 66 项
- 脚本：`ch4_validation/scripts/FIGALL_refs.py`
- 生成：2026-07-29 00:29:42

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 全文 |
| 编号来源 aux | `../JASA/OE/els-cas-templates/OE_submission.aux` | \newlabel 解析 |

## 1. 无孤图：每个图 label 至少被引用一次

> 统计每个 label 的 \ref 出现次数，并区分正文引用与 caption 内交叉引用。区间引用 `\ref{A}--\ref{B}` 只写出两个端点，中间各图（如 Fig 8）的 \ref 计数为 0——故对区间内部的图，以『存在覆盖它的区间』作为已引证据，不能只看自身计数。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文存在区间引用 | 共 5 处 | PASS |
| Fig 3 (`fig:ideal-rect`) 已被引用 | 正文 1 处；caption 内 3 处 | PASS |
| Fig 4 (`fig:ideal-wedge`) 已被引用 | 正文 1 处；caption 内 2 处 | PASS |
| Fig 5 (`fig:res-128`) 已被引用 | 正文 4 处；caption 内 2 处 | PASS |
| Fig 6 (`fig:res-256`) 已被引用 | 正文 2 处 | PASS |
| Fig 7 (`fig:res-512`) 已被引用 | 正文 2 处 | PASS |
| Fig 8 (`fig:res-rect-100`) 已被引用 | 正文 1 处；caption 内 3 处 | PASS |
| Fig 9 (`fig:res-wedge-100`) 已被引用 | 正文 3 处；caption 内 3 处 | PASS |
| Fig 10 (`fig:dl-cmp-rect`) 已被引用 | 正文 1 处 | PASS |
| Fig 11 (`fig:dl-cmp-wedge`) 已被引用 | 正文 1 处 | PASS |
| Fig 12 (`fig:dl-abl-rect`) 已被引用 | 正文 2 处 | PASS |
| Fig 13 (`fig:dl-abl-wedge`) 已被引用 | 正文 2 处 | PASS |
| Fig 14 (`fig:perf-rect`) 已被引用 | 正文 2 处；caption 内 2 处 | PASS |
| Fig 15 (`fig:perf-wedge`) 已被引用 | 正文 2 处；caption 内 1 处 | PASS |
| Fig 16 (`fig:abl-rect`) 已被引用 | 正文 1 处；caption 内 2 处 | PASS |
| Fig 17 (`fig:abl-wedge`) 已被引用 | 正文 1 处；caption 内 1 处 | PASS |
| Fig 18 (`fig:mesh-rect`) 已被引用 | 正文 1 处；caption 内 3 处 | PASS |
| Fig 19 (`fig:mesh-wedge`) 已被引用 | 正文 1 处；caption 内 3 处 | PASS |
| Fig 20 (`fig:gen-split`) 已被引用 | 正文 1 处 | PASS |
| Fig 21 (`fig:gen-grid`) 已被引用 | 正文 1 处；caption 内 1 处 | PASS |
| Fig 22 (`fig:gen-grid-wedge`) 已被引用 | 正文 1 处 | PASS |
| Fig 23 (`fig:perf`) 已被引用 | 正文 2 处 | PASS |

## 2. 无悬空引用：每个 \ref{fig:...} 都指向真实 label

> 反向查：正文里引用的图号必须在 aux 里注册，否则排版出 `??`。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 22 个被引 label 均已注册 | 全部合规 | PASS |

## 3. 每图均有独立正文引用（不靠区间/caption 兜底）

> ★ 这一节把标准统一收紧：第 1 节只要求『被引』，区间内部的图或仅靠 caption 交叉引用的图也算过。但读者在正文里读不到直接指引并不理想，故此处要求每张图在 figure 环境**之外**至少有一处自己的 \ref。这是比第 1 节更强的判据。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Fig 3 (`fig:ideal-rect`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 4 (`fig:ideal-wedge`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 5 (`fig:res-128`) 有独立正文引用 | figure 环境外 4 处 | PASS |
| Fig 6 (`fig:res-256`) 有独立正文引用 | figure 环境外 2 处 | PASS |
| Fig 7 (`fig:res-512`) 有独立正文引用 | figure 环境外 2 处 | PASS |
| Fig 8 (`fig:res-rect-100`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 9 (`fig:res-wedge-100`) 有独立正文引用 | figure 环境外 3 处 | PASS |
| Fig 10 (`fig:dl-cmp-rect`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 11 (`fig:dl-cmp-wedge`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 12 (`fig:dl-abl-rect`) 有独立正文引用 | figure 环境外 2 处 | PASS |
| Fig 13 (`fig:dl-abl-wedge`) 有独立正文引用 | figure 环境外 2 处 | PASS |
| Fig 14 (`fig:perf-rect`) 有独立正文引用 | figure 环境外 2 处 | PASS |
| Fig 15 (`fig:perf-wedge`) 有独立正文引用 | figure 环境外 2 处 | PASS |
| Fig 16 (`fig:abl-rect`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 17 (`fig:abl-wedge`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 18 (`fig:mesh-rect`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 19 (`fig:mesh-wedge`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 20 (`fig:gen-split`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 21 (`fig:gen-grid`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 22 (`fig:gen-grid-wedge`) 有独立正文引用 | figure 环境外 1 处 | PASS |
| Fig 23 (`fig:perf`) 有独立正文引用 | figure 环境外 2 处 | PASS |
| 全部 21 张图均有独立正文引用 | 全部合规 | PASS |

## 4. 编号与预期一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| `fig:ideal-rect` 编号 = 3 | aux `3` / 预期 `3` | PASS |
| `fig:ideal-wedge` 编号 = 4 | aux `4` / 预期 `4` | PASS |
| `fig:res-128` 编号 = 5 | aux `5` / 预期 `5` | PASS |
| `fig:res-256` 编号 = 6 | aux `6` / 预期 `6` | PASS |
| `fig:res-512` 编号 = 7 | aux `7` / 预期 `7` | PASS |
| `fig:res-rect-100` 编号 = 8 | aux `8` / 预期 `8` | PASS |
| `fig:res-wedge-100` 编号 = 9 | aux `9` / 预期 `9` | PASS |
| `fig:dl-cmp-rect` 编号 = 10 | aux `10` / 预期 `10` | PASS |
| `fig:dl-cmp-wedge` 编号 = 11 | aux `11` / 预期 `11` | PASS |
| `fig:dl-abl-rect` 编号 = 12 | aux `12` / 预期 `12` | PASS |
| `fig:dl-abl-wedge` 编号 = 13 | aux `13` / 预期 `13` | PASS |
| `fig:perf-rect` 编号 = 14 | aux `14` / 预期 `14` | PASS |
| `fig:perf-wedge` 编号 = 15 | aux `15` / 预期 `15` | PASS |
| `fig:abl-rect` 编号 = 16 | aux `16` / 预期 `16` | PASS |
| `fig:abl-wedge` 编号 = 17 | aux `17` / 预期 `17` | PASS |
| `fig:mesh-rect` 编号 = 18 | aux `18` / 预期 `18` | PASS |
| `fig:mesh-wedge` 编号 = 19 | aux `19` / 预期 `19` | PASS |
| `fig:gen-split` 编号 = 20 | aux `20` / 预期 `20` | PASS |
| `fig:gen-grid` 编号 = 21 | aux `21` / 预期 `21` | PASS |
| `fig:gen-grid-wedge` 编号 = 22 | aux `22` / 预期 `22` | PASS |
| `fig:perf` 编号 = 23 | aux `23` / 预期 `23` | PASS |

