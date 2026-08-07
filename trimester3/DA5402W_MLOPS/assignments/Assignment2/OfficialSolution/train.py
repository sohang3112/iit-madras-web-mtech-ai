"""
Part B: Model Training using Ray Tune + MLflow Logging.
Part C: Model Registration.

Loads the Parquet dataset produced by features_ic39149.py, splits it into
train/validation (80:20), tunes a PyTorch binary classifier's hyperparameters
with Ray Tune (>= 10 trials, maximizing validation F1-score), logs every
trial as its own MLflow run under experiment "assignment_2_ic39149" (params,
metrics, and artifacts), registers the run with the best validation F1-score
in the MLflow Model Registry as "Assignment2Classifier_ic39149", then
demonstrates loading the registered model back and running inference on the
processed test.csv dataset, saving the result to predictions_ic39149.csv.

Usage:
    python train_ic39149.py \
        --train-data data/processed/train_processed_ic39149.parquet \
        --test-data data/processed/test_processed_ic39149.parquet \
        --tracking-uri sqlite:///mlflow.db \
        --num-samples 10 --epochs 20
"""

import argparse
import os
import tempfile
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import mlflow.pytorch
import numpy as np
import pandas as pd
import ray
import torch
import torch.nn as nn
from mlflow.tracking import MlflowClient
from ray import tune
from ray.tune import Tuner, TuneConfig
from ray.air import RunConfig
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

ROLL_NO = "ic39149"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ray Tune + MLflow training pipeline for the Bank Marketing classifier"
    )
    parser.add_argument(
        "--train-data", type=str,
        default=f"/storage/models/web-mtech-ai/train_processed_{ROLL_NO}.parquet",
    )
    parser.add_argument(
        "--test-data", type=str,
        default=f"/storage/models/web-mtech-ai/test_processed_{ROLL_NO}.parquet",
    )
    parser.add_argument("--experiment-name", type=str, default=f"assignment_2_{ROLL_NO}")
    parser.add_argument(
        "--registered-model-name", type=str, default=f"Assignment2Classifier_{ROLL_NO}"
    )
    parser.add_argument(
        "--tracking-uri", type=str,
        default=os.environ.get(
            "MLFLOW_TRACKING_URI",
            f"sqlite:////storage/models/web-mtech-ai/mlflow_{ROLL_NO}.db",
        ),
    )
    parser.add_argument("--num-samples", type=int, default=10, help="Number of Ray Tune trials")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--ray-results-dir", type=str, default="./ray_results")
    parser.add_argument("--output-dir", type=str, default="/storage/models/web-mtech-ai/")
    return parser.parse_args()


