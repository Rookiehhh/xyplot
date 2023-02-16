from abc import ABCMeta, abstractmethod
from .cfg_names import BRANCH_NAME


class AbstractSetCls(metaclass=ABCMeta):
    def __init__(self, module, **kwargs):
        self.module = module
        if len(kwargs):
            self.auto_set(module, **kwargs)

    def auto_set(self, module, **kwargs):
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

