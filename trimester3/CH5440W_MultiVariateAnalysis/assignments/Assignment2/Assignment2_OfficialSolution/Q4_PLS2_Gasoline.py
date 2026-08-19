"""
CH5440W Assignment 2 Part 1 - Question 4
Gasoline NIR data: NIPALS PLS calibration.

The script:
1. Reads Gasoline_Rigorous_JMP.xlsx.
2. Uses Octane as Y and 401 NIR variables as X.
3. Mean-centers X and Y; no scaling.
4. Performs LOO cross-validation for 1 to 10 factors.
5. Fits the selected 4-factor model.
6. Exports W, T, U, P and B as CSV files.

Requires this file and pls2_nipals.py to be in the same folder.
"""

from pathlib import Path
import numpy as np
import openpyxl

from pls2_nipals import pls2_nipals, predict

np.set_printoptions(precision=6, suppress=True)

# Accept either of the filenames used during the assignment work.
INPUT_CANDIDATES = [
    "Gasoline_Rigorous_JMP.xlsx"
]

input_file = None
for name in INPUT_CANDIDATES:
    if Path(name).exists():
        input_file = name
        break

if input_file is None:
    raise FileNotFoundError(
        "Gasoline Excel file not found. Expected one of: "
        + ", ".join(INPUT_CANDIDATES)
    )

# ---------- Read data ----------
wb = openpyxl.load_workbook(input_file, data_only=True)
ws = wb.active

# Original assignment workbook layout:
# first column = sample identifier
# next column = Octane
# next 401 columns = NIR wavelengths
rows = [
    r for r in ws.iter_rows(min_row=2, values_only=True)
    if r[0] is not None
]

data = np.array([r[1:403] for r in rows], dtype=float)

Y = data[:, 0:1]
X = data[:, 1:]

if X.shape != (48, 401):
    raise ValueError(
        f"Unexpected data shape: X={X.shape}, Y={Y.shape}. "
        "Expected X=(48, 401) and Y=(48, 1)."
    )

print("Input file:", input_file)
print("X shape:", X.shape)
print("Y shape:", Y.shape)

# ---------- LOO cross-validation ----------
n = X.shape[0]
MAX_COMPONENTS = 10
rmsecv = []

for a in range(1, MAX_COMPONENTS + 1):
    squared_error = 0.0

    for i in range(n):
        mask = np.ones(n, dtype=bool)
        mask[i] = False

        loo_model = pls2_nipals(
            X[mask], Y[mask],
            ncomp=a,
            center=True,
            scale=False,
            rescale_w_after_p=True
        )

        yhat_i = predict(loo_model, X[i:i+1])
        squared_error += np.sum(
            (Y[i:i+1] - yhat_i) ** 2
        )

    value = np.sqrt(squared_error / n)
    rmsecv.append(value)
    print(f"A={a:2d}  LOO-RMSECV={value:.4f}")

# Four factors are used as the parsimonious operating model
NCOMP = 4

# ---------- Final 4-factor calibration ----------
model = pls2_nipals(
    X, Y,
    ncomp=NCOMP,
    center=True,
    scale=False,
    rescale_w_after_p=True
)

Yhat = predict(model, X)
residual = Y - Yhat

R2 = 1.0 - (
    np.sum(residual ** 2)
    / np.sum((Y - Y.mean()) ** 2)
)

RMSEC = np.sqrt(np.mean(residual ** 2))
RMSECV_A4 = rmsecv[NCOMP - 1]

print("\nFinal model: A =", NCOMP)
print("R2 =", R2)
print("RMSEC =", RMSEC)
print("RMSECV =", RMSECV_A4)
print("Mean Octane =", model["y_mean"][0])
print("Q =", model["Q"].ravel())

# ---------- Export matrices ----------
np.savetxt(
    "Q4_B_coefficients.csv",
    model["B"],
    delimiter=",",
    header="beta (PLS regression coefficient per wavelength)",
    comments=""
)

np.savetxt(
    "Q4_W_weights.csv",
    model["W"],
    delimiter=","
)

np.savetxt(
    "Q4_T_scores.csv",
    model["T"],
    delimiter=","
)

np.savetxt(
    "Q4_U_scores.csv",
    model["U"],
    delimiter=","
)

np.savetxt(
    "Q4_P_loadings.csv",
    model["P"],
    delimiter=","
)

print("\nCSV files exported successfully:")
print("Q4_B_coefficients.csv")
print("Q4_W_weights.csv")
print("Q4_T_scores.csv")
print("Q4_U_scores.csv")
print("Q4_P_loadings.csv")