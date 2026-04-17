"""Data-efficiency experiment (Figure 8 data source).

At a fixed noise level (50 %), sweeps the training-set size from 100 up
to the full 44 400-sample pool and repeats each setting ``N_REPEATS``
times.  The aggregated R^2 stats are written to
``results/efficiency/Data_Efficiency_Curve.csv``.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pysr import PySRRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

from src._bootstrap import DATA_DIR, RESULTS_DIR

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATA_SIZES = [100, 200, 300, 400, 500, 750, 1000, 2000, 3000, 4000, 5000,
              7500, 10000, 20000, 30000, 44400]
FIXED_NOISE = 0.5      # 50 % Gaussian noise on the target
N_REPEATS = 20
SCALE = 1e7
FEATURE_NAMES = ["V_in", "C_in", "Area", "Distance"]

OUTPUT_DIR = RESULTS_DIR / "efficiency"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    print("Loading data...")
    df = pd.read_csv(DATA_DIR / "train_dataset_ready.csv")
    df["C_in"] *= SCALE
    df["C_out"] *= SCALE

    unique_cases = df["Case"].unique()
    train_cases, test_cases_fixed = train_test_split(
        unique_cases, test_size=0.2, random_state=42)
    test_df = df[df["Case"].isin(test_cases_fixed)]
    X_test = test_df[FEATURE_NAMES].values
    y_test_clean = test_df["C_out"].values

    train_df_pool = df[df["Case"].isin(train_cases)]
    pool_idx = np.arange(len(train_df_pool))
    print(f"Data ready. Each experiment is repeated {N_REPEATS} times.")

    results_summary = []

    for size in DATA_SIZES:
        print(f"\n{'=' * 40}\nEvaluating training size: {size}\n{'=' * 40}")
        current_size = min(size, len(pool_idx))
        r2_scores_hybrid = []

        for i in range(N_REPEATS):
            seed = 42 + size + i
            np.random.seed(seed)

            sampled_idx = np.random.choice(pool_idx, current_size, replace=False)
            X_train = train_df_pool.iloc[sampled_idx][FEATURE_NAMES].values
            y_clean = train_df_pool.iloc[sampled_idx]["C_out"].values

            # Inject noise
            noise = np.random.normal(0, FIXED_NOISE * y_clean)
            y_noisy = np.maximum(y_clean + noise, 1e-6)

            # MLP denoiser
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_train)
            mlp = MLPRegressor(
                hidden_layer_sizes=(128, 64, 32), activation="relu",
                learning_rate_init=0.001, max_iter=500, random_state=seed,
            )
            try:
                mlp.fit(X_scaled, y_noisy)
            except Exception as e:                     # noqa: BLE001
                print(f"    [Warning] MLP fit failed: {e}")
                continue

            # Hybrid PySR on MLP-denoised labels (cap PySR inputs at 2000 for speed)
            pysr_n = min(current_size, 2000)
            pysr_idx = np.random.choice(len(X_train), pysr_n, replace=False)
            y_denoised = np.maximum(mlp.predict(X_scaled[pysr_idx]), 1e-6)

            model_hybrid = PySRRegressor(
                niterations=40, populations=15,
                binary_operators=["+", "*", "-", "/"],
                unary_operators=["inv(x)=1/x", "sqrt", "square"],
                extra_sympy_mappings={"inv": lambda x: 1 / x},
                verbosity=0, temp_equation_file=True, delete_tempfiles=True,
            )
            r2 = -1.0
            try:
                model_hybrid.fit(X_train[pysr_idx], y_denoised, variable_names=FEATURE_NAMES)
                y_pred = model_hybrid.predict(X_test)
                if not np.all(np.isfinite(y_pred)):
                    print(f"    Repeat {i+1}/{N_REPEATS} | singular formula (Inf/NaN) - skip")
                    r2 = 0.0
                else:
                    r2 = r2_score(y_test_clean, y_pred)
                    print(f"    Repeat {i+1}/{N_REPEATS} | Hybrid R^2 = {r2:.4f}")
            except Exception as e:                     # noqa: BLE001
                print(f"    Repeat {i+1}/{N_REPEATS} | PySR error: {e}")
                r2 = 0.0
            r2_scores_hybrid.append(r2)

        valid = [s for s in r2_scores_hybrid if s > 0.0]
        mean_r2 = float(np.mean(valid)) if valid else 0.0
        std_r2 = float(np.std(valid)) if valid else 0.0
        print(f"  >>> size {current_size}: mean R^2 = {mean_r2:.4f} (std: {std_r2:.4f})")

        results_summary.append({
            "Training_Size": current_size,
            "Mean_R2": mean_r2,
            "Std_R2": std_r2,
            "Raw_Scores": str(r2_scores_hybrid),
        })
        # Persist after every size in case the run is interrupted
        pd.DataFrame(results_summary).to_csv(
            OUTPUT_DIR / "Data_Efficiency_Curve.csv", index=False)

    print("\n" + "=" * 50)
    print(f"Done. Results: {OUTPUT_DIR / 'Data_Efficiency_Curve.csv'}")
    print("=" * 50)


if __name__ == "__main__":
    main()
