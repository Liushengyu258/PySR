from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 项目根目录 (scripts/lhs_sampling/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = PROJECT_ROOT / 'figures'
FIG_DIR.mkdir(exist_ok=True)

# --- 1. 设置绘图风格 (Times New Roman) ---
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'  # 保证数学公式字体也协调

# --- 2. 读取数据 ---
try:
    df = pd.read_csv(PROJECT_ROOT / 'cfd_lhs_cases.csv')
except FileNotFoundError:
    print("错误: 未找到文件 cfd_lhs_cases.csv")
    exit()

# --- 3. 定义归一化边界 ---
c_in_bounds = [0.0000011615, 0.00006778]
v_in_bounds = [0.2, 2.0]
area_bounds = [23, 68]

# --- 4. 执行归一化 ---
df['C_in_norm'] = (df['C_in'] - c_in_bounds[0]) / (c_in_bounds[1] - c_in_bounds[0])
df['V_in_norm'] = (df['V_in'] - v_in_bounds[0]) / (v_in_bounds[1] - v_in_bounds[0])
df['Area_norm'] = (df['Area'] - area_bounds[0]) / (area_bounds[1] - area_bounds[0])

# --- 5. 设置画布尺寸 (12cm x 9cm) ---
# Matplotlib 使用英寸 (inch)，1 inch = 2.54 cm
cm_to_inch = 1 / 2.54
width = 12 * cm_to_inch
height = 9 * cm_to_inch

fig = plt.figure(figsize=(width, height))  # 设置尺寸
ax = fig.add_subplot(111, projection='3d')

# --- 6. 绘制 3D 散点图 ---
scatter = ax.scatter(
    df['C_in_norm'],
    df['V_in_norm'],
    df['Area_norm'],
    c='b',
    marker='o',
    s=10,           # 因为图片变小了，点的大小稍微调小一点 (15 -> 10)
    alpha=0.6,
    edgecolors='k',
    linewidth=0.2   # 边框线变细一点
)

# --- 7. 标签与坐标轴设置 ---
# 字体大小调整为 10.5 (接近论文常用字号)
label_font_size = 10.5

ax.set_xlabel('C_in (Normalized)', fontsize=label_font_size, labelpad=5)
ax.set_ylabel('V_in (Normalized)', fontsize=label_font_size, labelpad=5)
ax.set_zlabel('Area (Normalized)', fontsize=label_font_size, labelpad=5)

# 设置坐标轴刻度字体大小
ax.tick_params(axis='both', which='major', labelsize=9)

# 设置坐标轴范围 [0, 1]
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)

# 调整视角 (可选)
ax.view_init(elev=45, azim=135)

# --- 8. 保存为 TIFF 格式 ---
output_filename = str(FIG_DIR / 'lhs_distribution.tiff')

# dpi=300: 打印级高分辨率
plt.savefig(output_filename, dpi=300, format='tiff', pad_inches=0.1)
plt.savefig(FIG_DIR / 'lhs_distribution.pdf', format='pdf', pad_inches=0.1)
print(f"图表已保存为: {output_filename} (尺寸: 12cm x 9cm, DPI: 300)")
plt.show()