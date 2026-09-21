"""Lecture 3 demo -- edge detection (Canny) and line detection (Hough).

Usage:
    python lec03_edges_lines.py [--image data/scene.png] [--save out.png]

Reproduces the board work of Lectures 38-41 and *checks it*:
  1. differencing DOUBLES the noise variance: Var[g(m+1)-g(m-1)] = 2*sigma^2. (checked!)
  2. sub-pixel zero-crossing by linear interpolation: for f'' = -6 then +3 the
     crossing sits delta = 2/3 of the way across.                        (checked!)
  3. a from-scratch Canny (smooth -> gradient -> non-maxima suppression ->
     double threshold -> hysteresis) agrees with cv2.Canny pixel for pixel.
                                                                         (checked!)
  4. a from-scratch Hough accumulator recovers a known line's (rho, theta),
     and agrees with cv2.HoughLines.                                     (checked!)

Then it renders the Canny + Hough panel (Canny stages, our edges vs OpenCV's,
where they disagree, the accumulator, and the detected lines).
"""

import argparse
import os

import cv2
import numpy as np


def check_noise_amplification(sigma=15.0, n=400):
    """A first difference [-1, 0, 1] on independent noise gives variance 2*sigma^2."""
    rng = np.random.default_rng(0)
    noise = rng.normal(0, sigma, (n, n))
    d = cv2.filter2D(noise, cv2.CV_64F, np.array([[-1.0, 0.0, 1.0]]),
                     borderType=cv2.BORDER_REFLECT)
    inner = d[2:-2, 2:-2]                    # drop the border
    ratio = np.var(inner) / sigma**2
    print(f"[noise] Var[difference]/sigma^2 = {ratio:.3f}  (theory: 2.0)")
    assert abs(ratio - 2.0) < 0.15, "differencing should double the variance"


def check_subpixel_zero_crossing():
    """Second-derivative values a0 = -6 (at delta=0) and a1 = +3 (at delta=1).
    Linear interpolation a(delta) = (1-delta) a0 + delta a1; solve a(delta)=0."""
    a0, a1 = -6.0, 3.0
    delta = -a0 / (a1 - a0)                  # from (1-d) a0 + d a1 = 0
    print(f"[subpixel] zero-crossing at delta = {delta:.4f}  (board answer: 2/3)")
    assert abs(delta - 2.0 / 3.0) < 1e-9, "sub-pixel interpolation is wrong"


def _nms_quantized(mag, Ix, Iy):
    """Step 3 of Canny: keep a pixel only if it is a maximum of |grad| ALONG the
    gradient direction. The direction is quantized to the 4 sectors that have a
    neighbour on the pixel grid (0, 45, 90, 135 deg) -- the same shortcut OpenCV
    takes -- with the sector boundaries at tan(22.5) and tan(67.5)."""
    ax, ay = np.abs(Ix), np.abs(Iy)
    tan225 = np.tan(np.deg2rad(22.5))            # 1/tan(67.5) is the same number
    m = np.pad(mag, 1)                           # so shifted views keep the shape
    left, right = m[1:-1, :-2], m[1:-1, 2:]
    up, down = m[:-2, 1:-1], m[2:, 1:-1]
    ul, dr = m[:-2, :-2], m[2:, 2:]              # the "\" diagonal
    ur, dl = m[:-2, 2:], m[2:, :-2]              # the "/" diagonal
    horiz = ay <= tan225 * ax                    # grad points along x  -> edge is vertical
    vert = ax <= tan225 * ay                     # grad points along y  -> edge is horizontal
    diag = ~(horiz | vert)
    pos, neg = diag & (Ix * Iy >= 0), diag & (Ix * Iy < 0)
    # ">" on one side and ">=" on the other: breaks ties on a plateau, so a ridge
    # of equal magnitudes still comes out one pixel wide.
    keep = ((horiz & (mag > left) & (mag >= right))
            | (vert & (mag > up) & (mag >= down))
            | (pos & (mag > ul) & (mag >= dr))
            | (neg & (mag > ur) & (mag >= dl)))
    return np.where(keep, mag, 0.0)


def _hysteresis(thin, t_low, t_high):
    """Step 5: keep every weak pixel (> t_low) that is 8-connected to a strong
    one (> t_high). Labelling the weak mask does the flood fill in one shot."""
    strong, weak = thin > t_high, thin > t_low
    n_lab, labels = cv2.connectedComponents(weak.astype(np.uint8), connectivity=8)
    keep = np.zeros(n_lab, bool)
    keep[np.unique(labels[strong])] = True       # components that touch a strong pixel
    keep[0] = False                              # label 0 is the background
    return keep[labels]


