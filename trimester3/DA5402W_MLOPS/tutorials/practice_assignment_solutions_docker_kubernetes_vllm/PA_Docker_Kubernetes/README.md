# Diabetes Prediction: Scikit-learn + Flask + Docker + Kubernetes

A small, end-to-end MLOps teaching example: train a Logistic Regression model
on the Pima Indians Diabetes dataset, serve it behind a Flask REST API,
containerize it with Docker, and deploy it to Kubernetes. The focus of this
assignment is **Docker and Kubernetes mechanics**, not model quality.

## Project structure

```
diabetes-mlops-assignment/
├── train.py              # Loads data, trains + evaluates the model, saves it with joblib
├── app.py                # Flask API: GET /health, POST /predict
├── requirements.txt      # pip dependencies (Python 3.11, no Conda)
├── Dockerfile             # Builds a self-contained image (trains the model at build time)
├── .dockerignore
├── k8s/
│   ├── deployment.yaml   # 2 replicas, resource requests/limits, probes
│   ├── service.yaml      # NodePort Service exposing the API
│   ├── configmap.yaml    # Non-sensitive config (LOG_LEVEL, MODEL_PATH, PORT)
│   └── secret.yaml       # Sensitive config (API_KEY)
├── data/                 # Dataset cache (created automatically)
├── model/                # Trained model + metrics (created automatically)
└── README.md
```

## Dataset

[Pima Indians Diabetes Dataset](https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv) — 768 samples, 8 numeric features, binary
`Outcome` label (1 = diabetic). `train.py` downloads and caches it
automatically under `data/` on first run — no manual download needed.

Features, in the exact order the model expects them:

| Field | Meaning |
|---|---|
| `Pregnancies` | Number of pregnancies |
| `Glucose` | Plasma glucose concentration |
| `BloodPressure` | Diastolic blood pressure (mm Hg) |
| `SkinThickness` | Triceps skin fold thickness (mm) |
| `Insulin` | 2-hour serum insulin (mu U/ml) |
| `BMI` | Body mass index |
| `DiabetesPedigreeFunction` | Diabetes pedigree function |
| `Age` | Age in years |

---

## 1. Run locally (no Docker)

Requires Python 3.11+.

```bash
cd diabetes-mlops-assignment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Train the model — downloads the dataset, cleans it, trains, evaluates,
# and writes model/model.joblib + model/metrics.json
python train.py
```

Expected console output includes accuracy/precision/recall/F1 and a
confusion matrix. On the default 80/20 split you should see roughly
0.75–0.80 accuracy — this is a small, noisy dataset, so treat these numbers
as illustrative rather than a target to chase.

Run the API:

```bash
export MODEL_PATH=model/model.joblib
python app.py
# Flask dev server listens on http://localhost:5000
```

Test it:

```bash
curl http://localhost:5000/health

curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
        "Pregnancies": 2,
        "Glucose": 130,
        "BloodPressure": 70,
        "SkinThickness": 25,
        "Insulin": 100,
        "BMI": 28.5,
        "DiabetesPedigreeFunction": 0.45,
        "Age": 33
      }'
```

If you set `API_KEY` in the environment before starting `app.py`, `/predict`
will require a matching `X-API-Key` header, e.g. `-H "X-API-Key: <value>"`.

---

## 2. Build and run with Docker

The model is trained **during the image build**, so the resulting image is
fully self-contained — no separate training step is needed at container
startup.

```bash
docker build -t diabetes-api:latest .

docker run --rm -p 5000:5000 \
  --cpus="0.5" --memory="512m" \
  -e LOG_LEVEL=INFO \
  -e API_KEY=my-secret-key \
  diabetes-api:latest
```

The `--cpus`/`--memory` flags mirror the resource limits used later in
Kubernetes, so you can sanity-check the container behaves under the same
constraints locally.

Test the same `curl` commands as above against `localhost:5000`.

Check the built-in Docker healthcheck:

```bash
docker ps    # STATUS column will show "healthy" once /health responds
```

---

## 3. Deploy to Kubernetes

