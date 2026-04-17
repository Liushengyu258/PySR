# -*- coding: utf-8 -*-
"""Chinese->English dictionary part 3: Visualization notebooks + misc words."""

T3 = {
    # ---- Visualization.ipynb (Fig. 1) ----
    "加载统一的绘图风格配置 (viz_config.py)，确保所有图表字体、颜色一致":
        "Load the shared plotting style (viz_config.py) so every figure uses the same fonts and colours",
    "加载统一的绘图风格配置 (viz_config.py)":
        "Load the shared plotting style (viz_config.py)",
    "定义输出目录，用于存放生成的 PDF 图表":
        "Define the output directory for the generated PDFs",
    "浓度数据的缩放因子，用于避免数值过小导致拟合不稳定":
        "Concentration scaling factor - avoids numerical instability caused by very small values",
    "原始数据可能是 1e-7 量级，缩放后变为 1.0 量级":
        "Raw values are ~1e-7; after scaling they become ~1.0",
    "正在读取数据...": "Reading data...",
    "错误：未找到 train_dataset_ready.csv 文件": "ERROR: train_dataset_ready.csv not found",
    "读取包含 CFD 模拟结果的 CSV 文件": "Read the CSV with the CFD simulation results",
    "对浓度数据进行缩放处理": "Apply scaling to the concentration data",
    "提取特征变量用于后续计算": "Extract features for downstream computation",
    "入口风速": "Inlet velocity",
    "截面积": "Cross-sectional area",
    "距离": "Distance",
    "缩放后的入口浓度": "Scaled inlet concentration",
    "缩放后的出口浓度 (真实值)": "Scaled outlet concentration (ground truth)",
    "正在执行代码 1 的拟合逻辑...": "Running the block-A fit...",
    "定义物理假设公式": "Define the physical hypothesis formula",
    "该公式基于物理直觉：浓度随距离衰减，且受风速和截面积影响":
        "Physics-motivated: concentration decays with distance, modulated by velocity and area",
    "时间尺度项：距离/速度的平方根，反映扩散时间特征":
        "Timescale term: sqrt(distance / velocity) - characteristic diffusion time",
    "有效面积项：考虑时间尺度对扩散范围的修正":
        "Effective-area term: diffusion range corrected by the timescale",
    "分母项：距离与有效面积的组合，类似于扩散方程的解的形式":
        "Denominator: distance combined with effective area - similar to diffusion-equation solutions",
    "确保分母不会因为有效面积为负而出现物理上不合理的数值":
        "Guard against physically meaningless values when the effective area goes negative",
    "拟合的初始猜测值 (Initial Guess)": "Initial guess for the fit",
    "打包自变量": "Pack the independent variables",
    "使用非线性最小二乘法拟合参数":
        "Fit the parameters via non-linear least squares",
    "限制参数范围，防止出现无物理意义的负值或过大值":
        "Constrain parameter ranges to avoid non-physical / too-large values",
    "计算拟合后的预测值": "Compute the fitted predictions",
    "计算决定系数 R2，评估拟合优度":
        "Compute R^2 as the goodness-of-fit measure",
    "代码 1 拟合成功。": "Block A fit succeeded.",
    "代码 1 拟合出错: {e}": "Block A fit failed: {e}",
    "正在执行代码 2 的残差计算逻辑...": "Running the block-B residual analysis...",
    "使用已知的第二组参数 (可能来自文献或之前的迭代)":
        "Use a known second parameter set (from literature or a prior iteration)",
    "使用原始比例的数据进行计算 (注意这里重新定义了变量名以免混淆)":
        "Operate on the raw-scale data (variables renamed here to avoid collisions)",
    "计算第二种模型下的预测值": "Compute predictions under the second model",
    "计算残差 (真实值 - 预测值)": "Compute residuals (truth - prediction)",
    "标准化残差 (Residuals / Std_Dev)，用于判断异常值 (通常 >2 或 <-2 为异常)":
        "Standardised residuals (residual / std) - |value| > 2 is typically an outlier",
    "计算该模型的 R2": "R^2 of this model",
    "正在绘制合并大图...": "Rendering the combined figure...",
    "创建大图画布，设置为 22x12 英寸": "Create a 22x12-inch canvas",
    "使用 GridSpec 将画布分为左右两部分 (比例 1.1:1)":
        "Split the canvas via GridSpec into a left/right pair (ratio 1.1:1)",
    "左侧区域: 4个典型案例的拟合曲线展示 ---":
        "Left panel: fit curves for four representative cases ---",
    "子图布局": "Sub-panel layout",
    "固定随机种子确保复现性": "Fix the RNG for reproducibility",
    "随机抽取 4 个 Case 进行展示": "Draw 4 cases for display",
    "仅在左上角第一个子图添加": "Only add this to the top-left sub-panel",
    "提取当前 Case 的数据并按距离排序":
        "Slice out the current case's data and sort by distance",
    "使用拟合好的参数计算预测曲线":
        "Compute the predicted curve from the fitted parameters",
    "绘制 CFD 真实数据点 (深蓝色)": "Plot the CFD data points (deep blue)",
    "绘制拟合曲线 (红色)": "Plot the fit curve (red)",
    "设置子图标题和坐标轴标签": "Set sub-panel titles and axes labels",
    "右侧区域: 统计分析图 (Parity Plot & Residual Plot) ---":
        "Right panel: statistical analysis (parity + residuals) ---",
    "右上: 对角线图 (Parity Plot) ---": "Top-right: parity plot ---",
    "用于展示预测值与真实值的一致性":
        "Shows how closely predictions track ground truth",
    "绘制散点 (真实值 vs 预测值)": "Scatter (truth vs prediction)",
    "绘制对角线 (理想情况 y=x)": "Draw the y=x reference line",
    "右下: 残差图 (Residual Plot) ---": "Bottom-right: residual plot ---",
    "用于检查异方差性 (Heteroscedasticity) 和模型偏差":
        "Inspect heteroscedasticity and model bias",
    "绘制标准化残差散点 (紫色)": "Scatter the standardised residuals (purple)",
    "绘制辅助线：0轴，以及 +/- 2 标准差警戒线":
        "Reference lines: y=0 and +/- 2 sigma thresholds",
    "调整布局以避免重叠，pad_inches 控制边缘留白":
        "tight_layout to avoid overlap; pad_inches controls the margin",
    "虽然有警告但在复杂 GridSpec 中通常能起作用":
        "Works despite the warning in complex GridSpec cases",
    "也可以尝试 fig.subplots_adjust() 手动调整":
        "You can also call fig.subplots_adjust() manually if needed",
    "带标签的合并图已保存至: {output_path}":
        "Labelled combined figure saved to: {output_path}",

    # ---- Visualization_1 (Fig. 4) ----
    "引入统一的配色和样式配置文件，确保所有插图符合学术发表标准":
        "Import the shared colour/style configuration so every figure meets publication standards",
    "定义结果输出目录，生成的 PDF 将保存在此处":
        "Output directory - generated PDFs land here",
    "检查数据文件是否存在，如果不存在则生成模拟数据用于演示代码逻辑":
        "If the data file is missing, generate synthetic data to exercise the plotting code",
    "构造模拟数据：模拟噪声比例从 0% 到 200% 的变化":
        "Synthetic data: noise levels from 0% to 200%",
    "保持高位直到 45% 左右开始下降，展示模型的鲁棒性边界":
        "Stay high until ~45%, then drop - illustrates the robustness boundary",
    "崩溃点": "breakdown point",
    "的 X 轴位置": " X position",
    "根据数据特征，模型在 47.5% 左右性能急剧下降":
        "Empirically, performance drops sharply around 47.5%",
    "绘制背景区域 (Background Zones)": "Plot the background zones",
    "利用不同颜色的背景区分模型的":
        "Use different background colours to split the model's",
    "左侧：鲁棒区域 (Robust Zone)，使用淡淡的绿色 (COLOR_SUCCESS)":
        "Left: robust zone (light green, COLOR_SUCCESS)",
    "右侧：失效区域 (Failure Zone)，使用淡淡的红色 (COLOR_HIGHLIGHT)":
        "Right: failure zone (light red, COLOR_HIGHLIGHT)",
    "绘制临界分界线 (Breakdown Threshold)":
        "Plot the breakdown threshold line",
    "在崩溃点处绘制一条垂直虚线，作为视觉分割":
        "Vertical dashed line at the breakdown point as a visual divider",
    "绘制性能衰减曲线 (Performance Curve)":
        "Plot the performance-degradation curve",
    "展示 R2 随噪声增加的变化趋势": "Shows R^2 vs. noise level",
    "使用主色调 (COLOR_MAIN) 绘制连线和数据点":
        "Use COLOR_MAIN for the line and markers",
    "添加区域文字标注 (Zone Labels)": "Add zone labels",
    "将文字放置在图表底部，避免遮挡数据曲线":
        "Place labels at the bottom to avoid covering the data",
    "标注 - 绿色加粗": "annotation - green bold",
    "标注 - 红色加粗": "annotation - red bold",
    "标注关键崩溃点 (Breakdown Point Annotation)":
        "Annotate the critical breakdown point",
    "在分界线中间位置添加说明文字，使用白色背景框增加可读性":
        "Annotate mid-way along the divider with a white bbox for legibility",
    "设置 X 轴刻度间隔为 20% (0.2)，并将其格式化为百分比字符串 (如":
        "X ticks every 20% (0.2), formatted as a percent string (e.g.",
    "设置坐标轴标签和主标题，支持 LaTeX 公式 (如 $R^2$)":
        "Axis labels and title (LaTeX supported, e.g. $R^2$)",
    "添加图例，放置在右上角": "Legend (top-right)",
    "添加网格线，帮助读取数值，使用浅灰色虚线":
        "Light dashed grid to help read values",
    "设置坐标轴显示范围": "Set axis limits",
    "保存为高分辨率 PDF (300 DPI)": "Save as a 300-DPI PDF",
    "图表已保存至: {output_path}": "Figure saved to: {output_path}",
    "鲁棒区": "robust zone",
    "失效区": "failure zone",

    # ---- Visualization_2 (Fig. 5) ----
    "应用统一的 VizConfig 配置，确保字体、DPI 等一致":
        "Apply the shared VizConfig so fonts, DPI, etc. stay consistent",
    "输入文件路径：包含 MLP 去噪前后的预测对比数据":
        "Input path: predictions before and after MLP denoising",
    "预定义单位字符串，方便后续 label 使用":
        "Pre-defined unit string for labels",
    "检查数据是否存在，若不存在则生成模拟数据，保证绘图代码可运行":
        "Fall back to synthetic data if the real file is missing",
    "文件路径不存在，生成模拟数据用于演示代码逻辑...":
        "File missing - generating synthetic data for demo purposes...",
    "模拟生成一条带有噪声和去噪结果的曲线":
        "Synthetic: a noisy curve plus its denoised counterpart",
    "真实值 (Clean Truth)": "Ground truth",
    "噪声值 (Noisy Input)": "Noisy input",
    "预测值 (MLP Output - 模拟去噪效果)":
        "Predicted (MLP output - synthetic denoising)",
    "错误：未找到数据文件 {INPUT_PATH}":
        "ERROR: data file not found: {INPUT_PATH}",
    "选择一个特定的 Case 进行展示": "Pick a representative case",
    "计算 R2 分数": "Compute R^2",
    "子图 (a)：局部序列对比 (Local Sequence Denoising)":
        "Sub-panel (a): local sequence denoising",
    "目的：直观展示去噪前后的序列形态对比":
        "Purpose: visualise sequence shape before/after denoising",
    "绘制含噪数据点 (Noisy Data)": "Plot noisy data points",
    "使用次要颜色 (灰色)，降低视觉权重，作为背景对比":
        "Use the secondary colour (grey) so they sit in the background",
    "绘制真实值数据点 (Ground Truth)": "Plot ground-truth points",
    "使用主色 (深蓝)，代表 Ground Truth":
        "Use COLOR_MAIN (deep blue) for ground truth",
    "绘制去噪后的预测曲线 (MLP Output)":
        "Plot the denoised prediction curve (MLP output)",
    "使用高亮色 (红色实线)，突出展示模型的输出效果":
        "Use the highlight colour (solid red) to emphasise the model output",
    "关键特性] 添加嵌入式放大图 (Inset Plot)":
        "Key feature] Add an inset zoom",
    "在主图 (ax1) 中创建一个子区域用于放大显示细节":
        "Create a sub-region inside ax1 to show detail",
    "分别代表 [x, y, width, height] 的相对比例坐标":
        "Values are [x, y, width, height] as fractions of the parent axes",
    "在放大区域中重新绘制同样的数据，保持颜色一致":
        "Redraw the same data in the inset, keeping colours consistent",
    "设置放大的 X 轴范围 (Zoom-in Region)": "Set the zoom-in X range",
    "自动计算放大区域对应的 Y 轴范围，避免手动写死":
        "Auto-compute the corresponding Y range (avoids hard-coding)",
    "调整子图样式": "Tweak sub-axes styling",
    "设置子图边框颜色": "Colour the inset spines",
    "绘制连接线，连接主图选区和放大图 (mark_inset)":
        "Connector lines between main axes and inset (mark_inset)",
    "子图 (b)：对角线图 (Parity Plot)": "Sub-panel (b): parity plot",
    "目的：对比": "Purpose: compare",
    "原始噪声 vs 真实值": "raw-noise vs ground truth",
    "去噪后 vs 真实值": "denoised vs ground truth",
    "的分布情况": " distributions",
    "绘制原始含噪数据 (Noisy vs Truth)": "Plot raw noisy data (noisy vs truth)",
    "颜色：灰色 (Secondary)，显示原始数据的离散程度":
        "Colour: grey (secondary) - shows raw-data spread",
    "绘制去噪后数据 (Denoised vs Truth)": "Plot denoised data (denoised vs truth)",
    "颜色：红色 (Highlight)，显示去噪后的收敛程度":
        "Colour: red (highlight) - shows denoised tightness",
    "绘制对角线 (Identity Line y=x)": "Draw the identity line (y = x)",
    "图已保存至: {output_pdf}": "Figure saved to: {output_pdf}",
    "去噪": "denoising",
    "添加": "add",

    # ---- Visualization_3 (Fig. 6) ----
    "引用配置中的常量，方便后续使用": "Pull constants from VizConfig for local reuse",
    "引用配置中的字号常量": "Pull font-size constants from VizConfig",
    "检查是否存在真实数据文件": "Check whether the real data file exists",
    "构造模拟数据用于展示图表效果":
        "Build synthetic data to show the figure appearance",
    "模拟噪声比例从 0% 到 200%": "Synthetic noise levels from 0% to 200%",
    "模拟 Baseline (Direct SR) 的表现：在 50% 噪声处发生崩溃 (Sigmoid 形状下降)":
        "Synthetic baseline (Direct SR): sigmoid drop around 50% noise",
    "截断底部，防止过低": "Floor value to keep the curve reasonable",
    "模拟 Ours (Hybrid Framework) 的表现：随噪声线性缓慢下降，保持较高的鲁棒性":
        "Synthetic Ours (hybrid framework): slow linear decline - robust",
    "定义关键的崩溃点 (Critical Breakdown Point) 位置，用于划分区域":
        "Pin the critical breakdown point used to split the zones",
    "轴显示的最大范围": "Max visible axis range",
    "绘制背景区域与分界线 (Zones & Thresholds)":
        "Plot background zones and threshold",
    "绘制背景色块，直观区分": "Coloured background blocks to separate",
    "左侧：鲁棒区域 (Robust Zone) - 浅绿色背景": "Left: robust zone (light green)",
    "右侧：失效区域 (Failure Zone) - 浅红色背景": "Right: failure zone (light red)",
    "绘制垂直分界线": "Draw the vertical divider",
    "在分界线上添加标注文字": "Annotate the divider with text",
    "添加白色背景以防文字与线重叠":
        "White bbox so the text does not clash with the line",
    "绘制数据曲线 (Data Curves)": "Plot the data curves",
    "使用次要颜色 (灰色) 和虚线，表示这是对照组":
        "Secondary colour (grey) + dashed - signals the control group",
    "只有边框颜色，中心为白色，增加层次感":
        "Edge-only markers with white centres for depth",
    "使用主色 (深蓝) 和实线，强调这是本文提出的方法":
        "COLOR_MAIN (deep blue) + solid - emphasises our proposed method",
    "使用星号标记，突出显示": "Star markers to stand out",
    "添加辅助标注 (Annotations)": "Add helper annotations",
    "区域名称标注 (放置在底部)": "Zone-name labels (bottom)",
    "绿色)": "green)",
    "红色)": "red)",
    "工程要求线 (Engineering Requirement Line)": "Engineering-requirement line",
    "在 R2=0.9 处绘制一条水平虚线，表示工程上可接受的最低精度":
        "Horizontal dashed line at R^2 = 0.9 - engineering-acceptable threshold",
    "轴刻度设置": "Tick configuration",
    "每隔 20% 设置一个刻度": "One tick every 20%",
    "将数值转换为百分比字符串 (如":
        "Format values as a percent string (e.g.",
    "图例": "Legend",
    "放置在右上角，带边框": "Top-right, with frame",
    "坐标轴范围与网格": "Axis limits and grid",
    "自动调整布局，pad_inches 防止边缘被裁剪":
        "tight_layout with pad_inches so margins are preserved",
    "保存为高精度 PDF": "Save as a high-resolution PDF",
    "对比图已保存至: {output_path}": "Comparison figure saved to: {output_path}",
    "提示：未找到文件 {csv_path}，使用模拟数据进行演示。":
        "Note: {csv_path} missing - using synthetic data for the demo.",

    # ---- Visualization_4 (Fig. 7) ----
    "定义要分析的噪声水平列表": "Noise levels to analyse",
    "定义目标物理公式 (Target Physics Formula)": "Define the target physics formula",
    "该公式用于从去噪后的数据中反演物理参数 (a, b, c, d)":
        "Used to invert physical parameters (a, b, c, d) from denoised data",
    "公式形式: C(Dist) = C_in * [ a / ( (Dist / (Area + c*sqrt(V_in) + d)) + b ) ]":
        "Formula: C(Dist) = C_in * [ a / ( (Dist / (Area + c*sqrt(V_in) + d)) + b ) ]",
    "物理假设公式，用于曲线拟合。": "Physics hypothesis formula used for curve fitting.",
    "输入 X: [V_in, C_in, Area, Distance]": "Input X: [V_in, C_in, Area, Distance]",
    "参数: a, b, c, d (待确定的物理系数)":
        "Parameters: a, b, c, d (physical coefficients to determine)",
    "输出: 预测的出口浓度 C_out": "Output: predicted outlet concentration C_out",
    "计算有效面积项 (Effective Area Term)": "Compute the effective-area term",
    "防止负数开根号及除零": "Guard against sqrt of negatives and division by zero",
    "防止分母为零": "Guard against a zero denominator",
    "计算中间分式: Dist / Effective_Area":
        "Intermediate ratio: Dist / effective_area",
    "计算总分母: term_middle + b": "Full denominator: term_middle + b",
    "最终计算浓度": "Final concentration",
    "正在处理数据...": "Processing data...",
    "错误：找不到 train_dataset_ready.csv":
        "ERROR: train_dataset_ready.csv not found",
    "读取原始训练数据": "Load the raw training data",
    "准备数据矩阵 X_raw": "Build the feature matrix X_raw",
    "对数据进行标准化，因为 MLP 模型是在标准化数据上训练的":
        "Standardise the data (the MLP was trained on standardised inputs)",
    "拟合初始猜测值 (Initial Guess)": "Initial guess for the fit",
    "这些值通常来自先验知识或初步探索":
        "Usually from prior knowledge or a preliminary exploration",
    "循环遍历每个噪声水平，分析参数稳定性":
        "Loop over every noise level and analyse parameter stability",
    "加载在该噪声水平下训练好的 MLP 模型":
        "Load the MLP trained at this noise level",
    "使用 MLP 对原始数据进行": "Use the MLP on the raw data for",
    "注意：这里我们假设 MLP 学到了潜在的物理规律，因此其预测值应更接近真实物理值":
        "Assumption: the MLP has learned the underlying physics, so its output is closer to the real values",
    "使用去噪后的数据拟合物理公式，提取参数":
        "Fit the physics formula on the denoised data and extract parameters",
    "增加迭代次数以确保收敛": "Bump the iteration count for convergence",
    "记录参数值": "Record the parameters",
    "处理失败: {e}": "Processing failed: {e}",
    "如果没有提取到参数 (例如文件缺失)，则生成模拟数据用于绘图演示":
        "If no parameters were extracted (e.g. missing files), fall back to synthetic data",
    "提示：未提取到参数，生成模拟数据用于绘图演示。":
        "Note: no parameters extracted - using synthetic data for the demo.",
    "模拟参数随噪声增加而在真值附近波动":
        "Synthetic parameters fluctuate around the true values as noise grows",
    "参数归一化 (Normalization)": "Parameter normalisation",
    "将所有参数除以基准值 (0% 噪声下的参数值)，以便在同一张图上比较相对变化":
        "Normalise every parameter by its zero-noise baseline so we can compare relative shifts",
    "正在绘制图 7...": "Plotting Figure 7...",
    "绘制高稳定性区域 (High Stability Zone)": "Plot the high-stability zone",
    "在 y=1.0 上下 10% 的范围内绘制阴影带，表示参数波动的可接受范围":
        "Shade a +/-10% band around y = 1.0 for acceptable fluctuation",
    "边框颜色": "Edge colour",
    "阴影样式": "Hatch style",
    "线宽": "Line width",
    "添加区域文字说明": "Region annotation",
    "绘制参数变化曲线": "Plot the parameter-trajectory curves",
    "使用配置中的调色板颜色": "Use the VizConfig palette colours",
    "参数对应的 LaTeX 希腊字母标签":
        "Greek-letter (LaTeX) labels for the parameters",
    "绘制基准线 (y=1.0)": "Plot the baseline (y = 1.0)",
    "轴刻度显示为百分比": "Axis ticks as percents",
    "动态调整 Y 轴范围": "Dynamically adjust the Y range",
    "自动调整布局": "tight_layout",
    "图 7 已保存至: {output_img}": "Figure 7 saved to: {output_img}",
    "背景透明": "transparent background",
    "透明度": "alpha (transparency)",

    # ---- Visualization_5 (Fig. 8) ----
    "应用统一的配色和样式配置 (viz_config.py)":
        "Apply the shared colour/style configuration (viz_config.py)",
    "路径设置": "Path configuration",
    "确保输出目录存在": "Make sure the output directory exists",
    "构造示例数据 (如果文件不存在)": "Build sample data (if the real file is missing)",
    "训练集大小": "Training-set size",
    "测试集 R2 均值": "Test-set R^2 mean",
    "测试集 R2 标准差 (用于误差棒)": "Test-set R^2 std (for error bars)",
    "按训练集大小排序，确保连线正确":
        "Sort by training-set size so the connecting line is correct",
    "设定阈值寻找": "Pick a threshold to locate",
    "最佳效率点": "optimal efficiency point",
    "定义为达到最大 R2 的 99% 时的最小样本量":
        "Defined as the smallest sample count reaching 99% of the peak R^2",
    "选取满足阈值条件的第一个点 (即样本量最小的点)":
        "Select the first point above the threshold (smallest sample count)",
    "高效率区域": "high-efficiency zone",
    "的 X 轴范围": " X range",
    "范围设定为最佳点的前一个点到最大值的后一个点 (或基于比例)":
        "Range from just-before-optimal to just-after-max (or proportionally)",
    "颜色定义 - 使用 VizConfig 统一配置": "Colour definitions (from VizConfig)",
    "主曲线颜色 (深蓝)": "Main-curve colour (deep blue)",
    "误差棒颜色 (灰色)": "Error-bar colour (grey)",
    "最佳点颜色 (红色)": "Optimal-point colour (red)",
    "高效率区域颜色 (绿色)": "High-efficiency zone colour (green)",
    "绘制高效率区域 (High Efficiency Zone)": "Plot the high-efficiency zone",
    "使用带斜线 (hatch=": "Use a hatched (hatch=",
    "的矩形区域标注": " rectangle to mark it",
    "斜线填充": "Hatch fill",
    "斜线颜色": "Hatch colour",
    "置于最底层": "Send to the back",
    "计算Y轴显示范围": "Compute the Y axis range",
    "添加区域文字标注": "Add the zone annotation",
    "对数坐标下的几何中心": "Geometric centre on the log axis",
    "使用数据坐标，y 使用轴相对坐标 (0-1)":
        "Data coords for X, axis-fraction coords for Y (0-1)",
    "表示底部向上 5% 的位置": "5% above the bottom",
    "绘制误差棒曲线": "Plot the error-bar curve",
    "使用半对数坐标系 (x轴为对数)": "Semi-log axes (log on X)",
    "标记最佳效率点 (Optimal Point)": "Mark the optimal efficiency point",
    "绘制通过最佳点的垂直虚线":
        "Vertical dashed line through the optimal point",
    "添加标注文字 (Annotation)": "Annotation text",
    "自动调整标注框位置，避免遮挡曲线":
        "Auto-adjust annotation position to avoid covering the curve",
    "设置 X 轴为对数刻度": "Set X axis to log scale",
    "网格设置": "Grid configuration",
    "边框设置 (加粗所有边框)": "Spine styling (bold every spine)",
    "刻度设置 (向内刻度)": "Tick styling (inward ticks)",
    "图例设置": "Legend configuration",
    "保存高分辨率 PDF": "Save as a high-resolution PDF",

    # ---- Small single-word fragments (applied last) ----
    "设置轴label与标题": "Axis labels and title",
    "设置轴标签与标题": "Axis labels and title",
    "读取数据 (Data Loading)": "Load data",
    "准备数据 (Data Preparation)": "Prepare the data",
    "加载 VizConfig 中的学术风格配置": "Load the paper-style configuration from VizConfig",
    "缩放系数：处理浓度 1e-7 的量级问题，将其映射到 [0, 10] 左右的区间，方便符号回归搜索":
        "Scaling factor: map the ~1e-7 concentrations to ~[0, 10] to make the symbolic-regression search easier",
    "预测": "prediction",
    "标签": "label",
    "保存输出": "Save output",
    "和": " and ",
    "定义": "Define",
    "绿色": "green",
    "红色": "red",
    "蓝色": "blue",
    "灰色": "grey",
}
