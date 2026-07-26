#!/usr/bin/env python3
"""
检查第四章数值格式 - 要求3位小数
找出所有不是3位小数的数值并生成修正建议
"""

import re
from pathlib import Path

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

report = []
report.append("# Chapter 4 - 3 Decimal Places Verification")
report.append("")
report.append("**Requirement**: All numerical data in tables should have 3 decimal places")
report.append("")
report.append("---")
report.append("")

# 查找第四章表格数据行
issues_2dp = []  # 2位小数需要补0
issues_1dp = []  # 1位小数需要补00
issues_0dp = []  # 整数需要补.000

for i, line in enumerate(lines, 1):
    # 表格数据行（以制表符+数字开头）
    if re.match(r'^\t+\d+\s+&', line):
        # 提取所有数值
        numbers = re.findall(r'(\d+\.\d+)', line)

        for num in numbers:
            decimal_part = num.split('.')[1]
            decimal_places = len(decimal_part)

            if decimal_places == 2:
                # 2位小数，需要补1个0
                new_num = num + '0'
                issues_2dp.append({
                    'line': i,
                    'old': num,
                    'new': new_num,
                    'full_line': line.strip()
                })
            elif decimal_places == 1:
                # 1位小数，需要补2个0
                new_num = num + '00'
                issues_1dp.append({
                    'line': i,
                    'old': num,
                    'new': new_num,
                    'full_line': line.strip()
                })

        # 检查整数（没有小数点）
        integers = re.findall(r'&\s+(\d+)\s+&', line)
        for num in integers:
            if num not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(num) < 4:  # 排除行号
                new_num = num + '.000'
                issues_0dp.append({
                    'line': i,
                    'old': num,
                    'new': new_num,
                    'full_line': line.strip()
                })

report.append("## Issues Found")
report.append("")
report.append(f"- **2 decimal places**: {len(issues_2dp)} (need to add 0)")
report.append(f"- **1 decimal place**: {len(issues_1dp)} (need to add 00)")
report.append(f"- **Integers**: {len(issues_0dp)} (need to add .000)")
report.append(f"- **Total**: {len(issues_2dp) + len(issues_1dp) + len(issues_0dp)}")
report.append("")

# 详细列表
if issues_2dp:
    report.append("---")
    report.append("")
    report.append("### 2 Decimal Places (add 0)")
    report.append("")
    for issue in issues_2dp[:30]:
        report.append(f"- Line {issue['line']}: `{issue['old']}` → `{issue['new']}`")
    if len(issues_2dp) > 30:
        report.append(f"- ... and {len(issues_2dp)-30} more")
    report.append("")

if issues_1dp:
    report.append("---")
    report.append("")
    report.append("### 1 Decimal Place (add 00)")
    report.append("")
    for issue in issues_1dp[:20]:
        report.append(f"- Line {issue['line']}: `{issue['old']}` → `{issue['new']}`")
    if len(issues_1dp) > 20:
        report.append(f"- ... and {len(issues_1dp)-20} more")
    report.append("")

if issues_0dp:
    report.append("---")
    report.append("")
    report.append("### Integers (add .000)")
    report.append("")
    for issue in issues_0dp[:20]:
        report.append(f"- Line {issue['line']}: `{issue['old']}` → `{issue['new']}`")
    if len(issues_0dp) > 20:
        report.append(f"- ... and {len(issues_0dp)-20} more")
    report.append("")

# 生成修正脚本
report.append("---")
report.append("")
report.append("## Auto-Fix Script")
report.append("")
report.append("Use the following Python script to automatically fix all issues:")
report.append("")
report.append("```python")
report.append("import re")
report.append("")
report.append("with open('OE_submission.tex', 'r', encoding='utf-8') as f:")
report.append("    content = f.read()")
report.append("")
report.append("# Fix 2 decimal places by adding 0")
for issue in issues_2dp[:5]:
    old = issue['old'].replace('.', r'\.')
    new = issue['new']
    report.append(f"content = re.sub(r'\\b{old}\\b', '{new}', content)")
report.append("# ... (continue for all)")
report.append("")
report.append("with open('OE_submission.tex', 'w', encoding='utf-8') as f:")
report.append("    f.write(content)")
report.append("```")
report.append("")

# 写入报告
output_path = Path('D:/Data/OceanAcoustic-FNO-FEM_github/Verification/THREE_DECIMAL_CHECK.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

# 打印摘要
print("=" * 70)
print("THREE DECIMAL PLACES CHECK")
print("=" * 70)
print(f"2 decimal places: {len(issues_2dp)}")
print(f"1 decimal place: {len(issues_1dp)}")
print(f"Integers: {len(issues_0dp)}")
print(f"Total issues: {len(issues_2dp) + len(issues_1dp) + len(issues_0dp)}")
print()
if len(issues_2dp) + len(issues_1dp) + len(issues_0dp) > 0:
    print("Sample issues:")
    for issue in (issues_2dp + issues_1dp + issues_0dp)[:5]:
        print(f"  Line {issue['line']}: {issue['old']} -> {issue['new']}")
print()
print("Report: THREE_DECIMAL_CHECK.md")
print("=" * 70)
