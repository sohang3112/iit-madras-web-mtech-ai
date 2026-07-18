from pathlib import Path
import mlflow

# BASE_DIR = Path(__file__).resolve().parent
# MLRUNS_DIR = BASE_DIR / "mlruns"
# MLRUNS_DIR.mkdir(parents=True, exist_ok=True)
# tracking_uri = MLRUNS_DIR.as_uri()

mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("DA25M622")