"""Sample: count the primes below N with a parallel segmented sieve.

The range [0, N) is split into segments; each Spark task sieves its own segment
independently and returns a count. Increase N for a bigger crunch.
"""
from pyspark.sql import SparkSession

N = 10_000_000  # count primes below this

spark = SparkSession.builder.appName("prime-count").getOrCreate()


def count_primes(seg):
    import math
    lo, hi = seg
    if hi <= 2:
        return 0
    lo = max(lo, 2)
    size = hi - lo
    comp = bytearray(size)                  # comp[i] == 1  ->  (lo + i) is composite
    root = math.isqrt(hi - 1)
    base = bytearray([1]) * (root + 1)      # small sieve of base primes up to sqrt(hi)
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


step = max(N // 64, 1)
segments = [(lo, min(lo + step, N)) for lo in range(0, N, step)]
total = (spark.sparkContext.parallelize(segments, len(segments))
         .map(count_primes).reduce(lambda a, b: a + b))

print(f"Number of primes below {N:,}: {total}")

spark.stop()
