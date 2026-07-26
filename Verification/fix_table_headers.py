#!/usr/bin/env python3
"""
批量修改表格列头
Sol → Sol-MSE
TL/MAE → TL-MAE
"""

import re

# 读取文件
with open('D:/JASA/OE/els-cas-templates/OE_submission.tex', 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# 替换规则
replacements = [
    # 表格列头中的模式
    (r'& Sol & TL(?!-MAE)', r'& Sol-MSE & TL-MAE'),
    (r'& MAE & Src', r'& TL-MAE & Src'),
    # 单独的TL列（后面跟&或\\）
    (r'& TL &', r'& TL-MAE &'),
    (r'& TL \\\\', r'& TL-MAE \\\\'),
    # Sol后面直接跟&的情况
    (r'& Sol &', r'& Sol-MSE &'),
    (r'& Sol \\\\', r'& Sol-MSE \\\\'),
]

count = 0
for pattern, replacement in replacements:
    matches = len(re.findall(pattern, content))
    if matches > 0:
        content = re.sub(pattern, replacement, content)
        count += matches
        print(f"替换 {pattern[:30]}... : {matches}处")

# 保存
if content != original:
    with open('D:/JASA/OE/els-cas-templates/OE_submission.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n总共替换: {count}处")
    print("保存成功！")
else:
    print("无需修改")
