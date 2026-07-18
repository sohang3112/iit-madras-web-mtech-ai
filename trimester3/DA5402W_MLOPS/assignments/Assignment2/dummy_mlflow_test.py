import os
import mlflow
from mlflow.tracking import MlflowClient
import tempfile

# Respect existing env var, default to local MLflow server UI commonly at http://127.0.0.1:5000
TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
print("Using MLflow tracking URI:", TRACKING_URI)
mlflow.set_tracking_uri(TRACKING_URI)

EXPERIMENT_NAME = "mlflow_dummy_test"
mlflow.set_experiment(EXPERIMENT_NAME)

client = MlflowClient(tracking_uri=TRACKING_URI)
exp = client.get_experiment_by_name(EXPERIMENT_NAME)
print("Experiment id:", exp.experiment_id)

with mlflow.start_run(run_name="dummy-run") as run:
    run_id = run.info.run_id
    print("Started run:", run_id)
    mlflow.log_param("param1", "value1")
    mlflow.log_metric("metric1", 0.42)

    # log a small artifact
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("hello mlflow\n")
        artifact_path = f.name

    mlflow.log_artifact(artifact_path, artifact_path="artifacts")

# fetch run data back from server
run_data = client.get_run(run_id)
print("Logged params:", run_data.data.params)
print("Logged metrics:", run_data.data.metrics)
print("Logged artifacts:")
for a in client.list_artifacts(run_id, path="artifacts"):
    print(" -", a.path)

print("Done")
