# Column Decimals

**Generated**: 2026-07-26 21:01:59

**Description**: Check decimal consistency in table columns

---

## Output

```
================================================================================
CHAPTER 4 - COLUMN-WISE DECIMAL CONSISTENCY CHECK
================================================================================

[ISSUE] tab:abl-rect
   Found 5 inconsistent columns:
   Column 3:
      1 decimals: 1 values
      2 decimals: 3 values
      Samples: ['16.64', '1563.1', '10.37']
   Column 5:
      1 decimals: 1 values
      2 decimals: 3 values
      Samples: ['0.51', '479.5', '0.58']
   Column 7:
      1 decimals: 1 values
      2 decimals: 3 values
      Samples: ['10.13', '424.6', '19.54']
   Column 9:
      1 decimals: 1 values
      2 decimals: 3 values
      Samples: ['18.65', '129.6', '22.92']
   Column 11:
      1 decimals: 1 values
      2 decimals: 3 values
      Samples: ['11.48', '649.2', '13.35']

[ISSUE] tab:abl-wedge
   Found 3 inconsistent columns:
   Column 3:
      1 decimals: 1 values
      2 decimals: 2 values
      Samples: ['33.35', '162.6', '57.36']
   Column 7:
      1 decimals: 1 values
      2 decimals: 3 values
      Samples: ['19.45', '685.3', '21.83']
   Column 9:
      1 decimals: 1 values
      2 decimals: 3 values
      Samples: ['33.08', '327.9', '55.65']

[OK] tab:dl-abl-rect - All columns consistent
[OK] tab:dl-abl-wedge - All columns consistent
[OK] tab:dl-cmp-rect - All columns consistent
[OK] tab:dl-cmp-wedge - All columns consistent
[OK] tab:gen-overall - All columns consistent
[OK] tab:ideal-depthline - All columns consistent
[OK] tab:ideal-overall - All columns consistent
[OK] tab:mesh-rect - All columns consistent
[OK] tab:mesh-wedge - All columns consistent
[OK] tab:perf-rect - All columns consistent
[OK] tab:perf-wedge - All columns consistent
[ISSUE] tab:res-rect-100
   Found 1 inconsistent columns:
   Column 4:
      2 decimals: 2 values
      3 decimals: 1 values
      Samples: ['0.058', '1.23', '10.42']

[OK] tab:res-rect-mf - All columns consistent
[OK] tab:res-wedge-100 - All columns consistent
[OK] tab:runtime-scale - All columns consistent
================================================================================
Summary: 3 tables with column inconsistencies
================================================================================

```


**Exit Code**: 0
