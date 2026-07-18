"""Each Ray task logs a separate MLflow run to the student's experiment."""
import os, ray, random, time, mlflow
ray.init(address="auto")

# MLflow tracking + experiment name come from the prelude env vars set
# by student-ui — every Ray task inherits them via runtime_env.

@ray.remote
def trial(seed: int) -> dict:
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
    mlflow.set_experiment(os.environ.get("MLFLOW_EXPERIMENT_NAME", "student/default"))
    with mlflow.start_run(run_name=f"trial-{seed}"):
        random.seed(seed)
        lr = 10 ** random.uniform(-4, -1)
        epochs = random.choice([10, 20, 40])
        mlflow.log_params({"lr": lr, "epochs": epochs})
        for e in range(epochs):
            # fake training loop
            loss = (epochs - e) * (0.5 + random.random() * 0.1) / epochs
            mlflow.log_metric("loss", loss, step=e)
            time.sleep(0.01)
        mlflow.log_metric("final_loss", loss)
        return {"seed": seed, "lr": lr, "final_loss": loss}

results = ray.get([trial.remote(s) for s in range(6)])
for r in results:
    print(r)
print("MLflow UI:", os.environ.get("MLFLOW_TRACKING_URI"), "experiment:",
      os.environ.get("MLFLOW_EXPERIMENT_NAME"))
