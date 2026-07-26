================================================================================
CHAPTER 4 - COMPREHENSIVE CONSISTENCY CHECK
================================================================================

TASK 1: Table Column Decimal Consistency
--------------------------------------------------------------------------------
[OK] tab:abl-rect
[ISSUE] tab:abl-wedge
  Column 3: {2: 3, 1: 1} - Samples: ['33.35', '9691.00', '162.6']
[OK] tab:dl-abl-rect
[OK] tab:dl-abl-wedge
[OK] tab:dl-cmp-rect
[OK] tab:dl-cmp-wedge
[OK] tab:gen-overall
[OK] tab:ideal-depthline
[OK] tab:ideal-overall
[OK] tab:mesh-rect
[OK] tab:mesh-wedge
[OK] tab:perf-rect
[OK] tab:perf-wedge
[OK] tab:res-rect-100
[OK] tab:res-rect-mf
[OK] tab:res-wedge-100
[OK] tab:runtime-scale

Summary: 1 tables with inconsistencies


TASK 2: Text Citations vs Table Consistency
--------------------------------------------------------------------------------
Found 0 dB values in text
Decimal distribution: {}
[OK] No 1-decimal values found in text


TASK 3: Helmholtz Sentence Check
--------------------------------------------------------------------------------
Found Helmholtz sentence (141 chars)
Content: Substituting the modal expansion into Eq.~\eqref{EQ1} and exploiting orthogonality yields a one-dime...
[WARNING] Sentence may be too long for single column


================================================================================
OVERALL SUMMARY
================================================================================
1. Table column consistency: 16/17 OK
2. Text citation format: Checked
3. Helmholtz sentence: Checked

STATUS: [ISSUES] 1 tables need fixing
================================================================================