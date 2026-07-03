# pip install pyspark==4.1.2
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    col,
    count,
    dayofweek,
    from_json,
    from_unixtime,
    hour,
    isnan,
    isnull,
    row_number,
    to_timestamp,
    unix_timestamp,
    when,
    window,
)
from pyspark.sql.functions import max as spark_max
from pyspark.sql.functions import min as spark_min
from pyspark.sql.functions import sum as spark_sum
from pyspark.sql.types import DoubleType, LongType, StringType, StructField, StructType
from pyspark.sql.window import Window

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_spark_session():
    """Create Spark session with Kafka support."""
    return (
        SparkSession.builder.appName("SensorStreamingPipeline")
        .config("spark.sql.streaming.schemaInference", "true")
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
        .config(
            # "spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:4.1.2",
        )
        .getOrCreate()
    )


def define_schema():
    """Define schema for incoming Kafka records."""
    schema = StructType(
        [
            StructField("sensor_id", StringType(), False),
            StructField("temperature", DoubleType(), True),
            StructField("timestamp", StringType(), False),
            StructField("status", StringType(), False),
        ]
    )
    return schema


def read_from_kafka(spark, kafka_brokers="localhost:9092", topic="sensor_DA25M622"):
    """Read data from Kafka topic."""
    schema = define_schema()

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_brokers)
        .option("subscribe", topic)
        .option("startingOffsets", "latest")
        .load()
    )

    # Parse JSON from Kafka value
    df = df.select(
        from_json(col("value").cast(StringType()), schema).alias("data")
    ).select("data.*")

    return df


def print_schema_and_sample(df):
    """Print schema information."""
    logger.info("=" * 80)
    logger.info("SCHEMA:")
    df.printSchema()
    logger.info("=" * 80)
    return df


def convert_timestamps(df):
    """Convert timestamp strings to Spark Timestamp format."""
    df = df.withColumn(
        "timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
    )
    return df


def handle_invalid_records(df):
    """Identify and remove invalid records."""
    # Track invalid records
    invalid_temp_low = col("temperature") < -20
    invalid_temp_high = col("temperature") > 100
    invalid_timestamp = col("timestamp").isNull()

    # Log invalid records before filtering
    invalid_df = df.filter(invalid_temp_low | invalid_temp_high | invalid_timestamp)

    # Remove invalid records
    df_valid = df.filter(
        (col("temperature") >= -20)
        & (col("temperature") <= 100)
        & (~col("timestamp").isNull())
    )

    return df_valid, invalid_df


def remove_duplicates(df):
    """Remove duplicate records using sensor_id + timestamp natively."""
    # We must define a watermark so Spark knows how long to keep keys in memory
    df = df.withWatermark("timestamp", "10 minutes")
    # Native streaming deduplication
    df = df.dropDuplicates(["sensor_id", "timestamp"])
    return df


# def remove_duplicates(df):
#     """Remove duplicate records using sensor_id + timestamp."""
#     window_spec = Window.partitionBy("sensor_id", "timestamp").orderBy("timestamp")
#     df = df.withColumn("row_num", row_number().over(window_spec))
#     df = df.filter(col("row_num") == 1).drop("row_num")
#     return df


def handle_missing_values(df):
    """Handle missing temperature values safely for streaming."""
    # Option: Fill missing temperatures with a baseline default (e.g., 25.0)
    # Or simply skip this and drop if you cannot infer it without batch windows.
    df = df.withColumn(
        "temperature",
        when(col("temperature").isNull(), 25.0).otherwise(col("temperature")),
    )

    df = df.filter(col("temperature").isNotNull())
    return df


# def handle_missing_values(df):
#     """Handle missing temperature values using 5-minute window average."""
#     # Calculate average temperature per sensor over 5-minute window
#     window_spec = (
#         Window.partitionBy("sensor_id")
#         .orderBy(col("timestamp").cast(LongType()))
#         .rangeBetween(-300, 0)
#     )  # 5 minutes in seconds

#     avg_temp_5min = avg(col("temperature")).over(window_spec)

#     # Replace missing temperatures with window average or drop if no history
#     df = df.withColumn(
#         "temperature",
#         when(col("temperature").isNull(), avg_temp_5min).otherwise(col("temperature")),
#     )

#     # Drop records with still-missing temperatures (insufficient history)
#     df = df.filter(col("temperature").isNotNull())

#     return df


def create_features(df):
    """Create temporal features."""
    df = (
        df.withColumn("hour_of_day", hour(col("timestamp")))
        .withColumn("day_of_week", dayofweek(col("timestamp")))
        .withColumn(
            "is_weekend",
            when((col("day_of_week") == 1) | (col("day_of_week") == 7), 1).otherwise(0),
        )
    )

    return df


# def data_preprocessing(spark, df):
#     """Execute all preprocessing steps."""
#     logger.info("Starting data preprocessing...")

#     # Step 1-2: Print schema
#     df = print_schema_and_sample(df)

