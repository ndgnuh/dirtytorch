# short_desc: unix-like find(root, name="*", type, walk, cases)
# usage:
#   find(root, name="glob*", type=("d"|"f"), walk=True, cases=True)
import os
from os import path
from fnmatch import fnmatch, fnmatchcase


def find(root, name="*", type=None, walk=True, cases=True):
    matcher = fnmatchcase if cases else fnmatch
    def type_matcher(x): return True
    if type == "d":
        type_matcher = path.isdir
    if type == "f":
        type_matcher = path.isfile

    def condition(file):
        if not matcher(file, name):
            return False

        if not type_matcher(file):
            return False

        if not path.exists(file):
            return False

        return True

    if walk:
        files = (path.join(rt, file)
                 for (rt, dirs, files) in os.walk(root)
                 for file in (dirs + files))
    else:
        files = (path.join(root, file) for file in os.listdir(root))
    files = filter(condition, files)
    return set(files)
