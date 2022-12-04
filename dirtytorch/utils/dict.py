# short_desc: Helpers for dict's (merge_dict, AttrDict)
from copy import copy as mcopy


class AttrDict(dict):
    def __init__(self, *arg, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def munchify(d: dict, max_depth=100, depth=0, copy=False):
    if depth > max_depth:
        print("Maximum recursion depth reached, returning base dict")
        return base

    if copy:
        d = mcopy.copy(d)

    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = munchify(v,
                            copy=copy,
                            max_depth=max_depth,
                            depth=depth+1)

    return AttrDict(d)


def merge_dict(base, *updates, max_depth=100, depth=0, copy=False):
    if depth > max_depth:
        print("Maximum recursion depth reached, returning base dict")
        return base

    if copy:
        base = mcopy.copy(base)

    for update in updates:
        for k, u in update.items():
            v = base.get(k, None)
            # If of different type, assign
            if not isinstance(u, type(v)):
                base[k] = u
                continue

            # Both are dict
            if isinstance(u, dict):
                base[k] = merge_dict(v, u,
                                     copy=copy,
                                     max_depth=max_depth,
                                     depth=depth+1)
                continue

            # Both are list or tuples, just extend
            if isinstance(v, (list, tuple)):
                base[k] = v + u
                continue

            # Fallback, just assign
            base[k] = u

    return base
