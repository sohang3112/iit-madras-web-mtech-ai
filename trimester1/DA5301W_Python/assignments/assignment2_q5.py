import pandas as pd
from itertools import combinations

# ChatGPT generated code - not mine unfortunately :( - TODO: study it
def frequent_product_pair(df: pd.DataFrame) -> tuple:
    """
    Return the most frequent ordered product pair.
    """
    # keep original order within each OrderID
    grouped = (
        df.sort_values(["OrderID", "Product"])
          .groupby("OrderID")["Product"]
          .apply(list)
    )

    # generate ordered product pairs per order
    all_pairs = []
    for products in grouped:
        for p1, p2 in combinations(products, 2):
            all_pairs.append((p1, p2))

    if not all_pairs:
        return ()

    # count frequency
    freq = pd.Series(all_pairs).value_counts()

    return freq.index[0]

# my original code - failing 1 private test
# my mistakes here pointed out by ChatGPT: 
#   * doing sort_values('Product') at start changes original product order, but question requires us to preserve product order
#   * combinations(products, 2) is used which always gives sorted combinations, NOT preserving original product order as required
# def frequent_product_pair(df: pd.DataFrame) -> tuple: 
#     '''Return product pair that appears most frequently together in same order. ''' 
#     ans = ( 
#         df .sort_values('Product') 
#         .groupby('OrderID')['Product'] 
#         # product pairs for each OrderID 
#         .apply(lambda products: list(combinations(products, 2))) 
#         # join all pairs (Series of lists of pairs -> Series of pairs) 
#         .apply(pd.Series).stack() 
#         # most frequent pair 
#         .mode() 
#     ) 
#     return () if ans.empty else ans.iloc[0]
