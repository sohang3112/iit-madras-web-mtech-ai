"""Preprocess data.csv and split it into training / validation data."""
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

data_dir = Path('96emojis_50descriptions')
df = pd.read_csv(data_dir / 'data.csv')
df['Descriptions'] = df['Descriptions'].str.split('; ')
df = df.explode('Descriptions')
df = df.rename(columns={'Descriptions': 'Description'})

train_df, val_df = train_test_split(
    df, 
    test_size=0.2,     # 80:20 train:test split
    random_state=42, 
    stratify=df['Emoji']
)

train_df.to_csv(data_dir / 'train.csv', index=False)
val_df.to_csv(data_dir / 'val.csv', index=False)

print(f"Preprocessing complete.")
print(f"Training samples: {len(train_df)}")
print(f"Validation samples: {len(val_df)}")

# checks
# Each should print '100' (the number of unique classes)
print(train_df['Emoji'].nunique())
print(val_df['Emoji'].nunique())

# Each should print '8' (samples per class in training)
print(train_df['Emoji'].value_counts().unique())