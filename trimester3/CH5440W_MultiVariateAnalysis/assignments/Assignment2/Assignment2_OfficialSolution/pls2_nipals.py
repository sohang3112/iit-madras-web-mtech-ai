"""
CH5440W Assignment 2 Part 1
Common NIPALS PLS implementation used by Questions 3 and 4.

The parameter rescale_w_after_p is included because the submitted Q3 and Q4
results were generated using two stored-W conventions:

Q3: rescale_w_after_p=False
    W remains unit-normalized after p normalization.
    This exactly reproduces the Q3 tables and PRESS values in the report.

Q4: rescale_w_after_p=True
    This preserves compatibility with the original PLS1/Q4 code used to
    generate the submitted Q4 report and CSV convention.

In both cases, the component reconstruction uses:
    E <- E - t p'
    F <- F - t q'
and:
    B = W (P'W)^(-1) Q'
"""

import numpy as np


def pls2_nipals(X, Y, ncomp, tol=1e-10, max_iter=10000,
                center=False, scale=False,
                rescale_w_after_p=False):

    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)

    if X.ndim != 2:
        raise ValueError("X must be a 2-D array.")
    if Y.ndim == 1:
        Y = Y.reshape(-1, 1)
    if Y.ndim != 2 or X.shape[0] != Y.shape[0]:
        raise ValueError("Y must match X in number of rows.")

    n, p = X.shape
    m = Y.shape[1]
    ncomp = min(int(ncomp), n, p)

    x_mean = X.mean(axis=0) if center else np.zeros(p)
    y_mean = Y.mean(axis=0) if center else np.zeros(m)

    x_std = X.std(axis=0, ddof=1) if scale else np.ones(p)
    y_std = Y.std(axis=0, ddof=1) if scale else np.ones(m)

    if np.any(x_std == 0) or np.any(y_std == 0):
        raise ValueError("Cannot scale a constant variable.")

    E = (X - x_mean) / x_std
    F = (Y - y_mean) / y_std

    W = np.zeros((p, ncomp))
    T = np.zeros((n, ncomp))
    U = np.zeros((n, ncomp))
    Q = np.zeros((m, ncomp))
    P = np.zeros((p, ncomp))

    for h in range(ncomp):

        u = F[:, np.argmax(np.var(F, axis=0))].copy()

        if m == 1:
            # PLS1 branch
            w = E.T @ u / (u @ u)
            w = w / np.linalg.norm(w)
            t = E @ w

            # Retain scalar q, matching the Q4 convention
            q = F.T @ t / (t @ t)
            u = F[:, 0].copy()

        else:
            # PLS2 NIPALS iteration
            u_old = np.zeros_like(u)

            for _ in range(max_iter):
                if np.linalg.norm(u - u_old) <= tol:
                    break

                u_old = u.copy()

                w = E.T @ u / (u @ u)
                w = w / np.linalg.norm(w)
                t = E @ w

                q = F.T @ t / (t @ t)
                q = q / np.linalg.norm(q)

                u = F @ q / (q @ q)
            else:
                raise RuntimeError(
                    f"NIPALS did not converge for component {h + 1}."
                )

        # X-loading
        p_raw = E.T @ t / (t @ t)
        p_norm = np.linalg.norm(p_raw)

        if p_norm == 0:
            raise RuntimeError(
                f"Zero X-loading encountered at component {h + 1}."
            )

        # Steps 9-10
        p_load = p_raw / p_norm
        t = t * p_norm

        # Convention switch for compatibility with the submitted results
        if rescale_w_after_p:
            w = w * p_norm

        # Deflation
        E = E - np.outer(t, p_load)
        F = F - np.outer(t, q)

        W[:, h] = w
        T[:, h] = t
        U[:, h] = u
        Q[:, h] = q
        P[:, h] = p_load

    B = W @ np.linalg.pinv(P.T @ W) @ Q.T

    return {
        "W": W, "T": T, "U": U, "Q": Q, "P": P, "B": B,
        "x_mean": x_mean, "y_mean": y_mean,
        "x_std": x_std, "y_std": y_std,
        "E_final": E, "F_final": F
    }


def predict(model, Xnew):
    Xnew = np.asarray(Xnew, dtype=float)
    if Xnew.ndim == 1:
        Xnew = Xnew.reshape(1, -1)

    Xs = (Xnew - model["x_mean"]) / model["x_std"]
    Ys = Xs @ model["B"]
    return Ys * model["y_std"] + model["y_mean"]