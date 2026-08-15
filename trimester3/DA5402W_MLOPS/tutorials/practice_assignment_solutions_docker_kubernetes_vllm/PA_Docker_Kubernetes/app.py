"""
app.py
======
Flask REST API serving the trained diabetes classifier.

Endpoints:
    GET  /health   -> liveness/readiness check, reports whether the model is loaded
    POST /predict  -> accepts the 8 Pima feature values as JSON, returns the
                       predicted class and the probability of a positive outcome

Configuration is read entirely from environment variables so the same image
can run unmodified across environments (local, Docker, Kubernetes):
    MODEL_PATH  - path to the joblib-serialized pipeline (default: model/model.joblib)
    LOG_LEVEL   - Python logging level name (default: INFO)
    API_KEY     - if set, POST /predict requires a matching 'X-API-Key' header
"""

import logging
import os

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request

MODEL_PATH = os.environ.get("MODEL_PATH", "model/model.joblib")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
API_KEY = os.environ.get("API_KEY")  # optional; auth is skipped if unset

# Order matters: must match the columns the model was trained on in train.py.
FEATURE_NAMES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Loaded once at process startup and reused across requests (thread-safe:
# scikit-learn estimators only read state during predict()).
model = None


def load_model():
    global model
    logger.info("Loading model from %s", MODEL_PATH)
    model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully.")


def validate_payload(payload: dict):
    """Return (cleaned_values, error_message). error_message is None on success."""
    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object."

    missing = [f for f in FEATURE_NAMES if f not in payload]
    if missing:
        return None, f"Missing required field(s): {', '.join(missing)}"

    values = {}
    for name in FEATURE_NAMES:
        raw_value = payload[name]
        try:
            values[name] = float(raw_value)
        except (TypeError, ValueError):
            return None, f"Field '{name}' must be numeric, got: {raw_value!r}"

    return values, None


@app.route("/health", methods=["GET"])
def health():
    """Used by Kubernetes liveness/readiness probes."""
    is_ready = model is not None
    status_code = 200 if is_ready else 503
    return (
        jsonify(
            {
                "status": "healthy" if is_ready else "unhealthy",
                "model_loaded": is_ready,
            }
        ),
        status_code,
    )


@app.route("/predict", methods=["POST"])
def predict():
    if API_KEY:
        provided_key = request.headers.get("X-API-Key")
        if provided_key != API_KEY:
            logger.warning("Rejected request with invalid or missing API key.")
            return jsonify({"error": "Unauthorized: invalid or missing X-API-Key header."}), 401

    if model is None:
        return jsonify({"error": "Model is not loaded yet. Try again shortly."}), 503

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    values, error = validate_payload(payload)
    if error:
        return jsonify({"error": error}), 400

    try:
        features = pd.DataFrame([[values[name] for name in FEATURE_NAMES]], columns=FEATURE_NAMES)
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])
    except Exception:
        logger.exception("Inference failed.")
        return jsonify({"error": "Internal error during inference."}), 500

    return jsonify(
        {
            "prediction": prediction,
            "outcome": "diabetic" if prediction == 1 else "non-diabetic",
            "probability": round(probability, 4),
        }
    )


# Loaded at import time so it works both under `python app.py` and under a
# WSGI server like gunicorn (which imports the module without running main()).
load_model()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port)
