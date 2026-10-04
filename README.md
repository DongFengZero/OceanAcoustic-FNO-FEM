# Ocean Acoustic Field Prediction with an FNO--FEM Hybrid Solver

Code and reproducibility resources for the paper *"Coupling Fourier Neural
Operators with Finite-Element Guided Graph Refinement for Ocean Acoustic Field
Prediction"* (Ocean Engineering, under review).

The solver couples a Fourier Neural Operator (FNO) physics prior with a
finite-element-guided graph correction to predict two-dimensional ocean acoustic
transmission-loss fields.

**This README is the single index for the paper's data and code.** The
manuscript's *Data and Code Availability* statement points here rather than
repeating the URLs, because Netdisk links and their access codes can change.

## What is here

Everything needed to reproduce the paper, at three levels of effort:

| Goal | Needs | Where |
|---|---|---|
| Check that every published number is correct | raw data, no GPU | [`ch4_validation/`](ch4_validation/) — `python verify.py` |
| Regenerate the figures and tables | raw data, no GPU | [`Validation_Scripts/`](Validation_Scripts/) |
| Retrain, or rebuild the datasets | GPU / MATLAB + COMSOL | [`Experiment_Code/`](Experiment_Code/) |

## Data

Code and scripts live in this repository (< 2 MB). The datasets and per-case
results are tens of gigabytes, so they are hosted on Baidu Netdisk:

