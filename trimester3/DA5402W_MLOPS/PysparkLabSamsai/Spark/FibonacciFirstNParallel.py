"""Sample: the first N Fibonacci numbers, computed in parallel.

Each F(i) is computed independently with fast-doubling (O(log i)), so the work
spreads across the Spark cluster. Increase N for much bigger numbers.
"""
from pyspark.sql import SparkSession

N = 10000  # compute F(0) .. F(N-1)

spark = SparkSession.builder.appName("fibonacci").getOrCreate()


def fib(n):
    def fd(k):
        if k == 0:
            return (0, 1)
        a, b = fd(k >> 1)
        c = a * ((b << 1) - a)
        d = a * a + b * b
        return (d, c + d) if (k & 1) else (c, d)
    return fd(n)[0]


fibs = spark.sparkContext.parallelize(range(N), 16).map(lambda i: (i, fib(i)))
max_digits = fibs.map(lambda t: len(str(t[1]))).max()

print(f"Computed F(0)..F({N-1}) across the cluster.")
print(f"Largest term F({N-1}) has {max_digits} digits.")
for i in (10, 20, 50, 100, 500):
    print(f"F({i}) = {fib(i)}")

spark.stop()
