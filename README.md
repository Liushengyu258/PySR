# Hybrid Symbolic-Regression Framework for Pollutant Concentration

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A compact, fully reproducible reference implementation of a **hybrid
framework that couples Symbolic Regression (PySR) with a neural denoiser**
to recover an interpretable closed-form law for the spatial decay of
pollutant concentration from noisy CFD simulation data.

This repository contains the exact code and data used to produce every
figure in our paper.

---

## Highlights

- **Closed-form law** &mdash; recovers an analytic formula
  `C(x) = C_in / [ (alpha * x) / max(Area - beta * sqrt(x/v) + gamma, 0.1) + delta ]`
  with physically interpretable parameters.
- **Noise-robust** &mdash; Hybrid PySR stays above R^2 = 0.9 up to ~47 % target
  noise, while direct symbolic regression collapses at ~50 %.
- **Data-efficient** &mdash; reaches 99 % of peak R^2 with only a few thousand
  training samples (see Figure 8).
- **Reproducible** &mdash; every random seed is pinned. Running the scripts end
  to end reproduces the paper figures.

---

## Project layout

```
PySR/
|-- README.md                   This file
|-- LICENSE                     MIT
|-- requirements.txt            Python dependencies (pysr requires Julia)
|-- .gitignore
|-- viz_config.py               Shared matplotlib style (paper fonts/palette)
|
|-- data/                       Raw + processed CSVs
|   |-- cases.csv               Per-case inlet conditions (V_in, C_in, Area)
|   |-- summary_0_499.csv       Per-case concentration profile (wide format)
|   |-- cfd_lhs_cases.csv       Latin-hypercube sampling of cases
|   |-- case.csv                Time-step table used by the Fluent batch runner
|   |-- train_dataset_ready.csv Merged ML-ready long-format dataset
|   `-- Data_Efficiency_Curve.csv
|
|-- src/                        Main pipeline
|   |-- __init__.py
|   |-- _bootstrap.py           Auto path resolution
|   |-- data_processing.py      Build train_dataset_ready.csv; case-profile plot
|   |-- stage1_exploration.py   PySR data-driven formula discovery
|   |-- stage2_fitting.py       Physics-informed curve_fit
|   |-- exp_robustness.py       Noise sweep 0-200% (Direct / MLP / Hybrid)
|   `-- exp_efficiency.py       Training-set-size sweep (100 - 44 400 samples)
|
|-- plotting/                   Post-processing: one script per paper figure
|   |-- __init__.py
|   |-- _paths.py
|   |-- fig1_fit_residual.py    Fig. 1  combined fit + residuals
|   |-- fig4_degradation.py     Fig. 4  performance degradation curve
|   |-- fig5_denoising.py       Fig. 5  sequence denoising + parity
|   |-- fig6_robustness.py      Fig. 6  robustness comparison
|   |-- fig7_stability.py       Fig. 7  parameter stability
|   `-- fig8_efficiency.py      Fig. 8  data efficiency
|
`-- results/                    Experiment outputs (committed for fast reproduction)
    |-- stage1/                 Candidate equations from PySR
    |-- stage2/                 Fitted parameters + validation PDFs
    |-- robustness/             Per-noise-level formulas, MLP models, comparisons
    |-- efficiency/             Data-efficiency sweep CSV
    `-- figures/                Final PDFs used in the paper
```

---

## Quick start

### 1. Install

```bash
git clone https://github.com/<user>/<repo>.git
cd <repo>
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate
pip install -r requirements.txt
```

`pysr` requires a Julia install; see the
[PySR docs](https://astroautomata.com/PySR/) for the one-time setup
(`python -c "import pysr; pysr.install()"`).

### 2. Reproduce every figure from the committed results (fast)

All experiment outputs needed to render the figures live under
`results/`, so the figure scripts run in seconds:

```bash
python -m plotting.fig1_fit_residual
python -m plotting.fig4_degradation
python -m plotting.fig5_denoising
python -m plotting.fig6_robustness
python -m plotting.fig7_stability
python -m plotting.fig8_efficiency
```

PDFs land in `results/figures/`.

### 3. Rebuild the entire pipeline from scratch (slow)

```bash
python -m src.data_processing      # build data/train_dataset_ready.csv
python -m src.stage1_exploration   # PySR formula discovery
python -m src.stage2_fitting       # curve_fit alpha/beta/gamma/delta
python -m src.exp_robustness       # noise sweep  (hours)
python -m src.exp_efficiency       # size sweep   (hours)
```

Then rerun the `plotting.*` scripts.

---

## The formula

The two-stage symbolic regression + physics-informed fit recovers

```
                              C_in
C(x) = -----------------------------------------------
            alpha * x
       ---------------------------------------  +  delta
       max(Area - beta * sqrt(x/v) + gamma, 0.1)
```

The Stage-2 parameters are persisted to
`results/stage2/final_parameters.txt`. Their stability across noise
levels is analysed in Figure 7.

---

## Conventions

- **Random seeds** are pinned (`random_state=42` throughout).
- **Concentration scaling**: raw CFD values (~1e-7 kg/m^3) are multiplied
  by `SCALE = 1e7` before fitting to avoid numerical issues; axis labels
  keep the original physical units.
- **Case-wise splitting**: train/test splits group by `Case` ID
  (never per row) to prevent leakage between correlated neighbouring
  points along the same tunnel geometry.
- **Plot style**: every figure uses the shared `viz_config.VizConfig`
  style (Times New Roman, deep-blue / red / green / grey palette).

---

## Citation

If you use this code or the framework in academic work, please cite:

```bibtex
@article{<citekey>,
  title   = {Hybrid Symbolic-Regression Framework for Pollutant Concentration Prediction},
  author  = {...},
  journal = {...},
  year    = {2026}
}
```

---

## License

Released under the [MIT License](LICENSE).
