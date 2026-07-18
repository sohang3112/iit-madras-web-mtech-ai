"""Ray Train + PyTorch on a generated 1-D regression (CPU-only)."""
import os, ray, torch
import torch.nn as nn

from ray import train
from ray.train import ScalingConfig, Checkpoint
from ray.train.torch import TorchTrainer

ray.init(address="auto")

def train_fn(cfg):
    n = 1024
    x = torch.linspace(-3, 3, n).unsqueeze(1)
    y = 2 * x + 1 + 0.3 * torch.randn_like(x)
    model = nn.Linear(1, 1)
    opt = torch.optim.SGD(model.parameters(), lr=cfg["lr"])
    loss_fn = nn.MSELoss()
    for epoch in range(cfg["epochs"]):
        pred = model(x)
        loss = loss_fn(pred, y)
        opt.zero_grad(); loss.backward(); opt.step()
        train.report({"epoch": epoch, "loss": float(loss.item())})
    print("trained weights:", model.weight.item(), model.bias.item())

trainer = TorchTrainer(
    train_loop_per_worker=train_fn,
    train_loop_config={"lr": 0.01, "epochs": 20},
    scaling_config=ScalingConfig(num_workers=2, use_gpu=False),
)
result = trainer.fit()
print("metrics:", result.metrics)

out = f"/storage/models/{__STUDENT_USERNAME}/{__JOB_NAME}/"
os.makedirs(out, exist_ok=True)
with open(out + "summary.txt", "w") as f:
    f.write(repr(result.metrics) + "\n")
print("wrote", out + "summary.txt")
