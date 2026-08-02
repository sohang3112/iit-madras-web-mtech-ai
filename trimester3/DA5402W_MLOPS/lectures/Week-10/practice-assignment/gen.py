from pathlib import Path

import nbformat as nbf


# Paths are relative to the directory from which this generator is run.
OUTPUT_FILE = Path("./practice_assignment_orchestration_deployment_solved.ipynb")


def md(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text):
    return nbf.v4.new_code_cell(text.strip())


cells = [
    md(r"""
# Practice Assignment 9 — ML Application Orchestration and Deployment

## Context

This assignment uses a local sentiment-analysis application. All required
application, Docker, and Kubernetes files are stored directly in this same
working directory.

## Learning Outcomes

After completing this notebook, you should be able to:

1. Explain the lifecycle of an ML inference API.
2. Test FastAPI health and prediction endpoints.
3. Build, inspect, and run a Docker image.
4. Explain Dockerfile instructions and container health checks.
5. Read Kubernetes Namespaces, ConfigMaps, Deployments, Services, PVs, and PVCs.
6. Deploy and inspect an ML service with `kubectl`.
7. Explain startup, readiness, and liveness probes.
8. Explain how an HPA scales a deployment.

Attempt every TODO before consulting the Week 9 lecture material.
"""),
    md(r"""
## Setup

Run this notebook from any directory. The setup cell creates all required
files in the notebook's current working directory (`./`).

### Google Colab

Run cells from top to bottom, one cell at a time. In Colab, the current
directory is usually `/content`. Docker and Kubernetes are represented by
notebook-only validation cells because standard Colab does not provide those
services.
"""),
    code(r"""
# Colab/local setup: run this cell first.
%pip -q install pyyaml fastapi pydantic uvicorn httpx

from pathlib import Path
import yaml

APP_DIR = Path.cwd()
files = {
    "app_main.py": '''from fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\n\napp = FastAPI(title="ML Sentiment API")\nready = True\n\nclass PredictRequest(BaseModel):\n    texts: list[str]\n\n@app.get("/health")\ndef health():\n    if not ready:\n        raise HTTPException(status_code=503, detail="model not ready")\n    return {"status": "ok", "model": "mock-sentiment-model"}\n\n@app.post("/predict")\ndef predict(req: PredictRequest):\n    if not ready:\n        raise HTTPException(status_code=503, detail="model not loaded")\n    return {"predictions": [{"text": text, "label": "POSITIVE" if any(w in text.lower() for w in ("love", "good", "great")) else "NEGATIVE", "score": 0.99} for text in req.texts]}\n''',
    "Dockerfile": 'FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY app_main.py .\nEXPOSE 8000\nCMD ["uvicorn", "app_main:app", "--host", "0.0.0.0", "--port", "8000"]\n',
    "requirements.txt": "fastapi\nuvicorn\npydantic\n",
    "k8s_namespace.yaml": "apiVersion: v1\nkind: Namespace\nmetadata:\n  name: ml-app\n",
    "k8s_configmap.yaml": "apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: ml-app-config\n  namespace: ml-app\ndata:\n  MODEL_NAME: mock-sentiment-model\n",
    "k8s_pv.yaml": "apiVersion: v1\nkind: PersistentVolume\nmetadata:\n  name: ml-app-model-cache-pv\nspec:\n  capacity:\n    storage: 5Gi\n  accessModes: [ReadWriteOnce]\n---\napiVersion: v1\nkind: PersistentVolumeClaim\nmetadata:\n  name: ml-app-model-cache-pvc\n  namespace: ml-app\nspec:\n  accessModes: [ReadWriteOnce]\n  resources:\n    requests:\n      storage: 5Gi\n",
    "k8s_deployment.yaml": "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: ml-app\n  namespace: ml-app\nspec:\n  replicas: 2\n  selector:\n    matchLabels: {app: ml-app}\n  template:\n    metadata:\n      labels: {app: ml-app}\n    spec:\n      containers:\n      - name: sentiment-api\n        image: sentiment-api:week9\n        ports: [{containerPort: 8000}]\n        envFrom: [{configMapRef: {name: ml-app-config}}]\n        resources:\n          requests: {cpu: 1, memory: 512Mi}\n          limits: {cpu: 2, memory: 1Gi}\n        startupProbe: {httpGet: {path: /health, port: 8000}}\n        readinessProbe: {httpGet: {path: /health, port: 8000}}\n        livenessProbe: {httpGet: {path: /health, port: 8000}}\n",
    "k8s_service.yaml": "apiVersion: v1\nkind: Service\nmetadata:\n  name: ml-app\n  namespace: ml-app\nspec:\n  selector: {app: ml-app}\n  ports: [{port: 80, targetPort: 8000}]\n",
    "k8s_hpa.yaml": "apiVersion: autoscaling/v2\nkind: HorizontalPodAutoscaler\nmetadata:\n  name: ml-app\n  namespace: ml-app\nspec:\n  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: ml-app}\n  minReplicas: 2\n  maxReplicas: 8\n  metrics: [{type: Resource, resource: {name: cpu, target: {type: Utilization, averageUtilization: 70}}}]\n",
}
for filename, content in files.items():
    (APP_DIR / filename).write_text(content)
print("Created", len(files), "assignment files in", APP_DIR.resolve())
"""),
    md(r"""
# Part 1 — Understand the FastAPI Application

## Task 1: Inspect the API contract

Read `app_main.py` and identify the model name, request schema, response
schema, and the behavior of `/health` and `/predict`. Explain why model loading
is placed in the FastAPI lifespan rather than inside every request.
"""),
    code(r"""
print((APP_DIR / "app_main.py").read_text())
"""),
    md(r"""
## Task 2: Run and test the service locally

Start the service with Uvicorn, then test the health endpoint and send at least
two texts to `/predict`. Record one successful response and explain what a
503 response means before the model has finished loading.
"""),
    code(r"""
# TODO: Test the service without starting a second terminal.
# Import the local FastAPI app and use TestClient for /health and /predict.
"""),
    md(r"""
# Part 2 — Containerize the ML Service

> Colab note: run the Python inspection cells normally. Docker commands are
> intentionally commented because a standard Colab runtime has no Docker
> daemon.

## Task 3: Explain the Dockerfile

Read the supplied `Dockerfile`. Explain the purpose of: the base image,
environment variables, `WORKDIR`, dependency installation, the non-root user,
model pre-download step, `EXPOSE`, `HEALTHCHECK`, and `CMD`.
"""),
    code(r"""
# TODO: Print the Dockerfile and annotate each important instruction.
"""),
    md(r"""
## Task 4: Build and run the image

Build the image as `sentiment-api:week9`, run it on host port 8000, and test
both endpoints. Inspect the image size and container logs. If Docker is not
available, write the commands and explain the expected result.
"""),
    code(r"""
# TODO: Validate the Dockerfile with Python. Do not run Docker commands in Colab.
"""),
    md(r"""
# Part 3 — Kubernetes Configuration

> Colab note: the YAML parsing cells run in Colab. `kubectl` commands are
> commented practice commands and require access to a Kubernetes cluster.

## Task 5: Parse and summarize manifests

Load every `k8s_*.yaml` manifest and create a table containing the filename,
Kubernetes kind, object name, and namespace. Explain why the
Namespace and ConfigMap are separate objects.
"""),
    code(r"""
for path in sorted(APP_DIR.glob("k8s_*.yaml")):
    for document in yaml.safe_load_all(path.read_text()):
        print(path.name, document.get("kind"), document.get("metadata", {}).get("name"),
              document.get("metadata", {}).get("namespace", "default"))
"""),
    md(r"""
## Task 6: Analyze the Deployment

Inspect `k8s_deployment.yaml`. Identify the desired replica count, container port,
image, environment source, CPU/memory requests and limits, probes, and mounted
volume. Explain how readiness differs from liveness and startup checks.
"""),
    code(r"""
deployment = yaml.safe_load((APP_DIR / "k8s_deployment.yaml").read_text())
spec = deployment["spec"]
container = spec["template"]["spec"]["containers"][0]
print("replicas:", spec["replicas"])
print("image:", container["image"])
print("ports:", container["ports"])
print("resources:", container["resources"])
print("probes:", {key: container[key] for key in ("startupProbe", "readinessProbe", "livenessProbe")})
"""),
    md(r"""
## Task 7: Deploy to Kubernetes

Apply the manifests in this order: namespace, ConfigMap, storage, Deployment,
Service, and HPA. Inspect pods, deployment rollout status, service details,
events, and logs. Port-forward the Service and test the API locally.
"""),
    code(r"""
# TODO: Simulate deployment by validating manifest relationships in Python.
"""),
    md(r"""
# Part 4 — Storage, Scaling, and Design Questions

## Task 8: Explain persistent storage

Describe the relationship between the PersistentVolume, PersistentVolumeClaim,
and Deployment volume mount. Discuss one limitation of the supplied `hostPath`
volume for a multi-node production cluster.
"""),
    code(r"""
# TODO: Answer the storage questions in your own words.
"""),
    md(r"""
## Task 9: Analyze autoscaling

Inspect `hpa.yaml`. State the minimum and maximum replicas, the target metric,
and the condition that causes scaling. Explain why CPU utilization may be an
imperfect proxy for inference latency or request throughput.
"""),
    code(r"""
hpa = yaml.safe_load((APP_DIR / "k8s_hpa.yaml").read_text())
print(hpa["spec"])
print("CPU alone may not represent latency, queue depth, or request throughput.")
"""),
    md(r"""
## Task 10: Troubleshooting and cleanup

For each symptom, give one diagnostic command and one likely cause:

1. The pod stays in `Running` but is not added to the Service endpoints.
2. The pod restarts repeatedly during model loading.
3. The HPA shows unknown CPU utilization.
4. The image builds but `/health` returns 503.

After testing, remove the local container and explain how you would remove the
Kubernetes resources without accidentally deleting shared cluster resources.
"""),
    code(r"""
# TODO: Provide commands and explanations for all four symptoms.
# TODO: Local cleanup example: docker stop sentiment-api
# TODO: Kubernetes cleanup example: kubectl delete -f k8s_hpa.yaml -f k8s_service.yaml -f k8s_deployment.yaml ...
"""),
    md(r"""
## Submission Checklist

- API contract and lifecycle explanation completed.
- Local or Docker endpoint tests documented.
- Dockerfile and Kubernetes manifests analyzed.
- Deployment, probes, storage, and HPA explained.
- Troubleshooting answers and cleanup commands included.
"""),
    md(r"""
# Solutions

Use this section only after attempting all TODO cells.
"""),
    md(r"""
## Solution 1 — API contract and lifecycle

`MODEL_NAME` is read from the environment and defaults to
`distilbert-base-uncased-finetuned-sst-2-english`. The lifespan handler loads
the Transformers sentiment pipeline once when the application starts. `/health`
returns 503 until loading completes; `/predict` accepts a non-empty list of
texts and returns one label and score per text. Loading at startup avoids
reloading the model for every request.
"""),
    code(r"""
print((APP_DIR / "app_main.py").read_text())
"""),
    md(r"""
## Solution 2 — Local and Docker testing

```bash
uvicorn app_main:app --host 0.0.0.0 --port 8000
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"texts":["I love this service", "This is terrible"]}'

docker build -t sentiment-api:week9 .
docker run --rm --name sentiment-api -p 8000:8000 sentiment-api:week9
docker images sentiment-api:week9
docker logs sentiment-api
```
"""),
    md(r"""
## Solution 3 — Manifest summary and deployment analysis

The Namespace isolates the application resources. The ConfigMap supplies
`MODEL_NAME` and `HF_HOME` without rebuilding the image. The Deployment runs
two replicas of `quay.io/ml-app/sentiment-api:latest`, exposes port 8000,
mounts the model-cache PVC, and requests 2 CPU/2 GiB while limiting each pod
to 4 CPU/4 GiB. Startup allows model loading time; readiness controls Service
traffic; liveness restarts an unhealthy container.
"""),
    code(r"""
for path in sorted(APP_DIR.glob("k8s_*.yaml")):
    document = yaml.safe_load(path.read_text())
    print(path.name, document.get("kind"), document.get("metadata", {}).get("name"),
          document.get("metadata", {}).get("namespace", "default"))
"""),
    md(r"""
## Solution 4 — Kubernetes deployment

```bash
kubectl apply -f k8s_namespace.yaml
kubectl apply -f k8s_configmap.yaml -f k8s_pv.yaml \
  -f k8s_deployment.yaml -f k8s_service.yaml -f k8s_hpa.yaml
kubectl -n ml-app get pods,svc,deploy,hpa,pvc
kubectl -n ml-app rollout status deployment/ml-app
kubectl -n ml-app logs deployment/ml-app
kubectl -n ml-app port-forward service/ml-app 8000:80
```

The PV provides storage, the PVC requests and binds that storage, and the
Deployment mounts it at `/app/models`. `hostPath` is node-local, so it is not a
portable production storage solution for pods scheduled on different nodes.
"""),
    md(r"""
## Solution 5 — HPA and troubleshooting

The HPA keeps between 2 and 8 replicas and targets average CPU utilization of
70% for the `ml-app` Deployment. CPU alone may not represent model latency,
queue depth, or request rate, so production scaling may need custom metrics.

- Not in Service endpoints: run `kubectl -n ml-app describe pod POD` and check selector labels and readiness probe events.
- Repeated restarts: run `kubectl -n ml-app logs POD --previous`; inspect memory limits and model-loading errors.
- Unknown HPA metric: run `kubectl top pods -n ml-app`; verify Metrics Server is installed.
- Health returns 503: inspect container logs; the model is still loading or failed to load.

Clean up only the named application resources:

```bash
kubectl delete -f k8s_hpa.yaml -f k8s_service.yaml -f k8s_deployment.yaml \
  -f k8s_configmap.yaml -f k8s_pv.yaml
kubectl delete namespace ml-app
```
"""),
]

