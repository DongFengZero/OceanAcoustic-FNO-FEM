# Chapter 4 objects → generator scripts

Every table and figure in the R1 manuscript maps to a script here. Tables print
their data (or dump XeLaTeX rows with `--tex`); figures regenerate the PDF the
paper includes.

Set these first (same as the verification suite):

```bash
export CH4_RAWROOT=/path/to/parent-of-Data_and_Code_Availability
export CH4_TEXDIR=/path/to/OE_Revision_R1_Submission   # needs OE_submission.aux
```

`_figpaths.py` resolves every figure-script path from those two variables, so
nothing under `fig*/` hard-codes a drive letter. The table scripts use the
equivalent layer in `ch4_validation/common/paths.py`.

## Figures — regenerate the PDF

Each figure lives in its own `figNN_*/` directory, and the directory name carries
the manuscript figure number, so the rows below are in paper order. Where one
script produces more than one figure, its directory name lists them all.

| Figure | Label | Cases | Script |
|---|---|---|---|
| 3 | `fig:ideal` | 1, 2 | `fig03_ideal/fig03_ideal.py` |
| 4 | `fig:res-128` | 3, 9 | `fig04_05_10_fields/fig04_05_10_fields.py` |
| 5 | `fig:sq100` | 6–8, 12–14 | `fig04_05_10_fields/fig04_05_10_fields.py` |
| 6 | `fig:dl-cmp` | 15–24 | `fig06_07_dl/fig06_07_dl.py` |
| 7 | `fig:dl-abl` | 25–32 | `fig06_07_dl/fig06_07_dl.py` |
| 8 | `fig:perf-cmp-r` | 15–19 | `fig08_09_perf_grid/fig08_09_perf_grid.py` |
| 9 | `fig:perf-cmp-w` | 20–24 | `fig08_09_perf_grid/fig08_09_perf_grid.py` |
| 10 | `fig:mesh` | 33–38 | `fig04_05_10_fields/fig04_05_10_fields.py` |
| 11 | `fig:gen-split` | 39–42 | `fig11_gen_split/fig11_gen_split.py` |
| 12 | `fig:gen-grid` | 39–42 | `fig12_gen_extrap/fig12_gen_extrap.py` |
| 13 | `fig:perf` | 43–50 | `fig13_perf/fig13_perf.py` |

Two notes on coverage:

- `fig04_05_10_fields.py` generates Figs. 4, 5 and 10, because those field panels
  share one renderer (same interpolation, mask and clip). Fig. 12's *rectangular*
  panels (`gen_extrap_R9/R10`) come from it as well, while the wedge ones come
  from `fig12_gen_extrap.py`. That split mirrors the two renderers behind the
  published files, so each output reproduces exactly what the paper carries.
- `fig13_perf.py` plots hard-coded constants that must track Table 14.
  `ch4_validation/scripts_figures/FIG13_perf.py` parses those constants with
  `ast` and compares them against the xlsx, which catches the real failure mode
  (a table value updated while the figure constant is left behind).

## Supplementary Material — Figs. S1–S7

The field figures moved out of the main text in R1 are redrawn at printed size by
`figS_supplementary/figS_supplementary.py`, which reuses the main-text renderers
(`fig04_05_10_fields.py` for field panels, `fig08_09_perf_grid.py` for the grids).

| Figure | Content | Cases | Original |
|---|---|---|---|
| S1 / S2 | 256 m fields, rectangular / wedge | 4 / 10 | 6 |
| S3 / S4 | 512 m fields, rectangular / wedge | 5 / 11 | 7 |
| S5 / S6 | Ablation-variant grids, R1 / W1 | 25–28 / 29–32 | 16 / 17 |
| S7 | Wedge extrapolation, W9 / W10 | 41 / 42 | 22 |

`ch4_validation/scripts_figures/FIGS_supplementary.py` recomputes every source position
and averaged error printed on these figures from the ep200 npz and cross-checks the
S-numbering across the manuscript, the supplementary document and the response letter.

