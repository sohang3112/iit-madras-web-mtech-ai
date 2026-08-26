"""Stage 3 — Train ResNet18 binary classifier, save model + training history."""
import sys, json, random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config.config import (
    DATA_DIR, MODEL_DIR, METRICS_DIR, CLASSES,
    IMG_SIZE, BATCH_SIZE, EPOCHS, LR, SEED,
)


# ── reproducibility ──────────────────────────────────────────────────────────
def set_seed(seed):
    random.seed(seed); np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ── dataset ──────────────────────────────────────────────────────────────────
class BinaryImageDataset(Dataset):
    def __init__(self, root, classes, transform=None):
        self.transform = transform
        self.samples = [
            (str(p), label)
            for label, cls in enumerate(classes)
            for p in (Path(root) / cls).glob("*.jpg")
        ]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, label


# ── transforms ───────────────────────────────────────────────────────────────
_norm = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

train_tf = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(**_norm),
])

val_tf = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(**_norm),
])


# ── model ─────────────────────────────────────────────────────────────────────
def build_model():
    m = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    for p in m.parameters():
        p.requires_grad = False
    m.fc = nn.Sequential(
        nn.Linear(m.fc.in_features, 128),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(128, 1),
    )
    return m


# ── training ─────────────────────────────────────────────────────────────────
def run_epoch(model, loader, criterion, optimizer, device, train=True):
    model.train() if train else model.eval()
    total_loss, correct = 0.0, 0
    ctx = torch.enable_grad() if train else torch.no_grad()
    with ctx:
        for imgs, labels in loader:
            imgs   = imgs.to(device)
            labels = labels.float().unsqueeze(1).to(device)
            logits = model(imgs)
            loss   = criterion(logits, labels)
            if train:
                optimizer.zero_grad(); loss.backward(); optimizer.step()
            total_loss += loss.item() * imgs.size(0)
            correct    += ((torch.sigmoid(logits) >= 0.5).float() == labels).sum().item()
    return total_loss / len(loader.dataset), correct / len(loader.dataset)


def train():
    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Stage 3] Device: {device}")

    train_ds = BinaryImageDataset(DATA_DIR / "seg_train", CLASSES, train_tf)
    train_ds = torch.utils.data.Subset(train_ds, list(range(0, len(train_ds), 5)))  # 20% for training

    val_ds   = BinaryImageDataset(DATA_DIR / "seg_test",  CLASSES, val_tf)
    val_ds   = torch.utils.data.Subset(val_ds, list(range(0, len(val_ds), 5)))  # 20% for validation
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=4)
    val_loader   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, num_workers=4)
    print(f"[Stage 3] Train: {len(train_ds)} | Val: {len(val_ds)}")

    model     = build_model().to(device)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=LR)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=4, gamma=0.3)

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    for epoch in range(1, EPOCHS + 1):
        tr_loss, tr_acc = run_epoch(model, train_loader, criterion, optimizer, device, train=True)
        vl_loss, vl_acc = run_epoch(model, val_loader,   criterion, optimizer, device, train=False)
        scheduler.step()
        history["train_loss"].append(tr_loss); history["train_acc"].append(tr_acc)
        history["val_loss"].append(vl_loss);   history["val_acc"].append(vl_acc)
        print(f"[Stage 3] Epoch {epoch:02d}/{EPOCHS}  "
              f"train_loss={tr_loss:.4f}  train_acc={tr_acc:.4f}  "
              f"val_loss={vl_loss:.4f}  val_acc={vl_acc:.4f}")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / "resnet18_binary.pth"
    torch.save(model.state_dict(), model_path)
    print(f"[Stage 3] Model saved → {model_path}")

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    hist_path = METRICS_DIR / "training_history.json"
    hist_path.write_text(json.dumps(history, indent=2))
    print(f"[Stage 3] History saved → {hist_path}")
    print("[Stage 3] Done.")


if __name__ == "__main__":
    train()
