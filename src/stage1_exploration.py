"""Stage 1 - data-driven formula discovery with PySR.

Runs symbolic regression on a random 5 000-sample subset of the training
data, after splitting cases 70/30 to avoid leakage, and saves every
candidate equation to ``results/stage1/stage1_all_equations.csv``.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pysr import PySRRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from src._bootstrap import DATA_DIR, RESULTS_DIR

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCALE = 1e7                                   # ~1e-7 -> ~1.0 for search friendliness
OUTPUT_DIR = RESULTS_DIR / "stage1"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PYSR_PARAMS = dict(
    niterations=150,
    populations=30,
    maxsize=25,
    binary_operators=["+", "*", "-", "/"],
    unary_operators=["exp", "log", "sqrt", "square", "inv(x)=1/x"],
    extra_sympy_mappings={"inv": lambda x: 1 / x},
    model_selection="best",
    temp_equation_file=True,
    delete_tempfiles=False,
    verbosity=1,
)

FEATURE_NAMES = ["V_in", "C_in", "Area", "Distance"]


def main() -> None:
    print("Loading data and performing a 7:3 case-wise split...")
    df = pd.read_csv(DATA_DIR / "train_dataset_ready.csv")
    df["C_in"] *= SCALE
    df["C_out"] *= SCALE

    # Case-wise split (prevents leakage from correlated points in the same case)
    unique_cases = df["Case"].unique()
    train_cases, test_cases = train_test_split(unique_cases, test_size=0.3, random_state=42)
    train_df = df[df["Case"].isin(train_cases)]
    test_df = df[df["Case"].isin(test_cases)]
    print(f"Train cases: {len(train_cases)}, test cases: {len(test_cases)}")

    X_train = train_df[FEATURE_NAMES].values
    y_train = train_df["C_out"].values
    X_test = test_df[FEATURE_NAMES].values
    y_test = test_df["C_out"].values

    # Sub-sample 5 000 rows for PySR (symbolic regression is not very sample-hungry)
    np.random.seed(42)
    sub_idx = np.random.choice(len(X_train), 5000, replace=False)

    print("\n>>> Starting Stage 1: pure data-driven exploration...")
    model = PySRRegressor(**PYSR_PARAMS)
    model.fit(X_train[sub_idx], y_train[sub_idx], variable_names=FEATURE_NAMES)

    equations_path = OUTPUT_DIR / "stage1_all_equations.csv"
    model.equations_.to_csv(equations_path)

    r2 = r2_score(y_test, model.predict(X_test))
    print("\n" + "=" * 40)
    print(f"Stage 1 exploration complete!")
    print(f"Full test-set R^2 (unseen cases): {r2:.5f}")
    print(f"All candidate formulas saved to: {equations_path}")
    print("=" * 40)
    print("\nRecommended best formula (SymPy form):")
    print(model.sympy())


if __name__ == "__main__":
    main()
