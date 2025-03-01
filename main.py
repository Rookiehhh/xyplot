# main.py - 项目主入口
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from xyplot import XyPlot
from utils import read_data, create_flow_field_config, create_sine_config

def main():
    try:
        # 数据文件路径 - 修改为使用数据目录
        file_path = r"data/P-L1-IMM-SWMF_20221018004619_0005M_SWMF.dat"
        
        # 读取数据
        df = read_data(file_path)
        
        # 绘制复杂可视化
        create_complex_visualization(df)
        
    except Exception as e:
        print(f"错误: {e}")
        print("显示基本正弦图示例...")
        create_simple_visualization()

def create_complex_visualization(df):
    """创建复杂流场可视化"""
    # 网格数据准备
    x, y = df['X [R]'].values, df['Y [R]'].values
    xx = yy = np.linspace(-6.5, 6.5, 1000)
    X, Y = np.meshgrid(xx, yy)
    grid_data = griddata((x, y), df[df.keys()[7]].values, (X, Y), method="linear")
    U = griddata((x, y), df[df.keys()[8]].values, (X, Y), method="linear")
    V = griddata((x, y), df[df.keys()[9]].values, (X, Y), method="linear")
    
    # 创建流场配置
    cfg_flow = create_flow_field_config(X, Y, U, V, grid_data)
    
    # 创建正弦图配置
    cfg_sin = create_sine_config()
    
    # 多子图布局
    fig_dict = dict(
        height=10, width=15,
        title=dict(args='XyPlot 演示'),
    )
    
    axes_dict = dict(
        set_fig=fig_dict,
        axes=dict(
            init=(dict(args=(1, 2, 1), ), 122),
            axes=(cfg_flow, cfg_sin)
        )
    )
    
    # 创建并显示图表
    xy_plot = XyPlot(**axes_dict)
    xy_plot.show()

def create_simple_visualization():
    """创建简单的正弦函数可视化"""
    x = np.linspace(-np.pi, np.pi, 100)
    y = np.sin(x)
    
    set_fig_dict = dict(height=8, width=10)
    axes_dict = dict(
        plot=dict(args=(x, y), label='y=sin(x)', c='r', lw=2),
        title=r'y=sin(x)',
        grid=dict(linestyle=':', color='gray'),
        xlabel="x",
        ylabel="y",
        legend=dict(loc='upper right'),
    )
    
    cfg = dict(set_fig=set_fig_dict, axes=axes_dict)
    xyplt = XyPlot(**cfg)
    xyplt.show()

if __name__ == "__main__":
    main()