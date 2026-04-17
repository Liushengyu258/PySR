"""Pipeline modules for the hybrid symbolic-regression study.

Run each stage directly, for example:
    python -m src.data_processing
    python -m src.stage1_exploration
    python -m src.stage2_fitting
    python -m src.exp_robustness
    python -m src.exp_efficiency
"""
from ._bootstrap import PROJECT_ROOT, DATA_DIR, RESULTS_DIR, FIG_DIR  # noqa: F401
