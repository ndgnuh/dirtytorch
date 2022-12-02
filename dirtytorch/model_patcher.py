import inspect
from lenses import bind

def parse_extra_repr(s):
    def take(*args, **kw):
        return args, kw
    return eval(f"take({s})")


def get_kw_position(f, kw):
    sig = inspect.signature(f)
    params = sig.parameters.keys()
    return list(params).index(kw)


def get_extra_repr(s):
    def take(*args, **kw):
        return args, kw
    return eval(f"take({s})")


def patch_arg(ref, *moda, **modk):
    Layer = type(ref)

    # Get the current configuration
    args, kwargs = parse_extra_repr(ref.extra_repr())
    args = list(args)

    # Update positionals
    for i, a in enumerate(moda):
        args[i] = a

    # Update keywords
    npositional = len(args)
    for k, v in modk.items():
        # If keyword is optionally positional
        # Put the keyword in the positional
        pos = get_kw_position(Layer, k)
        if pos < npositional:
            args[pos] = v
        else:
            kwargs[k] = v

    # Return patched layer
    return Layer(*args, **kwargs)


def get_module(net, path):
    lens_ = bind(net)
    for name in path.split("."):
        lens_ = lens_.GetAttr(name)
    return lens_.get()


def set_module(net, path, module):
    lens_ = bind(net)
    for name in path.split("."):
        lens_ = lens_.GetAttr(name)
    return lens_.set(module)


def patch_net(net, patch, condition):
    for name, module in net.named_modules():
        if condition(module, name):
            patched = patch(module, name)
            net = set_module(net, name, patched)
    return net
