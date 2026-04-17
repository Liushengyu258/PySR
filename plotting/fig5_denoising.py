"""Figure 5 - sequence denoising + parity plot (replica of Visualization_2.ipynb)."""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from sklearn.metrics import r2_score

from plotting._paths import ROBUSTNESS_DIR, FIG_DIR
from viz_config import VizConfig

VizConfig.set_style()
TITLE_SIZE = VizConfig.TITLE_SIZE
LABEL_SIZE = VizConfig.LABEL_SIZE
TICK_SIZE = VizConfig.TICK_SIZE
LEGEND_SIZE = VizConfig.LEGEND_SIZE

UNIT_C = r"($10^{-7} \cdot \text{kg/m}^3$)"
UNIT_D = r"($\text{m}$)"


def _synthetic():
    dist = np.linspace(0, 1000, 200)
    clean = 10 * np.exp(-dist / 300) + 2 * np.sin(dist / 50)
    noisy = clean + np.random.normal(0, 1, size=len(dist))
    pred = clean + np.random.normal(0, 0.2, size=len(dist))
    return pd.DataFrame({
        "Distance": dist, "True_Clean": clean, "True_Noisy": noisy,
        "Pred_MLP": pred, "Case": "dp0",
    }), 0.85, 0.98, "dp0"


def main() -> None:
    input_path = ROBUSTNESS_DIR / "Noise_50pct" / "predictions_comparison.csv"
    if not input_path.exists():
        print(f"Warning: {input_path} missing - using synthetic data.")
        case_df, r2_noisy, r2_denoised, selected_case = _synthetic()
    else:
        df = pd.read_csv(input_path)
        selected_case = "dp0"
        case_df = df[df["Case"] == selected_case].sort_values("Distance")
        r2_noisy = r2_score(case_df["True_Clean"], case_df["True_Noisy"])
        r2_denoised = r2_score(case_df["True_Clean"], case_df["Pred_MLP"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # ---- (a) local sequence denoising ---------------------------------
    ax1.scatter(case_df["Distance"], case_df["True_Noisy"],
                color=VizConfig.COLOR_SECONDARY, alpha=0.5, s=20,
                label="Noisy Data (50%)", rasterized=True, edgecolors="none")
    ax1.scatter(case_df["Distance"], case_df["True_Clean"],
                color=VizConfig.COLOR_MAIN, alpha=0.8, s=20,
                label="Ground Truth (CFD)", rasterized=True, edgecolors="none")
    ax1.plot(case_df["Distance"], case_df["Pred_MLP"],
             color=VizConfig.COLOR_HIGHLIGHT, linestyle="-", linewidth=2.5,
             label="MLP Denoised Output")
    ax1.set_xlabel(f"Distance {UNIT_D}", fontsize=LABEL_SIZE, labelpad=10)
    ax1.set_ylabel(f"Concentration {UNIT_C}", fontsize=LABEL_SIZE, labelpad=10)
    ax1.set_title(f"(a) Local Sequence Denoising (Case: {selected_case})",
                  fontsize=TITLE_SIZE, pad=15, fontweight="bold")
    ax1.tick_params(labelsize=TICK_SIZE)
    ax1.legend(fontsize=LEGEND_SIZE, loc="upper right", frameon=True)
    ax1.grid(True, alpha=0.4, linestyle="--")

    # Inset zoom
    axins = ax1.inset_axes([0.45, 0.45, 0.35, 0.35])
    axins.scatter(case_df["Distance"], case_df["True_Noisy"],
                  color=VizConfig.COLOR_SECONDARY, alpha=0.5, s=20,
                  rasterized=True, edgecolors="none")
    axins.scatter(case_df["Distance"], case_df["True_Clean"],
                  color=VizConfig.COLOR_MAIN, alpha=0.8, s=20,
                  rasterized=True, edgecolors="none")
    axins.plot(case_df["Distance"], case_df["Pred_MLP"],
               color=VizConfig.COLOR_HIGHLIGHT, linestyle="-", linewidth=2.5)
    x1_, x2_ = 200, 400
    axins.set_xlim(x1_, x2_)
    mask_zoom = (case_df["Distance"] >= x1_) & (case_df["Distance"] <= x2_)
    y_seg = pd.concat([
        case_df.loc[mask_zoom, "True_Noisy"],
        case_df.loc[mask_zoom, "True_Clean"],
        case_df.loc[mask_zoom, "Pred_MLP"],
    ])
    if not y_seg.empty:
        y_min, y_max = y_seg.min(), y_seg.max()
        m = (y_max - y_min) * 0.1
        axins.set_ylim(y_min - m, y_max + m)
    axins.tick_params(labelsize=10)
    axins.grid(True, alpha=0.3, linestyle=":")
    axins.spines["bottom"].set_color(VizConfig.COLOR_AXIS)
    axins.spines["left"].set_color(VizConfig.COLOR_AXIS)
    mark_inset(ax1, axins, loc1=2, loc2=4, fc="none", ec="0.5", linestyle="--")

    # ---- (b) parity plot ---------------------------------------------
    ax2.scatter(case_df["True_Clean"], case_df["True_Noisy"],
                color=VizConfig.COLOR_SECONDARY, alpha=0.5, s=15,
                label=f"Raw Noise vs. Truth ($R^2 = {r2_noisy:.4f}$)",
                rasterized=True, edgecolors="none")
    ax2.scatter(case_df["True_Clean"], case_df["Pred_MLP"],
                color=VizConfig.COLOR_HIGHLIGHT, alpha=0.6, s=15,
                label=f"Denoised vs. Truth ($R^2 = {r2_denoised:.4f}$)",
                rasterized=True, edgecolors="none")
    all_vals = pd.concat([case_df["True_Clean"], case_df["True_Noisy"], case_df["Pred_MLP"]])
    ax2.plot([all_vals.min(), all_vals.max()],
             [all_vals.min(), all_vals.max()],
             color=VizConfig.COLOR_AXIS, linestyle="--", alpha=0.8,
             linewidth=1.5, zorder=3)
    ax2.set_xlabel(f"Ground Truth Concentration {UNIT_C}",
                   fontsize=LABEL_SIZE, labelpad=10)
    ax2.set_ylabel(f"Observed/Predicted Concentration {UNIT_C}",
                   fontsize=LABEL_SIZE, labelpad=10)
    ax2.set_title(f"(b) Parity Plot (Case: {selected_case})",
                  fontsize=TITLE_SIZE, pad=15, fontweight="bold")
    ax2.tick_params(labelsize=TICK_SIZE)
    ax2.legend(fontsize=LEGEND_SIZE, loc="upper left")
    ax2.grid(True, alpha=0.4, linestyle="--")

    plt.tight_layout()
    out = FIG_DIR / "fig5_denoising.pdf"
    plt.savefig(out, dpi=VizConfig.DPI, bbox_inches="tight", pad_inches=0.1)
    print(f"Saved: {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
