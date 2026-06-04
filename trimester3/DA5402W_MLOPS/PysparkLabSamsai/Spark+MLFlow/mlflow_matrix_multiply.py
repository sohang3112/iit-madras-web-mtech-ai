"""Sample (MLflow): distributed matrix multiply, logging size + GFLOP/s to MLflow.

Logs to experiment student/<your-username>.
"""
import os
import time

import mlflow
import numpy as np
from pyspark.sql import SparkSession

N = 1000
BLOCKS = 16

spark = SparkSession.builder.appName("mlflow-matrix").getOrCreate()
sc = spark.sparkContext
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow-server:5000"))
mlflow.set_experiment(os.environ.get("MLFLOW_EXPERIMENT_NAME", "student/unknown"))

rng = np.random.default_rng(0)
A = rng.standard_normal((N, N))
B = rng.standard_normal((N, N))
B_bc = sc.broadcast(B)
rows_per = (N + BLOCKS - 1) // BLOCKS
blocks = [(i * rows_per, A[i * rows_per:(i + 1) * rows_per]) for i in range(BLOCKS)]

with mlflow.start_run(run_name="matrix-multiply"):
    mlflow.log_param("N", N)
    mlflow.log_param("blocks", BLOCKS)
    t0 = time.time()
    result = sc.parallelize(blocks, BLOCKS).map(lambda ob: (ob[0], ob[1] @ B_bc.value)).collect()
    C = np.vstack([blk for _, blk in sorted(result, key=lambda x: x[0])])
    elapsed = time.time() - t0
    mlflow.log_metric("elapsed_seconds", elapsed)
    mlflow.log_metric("c_trace", float(np.trace(C)))
    mlflow.log_metric("gflops", (2.0 * N ** 3 / 1e9) / max(elapsed, 1e-9))
    print(f"{N}x{N} multiply done in {elapsed:.2f}s - metrics logged to MLflow")

spark.stop()