`legacy/` holds the pre-revision scripts, kept for provenance. They are no longer
entry points and still carry the old figure numbering.

## Tables — print the data

| Table | Label | Cases | Script |
|---|---|---|---|
| 1 | `tab:applicability` | — | typeset in the manuscript source |
| 2 | `tab:symbols` | — | typeset in the manuscript source |
| 3 | `tab:datasets` | 1–50 | `table03_datasets.py` |
| 4 | `tab:ideal-overall` | 1–2 | `table04_05_ideal.py` |
| 5 | `tab:ideal-depthline` | 1–2 | `table04_05_ideal.py` |
| 6 | `tab:res-rect-mf` | 3–5, 9–11 | `table06_08_forward.py` |
| 7 | `tab:sq100` | 6–8, 12–14 | `table06_08_forward.py` |
| 8 | `tab:dl-cmp` | 15–24 | `table09_12_depthline.py` |
| 9 | `tab:dl-abl` | 25–32 | `table09_12_depthline.py` |
| 10 | `tab:perf-cmp` | 15–24 | `table13_14_perf.py` |
| 11 | `tab:abl` | 25–32 | `table15_19_abl_mesh_gen.py` |
| 12 | `tab:mesh` | 33–38 | `table15_19_abl_mesh_gen.py` |
| 13 | `tab:gen-overall` | 39–42 | `table15_19_abl_mesh_gen.py` |
| 14 | `tab:runtime` | 43–50 | `table20_21_runtime.py` |

Tables 7--12 each merge the rectangular and wedge halves into one float: a single
`tabular` with the two geometries side by side as column groups (not two
`tabular`s). Table 14 is the exception — one float, two `minipage`s, two
`tabular`s, written `(a)` and `(b)`. `--tex` handles both: it dumps the float's
first `tabular`, and for Table 14 prints each half separately.

The left column is the R1 manuscript numbering. The script file names keep their
original T-numbers, so `table09_12_depthline.py` prints Tables 9–12 of this list.

## Where the numbers come from

| Object | Reads | Layer |
|---|---|---|
| Figs. 3–12 | `.npz` / `.mat` | raw |
| Table 3 | COMSOL mesh `.mat` | raw |
| Tables 5, 9–12 | `.npz`, recomputed at full precision | raw |
| Tables 4, 6–8, 13 | archived summary `.xlsx` | summary |
| Table 14 | archived runtime `.xlsx` | summary |
| Fig. 13 | constants in the script, transcribed from Table 14 | transcribed |

The summary layer is one step removed from the logs, so both `.xlsx` families
have a generator in this folder and the chain closes:

```
full_run_*.log  --build_accuracy_xlsx.py-->  4.2-4.7 accuracy xlsx  -->  Tables 4-7, 10-13
full_run_*.log  --build_perf.py---------->  4.8 runtime xlsx      -->  Table 14, Fig. 13
```

`build_accuracy_xlsx.py --check` rebuilds every accuracy value from the training
logs and compares it against the archived spreadsheet: 420 checks (42 cases × 5
groups × Sol/TL) agree, plus the best epoch of each case. Run it to confirm the
spreadsheets are faithful to the logs rather than taking them on trust.

## Why the table scripts are trustworthy

They do not re-implement any parsing. Each one imports the loader the
verification suite itself uses — `common/metrics.py:xlsx_case()` for the
accuracy tables, `common/depthline.py:recompute()` for the depth-line tables
(full precision, recomputed from the `.npz`), and `load_base()` / `load_scale()`
of `ch4_validation/scripts/T14_runtime.py` for the runtime table. A printed value
and the value `verify.py` checks come from the same function call, so the two
cannot drift apart.

For the authoritative pass/fail on all 23 objects, run the suite itself:

```bash
cd ../ch4_validation && python verify.py
```
