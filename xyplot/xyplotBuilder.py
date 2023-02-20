import copy
from abc import ABCMeta, abstractmethod
from typing import Optional

import matplotlib as mpl
import matplotlib.pyplot as plt

from .utils import method_call
from .Adapter import XyPlotAdapter
from .Set import SetFigure, SetAxes
from .cfg_names import SET_RC_NAME, AXES_NAME, SUBPLOT_NAME, SUBPLOT2GRID_NAME, SET_FIG_NAME, ADD_AXES_NAME, INIT_NAME

__author__ = 'Rookie'
__all__ = [
    'XyPlotDirector',   # 顶层绘图方法
    'AxesBuilder',      # axes 子区域对象的创建绘制 模板抽象类
    'SubplotBuilder',   # 使用subplot创建绘制axes子区域类
    'Subplot2gridBuilder',  # 使用subplot2grid创建绘制axes子区域类
    'AddAxesBuilder',    # 使用add_axes 创建绘制axes子区域类
    'SetTempRc',        # 设置临时全局mpl.rcParams
]


class XyPlotDirector:
    """
    蜥蜴绘图(Xi Yi Plot)
        针对气象行业主要的绘图场景, 专门设计的绘图封装库。 其研发的主要目的包括：
            1. 简化绘图方法, 降低绘图代码量
            2. 便于绘图代码的封装分类, 提高其复用性和维护性
            3. 更好地支持通过外部配置文件对单独的可视化产品进行个性化定制
            4. 为未来的绘图GUI/Web配置化打下基础, 以实现未来可视化工作的无代码化
        其中, 'xy' 既可以理解为其绘制的图形主要是二维笛卡尔坐标的, 也可以理解为它是由云蜥数字科技研发
    Parameters
    ----------
    kwargs:
        set_rc:
            dict类型, 修改mpl.rcParams, 会在绘图对象绘图完成后恢复到原本的设置
        set_fig:
            dict类型, 设置画布信息
        axes:
            dict类型,子区域axes对象绘图信息
        subplot:
            dict类型, 使用subplot创建axes对象并绘图, 内部包含两个键分别为 init and axes.
            init 用于初始化subplot创建axes对象, axes 包含绘图对象的绘图信息, 具体使用方法
            和顶层axes一致
        subplot2grid:
            dict类型， 使用subplot2grid创建axes对象并绘图, 具体使用方法与subplot同理
        add_axes:
            dict类型， 使用add_axes创建axes对象并绘图, 具体使用方法与subplot同理
    -------
    Example
        1. 绘制单个axes对象
            >>> import numpy as np
            >>> x = np.linspace(-np.pi, np.pi, 100)
            >>> y = np.sin(x)
            >>> set_fig_dict = dict(height=10,width=10)
            >>> axes_dict = dict(plot=dict(args=(x, y), label='y=sin(x)', c='k'), title=r'y=sin(x)')
            >>> set_rc_dict = {'figure.facecolor': 'k', 'axes.labelcolor': 'w',
            >>> 'axes.titlecolor': 'w', 'ytick.color': 'w', 'xtick.color': 'w'}
            >>> cfg = dict(set_rc=set_rc_dict, set_fig=set_fig_dict, axes=axes_dict)
            >>> xyplt = XyPlotDirector(**cfg)
            >>> xyplt.show()
        2. 绘制多个axes对象
            >>> import numpy as np
            >>> x = np.linspace(-np.pi, np.pi, 100)
            >>> y1 = np.sin(x)
            >>> y2 = np.cos(x)
            >>> ax1_dict = dict(plot=dict(args=(x, y1), color='r', lw=2), title='y1= sin(x)')
            >>> ax2_dict = dict(scatter=dict(args=(x, y2), color='r', lw=2), title='y2= cos(x)')
            >>> subplot_dict = dict(
            >>>                 init=(121, 122),
            >>>                 axes=(ax1_dict, ax2_dict)
            >>>                )
            >>> XyPlotDirector(subplot=subplot_dict).save('test.png')

    -------
    Returns
    -------

    """

    def __init__(self, **kwargs):
        kwargs = copy.deepcopy(kwargs)  # 由于执行该class时会修改kwargs内容, 所以要对其进行深拷贝
        self.figure = None
        if len(kwargs):
            self.execute(**kwargs)

    def execute(self, **kwargs):
        # 修改mpl.rcParams
        tmp_rc = None
        if SET_RC_NAME in kwargs:
            tmp_rc = SetTempRc(**kwargs[SET_RC_NAME])
        # 如果kwargs键中存在AXES_NAME, 则调度subplot方法构建axes子区域集
        if AXES_NAME in kwargs:
            self.figure = SubplotBuilder(self.figure, **kwargs[AXES_NAME])()
        # 如果kwargs键中存在SUBPLOT_NAME, 则调度subplot方法构建axes子区域集
        if SUBPLOT_NAME in kwargs:
            self.figure = SubplotBuilder(self.figure, **kwargs[SUBPLOT_NAME])()
        # 如果kwargs键中存在SUBPLOT2GRID_NAME, 则调度subplot2grid 方法构建axes子区域集
        if SUBPLOT2GRID_NAME in kwargs:
            self.figure = Subplot2gridBuilder(self.figure, **kwargs[SUBPLOT2GRID_NAME])()
        # 如果kwargs键中存在ADD_AXES_NAME, 则调度fig.ADD_AXES_NAME 方法构建 axes 子区域集
        if ADD_AXES_NAME in kwargs:
            self.figure = AddAxesBuilder(self.figure, **kwargs[ADD_AXES_NAME])()
        # 如果kwargs键中存在SET_FIG_NAME, 则调度SetFigure 方法构建
        self.check()    # 在设置画布前先进行检查figure对象是否已经创建
        if SET_FIG_NAME in kwargs:
            SetFigure(self.figure, **kwargs[SET_FIG_NAME])
        # 还原原有的mpl.rcParams
        if SET_RC_NAME in kwargs:
            tmp_rc.revert()

    @staticmethod
    def show():
        """显示画布"""
        plt.show()

    @staticmethod
    def save(*args, **kwargs):
        """保存画布"""
        plt.savefig(*args, **kwargs)

    def check(self):
        """检查"""
        if self.figure is None:
            raise TypeError(
                f"Figure is not created, You need to create at least one axes object to create a canvas"
            )


