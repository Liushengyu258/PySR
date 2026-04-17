# A Hybrid Symbolic-Regression Framework for Pollutant Concentration Prediction

This project implements a hybrid framework that combines **Symbolic Regression
(PySR)** with physics-informed hypotheses to predict the spatial distribution
of pollutant concentration.  It covers the full pipeline: raw CFD data
ingestion, formula discovery, parameter fitting, robustness / data-efficiency
experiments, and publication-quality figure generation.

---

## Project layout

```
PySR/
├── README.md
├── .gitignore
├── viz_config.py                    # Global matplotlib style (fonts, palette, sizes)
│
├── data/                            # Raw and processed datasets
│   ├── cases.csv                    # Per-case inlet conditions (V_in, C_in, Area)
│   ├── summary_0_499.csv            # Raw CFD concentration profiles
│   ├── cfd_lhs_cases.csv            # Cases sampled by Latin Hypercube Sampling
│   ├── case.csv                     # Time-step table used by the Fluent batch runner
│   ├── train_dataset_ready.csv      # Merged long-format ML-ready dataset
│   └── Data_Efficiency_Curve.csv
│
├── notebooks/                       # Jupyter analysis pipeline
│   ├── 00_data_preparation/
│   │   ├── data.ipynb               # Clean & merge cases + summary -> train_dataset_ready
│   │   └── datasee.ipynb            # Quick per-case concentration-profile viewer
│   ├── 01_stage1_exploration/
│   │   └── Stage1.ipynb             # PySR data-driven formula discovery
│   ├── 02_stage2_verification/
│   │   └── Stage2.ipynb             # Physics-informed fit (curve_fit) for alpha/beta/gamma/delta
│   ├── 03_experiments/
│   │   ├── klw PySR.ipynb           # Robustness experiment (noise 0%-200%)  -> Fig. 6, 7
│   │   └── add.ipynb                # Data-efficiency experiment (100-44400 samples) -> Fig. 8
│   └── 04_visualization/
│       ├── Visualization.ipynb      # Fig. 1 - combined fit + residual analysis
│       ├── Visualization_1.ipynb    # Fig. 4 - performance degradation curve
│       ├── Visualization_2.ipynb    # Fig. 5 - sequence denoising effect
│       ├── Visualization_3.ipynb    # Fig. 6 - robustness comparison
│       ├── Visualization_4.ipynb    # Fig. 7 - parameter stability
│       └── Visualization_5.ipynb    # Fig. 8 - data efficiency
│
├── scripts/                         # Stand-alone Python scripts
│   ├── cfd_pipeline/                # CFD pre-processing & batch automation
│   │   ├── data_generate.py         # LHS -> cfd_lhs_cases.csv
│   │   ├── case_copy.py             # Re-organise Fluent case files
│   │   ├── extract_data.py          # Extract profiles from dpX_area.out
│   │   ├── run_automation_linux.py  # Generate Linux batch .sh scripts
│   │   └── fluent_template.jou      # Fluent Journal template
│   ├── lhs_sampling/                # LHS distribution plotting
│   │   ├── lhs.py
│   │   └── plot_lhs.py
│   ├── analysis_legacy/             # Early exploration scripts (superseded by notebooks)
│   │   ├── fig.py
│   │   ├── pysr1.py
│   │   ├── test2.py
│   │   └── test_pysr.py
│   └── _patch_notebooks.py          # Internal tool - inject project-root bootstrap cells
│
├── figures/                         # Publication-ready figures
│   ├── Formula_Performance.png
│   ├── lhs_distribution.pdf / .tiff
│   └── 9.pdf
│
├── docs/
│   └── UNTITLED.opju                # Origin project file
│
├── Stage1_Exploration/              # Output of Stage1.ipynb
├── Stage2_Hypothesis_Verification/  # Output of Stage2.ipynb
├── Refined_Results_v4/              # Robustness-experiment output (source for Fig. 6/7)
├── Data_Efficiency_Results/         # Data-efficiency output (source for Fig. 8)
└── outputs/                         # Raw PySR run directories (gitignored)
```

> **Path convention** — Every notebook begins with an auto-injected cell
> marked `# [auto] project-root setup`.  That cell walks up from the current
> working directory until it finds the folder containing `.gitignore`
> (the project root), then does `os.chdir(PROJECT_ROOT)` and appends the
> root to `sys.path`.  This way every relative path (`data/...`,
> `Stage1_Exploration/...`, `from viz_config import VizConfig`) keeps
> working no matter where the notebook is launched from.

---

## Workflow

1. **Build the dataset** — run `notebooks/00_data_preparation/data.ipynb` to
   produce `data/train_dataset_ready.csv`.
2. **Formula discovery** — run `notebooks/01_stage1_exploration/Stage1.ipynb`.
3. **Hypothesis verification** — run
   `notebooks/02_stage2_verification/Stage2.ipynb`.
4. **Experiments**
   * `notebooks/03_experiments/klw PySR.ipynb` &mdash; robustness study.
   * `notebooks/03_experiments/add.ipynb` &mdash; data-efficiency study.
5. **Figures** — run the notebooks under `notebooks/04_visualization/`.

---

## Conventions & notes

* **Colour scheme**
  * Deep blue — ground truth / core model
  * Red &mdash; fit line / highlight
  * Green &mdash; robust region
  * Grey &mdash; baseline / control group
* All random seeds are fixed (`random_state=42`) for reproducibility.
* Concentration values are pre-scaled by a factor of `1e7` throughout the
  pipeline.

---

## Requirements

Core dependencies:

```
numpy, pandas, scipy, scikit-learn, matplotlib, seaborn, torch, pysr
```

`pysr` requires a working Julia installation; see the
[PySR documentation](https://astroautomata.com/PySR/) for setup details.
