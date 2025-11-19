# You are given two 2D NumPy arrays, A and B, representing two sets of points in 2D space. Compute the Euclidean distance between every pair of points (i, j) where i is from A and j is from B. Each pair (i, j) is considered only once — symmetric duplicates are not counted again. Return the average of all unique pairwise distances.

# Mathematical Expression:
# [
# d(i,j) = \sqrt{(A_i[0] - B_j[0])^2 + (A_i[1] - B_j[1])^2}
# ]
# Then compute the mean over all unique (i, j) pairs.

# Input:
# A: NumPy array of shape (M, 2)
# B: NumPy array of shape (N, 2)

# Output:
# A single float — the average of all unique pairwise Euclidean distances

# MISTAKE IN MY ORIGINAL CODE: I was pairing points like (ith point/row in A, ith point/row in B), but actually had to do: foreach pointA in A, foreach pointB in B

import numpy as np

# ChatGPT generated code - not mine unfortunately :( TODO: study, understand this code
def pairwise_distance(A: np.ndarray, B: np.ndarray) -> float:
    # Compute all pairwise differences: shape (M, N, 2)
    diff = A[:, None, :] - B[None, :, :]
    # Euclidean norms for all M*N pairs
    distances = np.linalg.norm(diff, axis=2)
    # Average over all unique (i, j) pairs (all pairs already unique)
    return distances.mean()
