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
from functools import wraps


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


def get_params(call):
    params = inspect.signature(call).parameters
    params = {k: p.default for k, p in params.items()}
    return params


def with_config_class(call, path):
    params = get_params(call)

    def from_config(cls, config):
        config = walk_dict(config, path)
        inputs = dict()
        for k, default in params.items():
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


def with_config_function(f, path):
    params = get_params(f)

    @wraps(f)
    def wrapped(config):
        config = walk_dict(config, path)
        inputs = dict()
        for k, default in params.items():
            if default == inspect._empty:
                inputs[k] = config[k]
            else:
                inputs[k] = config.get(k, default)

        return f(**inputs)
    return wrapped


def with_config(arg, path=""):
    if isinstance(arg, str):
        return lambda cb: with_config(cb, arg)

    if isinstance(arg, type):
        return with_config_class(arg, path)

    return with_config_function(arg, path)
