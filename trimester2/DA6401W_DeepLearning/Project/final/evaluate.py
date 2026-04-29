from pathlib import Path
import urllib.request

from matplotlib import pyplot as plt, font_manager as fm
import pandas as pd
import lightning as L
from torch.utils.data import DataLoader

# custom user modules
from train import EmojiClassifier, EmojiDataset


train_path = Path("../v1_scratch_embeddings/96emojis_50descriptions/train.csv")
val_path = Path("../v1_scratch_embeddings/96emojis_50descriptions/val.csv")
emojis = sorted(pd.read_csv(val_path)["Emoji"].unique())
Path("emoji_classes.txt").write_text("\n".join(emojis))
val_ds = EmojiDataset(val_path)
val_loader = DataLoader(val_ds, batch_size=64, shuffle=False)
model = EmojiClassifier.load_from_checkpoint(
    "lightning_logs/version_2/checkpoints/epoch=10-step=638.ckpt",
    input_dim=768,
    num_classes=96,
    emojis=emojis,
)
trainer = L.Trainer(accelerator="auto")
trainer.test(model, dataloaders=val_loader)
