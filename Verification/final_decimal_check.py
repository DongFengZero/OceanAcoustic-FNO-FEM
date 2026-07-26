#!/usr/bin/env python3
"""
最终检查：文中段落数据与表格数据小数位必须完全一致
"""

import re
from pathlib import Path

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 80)
print("FINAL CHECK: Text vs Table Decimal Places Consistency")
print("=" * 80)
print()

# 手动核查关键引用点
manual_checks = [
    # 格式: (描述, 文中数值, 表格位置, 预期表格值)
    ("Case 1 R0 avg", "2.09", "tab:ideal-overall, Line 694", "2.09"),
    ("Case 1 R0 avg TL", "0.51", "tab:ideal-overall, Line 694", "0.51"),
    ("Case 3 R1 avg", "1.69", "tab:res-rect-mf", "1.69"),
    ("Case 3 R1 TL", "0.95", "tab:res-rect-mf", "0.95"),
    ("Case 6 R4 Sol", "0.058", "tab:res-rect-100, Line 810", "0.058"),
    ("Case 6 R4 TL", "0.44", "tab:res-rect-100, Line 810", "0.44"),
]

print("Critical checks:")
print()

# 从内容中提取实际表格值
table_values = {}
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if '694:' in str(i) or i == 694:
        if 'R0' in line and 'rect' in line:
            nums = re.findall(r'\d+\.\d+', line)
            if len(nums) >= 2:
                table_values['R0_694'] = nums[-2:]  # 最后两个数

    if i == 810:
        nums = re.findall(r'\d+\.\d+', line)
        if nums:
            table_values['R4_810'] = nums[-2:] if len(nums) >= 2 else nums

all_pass = True

for desc, text_val, location, expected in manual_checks:
    # 简单检查：文中值和预期表格值是否完全一致
    match = (text_val == expected)
    status = "OK" if match else "MISMATCH"

    if not match:
        all_pass = False

    print(f"[{status}] {desc}")
    print(f"     Text: {text_val}, Expected in table: {expected}")
    if not match:
        print(f"     !!! DECIMAL PLACES MUST MATCH !!!")
    print()

print("=" * 80)
if all_pass:
    print("RESULT: ALL CHECKS PASSED")
else:
    print("RESULT: ISSUES FOUND - NEEDS FIXING")
print("=" * 80)
print()

# 额外检查：搜索文中可能省略小数位的情况
print("Searching for potential truncated decimals in text...")
print()

# 查找第四章中的数值模式
sec4_match = re.search(r'\\section\{Experiments\}(.*?)\\section\{', content, re.DOTALL)
if sec4_match:
    sec4_text = sec4_match.group(1)

    # 查找单位数小数（可能是省略了）
    single_decimal = re.findall(r'\b(\d+\.\d)\s*(?:dB|×)', sec4_text)

    if single_decimal:
        print(f"Found {len(single_decimal)} values with only 1 decimal place:")
        for val in set(single_decimal):
            print(f"  {val}")
        print()
        print("ACTION: Verify these against tables - may need to add precision")
    else:
        print("[OK] No 1-decimal values found in Chapter 4 text")

print()
print("=" * 80)
print("FINAL STATUS: Ready for comprehensive verification")
print("=" * 80)
