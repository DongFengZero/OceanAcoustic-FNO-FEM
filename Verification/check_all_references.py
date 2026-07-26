#!/usr/bin/env python3
"""
Complete Figure and Table Reference Check
Ensures all figures and tables are cited in text
"""

import re
import subprocess

# Read paper
with open('D:/JASA/OE/els-cas-templates/OE_submission.tex', 'r', encoding='utf-8') as f:
    paper = f.read()

report = []
report.append("# Complete Figure and Table Reference Check")
report.append("")
report.append("**Generated**: 2026-07-26")
report.append("")
report.append("This report verifies that ALL figures and tables are properly referenced in the text.")
report.append("")
report.append("---")
report.append("")

issues = []

# Extract all labels
all_figs = re.findall(r'\\label\{(fig:[^}]+)\}', paper)
all_tabs = re.findall(r'\\label\{(tab:[^}]+)\}', paper)

report.append("## Summary")
report.append("")
report.append(f"**Total figures found**: {len(all_figs)}")
report.append(f"**Total tables found**: {len(all_tabs)}")
report.append("")

# Check which are subfigures/subtables (have parent references)
subfigs = []
subtabs = []

# Strategy 1: Labels with -a, -b, -c pattern
for fig in all_figs:
    if re.match(r'fig:[^-]+-[a-z]$', fig):
        parent = re.sub(r'-[a-z]$', '', fig)
        if parent in all_figs:
            subfigs.append(fig)

# Strategy 2: Look for subfloat/subcaption near the label
for fig in all_figs:
    if fig in subfigs:
        continue
    # Find label position
    match = re.search(r'\\label\{' + re.escape(fig) + r'\}', paper)
    if match:
        # Check 500 chars before the label for subfloat or subcaption
        context_start = max(0, match.start() - 500)
        context = paper[context_start:match.start()]
        if r'\subfloat' in context or r'\subcaption' in context:
            # This is a subfigure, check if parent figure exists
            # Look ahead for parent label
            context_after = paper[match.end():match.end() + 500]
            parent_match = re.search(r'\\label\{(fig:[^}]+)\}', context_after)
            if parent_match:
                parent_label = parent_match.group(1)
                if parent_label != fig and parent_label in all_figs:
                    subfigs.append(fig)

report.append(f"**Subfigures (don't need individual references)**: {len(subfigs)}")
report.append("")

# Main figures/tables that need references
main_figs = [f for f in all_figs if f not in subfigs]
main_tabs = all_tabs  # Usually no subtables

report.append(f"**Main figures requiring references**: {len(main_figs)}")
report.append(f"**Main tables requiring references**: {len(main_tabs)}")
report.append("")

# Check references
report.append("---")
report.append("")
report.append("## Unreferenced Items")
report.append("")

unreferenced_figs = []
unreferenced_tabs = []

# Check main figures
for fig in main_figs:
    # Look for \ref{fig}, Fig.~\ref{fig}, Figs.~\ref{fig}
    pattern = r'(?:Fig(?:s|ure)?(?:s)?\.?~)?\\ref\{' + re.escape(fig) + r'\}'
    if not re.search(pattern, paper):
        unreferenced_figs.append(fig)
        issues.append(f"Figure {fig} not referenced in text")

# Check tables
for tab in main_tabs:
    pattern = r'(?:Table(?:s)?~)?\\ref\{' + re.escape(tab) + r'\}'
    if not re.search(pattern, paper):
        # Check if it's in a range reference like \ref{tab1}--\ref{tab2}
        in_range = False
        range_refs = re.findall(r'\\ref\{(tab:[^}]+)\}--\\ref\{(tab:[^}]+)\}', paper)
        for start_ref, end_ref in range_refs:
            # Simple heuristic: if tab is alphabetically between start and end
            if start_ref <= tab <= end_ref or end_ref <= tab <= start_ref:
                in_range = True
                break

        if not in_range:
            unreferenced_tabs.append(tab)
            issues.append(f"Table {tab} not referenced in text")

if unreferenced_figs:
    report.append("### Unreferenced Figures")
    report.append("")
    for fig in unreferenced_figs:
        report.append(f"- `{fig}` - [ACTION REQUIRED] Add reference in text")
    report.append("")
