import pandas as pd
import torch
from transformers import pipeline
from tqdm import tqdm
import random
import string

def is_valid_token(token):
    """Checks if the token is actual text and not just punctuation or junk."""
    # Remove BERT subword markers
    clean_token = token.replace("##", "").strip()
    if not clean_token:
        return False
    # Reject if it's just punctuation or a single special character
    if all(char in string.punctuation for char in clean_token):
        return False
    # Reject if it's too short (unless it's 'a' or 'i')
    if len(clean_token) < 2 and clean_token not in ['a', 'i']:
        return False
    return True

def augment_emoji_data(input_file, output_file, aug_factor=3):
    df = pd.read_csv(input_file)
    
    device = 0 if torch.cuda.is_available() else -1
    # Use 'distilbert' - it's faster and often less 'random' than base BERT for simple tasks
    augmenter = pipeline('fill-mask', model='distilbert-base-uncased', device=device)
    
    augmented_data = []

    print(f"Augmenting {len(df)} rows with strict filtering...")
    
    for _, row in tqdm(df.iterrows(), total=len(df)):
        emoji = row['Emoji']
        name = row['Unicode Name']
        desc = str(row['Description']).lower().strip()
        
        # 1. Keep the original
        augmented_data.append([emoji, name, desc])
        
        words = desc.split()
        
        # 2. Generate variations
        attempts = 0
        successes = 0
        
        # We try to get 'aug_factor' valid variations
        while successes < aug_factor and attempts < 10:
            attempts += 1
            new_desc = desc
            
            try:
                if len(words) >= 1:
                    # Pick a random word to mask
                    target_idx = random.randint(0, len(words) - 1)
                    copy_words = words.copy()
                    original_word = copy_words[target_idx]
                    
                    copy_words[target_idx] = augmenter.tokenizer.mask_token
                    masked_sentence = " ".join(copy_words)
                    
                    # Get predictions
                    preds = augmenter(masked_sentence)
                    
                    # Filter predictions for quality
                    valid_preds = [
                        p['token_str'] for p in preds 
                        if is_valid_token(p['token_str']) and p['token_str'].lower() != original_word
                    ]
                    
                    if valid_preds:
                        # Pick a random valid suggestion
                        copy_words[target_idx] = random.choice(valid_preds[:3]) # Top 3 are usually safest
                        new_desc = " ".join(copy_words).strip()
                        
                        # Final check: Don't add if it's just garbage or identical
                        if new_desc and new_desc != desc:
                            augmented_data.append([emoji, name, new_desc])
                            successes += 1
                
                # If it's a multi-word description, occasionally just swap words
                elif len(words) >= 2 and random.random() > 0.7:
                    idx1, idx2 = random.sample(range(len(words)), 2)
                    copy_words = words.copy()
                    copy_words[idx1], copy_words[idx2] = copy_words[idx2], copy_words[idx1]
                    new_desc = " ".join(copy_words).strip()
                    augmented_data.append([emoji, name, new_desc])
                    successes += 1
                    
            except Exception:
                continue

    new_df = pd.DataFrame(augmented_data, columns=['Emoji', 'Unicode Name', 'Description'])
    new_df = new_df[new_df['Description'].str.contains('[a-zA-Z0-9]', na=False)]   # Remove any garbage rows where Description is just punctuation (last line of defense)
    new_df = new_df.drop_duplicates(subset=['Emoji', 'Description'])
    new_df.to_csv(output_file, index=False)
    print(f"Done! Expanded to {len(new_df)} rows.")

if __name__ == "__main__":
    augment_emoji_data('../v1_scratch_embeddings/96emojis_50descriptions/train.csv', 'train_augmented.csv', aug_factor=3)