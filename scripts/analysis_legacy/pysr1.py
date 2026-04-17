from pathlib import Path
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Project root (scripts/analysis_legacy/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================
# 1. Load data
# ==========================================
df_cases = pd.read_csv(PROJECT_ROOT / 'cases.csv')
df_summary = pd.read_csv(PROJECT_ROOT / 'summary_0_499.csv')
df_long = df_summary.melt(id_vars=['Case'], var_name='Distance', value_name='C_out')
df_long['Distance'] = df_long['Distance'].astype(float)
df_merged = pd.merge(df_long, df_cases, on='Case', how='left').dropna()

# Build features
D_char = np.sqrt(df_merged['Area'].values)
X_star = df_merged['Distance'].values / D_char  # Normalised distance
V_in = df_merged['V_in'].values
y_true = df_merged['C_out'].values
y_log_target = np.log(df_merged['C_out'] / df_merged['C_in']).values

# ==========================================
# 2. Physics-constrained model (forced through the origin)
# ==========================================

# Retain the structure PySR found: exponent = k * X_star * (V_in - V_critical)
# No constant term (i.e. intercept fixed at 0).
def physical_model(X, k, V_critical):
    v_in, x_star = X
    return k * x_star * (v_in - V_critical)

# ==========================================
# 3. Fit parameters
# ==========================================

# Stack inputs for curve_fit
X_data = (V_in, X_star)

# Run the fit
params, covariance = curve_fit(physical_model, X_data, y_log_target)

k_new, V_cr_new = params

print("=" * 40)
print("Physics-constrained fit parameters")
print("=" * 40)
print(f"Decay constant k (new): {k_new:.6f}")
print(f"Critical velocity V_cr (new): {V_cr_new:.4f}")

# ==========================================
# 4. Validate accuracy
# ==========================================

# Predicted log-ratio
y_log_pred = physical_model(X_data, k_new, V_cr_new)

# Convert back to true concentration
# Formula: C(x) = C_in * exp( k * x* * (V - Vcr) )
C_in_raw = df_merged['C_in'].values
y_pred_final = C_in_raw * np.exp(y_log_pred)

r2 = r2_score(y_true, y_pred_final)
print(f"\nFinal R^2 score (intercept fixed at 1): {r2:.5f}")

# Final formula string
print("\nFinal paper-ready formula:")
print(f"C(x) = C_in * exp( {k_new:.6f} * (x / sqrt(A)) * (V_in - {V_cr_new:.4f}) )")
