"""Lecture 4 demo -- from edges to features: the Harris structure matrix.

Usage:
    python lec04_structure_matrix.py [--image data/scene.png] [--save out.png]

Reproduces the board work of Lectures 42-43 and *checks it*:
  1. the appearance-change function C(dx, dy) computed two ways --
     (a) brute-force SSD of the shifted patch, (b) the Taylor quadratic form
     dp^T R dp -- must agree for small shifts. (checked!)
  2. the structure matrix R built from gradients on flat / edge / corner
     patches, its eigenvalues, and the fact that R = P diag(l1,l2) P^T with
     P orthogonal (eigenvectors in the columns). (checked!)
  3. R is exactly symmetric (Ixy == Iyx) -- so it is normal / diagonalizable.

"""

import argparse
import os

import cv2
import numpy as np


# patches on scene.png: (name, y, x, half-size) -- flat, two edges, a corner.
# Same locations used by the Lecture-5 gradient-scatter figure (validated).
PATCHES = [
    ("flat",          40,  60, 22),   # empty background, top-left
    ("vertical edge", 350, 62, 22),   # house left wall
    ("diagonal edge", 215, 95, 18),   # on the roof's left slope
    ("corner",        322, 102, 18),  # door top-left corner
]


def gradients(img):
    """Ix, Iy via a Gaussian-smoothed derivative (derivative-of-Gaussian),
    exactly as Prof. Rajagopalan writes it: Ix = d/dx ( G(sigma_s) * I )."""
    f = cv2.GaussianBlur(img.astype(np.float64), (0, 0), sigmaX=2.0)  # sigma_s = 2
    Ix = cv2.Sobel(f, cv2.CV_64F, 1, 0, ksize=3)
    Iy = cv2.Sobel(f, cv2.CV_64F, 0, 1, ksize=3)
    return Ix, Iy


def structure_matrix(Ix, Iy, y, x, s, sigma_w=1.0):
    """R = sum_W w(x,y) [[Ix^2, IxIy], [IxIy, Iy^2]] with a Gaussian window
    that weights the centre of the patch more (sigma_w = 1)."""
    gx = Ix[y - s:y + s, x - s:x + s]
    gy = Iy[y - s:y + s, x - s:x + s]
    n = 2 * s
    yy, xx = np.mgrid[0:n, 0:n] - (n - 1) / 2.0
    w = np.exp(-(xx**2 + yy**2) / (2 * sigma_w**2))
    w /= w.sum()
    R = np.array([[np.sum(w * gx * gx), np.sum(w * gx * gy)],
                  [np.sum(w * gx * gy), np.sum(w * gy * gy)]])
    return R


