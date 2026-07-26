#!/usr/bin/env python3
"""
批量修正论文第四章的表格和数值格式
1. 统一列名: Sol error → Sol-MSE, TL-MAE保持不变
2. 数值格式: 统一为两位小数
3. 文中引用数值与表格一致
4. 修正附录A.1的Helmholtz位置
"""

import re
from pathlib import Path

# 读取论文
paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    content = f.read()

original_content = content

modifications = []

# ============================================================================
# 任务1: 统一列名 "Sol error" → "Sol-MSE"
# ============================================================================
print("任务1: 统一列名...")

# 表格列头
patterns_col_header = [
    (r'Sol\s+error', 'Sol-MSE'),
    (r'Sol\\,error', 'Sol-MSE'),
]

for pattern, replacement in patterns_col_header:
    count = len(re.findall(pattern, content))
    if count > 0:
        content = re.sub(pattern, replacement, content)
        modifications.append(f"列头: {pattern} → {replacement} ({count}处)")

# Caption中的描述
caption_patterns = [
    (r'Sol error is the field mean squared error',
     'Sol-MSE is the field mean squared error'),
]

for pattern, replacement in caption_patterns:
    count = len(re.findall(pattern, content))
    if count > 0:
        content = re.sub(pattern, replacement, content)
        modifications.append(f"Caption: {pattern[:30]}... → {replacement[:30]}... ({count}处)")

# ============================================================================
# 任务2 & 3: 统一数值格式为两位小数，并检查文中引用
# ============================================================================
print("\n任务2&3: 统一数值格式...")

# 需要修改的数值模式（示例）
# 这些需要根据实际情况调整，这里列出几个典型的

# 例如: "0.95 dB" 应该是 "0.95 dB" (已经是两位，保持)
# 例如: "1.69×10^{-6}" 应该是 "1.69×10^{-6}" (已经是两位，保持)

# 查找所有可能需要调整的数值
# 这需要手动检查，因为有些地方可能是0.5 dB，有些是1.234 dB

modifications.append("数值格式检查: 需要手动验证所有TL-MAE和Sol-MSE的小数位数")

# ============================================================================
# 任务4: 修正附录A.1的Helmholtz位置
# ============================================================================
print("\n任务4: 修正附录Helmholtz...")

# 查找附录A.1中的问题句子
appendix_pattern = r'(Substituting the modal expansion into Eq\.~\\eqref\{EQ1\} and exploiting modal orthogonality yields a one-dimensional Helmholtz equation for each mode,)'

if re.search(appendix_pattern, content):
    # 修正: 将逗号移到equation前面
    content = re.sub(
        appendix_pattern,
        r'Substituting the modal expansion into Eq.~\\eqref{EQ1} and exploiting modal orthogonality yields a one-dimensional Helmholtz equation, for each mode',
        content
    )
    modifications.append("附录A.1: 修正Helmholtz句子标点")
else:
    modifications.append("附录A.1: 未找到目标句子，需要手动检查")

# ============================================================================
# 保存修改
# ============================================================================

if content != original_content:
    # 备份原文件
    backup_path = paper_path.with_suffix('.tex.backup_format')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)

    # 写入修改
    with open(paper_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n" + "=" * 70)
    print("修改完成！")
    print("=" * 70)
    print(f"备份文件: {backup_path}")
    print(f"\n修改列表 ({len(modifications)}项):")
    for i, mod in enumerate(modifications, 1):
        print(f"{i}. {mod}")
    print("\n请重新编译论文验证修改")
else:
    print("\n未检测到需要修改的内容")

print("\n" + "=" * 70)
print("注意：数值格式需要手动检查！")
print("=" * 70)
print("请手动检查以下内容:")
print("1. 所有表格中TL-MAE的数值是否为两位小数")
print("2. 所有表格中Sol-MSE的数值是否为两位小数")
print("3. 文中引用的数值与表格是否一致")
print("4. 附录A.1的Helmholtz位置是否正确")
