from .AbstractCls import AbstractDrawCls, ModuleSetter
from .utils import method_call, xy_call
from .Adapter import XyPlotAdapter
from .cfg_names import INIT_NAME

__author__ = 'Rookie'
__all__ = [
    'ContourfDirector',     # 绘制contourf等高线填色图(该模块的顶层设置者)
    'ColorMapBuilder',      # 色阶颜色映射 colormap 构建设置类
    'DrawColorBar',         # 色卡构建设置类对象
]


class ContourfDirector(AbstractDrawCls):
    """
    绘制等高线填充图
    """
    def __init__(self, axes, **kwargs):
        """
        :param axes: plt.Axes
        """
        self.axes = axes
        self._draw(axes, **kwargs)

    @staticmethod
    def _draw(axes, **kwargs):
        """

        :param axes:
        :param kwargs:
        :return:
        """
        # 进行绘制
        if INIT_NAME in kwargs:
            # 取出颜色映射配置并进行设置
            if 'cmap' in kwargs[INIT_NAME]:
                kwargs[INIT_NAME]['cmap'] = ColorMapBuilder(kwargs[INIT_NAME]['cmap'])()
            cset = method_call(axes.contourf, kwargs[INIT_NAME])
            if 'cbar' in kwargs:
                if isinstance(kwargs['cbar'], dict):
                    kwargs['cbar'][INIT_NAME] = dict(mappable=cset, **kwargs['cbar'][INIT_NAME], ax=axes)
                    DrawColorBar(axes.figure.colorbar, **kwargs['cbar'])


class ColorMapBuilder:
    """
    建造颜色映射
    """
    def __init__(self, parameter):
        # 默认色卡映射为jet
        self.colormap = "jet"
        # 当传入cmap设置信息为str时
        if isinstance(parameter, str):
            self.colormap = parameter
        # 当传入cmap设置信息为字典时, 如下
        elif isinstance(parameter, dict):
            if INIT_NAME not in parameter and not isinstance(parameter[INIT_NAME], dict):
                raise Exception(
                    f"{INIT_NAME!r} must exist and is of dict type"
                )
            else:
                init = parameter.pop(INIT_NAME)
                self.colormap = self.create_colormap(**init)
                self.native_api(self.colormap, **parameter)
        else:
            raise TypeError()

    def __call__(self, *args, **kwargs):
        return self.colormap

    @staticmethod
    def create_colormap(**kwargs):
        method = 'linear' if 'method' not in kwargs else kwargs['method']
        if method == 'linear':
            from matplotlib.colors import LinearSegmentedColormap
            return method_call(LinearSegmentedColormap.from_list, kwargs)

    @xy_call()
    def native_api(self, colormap, **kwargs):
        return dict(
            set_under=colormap.set_under,   # 低于色阶时的映射颜色
            set_over=colormap.set_over,     # 高于色阶时的映射颜色
        )


class DrawColorBar(ModuleSetter):
    """设置色卡"""

    @xy_call(XyPlotAdapter)
    def native_api(self, c_bar, **kwargs):
        from .Set import SetAxes
        return dict(
            ax=(SetAxes, c_bar.ax),
        )

    def branch_api(self, module, **kwargs): ...
