import torch
from torch.nn import functional as F
from dataclasses import dataclass


@dataclass
class BalancedBCEWithLogitsLoss:
    k: int = 3  # negative / positive ratio

    def __call__(self, predicts, targets):
        target_mask = torch.sigmoid(targets) >= 0.5
        n_positive = torch.count_nonzero(target_mask)
        n_negative = torch.min(torch.count_nonzero(
            ~target_mask), self.k * n_positive)
        losses = F.binary_cross_entropy_with_logits(
            predicts, targets, reduction="none")

        pos_losses = torch.sum(losses[target_mask].sort(
            descending=True).values[:n_positive])
        neg_losses = torch.sum(losses[~target_mask].sort(
            descending=True).values[:n_negative])
        balanced_loss = (pos_losses + neg_losses) / (n_positive + n_negative)
        return balanced_loss


@dataclass
class BalancedBCELoss:
    k: int = 3  # negative / positive ratio

    def __call__(self, predicts, targets):
        assert targets.min() >= 0 and targets.max() <= 1
        assert predicts.min() >= 0 and predicts.max() <= 1
        target_mask = targets >= 0.5
        n_positive = torch.count_nonzero(target_mask)
        n_negative = torch.min(torch.count_nonzero(
            ~target_mask), self.k * n_positive)
        losses = F.binary_cross_entropy(predicts, targets, reduction="none")
        pos_losses = torch.sum(losses[target_mask].sort(
            descending=True).values[:n_positive])
        neg_losses = torch.sum(losses[~target_mask].sort(
            descending=True).values[:n_negative])
        balanced_loss = (pos_losses + neg_losses) / (n_positive + n_negative)
        return balanced_loss
