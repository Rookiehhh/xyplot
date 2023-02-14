from .AbstractCls import AbstractSetCls
from .utils import xy_call
from .Adapter import DrawAdapter


class SetAxis(AbstractSetCls):
    """

    """
    @xy_call()
    def branch_api(self, axes, **kwargs): ...

    @xy_call(DrawAdapter)
    def native_api(self, axes, **kwargs):
        """"""
        return dict(
            spines=(SetSpines, axes.spines),
            xaxis=(SetXyAxis, axes.xaxis),
            yaxis=(SetXyAxis, axes.yaxis),
        )


class SetSpines(AbstractSetCls):

    @xy_call(DrawAdapter)
    def native_api(self, spines, **kwargs):
        return dict(
            top=(self.set_spines, spines['top']),
            bottom=(self.set_spines, spines['bottom']),
            right=(self.set_spines, spines['right']),
            left=(self.set_spines, spines['left']),
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


class SetXyAxis(AbstractSetCls):

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
