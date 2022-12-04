from pytorch_lightning import loggers
from pytorch_lightning.loggers.logger import Logger, rank_zero_experiment
from pytorch_lightning.utilities import rank_zero_only
from tqdm import tqdm
from pprint import pformat


class ConsoleLogger(Logger):
    def __init__(self, indent=1, width=80):
        super().__init__()
        self.indent = indent
        self.width = width

    @property
    def name(self):
        return "ConsoleLogger"

    @property
    def version(self):
        # Return the experiment version, int or str.
        return 0

    @rank_zero_only
    def log_hyperparams(self, params):
        # params is an argparse.Namespace
        # your code to record hyperparameters goes here
        fmt = pformat(params, width=self.width, indent=self.indent)
        tqdm.write(fmt)

    @rank_zero_only
    def log_metrics(self, metrics, step):
        # metrics is a dictionary of metric names and values
        # your code to record metrics goes here
        metrics['_step'] = step
        fmt = pformat(metrics,
                      width=self.width, indent=self.indent)
        tqdm.write(fmt)

    @rank_zero_only
    def save(self):
        # Optional. Any code necessary to save logger data goes here
        pass

    @rank_zero_only
    def finalize(self, status):
        # Optional. Any code that needs to be run after training
        # finishes goes here
        pass


def MLFlowLogger(*args, tracking_uri=None, **kwargs):
    import mlflow
    logger = loggers.MLFlowLogger(*args, **kwargs, tracking_uri=tracking_uri)
    mlflow.set_tracking_uri(tracking_uri)
    return logger
