"""
对 axes 进行相应的设置
"""
from .AbstractCls import ModuleSetter
from .utils import xy_call
from .Adapter import XyPlotAdapter
import matplotlib.pyplot as plt
from .SetAxis import SetAxis
from .DrawContourf import ContourfDirector

__author__ = 'Rookie'
__all__ = ['SetFigure',     # 设置画布
           'SetAxes',       # 设置子区域绘图对象
           'SetPatches'     # 设置添加几何图形
           ]


class SetFigure(ModuleSetter):
    """
    功能: 用于对 matplotlib 的 figure 进行设置操作
    """
    @xy_call()
    def native_api(self, figure: plt.Figure, **kwargs):
        """
        通过画布对象figure的方法来对画布进行修改
        Parameters
        ----------
        figure: 画布对象plt.Figure
        kwargs: 相应的设置项, 具体包括:
            height: 设置画布高度, 对应的方法接口对象为fig.set_figheight
            width: 设置画布宽度, 对应的方法接口对象为fig.set_figwidth
            edgecolor: 设置画布边框颜色, 对应的方法接口对象为fig.set_edgecolor
            frameon: 设置是否显示边框, 对应的方法接口对象为fig.set_frameon
            facecolor: 设置是否显示边框, 对应的方法接口对象为fig.set_facecolor
            frameon: 设置画布背景色, 对应的方法接口对象为fig.set_frameon
            dpi: 设置画布的分辨率, 对应的方法接口对象为fig.set_dpi
            alpha: 画布透明度, 对应的方法接口对象为fig.set_alpha
            legend: 添加画布图例, 对应的方法接口对象为fig.legend
            title: 添加画布标题, 对应的方法接口对象为fig.suptitle

        Returns
        -------

        """
        return dict(
            height=figure.set_figheight,    # 设置画布高度
            width=figure.set_figwidth,  # 设置画布宽度
            edgecolor=figure.set_edgecolor,    # 设置画布边框色
            frameon=figure.set_frameon,     # 设置是否显示边框
            facecolor=figure.set_facecolor,    # 设置画布背景色
            dpi=figure.set_dpi,  # 设置画布的分辨率
            alpha=figure.set_alpha,  # 设置图像的透明度

            legend=figure.legend,   # 添加画布图例
            title=figure.suptitle,  # 设置图像的主标题
            subplots_adjust=figure.subplots_adjust,     # 调整子图之间的间距和边缘
        )

    @xy_call(XyPlotAdapter)
    def branch_api(self, figure: plt.Figure, **kwargs):
        return dict()


