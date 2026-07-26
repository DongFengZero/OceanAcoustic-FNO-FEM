#!/usr/bin/env python3
"""
自动修正第四章表格中的数值为3位小数
"""

import re
from pathlib import Path

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')

# 备份
backup_path = paper_path.with_suffix('.tex.backup_3decimal')
with open(paper_path, 'r', encoding='utf-8') as f:
    original_content = f.read()

with open(backup_path, 'w', encoding='utf-8') as f:
    f.write(original_content)

print(f"Backup created: {backup_path.name}")

# 读取所有行
lines = original_content.split('\n')
modified_lines = []
modification_count = 0

for i, line in enumerate(lines, 1):
    # 只处理表格数据行
    if re.match(r'^\t+\d+\s+&', line):
        original_line = line

        # 策略：逐个替换数值
        # 1. 找到所有2位小数，补0
        def add_zero_2dp(match):
            return match.group(0) + '0'
        line = re.sub(r'\b\d+\.\d{2}\b', add_zero_2dp, line)

        # 2. 找到所有1位小数，补00
        def add_zeros_1dp(match):
            return match.group(0) + '00'
        line = re.sub(r'\b\d+\.\d{1}\b', add_zeros_1dp, line)

        # 3. 整数处理较复杂，需要区分行号和数据
        # 暂时跳过，因为大部分表格数值应该已经有小数点

        if line != original_line:
            modification_count += 1

        modified_lines.append(line)
    else:
        modified_lines.append(line)

# 写入修改后的内容
with open(paper_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(modified_lines))

print(f"Modified {modification_count} lines")
print("Conversion complete!")
print("\nNext steps:")
print("1. Compile the paper")
print("2. Check PDF output")
print("3. If issues, restore from backup")
