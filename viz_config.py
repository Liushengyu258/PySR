import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

class VizConfig:
    # ==========================================
    # 1. 字体与尺寸设置 (Fonts & Sizes)
    # ==========================================
    FONT_FAMILY = 'serif'
    FONT_SERIF = ['Times New Roman'] # 论文标准字体
    MATH_FONT = 'stix'               # 数学公式字体，风格接近 Times
    
    TITLE_SIZE = 18    # 图表标题字号
    LABEL_SIZE = 18    # 坐标轴标签字号 (如 "Distance (m)")
    TICK_SIZE = 15     # 刻度数字字号 (如 "0.0, 0.5, 1.0")
    LEGEND_SIZE = 16   # 图例文字字号
    DPI = 300          # 输出图片清晰度

    # ==========================================
    # 2. 高级配色方案 (Advanced Color Palettes)
    #    风格: Nature/Science 学术风
    # ==========================================
    
    # --- 基础色板 (6色循环) ---
    # Index 0: 深蓝 (Deep Blue)
    # Index 1:  slate灰色 (Slate Grey)
    # Index 2: 浓红 (Rich Red)
    # Index 3: 森林绿 (Forest Green)
    # Index 4: 琥珀黄 (Goldenrod)
    # Index 5: 深紫 (Deep Purple)
    COLOR_PALETTE = ['#00467F', '#A5A5A5', '#D62728', '#2E7D32', '#FFB300', '#5B358C']
    
    # --- 语义化颜色映射 (关键部分) ---
    
    # 1. 主要数据/模型 (Main Data)
    #    用途: 
    #      - 图1(Combined): CFD 原始数据点 (Scatter points)
    #      - 图4(Degradation): Direct SR 基准曲线
    #      - 图5(Denoising): Ground Truth (真实值) 点
    #      - 图6(Robustness): Ours (Hybrid) 本文方法曲线 (原有图3逻辑)
    #      - 图8(Efficiency): R2 均值曲线
    COLOR_MAIN = '#00467F'       # 深蓝色
    
    # 2. 次要数据/基准/背景 (Secondary Data)
    #    用途:
    #      - 图4: 临界分界线 (Breakdown Point Line)
    #      - 图5: 含噪数据点 (Noisy Data)
    #      - 图6: Baseline (Direct SR) 对比方法曲线
    #      - 图8: 误差棒颜色 (Error Bars)
    #      - 图7: 稳定性区域阴影边框
    COLOR_SECONDARY = '#A5A5A5'  # 灰色
    
    # 3. 高亮/重点/拟合线 (Highlight/Fit)
    #    用途:
    #      - 图1: 提出的公式拟合线 (Proposed Formula Line)
    #      - 图4: 失败区域背景 (Failure Zone) - 需配合 alpha 透明度
    #      - 图5: MLP 去噪后输出线 (Denoised Line)
    #      - 图8: 最佳效率点 (Optimal Point) 及指示线
    COLOR_HIGHLIGHT = '#CD5C5C'  # 红色
    
    # 4. 成功/安全/稳定区域 (Success/Safe Zone)
    #    用途:
    #      - 图4: 鲁棒区域背景 (Robust Zone)
    #      - 图6: 鲁棒区域背景
    #      - 图8: 高效率区域阴影线 (High Efficiency Zone Hatch)
    COLOR_SUCCESS = '#00E079'    # 绿色
    
    # 5. 警告/辅助/阈值 (Warning/Threshold)
    #    用途:
    #      - 图1: 残差图的 ±2 标准差阈值线
    COLOR_WARNING = '#FFB300'    # 琥珀色/黄色
    
    # --- UI 元素颜色 ---
    COLOR_GRID = '#E0E0E0'       # 网格线 (浅灰)
    COLOR_AXIS = '#333333'       # 坐标轴与文字 (深灰，避免纯黑太刺眼)
    COLOR_BACKGROUND = '#FFFFFF' # 背景色

    @classmethod
    def set_style(cls):
        """应用全局 matplotlib 样式设置"""
        plt.rcParams['font.family'] = cls.FONT_FAMILY
        plt.rcParams['font.serif'] = cls.FONT_SERIF
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['mathtext.fontset'] = cls.MATH_FONT
        plt.rcParams['figure.dpi'] = cls.DPI
        
        # 轴线与网格
        plt.rcParams['axes.edgecolor'] = cls.COLOR_AXIS
        plt.rcParams['axes.labelcolor'] = cls.COLOR_AXIS
        plt.rcParams['xtick.color'] = cls.COLOR_AXIS
        plt.rcParams['ytick.color'] = cls.COLOR_AXIS
        plt.rcParams['grid.color'] = cls.COLOR_GRID
        plt.rcParams['grid.linestyle'] = '--'
        plt.rcParams['grid.alpha'] = 0.6
        
        # 图例
        plt.rcParams['legend.frameon'] = True
        plt.rcParams['legend.framealpha'] = 0.95
        plt.rcParams['legend.edgecolor'] = cls.COLOR_AXIS
        plt.rcParams['legend.fancybox'] = False

    @classmethod
    def get_color(cls, index):
        """根据索引获取调色板颜色 (自动循环)"""
        return cls.COLOR_PALETTE[index % len(cls.COLOR_PALETTE)]
