from pathlib import Path

import torch
from torch import nn
import pandas as pd
import lightning as L
from torch.utils.data import DataLoader, Dataset
from lightning.pytorch.callbacks.early_stopping import EarlyStopping
from sentence_transformers import SentenceTransformer


class EmojiDataset(Dataset):
    """Uses pre-trained word embeddings."""
    
    def __init__(self, csv_path, model_name='all-MiniLM-L6-v2'):
        self.df = pd.read_csv(csv_path)
        self.df = self.df.drop_duplicates()
        self.df = self.df.dropna()        # drop any blank rows
        self.encoder = SentenceTransformer(model_name)
        
        self.embeddings = self.encoder.encode(self.df['Description'].tolist(), 
                                            convert_to_tensor=True, 
                                            show_progress_bar=True)
        
        self.emojis = sorted(self.df['Emoji'].unique())
        self.emoji_to_idx = {emoji: i for i, emoji in enumerate(self.emojis)}
        self.labels = torch.tensor([self.emoji_to_idx[e] for e in self.df['Emoji']], dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.embeddings[idx], self.labels[idx]

# 2. Improved Classifier Model
class EmojiClassifier(L.LightningModule):
    def __init__(self, input_dim, num_classes):
        super().__init__()
        # Deeper architecture with Batch Normalization and Dropout
        self.model = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )
        # Label smoothing helps with small, potentially noisy datasets
        self.criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        features, labels = batch
        logits = self(features)
        loss = self.criterion(logits, labels)
        self.log("train_loss", loss, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        features, labels = batch
        logits = self(features)
        loss = self.criterion(logits, labels)
        acc = (logits.argmax(1) == labels).float().mean()
        self.log_dict({"val_loss": loss, "val_acc": acc}, prog_bar=True)

    def configure_optimizers(self):
        # AdamW is Adam with better weight decay (regularization)
        optimizer = torch.optim.AdamW(self.parameters(), lr=1e-3, weight_decay=1e-2)
        # Reduce LR when the model stops improving
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=5
        )
        return {
            "optimizer": optimizer,
            "lr_scheduler": {"scheduler": scheduler, "monitor": "val_loss"}
        }

if __name__ == "__main__":
    data_dir = Path('../v1_scratch_embeddings/96emojis_50descriptions')           # same data as v1
    # data_dir = Path('../v3_data_augment/')           # augmented data from v3 (although the v3 train.py proved to have horrible performance of 0.1% accuracy - hopefully at least data is ok!)
    # Note: SentenceTransformer handles the tokenization and vocab internally
    # train_ds = EmojiDataset(data_dir / 'train_final.csv')
    # val_ds = EmojiDataset(data_dir / 'val_final.csv')
    train_ds = EmojiDataset(data_dir / 'train.csv')
    val_ds = EmojiDataset(data_dir / 'val.csv')
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32)

    # all-MiniLM-L6-v2 produces vectors of size 384
    model = EmojiClassifier(input_dim=384, num_classes=len(train_ds.emojis))

    trainer = L.Trainer(
        max_epochs=100, 
        callbacks=[EarlyStopping(monitor="val_loss", patience=15)],
        accelerator="auto"
    )
    trainer.fit(model, train_loader, val_loader)

    model_path = data_dir / 'model_weights.pth'
    torch.save({
        'state_dict': model.state_dict(),
        'emoji_list': train_ds.emojis
    }, model_path)
    print(f"Model saved at {model_path}. Used Transfer Learning.")