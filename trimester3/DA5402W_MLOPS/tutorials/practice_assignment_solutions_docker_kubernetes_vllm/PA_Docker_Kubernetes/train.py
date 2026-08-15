"""
train.py
========
Trains a Logistic Regression classifier on the Pima Indians Diabetes dataset,
evaluates it, and persists the fitted pipeline (scaler + model) with joblib.

Usage:
    python train.py
    python train.py --data-path data/pima-indians-diabetes.csv --model-path model/model.joblib

The script is self-contained: if the dataset CSV is not found locally it is
downloaded once from a public mirror and cached under `data/`.
"""

import argparse
import json
import logging
import os
import urllib.request
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# The raw dataset has no header row; these are the canonical Pima column names.
COLUMN_NAMES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]

# For these clinical measurements a value of 0 is biologically implausible and
# actually encodes a missing reading in this dataset. They are imputed with
# the column median rather than dropped, to keep every row usable.
ZERO_AS_MISSING_COLUMNS = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
]

DATASET_URL = (
    "https://raw.githubusercontent.com/jbrownlee/Datasets/master/"
    "pima-indians-diabetes.data.csv"
)


def download_dataset(destination: Path) -> None:
    """Download the Pima Indians Diabetes CSV if it isn't already cached."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Dataset not found locally. Downloading from %s", DATASET_URL)
    urllib.request.urlretrieve(DATASET_URL, destination)
    logger.info("Dataset downloaded to %s", destination)


def load_dataset(data_path: Path) -> pd.DataFrame:
    """Load the dataset from disk, downloading it first if necessary."""
    if not data_path.exists():
        download_dataset(data_path)
    df = pd.read_csv(data_path, header=None, names=COLUMN_NAMES)
    logger.info("Loaded dataset with shape %s", df.shape)
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Replace biologically-invalid zeros with the column median."""
    df = df.copy()
    for column in ZERO_AS_MISSING_COLUMNS:
        median = df.loc[df[column] != 0, column].median()
        num_zeros = (df[column] == 0).sum()
        if num_zeros:
            logger.info(
                "Imputing %d zero value(s) in '%s' with median %.2f",
                num_zeros,
                column,
                median,
            )
        df[column] = df[column].replace(0, median)
    return df


def build_pipeline(C: float, max_iter: int, random_state: int) -> Pipeline:
    """Standardize features, then fit Logistic Regression. Bundled as one
    pipeline so scaling is applied consistently at inference time."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    C=C,
                    max_iter=max_iter,
                    random_state=random_state,
                ),
            ),
        ]
    )


def evaluate(model: Pipeline, X_test, y_test) -> dict:
    """Compute the standard classification metrics for the held-out test set."""
    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
    }

    logger.info("Evaluation metrics: %s", json.dumps(metrics, indent=2))
    logger.info("Confusion matrix:\n%s", confusion_matrix(y_test, y_pred))
    logger.info("Classification report:\n%s", classification_report(y_test, y_pred))

    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-path",
        type=Path,
        default=Path(os.environ.get("DATA_PATH", "data/pima-indians-diabetes.csv")),
        help="Path to the dataset CSV (downloaded automatically if missing).",
    )
    parser.add_argument(
        "--model-path",
        type=Path,
        default=Path(os.environ.get("MODEL_PATH", "model/model.joblib")),
        help="Where to save the trained pipeline.",
    )
    parser.add_argument(
        "--metrics-path",
        type=Path,
        default=Path("model/metrics.json"),
        help="Where to save the evaluation metrics as JSON.",
    )
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--C", type=float, default=1.0, help="Inverse regularization strength.")
    parser.add_argument("--max-iter", type=int, default=1000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    df = load_dataset(args.data_path)
    df = clean_dataset(df)

    X = df.drop(columns=["Outcome"])
    y = df["Outcome"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )
    logger.info("Train size: %d | Test size: %d", len(X_train), len(X_test))

    model = build_pipeline(C=args.C, max_iter=args.max_iter, random_state=args.random_state)
    model.fit(X_train, y_train)
    logger.info("Model training complete.")

    metrics = evaluate(model, X_test, y_test)

    args.model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model_path)
    logger.info("Model saved to %s", args.model_path)

    args.metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with open(args.metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    logger.info("Metrics saved to %s", args.metrics_path)


if __name__ == "__main__":
    main()
