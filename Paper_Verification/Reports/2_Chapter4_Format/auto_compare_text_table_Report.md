# Auto Compare Text Table

**Script**: auto_compare_text_table.py
**Category**: 2_Chapter4_Format
**Generated**: 2026-07-26 21:31:27
**Exit Code**: 0

---

## Output

```
================================================================================
AUTOMATIC TEXT vs TABLE COMPARISON
================================================================================

Extracted table data:

tab:ideal-overall:
  Case 1: ['0', '0.15', '40', '36', '0.13']...
  Case 2: ['0', '0.11', '63', '14', '0.07']...

tab:res-rect-mf:
  Case 3: ['1', '128', '2.48', '0.70', '0.27']...
  Case 4: ['2', '256', '3.01', '0.79', '1.10']...
  Case 5: ['3', '512', '3.95', '0.88', '6.62']...

tab:res-wedge-100:
  Case 12: ['4', '100', '10', '128', '128']...
  Case 13: ['5', '100', '11', '256', '256']...
  Case 14: ['6', '100', '12', '512', '512']...

tab:res-rect-100:
  Case 6: ['4', '100', '4', '128', '128']...
  Case 7: ['5', '100', '5', '256', '256']...
  Case 8: ['6', '100', '6', '512', '512']...

tab:abl-rect:
  Case 25: ['16.64', '1.38', '0.51', '0.60', '10.13']...
  Case 26: ['1563.1', '22.93', '479.5', '32.72', '424.6']...
  Case 27: ['10.37', '1.09', '0.58', '0.63', '19.54']...

tab:mesh-rect:
  Case 33: ['4', '1.00', '0.058', '0.44']...
  Case 34: ['7', '0.50', '0.131', '0.38']...
  Case 35: ['8', '0.25', '0.287', '0.39']...

================================================================================

KEY COMPARISONS:

Case 1 (R0) - Avg values:
  Sol: Text=2.09, Table=23 - MISMATCH
  TL:  Text=0.51, Table=54 - MISMATCH

Case 3 (R1) - Avg values:
  Sol: Text=1.69, Table=1.69 - OK
  TL:  Text=0.95, Table=0.95 - OK

Case 6 (R4) - 100Hz values:
  Sol: Text=0.058, Table=0.058 - OK
  TL:  Text=0.44, Table=0.44 - OK

================================================================================
SUMMARY: 1 mismatches found
================================================================================

DETAILED ISSUES:

Case 1 (R0) - Avg values (Line 712):
  Table: tab:ideal-overall, Case: 1
  Sol: 2.09 (text) vs 23 (table)
  TL: 0.51 (text) vs 54 (table)

================================================================================
RECOMMENDATION:
================================================================================
1. All text citations should match table values EXACTLY
2. Including decimal places (0.95 not 0.9, 0.058 not 0.06)
3. Manual review needed for all 51 citations identified
================================================================================

```

## Status

✅ **PASSED** - Script completed successfully

---
*Report generated: 2026-07-26 21:31:27*