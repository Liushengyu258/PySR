"""Robustness experiment (Figures 6 & 7 data source).

Sweeps noise levels 0 %..200 % and at each level trains:
    1. Direct PySR         (baseline - symbolic regression on noisy data)
    2. MLP                 (non-linear denoiser, 128-64-32)
    3. Hybrid PySR         (our method - symbolic regression on MLP-denoised data)

Per-noise outputs land in ``results/robustness/Noise_<pct>pct/``:
    * ``all_formulas_direct_<pct>pct.csv``
    * ``all_formulas_hybrid_<pct>pct.csv``
    * ``mlp_loss_history.csv``
    * ``mlp_model.pkl``
    * ``scaler_X.pkl``
    * ``predictions_comparison.csv``

The top-level ``results/robustness/final_summary_r2.csv`` is the
source for the robustness curve in Figure 6.
"""
from __future__ import annotations
import os
import joblib
import numpy as np
import pandas as pd
from pysr import PySRRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

from src._bootstrap import DATA_DIR, RESULTS_DIR

NOISE_LEVELS = [
    0, 0.1, 0.2, 0.3, 0.35, 0.40, 0.45, 0.50, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,
    0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
]
BASE_DIR = RESULTS_DIR / "robustness"
BASE_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_NAMES = ["V_in", "C_in", "Area", "Distance"]
SCALE = 1e7


def _pysr_regressor() -> PySRRegressor:
    return PySRRegressor(
        niterations=150,
        populations=30,
        maxsize=25,
        binary_operators=["+", "*", "-", "/"],
        unary_operators=["exp", "log", "sqrt", "square", "inv(x)=1/x"],
        extra_sympy_mappings={"inv": lambda x: 1 / x},
        temp_equation_file=True,
        delete_tempfiles=False,
        verbosity=0,
    )


def main() -> None:
    print("Loading data and performing a case-wise split...")
    df = pd.read_csv(DATA_DIR / "train_dataset_ready.csv")
    df["C_in"] *= SCALE
    df["C_out"] *= SCALE

    unique_cases = df["Case"].unique()
    train_cases, test_cases = train_test_split(unique_cases, test_size=0.3, random_state=42)
    train_df = df[df["Case"].isin(train_cases)]
    test_df = df[df["Case"].isin(test_cases)]
    print(f"Train cases: {len(train_cases)}, test cases: {len(test_cases)}")

    X_train_clean = train_df[FEATURE_NAMES].values
    y_train_clean = train_df["C_out"].values
    X_test = test_df[FEATURE_NAMES].values
    y_test_clean = test_df["C_out"].values
    test_cases_col = test_df["Case"].values
    test_dist_col = test_df["Distance"].values

    summary = []

    for noise_pct in NOISE_LEVELS:
        noise_label = f"{int(noise_pct * 100)}pct"
        path = BASE_DIR / f"Noise_{noise_label}"
        path.mkdir(parents=True, exist_ok=True)
        print(f"\n>>> Noise level {noise_pct * 100:.0f}%")

        # --- inject noise -------------------------------------------------
        np.random.seed(42)
        if noise_pct > 0:
            noise_train = np.random.normal(0, noise_pct * y_train_clean)
            noise_test = np.random.normal(0, noise_pct * y_test_clean)
        else:
            noise_train = noise_test = 0
        y_train_noisy = np.maximum(y_train_clean + noise_train, 1e-6)
        y_test_noisy = np.maximum(y_test_clean + noise_test, 1e-6)

        # --- Task 1: Direct PySR -----------------------------------------
        print("    [Task 1] Direct PySR...")
        sub_idx = np.random.choice(len(y_train_noisy), 5000, replace=False)
        model_direct = _pysr_regressor()
        model_direct.fit(
            X_train_clean[sub_idx], y_train_noisy[sub_idx],
            variable_names=FEATURE_NAMES,
        )
        model_direct.equations_.to_csv(path / f"all_formulas_direct_{noise_label}.csv")
        y_pred_direct = model_direct.predict(X_test)

        # --- Task 2: MLP --------------------------------------------------
        print("    [Task 2] Training MLP...")
        scaler_X = StandardScaler()
        X_train_scaled = scaler_X.fit_transform(X_train_clean)
        X_test_scaled = scaler_X.transform(X_test)
        mlp = MLPRegressor(
            hidden_layer_sizes=(128, 64, 32),
            learning_rate_init=0.001,
            activation="relu",
            max_iter=1000,
            random_state=42,
            early_stopping=False,
        )
        mlp.fit(X_train_scaled, y_train_noisy)
        pd.DataFrame(mlp.loss_curve_, columns=["Loss"]).to_csv(path / "mlp_loss_history.csv")
        y_pred_mlp = mlp.predict(X_test_scaled)

        # --- Task 3: Hybrid PySR -----------------------------------------
        print("    [Task 3] Hybrid PySR...")
        y_denoised_train_sub = mlp.predict(X_train_scaled[sub_idx])
        model_hybrid = _pysr_regressor()
        model_hybrid.fit(
            X_train_clean[sub_idx], y_denoised_train_sub,
            variable_names=FEATURE_NAMES,
        )
        model_hybrid.equations_.to_csv(path / f"all_formulas_hybrid_{noise_label}.csv")
        y_pred_hybrid = model_hybrid.predict(X_test)

        # --- save predictions & metrics ----------------------------------
        pd.DataFrame({
            "Case": test_cases_col, "Distance": test_dist_col,
            "True_Clean": y_test_clean, "True_Noisy": y_test_noisy,
            "Pred_Direct_PySR": y_pred_direct,
            "Pred_MLP": y_pred_mlp,
            "Pred_Hybrid_PySR": y_pred_hybrid,
        }).to_csv(path / "predictions_comparison.csv", index=False)

        r2_direct = r2_score(y_test_clean, y_pred_direct)
        r2_mlp = r2_score(y_test_clean, y_pred_mlp)
        r2_hybrid = r2_score(y_test_clean, y_pred_hybrid)
        summary.append({
            "Noise_Ratio": noise_pct,
            "R2_Direct_PySR": r2_direct,
            "R2_MLP": r2_mlp,
            "R2_Hybrid_PySR": r2_hybrid,
        })
        print(f"    R^2 Direct={r2_direct:.4f}, Hybrid={r2_hybrid:.4f}")

        joblib.dump(mlp, path / "mlp_model.pkl")
        joblib.dump(scaler_X, path / "scaler_X.pkl")

    pd.DataFrame(summary).to_csv(BASE_DIR / "final_summary_r2.csv", index=False)
    print("\n" + "=" * 50)
    print("All noise levels finished.")
    print(f"Summary:  {BASE_DIR / 'final_summary_r2.csv'}")
    print(f"Per-noise CSVs under:  {BASE_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
