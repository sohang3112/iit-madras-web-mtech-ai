"""Template (b): Spark job that logs params + metrics to MLflow.

Logs to experiment student/<your-username> (set automatically by the platform).
Open the MLflow link in the UI afterwards to see the run. This template logs
params + metrics only (no artifacts), so it needs no object-store credentials.
"""
import os
import random

import mlflow
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("spark-mlflow").getOrCreate()

# Tracking URI + experiment are injected by the platform via env vars.
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow-server:5000"))
mlflow.set_experiment(os.environ.get("MLFLOW_EXPERIMENT_NAME", "student/unknown"))

num_samples = 1_000_000
with mlflow.start_run(run_name="pi-estimate"):
    mlflow.log_param("num_samples", num_samples)

    def _inside(_):
        x, y = random.random(), random.random()
        return x * x + y * y < 1.0

    count = spark.sparkContext.parallelize(range(num_samples), 8).filter(_inside).count()
    pi = 4.0 * count / num_samples

    mlflow.log_metric("pi_estimate", pi)
    mlflow.log_metric("abs_error", abs(pi - 3.141592653589793))
    print(f"pi ~= {pi}  (params + metrics logged to MLflow)")

spark.stop()
