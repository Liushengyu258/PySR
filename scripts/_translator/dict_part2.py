# -*- coding: utf-8 -*-
"""Chinese->English dictionary part 2: Stage1, Stage2, klw PySR, add."""

T2 = {
    # ---- Stage1 ----
    "这些参数控制了符号回归搜索的广度和深度":
        "Hyperparameters controlling breadth and depth of the symbolic-regression search",
    "迭代次数：越大搜索越久，结果通常越好":
        "Iteration count - higher = longer search, usually better results",
    "种群数量：并行搜索的独立种群数":
        "Number of populations searched in parallel",
    "公式最大长度：防止生成过于复杂的过拟合公式":
        "Max formula length - prevents overly complex / overfitting expressions",
    "允许的二元运算符": "Allowed binary operators",
    "允许的一元运算符：包含物理模型中常见的指数、对数、平方根等":
        "Allowed unary operators (exp, log, sqrt, ...) typical of physical models",
    "自定义算子的 SymPy 映射": "Custom operator mapping for SymPy",
    "模型选择策略：选择综合评分最高的":
        "Model-selection strategy: pick the best-scoring expression",
    "保存临时方程文件，防止中断丢失":
        "Save intermediate equation files so nothing is lost on interruption",
    "保留临时文件用于调试": "Keep temp files for debugging",
    "开启日志，方便观察搜索进展": "Enable logging to watch search progress",
    "正在加载数据并按 Case 进行 7:3 划分...":
        "Loading data and performing a 7:3 case-wise split...",
    "读取清洗后的数据集": "Read the cleaned dataset",
    "将物理量纲统一调整到数值计算友好的范围":
        "Bring the physical scales into a numerically friendly range",
    "关键步骤：必须按 Case 划分训练/测试集，而不是按样本点随机划分":
        "Crucial: split by case, not by individual row",
    "这是为了防止": "This avoids",
    "数据泄露": "data leakage",
    "，因为同一个 Case 内的相邻点高度相关":
        " - neighbouring points within the same case are strongly correlated",
    "根据 Case ID 筛选数据": "Filter rows by Case ID",
    "训练集 Case 数: {len(train_cases)}, 测试集 Case 数: {len(test_cases)}":
        "Train cases: {len(train_cases)}, test cases: {len(test_cases)}",
    "准备特征矩阵 X 和目标向量 y": "Build feature matrix X and target vector y",
    "为了兼顾 PySR 的运行性能和搜索深度，从训练集中随机抽取 5000 个样本点":
        "To balance PySR speed and search depth, draw 5000 random training samples",
    "符号回归对数据量不敏感，5000个点通常足以捕捉物理规律，过多的数据会显著拖慢进化速度)":
        "symbolic regression is not that sensitive to sample count; 5000 usually captures the physics and more just slows evolution)",
    "开始第一阶段：完全数据驱动探索 (Data-Driven Exploration)...":
        "Starting Stage 1: pure data-driven exploration...",
    "初始化回归器": "Initialise the regressor",
    "开始拟合": "Begin fitting",
    "用于让输出的公式直接显示物理变量名，而不是 x0, x1...":
        "So the printed formula uses physical variable names instead of x0, x1, ...",
    "保存所有候选公式到 CSV，供后续分析":
        "Save every candidate formula to CSV for later analysis",
    "在全量测试集上评估泛化性能":
        "Evaluate generalisation on the full test set",
    "注意：这里使用的是从未见过的 Test Cases，能真实反映公式的物理泛化能力":
        "Note: test cases are fully unseen - this is a realistic measure of generalisation",
    "第一阶段探索完成！": "Stage 1 exploration complete!",
    "全量测试集 (新Case) R2: {r2:.5f}":
        "Full test-set R^2 (unseen cases): {r2:.5f}",
    "所有候选公式已保存至: {equations_path}":
        "All candidate formulas saved to: {equations_path}",
    "输出 PySR 认为的最佳公式 (Pareto Front 上的最优解)":
        "Print the PySR best pick (optimum on the Pareto front)",
    "推荐的最佳公式 (SymPy 格式):": "Recommended best formula (SymPy form):",

    # ---- Stage2 ----
    "引入统一的绘图风格配置 (viz_config.py)，确保本阶段生成的验证图风格一致":
        "Import the shared plotting style (viz_config.py) to keep validation figures consistent",
    "将 1e-7 量级的浓度数据放大到 1.0 量级，避免非线性拟合时的数值稳定性问题":
        "Scale ~1e-7 concentration values to ~1.0 to avoid numerical instability during nonlinear fitting",
    "提取特征变量用于后续拟合": "Extract features for the fit",
    "对浓度进行缩放处理": "Apply scaling to the concentration",
    "该公式结构是基于 Stage 1 (PySR) 的探索结果和物理直觉提炼而成的":
        "This structure was refined from the Stage 1 PySR results plus physical intuition",
    "形式：C = C_in / [ (a * x) / (S - b * sqrt(x/v) + c) + d ]":
        "Form: C = C_in / [ (a * x) / (S - b * sqrt(x/v) + c) + d ]",
    "物理量纲项：dist/v 具有时间的量纲 (Time Scale)":
        "Dimensional term: dist / v has units of time",
    "用于防止除零错误": "Prevent division by zero",
    "有效面积项 (Effective Area Term)": "Effective-area term",
    "分母中的核心项，反映了随时间和距离扩散后的等效影响面积":
        "Core denominator term - effective area of influence after diffusion",
    "确保该项不为负，维持物理意义":
        "Keep this term non-negative to preserve physical meaning",
    "构造完整的分母": "Build the full denominator",
    "正在进行非线性最小二乘拟合...": "Running non-linear least-squares fit...",
    "初始猜测值 (Initial Guess)": "Initial guess",
    "这些值来源于 Stage 1 的符号回归初步结果，作为优化的起点":
        "Seeded from the Stage 1 symbolic-regression results",
    "使用 scipy.optimize.curve_fit 进行拟合":
        "Fit with scipy.optimize.curve_fit",
    "限制了参数的搜索空间，确保参数具有合理的物理符号 (如全部为正)":
        "Bound the parameters to physically reasonable signs (e.g. all positive)",
    "使用优化后的参数计算预测值":
        "Compute predictions with the optimised parameters",
    "拟合成功！最优参数如下：": "Fit succeeded - best parameters:",
    "计算评估指标 (R2 和 RMSE)": "Compute metrics (R^2, RMSE)",
    "保存最终参数结果到文本文件": "Save final parameters to a text file",
    "正在绘制 1.pdf (衰减曲线对比)...": "Plotting 1.pdf (decay curves)...",
    "正在绘制 2.pdf (预测对比图)...": "Plotting 2.pdf (parity plot)...",
    "定义局部字号 (也可直接使用 VizConfig)":
        "Local font sizes (feel free to pull from VizConfig instead)",
    "提取当前 Case 数据": "Extract the current case data",
    "使用拟合参数生成预测曲线":
        "Generate the predicted curve from the fitted parameters",
    "绘制真实值散点 (CFD Data)": "Scatter the ground truth (CFD data)",
    "绘制预测曲线 (Proposed Formula) - 红色高亮":
        "Plot the predicted curve (proposed formula) - red highlight",
    "绘制所有样本点的预测值 vs 真实值":
        "Scatter predictions vs ground truth for every sample",
    "绘制 1:1 参考线 (完美预测线)":
        "Draw the 1:1 reference line (perfect prediction)",
    "任务完成！": "Done!",
    "拟合结果已成功保存。": "Fit results saved successfully.",
    "拟合过程中出现错误: {e}": "Error during fitting: {e}",

    # ---- add.ipynb (data-efficiency experiment) ----
    "定义不同的训练集大小，用于评估模型的数据效率":
        "Training-set sizes to sweep for the data-efficiency study",
    "从极小样本 (100) 到全量样本 (44400)":
        "From very small (100) to the full pool (44400)",
    "固定噪声水平 (50%)": "Fixed noise level (50%)",
    "每个样本量重复实验次数，以获取统计显著性":
        "Number of repetitions per size for statistical significance",
    "正在加载数据...": "Loading data...",
    "划分固定的测试集 (Test Set)": "Build a fixed test set",
    "关键：测试集必须在所有实验中保持一致，以确保比较的公平性":
        "Critical: the test set must be identical across every experiment for fair comparison",
    "准备测试数据 (保持干净，作为 Ground Truth)":
        "Prepare clean test data (ground truth)",
    "准备训练数据池 (Training Pool)": "Build the training pool",
    "后续将从这里根据 DATA_SIZES 进行不同规模的采样":
        "We sample from this pool at different sizes according to DATA_SIZES",
    "数据准备完毕。实验将重复 {N_REPEATS} 次。":
        "Data ready. Each experiment will be repeated {N_REPEATS} times.",
    "正在评估训练集大小: {size}": "Evaluating training size: {size}",
    "设置不同的随机种子，确保每次采样的样本不同":
        "Vary the random seed so each repetition draws a different subset",
    "随机采样 (Random Sampling)": "Random sampling",
    "注入噪声 (Inject Noise)": "Inject noise",
    "模拟真实环境中的高噪声数据 (50% 噪声)":
        "Simulates high-noise real-world data (50% noise)",
    "训练 MLP 去噪器 (MLP Denoiser)": "Train the MLP denoiser",
    "混合训练 (Hybrid PySR Training)": "Hybrid PySR training",
    "为了速度，PySR 的输入样本量上限限制在 2000":
        "Cap the PySR input size at 2000 for speed",
    "核心步骤：使用 MLP 对 PySR 的训练数据进行":
        "Core step: pre-clean the PySR training data with the MLP",
    "预清洗": "pre-cleaning",
    "拟合去噪后的数据": "Fit the denoised data",
    "迭代次数较少，追求快速验证":
        "Few iterations - we just need a quick sanity check",
    "默认失败分数": "Default failure score",
    "安全性检查 ---": "Safety check ---",
    "检查是否有无穷大或NaN (可能是生成的公式有奇点)":
        "Check for Inf / NaN (generated formula may have singularities)",
    "生成了奇点公式 (Inf/NaN)，本次跳过。":
        "Singular formula (Inf/NaN) - skipping this run.",
    "在干净的测试集上评估 R2": "Evaluate R^2 on the clean test set",
    "结果: Mean R2 = {mean_r2:.4f} (Std: {std_r2:.4f})":
        "Result: mean R^2 = {mean_r2:.4f} (std: {std_r2:.4f})",
    "保存该数据规模下的统计结果":
        "Save the aggregated stats for this training size",
    "实验运行完成。数据已保存至 Data_Efficiency_Curve.csv":
        "Experiment finished. Data saved to Data_Efficiency_Curve.csv",

    # ---- klw PySR (robustness) ----
    "定义一系列噪声水平 (0% - 200%)，用于全面评估模型的鲁棒性":
        "Noise levels to sweep (0%..200%) for a full robustness picture",
    "结果保存目录 (Refined_Results_v5)": "Output directory (Refined_Results_v5)",
    "用于收集所有噪声水平下的 R2 结果，最终汇总为 CSV":
        "Collects R^2 at every noise level - summarised to CSV at the end",
    "正在加载并按 Case 划分数据...":
        "Loading data and performing a case-wise split...",
    "保证测试集中的工况 (Case) 是模型从未见过的":
        "Ensures the test-set cases are completely unseen",
    "筛选数据": "Filter the data",
    "划分完成: 训练集 Case 数: {len(train_cases)}, 测试集 Case 数: {len(test_cases)}":
        "Split done. Train cases: {len(train_cases)}, test cases: {len(test_cases)}",
    "训练集行数: {len(train_df)}, 测试集行数: {len(test_df)}":
        "Train rows: {len(train_df)}, test rows: {len(test_df)}",
    "准备训练数据 (Clean Baseline)": "Prepare training data (clean baseline)",
    "注意：X_train_clean 和 y_train_clean 是干净的基准数据":
        "Note: X_train_clean / y_train_clean are the clean baseline",
    "在后续循环中，我们会人为向 y_train_clean 添加噪声":
        "Noise will be added to y_train_clean inside the loop below",
    "准备测试数据 (Ground Truth)": "Prepare test data (ground truth)",
    "测试集始终保持干净，用于评估模型在真实场景下的准确度":
        "The test set always stays clean so it reflects real-world accuracy",
    "保留测试集的辅助列 (Case ID 和 Distance)，用于后续按 Case 画图分析":
        "Keep auxiliary columns (Case ID, Distance) for later per-case plotting",
    "遍历每一个定义的噪声水平，对比 Direct PySR, MLP 和 Hybrid PySR 的表现":
        "Loop over every noise level and compare Direct PySR, MLP and Hybrid PySR",
    "运行实验: 噪声等级 {noise_pct*100}%":
        "Running experiment at noise level {noise_pct*100}%",
    "构造带噪训练集 (Noise Injection) ---": "Build the noisy training set ---",
    "仅对训练集的目标值 y 添加高斯白噪声，模拟传感器误差或环境干扰":
        "Add Gaussian white noise to the target y only - mimics sensor / environmental noise",
    "构造带噪测试集 (仅用于观察 MLP 对噪声数据的拟合能力，不作为最终指标)":
        "Build a noisy test set (only for MLP observation - not a final metric)",
    "物理约束：浓度不能为负，设置下限为 1e-6":
        "Physical constraint: concentration cannot be negative - floor at 1e-6",
    "任务 1: 直接符号回归 (Direct PySR Baseline) ---":
        "Task 1: Direct symbolic regression (baseline) ---",
    "直接使用带噪数据训练 PySR，作为对照组 (Baseline)":
        "Train PySR directly on the noisy data - baseline / control",
    "运行直接 PySR...": "Running direct PySR...",
    "随机抽样 5000 个点加速训练": "Sub-sample to 5000 points for speed",
    "保留临时文件以备查": "Keep temp files for reference",
    "训练": "training",
    "保存公式到 CSV": "Save formulas to CSV",
    "在干净测试集上预测": "Predict on the clean test set",
    "任务 2: 神经网络训练 (MLP Training) ---": "Task 2: MLP training ---",
    "训练 MLP 作为一个非线性去噪器":
        "Train an MLP to act as a nonlinear denoiser",
    "训练 MLP...": "Training the MLP...",
    "数据标准化 (Standardization) 对 MLP 至关重要":
        "Input standardisation is essential for the MLP",
    "层隐藏层": "-layer hidden network",
    "保存 Loss 曲线，用于检查收敛情况":
        "Save the loss curve for convergence inspection",
    "任务 3: 混合框架 (Hybrid Framework) ---":
        "Task 3: Hybrid framework ---",
    "策略：先用 MLP 对训练数据进行":
        "Strategy: first denoise the training data with the MLP,",
    "，再用 PySR 拟合去噪后的数据":
        " then fit the denoised data with PySR",
    "运行混合 PySR...": "Running hybrid PySR...",
    "去噪 (Denoising): 使用训练好的 MLP 预测训练集子集":
        "Denoise: use the trained MLP to predict the training subset",
    "假设 MLP 学习到了潜在的物理流形，其预测值比原始含噪标签更接近真值":
        "Assumption: the MLP has learned the physical manifold, so its output is closer to ground truth than noisy labels",
    "拟合 (Symbolic Regression): 拟合去噪后的标签":
        "Symbolic regression: fit the denoised labels",
    "保存公式": "Save formulas",
    "保存所有方法的预测结果，用于后续绘制 Parity Plot 和 序列对比图":
        "Save predictions from every method for later parity / sequence plots",
    "保存预测对比数据...": "Saving prediction comparison data...",
    "结果: Direct R2={r2_direct:.4f}, Hybrid R2={r2_hybrid:.4f}":
        "Result: Direct R^2 = {r2_direct:.4f}, Hybrid R^2 = {r2_hybrid:.4f}",
    "保存训练好的模型对象": "Persist the trained model objects",
    "保存不同噪声水平下的 R2 汇总表，用于绘制鲁棒性曲线 (Figure 6)":
        "Save the R^2 summary across noise levels (used to plot Figure 6)",
    "所有实验结束！": "All experiments complete!",
    "折线图数据: {os.path.join(BASE_DIR,": "Line-plot data: {os.path.join(BASE_DIR,",
    "散点图数据: 在每个 Noise_xxx 文件夹下的 predictions_comparison.csv 中":
        "Scatter-plot data: see predictions_comparison.csv inside each Noise_xxx folder",
}