class BankMarketingClassifier(nn.Module):
    def __init__(self, input_dim, hidden_size=64, dropout=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, max(hidden_size // 2, 2)),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(max(hidden_size // 2, 2), 1),
        )

    def forward(self, x):
        return self.net(x)


def train_one_trial(config, X_train, y_train, X_val, y_val, input_dim,
                     experiment_name, tracking_uri, epochs):
    """One Ray Tune trial: trains a model with the sampled hyperparameters and
    logs the full run (params, metrics, artifacts) to its own MLflow run."""
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    lr = config["lr"]
    batch_size = config["batch_size"]
    hidden_size = config["hidden_size"]
    dropout = config["dropout"]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_ds = TensorDataset(
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.float32).unsqueeze(1),
    )
    val_ds = TensorDataset(
        torch.tensor(X_val, dtype=torch.float32),
        torch.tensor(y_val, dtype=torch.float32).unsqueeze(1),
    )
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    model = BankMarketingClassifier(input_dim, hidden_size, dropout).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCEWithLogitsLoss()

    with mlflow.start_run(
        run_name=f"lr{lr:.5f}_bs{batch_size}_hs{hidden_size}_do{dropout:.2f}"
    ):
        mlflow.log_params({
            "learning_rate": lr,
            "batch_size": batch_size,
            "hidden_layer_size": hidden_size,
            "dropout": dropout,
            "epochs": epochs,
        })

        start_time = time.time()
        train_loss, val_loss = 0.0, 0.0
        for epoch in range(epochs):
            model.train()
            running_loss = 0.0
            for xb, yb in train_loader:
                xb, yb = xb.to(device), yb.to(device)
                optimizer.zero_grad()
                logits = model(xb)
                loss = criterion(logits, yb)
                loss.backward()
                optimizer.step()
                running_loss += loss.item() * xb.size(0)
            train_loss = running_loss / len(train_ds)

            model.eval()
            running_val_loss = 0.0
            with torch.no_grad():
                for xb, yb in val_loader:
                    xb, yb = xb.to(device), yb.to(device)
                    loss = criterion(model(xb), yb)
                    running_val_loss += loss.item() * xb.size(0)
            val_loss = running_val_loss / len(val_ds)

            mlflow.log_metric("training_loss", train_loss, step=epoch)
            mlflow.log_metric("validation_loss", val_loss, step=epoch)

        training_time = time.time() - start_time

        model.eval()
        all_probs, all_labels = [], []
        with torch.no_grad():
            for xb, yb in val_loader:
                probs = torch.sigmoid(model(xb.to(device))).cpu().numpy().ravel()
                all_probs.append(probs)
                all_labels.append(yb.numpy().ravel())
        y_prob = np.concatenate(all_probs)
        y_true = np.concatenate(all_labels)
        y_pred = (y_prob >= 0.5).astype(int)

        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_true, y_prob)

        mlflow.log_metrics({
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "roc_auc": roc_auc,
            "training_time": training_time,
            "final_training_loss": train_loss,
            "final_validation_loss": val_loss,
        })

        artifact_dir = tempfile.mkdtemp()

        cm = confusion_matrix(y_true, y_pred)
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(cm, cmap="Blues")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion Matrix")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center")
        cm_path = os.path.join(artifact_dir, "confusion_matrix.png")
        fig.savefig(cm_path, bbox_inches="tight")
        plt.close(fig)
        mlflow.log_artifact(cm_path)

        report_text = classification_report(y_true, y_pred, target_names=["no", "yes"])
        report_path = os.path.join(artifact_dir, "classification_report.txt")
        with open(report_path, "w") as f:
            f.write(report_text)
        mlflow.log_artifact(report_path)

        preds_path = os.path.join(artifact_dir, "val_predictions.csv")
        pd.DataFrame({"y_true": y_true, "y_pred": y_pred, "y_prob": y_prob}).to_csv(
            preds_path, index=False
        )
        mlflow.log_artifact(preds_path)

        input_example = X_train[:1]
        
        if int(mlflow.__version__.split(".")[0]) >= 3:
            mlflow.pytorch.log_model(
                model, name="model", input_example=input_example, serialization_format="pickle"
            )
        else:
            mlflow.pytorch.log_model(model, artifact_path="model", input_example=input_example)

        run_id = mlflow.active_run().info.run_id

    metrics = {
        "f1_score": f1,
        "accuracy": accuracy,
        "roc_auc": roc_auc,
        "validation_loss": val_loss,
        "mlflow_run_id": run_id,
    }
   
    if hasattr(tune, "report"):
        tune.report(metrics)
    else:
        from ray.air import session
        session.report(metrics)


def register_best_model(experiment_name, registered_model_name):
    """MLflow is the source of truth for 'highest validation F1-score' (Part C)."""
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    best_runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.f1_score DESC"],
        max_results=1,
    )
    if not best_runs:
        raise RuntimeError(
            f"No runs found in MLflow experiment '{experiment_name}' at "
            f"{mlflow.get_tracking_uri()}. If trials ran on multiple Ray "
            f"nodes, make sure --tracking-uri points at storage shared by "
            f"every node (e.g. a path under /storage), not a node-local path."
        )
    best_run = best_runs[0]
    best_run_id = best_run.info.run_id
    print(f"Best MLflow run: {best_run_id} (F1={best_run.data.metrics.get('f1_score'):.4f})")

    model_uri = f"runs:/{best_run_id}/model"
    registered = mlflow.register_model(model_uri=model_uri, name=registered_model_name)
    print(f"Registered model '{registered_model_name}' version {registered.version}")
    return registered.version


