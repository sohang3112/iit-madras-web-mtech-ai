from pathlib import Path
import urllib.request

from matplotlib import pyplot as plt, font_manager as fm
import pandas as pd
import lightning as L
from torch.utils.data import DataLoader

# custom user modules
from train import EmojiClassifier, EmojiDataset


# def setup_emoji_font():
#     font_path = Path("NotoColorEmoji.ttf")
#     if not font_path.exists():
#         print("Downloading Noto Color Emoji font...")
#         url = "https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoColorEmoji.ttf"
#         urllib.request.urlretrieve(url, font_path)
    
#     fe = fm.FontEntry(
#         fname=str(font_path),
#         name='NotoColorEmoji'
#     )
#     fm.fontManager.ttflist.insert(0, fe)
    
#     plt.rcParams['font.family'] = fe.name
#     # This prevents matplotlib from trying to use 'bold' or 'italic' 
#     # which Noto Emoji doesn't support
#     plt.rcParams['axes.unicode_minus'] = False 
#     print("Emoji font registered successfully.")

# setup_emoji_font()
train_path = Path('../v1_scratch_embeddings/96emojis_50descriptions/train.csv')
val_path = Path('../v1_scratch_embeddings/96emojis_50descriptions/val.csv')
emojis = list(pd.read_csv(train_path)['Emoji'].drop_duplicates())
Path('emoji_classes.txt').write_text('\n'.join(emojis))
val_ds = EmojiDataset(val_path)
val_loader = DataLoader(val_ds, batch_size=64, shuffle=False)
# model = EmojiClassifier.load_from_checkpoint(
#     checkpoint_path='SEQV1_model_weights_epoch25_75.6accuracy.pth',
#     #hparams_file=
#     #map_location=None
# )
# all-mpnet-base-v2 uses 768 dimensions, 96 emoji output classes
model = EmojiClassifier.load_from_checkpoint('lightning_logs/version_2/checkpoints/epoch=10-step=638.ckpt', input_dim=768, num_classes=96, emojis=emojis)   
trainer = L.Trainer(accelerator="auto")
trainer.test(model, dataloaders=val_loader)