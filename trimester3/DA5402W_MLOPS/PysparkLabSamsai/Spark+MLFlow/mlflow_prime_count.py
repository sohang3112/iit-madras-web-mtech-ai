"""Sample (MLflow): count primes below N, logging params + metrics to MLflow.

Logs to experiment student/<your-username>; open the MLflow link afterwards.
"""
import os
import time

import mlflow
from pyspark.sql import SparkSession

N = 10_000_000

spark = SparkSession.builder.appName("mlflow-primes").getOrCreate()
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow-server:5000"))
mlflow.set_experiment(os.environ.get("MLFLOW_EXPERIMENT_NAME", "student/unknown"))


def count_primes(seg):
    import math
    lo, hi = seg
    if hi <= 2:
        return 0
    lo = max(lo, 2)
    size = hi - lo
    comp = bytearray(size)
    root = math.isqrt(hi - 1)
    base = bytearray([1]) * (root + 1)
    for p in range(2, math.isqrt(root) + 1):
        if base[p]:
            base[p * p::p] = bytes(len(base[p * p::p]))
    for p in range(2, root + 1):
        if not base[p]:
            continue
        start = max(p * p, ((lo + p - 1) // p) * p)
        if start < hi:
            comp[start - lo::p] = bytes([1]) * (((hi - 1 - start) // p) + 1)
    return size - sum(comp)


with mlflow.start_run(run_name="prime-count"):
    mlflow.log_param("N", N)
    mlflow.log_param("partitions", 64)
    t0 = time.time()
    step = max(N // 64, 1)
    segments = [(lo, min(lo + step, N)) for lo in range(0, N, step)]
    total = (spark.sparkContext.parallelize(segments, len(segments))
             .map(count_primes).reduce(lambda a, b: a + b))
    elapsed = time.time() - t0
    mlflow.log_metric("prime_count", total)
    mlflow.log_metric("elapsed_seconds", elapsed)
    print(f"primes below {N:,}: {total}  ({elapsed:.1f}s) - logged to MLflow")

spark.stop()
