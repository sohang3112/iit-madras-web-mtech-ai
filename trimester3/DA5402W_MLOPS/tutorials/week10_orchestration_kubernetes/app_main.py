from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ML Sentiment API")
ready = True

class PredictRequest(BaseModel):
    texts: list[str]

@app.get("/health")
def health():
    if not ready:
        raise HTTPException(status_code=503, detail="model not ready")
    return {"status": "ok", "model": "mock-sentiment-model"}

@app.post("/predict")
def predict(req: PredictRequest):
    if not ready:
        raise HTTPException(status_code=503, detail="model not loaded")
    return {"predictions": [{"text": text, "label": "POSITIVE" if any(w in text.lower() for w in ("love", "good", "great")) else "NEGATIVE", "score": 0.99} for text in req.texts]}
