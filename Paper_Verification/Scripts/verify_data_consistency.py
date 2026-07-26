#!/usr/bin/env python3
"""
验证论文中的数值与原始数据是否一致
不做任何修改，只检查和报告
"""

import re
from pathlib import Path

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    content = f.read()

report = []
report.append("# Chapter 4 Data Consistency Verification")
report.append("")
report.append("**Purpose**: Verify all numbers in paper match original data")
report.append("**Date**: 2026-07-26")
report.append("")
report.append("---")
report.append("")

# 从验证报告中已知的原始数据示例
known_data = {
    'Case 3 (R1)': {
        '25Hz': {'sol': '1.69', 'tl': '0.52'},  # 实际应该是什么
        '50Hz': {'sol': '1.47', 'tl': '0.61'},
        '75Hz': {'sol': '2.11', 'tl': '1.09'},
        '100Hz': {'sol': '3.04', 'tl': '1.49'},
    }
}

# 提取论文表格中Case 3的数据
report.append("## Sample Check: Case 3 (R1)")
report.append("")

# 查找Case 3的表格行
case3_pattern = r'3\s+&\s+R1\s+&[^\\]+\\\\'
case3_match = re.search(case3_pattern, content)

if case3_match:
    line = case3_match.group(0)
    report.append("**Found in paper**:")
    report.append(f"```")
    report.append(line.strip())
    report.append("```")
    report.append("")

    # 提取数值
    numbers = re.findall(r'\d+\.\d+', line)
    report.append(f"**Numbers extracted**: {numbers}")
    report.append("")
else:
    report.append("⚠️ Case 3 not found in paper")
    report.append("")

# 说明原始数据格式
report.append("---")
report.append("")
report.append("## Original Data Format")
report.append("")
report.append("Based on verification reports and training logs:")
report.append("")
report.append("1. **TL-MAE**: 2 decimal places (e.g., 0.52, 1.49, 12.34)")
report.append("2. **Sol error**: Scientific notation shown as plain numbers in tables")
report.append("   - Example: 1.69×10^{-6} shown as 1.69 in table")
report.append("   - 2-3 decimal places depending on magnitude")
report.append("")

report.append("---")
report.append("")
report.append("## Recommendations")
report.append("")
report.append("### Task 1: Match表格数值与原始数据")
report.append("")
report.append("需要逐案例对比:")
report.append("1. 从训练日志/JSON/Excel中提取原始数值")
report.append("2. 与论文表格对比")
report.append("3. 确认小数位数一致")
report.append("")
report.append("### Task 2: 文中引用与表格一致")
report.append("")
report.append("搜索文中所有数值引用:")
report.append("```bash")
report.append("grep -n 'dB\\|×10' OE_submission.tex | awk '/^6[0-9][0-9]:/,/^11[0-9][0-9]:/'")
report.append("```")
report.append("")
report.append("对于每个引用:")
report.append("- 找到对应表格")
report.append("- 确认数值完全一致（包括小数位数）")
report.append("")

report.append("---")
report.append("")
report.append("## 关键原则")
report.append("")
report.append("**不要补0！不要改数据！**")
report.append("")
report.append("- ✓ 如果原始数据是 0.52 → 论文写 0.52")
report.append("- ✓ 如果原始数据是 1.690 → 论文写 1.690")
report.append("- ✗ 不要为了统一格式而补0或截断")
report.append("")
report.append("**保持与原始数据完全一致！**")
report.append("")

# 写入报告
output_path = Path('D:/Data/OceanAcoustic-FNO-FEM_github/Verification/DATA_CONSISTENCY_VERIFICATION.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print("=" * 70)
print("DATA CONSISTENCY VERIFICATION")
print("=" * 70)
print("Task: Verify paper numbers match original data")
print()
print("Key principles:")
print("  - DO NOT add zeros")
print("  - DO NOT change precision")
print("  - Match original data EXACTLY")
print()
print("Report: DATA_CONSISTENCY_VERIFICATION.md")
print()
print("Next steps:")
print("  1. Compare each table with original data files")
print("  2. Check text citations match tables")
print("  3. Only fix actual discrepancies")
print("=" * 70)
