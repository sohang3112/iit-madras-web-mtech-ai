"""Sample: distributed N x N matrix multiply, C = A @ B.

A is split into row-blocks (one Spark task each); B is broadcast to every task,
which multiplies its block by B using NumPy/BLAS. The blocks are reassembled on
the driver. Increase N for a bigger multiply.
"""
import numpy as np
from pyspark.sql import SparkSession

N = 1000      # matrices are N x N
BLOCKS = 16   # row-blocks of A (degree of parallelism)

spark = SparkSession.builder.appName("matrix-multiply").getOrCreate()
sc = spark.sparkContext

rng = np.random.default_rng(42)
A = rng.standard_normal((N, N))
B = rng.standard_normal((N, N))
B_bc = sc.broadcast(B)

rows_per = (N + BLOCKS - 1) // BLOCKS
blocks = [(i * rows_per, A[i * rows_per:(i + 1) * rows_per]) for i in range(BLOCKS)]

result = (sc.parallelize(blocks, BLOCKS)
            .map(lambda ob: (ob[0], ob[1] @ B_bc.value))
            .collect())

C = np.vstack([blk for _, blk in sorted(result, key=lambda x: x[0])])
print(f"Computed C = A @ B for {N}x{N} matrices, distributed over {BLOCKS} blocks.")
print(f"C shape {C.shape}, C[0,0]={C[0,0]:.6f}, trace={np.trace(C):.4f}")
print("row 0 matches a direct NumPy multiply:", bool(np.allclose(C[0], A[0] @ B)))

spark.stop()