# Put an answer immediately after each exercise's TODO cell. Commands that
# start services or change Docker/Kubernetes state stay commented for safety.
solutions = [
    """# Solution: inspect the local API implementation.\nprint((APP_DIR / \"app_main.py\").read_text())""",
    """# Solution: test the API in-process; no terminal or background server is needed.\nfrom fastapi.testclient import TestClient\nimport importlib.util\nspec = importlib.util.spec_from_file_location(\"app_main\", APP_DIR / \"app_main.py\")\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\nclient = TestClient(module.app)\nprint(client.get(\"/health\").json())\nprint(client.post(\"/predict\", json={\"texts\": [\"I love this\", \"This is terrible\"]}).json())""",
    """# Solution: inspect and explain the local Dockerfile.\nprint((APP_DIR / \"Dockerfile\").read_text())""",
    """# Solution: validate Dockerfile instructions without a Docker daemon.\ndockerfile = (APP_DIR / \"Dockerfile\").read_text().splitlines()\nrequired = [\"FROM\", \"WORKDIR\", \"COPY\", \"EXPOSE\", \"CMD\"]\nfor instruction in required:\n    assert any(line.startswith(instruction) for line in dockerfile), f\"Missing {instruction}\"\nprint(\"Dockerfile validation passed\")\n# Outside Colab, the equivalent commands would be:\n# docker build -t sentiment-api:week9 .\n# docker run --rm -p 8000:8000 sentiment-api:week9""",
    """# Solution: summarize all local Kubernetes manifests.\nfor path in sorted(APP_DIR.glob(\"k8s_*.yaml\")):\n    for document in yaml.safe_load_all(path.read_text()):\n        print(path.name, document.get(\"kind\"), document.get(\"metadata\", {}).get(\"name\"), document.get(\"metadata\", {}).get(\"namespace\", \"default\"))""",
    """# Solution: inspect replicas, image, resources, port, and probes.\ndeployment = yaml.safe_load((APP_DIR / \"k8s_deployment.yaml\").read_text())\nspec = deployment[\"spec\"]\ncontainer = spec[\"template\"][\"spec\"][\"containers\"][0]\nprint(\"replicas:\", spec[\"replicas\"])\nprint(\"image:\", container[\"image\"])\nprint(\"resources:\", container[\"resources\"])\nprint(\"startup:\", container[\"startupProbe\"])\nprint(\"readiness:\", container[\"readinessProbe\"])\nprint(\"liveness:\", container[\"livenessProbe\"])""",
    """# Solution: validate the deployment graph in Python.\ndef read_yaml(name):\n    return yaml.safe_load((APP_DIR / name).read_text())\nnamespace = read_yaml(\"k8s_namespace.yaml\")\nconfig = read_yaml(\"k8s_configmap.yaml\")\ndeployment = read_yaml(\"k8s_deployment.yaml\")\nservice = read_yaml(\"k8s_service.yaml\")\nhpa = read_yaml(\"k8s_hpa.yaml\")\nassert config[\"metadata\"][\"namespace\"] == namespace[\"metadata\"][\"name\"]\nassert deployment[\"spec\"][\"template\"][\"metadata\"][\"labels\"] == service[\"spec\"][\"selector\"]\nassert hpa[\"spec\"][\"scaleTargetRef\"][\"name\"] == deployment[\"metadata\"][\"name\"]\nprint(\"Kubernetes deployment simulation passed\")""",
    """# Solution: the PVC requests 5Gi from the PV and the Deployment mounts it at /app/models.\n# hostPath is node-local and is unsuitable for portable multi-node production storage.""",
    """# Solution: inspect HPA settings.\nhpa = yaml.safe_load((APP_DIR / \"k8s_hpa.yaml\").read_text())\nprint(hpa[\"spec\"])\n# It scales from 2 to 8 replicas when average CPU utilization exceeds 70%.""",
    """# Solution diagnostics:\n# kubectl -n ml-app describe pod POD\n# kubectl -n ml-app logs POD --previous\n# kubectl top pods -n ml-app\n# kubectl -n ml-app get events --sort-by=.lastTimestamp\n# docker stop sentiment-api\n# kubectl delete -f k8s_hpa.yaml -f k8s_service.yaml -f k8s_deployment.yaml -f k8s_configmap.yaml -f k8s_pv.yaml\n# kubectl delete namespace ml-app""",
]

expanded_cells = []
solution_index = 0
for cell in cells:
    expanded_cells.append(cell)
    if cell.cell_type == "code" and "TODO" in cell.source and solution_index < len(solutions):
        expanded_cells.append(md("## Solution"))
        expanded_cells.append(code(solutions[solution_index]))
        solution_index += 1
cells = expanded_cells

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT_FILE.open("w", encoding="utf-8") as handle:
    nbf.write(nb, handle)
print(f"Wrote {OUTPUT_FILE}")
