# Chapter 4 objects → generator scripts

Every table and figure in Chapter 4 maps to a script here. Tables print their
data to stdout; figures regenerate the PDF that the paper includes. Objects of
the same kind share a script where the extraction logic is identical.

Set these first (same as the verification suite):

```bash
export CH4_RAWROOT=/path/to/parent-of-Data_and_Code_Availability
export CH4_TEXDIR=/path/to/els-cas-templates    # needs OE_submission.aux
```

## Tables — print the data

| Table | Label | Cases | Script |
|---|---|---|---|
| 3 | `tab:datasets` | 1–50 | `table03_datasets.py` |
| 4 | `tab:ideal-overall` | 1–2 | `table04_05_ideal.py` |
| 5 | `tab:ideal-depthline` | 1–2 | `table04_05_ideal.py` |
| 6 | `tab:res-rect-mf` | 3–5, 9–11 | `table06_08_forward.py` |
| 7 | `tab:res-rect-100` | 6–8 | `table06_08_forward.py` |
| 8 | `tab:res-wedge-100` | 12–14 | `table06_08_forward.py` |
| 9 | `tab:dl-cmp-rect` | 15–19 | `table09_12_depthline.py` |
| 10 | `tab:dl-cmp-wedge` | 20–24 | `table09_12_depthline.py` |
| 11 | `tab:dl-abl-rect` | 25–28 | `table09_12_depthline.py` |
| 12 | `tab:dl-abl-wedge` | 29–32 | `table09_12_depthline.py` |
| 13 | `tab:perf-rect` | 15–19 | `table13_14_perf.py` |
| 14 | `tab:perf-wedge` | 20–24 | `table13_14_perf.py` |
| 15 | `tab:abl-rect` | 25–28 | `table15_19_abl_mesh_gen.py` |
| 16 | `tab:abl-wedge` | 29–32 | `table15_19_abl_mesh_gen.py` |
| 17 | `tab:mesh-rect` | 33–35 | `table15_19_abl_mesh_gen.py` |
| 18 | `tab:mesh-wedge` | 36–38 | `table15_19_abl_mesh_gen.py` |
| 19 | `tab:gen-overall` | 39–42 | `table15_19_abl_mesh_gen.py` |
| 20 | `tab:runtime` | 43–44 | `table20_21_runtime.py` |
| 21 | `tab:runtime-scale` | 45–50 | `table20_21_runtime.py` |

Pass `--tex` to any table script to also dump the typeset rows, so printed and
typeset values can be compared side by side.

## Figures — regenerate the PDF

| Figure | Label | Cases | Script |
|---|---|---|---|
| 3 | `fig:ideal-rect` | 1 | `regen_ideal_panels.py` |
| 4 | `fig:ideal-wedge` | 2 | `regen_ideal_panels.py` |
| 5 | `fig:res-128` | 3, 9 | `regen_results_bigfont.py` |
| 6 | `fig:res-256` | 4, 10 | `regen_results_bigfont.py` |
| 7 | `fig:res-512` | 5, 11 | `regen_results_bigfont.py` |
| 8 | `fig:res-rect-100` | 6–8 | `regen_results_bigfont.py` |
| 9 | `fig:res-wedge-100` | 12–14 | `regen_results_bigfont.py` |
| 10 | `fig:dl-cmp-rect` | 15–19 | `advantage_depth_line.py` |
| 11 | `fig:dl-cmp-wedge` | 20–24 | `advantage_depth_line.py` |
| 12 | `fig:dl-abl-rect` | 25–28 | `advantage_depth_line.py` |
| 13 | `fig:dl-abl-wedge` | 29–32 | `advantage_depth_line.py` |
| 14 | `fig:perf-rect` | 15–19 | `regen_method_grid.py` |
| 15 | `fig:perf-wedge` | 20–24 | `regen_method_grid.py` |
| 16 | `fig:abl-rect` | 25–28 | `regen_method_grid.py` |
| 17 | `fig:abl-wedge` | 29–32 | `regen_method_grid.py` |
| 18 | `fig:mesh-rect` | 33–35 | `regen_results_bigfont.py` |
| 19 | `fig:mesh-wedge` | 36–38 | `regen_results_bigfont.py` |
| 20 | `fig:gen-split` | 39–42 | `plot_generalization_split.py` |
| 21 | `fig:gen-grid` | 39–40 | `regen_gen_extrap_bigfont.py` |
| 22 | `fig:gen-grid-wedge` | 41–42 | `regen_gen_extrap_bigfont.py` |
| 23 | `fig:perf` | 43–50 | `build_perf_figure.py` |

Every figure script carries the same mapping in its own module docstring, so the
script alone tells you which figures it produces.

Two scripts here are not figure entry points:

- `build_perf.py` writes the runtime `.xlsx` that Tables 20–21 and Fig. 23 read.
  Run it before `build_perf_figure.py` if the raw logs have changed. It draws
  nothing.
- `regen_wide_fields.py` re-renders only the wide-flat domains (Cases 4, 5, 10,
  11) to fix a colorbar-versus-field aspect problem. Those cases appear in
  Figs. 6–7, whose entry point — and the script the verification checks — is
  `regen_results_bigfont.py`.

## Where the numbers come from

Not every script reads the raw arrays directly, so it is worth being precise
about which layer each one sits on.

| Object | Reads | Layer |
|---|---|---|
| Figs. 3–22 | `.npz` / `.mat` | raw |
| Table 3 | COMSOL mesh `.mat` | raw |
| Tables 5, 9–12 | `.npz`, recomputed at full precision | raw |
| Tables 4, 6–8, 13–19 | archived summary `.xlsx` | summary |
| Tables 20–21 | archived runtime `.xlsx` | summary |
| Fig. 23 | constants in the script, transcribed from Tables 20–21 | transcribed |

The summary layer is one step removed from the logs, so both `.xlsx` families
have a generator in this folder and the chain closes:

```
full_run_*.log  --build_accuracy_xlsx.py-->  4.2-4.7 accuracy xlsx  -->  Tables 4, 6-8, 13-19
full_run_*.log  --build_perf.py---------->  4.8 runtime xlsx      -->  Tables 20-21, Fig. 23
```

`build_accuracy_xlsx.py --check` rebuilds every accuracy value from the training
logs and compares it against the archived spreadsheet: 420 checks (42 cases × 5
groups × Sol/TL) agree, plus the best epoch of each case. Run it to confirm the
spreadsheets are faithful to the logs rather than taking them on trust.

Fig. 23 is the one transcribed object — its values are literal constants rather
than a spreadsheet read. That is deliberate: `FIG23_perf.py` parses those
constants with `ast` and compares them against the xlsx, which catches the real
failure mode (a table value updated while the figure constant is left behind).
Reading the xlsx at plot time would remove that check without adding a
guarantee, since the plotted numbers still have to match the typeset table.

## Why the table scripts are trustworthy

They do not re-implement any parsing. Each one imports the loader the
verification suite itself uses — `common/metrics.py:xlsx_case()` for the
accuracy tables, `common/depthline.py:recompute()` for the depth-line tables
(full precision, recomputed from the `.npz`), and the `load_xlsx()` of the
matching `ch4_validation/scripts/T*.py` for the runtime tables. A printed value
and the value `verify.py` checks come from the same function call, so the two
cannot drift apart.

For the authoritative pass/fail on all 40 objects, run the suite itself:

```bash
cd ../ch4_validation && python verify.py
```
