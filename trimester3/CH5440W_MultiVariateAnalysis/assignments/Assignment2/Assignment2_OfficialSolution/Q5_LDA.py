"""
CH5440W Assignment 2 - Question 5
Linear Discriminant Analysis (2 classes, cost ratio = prior ratio = 1)
"""
import numpy as np
import openpyxl

np.set_printoptions(precision=5, suppress=True)

wb = openpyxl.load_workbook("DataforQuestion5.xlsx", data_only=True)
ws = wb.active
rows = list(ws.iter_rows(min_row=3, max_row=48, values_only=True))
g1, g2, test = [], [], []
for r in rows:
    if isinstance(r[0], (int, float)) and isinstance(r[1], (int, float)):
        g1.append((r[0], r[1]))
    if isinstance(r[3], (int, float)) and isinstance(r[4], (int, float)):
        g2.append((r[3], r[4]))
    if isinstance(r[8], (int, float)) and isinstance(r[9], (int, float)):
        test.append((r[8], r[9]))
G1, G2, Test = np.array(g1), np.array(g2), np.array(test)
n1, n2 = G1.shape[0], G2.shape[0]

# (a) Variance matrices
mu1, mu2 = G1.mean(axis=0), G2.mean(axis=0)
S1 = np.cov(G1.T, ddof=1)
S2 = np.cov(G2.T, ddof=1)
print("S1 =\n", S1)
print("S2 =\n", S2)

# (b) Pooled covariance
Sp = ((n1 - 1) * S1 + (n2 - 1) * S2) / (n1 + n2 - 2)
print("\nSp (pooled) =\n", Sp)

# (c) Linear classification equation (cost ratio = prior ratio = 1)
Sp_inv = np.linalg.inv(Sp)
w = Sp_inv @ (mu1 - mu2)
c = 0.5 * (mu1 + mu2) @ Sp_inv @ (mu1 - mu2)
print(f"\nd(x) = {w[0]:.4f}*F1 + {w[1]:.4f}*F2 - {c:.4f}")
print("Classify Group 1 if d(x) > 0, else Group 2")


def classify(Xarr):
    d = Xarr @ w - c
    return np.where(d > 0, 1, 2), d


# (d) Training misclassification
cls1, d1 = classify(G1)
mis1 = np.where(cls1 != 1)[0]
cls2, d2 = classify(G2)
mis2 = np.where(cls2 != 2)[0]
print(f"\nGroup1 misclassified (0-based idx): {mis1.tolist()}  n={len(mis1)}")
print(f"Group2 misclassified (0-based idx): {mis2.tolist()}  n={len(mis2)}")
print(f"Training accuracy = {1 - (len(mis1)+len(mis2))/(n1+n2):.4f}")

# (e) Classify test set
clst, dt = classify(Test)
for i, (pt, c_) in enumerate(zip(Test, clst)):
    print(f"Test pt {i+1}: {pt} -> class {c_}")
