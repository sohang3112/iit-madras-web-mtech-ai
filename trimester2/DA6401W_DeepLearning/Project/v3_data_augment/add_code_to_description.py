import pandas as pd

def main(df_path, out_df_path):
    df = pd.read_csv(df_path)
    names_df = df.drop_duplicates(['Emoji','Unicode Name'])
    names_df['Description'] = names_df['Unicode Name']
    df = pd.concat([df, names_df])
    df.to_csv(out_df_path, index=False)

main('train_augment_llm_corrected.csv', 'train_final.csv')
main('../v1_scratch_embeddings/96emojis_50descriptions/val.csv', 'val_final.csv')