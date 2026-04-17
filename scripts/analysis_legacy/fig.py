from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Project root (scripts/analysis_legacy/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = PROJECT_ROOT / 'figures'
FIG_DIR.mkdir(exist_ok=True)

# ==========================================
# 1. Load data and compute predictions
# ==========================================
# Assumes upstream code has produced df_merged plus k_new and V_cr_new
df_cases = pd.read_csv(PROJECT_ROOT / 'cases.csv')
df_summary = pd.read_csv(PROJECT_ROOT / 'summary_0_499.csv')
df_long = df_summary.melt(id_vars=['Case'], var_name='Distance', value_name='C_out')
df_long['Distance'] = df_long['Distance'].astype(float)
df_merged = pd.merge(df_long, df_cases, on='Case', how='left').dropna()

k_new = 0.001541
V_cr_new = 5.5024
# Recompute the final prediction.
# Formula: C = C_in * exp( k * (x / sqrt(A)) * (V - Vcr) )
# Note: the fitted k is positive, (V - Vcr) is negative, so the product decays.
exponent = k_new * (df_merged['Distance'] / np.sqrt(df_merged['Area'])) * (df_merged['V_in'] - V_cr_new)
y_pred = df_merged['C_in'] * np.exp(exponent)
y_true = df_merged['C_out']

# ==========================================
# 2. Metrics
# ==========================================
r2 = r2_score(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mae = mean_absolute_error(y_true, y_pred)

print(f"R2:   {r2:.4f}")
print(f"RMSE: {rmse:.2e}")
print(f"MAE:  {mae:.2e}")

# ==========================================
# 3. Plot (paper-style colours)
# ==========================================
plt.figure(figsize=(8, 7), dpi=120)

# Scatter
plt.scatter(y_true, y_pred,
            alpha=0.3,
            s=10,
            c='dodgerblue',
            edgecolors='none',
            label='Data Points')

# Perfect-fit diagonal
min_val = min(y_true.min(), y_pred.min())
max_val = max(y_true.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val],
         'r--', linewidth=2, label='Perfect Fit (y=x)')

# Optional error band (e.g. +/- 20%)
# plt.plot([min_val, max_val], [min_val*1.2, max_val*1.2], 'k:', alpha=0.5, label='+/- 20% Error')
# plt.plot([min_val, max_val], [min_val*0.8, max_val*0.8], 'k:', alpha=0.5)

# Axes
plt.xlabel(r'CFD Simulated Concentration ($C_{CFD}$)', fontsize=12)
plt.ylabel(r'Formula Predicted Concentration ($C_{Pred}$)', fontsize=12)
plt.title(f'Performance of the Derived Semi-Empirical Formula\n($R^2={r2:.3f}$)', fontsize=14)

# Scientific notation for axis ticks
plt.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))

plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Save
plt.savefig(FIG_DIR / 'Formula_Performance.png', dpi=300)
plt.show()
