from pytorch_lightning.callbacks import Callback
from typing import Callable
from functools import wraps
import torch


class GlobalStepLRScheduler(Callback):
    def __init__(self, every: int = None, only=True):
        super().__init__()
        self.every = every
        self.only = only

    def on_before_optimizer_step(self,
                                 trainer,
                                 pl_module,
                                 optimizer,
                                 optimizer_idx):
        global_step = trainer.global_step

        if global_step != 0 and global_step % self.every == 0:
            for lrs in trainer.lr_scheduler_configs:
                lr_scheduler = lrs.scheduler
                lr_scheduler.step()
                for lr in lr_scheduler.get_lr():
                    pl_module.log("learning_rate", lr)

    def on_train_start(self, trainer, model):
        # Co-exist with the original config
        if not self.only:
            return

        # Disable calling lr scheduler from the model
        for lrs in trainer.lr_scheduler_configs:
            lrs.interval = 'epoch'
            lrs.frequency = 99999999999999999


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