class SetAxes(ModuleSetter):
    """
    设置修改axes绘图对象
    Parameters
    ----------
    axes: `matplotlib.Axes
    kwargs:
        contourf:
            API: `matplotlib.Axes.contourf
            功能: 绘制等高线填充图
        streamplot:
            API: `matplotlib.Axes.streamplot
            功能: 绘制流线
        plot:
            API: `matplotlib.Axes.plot
            功能: 绘制折线
        scatter:
            API: `matplotlib.Axes.scatter
            功能: 绘制散点
        fill:
            API: `matplotlib.Axes.fill
            功能: 绘制散点
        title:
            API: `matplotlib.Axes.set_title
            功能: 添加图形内容的标题
        xlabel:
            API: `matplotlib.Axes.set_xlabel
            功能: 设置x轴标签
        ylabel:
            API: `matplotlib.Axes.set_ylabel
            功能: 设置y轴标签
        xlim:
            API: `matplotlib.Axes.set_xlim
            功能: 设置x轴数值显示范围
        ylim:
            API: `matplotlib.Axes.set_xlim
            功能: 设置y轴数值显示范围
        xticks:
            API: `matplotlib.Axes.set_xticks
            功能: 设置x轴上的刻度位置
        yticks:
            API: `matplotlib.Axes.set_xticks
            功能: 设置y轴上的刻度位置
        xticklabels:
            API: `matplotlib.Axes.set_xticklabels
            功能: 设置x轴上的刻度标签文本
        yticklabels:
            API: `matplotlib.Axes.set_yticklabels
            功能: 设置y轴上的刻度标签文本
        legend:
            API: `matplotlib.Axes.legend
            功能: 设置标示不同图形的文本标签图例
        text:
            API: `matplotlib.Axes.text
            功能: 添加图形内容细节的无指向型注释文本
        annotate:
            API: `matplotlib.Axes.annotate
            功能: 添加图形内容细节的指向型注释文本
        grid:
            API: `matplotlib.Axes.grid
            功能: 绘制刻度线的网格线
        axhspan:
            API: `matplotlib.Axes.axhspan
            功能: 绘制平行于x轴的参考区域
        axvspan:
            API: `matplotlib.Axes.axvspan
            功能: 绘制垂直于x轴的参考区域
        axhline:
            API: `matplotlib.Axes.axhline
            功能: 绘制平行于x轴的水平参考线
        axvline:
            API: `matplotlib.Axes.axvline
            功能: 绘制垂直于x轴的竖直参考线
        axvline:
            API: `matplotlib.Axes.axvline
            功能: 绘制垂直于x轴的竖直参考线
        axvline:
            API: `matplotlib.Axes.axvline
            功能: 绘制垂直于x轴的竖直参考线
        aspect:
            API: `matplotlib.Axes.set_aspect
            功能: 设置子区域的横纵比
        tick_params:
            API: `matplotlib.Axes.tick_params
            功能: 设置刻度标签、刻度线、网格线等
    Returns
    -------

    """

    @xy_call()
    def native_api(self, axes, **kwargs):
        return dict(
            contourf=axes.contourf,  # 绘制等高线填充图
            streamplot=axes.streamplot,    # 绘制流线
            plot=axes.plot,  # 绘制折线
            scatter=axes.scatter,  # 绘制散点
            fill=axes.fill,

            title=axes.set_title,  # 添加图形内容的标题
            xlabel=axes.set_xlabel,    # 设置x轴标签文本
            ylabel=axes.set_ylabel,    # 设置y轴标签文本
            xlim=axes.set_xlim,    # 设置x轴数值显示范围
            ylim=axes.set_ylim,    # 设置y轴数值显示范围
            xticks=axes.set_xticks,     # 设置x轴上的刻度位置
            yticks=axes.set_yticks,     # 设置y轴上的刻度位置
            xticklabels=axes.set_xticklabels,   # 设置x轴上的刻度标签文本
            yticklabels=axes.set_yticklabels,   # 设置y轴上的刻度标签文本
            legend=axes.legend,    # 设置标示不同图形的文本标签图例
            text=axes.text,    # 添加图形内容细节的无指向型注释文本
            annotate=axes.annotate,    # 添加图形内容细节的指向型注释文本
            grid=axes.grid,    # 绘制刻度线的网格线
            axhspan=axes.axhspan,  # 绘制平行于x轴的参考区域
            axvspan=axes.axvspan,  # 绘制垂直于x轴的参考区域
            axhline=axes.axhline,  # 绘制平行于x轴的水平参考线
            axvline=axes.axvline,  # 绘制垂直于x轴的竖直参考线
            aspect=axes.set_aspect,    # 设置子区域的横纵比
            tick_params=axes.tick_params,   # 设置刻度标签、刻度线、网格线等
        )

    @xy_call(XyPlotAdapter)
    def branch_api(self, axes, **kwargs):
        return dict(
            contourf=(ContourfDirector, axes),  # 绘制带色卡的填色图
            patches=(SetPatches, axes),     # 绘制几何图形
            axis=(SetAxis, axes)    # 设置坐标轴: 包括轴脊、刻度线、刻度标签等
        )


class SetPatches(ModuleSetter):

    @xy_call(XyPlotAdapter)
    def native_api(self, axes, **kwargs):
        """

        Parameters
        ----------
        axes: plt.Axes 对象
        kwargs:
            circle: 绘制圆, 对应的方法接口对象为matplotlib.patches.Circle
            ellipse: 绘制椭圆, 对应的方法接口对象为matplotlib.patches.Ellipse
            rectangle: 绘制矩形, 对应的方法接口对象为matplotlib.patches.Rectangle
            arc: 绘制圆弧, 对应的方法接口对象为matplotlib.patches.Arc
            wedge: 绘制楔形, 对应的方法接口对象为matplotlib.patches.Wedge
        Returns
        -------

        """
        return dict(
            circle=(self.draw_circle, axes),    # 绘制圆
            ellipse=(self.draw_ellipse, axes),  # 绘制椭圆
            rectangle=(self.draw_rectangle, axes),  # 绘制矩形
            arc=(self.draw_arc, axes),  # 绘制圆弧
            wedge=(self.draw_wedge, axes),  # 绘制楔形
        )

    def branch_api(self, module, **kwargs): ...

    @staticmethod
    def draw_circle(axes, **kwargs):
        """绘制圆形"""
        from matplotlib.patches import Circle
        axes.add_patch(Circle(**kwargs))

    @staticmethod
    def draw_ellipse(axes, **kwargs):
        """绘制椭圆"""
        from matplotlib.patches import Ellipse
        axes.add_patch(Ellipse(**kwargs))

    @staticmethod
    def draw_rectangle(axes, **kwargs):
        """绘制矩形"""
        from matplotlib.patches import Rectangle
        axes.add_patch(Rectangle(**kwargs))

    @staticmethod
    def draw_arc(axes, **kwargs):
        """绘制圆弧"""
        from matplotlib.patches import Arc
        axes.add_patch(Arc(**kwargs))

    @staticmethod
    def draw_wedge(axes, **kwargs):
        """绘制楔形"""
        from matplotlib.patches import Wedge
        axes.add_patch(Wedge(**kwargs))
