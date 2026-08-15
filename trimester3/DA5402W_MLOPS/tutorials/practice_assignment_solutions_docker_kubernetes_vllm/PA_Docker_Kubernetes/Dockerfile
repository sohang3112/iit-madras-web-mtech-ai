# syntax=docker/dockerfile:1

# Python 3.11 slim image, pip + requirements.txt only (no Conda), kept small
# on purpose since the target host is constrained to 2 CPU cores / 4GB RAM.
FROM python:3.11-slim

# Prevent .pyc files and force stdout/stderr to be unbuffered so logs show up
# immediately with `kubectl logs` / `docker logs`.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/model/model.joblib \
    DATA_PATH=/app/data/pima-indians-diabetes.csv \
    PORT=5000

WORKDIR /app

# Install dependencies first so this layer is cached unless requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and training code.
COPY train.py app.py ./

# Train the model at build time so the resulting image is self-contained and
# starts serving immediately, with no training step needed at runtime.
RUN python train.py --data-path ${DATA_PATH} --model-path ${MODEL_PATH}

# Run as a non-root user for defense in depth.
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Kubernetes performs its own liveness/readiness checks (see k8s/deployment.yaml);
# this HEALTHCHECK also lets plain `docker run` report container health.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=3).status == 200 else 1)"

# Two workers with two threads each is enough concurrency for a lightweight
# logistic-regression model while staying inside the 512Mi memory limit set
# in k8s/deployment.yaml.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "60", "app:app"]
