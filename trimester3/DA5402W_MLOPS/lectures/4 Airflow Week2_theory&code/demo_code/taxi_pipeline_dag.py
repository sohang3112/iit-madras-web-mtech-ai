from datetime import datetime
from airflow.sdk import DAG, task

DATA_DIR    = "/home/alka/MLOPs-Class/spark_demo/taxi_data"
OUTPUT_DIR  = "/tmp/taxi_pipeline"
DATA_GLOB   = f"{DATA_DIR}/yellow_tripdata_202*.parquet"


def _get_spark(app_name: str):
    from pyspark.sql import SparkSession
    return (
        SparkSession.builder
        .appName("apache airflow taxi pipeline - " + app_name)
        .master("local[*]")
        .config("spark.driver.memory", "2g")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )


ALERT_FILE = f"{OUTPUT_DIR}/pipeline_alerts.txt"

def notify_failure(context):
    import os
    ti  = context["task_instance"]
    msg = (
        f"[ALERT] Task '{ti.task_id}' in DAG '{ti.dag_id}' FAILED\n"
        f"        Run: {context['run_id']}\n"
    )
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(ALERT_FILE, "a") as f:
        f.write(msg)
    print(msg)


# ──────────────────────────────────────────────────────────────────────────────
with DAG(
    dag_id="taxi_pyspark_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,          # trigger manually from UI
    catchup=False,
    tags=["pyspark", "taxi"],
) as dag:

    # ── Task 1: Ingest ────────────────────────────────────────────────────────
    # Validate files exist and return basic row count + column list.
    # Downstream tasks receive these via XCom so they know what to expect.
    @task(on_failure_callback=notify_failure)
    def ingest_data() -> dict:
        import glob
        from pyspark.sql import functions as F

        files = sorted(glob.glob(DATA_GLOB))
        if not files:
            raise FileNotFoundError(f"No parquet files found at: {DATA_GLOB}")

        spark = _get_spark("taxi_ingest")
        sdf   = spark.read.parquet(DATA_GLOB)

        row_count = sdf.count()
        columns   = sdf.columns

        print(f"Files found     : {len(files)}")
        print(f"Total rows      : {row_count:,}")
        print(f"Columns ({len(columns)}): {columns}")
        sdf.printSchema()

        spark.stop()
        return {"row_count": row_count, "files": files, "columns": columns}

    # ── Task 2: Clean ─────────────────────────────────────────────────────────
    # Drop nulls on key columns, remove nonsensical values, filter to valid
    # credit-card trips (payment_type == 1 → tips are real).
    # Saves cleaned parquet to OUTPUT_DIR/cleaned/.
    @task(on_failure_callback=notify_failure)
    def clean_data(ingest_result: dict) -> dict:
        import os
        from pyspark.sql import functions as F

        out_path = f"{OUTPUT_DIR}/cleaned"
        os.makedirs(out_path, exist_ok=True)

        spark = _get_spark("taxi_clean")
        sdf   = spark.read.parquet(DATA_GLOB)

        raw_count = ingest_result["row_count"]

        sdf_clean = (
            sdf
            .dropna(subset=["fare_amount", "trip_distance", "passenger_count",
                            "tpep_pickup_datetime", "tpep_dropoff_datetime"])
            .filter(F.col("fare_amount")     > 0)
            .filter(F.col("trip_distance")   > 0)
            .filter(F.col("passenger_count") > 0)
            .filter(F.col("passenger_count") <= 6)
            # keep only credit-card trips so tip_amount is meaningful
            .filter(F.col("payment_type") == 1)
        )

        clean_count = sdf_clean.count()
        dropped     = raw_count - clean_count

        print(f"Raw rows    : {raw_count:,}")
        print(f"Clean rows  : {clean_count:,}")
        print(f"Dropped     : {dropped:,}  ({dropped/raw_count*100:.1f}%)")

        sdf_clean.write.mode("overwrite").parquet(out_path)
        print(f"Saved cleaned data → {out_path}")

        spark.stop()
        return {"clean_count": clean_count, "clean_path": out_path}

    # ── Task 3: Feature engineering ───────────────────────────────────────────
    # Add derived columns useful for analysis or downstream ML:
    #   trip_duration_min, hour_of_day, day_of_week, is_airport, tip_pct
    @task(on_failure_callback=notify_failure)
    def feature_engineering(clean_result: dict) -> dict:
        import os
        from pyspark.sql import functions as F

        out_path = f"{OUTPUT_DIR}/features"
        os.makedirs(out_path, exist_ok=True)

        spark = _get_spark("taxi_features")
        sdf   = spark.read.parquet(clean_result["clean_path"])

        sdf_feat = (
            sdf
            .withColumn(
                "trip_duration_min",
                (F.unix_timestamp("tpep_dropoff_datetime")
                 - F.unix_timestamp("tpep_pickup_datetime")) / 60
            )
            .withColumn("hour_of_day",  F.hour("tpep_pickup_datetime"))
            .withColumn("day_of_week",  F.dayofweek("tpep_pickup_datetime"))  # 1=Sun … 7=Sat
            .withColumn("year",         F.year("tpep_pickup_datetime"))
            # RatecodeID 2 = JFK airport, 3 = Newark airport
            .withColumn("is_airport",   F.col("RatecodeID").isin([2, 3]).cast("int"))
            .withColumn(
                "tip_pct",
                F.round(F.col("tip_amount") / F.col("fare_amount") * 100, 2)
            )
            # drop trips with negative or impossibly long durations
            .filter(F.col("trip_duration_min").between(1, 180))
        )

        feat_count = sdf_feat.count()
        print(f"Feature rows : {feat_count:,}")
        print("Sample:")
        sdf_feat.select(
            "year", "hour_of_day", "day_of_week", "trip_duration_min",
            "trip_distance", "fare_amount", "tip_amount", "tip_pct", "is_airport"
        ).show(5, truncate=False)

        sdf_feat.write.mode("overwrite").parquet(out_path)
        print(f"Saved features → {out_path}")

        spark.stop()
        return {"feat_count": feat_count, "feat_path": out_path}

    # ── Task 4: Aggregate stats ───────────────────────────────────────────────
    # Year-over-year summary: trip volume, avg fare, avg distance, avg tip %.
    # Mirrors the YoY analysis in pyspark_demo_with_taxi_data.ipynb.
    @task(on_failure_callback=notify_failure)
    def aggregate_stats(feat_result: dict) -> dict:
        import os
        from pyspark.sql import functions as F

        out_path = f"{OUTPUT_DIR}/stats"
        os.makedirs(out_path, exist_ok=True)

        spark = _get_spark("taxi_stats")
        sdf   = spark.read.parquet(feat_result["feat_path"])

        yoy = (
            sdf
            .groupBy("year")
            .agg(
                F.count("*")                          .alias("total_trips"),
                F.round(F.avg("fare_amount"),    2)   .alias("avg_fare"),
                F.round(F.avg("trip_distance"),  2)   .alias("avg_distance_mi"),
                F.round(F.avg("tip_amount"),     2)   .alias("avg_tip"),
                F.round(F.avg("tip_pct"),        2)   .alias("avg_tip_pct"),
                F.round(F.avg("trip_duration_min"), 2).alias("avg_duration_min"),
                F.round(F.sum("fare_amount"),    0)   .alias("total_revenue"),
            )
            .orderBy("year")
        )

        print("=== Year-over-Year Summary (credit-card trips) ===")
        yoy.show(truncate=False)

        # Hour-of-day breakdown (busiest hours)
        hourly = (
            sdf
            .groupBy("hour_of_day")
            .agg(F.count("*").alias("trips"), F.round(F.avg("tip_pct"), 2).alias("avg_tip_pct"))
            .orderBy("hour_of_day")
        )
        print("=== Hourly Trip Distribution ===")
        hourly.show(24, truncate=False)

        yoy.write.mode("overwrite").csv(f"{out_path}/yoy", header=True)
        hourly.write.mode("overwrite").csv(f"{out_path}/hourly", header=True)
        print(f"Saved stats → {out_path}")

        total_revenue = yoy.agg(F.sum("total_revenue")).collect()[0][0]
        spark.stop()
        return {"stats_path": out_path, "total_revenue": float(total_revenue)}

    # ── Task 5: Write report ──────────────────────────────────────────────────
    # Summarise the pipeline run to a plain-text file — useful as a lightweight
    # audit trail when MLflow is not in the stack.
    @task()
    def write_report(ingest_result: dict, feat_result: dict, stats_result: dict) -> None:
        import os
        from datetime import datetime as dt

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        report_path = f"{OUTPUT_DIR}/pipeline_report.txt"

        lines = [
            "=" * 55,
            "  NYC TAXI PYSPARK PIPELINE — RUN REPORT",
            f"  {dt.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 55,
            f"  Files processed : {len(ingest_result['files'])}",
            f"  Raw rows        : {ingest_result['row_count']:,}",
            f"  Feature rows    : {feat_result['feat_count']:,}",
            f"  Total revenue   : ${stats_result['total_revenue']:,.0f}",
            f"  Stats saved to  : {stats_result['stats_path']}",
            "=" * 55,
        ]
        report = "\n".join(lines)
        print(report)

        with open(report_path, "w") as f:
            f.write(report + "\n")
        print(f"Report saved → {report_path}")

    # ── Wire up dependencies ──────────────────────────────────────────────────
    ingest_result = ingest_data()
    clean_result  = clean_data(ingest_result)
    feat_result   = feature_engineering(clean_result)
    stats_result  = aggregate_stats(feat_result)
    write_report(ingest_result, feat_result, stats_result)
