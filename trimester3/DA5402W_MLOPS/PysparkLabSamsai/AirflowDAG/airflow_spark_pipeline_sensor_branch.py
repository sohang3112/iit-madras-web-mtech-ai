"""Sample (Airflow + Spark): a realistic data pipeline on the cluster.

    generate_data >> wait_for_data >> check_quality
    check_quality -> run_spark_job -> done   (enough rows)
    check_quality -> flag_bad_data -> done   (too few rows)

Concepts shown:
  * generate synthetic data in-DAG (no external download)
  * a SENSOR that waits until the data exists (PythonSensor; FileSensor is the
    file-specific variant, but it needs an 'fs_default' Airflow connection)
  * @task.branch -- a data-quality gate that picks the next step
  * REAL cluster Spark via  docker exec spark-master spark-submit  (platform pattern)
  * trigger_rule="all_done" -- converge no matter which branch ran
"""
import os
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.sensors.python import PythonSensor

# The worker writes here; spark-master sees the same files under /opt/spark/code.
HOST_DIR = "/opt/spark-platform/code/student_demo/__STUDENT_DAG_ID__"
SPARK_DIR = "/opt/spark/code/student_demo/__STUDENT_DAG_ID__"
DATA_FILE = "trips.csv"
JOB_FILE = "process_trips.py"
MIN_ROWS = 100_000

SPARK_JOB_SRC = """
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("taxi-hourly").getOrCreate()
df = spark.read.csv(sys.argv[1], header=True, inferSchema=True)
summary = (df.filter(F.col("fare") > 0)
             .groupBy("hour")
             .agg(F.count("*").alias("trips"), F.round(F.avg("fare"), 2).alias("avg_fare"))
             .orderBy("hour"))
print("=== Hourly trip summary ===")
summary.show(24)
spark.stop()
"""


def _data_ready():
    return os.path.exists(f"{HOST_DIR}/{DATA_FILE}")


with DAG(
    dag_id="__STUDENT_DAG_ID__",
    description="Airflow + Spark data pipeline (sensor + branch)",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    is_paused_upon_creation=False,
    tags=["student-ui", "spark", "pipeline"],
) as dag:

    @task(task_id="generate_data")
    def generate_data():
        import csv
        import random
        os.makedirs(HOST_DIR, exist_ok=True)
        rng = random.Random(42)
        rows = 200_000
        with open(f"{HOST_DIR}/{DATA_FILE}", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["hour", "fare"])
            for _ in range(rows):
                w.writerow([rng.randint(0, 23), round(rng.uniform(2.5, 80.0), 2)])
        with open(f"{HOST_DIR}/{JOB_FILE}", "w") as fh:
            fh.write(SPARK_JOB_SRC)
        print(f"generated {rows} rows -> {HOST_DIR}/{DATA_FILE}")

    wait_for_data = PythonSensor(
        task_id="wait_for_data",
        python_callable=_data_ready,
        poke_interval=5,
        timeout=120,
        mode="poke",
    )

    @task.branch(task_id="check_quality")
    def check_quality():
        with open(f"{HOST_DIR}/{DATA_FILE}") as fh:
            n = sum(1 for _ in fh) - 1
        print(f"row count = {n:,} (minimum {MIN_ROWS:,})")
        return "run_spark_job" if n >= MIN_ROWS else "flag_bad_data"

    run_spark_job = BashOperator(
        task_id="run_spark_job",
        bash_command=(
            "docker exec spark-master /opt/spark/bin/spark-submit "
            "--master spark://spark-master:7077 "
            f"{SPARK_DIR}/{JOB_FILE} {SPARK_DIR}/{DATA_FILE}"
        ),
    )

    @task(task_id="flag_bad_data")
    def flag_bad_data():
        print("Data-quality gate FAILED: too few rows. Halting pipeline.")

    @task(task_id="done", trigger_rule="all_done")
    def done():
        print("Pipeline complete.")

    gen = generate_data()
    branch = check_quality()
    bad = flag_bad_data()
    fin = done()

    gen >> wait_for_data >> branch
    branch >> run_spark_job >> fin
    branch >> bad >> fin