| Data | Size | Link |
|---|---|---|
| Simulation datasets (22 configs, R0--R10 / W0--W10) | ~74 GB | [Dataset](https://pan.baidu.com/s/1-G0axu7IRo3KiqnLv4bI-Q?pwd=9u97) · code `9u97` |
| Raw experimental data (per-case results + training logs) | 20.9 GB | [Raw_Experimental_Data](https://pan.baidu.com/s/1o3Avf2c7tQyKA3huSwkoSg?pwd=463b) · code `463b` |

The access code is the four characters after `pwd=` in each URL, repeated in the
last column. Downloading needs a Baidu Netdisk account.

Both folders unzip to the layout the scripts expect: `Dataset/` is organized as
`R0`--`R10` / `W0`--`W10`; `Raw_Experimental_Data/` is grouped by paper section
(`4.2_Validation` ... `4.8_Performance`), one subfolder per case. The
case-to-figure/table mapping is Table 3 of the paper, which `ch4_validation/`
verifies against the dataset folders directly.

## Repository layout

```
.
├── Experiment_Code/
│   ├── Data_Generate/       MATLAB + COMSOL dataset generation
│   └── Main_Code/           .mat -> HDF5 conversion, training, inference
├── Validation_Scripts/      scripts that regenerate the paper tables/figures
│   ├── INDEX.md             full object -> script map (paper order)
│   ├── fig03_ideal/         one directory per figure family
│   ├── ...                  (fig04_05_10_fields, fig06_07_dl, ... fig13_perf)
│   ├── table03_datasets.py  one script per table family
│   ├── ...
│   ├── table14_runtime.py
│   └── run_all.py           prints every table in one command
├── ch4_validation/          value-level verification of every table and figure
│   ├── verify.py            entry point: python verify.py
│   ├── REPORT.md            aggregate report (auto-generated)
│   ├── scripts/             table checkers, one per object
│   ├── scripts_figures/     figure checkers
│   └── reports/             per-object itemized results
└── README.md
```

Script names follow the R1 numbering of tables and figures (Figs. S1--S7 for the
Supplementary Material); `Validation_Scripts/INDEX.md` maps every object to its
script in paper order.

## Reproducing the results

### Verification suite (automated, no GPU)

`ch4_validation/` recomputes every printed value in the 12 tables and 11 figures
that Section 4 of the R1 manuscript carries (Tables 3--14, Figures 3--13) from
the archived raw data, then compares it against the typeset value. Tables 1--2
(`tab:applicability`, `tab:symbols`) and Figures 1--2 are descriptive objects — a
table of acronyms, a table of symbols, a geometry sketch and a block diagram — so
they hold no measured values and are outside the suite's scope.

Two comparison layers with deliberately different tolerances are used:

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
  differ in the 7th--8th significant digit. Agreement is therefore required only
  to within the significant figures the table actually reports; matching to that
  precision is what establishes the two channels describe the same run.

```bash
# 1. Download Raw_Experimental_Data from Baidu (link above), 20.9 GB
# 2. Point the suite at the data and the compiled paper
export CH4_RAWROOT=/path/to/parent-of-Data_and_Code_Availability
export CH4_TEXDIR=/path/to/OE_Revision_R1_Submission   # needs OE_submission.aux
# 3. Run
cd ch4_validation && python verify.py
```

Expected output: **23/23 objects, 3348 checks passed, 0 failed, 19 exempt**
(about 3 minutes).

Beyond the numbers themselves, the suite also checks the things that never
trigger a compile error — whether each table and figure is actually cited in the
body text, whether the numbers quoted in prose match both the table and the
source data, whether derived ratios are reproducible from the printed values,
and whether every caption's `best epoch` / `last epoch` claim matches the epoch
the data actually came from. See `ch4_validation/README.md` and the generated
`ch4_validation/REPORT.md`.

### Regenerating figures (no GPU)

Each figure lives in its own `figNN_*/` directory whose name carries the
manuscript figure number, so the listing below is in paper order:

| Figure | Label | Cases | Script |
|---|---|---|---|
| 3 | `fig:ideal` | 1, 2 | `fig03_ideal/fig03_ideal.py` |
| 4 | `fig:res-128` | 3, 9 | `fig04_05_10_fields/fig04_05_10_fields.py` |
| 5 | `fig:sq100` | 6--8, 12--14 | `fig04_05_10_fields/fig04_05_10_fields.py` |
| 6 | `fig:dl-cmp` | 15--24 | `fig06_07_dl/fig06_07_dl.py` |
| 7 | `fig:dl-abl` | 25--32 | `fig06_07_dl/fig06_07_dl.py` |
| 8 | `fig:perf-cmp-r` | 15--19 | `fig08_09_perf_grid/fig08_09_perf_grid.py` |
| 9 | `fig:perf-cmp-w` | 20--24 | `fig08_09_perf_grid/fig08_09_perf_grid.py` |
| 10 | `fig:mesh` | 33--38 | `fig04_05_10_fields/fig04_05_10_fields.py` |
| 11 | `fig:gen-split` | 39--42 | `fig11_gen_split/fig11_gen_split.py` |
| 12 | `fig:gen-grid` | 39--42 | `fig12_gen_extrap/fig12_gen_extrap.py` |
| 13 | `fig:perf` | 43--50 | `fig13_perf/fig13_perf.py` |

Two coverage notes. `fig04_05_10_fields.py` generates Figures 4, 5 and 10
because those field panels share one renderer (same interpolation, mask and
clip); Figure 12's *rectangular* panels come from it as well, while the wedge
ones come from `fig12_gen_extrap.py` — that split mirrors the two renderers
behind the published files, so each output reproduces exactly what the paper
carries. And `fig13_perf.py` plots hard-coded constants that must track Table 14;
`ch4_validation/scripts_figures/FIG13_perf.py` parses those constants with `ast`
and compares them against the spreadsheet, which catches the real failure mode (a
table value updated while the figure constant is left behind). `legacy/` holds
the pre-revision scripts for provenance; they carry the old figure numbering and
are not entry points.

Set the two path variables before running any of them:

```bash
export CH4_RAWROOT=/path/to/parent-of-Data_and_Code_Availability
export CH4_TEXDIR=/path/to/OE_Revision_R1_Submission
```

Redrawing rewrites the PDFs' embedded timestamps, so their byte `md5` will differ
from the paper's copies even with identical data. The suite treats that as an
expected exemption rather than a failure; to make the paper carry the redrawn
figures, copy the outputs into the manuscript's figure directory yourself.

### Regenerating tables (no GPU)

Each script prints its values, so the output can be diffed against the paper.
Table numbers are R1's:

| Table | Label | Cases | Script |
|---|---|---|---|
| 3 | `tab:datasets` | 1--50 | `table03_datasets.py` |
| 4 | `tab:ideal-overall` | 1--2 | `table04_05_ideal.py` |
| 5 | `tab:ideal-depthline` | 1--2 | `table04_05_ideal.py` |
| 6 | `tab:res-rect-mf` | 3--5, 9--11 | `table06_07_forward.py` |
| 7 | `tab:sq100` | 6--8, 12--14 | `table06_07_forward.py` |
| 8 | `tab:dl-cmp` | 15--24 | `table08_09_depthline.py` |
| 9 | `tab:dl-abl` | 25--32 | `table08_09_depthline.py` |
| 10 | `tab:perf-cmp` | 15--24 | `table10_perf_cmp.py` |
| 11 | `tab:abl` | 25--32 | `table11_13_abl_mesh_gen.py` |
| 12 | `tab:mesh` | 33--38 | `table11_13_abl_mesh_gen.py` |
| 13 | `tab:gen-overall` | 39--42 | `table11_13_abl_mesh_gen.py` |
| 14 | `tab:runtime` | 43--50 | `table14_runtime.py` |

Tables 1--2 are typeset directly in the manuscript source and have no generating
script.

Add `--tex` to any of them to also dump the typeset rows of that float, for
character-by-character comparison against the table it regenerates.

These scripts do not re-implement any parsing: each imports the same loader the
verification suite uses (`common/metrics.py:xlsx_case()`,
`common/depthline.py:recompute()`, or the matching `scripts/T*.py`), so a printed
value and a verified value come from one function call and cannot drift apart.
`run_all.py` covers the whole folder:

```bash
cd Validation_Scripts
python run_all.py                 # print every table (fast, writes nothing)
python run_all.py --xlsx-check    # also confirm the xlsx rebuilds from the logs
```

`run_all.py` checks how many tables each script was supposed to print and fails
if any are missing, so a broken script cannot pass unnoticed.
`build_accuracy_xlsx.py` closes the last gap in the provenance chain: the
accuracy spreadsheets behind the accuracy tables were produced by the original
training runs, and this script rebuilds them from the training logs alone. Its
`--check` mode reports **420/420 values matching** the archived spreadsheets
across Cases 1--42, which is what lets those tables be traced back to raw logs
rather than taken on trust.

`Validation_Scripts/INDEX.md` holds the same two maps plus where each number
comes from (raw `.npz`/`.mat` vs. archived summary `.xlsx`).

### Retraining (GPU) or rebuilding the datasets (MATLAB + COMSOL)

Convert the `.mat` datasets to HDF5 with
`Experiment_Code/Main_Code/Ocean_Dataset_barrier_comsol.py`, then train with
`ocean_trainer_forward_b.py`; see `Experiment_Code/README.md` for commands. The
datasets themselves are rebuilt with `Experiment_Code/Data_Generate/`.

## Environment

Python 3.11 with `torch`, `torch_geometric`, `h5py`, `numpy`, `scipy`,
`scikit-learn`, `matplotlib`, `tqdm`, `openpyxl`. Dataset generation additionally
requires MATLAB and COMSOL Multiphysics 6.4 (release of November 18, 2025;
LiveLink for MATLAB), as described in Section 4.1 of the paper.

The verification suite needs no GPU, but does need `pandas` and the `pdftotext`
utility (Poppler) — it reads the text layer of the figure PDFs to compare the
annotations drawn inside them against the source data.

## Citation

Please cite the paper if you use this code or data. A BibTeX entry will be added
here upon publication.
