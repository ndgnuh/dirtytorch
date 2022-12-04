from pytorch_lightning.callbacks import Callback
from typing import Callable
from functools import wraps
import torch


class GlobalStepLRScheduler(Callback):
    def __init__(self, every: int = None, model=None, trainer=None):
        super().__init__()
        self.every = every
        self.model = model
        self.trainer = trainer

    def on_before_optimizer_step(self, *args, **kwargs):
        if self.trainer is not None:
            global_step = self.trainer.global_step
            model = self.trainer.model
        elif self.model is not None:
            global_step = self.model.global_step
            model = self.model
        else:
            raise ValueError(
                "Bind this callback with a model or a trainer first")

        if global_step != 0 and global_step % self.every == 0:
            lr_schedulers = model.lr_schedulers()
            if lr_schedulers is None:
                return
            if not isinstance(lr_schedulers, list):
                lr_schedulers = [lr_schedulers]
            for lr_scheduler in lr_schedulers:
                lr_scheduler.step()


class MetricMonitorCallback(Callback):
    def __init__(self,
                 metric: str,
                 mode: str,
                 callback: Callable,
                 on: str, model=None):
        super().__init__()
        assert mode in ["min", "max"]
        assert on.startswith("on_") and hasattr(Callback, on)

        # Every hook receive trainer as first argument
        @wraps(getattr(self, on))
        def callback_wrapper(trainer, *args, **kwargs):
            current_metric = trainer.logged_metrics[self.metric]
            if self.mode == "min":
                cond = current_metric < self.current_metric
            elif self.mode == "max":
                cond = current_metric > self.current_metric
            if cond:
                self.current_metric = current_metric
                self.callback(self, *args, **kwargs)

        setattr(self, on, callback_wrapper)
        if mode == "min":
            self.current_metric = torch.inf
        elif mode == "max":
            self.current_metric = -torch.inf
        self.callback = callback
        self.metric = metric
        self.mode = mode
        self.model = model
        self.on = on

    def __repr__(self):
        name = self.__class__.__name__
        args = [
            f"metric={self.metric}",
            f"mode={self.mode}",
            f"on={self.on}",
        ]
        args = ', '.join(args)
        return f"{name}({args})"
