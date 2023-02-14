from abc import ABCMeta, abstractmethod


class AbstractSetCls(metaclass=ABCMeta):
    def __init__(self, module, **kwargs):
        self.module = module
        if len(kwargs):
            self._set(module, **kwargs)

    def _set(self, module, **kwargs):
        branch = None if 'branch' not in kwargs else kwargs.pop('branch')
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
