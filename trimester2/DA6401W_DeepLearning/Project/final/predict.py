from pathlib import Path
import string

import gradio as gr
from sentence_transformers import SentenceTransformer
import torch
import nltk
from nltk.corpus import stopwords

# custom user module
from train import EmojiClassifier

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

emojis = Path("emoji_classes.txt").read_text().splitlines()
encoder = SentenceTransformer("all-mpnet-base-v2")
model = EmojiClassifier.load_from_checkpoint(
    "model/epoch=10-step=638.ckpt", input_dim=768, num_classes=96, emojis=emojis
)


def preprocess(text: str) -> str:
    text = text.lower()
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )  # remove punctuation
    text = " ".join(
        [word for word in text.split() if word not in stop_words]
    )  # remove stop words
    return text


def predict(text: str):
    text = preprocess(text)
    embedding = torch.from_numpy(encoder.encode([text]))

    with torch.no_grad():
        output = model(embedding)
        probs = torch.nn.functional.softmax(output[0], dim=0)

    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    confidences = {emojis[i]: float(sorted_probs[i]) for i in range(5)}  # top 5 emojis
    return confidences


gr.Interface(fn=predict, inputs="text", outputs=gr.Label(num_top_classes=5)).launch()
