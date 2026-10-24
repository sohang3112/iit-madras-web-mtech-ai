"""Lecture 15, camera calibration: a printable checkerboard target.

Writes an A4-landscape PDF (and a 300 dpi PNG) of a checkerboard whose square size is known exactly, so that the world coordinates of its corners are known by construction, which is the second virtue of the planar target on the slides. The default is 10 x 7 squares of 25 mm, giving a 9 x 6 grid of inner corners. Odd-by-even is deliberate: a board with an asymmetric corner grid has no 180-degree ambiguity, so the detector orders the corners the same way in every view.

Print it at 100 % scale (no "fit to page"), on matte paper, and glue it to something flat and rigid. Then measure one square with a ruler and pass that number to lec14_live_calibration.py as --square.

Usage:  python lec14_checkerboard_target.py [--cols 10 --rows 7 --square 25]
"""

import argparse
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "lec14_target")

A4_MM = (297.0, 210.0)           # landscape
DPI = 300
MM = DPI / 25.4                  # pixels per millimetre


def draw_board(cols, rows, square_mm):
    W, H = (int(round(m * MM)) for m in A4_MM)
    img = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(img)

    board_w, board_h = cols * square_mm, rows * square_mm
    if board_w > A4_MM[0] - 20 or board_h > A4_MM[1] - 30:
        raise SystemExit(f"{cols}x{rows} squares of {square_mm} mm do not fit A4 landscape with margins")

    # centre the board, leaving room for the caption below it
    x0 = (A4_MM[0] - board_w) / 2
    y0 = (A4_MM[1] - board_h) / 2 - 5
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                x1, y1 = (x0 + c * square_mm) * MM, (y0 + r * square_mm) * MM
                x2, y2 = (x0 + (c + 1) * square_mm) * MM, (y0 + (r + 1) * square_mm) * MM
                d.rectangle([round(x1), round(y1), round(x2) - 1, round(y2) - 1], fill=0)

    # a 100 mm scale bar and a caption, so the printed scale can be checked with a ruler
    bar_y = (y0 + board_h + 8) * MM
    bar_x = (A4_MM[0] / 2 - 50) * MM
    d.rectangle([bar_x, bar_y, bar_x + 100 * MM, bar_y + 1.0 * MM], fill=0)
    for k in (0, 100):
        d.rectangle([bar_x + k * MM - 1, bar_y - 2 * MM, bar_x + k * MM + 1, bar_y + 3 * MM], fill=0)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", int(3.2 * MM))
    except OSError:
        font = ImageFont.load_default()
    caption = (f"DA3451 L14 calibration target: {cols} x {rows} squares of {square_mm:g} mm, "
               f"{cols - 1} x {rows - 1} inner corners. Bar below the board is 100 mm at 100 % print scale.")
    d.text((x0 * MM, bar_y + 4.5 * MM), caption, fill=0, font=font)
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cols", type=int, default=10, help="squares across (default 10)")
    ap.add_argument("--rows", type=int, default=7, help="squares down (default 7)")
    ap.add_argument("--square", type=float, default=25.0, help="square size in mm (default 25)")
    args = ap.parse_args()

    if (args.cols - 1) % 2 == (args.rows - 1) % 2:
        print("warning: the inner-corner grid is symmetric, so the board is 180-degree ambiguous; "
              "prefer one odd and one even count of squares")

    os.makedirs(OUT, exist_ok=True)
    img = draw_board(args.cols, args.rows, args.square)
    stem = os.path.join(OUT, f"checkerboard_{args.cols}x{args.rows}_{args.square:g}mm")
    img.save(stem + ".pdf", "PDF", resolution=DPI)
    img.save(stem + ".png", dpi=(DPI, DPI))
    print(f"wrote {stem}.pdf and .png  ({args.cols - 1} x {args.rows - 1} inner corners, "
          f"pattern size for OpenCV: ({args.cols - 1}, {args.rows - 1}))")


if __name__ == "__main__":
    main()
