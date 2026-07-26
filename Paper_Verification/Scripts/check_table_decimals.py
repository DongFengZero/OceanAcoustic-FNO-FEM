#!/usr/bin/env python3
"""
详细检查第四章所有表格，按表格和列统计小数位数
"""

import re
from pathlib import Path
from collections import defaultdict

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 按表格分组统计
tables = defaultdict(lambda: {'lines': [], 'numbers': []})
current_table = None
in_chapter4 = False

for i, line in enumerate(lines, 1):
    # 检测进入第四章
    if r'\section{Experiments}' in line:
        in_chapter4 = True
    elif r'\section{' in line and in_chapter4:
        in_chapter4 = False

    if not in_chapter4:
        continue

    # 检测表格标签
    if r'\label{tab:' in line:
        match = re.search(r'\\label\{(tab:[^}]+)\}', line)
        if match:
            current_table = match.group(1)

    # 提取表格数据行
    if current_table and re.match(r'^\t+\d+\s+&', line):
        # 提取所有数值
        numbers = re.findall(r'(\d+\.\d+)', line)
        for num in numbers:
            decimal_places = len(num.split('.')[1])
            tables[current_table]['numbers'].append({
                'line': i,
                'value': num,
                'decimals': decimal_places
            })
        tables[current_table]['lines'].append(i)

# 生成报告
print("=" * 80)
print("CHAPTER 4 - DECIMAL PLACES CONSISTENCY CHECK")
print("=" * 80)
print()

total_issues = 0

for table_name in sorted(tables.keys()):
    table_data = tables[table_name]
    if not table_data['numbers']:
        continue

    # 统计每个表格的小数位数分布
    from collections import Counter
    decimal_counts = Counter(n['decimals'] for n in table_data['numbers'])

    # 检查是否一致
    if len(decimal_counts) > 1:
        print(f"❌ {table_name}")
        print(f"   Lines: {min(table_data['lines'])}-{max(table_data['lines'])}")
        print(f"   Decimal places distribution:")
        for places, count in sorted(decimal_counts.items()):
            print(f"      {places} decimals: {count} numbers")

        # 显示不一致的示例
        print(f"   Sample values:")
        samples_by_decimal = defaultdict(list)
        for n in table_data['numbers'][:20]:
            samples_by_decimal[n['decimals']].append(n['value'])
        for places, values in sorted(samples_by_decimal.items()):
            print(f"      {places} decimals: {', '.join(values[:5])}")

        total_issues += 1
        print()
    else:
        decimal_place = list(decimal_counts.keys())[0]
        print(f"✓ {table_name}")
        print(f"   All {len(table_data['numbers'])} numbers have {decimal_place} decimal places")
        print()

print("=" * 80)
print(f"Summary: {total_issues} tables with inconsistent decimal places")
print("=" * 80)
