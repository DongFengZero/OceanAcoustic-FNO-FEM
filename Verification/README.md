# Chapter 4 Verification Suite

This package systematically verifies that every table and figure in Chapter 4 of the paper is reproducible from the archived raw experimental data. It recomputes all printed values from the source spreadsheets and NPZ field dumps, then diffs them against the transcribed paper values to confirm correctness.

## What It Verifies

### Tables (226 checks)
- **T4** (ideal validation): Cases 1–2, 4 frequencies each
- **T6** (forward multi-freq): Cases 3–5, 9–11, 4 frequencies each
- **T7/T8** (forward 100Hz): Cases 6–8, 12–14, single frequency
- **T13/T14** (comparison): Cases 15–24, 4 frequencies each
- **T15/T16** (ablation): Cases 25–32, 4 frequencies each
- **T17/T18** (mesh independence): Cases 33–38, single frequency
- **T19** (generalization): Cases 39–42, 4 frequencies each
- **T5** (ideal depth-line): Cases 1–2, min-MAE sample per frequency
- **T9–T12** (comparison/ablation depth-line): 4 groups, forced-y selection pipeline
- **T20** (runtime base-scale): Cases 43–44, COMSOL vs 1/2/4 GPU
- **T21** (runtime scaling): Cases 45–50, domain-size scaling

### Figures (124 checks)
- **Field figures**: NPZ existence, shape `[8,N]` or `[2,N]`, frequency set, node count cross-checks
- **Depth-line figures**: ensemble NPZ integrity, selection pipeline reproducibility
- **Split figure**: source-position array shape `[8,2]`
- **Runtime figure**: performance xlsx rows, node count cross-checks

Each check yields PASS/FAIL with source file traceability.

## Structure

```
Verification/
├── README.md                     # this file
├── paper_values.py               # transcribed printed values (ground truth)
├── data_sources.py               # loaders for xlsx and npz raw data
├── depthline_recompute.py        # depth-line selection pipeline
├── verify_tables.py              # table recomputation + diff
├── verify_figures.py             # figure provenance + structural checks
├── run_all.py                    # master runner
├── provenance.json               # machine-readable artifact→source map
├── VERIFICATION_REPORT.md        # human-readable report (generated)
└── verification_results.json     # structured results (generated)
```

## Requirements

- Python 3.7+
- pandas
- numpy
- scipy
- openpyxl (for xlsx reading)

Install with:
```bash
pip install pandas numpy scipy openpyxl
```

## Usage

1. **Download the raw data** from the Baidu links in the main README (Simulation datasets ~74GB, Raw experimental data ~21GB).

2. **Extract** `Raw_Experimental_Data/` to a known location.

3. **Set the path** via environment variable:
   ```bash
   export RAW_ROOT=/path/to/Raw_Experimental_Data
   ```
   or edit `data_sources.py` to add your path to `_CANDIDATES`.

4. **Run the suite**:
   ```bash
   cd Verification
   python run_all.py
   ```

Expected output:
```
======================================================================
Chapter 4 Verification Suite
Recomputing all tables and figures from raw data...
======================================================================

[1/2] Verifying tables (accuracy + depth-line + runtime)...
[2/2] Verifying figures (field + depth-line + split + runtime)...

======================================================================
SUMMARY
======================================================================
Total:  350 checks
Passed: 350
Failed: 0
Time:   12.3s
  table: 226/226 pass
  figure: 124/124 pass

JSON report written to verification_results.json
Markdown report written to VERIFICATION_REPORT.md

======================================================================
✓ ALL CHECKS PASSED
======================================================================
```

## What Gets Recomputed

### Accuracy Tables
The verifier recomputes `Sol_error` (field MSE × 1e6) and `TL-MAE` (dB) from the `损失(loss)` and `Comsol vs sol` columns in the per-group xlsx files using the formula:
```python
Sol = (loss - comsol_vs_sol) * 1e4    # normal rows
Sol = loss * 1e4                      # ablation "w/o prior-sup." rows
TL  = "TL vs COMSOL" column           # verbatim
```
This is more reliable than the rounded `MSE` column. Tolerances: Sol ±0.05 or 1.2%, TL ±0.02 dB.

### Depth-Line Tables
Re-runs the selection pipeline from `advantage_depth_line.py`:
1. Load ensemble NPZ for all methods in the group.
2. Cubic-interpolate each sample onto a 300×300 grid.
3. Mask wedge/ellipse regions, clip to [vmin, vmax].
4. At the forced-y row, for each frequency, pick the sample maximizing "Full's advantage" (min(baseline_MAE) - Full_MAE) subject to a minimum point count.
5. Report the MAE of that sample.

Tolerances: ±0.02 dB.

### Runtime Tables
Read from the performance xlsx two-sheet structure and cross-check node counts against the NPZ `x_coords` length. Tolerances: time/throughput ±1%, speedup ±2%.

### Figures
Structural checks only:
- NPZ file exists at the expected path.
- Shape is `[nsamples, N]` where nsamples = 8 (multi-freq) or 2 (single-freq).
- Frequency array matches [25, 50, 75, 100] or [100].
- Node count `N` matches the xlsx-cited or text-cited value.

Pixel-level figure reproduction is not verified (would require matplotlib version pinning and font matching). The figures are rendered by scripts in `Validation_Scripts/`; this suite confirms their input data is valid.

## Provenance

See `provenance.json` for a machine-readable map of every artifact (table/figure) to its source files (xlsx/npz) and generating script. The paper cites the GitHub repo and Baidu links in the Data and Code Availability section; this package closes the loop by making every printed number independently recomputable.

## Troubleshooting

**`FileNotFoundError: Raw_Experimental_Data not found`**  
→ Set `RAW_ROOT` environment variable or edit `data_sources.py` `_CANDIDATES`.

**`pandas/numpy/scipy not found`**  
→ `pip install pandas numpy scipy openpyxl`

**Verification failures**  
→ Check that you extracted the latest version of Raw_Experimental_Data. The Baidu links are versioned; older downloads may have different rounding or missing files.

## License

Same as the parent repository (see top-level LICENSE).
