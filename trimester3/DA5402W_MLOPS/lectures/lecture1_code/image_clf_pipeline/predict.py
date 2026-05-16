"""Inference script — predict class for a single image or all images in a folder.

Usage:
    python predict.py path/to/image.jpg
    python predict.py path/to/folder/
"""
import sys
import argparse
from pathlib import Path

import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config.config import MODEL_DIR, CLASSES, IMG_SIZE


def load_model(device):
    m = models.resnet18(weights=None)
    m.fc = nn.Sequential(
        nn.Linear(m.fc.in_features, 128),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(128, 1),
    )
    m.load_state_dict(torch.load(MODEL_DIR / "resnet18_binary.pth", map_location=device))
    m.eval()
    return m.to(device)


_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def predict_image(model, device, image_path):
    img = Image.open(image_path).convert("RGB")
    tensor = _transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        prob = torch.sigmoid(model(tensor)).item()
    label = CLASSES[1] if prob >= 0.5 else CLASSES[0]
    confidence = prob if prob >= 0.5 else 1 - prob
    return label, confidence


def main():
    parser = argparse.ArgumentParser(description="Image classifier inference")
    parser.add_argument("path", help="Image file or directory of images")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_model(device)
    print(f"Model loaded | device: {device}\n")

    target = Path(args.path)
    if target.is_dir():
        images = sorted(target.glob("*.jpg")) + sorted(target.glob("*.png"))
        if not images:
            print(f"No .jpg/.png images found in {target}")
            sys.exit(1)
    else:
        images = [target]

    print(f"{'File':<40} {'Prediction':<12} {'Confidence':>10}")
    print("-" * 64)
    for img_path in images:
        label, conf = predict_image(model, device, img_path)
        print(f"{img_path.name:<40} {label:<12} {conf:>9.1%}")


if __name__ == "__main__":
    main()
