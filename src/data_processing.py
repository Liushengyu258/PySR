"""Build the ML-ready dataset from the raw CFD outputs.

Inputs  (in ``data/``):
    cases.csv          - per-case inlet conditions (V_in, C_in, Area)
    summary_0_499.csv  - per-case concentration profile along the domain (wide format)

Output  (in ``data/``):
    train_dataset_ready.csv  - merged long-format ML-ready dataset

Also provides :func:`plot_case_profile` for quick visual inspection of any case.
"""
from __future__ import annotations
import os
import pandas as pd
import matplotlib.pyplot as plt

from src._bootstrap import DATA_DIR


# ---------------------------------------------------------------------------
# Dataset construction
# ---------------------------------------------------------------------------
def build_dataset() -> pd.DataFrame:
    """Merge cases + summary tables, melt to long format, drop NaN rows, save."""
    cases_file = DATA_DIR / "cases.csv"
    summary_file = DATA_DIR / "summary_0_499.csv"
    if not cases_file.exists() or not summary_file.exists():
        raise FileNotFoundError(
            f"Missing raw CSVs. Looked for {cases_file} and {summary_file}."
        )

    print("Reading raw data files...")
    df_cases = pd.read_csv(cases_file)
    df_summary = pd.read_csv(summary_file)

    # Wide -> long: one sample per (case, distance)
    print("Melting the summary table to long format...")
    df_long = df_summary.melt(id_vars=["Case"], var_name="Distance", value_name="C_out")
    df_long["Distance"] = df_long["Distance"].astype(float)

    # Attach per-case parameters via Case ID
    print("Merging case parameters...")
    df_merged = pd.merge(df_long, df_cases, on="Case", how="left")

    feature_cols = ["V_in", "C_in", "Area", "Distance"]
    target_col = ["C_out"]

    print(f"Merged shape:           {df_merged.shape}")
    df_merged = df_merged.dropna()
    print(f"Cleaned shape (no NaN): {df_merged.shape}")
    print("\nData preview (first 5 rows):")
    print(df_merged[feature_cols + target_col].head())

    out_path = DATA_DIR / "train_dataset_ready.csv"
    df_merged.to_csv(out_path, index=False)
    print(f"\nDataset saved to {out_path}")
    return df_merged


# ---------------------------------------------------------------------------
# Per-case sanity-check plot
# ---------------------------------------------------------------------------
def plot_case_profile(case_name: str, show: bool = True) -> None:
    """Plot the concentration profile for one case (quick sanity check)."""
    cases_file = DATA_DIR / "cases.csv"
    summary_file = DATA_DIR / "summary_0_499.csv"
    if not cases_file.exists() or not summary_file.exists():
        print(f"ERROR: cannot find {cases_file} or {summary_file}")
        return

    df_cases = pd.read_csv(cases_file)
    df_summary = pd.read_csv(summary_file)
    if case_name not in df_cases["Case"].values:
        print(f"ERROR: case not found: '{case_name}'")
        return

    case_info = df_cases.loc[df_cases["Case"] == case_name].iloc[0]
    c_in, v_in, area = case_info["C_in"], case_info["V_in"], case_info["Area"]

    profile = df_summary.loc[df_summary["Case"] == case_name].drop(columns=["Case"]).iloc[0]
    distances = [float(c) for c in profile.index]
    concentrations = profile.values.astype(float)

    plt.figure(figsize=(12, 6))
    plt.plot(distances, concentrations, color="blue", linewidth=2, marker=".",
             markersize=5, label=f"Concentration profile ({case_name})")
    plt.axhline(y=c_in, color="red", linestyle="--",
                label=f"Inlet C_in = {c_in:.2e}")
    plt.title(
        f"Tunnel Concentration Profile: {case_name}\n"
        f"(Vin={v_in:.2f} m/s, Area={area:.1f} m^2)", fontsize=14,
    )
    plt.xlabel("Distance from Inlet (m)", fontsize=12)
    plt.ylabel("Particle Concentration (kg/m^3)", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    print(f"--- {case_name} Data summary ---")
    print(f"Inlet conditions: C_in={c_in:.2e}, V_in={v_in:.2f}, Area={area:.1f}")
    print(f"Max concentration along path: {concentrations.max():.2e}")
    print(f"Min concentration along path: {concentrations.min():.2e}")
    print(f"Outlet (1100 m) concentration: {concentrations[-1]:.2e}")

    if show:
        plt.show()


if __name__ == "__main__":
    build_dataset()
    # Uncomment to preview any case after building:
    # plot_case_profile("dp110")