`kind` (Kubernetes-in-Docker) is used here rather than `minikube` because its
control plane is a single lightweight container — important when each
student's login is capped at 2 CPU / 4GB, since `minikube`'s VM/control-plane
overhead alone can consume most of that budget. `kind` and `minikube` are
otherwise interchangeable for this exercise.

```bash
kind create cluster --name diabetes

# Load the already-built local image straight into the kind node — no
# registry push needed.
kind load docker-image diabetes-api:latest --name diabetes
```

Apply the manifests (ConfigMap and Secret first, since the Deployment
references them):

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check status:

```bash
kubectl get pods -l app=diabetes-api
kubectl get deployment diabetes-api
kubectl describe pod <pod-name>     # inspect probe results, resource usage
kubectl logs -l app=diabetes-api --tail=50
```

Access the API (kind doesn't expose NodePort on the host by default, so
port-forward is the simplest path):

```bash
kubectl port-forward svc/diabetes-api-service 8080:80

curl http://localhost:8080/health

curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me-super-secret-key" \
  -d '{
        "Pregnancies": 2, "Glucose": 130, "BloodPressure": 70,
        "SkinThickness": 25, "Insulin": 100, "BMI": 28.5,
        "DiabetesPedigreeFunction": 0.45, "Age": 33
      }'
```

(The `X-API-Key` value must match `API_KEY` in `k8s/secret.yaml` — change
both together if you edit the secret.)

<details>
<summary>Using minikube instead</summary>

```bash
minikube start --cpus=2 --memory=3200 --driver=docker
eval $(minikube docker-env)
docker build -t diabetes-api:latest .
kubectl apply -f k8s/
minikube service diabetes-api-service --url
```
</details>

### What to observe

- **Rolling replicas**: `kubectl get pods -l app=diabetes-api -w` — 2 pods
  come up independently; killing one (`kubectl delete pod <name>`) causes
  the Deployment controller to recreate it automatically.
- **Readiness gating**: a pod only receives traffic (shows up in
  `kubectl get endpoints diabetes-api-service`) once `/health` returns 200.
- **Resource limits**: `kubectl top pod -l app=diabetes-api` (requires
  metrics-server) shows usage staying within the 250m/256Mi requests and
  500m/512Mi limits configured in `deployment.yaml`.
- **Config/Secret separation**: `kubectl exec` into a pod and run
  `env | grep -E 'LOG_LEVEL|MODEL_PATH|API_KEY'` to see both sources land as
  plain environment variables, while only `API_KEY` came from a Secret.

### Cleanup

```bash
kubectl delete -f k8s/
kind delete cluster --name diabetes
```

---

## Resource sizing rationale

The whole exercise is scoped to run comfortably on a 2-core / 4GB Linux
machine:

- Each pod requests 250m CPU / 256Mi RAM and is capped at 500m CPU / 512Mi
  RAM — two replicas therefore request at most 500m CPU / 512Mi RAM total
  and can burst to 1 CPU / 1GiB, leaving headroom for the OS, Docker/kubelet,
  and the cluster's own control-plane components.
- Gunicorn runs with 2 workers × 2 threads — enough concurrency for a
  logistic-regression model (inference is microseconds) without paging under
  the 512Mi limit.
- The Docker image is `python:3.11-slim` (not the full `python:3.11`), and no
  Conda environment is used, to keep the image small and the build fast.

## Notes on the API design

- `POST /predict` validates that all 8 required fields are present and
  numeric, returning `400` with a descriptive error otherwise — a common
  pattern when the caller is not always a curated internal client.
- `GET /health` returns `503` if the model failed to load, so Kubernetes
  probes correctly mark the pod unready/unhealthy instead of routing traffic
  to a broken instance.
- The optional `API_KEY` check demonstrates why Secrets exist separately
  from ConfigMaps: `kubectl get configmap diabetes-api-config -o yaml` is
  plaintext by design, while `kubectl get secret diabetes-api-secret -o yaml`
  base64-encodes the value (still not encryption — enable encryption-at-rest
  or a secrets manager for real deployments).
