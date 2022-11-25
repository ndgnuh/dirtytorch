from pytorch_lightning.callbacks import Callback, ModelCheckpoint
import pytorch_lightning as pl
import torch
from os import path
import os


class Learner(pl.LightningModule):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.save_hyperparameters()

    def training_step(self, batch):
        output = self(batch)
        return output['loss']

    def training_epoch_end(self, outputs):
        losses = [output['loss'].detach().item() for output in outputs]
        mean_loss = sum(losses) / len(losses)
        self.log("Train loss", mean_loss)

    def validation_step(self, batch, idx):
        output = self(batch)
        scores = output.get('scores', tuple())
        if not isinstance(scores, tuple):
            scores = (scores,)
        return scores

    def validation_epoch_end(self, outputs):
        n = len(outputs)
        names = self.get_score_names()
        scores = dict()

        # Calculate total score
        for output in outputs:
            for (name, score) in zip(names, output):
                scores[name] = scores.get(name, 0) + score

        # Divide by batch
        for (name, score) in scores.items():
            scores[name] = score.detach().item() / n

        # Best scores
        best_scores = getattr(self, "best_scores", dict())
        for name, score in scores.items():
            best_name = f"Best {name}"
            best = best_scores.get(best_name, 0)
            if score > best:
                best_scores[best_name] = score
        self.best_scores = best_scores

        # log
        self.log_dict(scores)
        self.log_dict(best_scores)

    def get_score_names(self):
        return tuple(f"Score {i:02d}" for i in range(10))

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=self.learning_rate)


class Trainable(pl.LightningModule):
    def training_step(self, batch, batch_idx):
        output = self(batch)

        self.log("metric/train_loss", output["loss"])
        return output['loss']

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=self.learning_rate)

    def validation_step(self, batch, idx):
        output = self(batch)
        pred = output['prediction']
        label = output['ground_truth']
        score = self.score(pred, label)
        return score

    @torch.no_grad()
    def validation_epoch_end(self, scores):
        score = sum(scores) / len(scores)
        score = score.detach().item()
        self.current_score = score
        score_name = self.score.__class__.__name__
        if getattr(self, "best_score", 0) < self.current_score:
            self.best_score = self.current_score
            torch.save(self.state_dict(), "best-score-classify.pt")
        self.log(f"score/{score_name}", self.current_score,
                 on_epoch=True, on_step=False)
        self.log(f"score/best_{score_name}", getattr(self,
                 'best_score', 0), on_epoch=True, on_step=False)
        print(f"{score_name}:", self.current_score,
              ", best:", getattr(self, "best_score", 0))


class RetuneLRCallback(Callback):
    def __init__(self, every=2, at_start=False):
        super().__init__()
        self.every = every
        self.at_start = True

    def on_train_epoch_start(self, trainer, model):
        run = model.current_epoch % self.every == 0
        if not self.at_start:
            run = run and model.current_epoch > 0
        if run:
            trainer.tune(model)


class CheckpointCallback(Callback):
    def __init__(self,  model_name, metric_name, dirpath='checkpoints'):
        super().__init__()
        self.model_name = model_name
        self.metric_name = metric_name
        self.dirpath = dirpath
        self.best = 0
        self.metric_basename = path.basename(metric_name)
        self.previous_checkpoint = ""

    def on_validation_epoch_end(self, trainer, module):
        metric = trainer.logged_metrics[self.metric_name]
        max_metric = max(metric, self.best)
        if max_metric == metric and self.best != max_metric:
            self.best = max_metric
            if path.isfile(self.previous_checkpoint):
                os.remove(self.previous_checkpoint)
            file = f"{self.metric_basename}={max_metric:.4f}_epoch={trainer.current_epoch:04d}.cpkt"
            file = path.join(self.dirpath, self.model_name, file)
            trainer.save_checkpoint(file)
            self.previous_checkpoint = file


# def CheckpointCallback(model_name, metric_name, save_top_k=None):
#     metric_basename = metric_name.replace("/", "-")
#     filename = f"{model_name}/{metric_basename}={{{metric_name}:.4f}}_epoch={{epoch:03d}}"
#     return ModelCheckpoint(
#         dirpath="checkpoints",
#         every_n_epochs=1,
#         monitor=metric_name,
#         filename=filename,
#         save_last=True,
#         verbose=True,
#         auto_insert_metric_name=False,
#         save_on_train_epoch_end=True,
#     )
