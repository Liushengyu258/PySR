# Hybrid Framework for Pollutant Concentration Prediction

本项目实现了一个基于符号回归 (Symbolic Regression, PySR) 与物理假设结合的混合框架，用于预测污染物浓度的空间分布。项目包含从数据清洗、公式探索、参数拟合、鲁棒性/数据效率实验到最终学术绘图的全套流程。

## 📂 项目文件结构 (Project Structure)

```
PySR/
├── README.md
├── .gitignore
├── viz_config.py              # 全局绘图风格配置 (字体/配色/字号)
│
├── data/                      # 所有原始与清洗后的数据
│   ├── cases.csv              # 每个 Case 的入口条件 (V_in, C_in, Area)
│   ├── summary_0_499.csv      # 每个 Case 沿程浓度分布 (原始 CFD 输出)
│   ├── cfd_lhs_cases.csv      # LHS 采样得到的工况点
│   ├── case.csv               # Fluent 自动化使用的时间步表
│   ├── train_dataset_ready.csv  # 融合后的长表数据 (机器学习标准输入)
│   └── Data_Efficiency_Curve.csv
│
├── notebooks/                 # 所有 Jupyter 分析流程
│   ├── 00_data_preparation/
│   │   ├── data.ipynb         # 数据清洗: cases+summary -> train_dataset_ready
│   │   └── datasee.ipynb      # 沿程浓度分布快速查看工具
│   ├── 01_stage1_exploration/
│   │   └── Stage1.ipynb       # PySR 纯数据驱动公式探索
│   ├── 02_stage2_verification/
│   │   └── Stage2.ipynb       # 物理假设拟合 (curve_fit) 提取 α,β,γ,δ
│   ├── 03_experiments/
│   │   ├── klw PySR.ipynb     # 鲁棒性实验 (噪声 0%~200%)  -> 图 6/7
│   │   └── add.ipynb          # 数据效率实验 (样本 100~44400) -> 图 8
│   └── 04_visualization/
│       ├── Visualization.ipynb    # 图 1: 综合展示 (拟合 + 残差)
│       ├── Visualization_1.ipynb  # 图 4: 性能衰减曲线
│       ├── Visualization_2.ipynb  # 图 5: 序列去噪效果
│       ├── Visualization_3.ipynb  # 图 6: 鲁棒性对比
│       ├── Visualization_4.ipynb  # 图 7: 参数稳定性
│       └── Visualization_5.ipynb  # 图 8: 数据效率
│
├── scripts/                   # 独立 Python 脚本
│   ├── cfd_pipeline/          # CFD 前处理与批处理
│   │   ├── data_generate.py     # LHS 生成 cfd_lhs_cases.csv
│   │   ├── case_copy.py         # 整理 Fluent 案例文件
│   │   ├── extract_data.py      # 从 dpX_area.out 提取沿程数据
│   │   ├── run_automation_linux.py  # 生成 Linux 批处理 .sh
│   │   └── fluent_template.jou      # Fluent Journal 模板
│   ├── lhs_sampling/          # LHS 分布可视化
│   │   ├── lhs.py
│   │   └── plot_lhs.py
│   ├── analysis_legacy/       # 早期探索脚本 (已被 notebooks 取代)
│   │   ├── fig.py
│   │   ├── pysr1.py
│   │   ├── test2.py
│   │   └── test_pysr.py
│   └── _patch_notebooks.py    # 内部工具 (批量修补 notebooks 的根路径)
│
├── figures/                   # 论文/报告用图
│   ├── Formula_Performance.png
│   ├── lhs_distribution.pdf
│   ├── lhs_distribution.tiff
│   └── 9.pdf
│
├── docs/
│   └── UNTITLED.opju          # Origin 工程文件
│
│── Stage1_Exploration/        # Stage1 notebook 输出 (保持在根目录以兼容)
│── Stage2_Hypothesis_Verification/  # Stage2 输出
│── Refined_Results_v4/        # 鲁棒性实验输出 (图 6/7 数据源)
│── Data_Efficiency_Results/   # 数据效率实验输出 (图 8 数据源)
└── outputs/                   # PySR 符号回归原始运行目录 (.gitignore)
```

> **路径约定**: 所有 notebook 的第 0 号 cell (`# [auto] project-root setup`)
> 会自动向上查找含 `.gitignore` 的目录并 `os.chdir()` 到项目根。
> 因此 notebook 无论放在哪里运行, 相对路径 (`data/...`, `Stage1_Exploration/...`)
> 都能正常工作。

---

## 🚀 使用流程 (Workflow)

1.  **数据构建**: 运行 `notebooks/00_data_preparation/data.ipynb` 生成 `data/train_dataset_ready.csv`。
2.  **公式探索**: 运行 `notebooks/01_stage1_exploration/Stage1.ipynb`。
3.  **假设验证**: 运行 `notebooks/02_stage2_verification/Stage2.ipynb`。
4.  **实验评估**:
    *   `notebooks/03_experiments/klw PySR.ipynb` — 鲁棒性数据。
    *   `notebooks/03_experiments/add.ipynb` — 数据效率数据。
5.  **生成图表**: 运行 `notebooks/04_visualization/Visualization*.ipynb`。

## 📝 备注 (Notes)

*   **配色方案**: 
    *   🔵 **Deep Blue**: 真实值 / 核心模型
    *   🔴 **Red**: 拟合线 / 重点高亮
    *   🟢 **Green**: 鲁棒区域
    *   ⚪ **Grey**: 对照组 (Baseline)
*   所有脚本已固定随机种子 (`random_state=42`) 以保证可复现性。
*   浓度数据均进行了 `1e7` 倍缩放处理。
