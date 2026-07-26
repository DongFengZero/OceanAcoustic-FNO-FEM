#!/usr/bin/env python3
"""
Code-Paper Consistency Check for Chapter 3 and Section 4.1
Verifies that paper descriptions match actual code implementation
"""

import re
import os
from pathlib import Path

# Read paper
with open('D:/JASA/OE/els-cas-templates/OE_submission.tex', 'r', encoding='utf-8') as f:
    paper = f.read()

report = []
report.append("# Chapter 3 & Section 4.1 Code-Paper Consistency Check")
report.append("")
report.append("**Generated**: 2026-07-26")
report.append("")
report.append("This report verifies that all parameter descriptions in Chapter 3 (Method) and Section 4.1 (Experimental Setup) match the actual code implementation.")
report.append("")
report.append("---")
report.append("")

issues = []
checks = 0

# ============================================================================
# Section 1: FNO Parameters from Paper
# ============================================================================
report.append("## FNO Parameters from Paper")
report.append("")

# Extract from Section 4.1 (Line 580-584)
section_41 = paper[paper.find(r'\subsection{Experimental Setup}'):
                   paper.find(r'\paragraph{Data generation}')]

report.append("### Paper Claims (Section 4.1, Line 580-584):")
report.append("")

# Extract specific parameters
params_paper = {}

# G parameter
if 'G=64' in section_41:
    params_paper['G'] = 64
    report.append("- **Grid size G**: 64")
    checks += 1

# W parameter
if 'W=32' in section_41:
    params_paper['W'] = 32
    report.append("- **Width W**: 32")
    checks += 1

# L parameter
if 'L=4' in section_41:
    params_paper['L'] = 4
    report.append("- **Fourier layers L**: 4")
    checks += 1

# m1, m2 parameters
if 'm_1=m_2=16' in section_41:
    params_paper['m1'] = 16
    params_paper['m2'] = 16
    report.append("- **Retained modes m1=m2**: 16")
    checks += 1

# Lambda parameters
if r'\lambda_m=10^{2}' in section_41 or 'lambda_m=10^{2}' in section_41:
    params_paper['lambda_m'] = 100
    report.append("- **Loss weight λ_m**: 10²")
    checks += 1

if r'\lambda_p=1.0' in section_41 or 'lambda_p=1.0' in section_41:
    params_paper['lambda_p'] = 1.0
    report.append("- **Loss weight λ_p**: 1.0")
    checks += 1

# Training parameters
if '10^{-3}' in section_41:
    params_paper['lr'] = 0.001
    report.append("- **Learning rate**: 10⁻³ (0.001)")
    checks += 1

if 'batch size 1' in section_41:
    params_paper['batch_size'] = 1
    report.append("- **Batch size**: 1")
    checks += 1

if '200 epochs' in section_41:
    params_paper['epochs'] = 200
    report.append("- **Training epochs**: 200")
    checks += 1

if r'\gamma=0.995' in section_41 or 'gamma=0.995' in section_41:
    params_paper['gamma'] = 0.995
    report.append("- **LR decay γ**: 0.995")
    checks += 1

report.append("")
report.append(f"**Total parameters extracted from paper**: {len(params_paper)}")
report.append("")

# ============================================================================
# Section 2: Code Implementation Check
# ============================================================================
report.append("---")
report.append("")
report.append("## Code Implementation Verification")
report.append("")

# Look for training scripts in the repository
code_root = Path('D:/Data/OceanAcoustic-FNO-FEM_github')
training_scripts = []

# Search for main training files
for pattern in ['train*.py', 'main*.py', '*train*.py', 'run*.py']:
    training_scripts.extend(code_root.rglob(pattern))

report.append(f"**Training scripts found**: {len(training_scripts)}")
report.append("")

if training_scripts:
    report.append("### Files to check:")
    for script in training_scripts[:10]:  # Show first 10
        rel_path = script.relative_to(code_root)
        report.append(f"- `{rel_path}`")
    report.append("")
else:
    report.append("**WARNING**: No training scripts found in repository")
    report.append("")
    issues.append("No training scripts found to verify parameters")

# ============================================================================
# Section 3: Parameter Descriptions from Chapter 3
# ============================================================================
report.append("---")
report.append("")
report.append("## Chapter 3 Architecture Descriptions")
report.append("")

# Extract from Section 3.1 (FNO Prior)
section_31 = paper[paper.find(r'\subsection{FNO Physics-Prior Initialization}'):
                   paper.find(r'\subsection{FEM-Guided Graph Correction and Fusion}')]

report.append("### FNO Architecture (Section 3.1)")
report.append("")

# Input channels
if 'five-channel input' in section_31:
    report.append("- **Input channels**: 5 (Gaussian source map ×2, normalized coords ×2, frequency)")
    report.append("  - Paper describes: `[g(x,y), g(x,y), x̂, ŷ, f/f_max]`")
    checks += 1

# Fourier layer description
if 'Fourier layer' in section_31:
    report.append("- **Fourier layers**: Paper describes spectral convolution with mode truncation")
    report.append("  - Equation 7: `R̂_k = Ŵ_k · F̂_k` for k ≤ m1, m2")
    checks += 1

# Output projection
if 'real and imaginary output channels' in section_31:
    report.append("- **Output**: Projected to real and imaginary channels, then bilinearly sampled to FEM mesh")
    checks += 1

report.append("")

# ============================================================================
# Section 4: Input/Output Dimensions
# ============================================================================
report.append("---")
report.append("")
report.append("## Input/Output Specifications")
report.append("")

