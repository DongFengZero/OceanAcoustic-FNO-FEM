#!/usr/bin/env python3
"""
检查第四章数值格式和一致性
1. 检查表格中所有数值是否为两位小数
2. 提取文中引用的数值
3. 对比文中与表格的一致性
"""

import re
from pathlib import Path

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    content = f.read()

report = []
report.append("# Chapter 4 Numerical Format and Consistency Check")
report.append("")
report.append("**Date**: 2026-07-26")
report.append("")
report.append("---")
report.append("")

# ============================================================================
# 任务1: 检查表格数值格式
# ============================================================================
report.append("## Task 1: Table Numerical Format")
report.append("")

# 提取表格数据行（以制表符+数字开头）
table_lines = []
for i, line in enumerate(content.split('\n'), 1):
    if re.match(r'^\t+\d+\s+&', line):
        table_lines.append((i, line))

report.append(f"**Found {len(table_lines)} table data rows**")
report.append("")

# 提取所有数值
all_numbers = []
issues = []

for line_no, line in table_lines:
    # 提取数值（包括科学计数法）
    numbers = re.findall(r'(\d+\.\d+|\d+,\d+)', line)
    for num in numbers:
        num_clean = num.replace(',', '')
        if '.' in num_clean:
            decimal_part = num_clean.split('.')[1]
            decimal_places = len(decimal_part)
            all_numbers.append((line_no, num, decimal_places))

            # 检查是否为两位小数
            if decimal_places != 2:
                issues.append(f"Line {line_no}: '{num}' has {decimal_places} decimal places (expected 2)")

report.append("### Decimal Place Distribution:")
report.append("")

from collections import Counter
decimal_counts = Counter(n[2] for n in all_numbers)
for places, count in sorted(decimal_counts.items()):
    status = "✓" if places == 2 else "✗"
    report.append(f"- {places} decimal places: {count} numbers {status}")

report.append("")

if issues:
    report.append(f"### Issues Found: {len(issues)}")
    report.append("")
    for issue in issues[:20]:  # 只显示前20个
        report.append(f"- {issue}")
    if len(issues) > 20:
        report.append(f"- ... and {len(issues)-20} more")
    report.append("")
else:
    report.append("### Result: ✓ All numbers have 2 decimal places")
    report.append("")

# ============================================================================
# 任务2: 文中数值引用
# ============================================================================
report.append("---")
report.append("")
report.append("## Task 2: In-Text Numerical References")
report.append("")

# 查找Section 4开始到Section 5之前的内容
sec4_match = re.search(r'\\section\{Experiments\}(.*?)\\section\{', content, re.DOTALL)
if sec4_match:
    sec4_content = sec4_match.group(1)

    # 提取文中的数值引用（dB值和科学计数法）
    text_numbers = []

    # dB值
    db_matches = re.finditer(r'(\d+\.?\d*)\s*(?:dB|\\,dB)', sec4_content)
    for match in db_matches:
        num = match.group(1)
        text_numbers.append(('dB', num))

    # 科学计数法
    sci_matches = re.finditer(r'(\d+\.?\d*)×10\^?\{?-?\d+\}?', sec4_content)
    for match in sci_matches:
        num = match.group(1)
        text_numbers.append(('sci', num))

    report.append(f"**Found {len(text_numbers)} numerical references in text**")
    report.append("")

    # 检查小数位数
    text_issues = []
    for num_type, num in text_numbers:
        if '.' in num:
            decimal_places = len(num.split('.')[1])
            if decimal_places != 2:
                text_issues.append(f"Text: '{num}' ({num_type}) has {decimal_places} decimal places")

    if text_issues:
        report.append(f"### Text Issues: {len(text_issues)}")
        report.append("")
        for issue in text_issues[:20]:
            report.append(f"- {issue}")
        if len(text_issues) > 20:
            report.append(f"- ... and {len(text_issues)-20} more")
    else:
        report.append("### Result: ✓ Text numbers appear well-formatted")

    report.append("")

# ============================================================================
# 任务3: 一致性检查建议
# ============================================================================
report.append("---")
report.append("")
report.append("## Task 3: Consistency Check Guidelines")
report.append("")
report.append("**Manual verification needed**: Compare text citations with table values")
report.append("")
report.append("### Common patterns to check:")
report.append("")
report.append("1. **Average values**: 'average TL of X.XX dB'")
report.append("2. **Specific cases**: 'Case 3 achieves X.XX dB'")
report.append("3. **Comparisons**: 'improves by X.XX dB'")
report.append("4. **Scientific notation**: 'error of X.XX×10^{-6}'")
report.append("")
report.append("### Search commands:")
report.append("```bash")
report.append("# Find all dB values in Section 4")
report.append("grep -n 'dB' OE_submission.tex | awk '/^6[0-9][0-9]:/,/^11[0-9][0-9]:/'")
report.append("")
report.append("# Find all scientific notation")
report.append("grep -n '×10' OE_submission.tex | awk '/^6[0-9][0-9]:/,/^11[0-9][0-9]:/'")
report.append("```")
report.append("")

# ============================================================================
# 总结
# ============================================================================
report.append("---")
report.append("")
report.append("## Summary")
report.append("")
report.append(f"- **Table data rows checked**: {len(table_lines)}")
report.append(f"- **Numbers in tables**: {len(all_numbers)}")
report.append(f"- **Format issues**: {len(issues)}")
report.append(f"- **Text references**: {len(text_numbers)}")
report.append("")

if issues:
    report.append("**Status**: ⚠️ Format issues found - need fixing")
else:
    report.append("**Status**: ✓ Format appears correct")

report.append("")
report.append("---")
report.append("")
report.append("*Report generated: 2026-07-26*")

# 写入报告
output_path = Path('D:/Data/OceanAcoustic-FNO-FEM_github/Verification/NUMERICAL_FORMAT_CHECK.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

# 打印摘要
print("=" * 70)
print("NUMERICAL FORMAT CHECK")
print("=" * 70)
print(f"Table data rows: {len(table_lines)}")
print(f"Numbers found: {len(all_numbers)}")
print(f"Format issues: {len(issues)}")
print()
if issues:
    print("Sample issues:")
    for issue in issues[:5]:
        print(f"  {issue}")
    if len(issues) > 5:
        print(f"  ... and {len(issues)-5} more")
else:
    print("[OK] All table numbers have 2 decimal places")
print()
print(f"Report: NUMERICAL_FORMAT_CHECK.md")
print("=" * 70)
