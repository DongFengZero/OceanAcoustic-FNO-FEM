#  — Tables 13–16 等宽版式一致性

- 对象：``（）
- 结论：**PASS** — 23 通过 / 0 失败 / 0 警告，共 23 项
- 脚本：`ch4_validation/scripts/T13_16_layout.py`
- 生成：2026-07-29 00:26:16

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 四张表所在 table* 环境 |

## 1. 四张表可定位

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 13 (tab:perf-rect) 环境存在 | 长度 1554 | PASS |
| Table 14 (tab:perf-wedge) 环境存在 | 长度 1550 | PASS |
| Table 15 (tab:abl-rect) 环境存在 | 长度 1520 | PASS |
| Table 16 (tab:abl-wedge) 环境存在 | 长度 1519 | PASS |

## 2. 样式宏正确性

> Tables 13/14 用 \TABstylePerf，Tables 15/16 用 \TABstylePerfTight

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 13 使用 `\TABstylePerf` | 存在 | PASS |
| Table 14 使用 `\TABstylePerf` | 存在 | PASS |
| Table 15 使用 `\TABstylePerfTight` | 存在 | PASS |
| Table 16 使用 `\TABstylePerfTight` | 存在 | PASS |

## 3. tabular preamble 一致性

> 四张表都是 12 列（No. + Method/Variant + 10 个数值），preamble 应为 `cl*{10}{c}` 或等价形式

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 13 preamble 可提取 | `@{\extracolsep{\fill` | PASS |
| Table 14 preamble 可提取 | `@{\extracolsep{\fill` | PASS |
| Table 15 preamble 可提取 | `@{\extracolsep{\fill` | PASS |
| Table 16 preamble 可提取 | `@{\extracolsep{\fill` | PASS |
| Table 14 preamble 与 Table 13 一致 | Table 14: `@{\extracolsep{\fill` / Table 13: `@{\extracolsep{\fill` | PASS |
| Table 15 preamble 与 Table 13 一致 | Table 15: `@{\extracolsep{\fill` / Table 13: `@{\extracolsep{\fill` | PASS |
| Table 16 preamble 与 Table 13 一致 | Table 16: `@{\extracolsep{\fill` / Table 13: `@{\extracolsep{\fill` | PASS |

## 4. 列数验证

> ncol=12 提取数据行，确认四张表都能提取到正确行数

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 13 数据行数 = 5 | 实得 5 | PASS |
| Table 14 数据行数 = 5 | 实得 5 | PASS |
| Table 15 数据行数 = 4 | 实得 4 | PASS |
| Table 16 数据行数 = 4 | 实得 4 | PASS |

## 5. 表头第二列标题一致性

> Tables 13/14 第二列应为 'Method'，Tables 15/16 应为 'Variant'

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| Table 13 第二列标题 = `Method` | 实得 `Method` | PASS |
| Table 14 第二列标题 = `Method` | 实得 `Method` | PASS |
| Table 15 第二列标题 = `Variant` | 实得 `Variant` | PASS |
| Table 16 第二列标题 = `Variant` | 实得 `Variant` | PASS |

