from functools import wraps
from typing import Union
from .Adapter import DrawAdapter


def merge(dict_1, dict_2):
    """递归合并字典"""
    result = dict_1.copy()
    for k, v in dict_1.items():
        if isinstance(v, dict) and k in dict_2:
            assert isinstance(dict_2[k], dict), f"For key {k}, value in dict_1 is dict, but is not in dict_2."
            merged_value = merge(dict_1[k], dict_2.pop(k))
            result[k] = merged_value
        elif k in dict_2:
            result[k] = dict_2.pop(k)
        else:
            pass
    result.update(dict_2)

    return result


def xy_call(adapter=None):

    def decorator(method):
        """
        装饰器, 根据method方法返回的对象映射表, 调度执行执行对应的方法
        :param method:
        :return:
        """
        @wraps(method)
        def inner(*args, **kwargs):
            # 调用执行核心代码
            obj_map = method(*args, **kwargs)
            # 检查返回结果类型
            assert isinstance(obj_map, dict), f"{method!r} does not return a dictionary"
            # 检查传入kwargs关键字的合法性
            for k, v in kwargs.items():
                assert k in obj_map, f"For key {k!r}, No corresponding executable object, Optional key includes:\n" \
                                     f" {list(obj_map.keys())!r}"
            # 根据对象映射 obj_map, 调度执行相应的类或方法
            if adapter is None:     # 当不存在适配器时
                for key in obj_map.keys():
                    if key in kwargs:
                        method_call(obj_map[key], kwargs[key])
            elif issubclass(adapter, DrawAdapter):  # 当使用 DrawAdapter 适配器时
                for key in obj_map.keys():
                    if key in kwargs:
                        obj, axes = obj_map[key]
                        method_call(DrawAdapter, kwargs[key], obj, axes)
            else:
                raise TypeError(
                    f"{adapter!r} TypeError"
                )

        return inner
    return decorator


def method_call(obj, parameter: Union[dict, tuple, list, ], *args):
    """
    调度执行对象
    :param obj: 调度执行对象
    :param parameter: 执行参数信息
    """
    # 定义调度方法的返回值
    ret_obj = None
    call_args = list(args)
    # 当parameter是字典类型时
    if isinstance(parameter, dict):
        if 'args' in parameter.keys():
            if isinstance(parameter['args'], (list, tuple)):
                call_args.extend(parameter.pop('args'))
            else:
                call_args.append(parameter.pop('args'))
        ret_obj = obj(*call_args, **parameter)
    # 当parameter是数组时, 进行遍历调度(递归)
    elif isinstance(parameter, (list, tuple)):
        for par in parameter:
            method_call(obj, par, *args)
    # ...
    else:
        ret_obj = obj(parameter) if len(args) == 0 else obj(parameter, *args)

    return ret_obj
