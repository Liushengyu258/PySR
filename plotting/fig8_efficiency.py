"""Figure 8 - data-efficiency analysis (replica of Visualization_5.ipynb)."""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from plotting._paths import EFFICIENCY_DIR, FIG_DIR
from viz_config import VizConfig

VizConfig.set_style()
TITLE_SIZE = VizConfig.TITLE_SIZE
LABEL_SIZE = VizConfig.LABEL_SIZE
TICK_SIZE = VizConfig.TICK_SIZE
LEGEND_SIZE = VizConfig.LEGEND_SIZE


def main() -> None:
    csv_path = EFFICIENCY_DIR / "Data_Efficiency_Curve.csv"
    print(f"Reading data: {csv_path}")
    if not csv_path.exists():
        print(f"Warning: {csv_path} not found. Using dummy data.")
        df = pd.DataFrame({
            "Training_Size": [100, 500, 1000, 2000, 4000, 10000, 20000],
            "Mean_R2": [0.6, 0.8, 0.9, 0.95, 0.97, 0.98, 0.985],
            "Std_R2": [0.1, 0.08, 0.05, 0.03, 0.02, 0.01, 0.01],
        })
    else:
        df = pd.read_csv(csv_path)

    df = df.sort_values("Training_Size")
    x = df["Training_Size"].values
    y = df["Mean_R2"].values
    yerr = df["Std_R2"].values

    max_r2 = np.max(y)
    max_idx = int(np.argmax(y))
    threshold = max_r2 * 0.99
    optimal_idx = np.where(y >= threshold)[0]
    best_idx = int(optimal_idx[0]) if len(optimal_idx) else max_idx
    best_size, best_r2 = x[best_idx], y[best_idx]

    zone_min = x[max(0, best_idx - 1)] if best_idx > 0 else best_size * 0.5
    zone_max = (x[min(len(x) - 1, max_idx + 1)] if max_idx < len(x) - 1
                else x[max_idx] * 1.5)

    fig, ax = plt.subplots(figsize=(10, 7))
    COLOR_MAIN = VizConfig.COLOR_MAIN
    COLOR_ERROR = VizConfig.COLOR_SECONDARY
    COLOR_OPTIMAL = VizConfig.COLOR_HIGHLIGHT
    COLOR_HATCH = VizConfig.COLOR_SUCCESS

    ax.axvspan(zone_min, zone_max, facecolor="none", hatch="//",
               edgecolor=COLOR_HATCH, alpha=0.3, zorder=0)

    y_min_val = min(y - yerr)
    ax.set_ylim(max(0, y_min_val - 0.1), 1.02)

    zone_center = np.sqrt(zone_min * zone_max)
    ax.text(zone_center, 0.05, "High Efficiency Zone",
            transform=ax.get_xaxis_transform(),
            ha="center", va="bottom", fontsize=12, fontweight="bold",
            color=COLOR_HATCH, style="italic",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=3))

    ax.errorbar(x, y, yerr=yerr, fmt="-o", markersize=8, linewidth=2.5,
                capsize=4, color=COLOR_MAIN, ecolor=COLOR_ERROR,
                elinewidth=1.5, markerfacecolor="white",
                markeredgecolor=COLOR_MAIN, markeredgewidth=2,
                label=r"Mean $R^2$ Score", zorder=3)
    ax.scatter(best_size, best_r2, s=120, color=COLOR_OPTIMAL, alpha=1.0,
               edgecolor="white", linewidth=2, zorder=4,
               label="Optimal Point")
    ax.axvline(best_size, color=COLOR_OPTIMAL, linestyle="--",
               linewidth=1.5, alpha=0.6, ymax=0.95, zorder=2)

    xytext_pos = ((best_size * 2, best_r2 - 0.08) if best_r2 > 0.8
                  else (best_size * 2, best_r2 + 0.1))
    ax.annotate(f"Optimal Sample Size\nN = {int(best_size)}",
                xy=(best_size, best_r2), xytext=xytext_pos,
                arrowprops=dict(arrowstyle="->",
                                color=VizConfig.COLOR_AXIS, lw=1.5,
                                connectionstyle="arc3,rad=-0.2"),
                fontsize=12, color=VizConfig.COLOR_AXIS, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", fc="white",
                          ec="#cfd8dc", alpha=0.95))

    ax.set_xscale("log")
    ax.set_xlabel("Training Dataset Size (Log Scale)", fontsize=LABEL_SIZE,
                  fontweight="bold", labelpad=10)
    ax.set_ylabel(r"Test Set $R^2$ Score", fontsize=LABEL_SIZE,
                  fontweight="bold", labelpad=10)
    ax.set_title("Data Efficiency Analysis", fontsize=TITLE_SIZE,
                 pad=20, fontweight="bold")
    ax.grid(True, which="major", linestyle="-", alpha=0.6,
            color=VizConfig.COLOR_GRID, linewidth=1)
    ax.grid(True, which="minor", linestyle=":", alpha=0.4,
            color=VizConfig.COLOR_GRID, linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2.0)
        spine.set_color(VizConfig.COLOR_AXIS)
    ax.tick_params(axis="both", which="major", labelsize=TICK_SIZE,
                   length=6, width=1.5, colors=VizConfig.COLOR_AXIS, direction="in")
    ax.tick_params(axis="both", which="minor", length=3, width=1,
                   colors=VizConfig.COLOR_AXIS, direction="in")
    legend = ax.legend(fontsize=LEGEND_SIZE, loc="lower right", frameon=True,
                       edgecolor=VizConfig.COLOR_AXIS, fancybox=False)
    legend.get_frame().set_linewidth(1.5)

    plt.tight_layout()
    out = FIG_DIR / "fig8_efficiency.pdf"
    plt.savefig(out, dpi=VizConfig.DPI, bbox_inches="tight", pad_inches=0.1)
    print(f"Saved: {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
