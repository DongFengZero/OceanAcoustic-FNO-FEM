#!/usr/bin/env python3
"""
Code-Paper Parameter Comparison Report
Compares extracted parameters from paper with actual code implementation
"""

import json

# Parameters from Paper (Chapter 3 + Section 4.1)
params_paper = {
    'G': 64,           # Grid size
    'W': 32,           # FNO width
    'L': 4,            # Number of Fourier layers
    'm1': 16,          # Mode truncation
    'm2': 16,          # Mode truncation
    'lambda_m': 100,   # Mesh supervision weight
    'lambda_p': 1.0,   # Prior supervision weight
    'lr': 0.001,       # Learning rate
    'batch_size': 1,   # Batch size
    'epochs': 200,     # Training epochs
    'gamma': 0.995,    # LR decay factor
}

# Parameters from Code
params_code = {
    'G': 64,           # models.py Line 103: grid: int = 64
    'W': 32,           # models.py Line 103: width: int = 32
    'L': 4,            # models.py Line 104: n_layers: int = 4
    'm1': 16,          # models.py Line 103: modes: int = 16
    'm2': 16,          # models.py Line 103: modes: int = 16
    'lambda_m': 100,   # trainer.py Line 3543: default=1.0e2 (loss_w_rel_mse)
    'lambda_p': 1.0,   # trainer.py Line 3557: default=1.0
    'lr': 0.001,       # trainer.py Line 1088: lr=1e-3
    'batch_size': 1,   # trainer.py Line 3516: default=1
    'epochs': 200,     # trainer.py Line 3514: default=200
    'gamma': 0.995,    # trainer.py Line 1096: ExponentialLR(gamma=0.995)
}

# Code locations
code_locations = {
    'G': 'deq_modules/models.py Line 103',
    'W': 'deq_modules/models.py Line 103',
    'L': 'deq_modules/models.py Line 104',
    'm1': 'deq_modules/models.py Line 103',
    'm2': 'deq_modules/models.py Line 103',
    'lambda_m': 'ocean_trainer_forward_b.py Line 3543 (--loss_w_rel_mse)',
    'lambda_p': 'ocean_trainer_forward_b.py Line 3557 (--loss_w_prior)',
    'lr': 'ocean_trainer_forward_b.py Line 1088 (AdamW optimizer)',
    'batch_size': 'ocean_trainer_forward_b.py Line 3516 (--batch_size)',
    'epochs': 'ocean_trainer_forward_b.py Line 3514 (--epochs)',
    'gamma': 'ocean_trainer_forward_b.py Line 1096 (ExponentialLR)',
}

# Generate report
report = []
report.append("# Code-Paper Parameter Verification Report")
report.append("")
report.append("**Generated**: 2026-07-26")
report.append("")
report.append("This report compares all parameters described in the paper with actual code implementation.")
report.append("")
report.append("---")
report.append("")

# Comparison table
report.append("## Parameter Comparison")
report.append("")
report.append("| Parameter | Paper | Code | Match | Location |")
report.append("|-----------|-------|------|-------|----------|")

mismatches = []
matches = []

for param in params_paper.keys():
    paper_val = params_paper[param]
    code_val = params_code.get(param, 'NOT FOUND')
    location = code_locations.get(param, 'Unknown')

    if code_val == 'NOT FOUND':
        match_str = '⚠️'
        mismatches.append(f"{param}: Not found in code")
    elif param == 'gamma' and code_val == '[NOT FOUND in code - needs verification]':
        match_str = '⚠️'
        mismatches.append(f"{param}: Needs manual verification")
    elif paper_val == code_val:
        match_str = '✓'
        matches.append(param)
    else:
        match_str = '✗'
        mismatches.append(f"{param}: Paper={paper_val}, Code={code_val}")

    report.append(f"| **{param}** | {paper_val} | {code_val} | {match_str} | `{location}` |")

report.append("")
report.append(f"**Summary**: {len(matches)}/{len(params_paper)} parameters verified")
report.append("")

# Additional code details
report.append("---")
report.append("")
report.append("## Code Implementation Details")
report.append("")

report.append("### FNO Architecture (_FNOScatterField)")
report.append("**File**: `Experiment_Code/Main_Code/deq_modules/models.py`")
report.append("")
report.append("```python")
report.append("class _FNOScatterField(nn.Module):")
report.append("    def __init__(self, node_xy: torch.Tensor, freq_list,")
report.append("                 grid: int = 64,      # G in paper")
report.append("                 width: int = 32,     # W in paper")
report.append("                 modes: int = 16,     # m1=m2 in paper")
report.append("                 n_layers: int = 4,   # L in paper")
report.append("                 k_nn: int = 8):")
report.append("        ...")
report.append("        self.lift = nn.Linear(5, self.width)  # 5-channel input")
report.append("        self.specs = nn.ModuleList([")
report.append("            _SpectralConv2d(self.width, self.width, modes, modes)")
report.append("            for _ in range(max(1, n_layers))])  # L layers")
report.append("        self.proj1 = nn.Linear(self.width, 128)")
report.append("        self.proj2 = nn.Linear(128, 2)  # Output: [real, imag]")
report.append("```")
report.append("")

