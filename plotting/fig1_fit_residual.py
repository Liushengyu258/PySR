"""Figure 1 - combined fit + residual analysis (replica of Visualization.ipynb)."""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

from plotting._paths import DATA_DIR, FIG_DIR
from viz_config import VizConfig

VizConfig.set_style()
SCALE = 1e7


def hypothesis_formula(X, a, b, c, d):
    v, area, dist, c_in = X
    time_scale = np.sqrt(dist / (v + 1e-6))
    effective_term = area - b * time_scale + c
    denominator = (a * dist) / np.maximum(effective_term, 0.1) + d
    return c_in / denominator


def main() -> None:
    csv = DATA_DIR / "train_dataset_ready.csv"
    if not csv.exists():
        raise FileNotFoundError(f"ERROR: {csv} not found")
    df = pd.read_csv(csv)

    df["C_in_scaled"] = df["C_in"] * SCALE
    df["C_out_scaled"] = df["C_out"] * SCALE
    V_in, Area, Dist = df["V_in"].values, df["Area"].values, df["Distance"].values
    C_in_scaled = df["C_in_scaled"].values
    C_out_scaled = df["C_out_scaled"].values
    X_data = (V_in, Area, Dist, C_in_scaled)

    # Block A: hypothesis fit
    popt, _ = curve_fit(
        hypothesis_formula, X_data, C_out_scaled,
        p0=[0.08, 0.6, 26.0, 1.0], maxfev=20000,
        bounds=([0, 0, 0, 0.5], [2.0, 10.0, 100.0, 2.0]),
    )
    y_pred_fit = hypothesis_formula(X_data, *popt)
    r2_fit = r2_score(C_out_scaled, y_pred_fit)
    print(f"Block A fit succeeded (R^2 = {r2_fit:.4f}).")

    # Block B: residuals under a known second parameter set
    a2, b2, c2, d2 = 9.851695, 10.058320, 34.511347, -14.437245
    C_in_raw = df["C_in"].values * SCALE
    C_true_raw = df["C_out"].values * SCALE
    effective_area_2 = Area + c2 * np.sqrt(V_in) + d2
    denominator_2 = (Dist / effective_area_2) + b2
    C_pred_2 = C_in_raw * (a2 / denominator_2)
    residuals_2 = C_true_raw - C_pred_2
    std_residuals_2 = residuals_2 / np.std(residuals_2)
    r2_2 = r2_score(C_true_raw, C_pred_2)

    # Combined figure
    print("Rendering combined figure...")
    fig = plt.figure(figsize=(22, 12))
    outer_gs = gridspec.GridSpec(1, 2, width_ratios=[1.1, 1], wspace=0.15)
    left_gs = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer_gs[0],
                                               hspace=0.25, wspace=0.2)
    np.random.seed(42)
    sample_cases = np.random.choice(df["Case"].unique(), 4, replace=False)
    unit_c = r"($10^{-7} \cdot \text{kg/m}^3$)"

    for i, case_id in enumerate(sample_cases):
        ax = fig.add_subplot(left_gs[i // 2, i % 2])
        if i == 0:
            ax.text(-0.15, 1.15, "(a)", transform=ax.transAxes, fontsize=26,
                    fontweight="bold", va="top", ha="right",
                    color=VizConfig.COLOR_AXIS)
        case_data = df[df["Case"] == case_id].sort_values("Distance")
        pred_c = hypothesis_formula(
            (case_data["V_in"].values, case_data["Area"].values,
             case_data["Distance"].values, case_data["C_in_scaled"].values),
            *popt,
        )
        ax.plot(case_data["Distance"].values, case_data["C_out_scaled"].values, "o",
                color=VizConfig.COLOR_MAIN, markersize=5, alpha=0.7,
                label="CFD Data", rasterized=True,
                markeredgecolor="white", markeredgewidth=0.5)
        ax.plot(case_data["Distance"].values, pred_c,
                color=VizConfig.COLOR_HIGHLIGHT, linewidth=2.5, label="Proposed Formula")
        ax.set_title(
            f"Case: {case_id} (V={case_data['V_in'].values[0]:.2f}m/s, "
            f"Area={case_data['Area'].values[0]:.1f}$m^2$)",
            fontsize=VizConfig.LABEL_SIZE, pad=12,
        )
        ax.set_xlabel("Distance (m)", fontsize=VizConfig.LABEL_SIZE, labelpad=8)
        ax.set_ylabel(f"Concentration {unit_c}",
                      fontsize=VizConfig.LABEL_SIZE, labelpad=8)
        ax.tick_params(axis="both", labelsize=VizConfig.TICK_SIZE)
        ax.legend(fontsize=VizConfig.LEGEND_SIZE)
        ax.grid(True, alpha=0.3)

    right_gs = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer_gs[1], hspace=0.35)
    ax_parity = fig.add_subplot(right_gs[0])
    ax_parity.text(-0.1, 1.1, "(b)", transform=ax_parity.transAxes, fontsize=26,
                   fontweight="bold", va="top", ha="right", color=VizConfig.COLOR_AXIS)
    ax_parity.plot(C_out_scaled, y_pred_fit, "o", color=VizConfig.COLOR_MAIN,
                   markersize=3, alpha=0.2, rasterized=True)
    ax_parity.plot([C_out_scaled.min(), C_out_scaled.max()],
                   [C_out_scaled.min(), C_out_scaled.max()],
                   linestyle="--", color=VizConfig.COLOR_HIGHLIGHT, linewidth=2)
    ax_parity.set_xlabel(f"True Concentration {unit_c}",
                         fontsize=VizConfig.LABEL_SIZE, labelpad=10)
    ax_parity.set_ylabel(f"Predicted Concentration {unit_c}",
                         fontsize=VizConfig.LABEL_SIZE, labelpad=10)
    ax_parity.set_title(f"Parity Plot ($R^2={r2_fit:.4f}$)",
                        fontsize=VizConfig.TITLE_SIZE, pad=15, fontweight="bold")
    ax_parity.tick_params(labelsize=VizConfig.TICK_SIZE)
    ax_parity.grid(True, alpha=0.3)

    ax_resid = fig.add_subplot(right_gs[1])
    ax_resid.text(-0.1, 1.1, "(c)", transform=ax_resid.transAxes, fontsize=26,
                  fontweight="bold", va="top", ha="right", color=VizConfig.COLOR_AXIS)
    ax_resid.plot(C_pred_2, std_residuals_2, "o",
                  color=VizConfig.COLOR_PALETTE[5], markersize=5,
                  alpha=0.2, rasterized=True, markeredgecolor="none")
    ax_resid.axhline(0, color=VizConfig.COLOR_AXIS, linestyle="--", linewidth=1.5)
    ax_resid.axhline(2, color=VizConfig.COLOR_WARNING, linestyle=":", linewidth=2)
    ax_resid.axhline(-2, color=VizConfig.COLOR_WARNING, linestyle=":", linewidth=2)
    ax_resid.set_xlabel(r"Predicted Concentration ($10^7 \cdot \text{kg/m}^3$)",
                        fontsize=VizConfig.LABEL_SIZE, labelpad=10)
    ax_resid.set_ylabel("Standardized Residuals (Dimensionless)",
                        fontsize=VizConfig.LABEL_SIZE, labelpad=10)
    ax_resid.set_title(
        f"Residual Plot (Check for Heteroscedasticity)\n$R^2 = {r2_2:.4f}$",
        fontsize=VizConfig.TITLE_SIZE, fontweight="bold", pad=15,
    )
    ax_resid.tick_params(labelsize=VizConfig.TICK_SIZE)
    ax_resid.grid(True, alpha=0.3)

    output = FIG_DIR / "fig1_fit_residual.pdf"
    plt.savefig(output, dpi=300, bbox_inches="tight", pad_inches=0.1)
    print(f"Saved: {output}")
    plt.close(fig)


if __name__ == "__main__":
    main()
