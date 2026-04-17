import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

class VizConfig:
    # ==========================================
    # 1. Fonts & sizes
    # ==========================================
    FONT_FAMILY = 'serif'
    FONT_SERIF = ['Times New Roman']  # Standard paper font
    MATH_FONT = 'stix'                # Math font, close to Times in style

    TITLE_SIZE = 18   # Figure title
    LABEL_SIZE = 18   # Axis labels (e.g. "Distance (m)")
    TICK_SIZE = 15    # Tick labels (e.g. "0.0, 0.5, 1.0")
    LEGEND_SIZE = 16  # Legend text
    DPI = 300         # Output resolution

    # ==========================================
    # 2. Advanced colour palette (Nature/Science style)
    # ==========================================

    # --- Base palette (6-colour cycle) ---
    # Index 0: Deep Blue
    # Index 1: Slate Grey
    # Index 2: Rich Red
    # Index 3: Forest Green
    # Index 4: Goldenrod
    # Index 5: Deep Purple
    COLOR_PALETTE = ['#00467F', '#A5A5A5', '#D62728', '#2E7D32', '#FFB300', '#5B358C']

    # --- Semantic colour mapping (key section) ---

    # 1. Main data / core model
    #    Used for:
    #      - Fig. 1 (Combined): raw CFD scatter points
    #      - Fig. 4 (Degradation): Direct SR baseline curve
    #      - Fig. 5 (Denoising): ground-truth points
    #      - Fig. 6 (Robustness): Ours (Hybrid) curve
    #      - Fig. 8 (Efficiency): mean-R2 curve
    COLOR_MAIN = '#00467F'       # Deep blue

    # 2. Secondary data / baseline / background
    #    Used for:
    #      - Fig. 4: breakdown-point reference line
    #      - Fig. 5: noisy data points
    #      - Fig. 6: baseline (Direct SR) comparison curve
    #      - Fig. 8: error bars
    #      - Fig. 7: stability-region shading outline
    COLOR_SECONDARY = '#A5A5A5'  # Grey

    # 3. Highlight / emphasis / fit line
    #    Used for:
    #      - Fig. 1: proposed formula fit line
    #      - Fig. 4: failure-zone background (combined with alpha)
    #      - Fig. 5: MLP denoised output line
    #      - Fig. 8: optimal operating point and its indicator
    COLOR_HIGHLIGHT = '#CD5C5C'  # Red

    # 4. Success / safe / robust zone
    #    Used for:
    #      - Fig. 4: robust-zone background
    #      - Fig. 6: robust-zone background
    #      - Fig. 8: high-efficiency hatch region
    COLOR_SUCCESS = '#00E079'    # Green

    # 5. Warning / auxiliary / threshold
    #    Used for:
    #      - Fig. 1: +/-2 std-dev threshold lines in the residual plot
    COLOR_WARNING = '#FFB300'    # Amber / yellow

    # --- UI element colours ---
    COLOR_GRID = '#E0E0E0'       # Gridlines (light grey)
    COLOR_AXIS = '#333333'       # Axes and text (dark grey, softer than pure black)
    COLOR_BACKGROUND = '#FFFFFF' # Background

    @classmethod
    def set_style(cls):
        """Apply the global matplotlib style."""
        plt.rcParams['font.family'] = cls.FONT_FAMILY
        plt.rcParams['font.serif'] = cls.FONT_SERIF
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['mathtext.fontset'] = cls.MATH_FONT
        plt.rcParams['figure.dpi'] = cls.DPI

        # Axes & grid
        plt.rcParams['axes.edgecolor'] = cls.COLOR_AXIS
        plt.rcParams['axes.labelcolor'] = cls.COLOR_AXIS
        plt.rcParams['xtick.color'] = cls.COLOR_AXIS
        plt.rcParams['ytick.color'] = cls.COLOR_AXIS
        plt.rcParams['grid.color'] = cls.COLOR_GRID
        plt.rcParams['grid.linestyle'] = '--'
        plt.rcParams['grid.alpha'] = 0.6

        # Legend
        plt.rcParams['legend.frameon'] = True
        plt.rcParams['legend.framealpha'] = 0.95
        plt.rcParams['legend.edgecolor'] = cls.COLOR_AXIS
        plt.rcParams['legend.fancybox'] = False

    @classmethod
    def get_color(cls, index):
        """Return the palette colour at the given index (wraps around)."""
        return cls.COLOR_PALETTE[index % len(cls.COLOR_PALETTE)]
