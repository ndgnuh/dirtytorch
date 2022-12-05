# short_desc: @with_config decorator for convoluted model configuration
#
# Usage:
# @with_config(path='module1')
# class Module1:
#   def __init__(self, size: int):
#       ...
# @with_config(path='module2')
# class Module2:
#   def __init__(self, size: int):
#       ...
#
# config = read_config(...)
# Module1.from_config(config)
# Module2.from_config(config)
import inspect
from dataclasses import dataclass
from typing import Callable

_function_type = type(lambda x: None)


@dataclass
class Function:
    f: Callable

    def from_config(cls, config):
        pass

    def __call__(self, *a, **k):
        return self.f(*a, **k)


def walk_dict(d, path="", delim='.', max_depth=100):
    if path.strip() == "":
        return d
    parts = path.split(delim)

    n = min(len(parts), max_depth)

    def recurse(d, i):
        if i == n:
            return d
        else:
            k = parts[i]
            if k not in d:
                raise KeyError(path)  # Show full path
            return recurse(d[k], i+1)
    return recurse(d, 0)


def with_config(call=None, path=""):
    if call is None:
        return lambda call: with_config(call, path=path)

    params = inspect.signature(call).parameters

    call.init_params = dict()
    for k, p in params.items():
        call.init_params[k] = p.default

    def from_config(cls, config):
        config = walk_dict(config, path)
        inputs = dict()
        for k, default in cls.init_params.items():
            if default == inspect._empty:
                inputs[k] = config[k]
            else:
                inputs[k] = config.get(k, default)

        print(inputs)
        return cls(**inputs)

    from_config.__name__ = "from_config"
    from_config.__qualname__ = "from_config"
    from_config.__module__ = call.__module__
    setattr(call, 'from_config', classmethod(from_config))
    return call
