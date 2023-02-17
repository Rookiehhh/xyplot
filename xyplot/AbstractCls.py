from abc import ABCMeta, abstractmethod
from .cfg_names import BRANCH_NAME, INIT_NAME
from .utils import method_call

__author__ = 'Rookie'
__all__ = [
    'ModuleSetter',     # 模块设置模板方法抽象类
    'AbstractDrawCls'
]


class ModuleSetter(metaclass=ABCMeta):
    def __init__(self, module, **kwargs):
        self.module = module
        if len(kwargs):
            self.auto_set(module, **kwargs)

    def auto_set(self, module, **kwargs):
        # 如果存在INIT_NAME, 代表此模块的调度的实际是传入模块被初始化后返回的模块对象
        init = None if INIT_NAME not in kwargs else kwargs.pop(INIT_NAME)
        if init is not None:
            module = method_call(module, init)
        # 分支, 一般用于自定义组合设置
        branch = None if BRANCH_NAME not in kwargs else kwargs.pop(BRANCH_NAME)
        if branch is not None:
            self.branch_api(module, **branch)
        self.native_api(module, **kwargs)

    @abstractmethod
    def native_api(self, module, **kwargs): ...
    @abstractmethod
    def branch_api(self, module, **kwargs): ...


class AbstractDrawCls(metaclass=ABCMeta):
    @abstractmethod
    def _draw(self, module, **kwargs): ...



