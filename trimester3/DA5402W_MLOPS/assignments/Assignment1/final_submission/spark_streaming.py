from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import DoubleType, LongType, StringType, StructField, StructType
from pyspark.sql.window import Window

session = (
    SparkSession.builder.appName("SensorStreamingPipeline")
    .config("spark.sql.streaming.schemaInference", "true")
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
    .config(
        # FINALLY THIS JAR WORKS!!!
        "spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.2"
    )
    .getOrCreate()
)

schema = StructType(
    [
        StructField("sensor_id", StringType(), False),
        StructField("temperature", DoubleType(), True),
        StructField("timestamp", StringType(), False),
        StructField("status", StringType(), False),
    ]
)

kafka_site = "localhost:9092"
topic = "sensor_DA25M622"
raw_df = (
    session.readStream.format("kafka")
    .option("kafka.bootstrap.servers", kafka_site)
    .option("subscribe", topic)
    .option("startingOffsets", "earliest")
    .load()
)

# parsed df according to schema
parsed_json_df = raw_df.select(
    F.from_json(F.col("value").cast(F.StringType()), schema).alias("data")
).select("data.*")
parsed_json_df.printSchema()

# timestamps: parse from strings
parsed_timestamps_df = (
    # .cast() would raise error on invalid string
    parsed_json_df.withColumn("timestamp", F.col("timestamp").try_cast("timestamp"))  # .try_cast() returns null on invalid string so we filter it out
    .filter(F.col("timestamp").isNotNull())  
)

# using 25.0 as default temperature for missing values
df = parsed_timestamps_df.withColumn(
    "temperature",
    F.when(F.col("temperature").isNull(), 25.0).otherwise(F.col("temperature"))
)

df = df.dropDuplicates(["sensor_id", "timestamp"])
df = df.filter((F.col("temperature") > -20) & (F.col("temperature") < 100))
df = df.withColumn("hour", F.hour(F.col("timestamp")))
df = df.withColumn("day_of_week", F.dayofweek(F.col("timestamp")))
df = df.withColumn("is_weekend", F.when(F.col("day_of_week").isin([1, 7]), True).otherwise(False))

# streaming statistics
watermarked = df.withWatermark("timestamp", "1 second")
avg_temp_per_sensor = watermarked.groupBy("sensor_id").agg(
    F.avg("temperature").alias("avg_temperature")
)
max_temp_per_sensor = watermarked.groupBy("sensor_id").agg(
    F.max("temperature").alias("max_temperature")
)
active_sensors = (
    watermarked.withColumn("window_time", F.window(F.col("timestamp"), "5 minutes"))
    .groupBy("window_time")
    .agg(F.count(F.col("sensor_id")).alias("active_sensor_count"))
)
status_distribution = watermarked.groupBy("status").agg(F.count("*").alias("count"))

# avg, tumbling window, 5 minutes, watermark also 5 minutes
windowed_avg = (
    df.withWatermark("timestamp", "5 minutes")
    .groupBy(
        F.window(F.col("timestamp"), "5 minutes"), F.col("sensor_id")
    )
    .agg(F.avg("temperature").alias("window_avg_temperature"))
)

def query_show(df):
    query = (
        df.writeStream
        .format("console")
        #.outputMode("append")        
        .outputMode("update")      # show output as soon as it arrives, for groupby since with append, error: Invalid streaming output mode: append. This output mode is not supported for streaming aggregations without watermark on streaming DataFrames/DataSets. 
        #.trigger(processingTime="2 seconds") 
        .trigger(availableNow=True)    # process only data currently available (2000 records in kafka), then close stream
        .start()
    )
    query.awaitTermination()
    return query

print("Avg temperature per sensor:")
_ = query_show(avg_temp_per_sensor)
print("Max temperature per sensor:")
_ = query_show(max_temp_per_sensor)
print("Active sensors:")
_ = query_show(active_sensors)
print("Status distribution:")
_ = query_show(status_distribution)
print("Windowed average temperature:")
_ = query_show(windowed_avg)

