
class DrawAdapter:
    """
    绘图对象适配器
    """
    def __init__(self, *args, **kwargs):
        adapt_obj, module = args[:2]
        adapt_obj(module, **kwargs)
