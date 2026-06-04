"""Sample (Kafka + Spark Structured Streaming): word count from a Kafka topic.

Seeds the topic with a small batch first, then runs a structured-streaming
word-count with trigger(availableNow=True) so it processes everything currently
in the topic and exits — perfect for a finite demo run.
"""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BROKER = "kafka:29092"
TOPIC = "demo-spark-kafka"

spark = SparkSession.builder.appName("kafka-streaming-wc").getOrCreate()

# Seed a few messages so the demo always has something to count.
seed = (spark.range(50)
        .selectExpr("CAST(id AS STRING) AS key",
                    "CAST(CASE WHEN id % 3 = 0 THEN 'lorem ipsum dolor sit amet' "
                              "WHEN id % 3 = 1 THEN 'the quick brown fox jumps' "
                              "ELSE 'sed do eiusmod tempor incididunt' END AS STRING) AS value"))
seed.write.format("kafka").option("kafka.bootstrap.servers", BROKER).option("topic", TOPIC).save()
print(f"Seeded 50 messages into '{TOPIC}'")

# Structured-streaming source -> word count -> console sink.
stream = (spark.readStream.format("kafka")
          .option("kafka.bootstrap.servers", BROKER)
          .option("subscribe", TOPIC)
          .option("startingOffsets", "earliest")
          .load()
          .selectExpr("CAST(value AS STRING) AS line")
          .select(F.explode(F.split(F.col("line"), " ")).alias("word"))
          .filter(F.col("word") != "")
          .groupBy("word").count())

q = (stream.writeStream.format("console")
     .outputMode("complete")
     .trigger(availableNow=True)
     .start())
q.awaitTermination()
print("Streaming word count finished.")
spark.stop()
