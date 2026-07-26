#!/usr/bin/env python3
"""
检查第四章文中段落引用的数据与表格数据是否完全一致
包括小数位数必须完全匹配
"""

import re
from pathlib import Path
from collections import defaultdict

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print("=" * 80)
print("TEXT vs TABLE DATA CONSISTENCY CHECK")
print("=" * 80)
print()

# ============================================================================
# Step 1: 提取第四章所有表格中的数值
# ============================================================================
print("Step 1: Extracting all table data from Chapter 4...")

table_data = {}  # {table_name: {row_id: [values]}}
current_table = None
in_chapter4 = False

for i, line in enumerate(lines, 1):
    if r'\section{Experiments}' in line:
        in_chapter4 = True
    elif r'\section{' in line and in_chapter4:
        break

    if not in_chapter4:
        continue

    # 检测表格标签
    if r'\label{tab:' in line:
        match = re.search(r'\\label\{(tab:[^}]+)\}', line)
        if match:
            current_table = match.group(1)
            table_data[current_table] = {}

    # 提取表格数据行
    if current_table and re.match(r'^\t+(\d+)\s+&', line):
        row_match = re.match(r'^\t+(\d+)\s+&', line)
        if row_match:
            row_num = row_match.group(1)
            # 提取该行所有数值
            numbers = re.findall(r'\b(\d+\.?\d*)\b', line)
            # 过滤掉行号本身
            numbers = [n for n in numbers if n != row_num]
            table_data[current_table][row_num] = numbers

print(f"Found {len(table_data)} tables with data")
print()

# ============================================================================
# Step 2: 提取第四章文中所有数值引用
# ============================================================================
print("Step 2: Extracting numerical citations from text...")

# 获取第四章内容（从Experiments到下一个section）
sec4_match = re.search(r'\\section\{Experiments\}(.*?)\\section\{', content, re.DOTALL)
if not sec4_match:
    print("ERROR: Cannot find Chapter 4")
    exit(1)

sec4_text = sec4_match.group(1)

# 提取所有数值引用（带上下文）
# 模式1: X.XX dB
db_pattern = r'(\d+\.?\d*)\s*(?:dB|\\,dB)'
db_matches = []
for match in re.finditer(db_pattern, sec4_text):
    value = match.group(1)
    start = max(0, match.start() - 50)
    end = min(len(sec4_text), match.end() + 50)
    context = sec4_text[start:end].replace('\n', ' ')
    db_matches.append({
        'value': value,
        'context': context,
        'type': 'dB'
    })

# 模式2: X.XX×10^{-6}
sci_pattern = r'(\d+\.?\d*)×10\^?\{?-?\d+\}?'
sci_matches = []
for match in re.finditer(sci_pattern, sec4_text):
    value = match.group(1)
    start = max(0, match.start() - 50)
    end = min(len(sec4_text), match.end() + 50)
    context = sec4_text[start:end].replace('\n', ' ')
    sci_matches.append({
        'value': value,
        'context': context,
        'type': 'sci'
    })

print(f"Found {len(db_matches)} dB values in text")
print(f"Found {len(sci_matches)} scientific notation values in text")
print()

# ============================================================================
# Step 3: 对比分析
# ============================================================================
print("Step 3: Checking for inconsistencies...")
print()

# 收集表格中的所有数值（建立索引）
all_table_values = set()
for table_name, rows in table_data.items():
    for row_id, values in rows.items():
        all_table_values.update(values)

# 检查文中数值
issues = []

print("Checking dB values...")
for item in db_matches[:20]:  # 检查前20个
    value = item['value']

    # 检查这个值是否在表格中
    if value in all_table_values:
        print(f"[OK] {value} dB - found in tables")
    else:
        # 检查是否有相似值（可能小数位数不同）
        base_val = float(value)
        similar = [v for v in all_table_values if abs(float(v) - base_val) < 0.01]

        if similar:
            print(f"[ISSUE] {value} dB - NOT in tables, but similar values exist: {similar}")
            issues.append({
                'text_value': value,
                'table_values': similar,
                'context': item['context']
            })
        else:
            print(f"[WARNING] {value} dB - not in tables (may be calculation/average)")

print()
print("Checking scientific notation values...")
for item in sci_matches[:20]:
    value = item['value']

    if value in all_table_values:
        print(f"[OK] {value}e-6 - found in tables")
    else:
        base_val = float(value)
        similar = [v for v in all_table_values if abs(float(v) - base_val) < 0.1]

        if similar:
            print(f"[ISSUE] {value}e-6 - NOT in tables, but similar values exist: {similar}")
            issues.append({
                'text_value': value,
                'table_values': similar,
                'context': item['context']
            })

print()
print("=" * 80)
print(f"SUMMARY: Found {len(issues)} potential inconsistencies")
print("=" * 80)

if issues:
    print()
    print("DETAILED ISSUES:")
    print()
    for i, issue in enumerate(issues, 1):
        print(f"{i}. Text has: {issue['text_value']}")
        print(f"   Table has: {issue['table_values']}")
        print(f"   Context: ...{issue['context']}...")
        print()

print("=" * 80)
print("Next: Manual verification needed for each issue")
print("=" * 80)
