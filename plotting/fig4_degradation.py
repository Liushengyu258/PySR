"""Figure 4 - performance-degradation curve (replica of Visualization_1.ipynb)."""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotting._paths import ROBUSTNESS_DIR, FIG_DIR
from viz_config import VizConfig

VizConfig.set_style()


def main() -> None:
    csv_path = ROBUSTNESS_DIR / "final_summary_r2.csv"
    if not csv_path.exists():
        print(f"Note: {csv_path} missing - using synthetic data for the demo.")
        x_raw = np.array([0, 0.1, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6,
                          0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
        y_pysr = np.array([0.99, 0.99, 0.98, 0.97, 0.96, 0.96, 0.96,
                           0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.74,
                           0.72, 0.70, 0.65, 0.59, 0.51])
    else:
        df = pd.read_csv(csv_path)
        x_raw = df["Noise_Ratio"].values
        y_pysr = df["R2_Direct_PySR"].values

    fig, ax = plt.subplots(figsize=(10, 7))
    cliff_x = 0.475                  # empirical breakdown point
    max_x = max(max(x_raw), 2.0)

    ax.axvspan(-0.05, cliff_x, color=VizConfig.COLOR_SUCCESS, alpha=0.08, zorder=0)
    ax.axvspan(cliff_x, max_x + 0.1, color=VizConfig.COLOR_HIGHLIGHT, alpha=0.08, zorder=0)
    ax.axvline(cliff_x, color=VizConfig.COLOR_SECONDARY, linestyle="--",
               linewidth=1.5, zorder=1)
    ax.plot(x_raw, y_pysr, marker="o", markersize=8, linewidth=2.5,
            color=VizConfig.COLOR_MAIN, zorder=2,
            label="Direct Symbolic Regression (Baseline)",
            markeredgecolor="white", markeredgewidth=1.5)

    text_y = 0.05
    ax.text(cliff_x / 2, text_y, "Robust Zone", color=VizConfig.COLOR_SUCCESS,
            fontsize=VizConfig.LABEL_SIZE, fontweight="bold", ha="center", va="bottom")
    ax.text(cliff_x + (max_x - cliff_x) / 2, text_y, "Failure Zone",
            color=VizConfig.COLOR_HIGHLIGHT, fontsize=VizConfig.LABEL_SIZE,
            fontweight="bold", ha="center", va="bottom")
    ax.text(cliff_x, 0.5, "Critical Breakdown Point", color=VizConfig.COLOR_AXIS,
            fontsize=12, ha="center", va="bottom", fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.7))

    x_ticks = np.arange(0, max_x + 0.1, 0.2)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f"{int(v*100)}%" for v in x_ticks],
                       fontsize=VizConfig.TICK_SIZE)
    ax.tick_params(axis="y", labelsize=VizConfig.TICK_SIZE)

    ax.set_xlabel("Noise Level (%)", fontsize=VizConfig.LABEL_SIZE, labelpad=10)
    ax.set_ylabel(r"Coefficient of Determination ($R^2$)",
                  fontsize=VizConfig.LABEL_SIZE, labelpad=10)
    ax.set_title("Model Performance Degradation Curve",
                 fontsize=VizConfig.TITLE_SIZE, pad=20, fontweight="bold")
    ax.legend(fontsize=VizConfig.LEGEND_SIZE, loc="upper right",
              frameon=True, facecolor="white", framealpha=1)
    ax.grid(True, linestyle="--", alpha=0.4, color=VizConfig.COLOR_GRID, zorder=1)
    ax.set_xlim(0, 2.05)
    ax.set_ylim(-0.05, 1.1)

    plt.tight_layout()
    out = FIG_DIR / "fig4_degradation.pdf"
    plt.savefig(out, dpi=VizConfig.DPI)
    print(f"Saved: {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
