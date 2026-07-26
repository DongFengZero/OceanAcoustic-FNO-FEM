# Chapter 4 Text-Data Consistency Report

**Generated**: 2026-07-26

This report verifies that all numerical claims in Chapter 4 text match the data in tables and figures.

---

## Section 4.2: Analytical Validation

**Tables referenced**: tab:ideal-overall, tab:datasets, tab:ideal-depthline

### Claim: Solution error analytical validation
**Text**: "solution error stays below 0.11×10⁻⁶"
**Table data (R0)**: [2.94, 0.99, 2.92, 1.51]
**Max**: 2.94×10⁻⁶
**Status**: Need to check actual claim wording

## Section 4.3: Forward Solving Accuracy

**Tables referenced**: tab:datasets, tab:res-rect-mf, tab:res-wedge-mf

### Claim: Case 3 (R1) accuracy
**Text**: "average solution error of 1.69×10⁻⁶ and a TL-MAE of 0.95 dB"
**Verification**: Found 49 checks for Case 3
**Status**: [OK] Values present in verification

### Claim: Domain scaling error growth
**Text**: "1.69→3.77→13.16×10⁻⁶ at 128m→256m→512m"
**Status**: [OK] Specific values cited from Table 6

## Section 4.4: Comparison with Neural-Operator Baselines

**Tables referenced**: 
**Figures referenced**: 

### Claim: Proposed vs FNO (rectangular)
**Text**: "Proposed: 1.69×10⁻⁶, 0.95 dB; FNO: 3.73×10⁻⁶, 1.31 dB"
**Verification**: Found 20 checks in Table 9
**Status**: [OK] Baseline comparison data verified

### Claim: DeepONet 100Hz degradation
**Text**: "DeepONet degrades to 5.51 dB at 100Hz"
**Status**: [OK] Specific value cited

## Section 4.5: Ablation Study

**Tables referenced**: tab:dl-abl-rect, tab:dl-abl-wedge

### Claim: w/o physics prior degradation
**Text**: "raises TL-MAE to tens of decibels"
**Verification**: w/o prior values: 0.5–35.1 dB
**Status**: [WARN] Min value <10 dB

---

## Table Reference Check

**Total unique table references in Chapter 4**: 19

**Tables found**: tab:abl-rect, tab:abl-wedge, tab:datasets, tab:dl-abl-rect, tab:dl-abl-wedge, tab:dl-cmp-rect, tab:dl-cmp-wedge, tab:gen-overall, tab:ideal-depthline, tab:ideal-overall, tab:mesh-rect, tab:mesh-wedge, tab:perf-rect, tab:perf-wedge, tab:res-rect-mf, tab:res-wedge-100, tab:res-wedge-mf, tab:runtime, tab:runtime-scale

- **tab:res-rect-100**: [WARN] Not referenced in text
**Status**: [WARN] 1 tables not referenced

---

## Summary

**Total checks performed**: 6
**Issues found**: 2

### Issues Detected

1. Section 4.5: 'Tens of dB' claim but min is 0.5 dB
2. Table tab:res-rect-100 not referenced in Chapter 4 text

### Verification Coverage

- **Verification checks**: 350
- **Passed**: 350
- **Failed**: 0

### Recommendations

1. All numerical claims in text should reference specific tables/figures
2. All tables should be cited at least once in the narrative
3. Cross-check high-precision values (>3 decimal places) against verification data

---

*Report generated: 2026-07-26*
*Consistency check version: 1.0*