#!/usr/bin/env python3
"""
检查第四章所有表格：同一列的小数位数必须一致
"""

import re
from pathlib import Path
from collections import defaultdict, Counter

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 查找表格并按列统计
tables_data = {}
current_table = None
current_table_rows = []
in_chapter4 = False

for i, line in enumerate(lines, 1):
    # 检测第四章
    if r'\section{Experiments}' in line:
        in_chapter4 = True
    elif r'\section{' in line and in_chapter4:
        break

    if not in_chapter4:
        continue

    # 检测表格标签
    if r'\label{tab:' in line:
        # 保存前一个表格
        if current_table and current_table_rows:
            tables_data[current_table] = current_table_rows

        match = re.search(r'\\label\{(tab:[^}]+)\}', line)
        if match:
            current_table = match.group(1)
            current_table_rows = []

    # 提取表格数据行
    if current_table and re.match(r'^\t+\d+\s+&', line):
        # 按 & 分割，提取每列的数值
        parts = line.split('&')
        row_numbers = []
        for part in parts:
            # 提取数值（可能有多个）
            nums = re.findall(r'\b(\d+\.\d+)\b', part)
            if nums:
                row_numbers.append(nums[0])  # 取第一个数值
            else:
                row_numbers.append(None)

        if row_numbers:
            current_table_rows.append({
                'line': i,
                'numbers': row_numbers,
                'raw': line.strip()
            })

# 保存最后一个表格
if current_table and current_table_rows:
    tables_data[current_table] = current_table_rows

# 按列检查每个表格
print("=" * 80)
print("CHAPTER 4 - COLUMN-WISE DECIMAL CONSISTENCY CHECK")
print("=" * 80)
print()

total_issues = 0

for table_name, rows in sorted(tables_data.items()):
    if not rows:
        continue

    # 确定列数（取最长的行）
    max_cols = max(len(row['numbers']) for row in rows)

    # 按列统计小数位数
    column_decimals = defaultdict(list)

    for row in rows:
        for col_idx, num in enumerate(row['numbers']):
            if num:
                decimal_places = len(num.split('.')[1]) if '.' in num else 0
                column_decimals[col_idx].append({
                    'line': row['line'],
                    'value': num,
                    'decimals': decimal_places
                })

    # 检查每列的一致性
    inconsistent_columns = []
    for col_idx, values in sorted(column_decimals.items()):
        decimal_counts = Counter(v['decimals'] for v in values)
        if len(decimal_counts) > 1:
            inconsistent_columns.append({
                'col': col_idx,
                'counts': decimal_counts,
                'samples': values[:5]
            })

    if inconsistent_columns:
        print(f"[ISSUE] {table_name}")
        print(f"   Found {len(inconsistent_columns)} inconsistent columns:")
        for col_info in inconsistent_columns:
            print(f"   Column {col_info['col']}:")
            for places, count in sorted(col_info['counts'].items()):
                print(f"      {places} decimals: {count} values")
            print(f"      Samples: {[v['value'] for v in col_info['samples'][:3]]}")
        print()
        total_issues += 1
    else:
        print(f"[OK] {table_name} - All columns consistent")

print("=" * 80)
print(f"Summary: {total_issues} tables with column inconsistencies")
print("=" * 80)
