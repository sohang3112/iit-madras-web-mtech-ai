"""Lecture 1 demo -- image filtering and separability.

Usage:
    python lec01_filtering.py [--image data/scene.png] [--save out.png]

Reproduces the lecture's experiments:
  the filter zoo (box, Gaussian, Sobel, sharpen) applied to one image
"""

import argparse
import os
import time

import cv2
import numpy as np


def filter_zoo(img):
    sx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
    sy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
    return {
        "original": img,
        "box 3x3": cv2.blur(img, (3, 3)),
        "box 9x9": cv2.blur(img, (9, 9)),
        "Gaussian sigma=3": cv2.GaussianBlur(img, (19, 19), 3),
        "|Sobel x|": cv2.convertScaleAbs(sx, alpha=0.25),
        "|Sobel y|": cv2.convertScaleAbs(sy, alpha=0.25),
        "sharpen": cv2.filter2D(img, -1, np.array([[0, -1, 0],
                                                   [-1, 5, -1],
                                                   [0, -1, 0]], np.float32)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default=os.path.join(os.path.dirname(__file__), "data", "scene.png"))
    ap.add_argument("--save", default=None, help="write the panel image instead of showing it")
    args = ap.parse_args()

    img = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"cannot read {args.image} (run make_data.py first?)")

    panels = filter_zoo(img)
    import matplotlib
    if args.save:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    for ax, (name, p) in zip(axes.ravel(), panels.items()):
        ax.imshow(p, cmap="gray", vmin=0, vmax=255)
        ax.set_title(name)
    for ax in axes.ravel():
        ax.axis("off")
    fig.tight_layout()
    if args.save:
        fig.savefig(args.save, bbox_inches="tight", dpi=130)
        print("wrote", args.save)
    else:
        plt.show()


if __name__ == "__main__":
    main()
