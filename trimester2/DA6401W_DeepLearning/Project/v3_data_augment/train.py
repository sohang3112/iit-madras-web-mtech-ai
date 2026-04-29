"""This proved to have absolutely horrible performance - 0.1% !!!"""
from pathlib import Path

from sklearn.metrics import balanced_accuracy_score, accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import lightning as L
from torch.utils.data import DataLoader, Dataset
from lightning.pytorch.callbacks.early_stopping import EarlyStopping
from lightning.pytorch.callbacks import ModelCheckpoint
from sentence_transformers import SentenceTransformer


class EmojiDataset(Dataset):
    def __init__(self, csv_path: Path, model_name='all-mpnet-base-v2'):
        self.df = pd.read_csv(csv_path)
        self.df = self.df.drop_duplicates(['Emoji','Description'])  # shouldn't be required, but just in case train data has any duplicates accidentally
        self.df = self.df.dropna()         # drop any blank rows
        self.encoder = SentenceTransformer(model_name)
        
        print(f"Encoding {csv_path}...")
        self.embeddings_path = csv_path.parent / f'{csv_path.stem}_embeddings.pth'
        if self.embeddings_path.exists():
            print(f'Embeddings already exist at:', self.embeddings_path)
            self.embeddings = torch.load(self.embeddings_path)
        else:
            self.embeddings = self.encoder.encode(        # this .encode() takes some time
                self.df['Description'].astype(str).tolist(), 
                convert_to_tensor=True, 
                show_progress_bar=True
            )
            torch.save(self.embeddings, self.embeddings_path)
            print(f'Saved embeddings to {self.embeddings_path}')
            
        self.emojis = sorted(self.df['Emoji'].unique())
        self.emoji_to_idx = {emoji: i for i, emoji in enumerate(self.emojis)}
        self.labels = torch.tensor([self.emoji_to_idx[e] for e in self.df['Emoji']], dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.embeddings[idx], self.labels[idx]

class EmojiClassifier(L.LightningModule):
    def __init__(self, input_dim, num_classes, emojis: list[str]):
        super().__init__()
        self.save_hyperparameters(ignore=['emojis'])
        self.emojis = emojis  
        
        self.model = nn.Sequential(       # i gave it name SEQ V1
            nn.Linear(input_dim, 512),
            nn.BatchNorm1d(512),
            nn.GELU(),
            nn.Dropout(0.4),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )
        self.criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
        
        self.test_step_outputs = []

    def forward(self, x):
        return self.model(x)

    def _shared_step(self, batch):
        """Helper to process a batch across train, val, and test steps"""
        features, labels = batch
        logits = self(features)
        loss = self.criterion(logits, labels)
        acc = (logits.argmax(1) == labels).float().mean()
        return loss, acc, logits, labels

    def training_step(self, batch, batch_idx):
        loss, acc, _, _ = self._shared_step(batch)
        self.log("train_loss", loss, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        loss, acc, _, _ = self._shared_step(batch)
        self.log_dict({"val_loss": loss, "val_acc": acc}, prog_bar=True)

    def test_step(self, batch, batch_idx):
        loss, acc, logits, labels = self._shared_step(batch)
        
        _, top5_preds = logits.topk(5, dim=1)
        # Check if labels are anywhere in the top 5 predictions along the class dimension
        top5_acc = (top5_preds == labels.unsqueeze(1)).any(dim=1).float().mean()
        
        output = {
            "labels": labels.cpu(), 
            "preds": logits.argmax(1).cpu(),
            "top5_acc": top5_acc.cpu()
        }
        self.test_step_outputs.append(output)
        return output

    def on_test_epoch_end(self):
        all_labels = torch.cat([x["labels"] for x in self.test_step_outputs]).numpy()
        all_preds = torch.cat([x["preds"] for x in self.test_step_outputs]).numpy()
        avg_top5 = torch.stack([x["top5_acc"] for x in self.test_step_outputs]).mean().item()

        print("\n" + "="*40)
        print("SKLEARN CLASSIFICATION REPORT")
        print("="*40)
        target_names = self.emojis
        print(classification_report(all_labels, all_preds, target_names=target_names))
        
        print(f"Balanced Accuracy: {balanced_accuracy_score(all_labels, all_preds):.4f}")
        print(f"Top-5 Accuracy:     {avg_top5:.4f}")

        cm = confusion_matrix(all_labels, all_preds)
        print('Confusion Matrix (saving to csv):')
        df_cm = pd.DataFrame(cm, index=self.emojis, columns=self.emojis)
        df_cm.to_csv('confusion_matrix.csv')
        #ConfusionMatrixDisplay(cm, display_labels=self.emojis).plot()
        #plt.savefig("confusion_matrix.png")
        
        self.test_step_outputs.clear()

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=1e-3, weight_decay=0.05)
        # OneCycleLR is great for small datasets to avoid local minima
        scheduler = torch.optim.lr_scheduler.OneCycleLR(
            optimizer,
            max_lr=1e-3,
            total_steps=self.trainer.estimated_stepping_batches,
            pct_start=0.2,
            div_factor=10,
            final_div_factor=100
        )
        return {
            "optimizer": optimizer,
            "lr_scheduler": {"scheduler": scheduler, "interval": "step"}
        }

if __name__ == "__main__":
    train_path = Path('../v1_scratch_embeddings/96emojis_50descriptions/train.csv')
    val_path = Path('../v1_scratch_embeddings/96emojis_50descriptions/val.csv')
    emojis = list(pd.read_csv(train_path)['Emoji'].drop_duplicates())
    Path('emoji_classes.txt').write_text('\n'.join(emojis))

    train_ds = EmojiDataset(train_path)
    val_ds = EmojiDataset(val_path)
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=64)

    # all-mpnet-base-v2 uses 768 dimensions
    model = EmojiClassifier(input_dim=768, num_classes=len(train_ds.emojis), emojis=emojis)

    checkpoint_callback = ModelCheckpoint(monitor="val_acc", mode="max", save_top_k=1)
    early_stop = EarlyStopping(monitor="val_acc", mode="max", patience=15)
    trainer = L.Trainer(
        max_epochs=200, 
        callbacks=[checkpoint_callback, early_stop],
        accelerator="auto",
        precision="16-mixed" # Faster training on modern GPUs
    )
    trainer.fit(model, train_loader, val_loader)
    
    best_model = EmojiClassifier.load_from_checkpoint(
        checkpoint_callback.best_model_path,
        input_dim=768,
        num_classes=len(train_ds.emojis)
    )
    best_model_path = Path('best_model_weights.pth')
    torch.save({
        'state_dict': best_model.state_dict(),
        'emoji_list': train_ds.emojis,
        'emoji_to_idx': train_ds.emoji_to_idx
    }, best_model_path)

    print(f"Final Weights Saved to {best_model_path} (Best Val Acc: {checkpoint_callback.best_model_score:.4f})")