"""Pipeline orchestrator — runs all stages in order, stops on failure."""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / "scripts"

STAGES = [
    ("Stage 1: Download Data",   "01_download_data.py"),
    ("Stage 2: Preprocess",      "02_preprocess.py"),
    ("Stage 3: Train",           "03_train.py"),
    ("Stage 4: Evaluate",        "04_evaluate.py"),
    ("Stage 5: Validate Model",  "05_validate_model.py"),
]


def run_stage(name, script):
    print(f"\n{'='*55}")
    print(f"  {name}")
    print(f"{'='*55}")
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script)],
        check=False,
    )
    if result.returncode != 0:
        print(f"\n[PIPELINE] FAILED at: {name}")
        sys.exit(result.returncode)


if __name__ == "__main__":
    print("Starting Image Classification Pipeline")
    for name, script in STAGES:
        run_stage(name, script)
    print("\n[PIPELINE] All stages completed successfully.")
