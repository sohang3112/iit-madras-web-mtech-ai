"""Ray Data: generate -> filter -> map -> aggregate -> write Parquet."""
import os, ray
ray.init(address="auto")

ds = ray.data.range(10_000)
even = ds.filter(lambda row: row["id"] % 2 == 0)
squared = even.map(lambda row: {"id": row["id"], "sq": row["id"] * row["id"]})
stats = squared.aggregate(
    ray.data.aggregate.Mean("sq"),
    ray.data.aggregate.Max("sq"),
)
print("stats:", stats)

out = f"/storage/runs/{__STUDENT_USERNAME}/{__JOB_NAME}/"
os.makedirs(out, exist_ok=True)
squared.write_parquet(out)
print("wrote parquet under", out)
