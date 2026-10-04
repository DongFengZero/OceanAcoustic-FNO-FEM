# Table 1-14 — 全章表格引用完整性

- 对象：`tab:* (all)`（Table 1-14）
- 结论：**PASS** — 44 通过 / 0 失败 / 0 警告，共 44 项
- 脚本：`ch4_validation/scripts/TABALL_refs.py`
- 生成：2026-10-04 11:11:08

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | 全文 |
| 编号来源 aux | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.aux` | \newlabel 解析 |

## 1. 无孤表：每个 label 至少被引用一次

> 区间引用只写两个端点，中间各表的自身 \ref 计数为 0，故对区间内部的表以『存在覆盖它的区间』作为已引证据。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 1 (`tab:method-comparison`) 已被引用 | 正文 1 处 | PASS |
| Table 2 (`tab:method-symbols`) 已被引用 | 正文 1 处 | PASS |
| Table 3 (`tab:datasets`) 已被引用 | 正文 9 处 | PASS |
| Table 4 (`tab:ideal-overall`) 已被引用 | 正文 1 处 | PASS |
| Table 5 (`tab:ideal-depthline`) 已被引用 | 正文 1 处；环境内 1 处 | PASS |
| Table 6 (`tab:res-rect-mf`) 已被引用 | 正文 2 处 | PASS |
| Table 7 (`tab:sq100`) 已被引用 | 正文 1 处 | PASS |
| Table 8 (`tab:dl-cmp`) 已被引用 | 正文 1 处；环境内 3 处 | PASS |
| Table 9 (`tab:dl-abl`) 已被引用 | 正文 4 处 | PASS |
| Table 10 (`tab:perf-cmp`) 已被引用 | 正文 1 处 | PASS |
| Table 11 (`tab:abl`) 已被引用 | 正文 1 处 | PASS |
| Table 12 (`tab:mesh`) 已被引用 | 正文 1 处 | PASS |
| Table 13 (`tab:gen-overall`) 已被引用 | 正文 1 处 | PASS |
| Table 14 (`tab:runtime`) 已被引用 | 正文 2 处 | PASS |

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
| Table 3 (`tab:datasets`) 有独立正文引用 | 环境外 9 处 | PASS |
| Table 4 (`tab:ideal-overall`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 5 (`tab:ideal-depthline`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 6 (`tab:res-rect-mf`) 有独立正文引用 | 环境外 2 处 | PASS |
| Table 7 (`tab:sq100`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 8 (`tab:dl-cmp`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 9 (`tab:dl-abl`) 有独立正文引用 | 环境外 4 处 | PASS |
| Table 10 (`tab:perf-cmp`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 11 (`tab:abl`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 12 (`tab:mesh`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 13 (`tab:gen-overall`) 有独立正文引用 | 环境外 1 处 | PASS |
| Table 14 (`tab:runtime`) 有独立正文引用 | 环境外 2 处 | PASS |
| 全部 14 张表均有独立正文引用 | 全部合规 | PASS |

## 4. 编号与预期一致

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| `tab:method-comparison` 编号 = 1 | aux `1` | PASS |
| `tab:method-symbols` 编号 = 2 | aux `2` | PASS |
| `tab:datasets` 编号 = 3 | aux `3` | PASS |
| `tab:ideal-overall` 编号 = 4 | aux `4` | PASS |
| `tab:ideal-depthline` 编号 = 5 | aux `5` | PASS |
| `tab:res-rect-mf` 编号 = 6 | aux `6` | PASS |
| `tab:sq100` 编号 = 7 | aux `7` | PASS |
| `tab:dl-cmp` 编号 = 8 | aux `8` | PASS |
| `tab:dl-abl` 编号 = 9 | aux `9` | PASS |
| `tab:perf-cmp` 编号 = 10 | aux `10` | PASS |
| `tab:abl` 编号 = 11 | aux `11` | PASS |
| `tab:mesh` 编号 = 12 | aux `12` | PASS |
| `tab:gen-overall` 编号 = 13 | aux `13` | PASS |
| `tab:runtime` 编号 = 14 | aux `14` | PASS |