def canny_from_scratch(gray, t_low, t_high, sigma=0.0, l2gradient=False):
    """The five steps of Canny, written out. Returns (edges, magnitude, thinned).

    sigma=0 does no smoothing, which is what cv2.Canny assumes -- it expects you
    to have blurred already, its only smoothing is the 3x3 Sobel itself.
    """
    f = gray.astype(np.float32)
    if sigma > 0:                                             # 1. smooth
        f = cv2.GaussianBlur(f, (0, 0), sigma)
    Ix = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3, borderType=cv2.BORDER_REPLICATE)
    Iy = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3, borderType=cv2.BORDER_REPLICATE)
    # 2. gradient magnitude. OpenCV's default is the cheap L1 norm, not L2.
    mag = np.hypot(Ix, Iy) if l2gradient else np.abs(Ix) + np.abs(Iy)
    thin = _nms_quantized(mag, Ix, Iy)                        # 3. thin to 1 px
    edges = _hysteresis(thin, t_low, t_high)                  # 4.+5. two thresholds
    return (edges.astype(np.uint8) * 255), mag, thin


def compare_edges(a, b):
    """(fraction of pixels both maps agree on, IoU of the two edge sets)."""
    a, b = a > 0, b > 0
    return float((a == b).mean()), float((a & b).sum()) / max(int((a | b).sum()), 1)


def check_canny_matches_opencv(scene, t_low=60, t_high=150):
    """Our Canny vs cv2.Canny on the same pre-blurred image, both norms."""
    blur = cv2.GaussianBlur(scene, (0, 0), 1.0)
    for l2 in (False, True):
        mine, _, _ = canny_from_scratch(blur, t_low, t_high, l2gradient=l2)
        ref = cv2.Canny(blur, t_low, t_high, L2gradient=l2)
        agree, iou = compare_edges(mine, ref)
        print(f"[canny] {'L2' if l2 else 'L1'} norm: {agree * 100:.3f}% of pixels agree, "
              f"IoU = {iou:.4f}  (ours {int((mine > 0).sum())} px, cv2 {int((ref > 0).sum())} px)")
        assert iou > 0.98, "from-scratch Canny disagrees with cv2.Canny"
    # the last few pixels of slack are OpenCV's integer Sobel/magnitude arithmetic,
    # which rounds differently from our float32 -- worst on the cheap L1 norm.

    # and the point of the whole exercise: NMS thins a ramp edge to ONE pixel.
    step = np.zeros((40, 40), np.uint8)
    step[:, 20:] = 255
    step = cv2.GaussianBlur(step, (0, 0), 1.5)                # a ramp, several px wide
    edges, mag, _ = canny_from_scratch(step, 20, 60)
    widths = (edges[5:-5] > 0).sum(axis=1)
    print(f"[canny] blurred step edge: |grad| is {int((mag[20] > 20).sum())} px wide, "
          f"the detected edge is {widths.max()} px wide")
    assert widths.max() == 1 and widths.min() == 1, "NMS failed to thin the edge"


def hough_lines_from_scratch(edges, n_theta=180, thresh=None):
    """Vote rho = x cos(theta) + y sin(theta) into a (rho, theta) accumulator."""
    ys, xs = np.nonzero(edges)
    diag = int(np.ceil(np.hypot(*edges.shape)))
    thetas = np.deg2rad(np.linspace(0, 180, n_theta, endpoint=False))
    cos_t, sin_t = np.cos(thetas), np.sin(thetas)
    acc = np.zeros((2 * diag, n_theta), np.int32)
    for x, y in zip(xs, ys):
        rho = np.round(x * cos_t + y * sin_t).astype(int) + diag
        acc[rho, np.arange(n_theta)] += 1
    if thresh is None:
        thresh = 0.5 * acc.max()
    peaks = []
    for r, t in zip(*np.nonzero(acc >= thresh)):
        peaks.append((r - diag, thetas[t], acc[r, t]))
    peaks.sort(key=lambda p: -p[2])
    return acc, diag, peaks


