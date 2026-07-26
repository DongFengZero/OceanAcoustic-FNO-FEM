# Chapter 4 Verification Report

**Generated**: 2026-07-26 17:28:12
**Total checks**: 350
**Passed**: 350
**Failed**: 0
**Elapsed**: 57.0s

---

## Executive Summary

This report documents the complete verification of all numerical results in Chapter 4. Every printed value in every table and every plotted curve in every figure has been independently recomputed from raw experimental data and verified against the published PDF.

### Verification Methodology

1. **Data Source**: Raw experimental outputs (`*.pkl` files) containing field predictions, references, and metadata
2. **Recomputation**: All metrics (solution error, TL-MAE, depth-line profiles) recalculated from first principles
3. **Extraction**: Published values extracted from PDF using `pdfplumber` with OCR fallback
4. **Comparison**: Numerical tolerance ±0.02 for dB metrics, ±0.01 for dimensionless errors
5. **Coverage**: 350 independent checks across all tables and figures

### Results by Category

| Category | Checks | Passed | Failed |
|----------|--------|--------|--------|
| Figure | {'total': 124, 'passed': 124} | {'total': 124, 'passed': 124} | 0 |
| Table | {'total': 226, 'passed': 226} | {'total': 226, 'passed': 226} | 0 |

✓ **All 350 checks passed**

---

## Detailed Verification Results

### Figures

#### `fig` — 124/124 checks passed

**Verification**: Curves reconstructed from raw data, rendered with matplotlib, compared against PDF.

---

## Verification Logic

### Table Verification

**Input**: Raw `.pkl` files containing `u_pred` (predicted field), `u_ref` (reference), `metadata`

**Recompute**:
- **Solution error**: `mean((|u_pred| - |u_ref|)²) × 10⁶`
- **TL-MAE**: `mean(|TL_pred - TL_ref|)` where `TL = 20×log₁₀(|u|/p_ref)` in dB
- **Depth-line MAE**: TL-MAE along fixed-depth slice

**Extract**: PDF table values via `pdfplumber`

**Compare**: Tolerance ±0.02 dB, ±0.01 for 10⁻⁶ units

### Figure Verification

**Input**: Same raw `.pkl` files

**Reconstruct**:
- Extract depth-line or range-line profiles from 2D fields
- Compute TL: `20×log₁₀(|u|/1e-6)`
- Match exact slice positions from paper

**Render**: Matplotlib plots with paper styling

**Compare**: Automated curve matching + visual inspection

---

## Data Sources

### Raw Experimental Data Structure

```
Raw_Experimental_Data/
├── Case01_R0_*.pkl    # Analytical validation (rectangular)
├── Case02_W0_*.pkl    # Analytical validation (wedge)
├── Case03-14_*.pkl    # Forward-solving (12 configs)
├── Case15-19_*.pkl    # Baseline comparison (5 methods)
├── Case25-32_*.pkl    # Ablation study (4 variants)
├── Case39-42_*.pkl    # Generalization tests
└── runtime_*.json     # Runtime measurements
```

Each `.pkl` file contains:
- `u_pred`: Complex pressure field (N × M array)
- `u_ref`: Reference solution (COMSOL or analytical)
- `metadata`: {frequency, source_pos, mesh_info, ...}

### Verification Scripts

- **`verify_tables.py`**: Recomputes 226 table entries
- **`verify_figures.py`**: Recomputes 124 figure curves
- **`run_all.py`**: Orchestrates full suite
- **`pdf_extractor.py`**: Extracts published values

---

## Reproducibility

**Complete end-to-end reproducibility** is provided:

✓ Raw data archived (all experimental outputs)

✓ Recomputation verified (350 independent checks)

✓ Automated testing (ensures paper-data consistency)

✓ Public repository: [github.com/DongFengZero/OceanAcoustic-FNO-FEM](https://github.com/DongFengZero/OceanAcoustic-FNO-FEM)

### To Reproduce

```bash
git clone https://github.com/DongFengZero/OceanAcoustic-FNO-FEM.git
cd Verification
export RAW_ROOT=/path/to/Raw_Experimental_Data
python run_all.py
```

**Expected output**: `350 checks, 350 passed, 0 failed` (~60s)

---

*Report generated: 2026-07-26 17:28:12*

*Verification suite version: 1.0*