def run_test_inference(registered_model_name, version, test_data_path, output_dir):
    """Part C: load the registered model and run inference on the processed
    test.csv dataset, saving predictions_ic39149.csv."""
    print(f"Loading test data from {test_data_path}")
    test_df = pd.read_parquet(test_data_path)
    X_test = np.stack(test_df["features"].to_numpy()).astype(np.float32)

    loaded_model = mlflow.pytorch.load_model(f"models:/{registered_model_name}/{version}")
    loaded_model.eval()
    with torch.no_grad():
        probs = torch.sigmoid(loaded_model(torch.tensor(X_test))).numpy().ravel()
    preds = (probs >= 0.5).astype(int)

    output = pd.DataFrame({
        "prediction_proba": probs,
        "prediction": preds,
    })
    if "id" in test_df.columns:
        output.insert(0, "id", test_df["id"].to_numpy())

    out_path = os.path.join(output_dir, f"predictions_{ROLL_NO}.csv")
    output.to_csv(out_path, index=False)
    print(f"Saved test predictions to {out_path}")


def main():
    args = parse_args()

    print(f"Loading processed training dataset from {args.train_data}")
    df = pd.read_parquet(args.train_data)
    X = np.stack(df["features"].to_numpy()).astype(np.float32)
    y = df["label"].to_numpy().astype(np.float32)
    input_dim = X.shape[1]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    mlflow.set_tracking_uri(args.tracking_uri)
    mlflow.set_experiment(args.experiment_name)

    ray.init(ignore_reinit_error=True, include_dashboard=False)

    search_space = {
        "lr": tune.loguniform(1e-4, 1e-1),
        "batch_size": tune.choice([32, 64, 128, 256]),
        "hidden_size": tune.choice([16, 32, 64, 128]),
        "dropout": tune.uniform(0.1, 0.5),
    }

    trainable = tune.with_parameters(
        train_one_trial,
        X_train=X_train, y_train=y_train,
        X_val=X_val, y_val=y_val,
        input_dim=input_dim,
        experiment_name=args.experiment_name,
        tracking_uri=args.tracking_uri,
        epochs=args.epochs,
    )
    trainable_with_resources = tune.with_resources(trainable, {"cpu": 1})

    tuner = Tuner(
        trainable_with_resources,
        param_space=search_space,
        tune_config=TuneConfig(
            metric="f1_score",
            mode="max",
            num_samples=args.num_samples,
        ),
        run_config=RunConfig(
            name="bank_marketing_ray_tune",
            storage_path=os.path.abspath(args.ray_results_dir),
        ),
    )

    print(f"Starting Ray Tune hyperparameter search with {args.num_samples} trials")
    results = tuner.fit()

    best_result = results.get_best_result(metric="f1_score", mode="max")
    print("Best trial config:", best_result.config)
    print("Best trial validation F1:", best_result.metrics["f1_score"])

    version = register_best_model(args.experiment_name, args.registered_model_name)

    print("Demonstrating inference with the registered model on the validation set")
    loaded_model = mlflow.pytorch.load_model(f"models:/{args.registered_model_name}/{version}")
    loaded_model.eval()
    sample = torch.tensor(X_val[:5], dtype=torch.float32)
    with torch.no_grad():
        probs = torch.sigmoid(loaded_model(sample)).numpy().ravel()
    for i, p in enumerate(probs):
        print(f"Sample {i}: P(y=yes) = {p:.4f} (true label = {int(y_val[i])})")

    run_test_inference(args.registered_model_name, version, args.test_data, args.output_dir)

    ray.shutdown()


if __name__ == "__main__":
    main()
