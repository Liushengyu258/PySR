# -*- coding: utf-8 -*-
"""Chinese->English dictionary part 1: setup cell, section headings, data prep."""

T1 = {
    # ---- Auto-injected setup cell ----
    "自动向上查找项目根目录 (含 .gitignore 的文件夹)":
        "Walk upward to find the project root (folder containing .gitignore)",
    "切换 cwd 到项目根, 使所有相对路径 (Stage1_Exploration/, Refined_Results_v4/ 等) 保持有效":
        "Switch cwd to the project root so every relative path (Stage1_Exploration/, Refined_Results_v4/, ...) keeps working",
    "让 notebooks 能 `from viz_config import VizConfig`":
        "Let the notebooks do `from viz_config import VizConfig`",

    # ---- Section headings ----
    "全局配置与环境初始化": "Global configuration and environment setup",
    "全局配置与风格设置": "Global configuration and style setup",
    "环境与参数配置 (Configuration)": "Environment and parameter configuration",
    "实验参数与路径配置 (Configuration)": "Experiment parameters and path configuration",
    "实验参数配置 (Experiment Configuration)": "Experiment configuration",
    "参数设置 (PySR Hyperparameters)": "PySR hyperparameters",
    "数据集构建脚本 (Dataset Construction)": "Dataset construction script",
    "数据准备 (Data Preparation)": "Data preparation",
    "数据读取 (Data Loading)": "Data loading",
    "数据读取与预处理": "Data loading and preprocessing",
    "数据加载与预处理 (Data Loading & Preprocessing)": "Data loading and preprocessing",
    "数据重构 (Reshaping: Wide to Long)": "Data reshaping (wide -> long)",
    "特征融合 (Feature Merging)": "Feature merging",
    "数据清洗与导出 (Cleaning & Export)": "Cleaning and export",
    "数据降采样 (Subsampling)": "Subsampling",
    "浓度预缩放 (Scaling)": "Concentration pre-scaling",
    "浓度预缩放": "Concentration pre-scaling",
    "配置与初始化 (Configuration & Initialization)": "Configuration and initialisation",
    "定义假设公式 (Hypothesis Formula Definition)": "Hypothesis formula definition",
    "执行参数拟合 (Parameter Fitting)": "Parameter fitting",
    "运行 PySR (Symbolic Regression Execution)": "Run PySR (symbolic regression)",
    "结果保存与性能评估 (Evaluation & Saving)": "Evaluation and saving",
    "可视化验证 1: 衰减曲线 (Curve Validation)": "Visual validation 1: decay curves",
    "可视化验证 2: 预测对比图 (Parity Plot)": "Visual validation 2: parity plot",
    "自动化实验循环 (Automated Experiment Loop)": "Automated experiment loop",
    "最终汇总 (Final Summary)": "Final summary",
    "循环测试 (Loop Experiment)": "Experiment loop",
    "统计结果 (Statistics)": "Statistics",
    "按 Case 名字划分 (Group Split)": "Group split by case",
    "按 Case 划分训练集和测试集": "Split train/test sets by case",
    "逻辑部分 A: 假设公式拟合 (Hypothesis Fitting)": "Block A: hypothesis formula fitting",
    "逻辑部分 B: 残差分析 (Residual Analysis)": "Block B: residual analysis",
    "绘图合并 (Combined Visualization)": "Combined visualisation",
    "绘图 (Figure 8: Data Efficiency)": "Plotting (Figure 8: Data Efficiency)",
    "核心逻辑: 参数提取与稳定性分析": "Core logic: parameter extraction and stability analysis",
    "核心绘图：背景区域与数据曲线": "Core plot: background zones and data curves",
    "绘图 (Plotting)": "Plotting",
    "绘图初始化": "Plot initialisation",
    "绘图初始化 (Plot Initialization)": "Plot initialisation",
    "绘图: 参数稳定性分析 (Figure 7)": "Plot: parameter stability (Figure 7)",
    "图表标注与细节美化": "Annotations and styling",
    "图表装饰 (Labels & Title)": "Labels and title",
    "轴刻度优化 (Axis Formatting)": "Axis formatting",
    "坐标轴与图例设置 (Axes & Legend)": "Axes and legend",
    "坐标轴与标签设置": "Axes and labels",
    "坐标轴与边框美化": "Axes and spines styling",
    "标题与图例设置": "Title and legend",
    "标题与标签": "Title and labels",
    "图例与网格": "Legend and grid",
    "保存与显示": "Save and show",
    "保存与输出": "Save and export",
    "结果保存 (Saving Predictions) ---": "Save predictions ---",
    "指标计算与汇总 (Metric Calculation) ---": "Metric calculation ---",
    "打印统计信息 (Statistics)": "Print statistics",
    "读取并准备数据": "Load and prepare data",
    "读取真实数据": "Load real data",
    "读取真实的实验结果数据": "Load real experimental data",
    "读取真实实验数据": "Load real experimental data",
    "执行绘图": "Run the plot",
    "开始绘图 (1x2 Subplots)": "Begin plotting (1x2 subplots)",
    "数据分析与关键点计算": "Data analysis and key-point computation",
    "浓度缩放系数 (Scaling Factor)": "Concentration scaling factor",
    "浓度缩放因子": "Concentration scaling factor",
    "缩放处理": "Apply scaling",

    # ---- data.ipynb ----
    "功能: 将原始的 CFD 模拟结果 (summary 表) 和工况参数 (cases 表)":
        "Purpose: merge the raw CFD results (summary table) with the case parameters (cases table)",
    "合并清洗为机器学习可用的标准数据集 (train_dataset_ready.csv)。":
        "and clean them into a ML-ready dataset (train_dataset_ready.csv).",
    "输入:": "Inputs:",
    "输出:": "Outputs:",
    "每个 Case 的入口条件 (V_in, C_in, Area)":
        "Per-case inlet conditions (V_in, C_in, Area)",
    "每个 Case 的沿程浓度分布数据":
        "Per-case concentration profile along the domain",
    "融合后的长表格式数据": "Merged long-format dataset",
    "读取原始数据": "Load the raw data",
    "正在读取原始数据文件...": "Reading raw data files...",
    "错误: 找不到文件 {e.filename}。请确保 cases.csv 和 summary_0_499.csv 在当前目录下。":
        "ERROR: file {e.filename} not found. Make sure cases.csv and summary_0_499.csv sit in the current directory.",
    "原始 summary 表是宽表格式 (每一列代表一个距离点)，不适合模型训练。":
        "The raw summary table is in wide format (one column per distance point), which is not ideal for training.",
    "使用 melt 函数将其转换为长表格式 (每一行代表一个样本点)。":
        "Use melt() to convert it to long format (one sample per row).",
    "正在执行数据透视 (Melting)...": "Running the melt step...",
    "类型转换": "Type casting",
    "列名默认为字符串，需转换为数值类型以便后续计算":
        "Column names are strings by default - cast them to floats for the downstream math.",
    "将工况参数 (V_in, C_in, Area) 根据 Case ID 关联到每一个样本点上。":
        "Join the per-case parameters (V_in, C_in, Area) onto every sample via Case ID.",
    "这样每个样本点都包含了完整的输入特征 (Input) 和输出目标 (Output)。":
        "Each sample then carries both its full input features and its target output.",
    "正在合并工况参数...": "Merging case parameters...",
    "检查数据完整性": "Sanity-check completeness",
    "原始合并数据形状: {df_merged.shape}": "Merged shape:           {df_merged.shape}",
    "清洗后数据形状 (去除空值): {df_merged.shape}": "Cleaned shape (no NaN): {df_merged.shape}",
    "预览数据": "Preview",
    "数据预览 (前5行):": "Data preview (first 5 rows):",
    "保存最终数据集": "Save the final dataset",
    "数据集已成功构建并保存至: {output_file}":
        "Dataset built successfully and saved to {output_file}",

    # ---- datasee.ipynb ----
    "绘图环境设置 (Plotting Setup)": "Plotting setup",
    "使用 Seaborn 默认风格，使图表更美观":
        "Use the seaborn default style for nicer looks",
    "中文支持配置 (如果系统中安装了 SimHei 字体可取消注释)":
        "Chinese font fallback (uncomment if SimHei is installed)",
    "读取并绘制指定 Case 的沿程浓度分布曲线 (Concentration Profile).":
        "Load and plot the concentration profile for a given Case.",
    "用于快速检查原始数据的质量和物理规律是否符合预期。":
        "Quick sanity check that the raw data behaves as expected.",
    "参数:": "Args:",
    "目标 Case ID (例如": "Target Case ID (e.g.",
    "工况参数文件路径 (包含 V_in, C_in, Area)":
        "Path to the cases file (V_in, C_in, Area)",
    "浓度分布数据文件路径 (包含沿程浓度)":
        "Path to the summary file (concentration profile)",
    "错误: 找不到数据文件 {cases_file} 或 {summary_file}":
        "ERROR: cannot find {cases_file} or {summary_file}",
    "检查 Case 是否存在": "Check that the case exists",
    "错误: 找不到 Case": "ERROR: case not found",
    "提取工况基本信息 (Extract Input Conditions)": "Extract inlet conditions",
    "获取该 Case 对应的入口浓度(C_in), 风速(V_in), 面积(Area)":
        "Grab the per-case C_in, V_in and Area",
    "提取浓度曲线数据 (Extract Output Profile)":
        "Extract the concentration profile",
    "在 summary 表中找到对应那一行":
        "Locate the matching row in the summary table",
    "去掉非数值列，剩余的列名即为距离点 (":
        "Drop non-numeric columns; the remaining column names are distance points (",
    "准备绘图数据": "Prepare plot data",
    "将列名转换浮点数作为 X 轴 (Distance)":
        "Cast column names to floats for the X axis (distance)",
    "将行数值转换为浮点数作为 Y 轴 (Concentration)":
        "Cast row values to floats for the Y axis (concentration)",
    "绘制沿程浓度曲线 (蓝色实线)":
        "Plot the concentration profile (solid blue)",
    "绘制入口浓度参考线 (红色虚线)":
        "Plot the inlet-concentration reference line (dashed red)",
    "用于直观对比当前浓度相对于入口浓度的衰减情况":
        "Gives a visual sense of decay relative to the inlet concentration",
    "添加网格以便读数": "Add a grid for easier reading",
    "数据概览 ---": "Data summary ---",
    "入口条件: C_in={c_in:.2e}, V_in={v_in:.2f}, Area={area:.1f}":
        "Inlet conditions: C_in={c_in:.2e}, V_in={v_in:.2f}, Area={area:.1f}",
    "沿程最大浓度: {concentrations.max():.2e}":
        "Max concentration along path: {concentrations.max():.2e}",
    "沿程最小浓度: {concentrations.min():.2e}":
        "Min concentration along path: {concentrations.min():.2e}",
    "出口(1100m)浓度: {concentrations[-1]:.2e}":
        "Outlet (1100 m) concentration: {concentrations[-1]:.2e}",
    "发生错误: {e}": "Error: {e}",
    "在此处修改你想查看的 Case 名字 (例如":
        "Change the case name you want to inspect here (e.g.",
}
