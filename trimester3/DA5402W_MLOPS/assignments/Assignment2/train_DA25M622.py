import pyspark
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
import ray
from ray import tune
from ray.tune.schedulers import ASHAScheduler
import ray.train
import mlflow
import time
import os
import tempfile
from pathlib import Path
import pandas as pd
import numpy as np
import traceback

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns

from ray.air.integrations.mlflow import setup_mlflow

# Keep Ray and Spark from overcommitting memory on this laptop.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")

ray.init(ignore_reinit_error=True, num_cpus=1)

DATASET_PATH = os.path.abspath("train_processed_DA25M622.parquet")

def trainable(config):
    # Enforce garbage collection inside workers to reclaim memory early
    import gc
    gc.collect()
    
    spark = None
    try:
        if not os.path.exists(DATASET_PATH):
            raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

        setup_mlflow(
            config,
            experiment_name="assignment 2 DA25M622",
            create_experiment_if_not_exists=True
        )
        
        spark = SparkSession.builder \
            .appName(f"Trial_{ray.tune.get_context().get_trial_id()}") \
            .config("spark.driver.bindAddress", "127.0.0.1") \
            .config("spark.driver.memory", "1g") \
            .config("spark.executor.memory", "1g") \
            .config("spark.driver.memoryOverhead", "512m") \
            .config("spark.executor.memoryOverhead", "512m") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
            .config("spark.sql.shuffle.partitions", "1") \
            .config("spark.default.parallelism", "1") \
            .master("local[1]") \
            .getOrCreate()
        
        df = spark.read.parquet(DATASET_PATH).select("features", "y")
        train_df, val_df = df.randomSplit([0.8, 0.2], seed=42)
        
        f1_evaluator = MulticlassClassificationEvaluator(labelCol="y", predictionCol="prediction", metricName="f1")
        acc_evaluator = MulticlassClassificationEvaluator(labelCol="y", predictionCol="prediction", metricName="accuracy")
        prec_evaluator = MulticlassClassificationEvaluator(labelCol="y", predictionCol="prediction", metricName="weightedPrecision")
        rec_evaluator = MulticlassClassificationEvaluator(labelCol="y", predictionCol="prediction", metricName="weightedRecall")
        roc_evaluator = BinaryClassificationEvaluator(labelCol="y", rawPredictionCol="rawPrediction", metricName="areaUnderROC")

        start_time = time.time()
        
        lr = LogisticRegression(
            regParam=1/config["C"], 
            maxIter=config["max_iter"], 
            featuresCol='features', 
            labelCol='y'
        )
        
        model = lr.fit(train_df)
        training_time = time.time() - start_time
        
        predictions = model.transform(val_df)
        
        f1_score = f1_evaluator.evaluate(predictions)
        accuracy = acc_evaluator.evaluate(predictions)
        precision = prec_evaluator.evaluate(predictions)
        recall = rec_evaluator.evaluate(predictions)
        roc_auc = roc_evaluator.evaluate(predictions)
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1_score)
        mlflow.log_metric("roc_auc", roc_auc)
        mlflow.log_metric("training_time", training_time)
        
        # Aggregate counts natively to keep driver payloads low
        counts_df = predictions.groupBy("y", "prediction").count().toPandas()
        
        unique_labels = sorted(list(set(counts_df["y"].unique()) | set(counts_df["prediction"].unique())))
        num_classes = len(unique_labels)
        label_map = {label: idx for idx, label in enumerate(unique_labels)}
        
        cm = np.zeros((num_classes, num_classes), dtype=int)
        for _, row in counts_df.iterrows():
            i = label_map[row["y"]]
            j = label_map[row["prediction"]]
            cm[i, j] = row["count"]
            
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = os.path.join(tmpdir, "classification_report.txt")
            with open(report_path, "w") as f:
                f.write(f"Accuracy: {accuracy:.4f}\n")
                f.write(f"Weighted Precision: {precision:.4f}\n")
                f.write(f"Weighted Recall: {recall:.4f}\n")
                f.write(f"F1 Score: {f1_score:.4f}\n")
            mlflow.log_artifact(report_path)
            
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                        xticklabels=unique_labels, yticklabels=unique_labels)
            ax.set_ylabel('Actual')
            ax.set_xlabel('Predicted')
            ax.set_title('Confusion Matrix')
            cm_path = os.path.join(tmpdir, "confusion_matrix.png")
            fig.savefig(cm_path)
            plt.close(fig)
            mlflow.log_artifact(cm_path)
            
            pred_path = os.path.join(tmpdir, "validation_counts.csv")
            counts_df.to_csv(pred_path, index=False)
            mlflow.log_artifact(pred_path)
            
            mlflow.spark.log_model(model, artifact_path="model")

        # Uncache data frames explicitly before closing the context
        train_df.unpersist()
        val_df.unpersist()
        spark.stop()
        
        ray.tune.report({"f1": f1_score, "accuracy": accuracy})

    except Exception as e:
        print("--- WORKER EXCEPTION ENCOUNTERED ---")
        traceback.print_exc()
        if spark:
            try:
                spark.stop()
            except:
                pass
        ray.tune.report({"f1": 0.0, "accuracy": 0.0})

# Resolve MLflow output from the script directory so it always lands in this project folder.
BASE_DIR = Path(__file__).resolve().parent
MLRUNS_DIR = BASE_DIR / "mlruns"
MLRUNS_DIR.mkdir(parents=True, exist_ok=True)
tracking_uri = MLRUNS_DIR.as_uri()

print(f"MLflow tracking URI: {tracking_uri}")
print(f"MLflow artifacts directory: {MLRUNS_DIR}")

os.environ['MLFLOW_ALLOW_FILE_STORE'] = 'true'
mlflow.set_tracking_uri(tracking_uri)
experiment_id = mlflow.create_experiment(
    "assignment2_DA25M622",
    artifact_location=tracking_uri
)

with mlflow.start_run(experiment_id=experiment_id):
    search_space = {
        "C": tune.choice([1.0]),
        "max_iter": tune.choice([100]),
    }

    tuner = tune.Tuner(
        tune.with_resources(trainable, resources={"cpu": 1}),
        param_space=search_space,
        tune_config=tune.TuneConfig(
            num_samples=1,
            max_concurrent_trials=1,
            scheduler=ASHAScheduler(metric="f1", mode="max"),
        ),
    )

    results = tuner.fit()
    best = results.get_best_result(metric="f1", mode="max")
    print("Best config:", best.config)
    print("Best F1 score recorded:", best.metrics.get("f1"))
    ray.shutdown()