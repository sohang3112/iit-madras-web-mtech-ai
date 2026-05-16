"""Stage 2 — Verify data integrity and report class distribution."""
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config.config import DATA_DIR, CLASSES, METRICS_DIR
import json


def preprocess():
    print("[Stage 2] Verifying dataset ...")
    stats = {}

    for split in ("seg_train", "seg_test"):
        stats[split] = {}
        total = 0
        for cls in CLASSES:
            cls_dir = DATA_DIR / split / cls
            if not cls_dir.exists():
                raise FileNotFoundError(
                    f"Missing: {cls_dir}. Run 01_download_data.py first."
                )
            n = len(list(cls_dir.glob("*.jpg")))
            stats[split][cls] = n
            total += n
            print(f"[Stage 2]   {split}/{cls}: {n} images")
        stats[split]["total"] = total

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    out = METRICS_DIR / "data_stats.json"
    out.write_text(json.dumps(stats, indent=2))
    print(f"[Stage 2] Stats saved to {out}")
    print("[Stage 2] Done.")


if __name__ == "__main__":
    preprocess()
