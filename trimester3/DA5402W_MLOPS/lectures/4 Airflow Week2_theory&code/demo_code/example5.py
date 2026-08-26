from datetime import datetime
import os

from airflow.sdk import DAG, task
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.providers.standard.operators.bash import BashOperator

DATA_FILE  = "/home/alka/MLOPs-Class/spark_demo/yellow_tripdata_2027-01.parquet"
OUTPUT_DIR = "/tmp/taxi_sensor_demo"

# ══════════════════════════════════════════════════════════════════════════════
# DAG 1: FileSensor — wait for data to arrive before processing
#
# Flow:
#   wait_for_data (FileSensor)
#       └── check_row_count (@task.branch)
#               ├── [enough rows]  process_data → write_output ──┐
#               └── [too few rows] flag_bad_data                 │
#                                                        pipeline_done (all_done)
#
# Key concepts:
#   FileSensor   — blocks until a file exists, then releases the pipeline
#   @task.branch — runs one downstream path based on a condition
#   trigger_rule='all_done' — pipeline_done runs regardless of which branch ran
# ══════════════════════════════════════════════════════════════════════════════
with DAG(
    dag_id="sensor_and_branch_demo",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["example", "sensor", "branch"],
) as dag:

    # ── Sensor ────────────────────────────────────────────────────────────────
    # Polls every 10 s, times out after 2 min.
    # In production this would wait for an S3 key, an SFTP drop, etc.
    # run below command once :
    #  airflow connections add fs_default \
    #--conn-type fs \
    #--conn-extra '{"path": "/"}'

    wait_for_data = FileSensor(
        task_id="wait_for_data",
        filepath=DATA_FILE,
        poke_interval=10,    # check every 10 seconds
        timeout=120,         # give up after 2 minutes
        mode="poke",         # keep the worker slot while waiting
    )

    # ── Branch ────────────────────────────────────────────────────────────────
    # Returns the task_id of whichever branch should run next.
    # Airflow skips all other downstream tasks not on the chosen path.
    @task.branch()
    def check_row_count() -> str:
        from pyspark.sql import SparkSession

        spark = (
            SparkSession.builder
            .appName("taxi_branch_check")
            .master("local[*]")
            .config("spark.driver.memory", "1g")
            .getOrCreate()
        )
        sdf   = spark.read.parquet(DATA_FILE)
        count = sdf.count()
        spark.stop()

        MIN_ROWS = 1_000_000
        print(f"Row count: {count:,}  (minimum expected: {MIN_ROWS:,})")

        if count >= MIN_ROWS:
            print("Quality check PASSED → routing to process_data")
            return "process_data"
        else:
            print("Quality check FAILED → routing to flag_bad_data")
            return "flag_bad_data"

    # ── Happy path ────────────────────────────────────────────────────────────
    @task(task_id="process_data")
    def process_data():
        from pyspark.sql import SparkSession
        from pyspark.sql import functions as F

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        spark = (
            SparkSession.builder
            .appName("taxi_process")
            .master("local[*]")
            .config("spark.driver.memory", "1g")
            .getOrCreate()
        )
        sdf = spark.read.parquet(DATA_FILE)

        result = (
            sdf
            .filter(F.col("fare_amount") > 0)
            .groupBy(F.hour("tpep_pickup_datetime").alias("hour"))
            .agg(
                F.count("*").alias("trips"),
                F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
            )
            .orderBy("hour")
        )
        print("=== Hourly Trip Summary ===")
        result.show(24)

        result.write.mode("overwrite").csv(f"{OUTPUT_DIR}/hourly_summary", header=True)
        print(f"Saved → {OUTPUT_DIR}/hourly_summary")
        spark.stop()

    @task(task_id="write_output")
    def write_output():
        report = f"{OUTPUT_DIR}/report.txt"
        with open(report, "w") as f:
            f.write(f"Pipeline completed at {datetime.now()}\n")
            f.write(f"Output: {OUTPUT_DIR}/hourly_summary\n")
        print(f"Report written → {report}")

    # ── Sad path ──────────────────────────────────────────────────────────────
    @task(task_id="flag_bad_data")
    def flag_bad_data():
        alert = f"{OUTPUT_DIR}/data_quality_alert.txt"
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        msg = f"[ALERT] {DATA_FILE} has fewer rows than expected. Pipeline halted.\n"
        with open(alert, "a") as f:
            f.write(msg)
        print(msg)

    # ── Converge ──────────────────────────────────────────────────────────────
    # trigger_rule='all_done' → runs after whichever branch completed,
    # whether it succeeded, failed, or was skipped.
    @task(task_id="pipeline_done", trigger_rule="all_done")
    def pipeline_done():
        print("Pipeline finished — sensor + branch demo complete.")

    # ── Wire up ───────────────────────────────────────────────────────────────
    branch        = check_row_count()
    process       = process_data()
    output        = write_output()
    bad_data      = flag_bad_data()
    done          = pipeline_done()

    wait_for_data >> branch
    branch >> process >> output >> done
    branch >> bad_data >> done