#     # Step 6: Convert timestamps
#     df = convert_timestamps(df)

#     # Step 5: Handle invalid records
#     df, invalid_df = handle_invalid_records(df)

#     # Step 4: Remove duplicates
#     df = remove_duplicates(df)

#     # Step 3: Handle missing values
#     df = handle_missing_values(df)

#     # Step 7: Create features
#     df = create_features(df)

#     logger.info("Data preprocessing completed.")
#     return df, invalid_df


def data_preprocessing(spark, df):
    logger.info("Starting data preprocessing...")

    # 1. Print schema
    df = print_schema_and_sample(df)

    # 2. Convert timestamps string -> Timestamp Type (CRITICAL to do first)
    df = convert_timestamps(df)

    # 3. Handle invalid records
    df, invalid_df = handle_invalid_records(df)

    # 4. Remove duplicates natively via dropDuplicates
    df = remove_duplicates(df)

    # 5. Handle missing values without analytical window functions
    df = handle_missing_values(df)

    # 6. Create features
    df = create_features(df)

    logger.info("Data preprocessing completed.")
    return df, invalid_df


def streaming_analytics(df):
    """Compute streaming analytics."""
    # Step 8: Average temperature per sensor
    avg_temp_per_sensor = df.groupBy("sensor_id").agg(
        avg("temperature").alias("avg_temperature")
    )

    # Step 9: Maximum temperature per sensor
    max_temp_per_sensor = df.groupBy("sensor_id").agg(
        spark_max("temperature").alias("max_temperature")
    )

    # Step 10: Active sensors in last 5 minutes
    active_sensors = (
        df.withColumn("window_time", window(col("timestamp"), "5 minutes"))
        .groupBy("window_time")
        .agg(count(col("sensor_id")).alias("active_sensor_count"))
    )

    # Step 11: Distribution of sensor status values
    status_distribution = df.groupBy("status").agg(count("*").alias("count"))

    return avg_temp_per_sensor, max_temp_per_sensor, active_sensors, status_distribution


def event_time_processing(df):
    """Implement 5-minute tumbling window with watermarking."""
    # Step 13: Apply watermarking (5 minutes delay)
    df_watermarked = df.withWatermark("timestamp", "5 minutes")

    # Step 12: 5-minute tumbling window with average temperature
    windowed_avg = df_watermarked.groupBy(
        window(col("timestamp"), "5 minutes"), col("sensor_id")
    ).agg(avg("temperature").alias("window_avg_temperature"))

    return windowed_avg, df_watermarked


def setup_query_metrics(spark):
    """Setup metrics tracking for performance analysis."""
    metrics = {
        "missing_values_corrected": 0,
        "duplicate_records_removed": 0,
        "invalid_records_removed": 0,
        "late_records_accepted": 0,
        "records_discarded": 0,
    }
    return metrics


def main():
    spark = create_spark_session()

    try:
        # Read from Kafka
        logger.info("Reading from Kafka topic: sensor_DA25M622")
        df = read_from_kafka(
            spark, kafka_brokers="localhost:9092", topic="sensor_DA25M622"
        )

        # Data Preprocessing
        df_processed, invalid_df = data_preprocessing(spark, df)

        # Streaming Analytics
        avg_temp, max_temp, active_sensors, status_dist = streaming_analytics(
            df_processed
        )

        # Event-Time Processing
        windowed_avg, df_watermarked = event_time_processing(df_processed)

        # Start streaming queries
        logger.info("Starting streaming queries...")

        # Query 1: Processed data with debug info
        query1 = (
            df_processed.writeStream.format("console")
            .option("numRows", 20)
            .option("truncate", False)
            .start()
        )

        # Query 2: Average temperature per sensor
        query2 = (
            avg_temp.writeStream.format("console")
            .option("numRows", 10)
            .trigger(processingTime="10 seconds")
            .start()
        )

        # Query 3: Max temperature per sensor
        query3 = (
            max_temp.writeStream.format("console")
            .option("numRows", 10)
            .trigger(processingTime="10 seconds")
            .start()
        )

        # Query 4: Active sensors
        query4 = (
            active_sensors.writeStream.format("console")
            .option("numRows", 10)
            .trigger(processingTime="10 seconds")
            .start()
        )

        # Query 5: Status distribution
        query5 = (
            status_dist.writeStream.format("console")
            .option("numRows", 10)
            .trigger(processingTime="10 seconds")
            .start()
        )

        # Query 6: Windowed averages
        query6 = (
            windowed_avg.writeStream.format("console")
            .option("numRows", 10)
            .trigger(processingTime="10 seconds")
            .start()
        )

        # Query 7: Invalid records monitoring
        query7 = (
            invalid_df.writeStream.format("console")
            .option("numRows", 5)
            .trigger(processingTime="10 seconds")
            .start()
        )

        logger.info("All queries started. Awaiting termination...")
        spark.streams.awaitAnyTermination()

    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
    finally:
        spark.stop()
        logger.info("Spark session stopped.")


if __name__ == "__main__":
    main()
