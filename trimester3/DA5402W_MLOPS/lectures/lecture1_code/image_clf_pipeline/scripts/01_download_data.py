"""Stage 1 — Download Intel Image Classification dataset via kagglehub."""
import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config.config import KAGGLE_DATASET, DATA_DIR, CLASSES

import kagglehub


def download():
    print(f"[Stage 1] Downloading dataset: {KAGGLE_DATASET}")
    raw_path = Path(kagglehub.dataset_download(KAGGLE_DATASET))
    print(f"[Stage 1] Downloaded to: {raw_path}")

    # Copy only the two binary-class folders into outputs/data/
    for split in ("seg_train", "seg_test"):
        # Dataset nests as seg_train/seg_train/buildings — find the deepest
        # occurrence that actually contains a known class subdirectory.
        candidates = list(raw_path.rglob(split))
        src_split = next(
            (c for c in reversed(candidates) if any((c / cls).exists() for cls in CLASSES)),
            None,
        )
        if src_split is None:
            print(f"[Stage 1] WARNING: could not find {split}")
            continue
        print(f"[Stage 1] Found {split} at: {src_split}")
        for cls in CLASSES:
            src = src_split / cls
            dst = DATA_DIR / split / cls
            if dst.exists():
                print(f"[Stage 1] Already exists, skipping: {dst}")
                continue
            shutil.copytree(src, dst)
            n = len(list(dst.glob("*.jpg")))
            print(f"[Stage 1] Copied {n} images → {dst}")

    print("[Stage 1] Done.")


if __name__ == "__main__":
    download()
