"""
设计思路:
    1. 指挥者 Director
    2.
"""
import copy
from abc import ABCMeta, abstractmethod
from typing import Optional

import matplotlib.pyplot as plt

from .utils import method_call, XyPlotAdapter
from .Set import SetFigure, SetAxes
from .cfg_names import SET_RC_NAME, AXES_NAME, SUBPLOT_NAME, SUBPLOT2GRID_NAME, SET_FIG_NAME, ADD_AXES_NAME, INIT_NAME


class XyPlotDirector:
    """指挥者"""

    def __init__(self, **kwargs):
        self.figure = None
        if len(kwargs):
            self.execute(**kwargs)

    def execute(self, **kwargs):
        # 如果存在对matplotlib设置信息的修改
        if SET_RC_NAME in kwargs:
            pass
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
        if SET_FIG_NAME in kwargs:
            SetFigure(self.figure, **kwargs[SET_FIG_NAME])

    def show(self):
        plt.show()

    def save(self, *args, **kwargs):
        plt.savefig(*args, **kwargs)


class AxesBuilder(metaclass=ABCMeta):
    """
    Axes 建造者
    """

    def __init__(self, figure: Optional[plt.Figure] = None, **kwargs):
        """
        根据kwargs构建画布
        """
        if figure is None:
            self.figure = plt.figure()
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
                f"The number of created axes ({len(ax_lst)})"
                f" is inconsistent with the number of corresponding set information list ({len(set_lst)})"
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

