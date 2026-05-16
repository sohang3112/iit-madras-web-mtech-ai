"""Stage 4 — Load saved model, run evaluation, save metrics + confusion matrix plot."""
import sys, json
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config.config import (
    DATA_DIR, MODEL_DIR, METRICS_DIR, CLASSES, IMG_SIZE, BATCH_SIZE,
)


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


def load_model(device):
    m = models.resnet18(weights=None)
    m.fc = nn.Sequential(
        nn.Linear(m.fc.in_features, 128),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(128, 1),
    )
    m.load_state_dict(torch.load(MODEL_DIR / "resnet18_binary.pth", map_location=device))
    return m.to(device)


def evaluate():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Stage 4] Device: {device}")

    tf = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    test_ds     = BinaryImageDataset(DATA_DIR / "seg_test", CLASSES, tf)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=4)

    model = load_model(device)
    model.eval()

    all_preds, all_labels = [], []
    with torch.no_grad():
        for imgs, labels in test_loader:
            logits = model(imgs.to(device)).cpu()
            preds  = (torch.sigmoid(logits) >= 0.5).long().squeeze(1)
            all_preds.extend(preds.tolist())
            all_labels.extend(labels.tolist())

    report = classification_report(all_labels, all_preds, target_names=CLASSES, output_dict=True)
    print("\n" + classification_report(all_labels, all_preds, target_names=CLASSES))

    # Save metrics JSON
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    metrics_path = METRICS_DIR / "eval_metrics.json"
    metrics_path.write_text(json.dumps(report, indent=2))
    print(f"[Stage 4] Metrics saved → {metrics_path}")

    # Save confusion matrix plot
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=CLASSES, yticklabels=CLASSES)
    plt.xlabel("Predicted"); plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plot_path = METRICS_DIR / "confusion_matrix.png"
    plt.savefig(plot_path)
    print(f"[Stage 4] Confusion matrix saved → {plot_path}")
    print("[Stage 4] Done.")


if __name__ == "__main__":
    evaluate()