class AxesBuilder(metaclass=ABCMeta):
    """
    Axes 建造者
    """

    def __init__(self, figure: Optional[plt.Figure] = None, **kwargs):
        """
        根据kwargs构建画布
        """
        self.figure = figure if figure is not None else plt.figure()
        self.execute(**kwargs)

    def execute(self, **kwargs):
        # 解析axes初始化设置信息
        init_lst = []
        if INIT_NAME not in kwargs:
            init_lst.append(dict())
        elif isinstance(kwargs[INIT_NAME], (tuple, list)):
            init_lst.extend(kwargs[INIT_NAME])
        elif isinstance(kwargs[INIT_NAME], dict):
            init_lst.append(kwargs[INIT_NAME])
        else:
            raise TypeError(
                f"Optional types of {INIT_NAME!r} include tuple、list、dict"
            )
        # 根据初始化设置信息调度构建方法, 创建 axes 对象 列表
        ax_lst = self.create_axes(self.figure, init_lst)
        # ax_lst = method_call(XyPlotAdapter, init_lst, self.create_axes, self.figure)
        if not isinstance(ax_lst, list):
            raise TypeError(
                f"Method AxesBuilder.create_axes The return type must be list"
            )
        # 解析 axes 设置/绘制 配置信息
        set_lst = []
        if AXES_NAME not in kwargs:
            if INIT_NAME not in kwargs:
                set_lst.append(kwargs)
            else:
                raise
        elif isinstance(kwargs[AXES_NAME], (tuple, list)):
            set_lst.extend(kwargs[AXES_NAME])
        elif isinstance(kwargs[AXES_NAME], dict):
            set_lst.append(kwargs[AXES_NAME])
        else:
            raise TypeError(
                f"Optional types of {AXES_NAME!r} include tuple、list、dict"
            )
        # 调度 set_axes 方法, 对画布中的各个子区域进行绘图设置
        if len(ax_lst) == len(set_lst):
            self.set_axes(ax_lst, set_lst)
        else:
            raise Exception(
                f"The number of created axes (number = {len(ax_lst)})"
                f" is inconsistent with the number of corresponding set information list ( number = {len(set_lst)})"
            )

    def __call__(self, *args, **kwargs):
        return self.figure

    @staticmethod
    def set_axes(ax_lst, cfg_lst):
        """
        调度设置axes
        """
        for ax, cfg in zip(ax_lst, cfg_lst):
            method_call(XyPlotAdapter, copy.deepcopy(cfg), SetAxes, ax)

    @abstractmethod
    def create_axes(self, figure: plt.figure, init_lst: list) -> list:
        ...


class SubplotBuilder(AxesBuilder):
    """
    使用subplot构建axes
    """
    def create_axes(self, figure: plt.figure, init_lst: list) -> list:
        ax_lst = []
        for init_cfg in init_lst:
            ax = method_call(plt.subplot, init_cfg)
            ax_lst.append(ax)
        return ax_lst


class Subplot2gridBuilder(AxesBuilder):
    """
    使用subplot2grid 构建 axes
    """
    def create_axes(self, figure: Optional[plt.figure], init_lst: list) -> list:
        ax_lst = []
        for init_cfg in init_lst:
            ax = method_call(plt.subplot2grid, init_cfg)
            ax_lst.append(ax)
        return ax_lst


class AddAxesBuilder(AxesBuilder):
    """
    使用add_axes 构建 axes
    """
    def create_axes(self, figure: plt.figure, init_lst: list) -> list:
        ax_lst = []
        for init_cfg in init_lst:
            ax = method_call(figure.add_axes, init_cfg)
            ax_lst.append(ax)
        return ax_lst


class SetTempRc:
    """
    修改mpl.rcParams
    """
    def __init__(self, **kwargs):
        self.Raw_Rc = copy.copy(mpl.rcParams)
        self.execute(**kwargs)

    @staticmethod
    def execute(**kwargs):
        """执行修改"""
        for k, v in kwargs.items():
            mpl.rcParams[k] = v

    def revert(self):
        """恢复原有设置"""
        for k, v in self.Raw_Rc.items():
            mpl.rcParams[k] = v
