# short_desc: unified `read` function, to be updated with formats
from os import path


def read_txt(f, **k):
    with open(f, **k) as io:
        return io.read()


def read_yml(f, encoding="utf-8", **k):
    import yaml
    k.setdefault("Loader", yaml.FullLoader)
    with open(f, encoding=encoding) as io:
        return yaml.load(io, **k)


read_yaml = read_yml


def read_toml(f, encoding="utf-8", **k):
    import toml
    with open(f, encoding=encoding) as io:
        return toml.load(io, **k)


def read_pickle(f, **k):
    import pickle
    with open(f) as io:
        return pickle.load(io)


def read_torch_pt(f, **k):
    import torch
    return torch.load(f)


def read_json(f, encoding="utf-8", **k):
    import json
    with open(f, encoding=encoding) as io:
        return json.load(io)


ext_reader_map = dict(
    yml=read_yml,
    yaml=read_yml,
    toml=read_toml,
    pkl=read_pickle,
    pt=read_torch_pt,
    json=read_json
)


def read(f, reader=None, **kw):
    if reader is None:
        ext = path.splitext(f)[-1].lstrip(".")
        reader = ext_reader_map.get(ext, read_txt)

    return reader(f, **kw)
