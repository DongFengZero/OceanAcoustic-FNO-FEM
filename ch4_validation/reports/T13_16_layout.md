#  — Tables 10-11 等宽版式一致性

- 对象：``（）
- 结论：**PASS** — 16 通过 / 0 失败 / 0 警告，共 16 项
- 脚本：`ch4_validation/scripts/T13_16_layout.py`
- 生成：2026-10-04 13:24:56

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/OE_Revision_R1_Submission/OE_submission.tex` | 两张表所在 table* 环境 |

## 1. 两张表可定位

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| `tab:perf-cmp` 表体可定位 | 长度 1804 | PASS |
| `tab:perf-cmp` 用 tabular*（等宽所需） | tabular* 的宽度参数即总宽 | PASS |
| `tab:perf-cmp` 编号 = 10 | aux `10` | PASS |
| `tab:abl` 表体可定位 | 长度 1736 | PASS |
| `tab:abl` 用 tabular*（等宽所需） | tabular* 的宽度参数即总宽 | PASS |
| `tab:abl` 编号 = 11 | aux `11` | PASS |

## 2. 列数与列定义

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| `tab:perf-cmp` 列定义可解析 | `@{\extracolsep{\fill}}cl*{10}{c}@{}` | PASS |
| `tab:abl` 列定义可解析 | `@{\extracolsep{\fill}}cl*{10}{c}@{}` | PASS |
| 两表列定义相同（数值列数与列距一致） | perf-cmp=`@{\extracolsep{\fill}}cl*{10}{c}@{}` / abl=`@{\extracolsep{\fill}}cl*{10}{c}@{}` | PASS |

## 3. tabular* 宽度参数一致（左右对齐的前提）

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 两表总宽参数相同 | perf-cmp=`\linewidth` / abl=`\linewidth` | PASS |

## 4. 样式宏各自配对

> 样式宏写在 \label 与 \begin{tabular} 之间，落在表体区间之外，故从 label 前后的一段源码里读，而不是从表体里找。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| `tab:perf-cmp` 用 TABstylePerf | label 邻域内实得 ['\\TABstylePerf'] | PASS |
| `tab:abl` 用 TABstylePerfTight | label 邻域内实得 ['\\TABstylePerfTight'] | PASS |

## 5. 两表数据行数与块结构

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| `tab:perf-cmp` 有数据行 | 实得 10 行 | PASS |
| `tab:perf-cmp` 有两个几何分组小标题行 | 实得 2 个 | PASS |
| `tab:abl` 有数据行 | 实得 8 行 | PASS |
| `tab:abl` 有两个几何分组小标题行 | 实得 2 个 | PASS |

