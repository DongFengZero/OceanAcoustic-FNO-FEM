#!/usr/bin/env python3
"""
恢复表格列名为简洁形式，并在4.1节添加缩写说明
Sol-MSE → Sol
TL-MAE → TL
"""

import re

# 读取文件
with open('D:/JASA/OE/els-cas-templates/OE_submission.tex', 'r', encoding='utf-8') as f:
    content = f.read()

original = content

print("=" * 70)
print("开始修改...")
print("=" * 70)

# ============================================================================
# 步骤1: 表格列名恢复简洁形式
# ============================================================================
print("\n步骤1: 恢复表格列名...")

# 恢复表格列头
replacements_table = [
    (r'& Sol-MSE & TL-MAE', r'& Sol & TL'),
    (r'& TL-MAE & Src', r'& TL & Src'),
    (r'& Sol-MSE &', r'& Sol &'),
    (r'& Sol-MSE \\\\', r'& Sol \\\\'),
    (r'& TL-MAE &', r'& TL &'),
    (r'& TL-MAE \\\\', r'& TL \\\\'),
    (r'& TL-MAE\(', r'& TL('),  # TL-MAE(dB)
]

count = 0
for pattern, replacement in replacements_table:
    matches = len(re.findall(pattern, content))
    if matches > 0:
        content = re.sub(pattern, replacement, content)
        count += matches
        print(f"  {pattern[:30]}... → {replacement[:30]}... : {matches}处")

# 但是caption中的描述保持Sol-MSE和TL-MAE，使用非表格列头的模式
# 不修改caption中的描述性文本

print(f"\n表格列头修改: {count}处")

# ============================================================================
# 步骤2: 在4.1节添加缩写说明
# ============================================================================
print("\n步骤2: 在4.1节添加缩写说明...")

# 找到评估指标段落的位置
metrics_pattern = r'(Accuracy is reported on the held-out test split with two complementary metrics.*?closely tied to sonar detection performance\.)'

metrics_match = re.search(metrics_pattern, content, re.DOTALL)

if metrics_match:
    # 在这段话后添加缩写说明
    metrics_text = metrics_match.group(1)

    # 添加缩写说明
    abbreviation_text = (
        " In the tables that follow, these metrics are abbreviated as "
        "\\emph{Sol} (for the field mean squared error in units of $10^{-6}$) "
        "and \\emph{TL} (for the transmission-loss mean absolute error in dB)."
    )

    new_text = metrics_text + abbreviation_text
    content = content.replace(metrics_text, new_text)
    print("  ✓ 已在评估指标段落后添加缩写说明")
else:
    print("  ⚠ 未找到评估指标段落，需要手动添加")

# ============================================================================
# 保存修改
# ============================================================================

if content != original:
    with open('D:/JASA/OE/els-cas-templates/OE_submission.tex', 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n" + "=" * 70)
    print("修改完成！")
    print("=" * 70)
    print(f"1. 表格列名已恢复为 Sol 和 TL")
    print(f"2. 在4.1节添加了缩写说明")
    print(f"3. Caption中保持Sol-MSE和TL-MAE全称")
    print("\n请重新编译论文验证")
else:
    print("\n未检测到需要修改的内容")
