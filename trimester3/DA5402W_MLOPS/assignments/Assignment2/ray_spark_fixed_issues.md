I’m summarizing the failures from the run and the fixes that resolved each one so you have a concise reference.

## Summary of the failures and fixes

Here is a compact breakdown of what went wrong during the run, what should be avoided next time, and how each issue was resolved.

### 1. Ray/Spark memory over-allocation
- Failure: Ray workers were killed because the machine was running out of memory during tuning.
- Why it happened: The script launched multiple Ray trials and Spark jobs with relatively high memory settings, which overwhelmed the laptop.
- What not to do in future:
  - Don’t run multiple concurrent Ray trials on a small machine.
  - Don’t use large Spark executor/driver memory settings unless the system has enough RAM.
- How it was fixed:
  - Reduced Ray concurrency to one trial.
  - Limited Spark memory and parallelism.
  - Kept Spark to a single local executor.

### 2. Ray initialization rejected the requested memory configuration
- Failure: Ray raised a ValueError during startup because the requested object-store memory was too large for the node.
- Why it happened: The object-store size was set too aggressively for the available machine memory.
- What not to do in future:
  - Don’t force a large Ray object-store size on a small local machine.
- How it was fixed:
  - Switched to a minimal Ray startup configuration using one CPU and default-safe settings.

### 3. Spark Java heap / cache memory pressure
- Failure: Training crashed with Java OutOfMemoryError during Spark’s in-memory processing.
- Why it happened: The script cached DataFrames aggressively, and Spark tried to materialize large blocks in memory, causing Java heap exhaustion.
- What not to do in future:
  - Don’t call cache/persist on large DataFrames unless you really need it.
  - Don’t let Spark process large intermediate data with too many partitions.
- How it was fixed:
  - Removed the eager caching step.
  - Reduced Spark partitions and parallelism.
  - Read only the required columns.

### 4. Matplotlib warning in worker threads
- Failure: A warning appeared about starting a GUI backend outside the main thread.
- Why it happened: Matplotlib was being used inside Ray worker processes, which is not ideal.
- What not to do in future:
  - Don’t rely on interactive plotting inside distributed / worker-based training jobs.
- How it was fixed:
  - Kept Matplotlib in a non-GUI backend with Agg, which is safe for headless workers.

### 5. The run initially completed with zero metrics after worker failure
- Failure: The tuning run ended with F1/accuracy reported as 0.0 because the worker crashed before finishing.
- Why it happened: The worker exception path in the script reported fallback zeros when training failed.
- What not to do in future:
  - Don’t treat a failed trial as a successful one; inspect the traceback instead of trusting the fallback metrics.
- How it was fixed:
  - By fixing the memory and Spark issues, the worker completed normally and produced real metrics.

---

## Best practices to follow next time

- Start with the smallest possible resource configuration.
- Use single-worker / single-trial runs first when debugging.
- Avoid Spark caching unless necessary.
- Use headless plotting backends.
- Keep Ray and Spark parallelism low on laptops or personal machines.

## Final outcome
The script now runs successfully and produced:
- F1 score: 0.823575
- Accuracy: 0.879783

If you want, I can also turn this into a short “lessons learned” note for your assignment folder.