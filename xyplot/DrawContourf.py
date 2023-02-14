from .AbstractCls import AbstractSetCls, AbstractDrawCls
from .utils import method_call, xy_call


class DrawContourf(AbstractDrawCls):
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
        if 'contourf' in kwargs:
            # 取出颜色映射配置并进行设置
            if 'cmap' in kwargs['contourf']:
                kwargs['contourf']['cmap'] = BuildColorMap(kwargs['contourf']['cmap'])()
            cset = method_call(axes.contourf, kwargs['contourf'])
            if 'cbar' in kwargs:
                kwargs['cbar'] = dict(mappable=cset, **kwargs['cbar'])
                DrawColorBar(axes, **kwargs['cbar'])


class BuildColorMap:
    """
    建造颜色映射
    """
    def __init__(self, parameter):
        self._cmap = parameter
        self._set()

    def __call__(self, *args, **kwargs):
        return self._cmap

    def _set(self, **kwargs): ...

    def native_api(self, module, **kwargs): ...

    def branch_api(self, module, **kwargs): ...


class DrawColorBar(AbstractDrawCls):

    def __init__(self, axes, **kwargs):
        self._axes = axes
        self._draw(axes, **kwargs)

    def _draw(self, axes, **kwargs):
        cbar_ax_dict = None if 'ax' not in kwargs else kwargs.pop('ax')
        self.cbar = method_call(axes.figure.colorbar, kwargs)
        if cbar_ax_dict is not None:
            self._set_cbar_ax(cbar_ax_dict)

    def _set_cbar_ax(self, cbar_ax_dict):
        from .Set import SetAxes
        SetAxes(self.cbar.ax, **cbar_ax_dict)