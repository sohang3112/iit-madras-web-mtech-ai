"""Template (a): PySpark word count (self-contained).

Counts words in an in-memory sample. Swap `text` for a read from
/opt/spark/data/... to process real input on the cluster.
"""
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("wordcount").getOrCreate()

text = [
    "the quick brown fox",
    "the lazy dog",
    "the fox jumps over the lazy dog",
]
counts = (
    spark.sparkContext.parallelize(text)
    .flatMap(lambda line: line.split())
    .map(lambda word: (word, 1))
    .reduceByKey(lambda a, b: a + b)
)

for word, n in sorted(counts.collect()):
    print(f"{word}\t{n}")

spark.stop()
