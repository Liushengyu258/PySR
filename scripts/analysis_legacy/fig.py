from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 项目根目录 (scripts/analysis_legacy/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = PROJECT_ROOT / 'figures'
FIG_DIR.mkdir(exist_ok=True)

# ==========================================
# 1. 准备数据和预测值
# ==========================================
# 假设上面的代码已经运行完，你有 df_merged 和 k_new, V_cr_new
df_cases = pd.read_csv(PROJECT_ROOT / 'cases.csv')
df_summary = pd.read_csv(PROJECT_ROOT / 'summary_0_499.csv')
df_long = df_summary.melt(id_vars=['Case'], var_name='Distance', value_name='C_out')
df_long['Distance'] = df_long['Distance'].astype(float)
df_merged = pd.merge(df_long, df_cases, on='Case', how='left').dropna()

k_new=0.001541
V_cr_new=5.5024
# 重新计算最终预测值
# 公式: C = C_in * exp( k * (x/sqrt(A)) * (V - Vcr) )
# 注意：代码里拟合出的 k 是正数，但 (V - Vcr) 是负数，所以直接乘就是衰减
exponent = k_new * (df_merged['Distance'] / np.sqrt(df_merged['Area'])) * (df_merged['V_in'] - V_cr_new)
y_pred = df_merged['C_in'] * np.exp(exponent)
y_true = df_merged['C_out']

# ==========================================
# 2. 评估指标
# ==========================================
r2 = r2_score(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mae = mean_absolute_error(y_true, y_pred)

print(f"R2: {r2:.4f}")
print(f"RMSE: {rmse:.2e}")
print(f"MAE: {mae:.2e}")

# ==========================================
# 3. 绘图 (论文级别配色)
# ==========================================
plt.figure(figsize=(8, 7), dpi=120)

# 绘制散点
plt.scatter(y_true, y_pred,
            alpha=0.3,       # 透明度，防止点重叠看不清
            s=10,            # 点的大小
            c='dodgerblue',  # 颜色
            edgecolors='none',
            label='Data Points')

# 绘制对角线 (完美预测线)
min_val = min(y_true.min(), y_pred.min())
max_val = max(y_true.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val],
         'r--', linewidth=2, label='Perfect Fit (y=x)')

# 绘制误差带 (可选，例如 +/- 20%)
# plt.plot([min_val, max_val], [min_val*1.2, max_val*1.2], 'k:', alpha=0.5, label='+/- 20% Error')
# plt.plot([min_val, max_val], [min_val*0.8, max_val*0.8], 'k:', alpha=0.5)

# 设置坐标轴
plt.xlabel(r'CFD Simulated Concentration ($C_{CFD}$)', fontsize=12)
plt.ylabel(r'Formula Predicted Concentration ($C_{Pred}$)', fontsize=12)
plt.title(f'Performance of the Derived Semi-Empirical Formula\n($R^2={r2:.3f}$)', fontsize=14)

# 使用科学计数法显示坐标轴
plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))

plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# 保存图片
plt.savefig(FIG_DIR / 'Formula_Performance.png', dpi=300)
plt.show()