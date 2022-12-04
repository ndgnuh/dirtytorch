from typing import Callable, Optional
from functools import wraps


class Functable(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def __call__(self, key, callback: Optional[Callable] = None):
        if callback is not None:
            self[key] = callback

        else:
            def register(callback: Callable):
                self[key] = callback

            return register
