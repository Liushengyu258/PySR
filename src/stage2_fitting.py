"""Stage 2 - physics-informed hypothesis fit.

Takes the structural prior discovered in Stage 1 and fits the four
physical parameters (alpha, beta, gamma, delta) via non-linear
least squares; saves the final parameters plus two validation figures.

Hypothesis formula::

    C(x) = C_in / [ (a * x) / max(Area - b * sqrt(x/v) + c, 0.1) + d ]
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, mean_squared_error

from src._bootstrap import DATA_DIR, RESULTS_DIR, FIG_DIR
from viz_config import VizConfig

VizConfig.set_style()

SCALE = 1e7
OUTPUT_DIR = RESULTS_DIR / "stage2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def hypothesis_formula(X, a, b, c, d):
    v, area, dist, c_in = X
    time_scale = np.sqrt(dist / (v + 1e-6))
    effective_term = area - b * time_scale + c
    denominator = (a * dist) / np.maximum(effective_term, 0.1) + d
    return c_in / denominator


def main() -> None:
    data_path = DATA_DIR / "train_dataset_ready.csv"
    if not data_path.exists():
        raise FileNotFoundError(f"ERROR: {data_path} not found")

    df = pd.read_csv(data_path)
    df["C_in_scaled"] = df["C_in"] * SCALE
    df["C_out_scaled"] = df["C_out"] * SCALE

    V_in = df["V_in"].values
    Area = df["Area"].values
    Dist = df["Distance"].values
    C_in_scaled = df["C_in_scaled"].values
    C_out_scaled = df["C_out_scaled"].values
    X_data = (V_in, Area, Dist, C_in_scaled)

    # --- non-linear least squares -----------------------------------------
    print("Running non-linear least-squares fit...")
    p0 = [0.08, 0.6, 26.0, 1.0]  # alpha, beta, gamma, delta seeded from Stage 1
    popt, _ = curve_fit(
        hypothesis_formula, X_data, C_out_scaled, p0=p0, maxfev=20000,
        bounds=([0, 0, 0, 0.5], [2.0, 10.0, 100.0, 2.0]),
    )
    a_opt, b_opt, c_opt, d_opt = popt
    y_pred = hypothesis_formula(X_data, *popt)
    r2 = r2_score(C_out_scaled, y_pred)
    rmse = np.sqrt(mean_squared_error(C_out_scaled, y_pred))

    print("\n" + "=" * 40)
    print("Fit succeeded - best parameters:")
    print(f"alpha (a) = {a_opt:.6f}")
    print(f"beta  (b) = {b_opt:.6f}")
    print(f"gamma (c) = {c_opt:.6f}")
    print(f"delta (d) = {d_opt:.6f}")
    print(f"R^2  = {r2:.6f}")
    print(f"RMSE = {rmse:.6f}")

    with open(OUTPUT_DIR / "final_parameters.txt", "w") as f:
        f.write(f"R2 Score: {r2:.6f}\nRMSE: {rmse:.6f}\n")
        f.write(f"alpha: {a_opt}\nbeta: {b_opt}\ngamma: {c_opt}\ndelta: {d_opt}\n")

    # --- validation plot 1: per-case decay curves -------------------------
    print("\nPlotting decay curves...")
    np.random.seed(42)
    sample_cases = np.random.choice(df["Case"].unique(), 4, replace=False)
    unit_c = r"($10^{-7} \cdot \text{kg/m}^3$)"

    fig1 = plt.figure(figsize=(15, 10))
    for i, case_id in enumerate(sample_cases):
        case_data = df[df["Case"] == case_id].sort_values("Distance")
        dist_case = case_data["Distance"].values
        pred_case = hypothesis_formula(
            (case_data["V_in"].values, case_data["Area"].values,
             dist_case, case_data["C_in_scaled"].values), *popt,
        )
        ax = plt.subplot(2, 2, i + 1)
        ax.plot(dist_case, case_data["C_out_scaled"].values, "o",
                color=VizConfig.COLOR_AXIS, markersize=4, alpha=0.6,
                label="CFD Data", rasterized=True)
        ax.plot(dist_case, pred_case, color=VizConfig.COLOR_HIGHLIGHT,
                linewidth=2, label="Proposed Formula")
        ax.set_title(
            f"Case: {case_id} (V={case_data['V_in'].values[0]:.2f} m/s, "
            f"Area={case_data['Area'].values[0]:.1f} $m^2$)",
            fontsize=VizConfig.TITLE_SIZE,
        )
        ax.set_xlabel("Distance (m)", fontsize=VizConfig.LABEL_SIZE)
        ax.set_ylabel(f"Concentration {unit_c}", fontsize=VizConfig.LABEL_SIZE)
        ax.tick_params(axis="both", labelsize=VizConfig.TICK_SIZE)
        ax.legend(fontsize=VizConfig.LEGEND_SIZE)
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    out1 = OUTPUT_DIR / "1.pdf"
    plt.savefig(out1, dpi=VizConfig.DPI)
    plt.savefig(FIG_DIR / "stage2_decay_curves.pdf", dpi=VizConfig.DPI)
    plt.close(fig1)

    # --- validation plot 2: parity ----------------------------------------
    print("Plotting parity plot...")
    plt.figure(figsize=(8, 8))
    plt.plot(C_out_scaled, y_pred, "o", color=VizConfig.COLOR_MAIN,
             markersize=2, alpha=0.1, rasterized=True)
    plt.plot([C_out_scaled.min(), C_out_scaled.max()],
             [C_out_scaled.min(), C_out_scaled.max()],
             color=VizConfig.COLOR_HIGHLIGHT, linestyle="--", linewidth=2)
    plt.xlabel(f"True Concentration {unit_c}",
               fontsize=VizConfig.LABEL_SIZE, labelpad=10)
    plt.ylabel(f"Predicted Concentration {unit_c}",
               fontsize=VizConfig.LABEL_SIZE, labelpad=10)
    plt.title(f"Parity Plot ($R^2={r2:.4f}$)",
              fontsize=VizConfig.TITLE_SIZE, pad=20)
    plt.xticks(fontsize=VizConfig.TICK_SIZE)
    plt.yticks(fontsize=VizConfig.TICK_SIZE)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out2 = OUTPUT_DIR / "2.pdf"
    plt.savefig(out2, dpi=VizConfig.DPI)
    plt.savefig(FIG_DIR / "stage2_parity.pdf", dpi=VizConfig.DPI)
    plt.close()

    print(f"\nDone. Figures: {out1}, {out2}")


if __name__ == "__main__":
    main()
