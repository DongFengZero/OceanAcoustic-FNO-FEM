#!/usr/bin/env python3
"""
第四章格式修正后的完整验证
1. 验证所有列名已统一
2. 检查数值格式（待手动检查）
3. 检查文中数值与表格一致性
4. 验证Helmholtz修正
"""

import re
from pathlib import Path

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    content = f.read()

report = []
report.append("# Chapter 4 Format Verification Report")
report.append("")
report.append("**Date**: 2026-07-26")
report.append("**Status**: Post-modification verification")
report.append("")
report.append("---")
report.append("")

# ============================================================================
# 任务1: 验证列名统一
# ============================================================================
report.append("## Task 1: Column Name Verification")
report.append("")

# 检查是否还有未替换的
old_patterns = [
    (r'& Sol & TL(?!-MAE)', 'Sol & TL (旧格式)'),
    (r'& MAE & Src', 'MAE & Src (旧格式)'),
    (r'\\bSol error\\b', 'Sol error'),
    (r'\\bSol\\s+error\\b', 'Sol error (空格)'),
]

issues_found = 0
for pattern, desc in old_patterns:
    matches = re.findall(pattern, content)
    if matches:
        report.append(f"- ❌ **{desc}**: 发现 {len(matches)} 处")
        issues_found += len(matches)
    else:
        report.append(f"- ✅ **{desc}**: 无残留")

report.append("")
if issues_found == 0:
    report.append("**结论**: ✅ 所有列名已统一为 Sol-MSE 和 TL-MAE")
else:
    report.append(f"**结论**: ❌ 发现 {issues_found} 处未替换")

report.append("")

# 统计新格式
new_patterns = [
    (r'Sol-MSE', 'Sol-MSE出现次数'),
    (r'TL-MAE', 'TL-MAE出现次数'),
]

report.append("### 新格式统计:")
report.append("")
for pattern, desc in new_patterns:
    count = len(re.findall(pattern, content))
    report.append(f"- **{desc}**: {count} 次")

report.append("")

# ============================================================================
# 任务2: 数值格式检查（需手动）
# ============================================================================
report.append("---")
report.append("")
report.append("## Task 2: Numerical Format Check")
report.append("")
report.append("**要求**: 所有TL-MAE和Sol-MSE数值保留两位小数")
report.append("")

# 提取所有可能的数值
numeric_patterns = [
    (r'(\d+\.\d+)\s*dB', 'dB值'),
    (r'(\d+\.\d+)×10', '科学计数法'),
]

report.append("### 待检查项目:")
report.append("")
report.append("1. **表格中的数值**: 需要逐表检查")
report.append("   - TL-MAE列: 保留两位小数（如 0.95, 1.23）")
report.append("   - Sol-MSE列: 保留两位小数（如 1.69, 2.94）")
report.append("")
report.append("2. **文中引用的数值**: 与表格保持一致")
report.append("   - 示例: '0.95 dB'而不是'0.9 dB'")
report.append("   - 示例: '1.69×10^{-6}'而不是'1.7×10^{-6}'")
report.append("")

# 查找文中的数值实例
sample_values = re.findall(r'(\d+\.\d{1,3})\s*(?:dB|×10)', content)
if sample_values:
    report.append("### 文中数值示例（前10个）:")
    report.append("")
    for val in sample_values[:10]:
        decimal_places = len(val.split('.')[1]) if '.' in val else 0
        status = "✓" if decimal_places == 2 else f"⚠ ({decimal_places}位)"
        report.append(f"- {val} {status}")
    report.append("")

# ============================================================================
# 任务3: 文中数值与表格一致性
# ============================================================================
report.append("---")
report.append("")
report.append("## Task 3: Text-Table Consistency")
report.append("")
report.append("**关键检查点**: 文中段落引用的数值必须与表格完全一致")
report.append("")

# 查找文中明确引用数值的句子
report.append("### 需要核对的引用:")
report.append("")
report.append("建议手动检查以下类型的引用:")
report.append("")
report.append("1. **具体案例结果**: 如'Case 3 (R1) achieves XXX dB'")
report.append("2. **平均值**: 如'average TL-MAE of XXX dB'")
report.append("3. **比较**: 如'improves by XXX dB'")
report.append("4. **科学计数**: 如'error of XXX×10^{-6}'")
report.append("")

# ============================================================================
# 任务4: Helmholtz验证
# ============================================================================
report.append("---")
report.append("")
report.append("## Task 4: Appendix A.1 Helmholtz Verification")
report.append("")

helmholtz_pattern = r'yields a one-dimensional Helmholtz equation, for each mode'
if re.search(helmholtz_pattern, content):
    report.append("✅ **Helmholtz句子已修正**")
    report.append("")
    report.append("正确格式:")
    report.append('```')
    report.append('yields a one-dimensional Helmholtz equation, for each mode')
    report.append('```')
else:
    # 检查旧格式
    old_helmholtz = r'yields a one-dimensional Helmholtz equation for each mode,'
    if re.search(old_helmholtz, content):
        report.append("❌ **Helmholtz句子未修正**")
        report.append("")
        report.append("需要修改为:")
        report.append('```')
        report.append('yields a one-dimensional Helmholtz equation, for each mode')
        report.append('```')
    else:
        report.append("⚠ **无法定位Helmholtz句子** - 需要手动检查")

report.append("")

# ============================================================================
# 总结
# ============================================================================
report.append("---")
report.append("")
report.append("## Summary")
report.append("")

completed_tasks = []
pending_tasks = []

# 任务1
if issues_found == 0:
    completed_tasks.append("✅ 任务1: 列名统一 (Sol-MSE, TL-MAE)")
else:
    pending_tasks.append(f"❌ 任务1: 还有 {issues_found} 处列名需要修正")

# 任务2
pending_tasks.append("⚠ 任务2: 数值格式需要手动检查")

# 任务3
pending_tasks.append("⚠ 任务3: 文中数值一致性需要手动检查")

# 任务4
if re.search(helmholtz_pattern, content):
    completed_tasks.append("✅ 任务4: Helmholtz已修正")
else:
    pending_tasks.append("❌ 任务4: Helmholtz需要修正")

report.append("### 已完成:")
report.append("")
for task in completed_tasks:
    report.append(f"- {task}")

report.append("")
report.append("### 待处理:")
report.append("")
for task in pending_tasks:
    report.append(f"- {task}")

report.append("")
report.append("---")
report.append("")
report.append("## Next Steps")
report.append("")
report.append("1. **立即执行**: 重新运行数据验证脚本")
report.append("2. **手动检查**: 逐表检查数值格式（两位小数）")
report.append("3. **交叉验证**: 文中数值与表格对照")
report.append("4. **最终编译**: 确认PDF无错误")
report.append("")
report.append("---")
report.append("")
report.append("*Report generated: 2026-07-26*")
report.append("*Verification version: Post-modification*")

# 写入报告
output_path = Path('D:/Data/OceanAcoustic-FNO-FEM_github/Verification/CHAPTER4_FORMAT_VERIFICATION.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print("=" * 70)
print("CHAPTER 4 FORMAT VERIFICATION")
print("=" * 70)
print(f"Column name issues: {issues_found}")
print(f"Completed tasks: {len(completed_tasks)}")
print(f"Pending tasks: {len(pending_tasks)}")
print()
print("Report: CHAPTER4_FORMAT_VERIFICATION.md")
print("=" * 70)
