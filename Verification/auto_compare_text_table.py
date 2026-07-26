#!/usr/bin/env python3
"""
自动对比文中数值与表格数值
直接提取表格数据并与文中引用对比
"""

import re
from pathlib import Path

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=" * 80)
print("AUTOMATIC TEXT vs TABLE COMPARISON")
print("=" * 80)
print()

# ============================================================================
# 提取关键表格的数据
# ============================================================================

tables = {
    'tab:ideal-overall': {},
    'tab:res-rect-mf': {},
    'tab:res-wedge-100': {},
    'tab:res-rect-100': {},
    'tab:abl-rect': {},
    'tab:mesh-rect': {},
}

current_table = None
for i, line in enumerate(lines, 1):
    # 检测表格标签
    if r'\label{tab:' in line:
        match = re.search(r'\\label\{(tab:[^}]+)\}', line)
        if match:
            table_name = match.group(1)
            if table_name in tables:
                current_table = table_name

    # 提取数据行
    if current_table and re.match(r'^\t+(\d+)\s+&', line):
        row_match = re.match(r'^\t+(\d+)\s+&(.+)\\\\', line)
        if row_match:
            case_num = row_match.group(1)
            data_part = row_match.group(2)
            # 提取所有数值
            numbers = re.findall(r'(\d+\.\d+|\d+)', data_part)
            tables[current_table][case_num] = {
                'line': i,
                'numbers': numbers,
                'raw': line.strip()
            }

# 显示提取的表格数据
print("Extracted table data:")
for table_name, cases in tables.items():
    if cases:
        print(f"\n{table_name}:")
        for case_num, data in list(cases.items())[:3]:  # 显示前3行
            print(f"  Case {case_num}: {data['numbers'][:5]}...")

print()
print("=" * 80)
print()

# ============================================================================
# 关键对比案例
# ============================================================================

print("KEY COMPARISONS:")
print()

comparisons = [
    {
        'name': 'Case 1 (R0) - Avg values',
        'table': 'tab:ideal-overall',
        'case': '1',
        'text_sol': '2.09',
        'text_tl': '0.51',
        'sol_col': -2,  # 倒数第二列
        'tl_col': -1,   # 最后一列
    },
    {
        'name': 'Case 3 (R1) - Avg values',
        'table': 'tab:res-rect-mf',
        'case': '3',
        'text_sol': '1.69',
        'text_tl': '0.95',
        'sol_col': -2,
        'tl_col': -1,
    },
    {
        'name': 'Case 6 (R4) - 100Hz values',
        'table': 'tab:res-rect-100',
        'case': '6',
        'text_sol': '0.058',
        'text_tl': '0.44',
        'sol_col': -2,
        'tl_col': -1,
    },
]

issues_found = []

for comp in comparisons:
    print(f"{comp['name']}:")

    table_data = tables.get(comp['table'], {})
    case_data = table_data.get(comp['case'])

    if not case_data:
        print(f"  [ERROR] Case {comp['case']} not found in {comp['table']}")
        continue

    numbers = case_data['numbers']

    # 提取对应列的值
    table_sol = numbers[comp['sol_col']] if len(numbers) > abs(comp['sol_col']) else 'N/A'
    table_tl = numbers[comp['tl_col']] if len(numbers) > abs(comp['tl_col']) else 'N/A'

    text_sol = comp['text_sol']
    text_tl = comp['text_tl']

    # 比较
    sol_match = (table_sol == text_sol)
    tl_match = (table_tl == text_tl)

    print(f"  Sol: Text={text_sol}, Table={table_sol} - {'OK' if sol_match else 'MISMATCH'}")
    print(f"  TL:  Text={text_tl}, Table={table_tl} - {'OK' if tl_match else 'MISMATCH'}")

    if not sol_match or not tl_match:
        issues_found.append({
            'name': comp['name'],
            'table': comp['table'],
            'case': comp['case'],
            'line': case_data['line'],
            'text_sol': text_sol,
            'table_sol': table_sol,
            'text_tl': text_tl,
            'table_tl': table_tl,
        })

    print()

print("=" * 80)
print(f"SUMMARY: {len(issues_found)} mismatches found")
print("=" * 80)

if issues_found:
    print()
    print("DETAILED ISSUES:")
    for issue in issues_found:
        print(f"\n{issue['name']} (Line {issue['line']}):")
        print(f"  Table: {issue['table']}, Case: {issue['case']}")
        if issue['text_sol'] != issue['table_sol']:
            print(f"  Sol: {issue['text_sol']} (text) vs {issue['table_sol']} (table)")
        if issue['text_tl'] != issue['table_tl']:
            print(f"  TL: {issue['text_tl']} (text) vs {issue['table_tl']} (table)")

print()
print("=" * 80)
print("RECOMMENDATION:")
print("=" * 80)
print("1. All text citations should match table values EXACTLY")
print("2. Including decimal places (0.95 not 0.9, 0.058 not 0.06)")
print("3. Manual review needed for all 51 citations identified")
print("=" * 80)
