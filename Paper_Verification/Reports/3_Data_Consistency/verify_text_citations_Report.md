# Verify Text Citations

**Script**: verify_text_citations.py
**Category**: 3_Data_Consistency
**Generated**: 2026-07-26 21:32:06
**Exit Code**: 0

---

## Output

```
================================================================================
DETAILED TEXT vs TABLE VERIFICATION
================================================================================

Found 51 numerical citations to verify

Checking each citation...

Line 676: R0 - Sol avg
  Text value: 2.0910^{-6} (2 decimals)
  Source: analytical validation
  [ACTION NEEDED] Verify against table

Line 676: W0 - Sol avg
  Text value: 3.3810^{-6} (2 decimals)
  Source: analytical validation
  [ACTION NEEDED] Verify against table

Line 676: R0/W0 - TL avg
  Text value: 0.51 (2 decimals)
  Source: analytical validation
  [ACTION NEEDED] Verify against table

Line 763: Case 3 (R1) - Sol avg
  Text value: 1.6910^{-6} (2 decimals)
  Source: forward 128m
  [ACTION NEEDED] Verify against table

Line 763: Case 9 (W1) - Sol avg
  Text value: 2.1210^{-6} (2 decimals)
  Source: forward 128m
  [ACTION NEEDED] Verify against table

Line 763: Case 3 - TL avg
  Text value: 0.95 (2 decimals)
  Source: forward 128m
  [ACTION NEEDED] Verify against table

Line 763: Case 9 - TL avg
  Text value: 0.90 (2 decimals)
  Source: forward 128m
  [ACTION NEEDED] Verify against table

Line 763: Case 6 - Sol
  Text value: 0.05810^{-6} (3 decimals)
  Source: 100Hz 128x128
  [ACTION NEEDED] Verify against table

Line 763: Case 12 - Sol
  Text value: 0.1010^{-6} (2 decimals)
  Source: 100Hz 128x128
  [ACTION NEEDED] Verify against table

Line 763: Case 6 - TL
  Text value: 0.44 (2 decimals)
  Source: 100Hz 128x128
  [ACTION NEEDED] Verify against table

Line 763: Case 12 - TL
  Text value: 0.61 (2 decimals)
  Source: 100Hz 128x128
  [ACTION NEEDED] Verify against table

Line 765: Case 3 (128m) - Sol avg
  Text value: 1.6910^{-6} (2 decimals)
  Source: scaling
  [ACTION NEEDED] Verify against table

Line 765: Case 4 (256m) - Sol avg
  Text value: 3.7710^{-6} (2 decimals)
  Source: scaling
  [ACTION NEEDED] Verify against table

Line 765: Case 5 (512m) - Sol avg
  Text value: 13.1610^{-6} (2 decimals)
  Source: scaling
  [ACTION NEEDED] Verify against table

Line 765: Case 3 - TL avg
  Text value: 0.95 (2 decimals)
  Source: scaling
  [ACTION NEEDED] Verify against table

Line 765: Case 4 - TL avg
  Text value: 1.37 (2 decimals)
  Source: scaling
  [ACTION NEEDED] Verify against table

Line 765: Case 5 - TL avg
  Text value: 2.16 (2 decimals)
  Source: scaling
  [ACTION NEEDED] Verify against table

Line 765: Case 9 - Sol avg
  Text value: 2.12 (2 decimals)
  Source: wedge scaling
  [ACTION NEEDED] Verify against table

Line 765: Case 11 - Sol avg
  Text value: 10.8010^{-6} (2 decimals)
  Source: wedge scaling
  [ACTION NEEDED] Verify against table

Line 765: Case 9 - TL avg
  Text value: 0.90 (2 decimals)
  Source: wedge scaling
  [ACTION NEEDED] Verify against table

Line 765: Case 11 - TL avg
  Text value: 1.85 (2 decimals)
  Source: wedge scaling
  [ACTION NEEDED] Verify against table

Line 858: Proposed (R1) - Sol avg
  Text value: 1.6910^{-6} (2 decimals)
  Source: baseline comp
  [ACTION NEEDED] Verify against table

Line 858: Proposed (R1) - TL avg
  Text value: 0.95 (2 decimals)
  Source: baseline comp
  [ACTION NEEDED] Verify against table

Line 858: FNO (R1) - Sol avg
  Text value: 3.7310^{-6} (2 decimals)
  Source: baseline comp
  [ACTION NEEDED] Verify against table

Line 858: FNO (R1) - TL avg
  Text value: 1.31 (2 decimals)
  Source: baseline comp
  [ACTION NEEDED] Verify against table

Line 858: Proposed (W1) - Sol avg
  Text value: 2.1210^{-6} (2 decimals)
  Source: baseline comp
  [ACTION NEEDED] Verify against table

Line 858: Proposed (W1) - TL avg
  Text value: 0.90 (2 decimals)
  Source: baseline comp
  [ACTION NEEDED] Verify against table

Line 858: FNO (W1) - Sol avg
  Text value: 3.1810^{-6} (2 decimals)
  Source: baseline comp
  [ACTION NEEDED] Verify against table

Line 858: FNO (W1) - TL avg
  Text value: 1.09 (2 decimals)
  Source: baseline comp
  [ACTION NEEDED] Verify against table

Line 858: Proposed 100Hz (W1) - TL
  Text value: 1.27 (2 decimals)
  Source: baseline comp
  [ACTION NEEDED] Verify against table

Line 1119: Full model (R1) - Sol avg
  Text value: 11.5 (1 decimals)
  Source: ablation
  [ACTION NEEDED] Verify against table

Line 1119: w/o prior (R1) - Sol avg
  Text value: 64910^{-6} (0 decimals)
  Source: ablation
  [ACTION NEEDED] Verify against table

Line 1119: Full model (W1) - Sol avg
  Text value: 21.7 (1 decimals)
  Source: ablation
  [ACTION NEEDED] Verify against table

Line 1119: w/o prior (W1) - Sol avg
  Text value: 3.010^{3}10^{-6} (1 decimals)
  Source: ablation
  [ACTION NEEDED] Verify against table

Line 1119: Full model - TL avg
  Text value: 1.9 (1 decimals)
  Source: ablation
  [ACTION NEEDED] Verify against table

Line 1119: w/o prior (R1) - TL avg
  Text value: 39 (0 decimals)
  Source: ablation
  [ACTION NEEDED] Verify against table

Line 1119: w/o prior (W1) - TL avg
  Text value: 49 (0 decimals)
  Source: ablation
  [ACTION NEEDED] Verify against table

Line 1129: R4 (=1.0) - Sol
  Text value: 0.058 (3 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1129: R8 (=0.25) - Sol
  Text value: 0.28710^{-6} (3 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1129: W4 (=1.0) - Sol
  Text value: 0.100 (3 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1129: W8 (=0.25) - Sol
  Text value: 0.32610^{-6} (3 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1129: R4 - TL
  Text value: 0.44 (2 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1129: R7 - TL
  Text value: 0.38 (2 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1129: R8 - TL
  Text value: 0.39 (2 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1129: W4 - TL
  Text value: 0.61 (2 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1129: W7 - TL
  Text value: 0.36 (2 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1129: W8 - TL
  Text value: 0.31 (2 decimals)
  Source: mesh
  [ACTION NEEDED] Verify against table

Line 1143: R9 - TL avg
  Text value: 3.6 (1 decimals)
  Source: generalization
  [ACTION NEEDED] Verify against table

Line 1143: R10 - TL avg
  Text value: 3.0 (1 decimals)
  Source: generalization
  [ACTION NEEDED] Verify against table

Line 1143: W9 - TL avg
  Text value: 4.3 (1 decimals)
  Source: generalization
  [ACTION NEEDED] Verify against table

Line 1143: W10 - TL avg
  Text value: 4.4 (1 decimals)
  Source: generalization
  [ACTION NEEDED] Verify against table

================================================================================
TOTAL: 51 citations need manual verification
================================================================================

Next steps:
1. For each citation above, locate the corresponding table
2. Check if the value matches EXACTLY (including decimal places)
3. Record any mismatches


```

## Status

✅ **PASSED** - Script completed successfully

---
*Report generated: 2026-07-26 21:32:06*