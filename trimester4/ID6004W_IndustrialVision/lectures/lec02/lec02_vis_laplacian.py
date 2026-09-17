import os
import cv2
import numpy as np

DIR = "."
F_PATH = os.path.join(DIR, "zero-crossing-original-values.npy")
LAP_PATH = os.path.join(DIR, "zero-crossing-laplacian-values.npy")
PATCH = 7    # odd -> this many array cells shown around the cursor, per side
CELL = 32    # on-screen size (px) of each magnified cell
SCALE = 4    # on-screen zoom of each panel in the main window
GAP = 8      # px between the two side-by-side panels

f = np.load(F_PATH)              # exact original intensities
lap = np.load(LAP_PATH)          # exact float64 Laplacian, no quantization
h, w = lap.shape
half = PATCH // 2
vext = np.abs(lap).max()


def diverging_bgr(vals):
    t = np.clip(vals / vext, -1, 1)
    out = np.full(vals.shape + (3,), 255, np.float64)
    pos, neg = t > 0, t < 0
    out[pos, 0] -= 255 * t[pos]; out[pos, 1] -= 255 * t[pos]        # white -> red
    out[neg, 1] += 255 * t[neg]; out[neg, 2] += 255 * t[neg]        # white -> blue
    return out.astype(np.uint8)


def gray_bgr(vals):
    g = np.clip(vals, 0, 255).astype(np.uint8)
    return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)


f_view = cv2.resize(gray_bgr(f), (w * SCALE, h * SCALE), interpolation=cv2.INTER_NEAREST)
lap_view = cv2.resize(diverging_bgr(lap), (w * SCALE, h * SCALE), interpolation=cv2.INTER_NEAREST)
panel_w = w * SCALE
main_view = np.full((h * SCALE, 2 * panel_w + GAP, 3), 40, np.uint8)
main_view[:, :panel_w] = f_view
main_view[:, panel_w + GAP:] = lap_view


def value_grid(vals, colors, x, y, fmt, fg_fn):
    x0, x1 = max(0, x - half), min(w, x + half + 1)
    y0, y1 = max(0, y - half), min(h, y + half + 1)
    sub = vals[y0:y1, x0:x1]
    rows, cols = sub.shape
    big = cv2.resize(colors[y0:y1, x0:x1], (cols * CELL, rows * CELL), interpolation=cv2.INTER_NEAREST)

    for j in range(rows):
        for i in range(cols):
            cv2.putText(big, fmt(sub[j, i]), (i * CELL + 1, j * CELL + CELL - 11),
                        cv2.FONT_HERSHEY_PLAIN, 0.85, fg_fn(sub[j, i]), 1, cv2.LINE_AA)
    for i in range(cols + 1):
        cv2.line(big, (i * CELL, 0), (i * CELL, big.shape[0]), (120, 120, 120), 1)
    for j in range(rows + 1):
        cv2.line(big, (0, j * CELL), (big.shape[1], j * CELL), (120, 120, 120), 1)

    cx, cy = x - x0, y - y0
    cv2.rectangle(big, (cx * CELL, cy * CELL), ((cx + 1) * CELL, (cy + 1) * CELL), (0, 215, 255), 2)
    return big, (x0, y0, rows, cols)


def magnify(x, y):
    f_big, _ = value_grid(f, gray_bgr(f), x, y,
                           lambda v: f"{v:.0f}",
                           lambda v: (0, 0, 0) if v > 128 else (255, 255, 255))
    lap_big, (x0, y0, rows, cols) = value_grid(lap, diverging_bgr(lap), x, y,
                                                lambda v: f"{v:+.1f}",
                                                lambda v: (150, 0, 0) if v > 0 else (0, 0, 150) if v < 0 else (0, 0, 0))

    # thick wall on the laplacian panel wherever the sign flips: the zero crossing
    sub = lap[y0:y0 + rows, x0:x0 + cols]
    for j in range(rows):
        for i in range(cols):
            if i + 1 < cols and (sub[j, i] > 0) != (sub[j, i + 1] > 0):
                cv2.line(lap_big, ((i + 1) * CELL, j * CELL), ((i + 1) * CELL, (j + 1) * CELL), (0, 0, 0), 3)
            if j + 1 < rows and (sub[j, i] > 0) != (sub[j + 1, i] > 0):
                cv2.line(lap_big, (i * CELL, (j + 1) * CELL), ((i + 1) * CELL, (j + 1) * CELL), (0, 0, 0), 3)

    gap = np.full((f_big.shape[0], GAP, 3), 40, np.uint8)
    return np.hstack([f_big, gap, lap_big])


def on_mouse(event, x, y, flags, param):
    if x < panel_w:
        ix = x // SCALE
    elif x >= panel_w + GAP:
        ix = (x - panel_w - GAP) // SCALE
    else:
        return
    iy = y // SCALE
    if 0 <= ix < w and 0 <= iy < h:
        cv2.imshow("pixel values  (left: f, right: Laplacian)", magnify(ix, iy))


cv2.imshow("f  |  Laplacian", main_view)
cv2.setMouseCallback("f  |  Laplacian", on_mouse)
on_mouse(cv2.EVENT_MOUSEMOVE, (w // 2) * SCALE, (h // 2) * SCALE, 0, None)
cv2.waitKey(0)
cv2.destroyAllWindows()
