"""Central config — all pipeline stages read from here."""
from pathlib import Path

# Paths
BASE_DIR    = Path(__file__).resolve().parents[1]
DATA_DIR    = BASE_DIR / "outputs" / "data"
MODEL_DIR   = BASE_DIR / "outputs" / "models"
METRICS_DIR = BASE_DIR / "outputs" / "metrics"

# Dataset
KAGGLE_DATASET = "puneet6060/intel-image-classification"
CLASSES        = ["buildings", "forest"]   # binary: 0=buildings, 1=forest

# Preprocessing
IMG_SIZE = 150

# Training
BATCH_SIZE = 32
EPOCHS     = 10
LR         = 1e-3

# Reproducibility
SEED = 42

# Model validation thresholds
MIN_ACCURACY  = 0.85
MIN_PRECISION = 0.80
MIN_RECALL    = 0.80
MIN_F1        = 0.80
