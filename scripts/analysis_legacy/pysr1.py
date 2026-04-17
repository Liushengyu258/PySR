from pathlib import Path
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# 项目根目录 (scripts/analysis_legacy/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================
# 1. 准备数据 (和之前一样)
# ==========================================
df_cases = pd.read_csv(PROJECT_ROOT / 'cases.csv')
df_summary = pd.read_csv(PROJECT_ROOT / 'summary_0_499.csv')
df_long = df_summary.melt(id_vars=['Case'], var_name='Distance', value_name='C_out')
df_long['Distance'] = df_long['Distance'].astype(float)
df_merged = pd.merge(df_long, df_cases, on='Case', how='left').dropna()

# 构造变量
D_char = np.sqrt(df_merged['Area'].values)
X_star = df_merged['Distance'].values / D_char  # 归一化距离
V_in = df_merged['V_in'].values
y_true = df_merged['C_out'].values
y_log_target = np.log(df_merged['C_out'] / df_merged['C_in']).values

# ==========================================
# 2. 定义物理约束模型 (强制过原点)
# ==========================================

# 我们保留 PySR 发现的结构： exponent = k * X_star * (V_in - V_critical)
# 但这里没有常数项 C (即强制截距为0)
def physical_model(X, k, V_critical):
    v_in, x_star = X
    return k * x_star * (v_in - V_critical)

# ==========================================
# 3. 重新拟合参数
# ==========================================

# 组合输入数据给 curve_fit 使用
X_data = (V_in, X_star)

# 开始拟合
params, covariance = curve_fit(physical_model, X_data, y_log_target)

k_new, V_cr_new = params

print("="*40)
print("物理约束修正后的参数")
print("="*40)
print(f"衰减常数 k (新): {k_new:.6f}")
print(f"临界风速 V_cr (新): {V_cr_new:.4f}")

# ==========================================
# 4. 验证新公式的精度
# ==========================================

# 预测对数值
y_log_pred = physical_model(X_data, k_new, V_cr_new)

# 还原到真实浓度
# 公式: C(x) = C_in * exp( k * x* * (V - Vcr) )
C_in_raw = df_merged['C_in'].values
y_pred_final = C_in_raw * np.exp(y_log_pred)

# 计算 R2
r2 = r2_score(y_true, y_pred_final)
print(f"\n修正后 (强制初始系数为1) 的 R² 分数: {r2:.5f}")

# 生成最终公式字符串
print("\n最终完美的论文公式：")
print(f"C(x) = C_in * exp( {k_new:.6f} * (x / sqrt(A)) * (V_in - {V_cr_new:.4f}) )")