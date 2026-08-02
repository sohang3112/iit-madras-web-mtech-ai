FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HOME=/app/.cache/huggingface \
    MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libgomp1 \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 mluser \
 && useradd --uid 1000 --gid mluser --shell /bin/bash --create-home mluser

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY --chown=mluser:mluser . .

RUN mkdir -p /app/models /app/data /app/logs /app/.cache/huggingface \
 && python -c "from transformers import pipeline; pipeline('sentiment-analysis', model='${MODEL_NAME}')" \
 && chown -R mluser:mluser /app

USER mluser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
