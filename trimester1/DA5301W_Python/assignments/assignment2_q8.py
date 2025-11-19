# Assignment 2 > Q8

# Compute the Weighted Moving Average (WMA) of total daily revenues per category across all days.
# The WMA assigns more weight to recent days (e.g., with weights [0.5, 0.3, 0.2], the latest day gets 0.5).

# Return a list containing the WMA value for each day. For the first few days (where there are fewer
# than the required number of previous days), compute the WMA using the available subset of weights
# (normalize them so they still sum to 1).

# Input:

# • df: Pandas DataFrame with columns ['OrderDate', 'Category', 'Price', 'Quantity'].
# • weights: list or NumPy array of weights (most recent day has the first weight).

# Output: List of floats — one WMA value per day.

import pandas as pd
import numpy as np

# ChatGPT generated code (not mine unfortunately) - TODO: study it!
def weighted_moving_average(df: pd.DataFrame, weights: np.ndarray) -> list:
    # Ensure weights are numpy array
    weights = np.array(weights, dtype=float)

    # Compute daily revenue summed over categories
    df['Revenue'] = df['Price'] * df['Quantity']
    daily = df.groupby('OrderDate')['Revenue'].sum().sort_index()

    revenues = daily.values
    n_days = len(revenues)
    w_len = len(weights)

    wma_values = []

    for i in range(n_days):
        # Determine the window of revenue values to use
        start = max(0, i - w_len + 1)
        window = revenues[start:i+1]

        # Select matching subset of weights (recent day first)
        sub_weights = weights[:len(window)]

        # Normalize to sum to 1
        sub_weights = sub_weights / sub_weights.sum()

        # Reverse window so most recent aligns with first weight
        window = window[::-1]

        wma = np.sum(window * sub_weights)
        wma_values.append(wma)

    return wma_values
