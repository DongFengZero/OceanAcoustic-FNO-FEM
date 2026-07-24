# Ocean Acoustic Field Prediction with an FNO--FEM Hybrid Solver

Code and reproducibility resources for the paper *"Coupling Fourier Neural Operators with Finite-Element Guided Graph Refinement for Ocean Acoustic Field Prediction"* (Ocean Engineering, under review).

The solver couples a Fourier Neural Operator (FNO) physics prior with a
finite-element-guided graph correction to predict two-dimensional ocean
acoustic transmission-loss fields.

## Resources

Small text assets (code, scripts, docs) live in **this GitHub repository**.
The large binary data (simulation `.mat`, model weights `.pth`) are hosted on
**Baidu Netdisk** because they exceed GitHub file-size limits.

| Resource | Size | Location |
|---|---|---|
| Experiment code + validation scripts | < 1 MB | this repository |
| Simulation datasets (22 configs, R0--R10 / W0--W10) | ~74 GB | [Baidu Netdisk — Dataset](https://pan.baidu.com/s/1-G0axu7IRo3KiqnLv4bI-Q?pwd=9u97) (code: `9u97`) |
| Raw experimental data (per-case results + training logs) | ~21 GB | [Baidu Netdisk — Raw Data](https://pan.baidu.com/s/14nrzOamy2SqJxcyQ5gz2Jw?pwd=eimh) (code: `eimh`) |

## Repository layout

```
.
├── Experiment_Code/
│   ├── Data_Generate/       MATLAB + COMSOL dataset generation
│   └── Main_Code/           .mat -> HDF5 conversion, training, inference
├── Validation_Scripts/      scripts that regenerate the paper tables/figures
├── MANIFEST.md              case <-> figure/table <-> data mapping
├── VERIFICATION_REPORT.md   table values verified against archived data
└── README.md
```

The two Baidu Netdisk folders mirror the structure documented in `MANIFEST.md`:
`Dataset/` is organized as `R0`--`R10` / `W0`--`W10`; `Raw_Experimental_Data/`
is grouped by paper section (`4.2_Validation` ... `4.8_Performance`), one
subfolder per case.

## Reproducing the results

1. **Clone this repository** for all code and scripts.
2. **Download data from Baidu Netdisk** as needed (see the table above); the
   `Dataset` and `Raw_Experimental_Data` folders unzip to the same layout
   referenced by the scripts.
3. **Figures / tables (no GPU needed).** Run the scripts in
   `Validation_Scripts/` against the downloaded `Raw_Experimental_Data` to
   regenerate the paper figures and tables.
4. **Retrain from scratch (GPU).** Convert the `.mat` datasets to HDF5 with
   `Experiment_Code/Main_Code/Ocean_Dataset_barrier_comsol.py`, then train with
   `ocean_trainer_forward_b.py`. See `Experiment_Code/README.md` for commands.
5. **Regenerate datasets (MATLAB + COMSOL).** Use the scripts in
   `Experiment_Code/Data_Generate/`.

## Environment

Python 3.11 with `torch`, `torch_geometric`, `h5py`, `numpy`, `scipy`,
`scikit-learn`, `matplotlib`, `tqdm`, `openpyxl`. Dataset generation additionally
requires MATLAB and COMSOL Multiphysics (LiveLink for MATLAB).

## Citation

Please cite the paper if you use this code or data. A BibTeX entry will be added
here upon publication.
