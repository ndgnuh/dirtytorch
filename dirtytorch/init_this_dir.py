# Warning
# - this module is hacky and use ugly exec code
# - this module is slow because of the exec
# - this module should should not be used in production
from os import path, listdir

modules = listdir(path.dirname(__file__))
modules = [path.splitext(module)[0] for module in modules
           if module.endswith(".py")
           and not (module.startswith("__") and module.endswith("__"))]
lines = [f"from .{module} import *" for module in modules]
exec("\n".join(lines))
