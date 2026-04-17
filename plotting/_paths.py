"""Resolve project-root paths for the plotting scripts."""
from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
ROBUSTNESS_DIR = RESULTS_DIR / "robustness"
EFFICIENCY_DIR = RESULTS_DIR / "efficiency"
STAGE1_DIR = RESULTS_DIR / "stage1"
STAGE2_DIR = RESULTS_DIR / "stage2"
FIG_DIR = RESULTS_DIR / "figures"

FIG_DIR.mkdir(parents=True, exist_ok=True)
os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
