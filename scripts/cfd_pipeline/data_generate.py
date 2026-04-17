from pathlib import Path
import pandas as pd
from scipy.stats import qmc

# 项目根目录 (scripts/cfd_pipeline/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# --- 1. 参数设置与边界定义 ---

# 你想要生成的工况数量
n_samples = 500

# 定义每个变量的物理区间 [下限, 上限]
# 变量1: 送风颗粒物浓度 (C_in)
c_in_bounds = [0.0000011615, 0.00006778]
# 变量2: 送风速度 (V_in)
v_in_bounds = [0.2, 2.0]
# 变量3: 面积 (Area) -> 【修复】这里变量名改为 area_bounds，避免覆盖
area_bounds = [3.35, 5.9]

# 将所有变量的下限和上限整合在一起 -> 【优化】对应3个变量
lower_bounds = [c_in_bounds[0], v_in_bounds[0], area_bounds[0]]
upper_bounds = [c_in_bounds[1], v_in_bounds[1], area_bounds[1]]

# 自动计算维度数量
n_dims = len(lower_bounds)

# --- 2. 使用LHS生成单位超立方体内的样本 ---

# 初始化拉丁超立方采样器
sampler = qmc.LatinHypercube(d=n_dims, seed=42)

# 生成单位区间 [0, 1] 内的样本
unit_samples = sampler.random(n=n_samples)

# --- 3. 将单位样本点缩放到实际的物理量区间 ---

# 线性映射到物理空间
physical_samples = qmc.scale(unit_samples, lower_bounds, upper_bounds)

# --- 4. 结果处理与保存 ---

# 定义列名 -> 【修复】增加 'Area'
col_names = ['C_in', 'V_in', 'Area']

# 创建 DataFrame
df_samples = pd.DataFrame(physical_samples, columns=col_names)

# 打印预览
print(f"生成维度: {n_dims}, 样本数: {n_samples}")
print("前5个工况点预览:")
print(df_samples.head())

# 保存为CSV
output_filename = PROJECT_ROOT / 'cfd_lhs_cases.csv'
df_samples.to_csv(output_filename, index=False)
print(f"\n已保存至文件: {output_filename}")