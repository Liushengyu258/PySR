from pathlib import Path
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from scipy.optimize import curve_fit
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# ==========================================
# 0. 数据准备
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
df_cases = pd.read_csv(PROJECT_ROOT / 'cases.csv')
df_summary = pd.read_csv(PROJECT_ROOT / 'summary_0_499.csv')
df_long = df_summary.melt(id_vars=['Case'], var_name='Distance', value_name='C_out')
df_long['Distance'] = df_long['Distance'].astype(float)
df_all = pd.merge(df_long, df_cases, on='Case', how='left').dropna()

# 全量验证数据
D_char_all = np.sqrt(df_all['Area'].values)
X_star_all = df_all['Distance'].values / D_char_all
V_in_all = df_all['V_in'].values
y_true_all = df_all['C_out'].values


# ==========================================
# 1. 核心工具函数
# ==========================================

# --- A. 智能采样函数 (模拟精心设计的实验) ---
def get_smart_samples(all_cases_df, n_samples):
    """
    使用 K-Means 算法从所有工况中挑选出最具代表性的 n 个工况
    保证采样点均匀覆盖参数空间 (V_in, Area)
    """
    # 提取工况特征 (V_in, Area)
    # 注意：summary表里有重复Case，我们需要去重的cases表
    unique_cases = all_cases_df[['Case', 'V_in', 'Area']].drop_duplicates()

    # 归一化特征 (防止Area数值大主导了距离计算)
    features = unique_cases[['V_in', 'Area']].values
    scaler = MinMaxScaler()
    features_norm = scaler.fit_transform(features)

    # K-Means 聚类
    kmeans = KMeans(n_clusters=n_samples, random_state=42, n_init=10)
    kmeans.fit(features_norm)

    # 找到距离每个聚类中心最近的那个点
    selected_case_ids = []
    centers = kmeans.cluster_centers_

    for center in centers:
        # 计算所有点到该中心的距离
        dists = np.linalg.norm(features_norm - center, axis=1)
        # 选最近的索引
        idx = np.argmin(dists)
        selected_case_ids.append(unique_cases.iloc[idx]['Case'])

    return selected_case_ids


# --- B. 物理公式拟合函数 (Student) ---
def fit_physics_formula(V, X_star, y_log_target):
    def func(X, k, V_cr):
        v, x_s = X
        return k * x_s * (v - V_cr)

    try:
        # 增加 maxfev 防止不收敛
        popt, _ = curve_fit(func, (V, X_star), y_log_target, p0=[0.0015, 5.0], maxfev=10000)
        return popt
    except:
        return [0, 0]


# --- C. 神经网络 (Teacher) ---
class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 64), nn.Tanh(),
            nn.Linear(64, 64), nn.Tanh(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.net(x)


def train_nn_surrogate(X_train, y_train, epochs=800):
    scaler_X = StandardScaler().fit(X_train)
    X_scaled = torch.FloatTensor(scaler_X.transform(X_train))
    y_tensor = torch.FloatTensor(y_train).view(-1, 1)

    model = SimpleNN()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    for _ in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(X_scaled), y_tensor)
        loss.backward()
        optimizer.step()
    return model, scaler_X


# ==========================================
# 2. 实验循环：对比 随机采样 vs 智能采样
# ==========================================

n_cases_list = [5, 10, 20, 30, 50, 100]  # 测试更少的点，突显差异
r2_random = []
r2_smart_nn = []

print("开始实验：不同采样策略与建模方法对比...")

for n in n_cases_list:
    print(f"--> 测试工况数 N = {n}")

    # -----------------------------------
    # 方案 A: 随机采样 + 直接拟合 (模拟小白做法)
    # -----------------------------------
    random_cases = np.random.choice(df_cases['Case'].unique(), n, replace=False)
    df_sample_rand = df_all[df_all['Case'].isin(random_cases)]

    # 直接拟合
    X_s_rand = df_sample_rand['Distance'].values / np.sqrt(df_sample_rand['Area'].values)
    V_rand = df_sample_rand['V_in'].values
    y_log_rand = np.log(df_sample_rand['C_out'] / df_sample_rand['C_in']).values

    k_r, vcr_r = fit_physics_formula(V_rand, X_s_rand, y_log_rand)

    # 全量验证
    y_pred_r_log = k_r * X_star_all * (V_in_all - vcr_r)
    y_pred_r = df_all['C_in'] * np.exp(y_pred_r_log)
    r2_random.append(r2_score(y_true_all, y_pred_r))

    # -----------------------------------
    # 方案 B: 智能采样(KMeans) + NN增强 (模拟你的高级做法)
    # -----------------------------------
    smart_cases = get_smart_samples(df_cases, n)
    df_sample_smart = df_all[df_all['Case'].isin(smart_cases)]

    # 1. 训练 NN (即便只有5个Case，也有550个点，NN能训练！)
    X_nn = df_sample_smart[['V_in', 'Area', 'Distance']].values
    y_nn = np.log(df_sample_smart['C_out'] / df_sample_smart['C_in']).values
    model, scaler = train_nn_surrogate(X_nn, y_nn)

    # 2. 生成 10000 个均匀分布的虚拟数据 (填补空间)
    n_virt = 10000
    v_virt = np.random.uniform(df_cases['V_in'].min(), df_cases['V_in'].max(), n_virt)
    a_virt = np.random.uniform(df_cases['Area'].min(), df_cases['Area'].max(), n_virt)
    d_virt = np.random.uniform(0, 1100, n_virt)

    X_virt_in = np.column_stack((v_virt, a_virt, d_virt))
    X_virt_scaled = torch.FloatTensor(scaler.transform(X_virt_in))
    with torch.no_grad():
        y_virt_log = model(X_virt_scaled).numpy().flatten()

    # 3. 用虚拟数据拟合公式
    X_star_virt = d_virt / np.sqrt(a_virt)
    k_s, vcr_s = fit_physics_formula(v_virt, X_star_virt, y_virt_log)

    # 全量验证
    y_pred_s_log = k_s * X_star_all * (V_in_all - vcr_s)
    y_pred_s = df_all['C_in'] * np.exp(y_pred_s_log)
    r2_smart_nn.append(r2_score(y_true_all, y_pred_s))

# ==========================================
# 3. 绘图
# ==========================================
plt.figure(figsize=(10, 6), dpi=100)
plt.plot(n_cases_list, r2_random, 'o--', color='gray', label='Random Sampling + Direct Fit')
plt.plot(n_cases_list, r2_smart_nn, 's-', color='red', linewidth=2, label='Smart Sampling + NN Enhanced')

plt.axhline(y=0.977, color='green', linestyle=':', label='Ground Truth (500 cases)')
plt.ylim(0.5, 1.0)  # 限制Y轴范围看清高分段
plt.xlabel('Number of CFD Cases')
plt.ylabel('Test R2 Score (on All 500 Cases)')
plt.title('Data Efficiency: How many CFD cases do we really need?')
plt.legend()
plt.grid(True)
plt.show()