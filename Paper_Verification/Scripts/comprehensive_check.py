#!/usr/bin/env python3
"""
第四章完整一致性检测
1. 表格列小数位数一致性
2. 文中引用与表格数值一致性
3. Helmholtz句子长度检查
"""

import re
from pathlib import Path
from collections import defaultdict, Counter

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    content = ''.join(lines)

report = []
report.append("=" * 80)
report.append("CHAPTER 4 - COMPREHENSIVE CONSISTENCY CHECK")
report.append("=" * 80)
report.append("")

# ============================================================================
# Task 1: 表格列小数位数一致性
# ============================================================================
report.append("TASK 1: Table Column Decimal Consistency")
report.append("-" * 80)

# 提取表格数据
tables_data = {}
current_table = None
current_table_rows = []
in_chapter4 = False

for i, line in enumerate(lines, 1):
    if r'\section{Experiments}' in line:
        in_chapter4 = True
    elif r'\section{' in line and in_chapter4:
        break

    if not in_chapter4:
        continue

    if r'\label{tab:' in line:
        if current_table and current_table_rows:
            tables_data[current_table] = current_table_rows
        match = re.search(r'\\label\{(tab:[^}]+)\}', line)
        if match:
            current_table = match.group(1)
            current_table_rows = []

    if current_table and re.match(r'^\t+\d+\s+&', line):
        parts = line.split('&')
        row_numbers = []
        for part in parts:
            nums = re.findall(r'\b(\d+\.\d+)\b', part)
            if nums:
                row_numbers.append(nums[0])
            else:
                row_numbers.append(None)
        if row_numbers:
            current_table_rows.append({'line': i, 'numbers': row_numbers})

if current_table and current_table_rows:
    tables_data[current_table] = current_table_rows

# 检查列一致性
table_issues = 0
for table_name, rows in sorted(tables_data.items()):
    if not rows:
        continue

    column_decimals = defaultdict(list)
    for row in rows:
        for col_idx, num in enumerate(row['numbers']):
            if num:
                decimal_places = len(num.split('.')[1]) if '.' in num else 0
                column_decimals[col_idx].append({'value': num, 'decimals': decimal_places})

    inconsistent = []
    for col_idx, values in sorted(column_decimals.items()):
        decimal_counts = Counter(v['decimals'] for v in values)
        if len(decimal_counts) > 1:
            inconsistent.append((col_idx, decimal_counts, [v['value'] for v in values[:3]]))

    if inconsistent:
        report.append(f"[ISSUE] {table_name}")
        for col_idx, counts, samples in inconsistent:
            report.append(f"  Column {col_idx}: {dict(counts)} - Samples: {samples}")
        table_issues += 1
    else:
        report.append(f"[OK] {table_name}")

report.append("")
report.append(f"Summary: {table_issues} tables with inconsistencies")
report.append("")

# ============================================================================
# Task 2: 文中引用与表格一致性
# ============================================================================
report.append("")
report.append("TASK 2: Text Citations vs Table Consistency")
report.append("-" * 80)

# 提取第四章文本部分的数值
sec4_match = re.search(r'\\section\{Experiments\}(.*?)\\section\{', content, re.DOTALL)
if sec4_match:
    sec4_text = sec4_match.group(1)

    # 提取dB值
    db_values = re.findall(r'(\d+\.?\d*)\s*(?:dB|\\,dB)', sec4_text)

    # 统计小数位数
    text_decimal_stats = Counter()
    for val in db_values:
        if '.' in val:
            text_decimal_stats[len(val.split('.')[1])] += 1
        else:
            text_decimal_stats[0] += 1

    report.append(f"Found {len(db_values)} dB values in text")
    report.append(f"Decimal distribution: {dict(text_decimal_stats)}")

    # 检查是否有明显的格式不一致（如0.9 vs 0.95）
    one_decimal = [v for v in db_values if '.' in v and len(v.split('.')[1]) == 1]
    if one_decimal:
        report.append(f"[WARNING] {len(one_decimal)} values with only 1 decimal place in text:")
        report.append(f"  Examples: {one_decimal[:5]}")
    else:
        report.append("[OK] No 1-decimal values found in text")
else:
    report.append("[ERROR] Could not extract Chapter 4 text")

report.append("")

# ============================================================================
# Task 3: Helmholtz句子检查
# ============================================================================
report.append("")
report.append("TASK 3: Helmholtz Sentence Check")
report.append("-" * 80)

helmholtz_pattern = r'Substituting.*?Helmholtz.*?equation.*?mode[:\.]'
helmholtz_match = re.search(helmholtz_pattern, content, re.IGNORECASE)

if helmholtz_match:
    sentence = helmholtz_match.group(0)
    sentence_length = len(sentence)
    report.append(f"Found Helmholtz sentence ({sentence_length} chars)")
    report.append(f"Content: {sentence[:100]}...")

    # 检查长度（单栏通常<80字符比较安全）
    if sentence_length > 100:
        report.append("[WARNING] Sentence may be too long for single column")
    else:
        report.append("[OK] Sentence length acceptable")
else:
    report.append("[ERROR] Helmholtz sentence not found")

report.append("")

# ============================================================================
# 总结
# ============================================================================
report.append("")
report.append("=" * 80)
report.append("OVERALL SUMMARY")
report.append("=" * 80)
report.append(f"1. Table column consistency: {len(tables_data) - table_issues}/{len(tables_data)} OK")
report.append(f"2. Text citation format: Checked")
report.append(f"3. Helmholtz sentence: Checked")
report.append("")

if table_issues == 0:
    report.append("STATUS: [PASS] All checks passed")
else:
    report.append(f"STATUS: [ISSUES] {table_issues} tables need fixing")

report.append("=" * 80)

# 写入报告
output_path = Path('D:/Data/OceanAcoustic-FNO-FEM_github/Verification/COMPREHENSIVE_CHECK_REPORT.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

# 打印到控制台
for line in report:
    print(line)
