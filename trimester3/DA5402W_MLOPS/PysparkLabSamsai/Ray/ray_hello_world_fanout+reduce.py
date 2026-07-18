"""Ray hello world: fan-out 20 tiny tasks across the 3 workers, then reduce."""
import ray, os, time, random

ray.init(address="auto")

@ray.remote
def square(x: int) -> int:
    time.sleep(random.uniform(0.1, 0.4))
    return x * x

futures = [square.remote(i) for i in range(20)]
results = ray.get(futures)
total = sum(results)
print(f"sum of squares 0..19 = {total} (expected 2470)")

# /storage is mounted at the same path on every worker.
out_dir = f"/storage/runs/{__STUDENT_USERNAME}/{__JOB_NAME}/"
os.makedirs(out_dir, exist_ok=True)
with open(out_dir + "result.txt", "w") as f:
    f.write(f"sum_of_squares={total}\n")
print("wrote", out_dir + "result.txt")
