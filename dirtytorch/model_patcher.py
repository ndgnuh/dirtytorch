import inspect
from lenses import bind


def get_num_args(f):
    sig = inspect.signature(f)
    return len(sig.parameters)


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


def patch_net(net, patch, condition, returns_info=False):
    num_args_condition = get_num_args(condition)
    num_args_patch = get_num_args(patch)
    index = 0

    if returns_info:
        info = []

    for name, module in net.named_modules():
        args = (module, name, index)
        if condition(*args[:num_args_condition]):
            patched = patch(*args[:num_args_patch])
            net = set_module(net, name, patched)
            if returns_info and patched != module:
                info.append((name, module, patched, index))
            index += 1

    if returns_info:
        return net, info
    else:
        return net


def create_equivalent(ref, Layer):
    args, kwargs = parse_extra_repr(ref.extra_repr())
    return Layer(*args, **kwargs)


def replace_layers(net, src_Layer, dst_Layer):
    def condition(module):
        return isinstance(module, src_Layer)

    def patch(module):
        return create_equivalent(module, dst_Layer)

    return patch_net(net, condition, patch)
