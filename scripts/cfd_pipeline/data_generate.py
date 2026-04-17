from pathlib import Path
import pandas as pd
from scipy.stats import qmc

# Project root (scripts/cfd_pipeline/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# --- 1. Parameters and physical bounds ---

# Number of cases to generate
n_samples = 500

# Physical range [lower, upper] for every variable
# Variable 1: inlet particulate concentration (C_in)
c_in_bounds = [0.0000011615, 0.00006778]
# Variable 2: inlet velocity (V_in)
v_in_bounds = [0.2, 2.0]
# Variable 3: cross-sectional area (Area)
area_bounds = [3.35, 5.9]

# Combine lower/upper vectors (one entry per variable)
lower_bounds = [c_in_bounds[0], v_in_bounds[0], area_bounds[0]]
upper_bounds = [c_in_bounds[1], v_in_bounds[1], area_bounds[1]]

# Number of dimensions inferred from the bound lists
n_dims = len(lower_bounds)

# --- 2. Latin Hypercube Sampling inside the unit hypercube ---

sampler = qmc.LatinHypercube(d=n_dims, seed=42)

# Samples inside [0, 1]
unit_samples = sampler.random(n=n_samples)

# --- 3. Rescale unit samples onto the physical ranges ---

physical_samples = qmc.scale(unit_samples, lower_bounds, upper_bounds)

# --- 4. Post-processing and output ---

col_names = ['C_in', 'V_in', 'Area']
df_samples = pd.DataFrame(physical_samples, columns=col_names)

print(f"Dimensions: {n_dims}, samples: {n_samples}")
print("First 5 cases:")
print(df_samples.head())

# Save as CSV under the project root
output_filename = PROJECT_ROOT / 'cfd_lhs_cases.csv'
df_samples.to_csv(output_filename, index=False)
print(f"\nSaved to: {output_filename}")
