from pytorch_lightning.callbacks import Callback


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
