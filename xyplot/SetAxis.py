from .AbstractCls import ModuleSetter
from .utils import xy_call
from .Adapter import XyPlotAdapter

__author__ = 'Rookie'
__all__ = [
    'SetAxis',      # axis坐标轴设置类
    'SetSpines',    # 轴脊设置类
    'SetXyAxis',    # x、y 轴刻度设置类
]


class SetAxis(ModuleSetter):
    """
    设置axes对象的坐标轴
    Parameters
    ----------
    kwargs:
        spines: dict, 轴脊设置
        xaxis: dict, x轴设置
        yaxis: dict, y轴设置
    Returns

    -------
    """
    @xy_call()
    def branch_api(self, axes, **kwargs): ...

    @xy_call(XyPlotAdapter)
    def native_api(self, axes, **kwargs):
        """"""
        return dict(
            spines=(SetSpines, axes.spines),    # 轴脊设置
            xaxis=(SetXyAxis, axes.xaxis),  # x轴设置
            yaxis=(SetXyAxis, axes.yaxis),  # y轴设置
        )


class SetSpines(ModuleSetter):
    """

    Parameters
    ----------
    spines: 轴脊设置对象： matplotlib.Axes.spines
    kwargs:
        top: dict, 顶部轴脊设置, 对应接口: `matplotlib.Axes.spines['top']
        bottom: dict, 底部轴脊设置, 对应接口: `matplotlib.Axes.spines['bottom']
        right: dict, 右侧轴脊设置, 对应接口: `matplotlib.Axes.spines['right']
        left: dict, 左侧轴脊设置, 对应接口: `matplotlib.Axes.spines['left']

    Returns
    -------

    """

    @xy_call(XyPlotAdapter)
    def native_api(self, spines, **kwargs):
        return dict(
            top=(self.set_spines, spines['top']),   # 顶部轴脊设置
            bottom=(self.set_spines, spines['bottom']),     # 底部轴脊设置
            right=(self.set_spines, spines['right']),   # 右侧轴脊设置
            left=(self.set_spines, spines['left']),     # 左侧轴脊设置
        )

    def branch_api(self, spines, **kwargs): ...

    @xy_call()
    def set_spines(self, module, **kwargs):
        """
        设置某位置的轴脊
        Parameters
        ----------
        module: `matplotlib.Axes.spines[Position] (Position = 'top'/'bottom'/'left'/'right')
        kwargs:
             visible: 设置是否显示脊线, 对应接口: matplotlib.Axes.spines[Position].set_visible
             position: 移动轴脊, 对应接口: matplotlib.Axes.spines[Position].set_position
             color: 设置脊线的颜色, 对应接口: matplotlib.Axes.spines[Position].set_color
             linestyle: 设置脊线的线条样式, 对应接口: matplotlib.Axes.spines[Position].set_linestyle

        Returns
        -------

        """
        return dict(
            visible=module.set_visible,     # 设置是否显示脊线
            position=module.set_position,   # 移动轴脊
            color=module.set_color,     # 设置脊线的颜色
            linestyle=module.set_linestyle,     # 设置脊线的线条样式
        )


class SetXyAxis(ModuleSetter):
    """
    设置 x轴 或 y轴
    Parameters
    ----------
    module: 坐标轴对象`matplotlib.Axes.xaxis or `matplotlib.Axes.yaxis
    kwargs:
        （以matplotlib.Axes.xaxis为例）
        inverted: 坐标轴反转, 对应接口: matplotlib.Axes.xaxis.set_inverted
        ticks_position: 设置轴刻度位置, 对应接口: matplotlib.Axes.xaxis.set_ticks_position
        label_position: 设置轴标签位置, 对应接口: matplotlib.Axes.xaxis.set_label_position
        label_coords: 设置标签坐标, 对应接口: matplotlib.Axes.xaxis.set_label_coords
        label_text: 设置标签内容, 对应接口: matplotlib.Axes.xaxis.set_label_text
        tick_params: 设置刻度, 对应接口: matplotlib.Axes.xaxis.set_tick_params
    Returns
    -------

    """
    @xy_call()
    def native_api(self, module, **kwargs):
        return dict(
            inverted=module.set_inverted,   # 坐标轴反转
            ticks_position=module.set_ticks_position,   # 设置轴刻度位置
            label_position=module.set_label_position,   # 设置轴标签位置
            label_coords=module.set_label_coords,   # 设置标签坐标
            label_text=module.set_label_text,   # 设置标签内容
            tick_params=module.set_tick_params,     # 设置刻度
        )
    
    def branch_api(self, xy_axis, **kwargs): ...
