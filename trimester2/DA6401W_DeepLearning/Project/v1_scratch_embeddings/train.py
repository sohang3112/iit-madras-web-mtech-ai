from collections import Counter
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
import lightning as L
from lightning.pytorch.callbacks.early_stopping import EarlyStopping
import pandas as pd


class EmojiDataset(Dataset):
    def __init__(self, csv_path, vocab=None):
        self.df = pd.read_csv(csv_path)
        self.data = [str(text).lower().split() for text in self.df['Description']]     # split into words (simple tokenizer)
        
        self.emojis = sorted(self.df['Emoji'].unique())
        self.emoji_to_idx = {emoji: i for i, emoji in enumerate(self.emojis)}
        self.labels = [self.emoji_to_idx[e] for e in self.df['Emoji']]
        
        # Build or use existing Vocab
        if vocab is None:
            counts = Counter([word for sublist in self.data for word in sublist])
            self.vocab = {word: i + 1 for i, (word, _) in enumerate(counts.items())}
            self.vocab['<pad>'] = 0
        else:
            self.vocab = vocab

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # Convert words to indices
        tokens = [self.vocab.get(w, 0) for w in self.data[idx]]
        return torch.tensor(tokens, dtype=torch.long), torch.tensor(self.labels[idx], dtype=torch.long)

def collate_batch(batch):
    """Combines variable length sequences for EmbeddingBag."""
    label_list, text_list, offsets = [], [], [0]
    for (_text, _label) in batch:
        label_list.append(_label)
        text_list.append(_text)
        offsets.append(_text.size(0))
    offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
    label_list = torch.stack(label_list)
    text_list = torch.cat(text_list)
    return label_list, text_list, offsets


class EmojiClassifier(L.LightningModule):
    def __init__(self, vocab_size, embed_dim, num_classes):
        super().__init__()
        # EmbeddingBag averages word vectors automatically
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=False)
        self.fc = nn.Sequential(
            nn.Linear(embed_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes)
        )
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        return self.fc(embedded)

    def training_step(self, batch, batch_idx):
        labels, text, offsets = batch
        logits = self(text, offsets)
        loss = self.criterion(logits, labels)
        self.log("train_loss", loss, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        labels, text, offsets = batch
        logits = self(text, offsets)
        loss = self.criterion(logits, labels)
        acc = (logits.argmax(1) == labels).float().mean()
        self.log_dict({"val_loss": loss, "val_acc": acc}, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)


if __name__ == "__main__":
    train_ds = EmojiDataset('train.csv')
    val_ds = EmojiDataset('val.csv', vocab=train_ds.vocab)
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True, collate_fn=collate_batch)
    val_loader = DataLoader(val_ds, batch_size=16, collate_fn=collate_batch)

    model = EmojiClassifier(
        vocab_size=len(train_ds.vocab),
        embed_dim=100, 
        num_classes=len(train_ds.emojis)
    )
    trainer = L.Trainer(
        max_epochs=200, 
        callbacks=[EarlyStopping(monitor="val_loss", mode="min", patience=10)],
        accelerator="auto"     # auto use cpu or gpu (best available on device)
    )
    trainer.fit(model, train_loader, val_loader)

    model_path = 'model_weighs.pth'
    torch.save(model.state_dict(), model_path)
    print(f'Saved model weights to {model_path}')
