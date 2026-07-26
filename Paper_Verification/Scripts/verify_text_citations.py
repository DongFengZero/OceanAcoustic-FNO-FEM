#!/usr/bin/env python3
"""
详细检查第四章文中引用的具体数值与表格是否完全一致
手动提取关键引用并验证
"""

import re
from pathlib import Path

paper_path = Path('D:/JASA/OE/els-cas-templates/OE_submission.tex')
with open(paper_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 80)
print("DETAILED TEXT vs TABLE VERIFICATION")
print("=" * 80)
print()

# 从文中提取的关键数值引用
text_citations = [
    # Line 676: Analytical validation
    {"line": 676, "text": "2.09×10^{-6}", "case": "R0", "metric": "Sol avg", "source": "analytical validation"},
    {"line": 676, "text": "3.38×10^{-6}", "case": "W0", "metric": "Sol avg", "source": "analytical validation"},
    {"line": 676, "text": "0.51", "case": "R0/W0", "metric": "TL avg", "source": "analytical validation"},

    # Line 763: Forward solving - 128m cases
    {"line": 763, "text": "1.69×10^{-6}", "case": "Case 3 (R1)", "metric": "Sol avg", "source": "forward 128m"},
    {"line": 763, "text": "2.12×10^{-6}", "case": "Case 9 (W1)", "metric": "Sol avg", "source": "forward 128m"},
    {"line": 763, "text": "0.95", "case": "Case 3", "metric": "TL avg", "source": "forward 128m"},
    {"line": 763, "text": "0.90", "case": "Case 9", "metric": "TL avg", "source": "forward 128m"},
    {"line": 763, "text": "0.058×10^{-6}", "case": "Case 6", "metric": "Sol", "source": "100Hz 128x128"},
    {"line": 763, "text": "0.10×10^{-6}", "case": "Case 12", "metric": "Sol", "source": "100Hz 128x128"},
    {"line": 763, "text": "0.44", "case": "Case 6", "metric": "TL", "source": "100Hz 128x128"},
    {"line": 763, "text": "0.61", "case": "Case 12", "metric": "TL", "source": "100Hz 128x128"},

    # Line 765: Domain scaling
    {"line": 765, "text": "1.69×10^{-6}", "case": "Case 3 (128m)", "metric": "Sol avg", "source": "scaling"},
    {"line": 765, "text": "3.77×10^{-6}", "case": "Case 4 (256m)", "metric": "Sol avg", "source": "scaling"},
    {"line": 765, "text": "13.16×10^{-6}", "case": "Case 5 (512m)", "metric": "Sol avg", "source": "scaling"},
    {"line": 765, "text": "0.95", "case": "Case 3", "metric": "TL avg", "source": "scaling"},
    {"line": 765, "text": "1.37", "case": "Case 4", "metric": "TL avg", "source": "scaling"},
    {"line": 765, "text": "2.16", "case": "Case 5", "metric": "TL avg", "source": "scaling"},
    {"line": 765, "text": "2.12", "case": "Case 9", "metric": "Sol avg", "source": "wedge scaling"},
    {"line": 765, "text": "10.80×10^{-6}", "case": "Case 11", "metric": "Sol avg", "source": "wedge scaling"},
    {"line": 765, "text": "0.90", "case": "Case 9", "metric": "TL avg", "source": "wedge scaling"},
    {"line": 765, "text": "1.85", "case": "Case 11", "metric": "TL avg", "source": "wedge scaling"},

    # Line 858: Baseline comparison
    {"line": 858, "text": "1.69×10^{-6}", "case": "Proposed (R1)", "metric": "Sol avg", "source": "baseline comp"},
    {"line": 858, "text": "0.95", "case": "Proposed (R1)", "metric": "TL avg", "source": "baseline comp"},
    {"line": 858, "text": "3.73×10^{-6}", "case": "FNO (R1)", "metric": "Sol avg", "source": "baseline comp"},
    {"line": 858, "text": "1.31", "case": "FNO (R1)", "metric": "TL avg", "source": "baseline comp"},
    {"line": 858, "text": "2.12×10^{-6}", "case": "Proposed (W1)", "metric": "Sol avg", "source": "baseline comp"},
    {"line": 858, "text": "0.90", "case": "Proposed (W1)", "metric": "TL avg", "source": "baseline comp"},
    {"line": 858, "text": "3.18×10^{-6}", "case": "FNO (W1)", "metric": "Sol avg", "source": "baseline comp"},
    {"line": 858, "text": "1.09", "case": "FNO (W1)", "metric": "TL avg", "source": "baseline comp"},
    {"line": 858, "text": "1.27", "case": "Proposed 100Hz (W1)", "metric": "TL", "source": "baseline comp"},

    # Line 1119: Ablation
    {"line": 1119, "text": "11.5", "case": "Full model (R1)", "metric": "Sol avg", "source": "ablation"},
    {"line": 1119, "text": "649×10^{-6}", "case": "w/o prior (R1)", "metric": "Sol avg", "source": "ablation"},
    {"line": 1119, "text": "21.7", "case": "Full model (W1)", "metric": "Sol avg", "source": "ablation"},
    {"line": 1119, "text": "3.0×10^{3}×10^{-6}", "case": "w/o prior (W1)", "metric": "Sol avg", "source": "ablation"},
    {"line": 1119, "text": "1.9", "case": "Full model", "metric": "TL avg", "source": "ablation"},
    {"line": 1119, "text": "39", "case": "w/o prior (R1)", "metric": "TL avg", "source": "ablation"},
    {"line": 1119, "text": "49", "case": "w/o prior (W1)", "metric": "TL avg", "source": "ablation"},

    # Line 1129: Mesh independence
    {"line": 1129, "text": "0.058", "case": "R4 (Δ=1.0)", "metric": "Sol", "source": "mesh"},
    {"line": 1129, "text": "0.287×10^{-6}", "case": "R8 (Δ=0.25)", "metric": "Sol", "source": "mesh"},
    {"line": 1129, "text": "0.100", "case": "W4 (Δ=1.0)", "metric": "Sol", "source": "mesh"},
    {"line": 1129, "text": "0.326×10^{-6}", "case": "W8 (Δ=0.25)", "metric": "Sol", "source": "mesh"},
    {"line": 1129, "text": "0.44", "case": "R4", "metric": "TL", "source": "mesh"},
    {"line": 1129, "text": "0.38", "case": "R7", "metric": "TL", "source": "mesh"},
    {"line": 1129, "text": "0.39", "case": "R8", "metric": "TL", "source": "mesh"},
    {"line": 1129, "text": "0.61", "case": "W4", "metric": "TL", "source": "mesh"},
    {"line": 1129, "text": "0.36", "case": "W7", "metric": "TL", "source": "mesh"},
    {"line": 1129, "text": "0.31", "case": "W8", "metric": "TL", "source": "mesh"},

    # Line 1143: Generalization
    {"line": 1143, "text": "3.6", "case": "R9", "metric": "TL avg", "source": "generalization"},
    {"line": 1143, "text": "3.0", "case": "R10", "metric": "TL avg", "source": "generalization"},
    {"line": 1143, "text": "4.3", "case": "W9", "metric": "TL avg", "source": "generalization"},
    {"line": 1143, "text": "4.4", "case": "W10", "metric": "TL avg", "source": "generalization"},
]

print(f"Found {len(text_citations)} numerical citations to verify")
print()
print("Checking each citation...")
print()

# 现在需要从表格中提取对应的值进行比对
# 先简单检查格式一致性
issues = []

for citation in text_citations:
    value = citation['text']
    # 提取数字部分
    num_match = re.search(r'(\d+\.?\d*)', value)
    if num_match:
        num_str = num_match.group(1)
        # 检查小数位数
        if '.' in num_str:
            decimal_places = len(num_str.split('.')[1])
            citation['decimals'] = decimal_places
        else:
            citation['decimals'] = 0

    # 标记需要人工核对的项
    print(f"Line {citation['line']}: {citation['case']} - {citation['metric']}")
    print(f"  Text value: {value} ({citation.get('decimals', 'N/A')} decimals)")
    print(f"  Source: {citation['source']}")
    print(f"  [ACTION NEEDED] Verify against table")
    print()

print("=" * 80)
print(f"TOTAL: {len(text_citations)} citations need manual verification")
print("=" * 80)
print()
print("Next steps:")
print("1. For each citation above, locate the corresponding table")
print("2. Check if the value matches EXACTLY (including decimal places)")
print("3. Record any mismatches")
print()
