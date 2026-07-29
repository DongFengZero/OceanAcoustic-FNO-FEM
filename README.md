# Ocean Acoustic Field Prediction with an FNO--FEM Hybrid Solver

Code and reproducibility resources for the paper *"Coupling Fourier Neural Operators with Finite-Element Guided Graph Refinement for Ocean Acoustic Field Prediction"* (Ocean Engineering, under review).

The solver couples a Fourier Neural Operator (FNO) physics prior with a
finite-element-guided graph correction to predict two-dimensional ocean
acoustic transmission-loss fields.

## What is here

Everything needed to reproduce the paper, at three levels of effort:

| Goal | Needs | Where |
|---|---|---|
| Check that every published number is correct | raw data, no GPU | [`ch4_validation/`](ch4_validation/) — `python verify.py` |
| Regenerate the figures and tables | raw data, no GPU | [`Validation_Scripts/`](Validation_Scripts/) |
| Retrain, or rebuild the datasets | GPU / MATLAB + COMSOL | [`Experiment_Code/`](Experiment_Code/) |

Code and scripts live in this repository (< 2 MB). The datasets and per-case
results are tens of gigabytes, so they are hosted on Baidu Netdisk:

| Data | Size | Link |
|---|---|---|
| Simulation datasets (22 configs, R0--R10 / W0--W10) | ~74 GB | [Dataset](https://pan.baidu.com/s/1-G0axu7IRo3KiqnLv4bI-Q?pwd=9u97) · code `9u97` |
| Raw experimental data (per-case results + training logs) | 20.9 GB | [Raw_Experimental_Data](https://pan.baidu.com/s/16Q---bIQs0Hpf-SJxBmnUg?pwd=hmzx) · code `hmzx` |

## Repository layout

```
.
├── Experiment_Code/
│   ├── Data_Generate/       MATLAB + COMSOL dataset generation
│   └── Main_Code/           .mat -> HDF5 conversion, training, inference
├── Validation_Scripts/      scripts that regenerate the paper tables/figures
├── ch4_validation/          value-level verification of every table and figure
│   ├── verify.py            entry point: python verify.py
│   ├── REPORT.md            aggregate report (auto-generated)
│   └── reports/             per-object itemized results
└── README.md
```

The two Baidu Netdisk folders unzip to the layout the scripts expect:
`Dataset/` is organized as `R0`--`R10` / `W0`--`W10`; `Raw_Experimental_Data/`
is grouped by paper section (`4.2_Validation` ... `4.8_Performance`), one
subfolder per case. The case-to-figure/table mapping is Table 3 of the paper,
which `ch4_validation/` verifies against the dataset folders directly.

## Reproducing the results

### Verification suite (automated, no GPU)

`ch4_validation/` recomputes every printed value in the 19 tables and 21 figures
of Chapter 4 from the archived raw data, then compares it against the typeset
value. Two comparison layers with deliberately different tolerances are used:

- **Printed value vs. typeset text — exact.** Each source value is rounded to
  the number of decimals actually printed and must then match the typeset digits
  character for character, with no tolerance. A tolerance here would hide both a
  real discrepancy and a zero-padded fabrication.
- **Source vs. source (xlsx vs. training log) — small numerical tolerance.** The
  same quantity is read from the summary `.xlsx` and independently recomputed
  from the training-log loss terms; these two channels must agree to a relative
  tolerance of `2e-6` (with a `1e-9` absolute floor). They are not expected to be
  bit-identical, because the spreadsheet stores values already rounded for
  display while the log figure is recomputed in full precision, so the two can
  differ in the 7th–8th significant digit. Agreement is therefore required only
  to within the significant figures the table actually reports; matching to that
  precision is what establishes the two channels describe the same run, and
  demanding bit-identical values would only flag a coincidence that rounding
  makes impossible.

```bash
# 1. Download Raw_Experimental_Data from Baidu (link above), 20.9 GB
# 2. Point the suite at the data and the compiled paper
export CH4_RAWROOT=/path/to/parent-of-Data_and_Code_Availability
export CH4_TEXDIR=/path/to/els-cas-templates    # needs OE_submission.aux
# 3. Run
cd ch4_validation && python verify.py
```

Expected output: **40/40 objects, 3068 checks passed, 0 failed**. Beyond the
numbers themselves, the suite also checks the things that never trigger a
compile error — whether each table and figure is actually cited in the body
text, whether the numbers quoted in prose match both the table and the source
data, whether derived ratios are reproducible from the printed values, and
whether every caption's `best epoch` / `last epoch` claim matches the epoch the
data actually came from. See `ch4_validation/README.md` and the generated
`ch4_validation/REPORT.md`.

### Regenerating figures and tables (no GPU)

Run the scripts in `Validation_Scripts/` against the downloaded
`Raw_Experimental_Data`. Each script regenerates one family of figures and
prints the values it writes, so its output can be diffed against the paper:

| Script | Produces |
|---|---|
| `regen_ideal_panels.py` | Figs. 3--4, analytical validation (`*_grid2.pdf`) |
| `regen_results_bigfont.py` | Figs. 5--9, forward-solving fields (`CaseNN_XX_TL.pdf`) |
| `advantage_depth_line.py` | Figs. 10--13 and Tables 9--12, depth-line families |
| `regen_method_grid.py` | Figs. 14--17, baseline and ablation grids |
| `plot_generalization_split.py` | Fig. 20, train/test source split |
| `regen_gen_extrap_bigfont.py` | Figs. 21--22, extrapolation fields |
| `build_perf.py` | Tables 20--21, runtime statistics (writes an `.xlsx`) |
| `build_perf_figure.py` | Fig. 23, the three runtime panels |

The remaining scripts in that folder (`redraw_tl_figures.py`,
`regen_wide_fields.py`, `restore_tl_figure.py`, `scan_depth_lines.py`) are
earlier or auxiliary tools kept for provenance; they are not the entry points
for any figure in the current manuscript.

Note that `build_perf.py` writes the runtime spreadsheet behind Tables 20--21
but does not plot; `build_perf_figure.py` draws Fig. 23 from it. The latter
carries its numbers as literals in the source rather than reading the
spreadsheet, so the verification suite parses those literals out of the script
and checks them against the spreadsheet — otherwise the figure could silently
go stale if a table value were updated. See
`ch4_validation/reports/FIG23_perf.md`.

### Retraining (GPU) or rebuilding the datasets (MATLAB + COMSOL)

Convert the `.mat` datasets to HDF5 with
`Experiment_Code/Main_Code/Ocean_Dataset_barrier_comsol.py`, then train with
`ocean_trainer_forward_b.py`; see `Experiment_Code/README.md` for commands.
The datasets themselves are rebuilt with `Experiment_Code/Data_Generate/`.

## Environment

Python 3.11 with `torch`, `torch_geometric`, `h5py`, `numpy`, `scipy`,
`scikit-learn`, `matplotlib`, `tqdm`, `openpyxl`. Dataset generation additionally
requires MATLAB and COMSOL Multiphysics (LiveLink for MATLAB).

The verification suite needs no GPU, but does need `pandas` and the `pdftotext`
utility (Poppler) — it reads the text layer of the figure PDFs to compare the
annotations drawn inside them against the source data.

## Citation

Please cite the paper if you use this code or data. A BibTeX entry will be added
here upon publication.
