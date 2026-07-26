# Chapter 4 Data Consistency Verification

**Purpose**: Verify all numbers in paper match original data
**Date**: 2026-07-26

---

## Sample Check: Case 3 (R1)

⚠️ Case 3 not found in paper

---

## Original Data Format

Based on verification reports and training logs:

1. **TL-MAE**: 2 decimal places (e.g., 0.52, 1.49, 12.34)
2. **Sol error**: Scientific notation shown as plain numbers in tables
   - Example: 1.69×10^{-6} shown as 1.69 in table
   - 2-3 decimal places depending on magnitude

---

## Recommendations

### Task 1: Match表格数值与原始数据

需要逐案例对比:
1. 从训练日志/JSON/Excel中提取原始数值
2. 与论文表格对比
3. 确认小数位数一致

### Task 2: 文中引用与表格一致

搜索文中所有数值引用:
```bash
grep -n 'dB\|×10' OE_submission.tex | awk '/^6[0-9][0-9]:/,/^11[0-9][0-9]:/'
```

对于每个引用:
- 找到对应表格
- 确认数值完全一致（包括小数位数）

---

## 关键原则

**不要补0！不要改数据！**

- ✓ 如果原始数据是 0.52 → 论文写 0.52
- ✓ 如果原始数据是 1.690 → 论文写 1.690
- ✗ 不要为了统一格式而补0或截断

**保持与原始数据完全一致！**
