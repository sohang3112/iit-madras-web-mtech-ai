"""Sample (Kafka + Spark): produce a batch of messages, then read them back.

Uses Spark's Kafka connector (auto-loaded via --packages in the generated DAG).
Each run tags its messages with a unique RUN_ID so the consumer can pick out
its own messages even on a shared demo topic.
"""
import uuid

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BROKER = "kafka:29092"
TOPIC = "demo-spark-kafka"
N = 1000
RUN_ID = uuid.uuid4().hex[:8]

spark = SparkSession.builder.appName("kafka-produce-consume").getOrCreate()

# Produce N (key, value) messages into the topic.
producer_df = (spark.range(N)
               .withColumn("key", F.concat(F.lit(RUN_ID + "-"), F.col("id").cast("string")))
               .withColumn("value", F.concat(F.lit("hello-"), F.col("id").cast("string")))
               .select(F.col("key").cast("string"), F.col("value").cast("string")))
(producer_df.write.format("kafka")
 .option("kafka.bootstrap.servers", BROKER)
 .option("topic", TOPIC)
 .save())
print(f"Produced {N} messages with key prefix '{RUN_ID}-' to topic '{TOPIC}'")

# Read everything in the topic, keep only this run's messages.
consumer_df = (spark.read.format("kafka")
               .option("kafka.bootstrap.servers", BROKER)
               .option("subscribe", TOPIC)
               .option("startingOffsets", "earliest")
               .load()
               .selectExpr("CAST(key AS STRING) AS key", "CAST(value AS STRING) AS value"))
mine = consumer_df.filter(F.col("key").startswith(RUN_ID + "-"))
print(f"Consumed back {mine.count()} messages tagged '{RUN_ID}':")
mine.show(5, truncate=False)

spark.stop()
