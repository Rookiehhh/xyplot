# utils.py - 实用函数
import numpy as np
import pandas as pd

def read_data(file):
    """
    从SWMF文件中读取数据
    
    参数:
        file (str): 文件路径
        
    返回:
        pandas.DataFrame: 包含数据的DataFrame
    """
    with open(file, 'r') as f:
        line_list = list(filter(lambda x: x[0] != '#', f.readlines()))
    variables = line_list[1].strip().split("=")[1].replace('"', '').split(",")
    data_list = []
    for line in line_list[6:]:
        try:
            line_data = [float(i) for i in line.strip().split(" ") if i]
        except:
            continue
        data_list.append(line_data)
    return pd.DataFrame(columns=variables, data=data_list)

def create_flow_field_config(X, Y, U, V, grid_data):
    """
    创建流场可视化配置
    
    参数:
        X, Y (ndarray): 网格坐标
        U, V (ndarray): 速度场分量
        grid_data (ndarray): 网格数据
        
    返回:
        dict: 流场图配置
    """
    return dict(
        title=dict(args="Flow Field Visualization", loc='left'),
        xlabel=dict(args="X [R]", c='k'),
        ylabel=dict(args="Y [R]", c='k'),
        streamplot=dict(args=(X, Y, U, V), density=1.5, linewidth=0.5, arrowsize=0.9, arrowstyle='->'),
        aspect=True,
        Branch=dict(
            contourf=dict(
                init=dict(args=(X, Y, grid_data), levels=np.linspace(0, 30, 50), extend="both", cmap=dict(
                            init=dict(
                                name='chaos',
                                colors=['black', 'purple', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red'], N=100),
                            under='k', over='r'),
                    ),
                cbar=dict(
                    init=dict(shrink=0.8, ticks=np.linspace(0, 30, 11), orientation='horizontal'),
                    ax=dict(title=dict(args='Value Range', c='k'), xlabel='Value', ylabel='',)
                )
            ),
            patches=dict(
                wedge=(
                    dict(center=(0, 0), r=1, theta1=90, theta2=270, color='k',),
                    dict(center=(0, 0), r=1, theta1=-90, theta2=90, edgecolor='k', facecolor='w'),
                )
            ),
        )
    )

def create_sine_config():
    """
    创建正弦函数图配置
    
    返回:
        dict: 正弦图配置
    """
    x_sin = np.linspace(-np.pi, np.pi, 100)
    y_sin = np.sin(x_sin)
    return dict(
        title=dict(args="Sine Function", loc='center'),
        xlabel=dict(args="x", c='k'),
        ylabel=dict(args=r'$\sin(x)$', c='k'),
        plot=dict(args=(x_sin, y_sin), label=r'$y = \sin(x)$', c='r', lw=2),
        grid=dict(linestyle=':', color='gray'),
        legend=dict(loc='upper right'),
    ) 