else:
    report.append("### Figures")
    report.append("**Status**: [OK] All main figures are referenced")
    report.append("")

if unreferenced_tabs:
    report.append("### Unreferenced Tables")
    report.append("")
    for tab in unreferenced_tabs:
        report.append(f"- `{tab}` - [ACTION REQUIRED] Add reference in text")
    report.append("")
else:
    report.append("### Tables")
    report.append("**Status**: [OK] All tables are referenced")
    report.append("")

# Detailed breakdown by chapter
report.append("---")
report.append("")
report.append("## Chapter 4 Detailed Analysis")
report.append("")

# Extract Chapter 4
ch4_start = paper.find(r'\subsection{Validation against Analytical Solutions}')
ch4_end = paper.find(r'\section{Conclusion}', ch4_start)
if ch4_end == -1:
    ch4_end = len(paper)
chapter4 = paper[ch4_start:ch4_end]

# Find all Chapter 4 figures and tables
ch4_figs = [f for f in main_figs if f in chapter4]
ch4_tabs = [t for t in main_tabs if t in chapter4]

report.append(f"**Chapter 4 figures**: {len(ch4_figs)}")
report.append(f"**Chapter 4 tables**: {len(ch4_tabs)}")
report.append("")

# Check each section
sections = [
    ('4.2', r'\subsection{Validation against Analytical Solutions}', r'\subsection{Forward Solving Accuracy}'),
    ('4.3', r'\subsection{Forward Solving Accuracy}', r'\subsection{Comparison with Neural-Operator Baselines}'),
    ('4.4', r'\subsection{Comparison with Neural-Operator Baselines}', r'\subsection{Ablation Study}'),
    ('4.5', r'\subsection{Ablation Study}', r'\subsection{Mesh Independence}'),
    ('4.6', r'\subsection{Mesh Independence}', r'\subsection{Generalization Testing}'),
    ('4.7', r'\subsection{Generalization Testing}', r'\subsection{Runtime}'),
    ('4.8', r'\subsection{Runtime}', r'\section{Conclusion}'),
]

for sec_num, start_marker, end_marker in sections:
    start = paper.find(start_marker)
    end = paper.find(end_marker, start) if end_marker else len(paper)
    if start == -1:
        continue

    section = paper[start:end]

    # Find referenced items in this section
    fig_refs = set(re.findall(r'\\ref\{(fig:[^}]+)\}', section))
    tab_refs = set(re.findall(r'\\ref\{(tab:[^}]+)\}', section))

    report.append(f"### Section {sec_num}")
    report.append(f"**Figures referenced**: {len(fig_refs)}")
    report.append(f"**Tables referenced**: {len(tab_refs)}")
    report.append("")

# Summary
report.append("---")
report.append("")
report.append("## Action Items")
report.append("")

if issues:
    report.append(f"**Total issues found**: {len(issues)}")
    report.append("")
    report.append("### Required Actions:")
    report.append("")
    for i, issue in enumerate(issues, 1):
        report.append(f"{i}. {issue}")
    report.append("")
    report.append("**All figures and tables MUST be referenced in the text according to journal requirements.**")
else:
    report.append("**Status**: [OK] All figures and tables are properly referenced")

report.append("")
report.append("---")
report.append("")
report.append("*Report generated: 2026-07-26*")
report.append("*Reference check version: 1.0*")

# Write report
with open('D:/Data/OceanAcoustic-FNO-FEM_github/Verification/FIGURE_TABLE_REFERENCE_CHECK.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

# Print summary
print("=" * 70)
print("FIGURE AND TABLE REFERENCE CHECK")
print("=" * 70)
print(f"Total figures: {len(all_figs)} ({len(main_figs)} main + {len(subfigs)} sub)")
print(f"Total tables: {len(all_tabs)}")
print()
print(f"Unreferenced figures: {len(unreferenced_figs)}")
print(f"Unreferenced tables: {len(unreferenced_tabs)}")
print()
if issues:
    print("ISSUES FOUND:")
    for issue in issues:
        print(f"  - {issue}")
    print()
    print("[ACTION REQUIRED] Add references for all unreferenced items")
else:
    print("[OK] All figures and tables are properly referenced")
print()
print("Report written to: FIGURE_TABLE_REFERENCE_CHECK.md")
print("=" * 70)