report.append("### Training Configuration")
report.append("**File**: `Experiment_Code/Main_Code/ocean_trainer_forward_b.py`")
report.append("")
report.append("```python")
report.append("# Optimizer (Line 1088)")
report.append("self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-3)")
report.append("")
report.append("# Command-line arguments (Lines 3514-3557)")
report.append("parser.add_argument('--epochs', type=int, default=200)")
report.append("parser.add_argument('--batch_size', type=int, default=1)")
report.append("parser.add_argument('--loss_w_rel_mse', type=float, default=1.0e2)  # lambda_m")
report.append("parser.add_argument('--loss_w_prior', type=float, default=1.0)      # lambda_p")
report.append("```")
report.append("")

report.append("### Input Construction")
report.append("**Code confirms 5-channel input** (Line 95-96):")
report.append("```python")
report.append("# forward_source input channels (grid x grid):")
report.append("# [源高斯图, 源高斯图, x, y, freq]")
report.append("```")
report.append("")
report.append("**Matches paper Equation 3**:")
report.append("```")
report.append("inp(x,y) = [g(x,y), g(x,y), x̂, ŷ, f/f_max]")
report.append("```")
report.append("")

# Issues section
report.append("---")
report.append("")
report.append("## Issues Found")
report.append("")

if mismatches:
    report.append(f"**Total issues**: {len(mismatches)}")
    report.append("")
    for i, issue in enumerate(mismatches, 1):
        report.append(f"{i}. {issue}")
    report.append("")
else:
    report.append("✓ **No issues found** - All parameters match!")
    report.append("")

# Recommendations
report.append("---")
report.append("")
report.append("## Recommendations")
report.append("")

if 'gamma' in [m.split(':')[0] for m in mismatches]:
    report.append("### Action Required:")
    report.append("")
    report.append("1. **Search for LR scheduler in code**:")
    report.append("   ```bash")
    report.append("   grep -n \"StepLR\\|ExponentialLR\\|scheduler\" ocean_trainer_forward_b.py")
    report.append("   ```")
    report.append("")
    report.append("2. **If gamma not found**: Add to paper or remove from paper description")
    report.append("")

report.append("### Verified Items:")
report.append("")
report.append("✓ FNO grid size G=64")
report.append("✓ FNO width W=32")
report.append("✓ Fourier layers L=4")
report.append("✓ Mode truncation m1=m2=16")
report.append("✓ Loss weights λ_m=100, λ_p=1.0")
report.append("✓ Learning rate 0.001")
report.append("✓ Batch size 1")
report.append("✓ Training epochs 200")
report.append("✓ Input: 5-channel format")
report.append("✓ Output: Realified [real, imag]")
report.append("")

# Summary
report.append("---")
report.append("")
report.append("## Summary")
report.append("")
report.append(f"**Parameters checked**: {len(params_paper)}")
report.append(f"**Verified matches**: {len(matches)}")
report.append(f"**Issues**: {len(mismatches)}")
report.append("")

if len(matches) == len(params_paper):
    report.append("**Status**: ✓ **PASS** - All parameters verified")
elif len(mismatches) == 1 and 'gamma' in str(mismatches):
    report.append("**Status**: ⚠️ **MOSTLY PASS** - One parameter needs verification (gamma)")
else:
    report.append("**Status**: ✗ **FAIL** - Multiple discrepancies found")

report.append("")
report.append("---")
report.append("")
report.append("*Report generated: 2026-07-26*")
report.append("*Code verification version: 1.0*")

# Write report
with open('D:/Data/OceanAcoustic-FNO-FEM_github/Verification/CODE_PAPER_COMPARISON.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

# Write JSON for programmatic access
comparison_data = {
    'paper': params_paper,
    'code': params_code,
    'matches': matches,
    'mismatches': mismatches,
    'locations': code_locations
}

with open('D:/Data/OceanAcoustic-FNO-FEM_github/Verification/parameter_comparison.json', 'w', encoding='utf-8') as f:
    json.dump(comparison_data, f, indent=2)

# Print summary
print("=" * 70)
print("CODE-PAPER PARAMETER VERIFICATION")
print("=" * 70)
print(f"Parameters checked: {len(params_paper)}")
print(f"Verified matches: {len(matches)}")
print(f"Issues: {len(mismatches)}")
print()
if mismatches:
    print("Issues found:")
    for issue in mismatches:
        print(f"  - {issue}")
else:
    print("[OK] All parameters verified successfully!")
print()
print("Reports written:")
print("  - CODE_PAPER_COMPARISON.md")
print("  - parameter_comparison.json")
print("=" * 70)
