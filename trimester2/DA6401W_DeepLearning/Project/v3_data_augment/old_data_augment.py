import pandas as pd
import nlpaug.augmenter.word as naw
from tqdm import tqdm

def augment_emoji_data(input_file, output_file, aug_factor=3):
    df = pd.read_csv(input_file)
    
    # Initialize augmenters
    # 1. Synonym replacement (Contextual Word Embeddings - uses BERT)
    # This replaces words with synonyms that fit the context
    aug_syn = naw.ContextualWordEmbsAug(
        model_path='bert-base-uncased', action="substitute", device='cpu'
    )
    
    # 2. Random Swap (Changes word order)
    aug_swap = naw.RandomWordAug(action="swap")

    augmented_data = []

    print(f"Augmenting {len(df)} rows...")
    for _, row in tqdm(df.iterrows(), total=len(df)):
        emoji = row['Emoji']
        name = row['Unicode Name']
        desc = str(row['Description'])
        
        # Keep the original
        augmented_data.append([emoji, name, desc])
        
        # Generate variations
        for _ in range(aug_factor):
            # Alternate between synonym replacement and swapping
            if _ % 2 == 0:
                new_desc = aug_syn.augment(desc)[0]
            else:
                new_desc = aug_swap.augment(desc)[0]
                
            augmented_data.append([emoji, name, new_desc])

    # Save to new CSV
    new_df = pd.DataFrame(augmented_data, columns=['Emoji', 'Unicode Name', 'Description'])
    new_df.to_csv(output_file, index=False)
    print(f"Augmentation complete! New dataset size: {len(new_df)}")

if __name__ == "__main__":
    # Factor of 3 means 1 original + 3 augmented = 4x data
    augment_emoji_data('../v1_scratch_embeddings/96emojis_50descriptions/train.csv', 'train_augmented.csv', aug_factor=3)