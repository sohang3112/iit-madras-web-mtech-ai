"""Sample: N decimal digits of Pi via the Chudnovsky series.

The series terms are independent, so the (factorial-heavy) terms are computed in
parallel across the cluster; the final sum + division happen on the driver at
full precision. Increase DIGITS for more precision.
"""
from decimal import Decimal, getcontext

from pyspark.sql import SparkSession

DIGITS = 2000             # decimal digits of Pi to compute
PREC = DIGITS + 20
TERMS = DIGITS // 14 + 2  # Chudnovsky adds ~14.18 digits per term

spark = SparkSession.builder.appName("pi-digits").getOrCreate()


def chudnovsky_term(k, prec=PREC):
    from decimal import Decimal, getcontext
    from math import factorial
    getcontext().prec = prec
    num = Decimal(factorial(6 * k)) * (Decimal(13591409) + Decimal(545140134) * k)
    den = Decimal(factorial(3 * k)) * Decimal(factorial(k)) ** 3 * Decimal(-262537412640768000) ** k
    return num / den


terms = spark.sparkContext.parallelize(range(TERMS), 16).map(chudnovsky_term).collect()

getcontext().prec = PREC
pi = (Decimal(426880) * Decimal(10005).sqrt()) / sum(terms)

print(f"Pi to {DIGITS} decimal digits (Chudnovsky, terms summed in parallel):")
print(str(pi)[:DIGITS + 2])

spark.stop()
