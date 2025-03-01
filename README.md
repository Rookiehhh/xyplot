# xyplot

## 项目简介

xyplot 是一个针对气象行业设计的 Python 绘图封装库，基于 Matplotlib 构建。它提供了简洁的 API 和灵活的配置选项，帮助用户高效地创建专业级别的气象数据可视化图表。

## 主要特性

- **简化绘图流程**：大幅减少绘图代码量，提高开发效率
- **配置化设计**：支持通过外部配置文件进行个性化定制
- **组件化架构**：便于代码复用和维护
- **丰富的图表类型**：支持等高线填充图、流线图、散点图、折线图等气象常用图表
- **灵活的布局系统**：支持多种子图布局方式（subplot、subplot2grid、add_axes）
- **精细化控制**：提供对坐标轴、色阶、图例等元素的详细设置

## 安装方法

```bash
pip install xyplot
```

## 基本用法

### 单个图表示例

```python
import numpy as np
from xyplot import XyPlot

# 准备数据
x = np.linspace(-np.pi, np.pi, 100)
y = np.sin(x)

# 配置字典
set_fig_dict = dict(height=10, width=10)
axes_dict = dict(
    plot=dict(args=(x, y), label='y=sin(x)', c='k'),
    title=r'y=sin(x)'
)
set_rc_dict = {
    'figure.facecolor': 'k',
    'axes.labelcolor': 'w',
    'axes.titlecolor': 'w',
    'ytick.color': 'w',
    'xtick.color': 'w'
}

# 创建并显示图表
cfg = dict(set_rc=set_rc_dict, set_fig=set_fig_dict, axes=axes_dict)
xyplt = XyPlot(**cfg)
xyplt.show()
```

### 多子图示例

```python
import numpy as np
from xyplot import XyPlot

# 准备数据
x = np.linspace(-np.pi, np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# 配置子图
ax1_dict = dict(plot=dict(args=(x, y1), color='r', lw=2), title='y1= sin(x)')
ax2_dict = dict(scatter=dict(args=(x, y2), color='r', lw=2), title='y2= cos(x)')
subplot_dict = dict(
    init=(121, 122),
    axes=(ax1_dict, ax2_dict)
)

# 创建并保存图表
XyPlot(subplot=subplot_dict).save('test.png')
```

### 等高线填充图示例

```python
import numpy as np
from xyplot import XyPlot

# 准备数据
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) + np.cos(Y)

# 配置等高线填充图
axes_dict = dict(
    contourf=dict(
        init=dict(args=(X, Y, Z), levels=15, cmap='jet'),
        cbar=dict(init=dict(label='数值'))
    ),
    title='等高线填充图示例'
)

# 创建并显示图表
XyPlot(axes=axes_dict).show()
```

## 主要组件

- **XyPlot**：顶层绘图对象，用于控制整体绘图流程
- **ModuleSetter**：模块设置模板方法抽象类
- **AxesBuilder**：用于构建和配置 Matplotlib Axes 对象
- **ContourfDirector**：等高线填充图绘制对象
- **ColorMapBuilder**：色阶颜色映射构建设置类
- **SetFigure**：画布设置类
- **SetAxes**：子区域绘图对象设置类
- **SetPatches**：几何图形设置类

## 设计理念

xyplot 采用面向对象的设计思路，结合了多种设计模式（建造者模式、适配器模式、模板方法模式等），使代码结构清晰、易于扩展。其目标是：

1. 简化绘图方法，降低绘图代码量
2. 便于绘图代码的封装分类，提高其复用性和维护性
3. 支持通过外部配置文件对可视化产品进行个性化定制
4. 为未来的绘图 GUI/Web 配置化打下基础

## 贡献

欢迎通过 Issue 和 Pull Request 的方式为项目做出贡献。请确保您的代码符合项目的编码风格，并提供相应的测试和文档。

## 许可

本项目采用 MIT 许可证。详情请查看项目中的 LICENSE 文件。