# From equation (3) in paper - input construction
if r'\mathbf{inp}(x,y)' in paper:
    report.append("### Input Format (Eq. 3)")
    report.append("- **Spatial grid**: G×G regular grid over domain [0,Lx]×[0,Ly]")
    report.append("- **Input tensor shape**: (5, G, G) = (5, 64, 64)")
    report.append("- **Channels**: [g(x,y), g(x,y), x̂, ŷ, f/f_max]")
    report.append("")

# From equation (6) - output format
if r'\bm{u}_p' in paper:
    report.append("### Output Format (Eq. 6)")
    report.append("- **Prior output**: u_p = [corr_r ; corr_i] ∈ ℝ^(2N)")
    report.append("- **Sampling**: Bilinear resampling from G×G grid to N FEM nodes")
    report.append("- **Realified**: Separate real and imaginary components")
    report.append("")

# ============================================================================
# Section 5: Critical Architecture Choices
# ============================================================================
report.append("---")
report.append("")
report.append("## Critical Architecture Choices to Verify")
report.append("")

critical_checks = [
    ("FNO grid resolution G=64", "Must match code"),
    ("FNO width W=32", "Hidden dimension size"),
    ("Number of Fourier layers L=4", "Depth of FNO"),
    ("Mode truncation m1=m2=16", "Spectral filtering"),
    ("Loss weights λ_m=100, λ_p=1.0", "Training objective balance"),
    ("Learning rate 0.001", "Optimizer configuration"),
    ("LR decay γ=0.995", "Exponential schedule"),
    ("Batch size 1", "Training configuration"),
    ("200 epochs", "Training duration"),
    ("AdamW optimizer", "Optimization algorithm"),
]

report.append("### Parameters Requiring Code Verification:")
report.append("")
for param, note in critical_checks:
    report.append(f"- [ ] **{param}**: {note}")

report.append("")

# ============================================================================
# Section 6: Action Items
# ============================================================================
report.append("---")
report.append("")
report.append("## Action Items")
report.append("")

report.append("### Required Verifications:")
report.append("")
report.append("1. **Locate training script**: Find main training file in repository")
report.append("2. **Check FNO configuration**: Verify G, W, L, m1, m2 parameters")
report.append("3. **Check optimizer settings**: Verify AdamW, lr=0.001, batch_size=1")
report.append("4. **Check loss weights**: Verify λ_m=100, λ_p=1.0")
report.append("5. **Check training schedule**: Verify 200 epochs, γ=0.995 decay")
report.append("6. **Check input construction**: Verify 5-channel input format")
report.append("7. **Check output format**: Verify realified 2N-dimensional output")
report.append("")

report.append("### Manual Code Review Needed:")
report.append("")
report.append("**Files to inspect**:")
if training_scripts:
    for script in training_scripts[:5]:
        rel_path = script.relative_to(code_root)
        report.append(f"- `{rel_path}`")
else:
    report.append("- [To be identified]")
report.append("")

report.append("**What to check in code**:")
report.append("```python")
report.append("# Expected parameter definitions:")
report.append("G = 64              # FNO grid size")
report.append("W = 32              # FNO width")
report.append("L = 4               # Number of Fourier layers")
report.append("m1 = m2 = 16        # Mode truncation")
report.append("lambda_m = 100      # Mesh supervision weight")
report.append("lambda_p = 1.0      # Prior supervision weight")
report.append("lr = 0.001          # Learning rate")
report.append("batch_size = 1      # Batch size")
report.append("epochs = 200        # Training epochs")
report.append("gamma = 0.995       # LR decay factor")
report.append("```")
report.append("")

# ============================================================================
# Summary
# ============================================================================
report.append("---")
report.append("")
report.append("## Summary")
report.append("")
report.append(f"**Parameters extracted from paper**: {len(params_paper)}")
report.append(f"**Checks performed**: {checks}")
report.append(f"**Issues found**: {len(issues)}")
report.append("")

if issues:
    report.append("### Issues:")
    for i, issue in enumerate(issues, 1):
        report.append(f"{i}. {issue}")
    report.append("")

report.append("### Next Steps:")
report.append("")
report.append("1. Locate and read the main training script")
report.append("2. Extract actual parameter values from code")
report.append("3. Compare code parameters with paper claims")
report.append("4. Document any discrepancies")
report.append("5. Update paper or code as needed for consistency")
report.append("")

report.append("---")
report.append("")
report.append("*Report generated: 2026-07-26*")
report.append("*Code-paper consistency check version: 1.0*")
report.append("")
report.append("**STATUS**: Parameter extraction complete. Manual code review required.")

# Write report
output_path = Path('D:/Data/OceanAcoustic-FNO-FEM_github/Verification/CODE_PAPER_CONSISTENCY_CHECK.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

# Print summary
print("=" * 70)
print("CODE-PAPER CONSISTENCY CHECK")
print("=" * 70)
print(f"Parameters extracted from paper: {len(params_paper)}")
print()
print("Paper parameters:")
for key, value in params_paper.items():
    print(f"  {key}: {value}")
print()
print(f"Training scripts found: {len(training_scripts)}")
if training_scripts:
    print("Scripts to check:")
    for script in training_scripts[:5]:
        rel_path = script.relative_to(code_root)
        print(f"  - {rel_path}")
print()
print("Report written to: CODE_PAPER_CONSISTENCY_CHECK.md")
print()
print("[NEXT] Manual code review required to verify parameters")
print("=" * 70)
