def init_mlflow_logger(*args, tracking_uri=None, **kwargs):
    from pytorch_lightning import loggers
    import mlflow
    logger = loggers.MLFlowLogger(*args, **kwargs, tracking_uri=tracking_uri)
    mlflow.set_tracking_uri(tracking_uri)
    return logger
