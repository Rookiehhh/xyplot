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
        return dict(
            set_visible=module.set_visible,     # 设置是否显示脊线
            set_position=module.set_position,   # 移动轴脊
            set_color=module.set_color,     # 设置脊线的颜色
            set_linestyle=module.set_linestyle,     # 设置脊线的线条样式
        )


class SetXyAxis(ModuleSetter):

    @xy_call()
    def native_api(self, module, **kwargs):
        return dict(
            set_inverted=module.set_inverted,   # 坐标轴反转
            set_ticks_position=module.set_ticks_position,   # 设置轴刻度位置
            set_label_position=module.set_label_position,   # 设置轴标签位置
            set_label_coords=module.set_label_coords,   # 设置标签坐标
            set_label_text=module.set_label_text,   # 设置标签内容
            set_tick_params=module.set_tick_params,     # 设置刻度
        )
    
    def branch_api(self, xy_axis, **kwargs): ...
