from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Project root (scripts/lhs_sampling/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = PROJECT_ROOT / 'figures'
FIG_DIR.mkdir(exist_ok=True)

# --- 1. Plot style (Times New Roman) ---
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'  # Keep the math font consistent

# --- 2. Load data ---
try:
    df = pd.read_csv(PROJECT_ROOT / 'cfd_lhs_cases.csv')
except FileNotFoundError:
    print("ERROR: cfd_lhs_cases.csv not found")
    exit()

# --- 3. Normalisation bounds ---
c_in_bounds = [0.0000011615, 0.00006778]
v_in_bounds = [0.2, 2.0]
area_bounds = [23, 68]

# --- 4. Normalise into [0, 1] ---
df['C_in_norm'] = (df['C_in'] - c_in_bounds[0]) / (c_in_bounds[1] - c_in_bounds[0])
df['V_in_norm'] = (df['V_in'] - v_in_bounds[0]) / (v_in_bounds[1] - v_in_bounds[0])
df['Area_norm'] = (df['Area'] - area_bounds[0]) / (area_bounds[1] - area_bounds[0])

# --- 5. Canvas size (12 cm x 9 cm) ---
# Matplotlib uses inches; 1 inch = 2.54 cm
cm_to_inch = 1 / 2.54
width = 12 * cm_to_inch
height = 9 * cm_to_inch

fig = plt.figure(figsize=(width, height))
ax = fig.add_subplot(111, projection='3d')

# --- 6. 3D scatter plot ---
scatter = ax.scatter(
    df['C_in_norm'],
    df['V_in_norm'],
    df['Area_norm'],
    c='b',
    marker='o',
    s=10,          # Smaller markers because the figure is compact
    alpha=0.6,
    edgecolors='k',
    linewidth=0.2  # Slimmer marker edges
)

# --- 7. Labels and axes ---
# Font size 10.5 matches common paper sizing
label_font_size = 10.5

ax.set_xlabel('C_in (Normalized)', fontsize=label_font_size, labelpad=5)
ax.set_ylabel('V_in (Normalized)', fontsize=label_font_size, labelpad=5)
ax.set_zlabel('Area (Normalized)', fontsize=label_font_size, labelpad=5)

# Tick label font size
ax.tick_params(axis='both', which='major', labelsize=9)

# Axis ranges
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)

# View angle (optional)
ax.view_init(elev=45, azim=135)

# --- 8. Save as TIFF and PDF ---
output_filename = str(FIG_DIR / 'lhs_distribution.tiff')

# dpi=300: print-quality resolution
plt.savefig(output_filename, dpi=300, format='tiff', pad_inches=0.1)
plt.savefig(FIG_DIR / 'lhs_distribution.pdf', format='pdf', pad_inches=0.1)
print(f"Figure saved to: {output_filename} (size 12 cm x 9 cm, DPI 300)")
plt.show()
