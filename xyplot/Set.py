"""
对 axes 进行相应的设置
"""
from .AbstractCls import AbstractDrawCls, AbstractSetCls
from .utils import xy_call
import matplotlib.pyplot as plt
from .Adapter import DrawAdapter
from .SetAxis import SetAxis
from .DrawContourf import DrawContourf


class SetFigure(AbstractSetCls):
    """
    功能: 用于对 matplotlib 的 figure 进行设置操作
    """
    @xy_call()
    def native_api(self, figure: plt.Figure, **kwargs):
        """

        :param figure:
        :param kwargs:
        :return:
        """
        return dict(
            height=figure.set_figheight,    # 设置画布高度
            width=figure.set_figwidth,  # 设置画布宽度
            edgecolor=figure.set_edgecolor,    # 设置画布边框色
            frameon=figure.set_frameon,     # 设置是否显示边框
            facecolor=figure.set_facecolor,    # 设置画布背景色
            dpi=figure.set_dpi,  # 设置画布的分辨率
            alpha=figure.set_alpha,  # 画布透明度

            legend=figure.legend,   # 添加画布图例

        )

    @xy_call(DrawAdapter)
    def branch_api(self, figure: plt.Figure, **kwargs):
        """

        :param figure:
        :param kwargs:
        :return:
        """
        return dict(

        )


class SetAxes(AbstractSetCls):
    """
    # 对 matplotlib 中 axes 子区域中的基本组成元素进行设置
    # :param axes:  plt.Axes object
    # :param title: 添加图形内容的标题 -> axes.set_title
    # :param xlabel: 设置x轴标签文本 -> axes.set_xlabel
    # :param ylabel: 设置y轴标签文本 -> axes.set_ylabel
    # :param xlim: 设置x轴数值显示范围 -> axes.set_xlim
    # :param ylim: 设置y轴数值显示范围 -> axes.set_ylim
    # :param legend: 设置标示不同图形的文本标签图例 -> axes.legend
    # :param text: 添加图形内容细节的无指向型注释文本 -> axes.text
    # :param annotate: 添加图形内容细节的指向型注释文本 -> axes.annotate
    # :param grid: 绘制刻度线的网格线 -> axes.grid
    # :param axhspan: 绘制平行于x轴的参考区域 -> axes.axhspan
    # :param axvspan: 绘制垂直于x轴的参考区域 -> axes.axvspan
    # :param axhline: 绘制平行于x轴的水平参考线 -> axes.axhline
    # :param axvline: 绘制垂直于x轴的竖直参考线 -> axes.axvline
    """

    @xy_call()
    def native_api(self, axes, **kwargs):
        """
        将配置信息分配给Axes实例化对象中的对应方法进行设置
        """
        return dict(
            contourf=axes.contourf,  # 绘制等高线填充图
            streamplot=axes.streamplot,    # 绘制流线
            plot=axes.plot,  # 绘制折线
            scatter=axes.scatter,  # 绘制散点

            title=axes.set_title,  # 添加图形内容的标题
            xlabel=axes.set_xlabel,    # 设置x轴标签文本
            ylabel=axes.set_ylabel,    # 设置y轴标签文本
            xlim=axes.set_xlim,    # 设置x轴数值显示范围
            ylim=axes.set_ylim,    # 设置y轴数值显示范围
            legend=axes.legend,    # 设置标示不同图形的文本标签图例
            text=axes.text,    # 添加图形内容细节的无指向型注释文本
            annotate=axes.annotate,    # 添加图形内容细节的指向型注释文本
            grid=axes.grid,    # 绘制刻度线的网格线
            axhspan=axes.axhspan,  # 绘制平行于x轴的参考区域
            axvspan=axes.axvspan,  # 绘制垂直于x轴的参考区域
            axhline=axes.axhline,  # 绘制平行于x轴的水平参考线
            axvline=axes.axvline,  # 绘制垂直于x轴的竖直参考线
            set_aspect=axes.set_aspect,    # 设置子区域的横纵比
        )

    @xy_call(DrawAdapter)
    def branch_api(self, axes, **kwargs):
        """
        组合接口
        :param axes:
        :param kwargs:
        :return:
        """
        return dict(
            contourf=(DrawContourf, axes),
            patches=(DrawPatches, axes),
            axis=(SetAxis, axes)

        )


class DrawPatches(AbstractDrawCls):
    """

    """
    def __init__(self, axes, **kwargs):
        """

        :param axes:
        :param kwargs:
        """
        self._axes = axes
        self._draw(axes, **kwargs)

    @xy_call(DrawAdapter)
    def _draw(self, axes, **kwargs):
        return dict(
            circle=(self.draw_circle, axes),
            ellipse=(self.draw_ellipse, axes),
            rectangle=(self.draw_rectangle, axes),
            arc=(self.draw_arc, axes),
            wedge=(self.draw_wedge, axes)
        )

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