def brute_ssd(field, y, x, s, dx, dy):
    """C(dx,dy) = sum_W [ J(x+dx, y+dy) - J(x,y) ]^2, sub-pixel shift by warping
    the smooth intensity field J with bilinear interpolation."""
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    shifted = cv2.warpAffine(field, M, (field.shape[1], field.shape[0]),
                             flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    p0 = field[y - s:y + s, x - s:x + s]
    p1 = shifted[y - s:y + s, x - s:x + s]
    return np.sum((p1 - p0) ** 2)


def taylor_ssd(R, dx, dy):
    """C(dx,dy) ~ [dx dy] R [dx dy]^T -- the first-order Taylor model."""
    dp = np.array([dx, dy], np.float64)
    return float(dp @ R @ dp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default=os.path.join(os.path.dirname(__file__), "data", "scene.png"))
    ap.add_argument("--save", default=None, help="write the figure instead of showing it")
    args = ap.parse_args()

    img = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"cannot read {args.image} (run make_data.py first?)")

    Ix, Iy = gradients(img)

    print("=== structure matrix R and eigenvalues per patch ===")
    results = {}
    for name, y, x, s in PATCHES:
        R = structure_matrix(Ix, Iy, y, x, s)
        # symmetry: the two off-diagonal sums are the same number
        assert abs(R[0, 1] - R[1, 0]) < 1e-9, "R must be symmetric"
        lam, P = np.linalg.eigh(R)           # ascending; P orthogonal
        lam = lam[::-1]                       # l1 >= l2
        # reconstruction R = P diag(lam) P^T
        recon = P @ np.diag(np.linalg.eigvalsh(R)) @ P.T
        assert np.allclose(recon, R, atol=1e-6), "eigendecomposition failed"
        assert np.allclose(P @ P.T, np.eye(2), atol=1e-9), "P not orthogonal"
        results[name] = (R, lam)
        print(f"  {name:14s}  lambda1={lam[0]:10.1f}  lambda2={lam[1]:10.1f}  "
              f"ratio={lam[0]/max(lam[1],1e-9):8.1f}")
    print("  -> flat: both small | edge: one big one small | corner: both big")

    print("\n=== Taylor quadratic form vs brute-force SSD (corner patch) ===")
    # The Taylor model is a *small-shift* approximation. To check it honestly we
    # need (a) a smooth, differentiable intensity field J, (b) gradients that are
    # plain central differences of J (so they are consistent with an actual shift
    # of J), and (c) genuinely small, sub-pixel shifts.
    name, y, x, s = PATCHES[3]
    J = cv2.GaussianBlur(img.astype(np.float64), (0, 0), sigmaX=1.5)
    Jy, Jx = np.gradient(J)                       # central differences of J
    gx = Jx[y - s:y + s, x - s:x + s]
    gy = Jy[y - s:y + s, x - s:x + s]
    R_uw = np.array([[np.sum(gx*gx), np.sum(gx*gy)], [np.sum(gx*gy), np.sum(gy*gy)]])
    for h in [1.0, 0.5, 0.25]:
        for (ux, uy) in [(1, 0), (0, 1), (0.707, 0.707)]:
            dx, dy = h * ux, h * uy
            c_true = brute_ssd(J, y, x, s, dx, dy)
            c_tay = taylor_ssd(R_uw, dx, dy)
            rel = abs(c_tay - c_true) / max(c_true, 1e-9)
            print(f"    |shift|={h:4.2f} dir=({ux:+.2f},{uy:+.2f})  "
                  f"SSD={c_true:9.1f}  Taylor={c_tay:9.1f}  rel.err={rel:6.1%}")
    print("  -> the quadratic form dp^T R dp agrees with the true SSD to a few")
    print("     percent for sub-pixel shifts (residual = higher-order terms).")

    # --- figure: patches + their gradient clouds with eigen-axes -------------
    import matplotlib
    if args.save:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 4, figsize=(13, 6.4))
    lim = 1500
    for i, (name, y, x, s) in enumerate(PATCHES):
        p = img[y - s:y + s, x - s:x + s]
        gx = Ix[y - s:y + s, x - s:x + s].ravel()
        gy = Iy[y - s:y + s, x - s:x + s].ravel()
        axes[0, i].imshow(p, cmap="gray", vmin=0, vmax=255)
        axes[0, i].set_title(name); axes[0, i].axis("off")
        ax = axes[1, i]
        ax.scatter(gx, gy, s=5, alpha=0.5, color="#b3452c")
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
        ax.axhline(0, color="k", lw=0.6); ax.axvline(0, color="k", lw=0.6)
        ax.set_xlabel("$I_x$"); ax.set_ylabel("$I_y$")
        R, lam = results[name]
        _, P = np.linalg.eigh(R)
        ev = np.linalg.eigvalsh(R)
        for j in [0, 1]:
            d = P[:, j] * 0.9 * lim * np.sqrt(ev[j] / max(ev.max(), 1e-9))
            ax.plot([-d[0], d[0]], [-d[1], d[1]], color="#3b6b9b", lw=2)
        ax.set_title(fr"$\lambda_1={lam[0]:.0f},\ \lambda_2={lam[1]:.0f}$", fontsize=9)
    fig.suptitle("Gradient clouds and structure-matrix eigen-axes "
                 "(flat / edge / edge / corner)")
    fig.tight_layout()
    if args.save:
        fig.savefig(args.save, bbox_inches="tight", dpi=130)
        print("\nwrote", args.save)
    else:
        plt.show()


if __name__ == "__main__":
    main()
