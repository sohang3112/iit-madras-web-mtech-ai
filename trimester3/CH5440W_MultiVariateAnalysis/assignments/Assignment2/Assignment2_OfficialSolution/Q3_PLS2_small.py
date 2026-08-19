"""
CH5440W Assignment 2 Part 1 - Question 3
PLS2 using NIPALS, 3 factors.
No centering, scaling or standardization.

Requires this file to be in the same folder as:
    pls2_nipals.py
"""

import numpy as np
from pls2_nipals import pls2_nipals, predict

np.set_printoptions(precision=4, suppress=True)

X = np.array([
    [2,  5,  3,  6,  8, 1],
    [4,  6,  5,  7,  9, 2],
    [5,  8,  6,  8, 10, 3],
    [7,  9,  8, 10, 12, 5],
    [9, 11,  9, 12, 13, 6]
], dtype=float)

Y = np.array([
    [20, 35],
    [24, 40],
    [28, 45],
    [36, 58],
    [42, 66]
], dtype=float)

NCOMP = 3

# Full calibration model: no centering and no scaling
model = pls2_nipals(
    X, Y,
    ncomp=NCOMP,
    center=False,
    scale=False,
    rescale_w_after_p=False
)

W = model["W"]
T = model["T"]
U = model["U"]
Q = model["Q"]
P = model["P"]
B = model["B"]

Yhat = predict(model, X)

print("W (X-weights) =\n", W)
print("\nT (X-scores) =\n", T)
print("\nU (Y-scores) =\n", U)
print("\nQ (Y-loadings) =\n", Q)
print("\nP (X-loadings) =\n", P)
print("\nB (regression coefficients; Yhat = X @ B) =\n", B)
print("\nPredicted Y =\n", Yhat)

# Internal reconstruction check
reconstruction_error = np.max(
    np.abs((Y - model["F_final"]) - T @ Q.T)
)
print("\nMax reconstruction error |(Y-F_final)-TQ'| =",
      reconstruction_error)

# ---------- Leave-One-Out PRESS ----------
n = X.shape[0]
sq_err = np.zeros_like(Y)

for i in range(n):
    mask = np.ones(n, dtype=bool)
    mask[i] = False

    loo_model = pls2_nipals(
        X[mask], Y[mask],
        ncomp=NCOMP,
        center=False,
        scale=False
    )

    yhat_i = predict(loo_model, X[i:i+1])
    sq_err[i] = (Y[i:i+1] - yhat_i) ** 2

PRESS_per_var = sq_err.sum(axis=0)
PRESS_total = sq_err.sum()

RMS_PRESS_per_var = np.sqrt(PRESS_per_var / n)
RMS_PRESS_total = np.sqrt(
    PRESS_total / (n * Y.shape[1])
)

print("\nPRESS per response variable =", PRESS_per_var)
print("PRESS total =", PRESS_total)
print("RMS PRESS per response variable =", RMS_PRESS_per_var)
print("Pooled RMS PRESS =", RMS_PRESS_total)

# Expected report values, rounded to four decimals:
# PRESS = [2313.3704, 6005.4105]
# Total PRESS = 8318.7809
# RMS PRESS = [21.5099, 34.6566]
# Pooled RMS PRESS = 28.8423