"""Shared path resolution so every pipeline script can be launched from any cwd.

Importing this module:
  * defines PROJECT_ROOT / DATA_DIR / RESULTS_DIR / FIG_DIR,
  * chdir's to PROJECT_ROOT (keeps every relative path in legacy code valid),
  * prepends PROJECT_ROOT to sys.path (so ``import viz_config`` works).
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
FIG_DIR = RESULTS_DIR / "figures"

for _d in (RESULTS_DIR, FIG_DIR):
    _d.mkdir(parents=True, exist_ok=True)

os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
