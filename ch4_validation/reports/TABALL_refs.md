# Table 1-21 — 全章表格引用完整性

- 对象：`tab:* (all)`（Table 1-21）
- 结论：**PASS** — 65 通过 / 0 失败 / 0 警告，共 65 项
- 脚本：`ch4_validation/scripts/TABALL_refs.py`
- 生成：2026-07-28 21:51:05

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 全文 |
| 编号来源 aux | `../JASA/OE/els-cas-templates/OE_submission.aux` | \newlabel 解析 |

## 1. 无孤表：每个 label 至少被引用一次

> 区间引用只写两个端点，中间各表的自身 \ref 计数为 0，故对区间内部的表以『存在覆盖它的区间』作为已引证据。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 1 (`tab:method-comparison`) 已被引用 | 正文 1 处 | PASS |
| Table 2 (`tab:method-symbols`) 已被引用 | 正文 1 处 | PASS |
| Table 3 (`tab:datasets`) 已被引用 | 正文 7 处 | PASS |
| Table 4 (`tab:ideal-overall`) 已被引用 | 正文 1 处 | PASS |
| Table 5 (`tab:ideal-depthline`) 已被引用 | 正文 1 处；环境内 2 处 | PASS |
| Table 6 (`tab:res-rect-mf`) 已被引用 | 正文 2 处 | PASS |
| Table 7 (`tab:res-rect-100`) 已被引用 | 正文 1 处 | PASS |
| Table 8 (`tab:res-wedge-100`) 已被引用 | 正文 1 处 | PASS |
| Table 9 (`tab:dl-cmp-rect`) 已被引用 | 正文 1 处 | PASS |
| Table 10 (`tab:dl-cmp-wedge`) 已被引用 | 正文 1 处 | PASS |
| Table 11 (`tab:dl-abl-rect`) 已被引用 | 正文 3 处 | PASS |
| Table 12 (`tab:dl-abl-wedge`) 已被引用 | 正文 3 处 | PASS |
| Table 13 (`tab:perf-rect`) 已被引用 | 正文 1 处 | PASS |
| Table 14 (`tab:perf-wedge`) 已被引用 | 正文 1 处 | PASS |
| Table 15 (`tab:abl-rect`) 已被引用 | 正文 1 处；环境内 1 处 | PASS |
| Table 16 (`tab:abl-wedge`) 已被引用 | 正文 1 处；环境内 1 处 | PASS |
| Table 17 (`tab:mesh-rect`) 已被引用 | 正文 1 处 | PASS |
| Table 18 (`tab:mesh-wedge`) 已被引用 | 正文 1 处 | PASS |
| Table 19 (`tab:gen-overall`) 已被引用 | 正文 1 处 | PASS |
| Table 20 (`tab:runtime`) 已被引用 | 正文 1 处 | PASS |
| Table 21 (`tab:runtime-scale`) 已被引用 | 正文 1 处 | PASS |

## 2. 无悬空引用：每个 \ref 都指向真实 label

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 \ref{tab:...} 的 label 均已注册 | 全部合规 | PASS |

## 3. 每表均有独立正文引用（不靠区间/环境内兜底）

> ★ 比第 1 节更强：要求每张表在 table/figure 环境**之外**至少有一处自己的 \ref。仅靠区间覆盖或 caption 交叉引用的表，读者在正文里读不到直接指引。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 1 (`tab:method-comparison`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 2 (`tab:method-symbols`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 3 (`tab:datasets`) 有独立正文引用 | 环境外 7 处 | PASS |
| Table 4 (`tab:ideal-overall`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 5 (`tab:ideal-depthline`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 6 (`tab:res-rect-mf`) 有独立正文引用 | 环境外 2 处 | PASS |
| Table 7 (`tab:res-rect-100`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 8 (`tab:res-wedge-100`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 9 (`tab:dl-cmp-rect`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 10 (`tab:dl-cmp-wedge`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 11 (`tab:dl-abl-rect`) 有独立正文引用 | 环境外 3 处 | PASS |
| Table 12 (`tab:dl-abl-wedge`) 有独立正文引用 | 环境外 3 处 | PASS |
| Table 13 (`tab:perf-rect`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 14 (`tab:perf-wedge`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 15 (`tab:abl-rect`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 16 (`tab:abl-wedge`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 17 (`tab:mesh-rect`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 18 (`tab:mesh-wedge`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 19 (`tab:gen-overall`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 20 (`tab:runtime`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 21 (`tab:runtime-scale`) 有独立正文引用 | 环境外 1 处 | PASS |
| 全部 21 张表均有独立正文引用 | 全部合规 | PASS |

## 4. 编号与预期一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| `tab:method-comparison` 编号 = 1 | aux `1` | PASS |
| `tab:method-symbols` 编号 = 2 | aux `2` | PASS |
| `tab:datasets` 编号 = 3 | aux `3` | PASS |
| `tab:ideal-overall` 编号 = 4 | aux `4` | PASS |
| `tab:ideal-depthline` 编号 = 5 | aux `5` | PASS |
| `tab:res-rect-mf` 编号 = 6 | aux `6` | PASS |
| `tab:res-rect-100` 编号 = 7 | aux `7` | PASS |
| `tab:res-wedge-100` 编号 = 8 | aux `8` | PASS |
| `tab:dl-cmp-rect` 编号 = 9 | aux `9` | PASS |
| `tab:dl-cmp-wedge` 编号 = 10 | aux `10` | PASS |
| `tab:dl-abl-rect` 编号 = 11 | aux `11` | PASS |
| `tab:dl-abl-wedge` 编号 = 12 | aux `12` | PASS |
| `tab:perf-rect` 编号 = 13 | aux `13` | PASS |
| `tab:perf-wedge` 编号 = 14 | aux `14` | PASS |
| `tab:abl-rect` 编号 = 15 | aux `15` | PASS |
| `tab:abl-wedge` 编号 = 16 | aux `16` | PASS |
| `tab:mesh-rect` 编号 = 17 | aux `17` | PASS |
| `tab:mesh-wedge` 编号 = 18 | aux `18` | PASS |
| `tab:gen-overall` 编号 = 19 | aux `19` | PASS |
| `tab:runtime` 编号 = 20 | aux `20` | PASS |
| `tab:runtime-scale` 编号 = 21 | aux `21` | PASS |

