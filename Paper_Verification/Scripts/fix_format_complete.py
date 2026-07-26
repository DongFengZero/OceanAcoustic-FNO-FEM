#!/usr/bin/env python3
"""
批量修正论文第四章的表格和数值格式
1. 统一列名: Sol error → Sol-MSE, TL/MAE/TL-MAE → TL-MAE
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

print("=" * 70)
print("开始批量修正...")
print("=" * 70)

# ============================================================================
# 任务1: 统一列名
# ============================================================================
print("\n任务1: 统一列名...")

# 1.1 Sol error → Sol-MSE (表格列头和caption)
patterns_sol = [
    (r'\bSol\s+error\b', 'Sol-MSE'),
    (r'\bSol\\,error\b', 'Sol-MSE'),
]

for pattern, replacement in patterns_sol:
    matches = re.findall(pattern, content)
    if matches:
        content = re.sub(pattern, replacement, content)
        modifications.append(f"  Sol error → Sol-MSE: {len(matches)}处")
        print(f"  ✓ {pattern} → {replacement}: {len(matches)}处")

# 1.2 TL/MAE → TL-MAE (避免混淆的斜杠表示)
# 需要小心处理，只替换表格相关的
patterns_tl = [
    # 表格列头中的TL/MAE
    (r'TL/MAE', 'TL-MAE'),
    # 确保TL-MAE保持不变
]

for pattern, replacement in patterns_tl:
    matches = re.findall(pattern, content)
    if matches:
        content = re.sub(pattern, replacement, content)
        modifications.append(f"  TL/MAE → TL-MAE: {len(matches)}处")
        print(f"  ✓ {pattern} → {replacement}: {len(matches)}处")

# ============================================================================
# 任务4: 修正附录A.1的Helmholtz位置
# ============================================================================
print("\n任务4: 修正附录A.1的Helmholtz句子...")

# 查找并修正
appendix_pattern = r'yields a one-dimensional Helmholtz equation for each mode,'
appendix_replacement = r'yields a one-dimensional Helmholtz equation, for each mode'

if re.search(appendix_pattern, content):
    content = re.sub(appendix_pattern, appendix_replacement, content)
    modifications.append("  附录A.1: Helmholtz逗号位置已修正")
    print("  ✓ Helmholtz句子标点已修正")
else:
    print("  ⚠ 未找到Helmholtz句子，可能已修正或需手动检查")

# ============================================================================
# 保存修改
# ============================================================================

if content != original_content:
    # 备份原文件
    backup_path = paper_path.with_suffix('.tex.backup_format2')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)

    # 写入修改
    with open(paper_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n" + "=" * 70)
    print("自动修改完成！")
    print("=" * 70)
    print(f"备份文件: {backup_path.name}")
    print(f"\n共执行 {len(modifications)} 项修改:")
    for mod in modifications:
        print(mod)
else:
    print("\n未检测到需要修改的内容")

# ============================================================================
# 输出待手动检查的项目
# ============================================================================
print("\n" + "=" * 70)
print("待手动检查的任务:")
print("=" * 70)
print("""
任务2: 检查数值格式（两位小数）
  需要手动检查所有表格，确保:
  - TL-MAE: 保留两位小数（如 0.95, 1.23, 12.34）
  - Sol-MSE: 保留两位小数（如 1.69, 2.54, 13.16）

  示例:
  ✓ 正确: 0.95 dB, 1.69×10^{-6}
  ✗ 错误: 0.9 dB, 1.7×10^{-6}, 0.950 dB

任务3: 检查文中数值与表格一致
  需要确认文中段落引用的数值与表格中的数值完全一致:
  - 小数位数相同
  - 数值精确匹配

  检查方法:
  1. 搜索文中所有提到具体数值的地方
  2. 对照相应表格验证
  3. 特别注意"平均值"、"最大值"、"最小值"等统计量

建议使用grep搜索:
  grep -n "dB\|×10" OE_submission.tex | grep -v "%"
""")

print("=" * 70)
print("下一步: 编译论文验证修改")
print("=" * 70)
