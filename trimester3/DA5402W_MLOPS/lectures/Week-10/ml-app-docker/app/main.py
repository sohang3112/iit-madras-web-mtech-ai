import logging
import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("ml-app")

MODEL_NAME = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")

state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("loading model: %s", MODEL_NAME)
    state["classifier"] = pipeline("sentiment-analysis", model=MODEL_NAME)
    state["ready"] = True
    logger.info("model loaded")
    yield
    state.clear()


app = FastAPI(title="ML Sentiment API", version="0.1.0", lifespan=lifespan)


class PredictRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_length=64, examples=[["I love this!", "This is terrible."]])


class Prediction(BaseModel):
    text: str
    label: str
    score: float


class PredictResponse(BaseModel):
    predictions: List[Prediction]


@app.get("/health")
def health():
    if not state.get("ready"):
        raise HTTPException(status_code=503, detail="model not ready")
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    classifier = state.get("classifier")
    if classifier is None:
        raise HTTPException(status_code=503, detail="model not loaded")
    results = classifier(req.texts)
    return PredictResponse(
        predictions=[
            Prediction(text=t, label=r["label"], score=float(r["score"]))
            for t, r in zip(req.texts, results)
        ]
    )