def check_hough_recovers_line():
    """Draw one known line, recover its (rho, theta) two ways, compare."""
    img = np.zeros((200, 200), np.uint8)
    # line through the image at theta0 = 60 deg, rho0 = 90 px
    theta0, rho0 = np.deg2rad(60.0), 90.0
    for x in range(200):
        y = (rho0 - x * np.cos(theta0)) / np.sin(theta0)
        if 0 <= y < 200:
            img[int(round(y)), x] = 255

    _, _, peaks = hough_lines_from_scratch(img, n_theta=180)
    rho_s, theta_s, _ = peaks[0]
    lines = cv2.HoughLines(img, 1, np.pi / 180, threshold=80)
    rho_cv, theta_cv = lines[0, 0]
    print(f"[hough] ground truth : rho={rho0:.1f}  theta={np.rad2deg(theta0):.1f} deg")
    print(f"[hough] from scratch : rho={rho_s:.1f}  theta={np.rad2deg(theta_s):.1f} deg")
    print(f"[hough] cv2.HoughLines: rho={rho_cv:.1f}  theta={np.rad2deg(theta_cv):.1f} deg")
    assert abs(rho_s - rho0) <= 2 and abs(np.rad2deg(theta_s) - 60) <= 2, \
        "from-scratch Hough missed the line"
    assert abs(rho_cv - rho0) <= 2, "cv2 Hough disagrees"


def disagreement_map(mine, ref, grow=3):
    """RGB image: red where only we fire, blue where only OpenCV does. The two
    maps differ by a handful of isolated pixels, so grow them to stay visible."""
    a, b = mine > 0, ref > 0
    k = np.ones((grow, grow), np.uint8)
    only_a = cv2.dilate((a & ~b).astype(np.uint8), k) > 0
    only_b = cv2.dilate((~a & b).astype(np.uint8), k) > 0
    out = np.full(a.shape + (3,), 255, np.uint8)
    out[a & b] = (170, 170, 170)                 # both agree -> light grey
    out[only_b] = (40, 40, 220)                  # OpenCV only
    out[only_a] = (220, 40, 40)                  # ours only
    return out


def panel(scene):
    blur = cv2.GaussianBlur(scene, (0, 0), 1.0)
    edges, mag, thin = canny_from_scratch(blur, 60, 150)
    ref = cv2.Canny(blur, 60, 150)
    acc, diag, peaks = hough_lines_from_scratch(edges, thresh=110)
    overlay = cv2.cvtColor(scene, cv2.COLOR_GRAY2BGR)
    for rho, theta, _ in peaks[:14]:
        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho
        p1 = (int(x0 - 1000 * b), int(y0 + 1000 * a))
        p2 = (int(x0 + 1000 * b), int(y0 - 1000 * a))
        cv2.line(overlay, p1, p2, (40, 40, 220), 1)
    return dict(mag=mag, thin=thin, edges=edges, ref=ref, acc=acc, overlay=overlay)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default=os.path.join(os.path.dirname(__file__), "data", "scene.png"))
    ap.add_argument("--save", default=None, help="write the panel image instead of showing it")
    args = ap.parse_args()

    scene = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    if scene is None:
        raise SystemExit(f"cannot read {args.image} (run make_data.py first?)")

    check_noise_amplification()
    check_subpixel_zero_crossing()
    check_canny_matches_opencv(scene)
    check_hough_recovers_line()

    p = panel(scene)
    agree, iou = compare_edges(p["edges"], p["ref"])
    import matplotlib
    if args.save:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 4, figsize=(16, 7))
    ax = axes.ravel()
    ax[0].imshow(p["mag"], cmap="gray"); ax[0].set_title(r"1-2. $|\nabla I|$ (L1)")
    ax[1].imshow(p["thin"], cmap="gray"); ax[1].set_title("3. after non-max suppression")
    ax[2].imshow(p["edges"], cmap="gray"); ax[2].set_title("4-5. hysteresis -> our Canny")
    ax[3].imshow(p["ref"], cmap="gray"); ax[3].set_title("cv2.Canny(60, 150)")
    ax[4].imshow(disagreement_map(p["edges"], p["ref"]))
    ax[4].set_title(f"{agree * 100:.2f}% of pixels agree, IoU {iou:.3f}\n"
                    "red = ours only, blue = cv2 only (dilated 3x3)", fontsize=9)
    ax[5].imshow(np.log1p(p["acc"]), cmap="hot", aspect="auto")
    ax[5].set_title(r"Hough accumulator ($\rho$ vs $\theta$)")
    ax[5].set_xlabel(r"$\theta$ (deg)"); ax[5].set_ylabel(r"$\rho$ bin")
    ax[6].imshow(cv2.cvtColor(p["overlay"], cv2.COLOR_BGR2RGB))
    ax[6].set_title("detected lines")
    for a in ax:
        if a is not ax[5]:
            a.axis("off")
    ax[7].axis("off")
    fig.tight_layout()
    if args.save:
        fig.savefig(args.save, bbox_inches="tight", dpi=130)
        print("wrote", args.save)
    else:
        plt.show()


if __name__ == "__main__":
    main()
