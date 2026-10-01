"""Lecture 5 demo -- Harris corners from scratch, exactly as derived in class.

Usage:
    python lec05_harris.py [--image data/scene.png] [--kappa 0.05]
                           [--rel-thresh 0.01] [--window box|gauss] [--save out.png]
    python lec05_harris.py --compare-windows     # box vs Gaussian, rotation test

Pipeline (each step is a slide):
  1. gradients Ix, Iy (Sobel = [1 2 1]' * [-1 0 1], so sigma_s is already here)
  2. structure matrix R = window-sum of [Ix^2, IxIy; IxIy, Iy^2]
     -- the window w is a box by default, to match cv2.cornerHarris; pass
        --window gauss for the circular Gaussian of L04 slide 13
  3. response M = det(R) - kappa * trace(R)^2      <- no eigen-decomposition!
  4. threshold (relative to max) + 3x3 non-maxima suppression
  5. sub-pixel refinement: one Newton step  delta = -H^{-1} grad f
Cross-checks our implementation against cv2.cornerHarris.
"""

import argparse
import os

import cv2
import numpy as np


def harris_response(gray, kappa=0.05, block=3, ksize=3, window="box", sigma_w=1.0,
                    sigma_s=0.0):
    """Response map M = det(R) - kappa*tr(R)^2.

    `window` selects the weighting w(x_i,y_i) in R = sum w * [Ix^2 IxIy; IxIy Iy^2]:
      "box"   -- uniform block x block, which is what cv2.cornerHarris uses;
                 pick this when you want the cross-check below to be meaningful.
      "gauss" -- the circular Gaussian of L04 slide 13, w = exp(-r^2/2 sigma_w^2),
                 which is what Harris and Stephens actually specified in 1988.
    The box window is anisotropic -- its corners reach sqrt(2) further than its
    edges -- so the corner strength is only approximately rotation-invariant.
    See --compare-windows for the measurement.

    `sigma_s` > 0 pre-smooths with G(sigma_s) before differencing, giving the
    derivative-of-Gaussian gradient of L04 slide 13. Bare Sobel (sigma_s = 0) is
    itself a crude, and slightly anisotropic, stand-in for the same thing.
    """
    f = gray.astype(np.float32) / 255.0
    if sigma_s > 0:
        f = cv2.GaussianBlur(f, (0, 0), sigma_s)
    Ix = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=ksize, scale=1.0 / 8)   # /8 = Sobel gain
    Iy = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=ksize, scale=1.0 / 8)
    # window-sum of the gradient products
    if window == "box":
        W = lambda a: cv2.boxFilter(a, -1, (block, block), normalize=False)
    else:
        # GaussianBlur normalises to unit mass; rescale so w peaks at 1, matching
        # the w = exp(-r^2 / 2 sigma_w^2) written on the slide.
        gain = 2 * np.pi * sigma_w ** 2
        W = lambda a: cv2.GaussianBlur(a, (0, 0), sigma_w) * gain
    Sxx, Syy, Sxy = W(Ix * Ix), W(Iy * Iy), W(Ix * Iy)
    det = Sxx * Syy - Sxy * Sxy
    tr = Sxx + Syy
    return det - kappa * tr * tr


def detect(resp, rel_thresh=0.01):
    """threshold at rel_thresh * max(M), then 3x3 non-maxima suppression"""
    T = resp.max() * rel_thresh
    local_max = cv2.dilate(resp, np.ones((3, 3), np.uint8))
    keep = (resp > T) & (resp >= local_max)
    ys, xs = np.nonzero(keep)
    return np.stack([xs, ys], axis=1)


def subpixel(resp, corners):
    """One Newton step per corner on the response surface (lecture kernels):
       fx ~ [1,0,-1]/2,  fxx ~ [1,-2,1],  fxy ~ cross-difference/4."""
    refined = []
    for x, y in corners:
        if not (1 <= x < resp.shape[1] - 1 and 1 <= y < resp.shape[0] - 1):
            refined.append((float(x), float(y)))
            continue
        w = resp[y - 1:y + 2, x - 1:x + 2].astype(np.float64)
        fx = (w[1, 2] - w[1, 0]) / 2
        fy = (w[2, 1] - w[0, 1]) / 2
        fxx = w[1, 2] - 2 * w[1, 1] + w[1, 0]
        fyy = w[2, 1] - 2 * w[1, 1] + w[0, 1]
        fxy = (w[2, 2] - w[2, 0] - w[0, 2] + w[0, 0]) / 4
        H = np.array([[fxx, fxy], [fxy, fyy]])
        if abs(np.linalg.det(H)) < 1e-12:
            refined.append((float(x), float(y)))
            continue
        d = -np.linalg.solve(H, np.array([fx, fy]))
        d = np.clip(d, -1, 1)          # the Taylor step is only valid locally
        refined.append((x + d[0], y + d[1]))
    return np.array(refined)


def show(title, bgr):
    """cv2.imshow only works on a GUI-enabled OpenCV build (headless wheels
    raise); fall back to matplotlib, which the other demos use anyway."""
    try:
        cv2.imshow(title, bgr)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except cv2.error:
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(9, 6))
        plt.imshow(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis("off")
        fig.tight_layout()
        plt.show()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default=os.path.join(os.path.dirname(__file__), "data", "scene.png"))
    ap.add_argument("--kappa", type=float, default=0.05)
    ap.add_argument("--rel-thresh", type=float, default=0.01)
    ap.add_argument("--window", choices=["box", "gauss"], default="box",
                    help="window w in R: 'box' matches cv2.cornerHarris, "
                         "'gauss' matches L04 slide 13 (Harris and Stephens 1988)")
    ap.add_argument("--sigma-w", type=float, default=1.0, help="only used by --window gauss")
    ap.add_argument("--save", default=None)
    args = ap.parse_args()


    gray = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise SystemExit(f"cannot read {args.image} (run make_data.py first?)")

    resp = harris_response(gray, kappa=args.kappa,
                           window=args.window, sigma_w=args.sigma_w)

    # cross-check against OpenCV's implementation (same block/ksize/kappa).
    # Only the box window can match it -- cv2.cornerHarris has no Gaussian option.
    ref = cv2.cornerHarris(np.float32(gray) / 255.0, 3, 3, args.kappa)
    corr = np.corrcoef(resp.ravel(), ref.ravel())[0, 1]
    if args.window == "box":
        print(f"[check] correlation with cv2.cornerHarris response: {corr:.6f} (should be ~1)")
    else:
        print(f"[check] correlation with cv2.cornerHarris response: {corr:.6f} "
              f"(expected < 1: OpenCV uses a box window, we used a Gaussian)")

    corners = detect(resp, args.rel_thresh)
    refined = subpixel(resp, corners)
    print(f"[detect] {len(corners)} corners "
          f"(kappa={args.kappa}, T={args.rel_thresh:.3f} * max M)")
    off = np.abs(refined - corners)
    print(f"[subpixel] mean |offset| = ({off[:, 0].mean():.3f}, {off[:, 1].mean():.3f}) px, "
          f"max = {off.max():.3f} px (must be <= 1)")

    vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    for (x, y), (rx, ry) in zip(corners, refined):
        cv2.circle(vis, (int(x), int(y)), 4, (0, 0, 230), 1)
        cv2.drawMarker(vis, (int(round(rx)), int(round(ry))), (0, 200, 0),
                       cv2.MARKER_CROSS, 5, 1)
    if args.save:
        cv2.imwrite(args.save, vis)
        print("wrote", args.save)
    else:
        show("Harris corners (red: grid max, green: sub-pixel)", vis)


if __name__ == "__main__":
    main()
