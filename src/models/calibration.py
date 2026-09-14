import torch
import torch.nn as nn
from torch import optim
from src.config import INITIAL_TEMPERATURE

class TemperatureScaling(nn.Module):
    """
    Post-hoc temperature scaling to calibrate model probabilities.
    """
    def __init__(self):
        super(TemperatureScaling, self).__init__()
        self.temperature = nn.Parameter(torch.ones(1) * INITIAL_TEMPERATURE)

    def forward(self, logits: torch.Tensor) -> torch.Tensor:
        """
        Applies temperature scaling.
        logits: (B, 1) or (B,) tensor
        """
        temperature = self.temperature.unsqueeze(1).expand(logits.size(0), logits.size(1)) if logits.dim() > 1 else self.temperature
        return torch.sigmoid(logits / temperature)

    def fit(self, logits_val: torch.Tensor, labels_val: torch.Tensor, max_iter: int = 50) -> float:
        """
        Learn temperature via LBFGS on BCEWithLogitsLoss.
        """
        nll_criterion = nn.BCEWithLogitsLoss()
        optimizer = optim.LBFGS([self.temperature], lr=0.01, max_iter=max_iter)

        def eval():
            optimizer.zero_grad()
            loss = nll_criterion(logits_val / self.temperature, labels_val.float())
            loss.backward()
            return loss
        
        optimizer.step(eval)
        return self.temperature.item()
