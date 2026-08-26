"""Stage 5 — Validate model metrics against thresholds. Fails pipeline if any check is missed."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config.config import (
    METRICS_DIR, CLASSES,
    MIN_ACCURACY, MIN_PRECISION, MIN_RECALL, MIN_F1,
)


def validate():
    metrics_path = METRICS_DIR / "eval_metrics.json"
    if not metrics_path.exists():
        print("[Stage 5] ERROR: eval_metrics.json not found. Run Stage 4 first.")
        sys.exit(1)

    metrics = json.loads(metrics_path.read_text())

    checks = []

    # Overall accuracy
    accuracy = metrics["accuracy"]
    checks.append(("Overall", "accuracy", accuracy, MIN_ACCURACY))

    # Per-class precision, recall, F1
    for cls in CLASSES:
        checks.append((cls, "precision", metrics[cls]["precision"], MIN_PRECISION))
        checks.append((cls, "recall",    metrics[cls]["recall"],    MIN_RECALL))
        checks.append((cls, "f1-score",  metrics[cls]["f1-score"],  MIN_F1))

    # Print report
    print(f"\n{'Class':<12} {'Metric':<12} {'Value':>8}  {'Threshold':>9}  {'Status':>6}")
    print("-" * 55)

    failed = []
    for cls, metric, value, threshold in checks:
        passed = value >= threshold
        status = "PASS" if passed else "FAIL"
        print(f"{cls:<12} {metric:<12} {value:>8.4f}  {threshold:>9.4f}  {status:>6}")
        if not passed:
            failed.append((cls, metric, value, threshold))

    print("-" * 55)

    if failed:
        print(f"\n[Stage 5] FAILED — {len(failed)} check(s) did not meet threshold:")
        for cls, metric, value, threshold in failed:
            print(f"  {cls} {metric}: {value:.4f} < {threshold:.4f}")
        sys.exit(1)
    else:
        print(f"\n[Stage 5] All {len(checks)} checks PASSED. Model is approved.")


if __name__ == "__main__":
    validate()
