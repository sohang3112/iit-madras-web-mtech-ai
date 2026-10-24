"""Lecture 15, camera calibration: live Zhang calibration from a webcam.

The classroom version of the slide "The full calibration procedure". The webcam runs, the checkerboard printed by lec14_checkerboard_target.py is detected in every frame, and each press of SPACE captures a view. From the captured views the program shows, side by side, the linear Zhang solution written on the slides (H by the DLT of L13, two rows per view, V b = 0 by SVD, K by Cholesky of B^-1) and OpenCV's cv2.calibrateCamera, which is that same initialization followed by the nonlinear refinement the slides defer to L16. The singular values of V are printed after every capture so that the class can watch sigma_5 leave the numerical floor at the third view, exactly as in the zhang-rank figure.

Keys
  SPACE   capture the current view (only when the board is detected)
  d       drop the last captured view
  c       calibrate now (also runs automatically after every capture once n >= 3)
  u       toggle the undistorted view once a calibration exists
  s       save the calibration to data/lec14_target/webcam_calibration.npz
  q/ESC   quit

Every captured frame is also written to data/lec14_target/captures/,
Usage
  python lec14_live_calibration.py                         # default 9x6 corners, 25 mm squares, camera 0
  python lec14_live_calibration.py --square 24.6 --camera 1
  python lec14_live_calibration.py --images data/lec14_target/captures   # offline replay
"""

import argparse
import glob
import os
import sys
import time

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lec13_calibration import K_from_B, homography_dlt, nearest_rotation, pose_from_H, zhang_rows  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "lec14_target")
CAPTURES = os.path.join(OUT, "captures")


# --------------------------------------------------------------------------
# the linear solution of the slides, on real corners
# --------------------------------------------------------------------------

def zhang_linear(obj_xy, img_pts):
    """K by the slides' steps 2 and 3: DLT homographies, V b = 0, Cholesky of B^-1.

    Returns K, the singular values of V, and the list of H, or (None, sigma, Hs) when B is not positive definite, which is the failure mode the slides warn about.
    """
    Hs = [homography_dlt(obj_xy, p) for p in img_pts]
    V = np.vstack([zhang_rows(H) for H in Hs])
    _, sigma, Vt = np.linalg.svd(V)
    b = Vt[-1]
    B = np.array([[b[0], b[1], b[3]], [b[1], b[2], b[4]], [b[3], b[4], b[5]]])
    try:
        K = K_from_B(B)
    except np.linalg.LinAlgError:
        K = None
    return K, sigma, Hs


def zhang_reprojection_rms(K, Hs, obj_xy, img_pts):
    """Reprojection error of the linear solution, with each R projected onto SO(3) and no distortion."""
    err = []
    X = np.column_stack([obj_xy, np.zeros(len(obj_xy)), np.ones(len(obj_xy))])
    for H, p in zip(Hs, img_pts):
        R, t = pose_from_H(K, H)
        R = nearest_rotation(R)
        P = K @ np.column_stack([R, t])
        x = X @ P.T
        x = x[:, :2] / x[:, 2:3]
        err.append(((x - p) ** 2).sum(axis=1))
    return float(np.sqrt(np.concatenate(err).mean()))


# --------------------------------------------------------------------------
# detection and drawing
# --------------------------------------------------------------------------

def detect(gray, pattern):
    """Sub-pixel corners of the board, in the fixed order the asymmetric grid guarantees."""
    ok, corners = cv2.findChessboardCornersSB(gray, pattern, flags=cv2.CALIB_CB_EXHAUSTIVE | cv2.CALIB_CB_ACCURACY)
    if not ok:
        ok, corners = cv2.findChessboardCorners(gray, pattern, flags=cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ok:
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                       (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-3))
    return ok, (corners.reshape(-1, 2) if ok else None)


def put(img, text, y, color=(255, 255, 255), scale=0.55):
    # one pass of text on a translucent dark box. A thick black outline under thin text does not work portably:
    # some OpenCV builds (e.g. on Windows) advance Hershey glyphs by thickness, so the two passes drift apart.
    font, x = cv2.FONT_HERSHEY_SIMPLEX, 10
    (tw, th), base = cv2.getTextSize(text, font, scale, 1)
    x0, y0 = max(x - 4, 0), max(y - th - 4, 0)
    x1, y1 = min(x + tw + 4, img.shape[1]), min(y + base + 3, img.shape[0])
    if x1 > x0 and y1 > y0:
        roi = img[y0:y1, x0:x1]
        roi[:] = (roi * 0.35).astype(img.dtype)
    cv2.putText(img, text, (x, y), font, scale, color, 1, cv2.LINE_AA)


def fmt_K(K):
    return f"fx={K[0, 0]:7.1f}  fy={K[1, 1]:7.1f}  s={K[0, 1]:6.2f}  u0={K[0, 2]:6.1f}  v0={K[1, 2]:6.1f}"


class Session:
    def __init__(self, pattern, square, image_size, flags=0):
        self.pattern = pattern
        self.flags = flags                      # cv2.calibrateCamera flags
        self.image_size = image_size            # (w, h)
        cols, rows = pattern
        self.obj_xy = np.array([(c * square, r * square) for r in range(rows) for c in range(cols)], float)
        self.obj_xyz = np.column_stack([self.obj_xy, np.zeros(len(self.obj_xy))]).astype(np.float32)
        self.views = []                         # list of (N,2) float arrays
        self.result = None                      # dict, once calibrated

    def add(self, corners):
        self.views.append(corners.astype(float))

    def drop(self):
        if self.views:
            self.views.pop()
        if len(self.views) < 3:
            self.result = None

    def calibrate(self):
        n = len(self.views)
        Kz, sigma, Hs = zhang_linear(self.obj_xy, self.views)
        res = {"n": n, "sigma": sigma, "K_zhang": Kz}
        print(f"\n--- {n} view(s) ---")
        print("singular values of V:", " ".join(f"{s:.2e}" for s in sigma))
        if n < 3:
            print("fewer than three views: the null space of V is not one-dimensional and b is arbitrary")
        if Kz is not None:
            res["rms_zhang"] = zhang_reprojection_rms(Kz, Hs, self.obj_xy, self.views)
            print(f"Zhang linear    {fmt_K(Kz)}   rms {res['rms_zhang']:.2f} px")
        else:
            print("Zhang linear    B not positive definite")
        if n >= 3:
            obj = [self.obj_xyz] * n
            img = [v.astype(np.float32).reshape(-1, 1, 2) for v in self.views]
            rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj, img, self.image_size, None, None, flags=self.flags)
            res.update(rms_cv=rms, K_cv=K, dist=dist.ravel())
            print(f"OpenCV refined  {fmt_K(K)}   rms {rms:.2f} px")
            print("distortion (k1 k2 p1 p2 k3):", " ".join(f"{d:+.4f}" for d in res["dist"]))
            # the tilt of the board in each view: the angle between its normal and the optical axis.
            # Views under ~15 degrees add almost no rank; 30-45 degrees is what to aim for.
            tilts = [np.degrees(np.arccos(abs(cv2.Rodrigues(rv)[0][2, 2]))) for rv in rvecs]
            res["tilts"] = tilts
            print("board tilt per view (deg):", " ".join(f"{t:4.0f}" for t in tilts))
            # the linear solution is only an initializer: compare the two
            if Kz is not None:
                df = np.hypot(Kz[0, 0] - K[0, 0], Kz[1, 1] - K[1, 1])
                print(f"linear vs refined focal length differs by {df:.1f} px")
        self.result = res
        return res

    def save(self):
        if not self.result or "K_cv" not in self.result:
            print("nothing to save yet")
            return
        os.makedirs(OUT, exist_ok=True)
        path = os.path.join(OUT, "webcam_calibration.npz")
        np.savez(path, K=self.result["K_cv"], dist=self.result["dist"], image_size=np.array(self.image_size),
                 rms=self.result["rms_cv"], K_zhang_linear=self.result["K_zhang"])
        print("saved", path)


def overlay(frame, sess, ok, corners, undistort):
    h, w = frame.shape[:2]
    res = sess.result
    show = frame
    if undistort and res and "K_cv" in res:
        show = cv2.undistort(frame, res["K_cv"], res["dist"])
        put(show, "UNDISTORTED", h - 12, (0, 255, 255))
    else:
        # the footprint of every captured view, so that coverage of the image is visible
        for v in sess.views:
            hull = cv2.convexHull(v.astype(np.float32).reshape(-1, 1, 2)).astype(np.int32)
            cv2.polylines(show, [hull], True, (80, 200, 80), 1, cv2.LINE_AA)
        if ok:
            cv2.drawChessboardCorners(show, sess.pattern, corners.reshape(-1, 1, 2).astype(np.float32), True)

    n = len(sess.views)
    put(show, f"views: {n}   board: {'FOUND' if ok else 'not found'}   SPACE capture  d drop  c calib  u undistort  s save  q quit",
        22, (0, 255, 0) if ok else (80, 80, 255))
    if res is not None:
        sig = res["sigma"]
        floor = sig[-1] if len(sig) >= 6 else 0.0
        s5 = sig[4] if len(sig) >= 5 else 0.0
        rank_ok = res["n"] >= 3 and res["K_zhang"] is not None
        put(show, f"sigma_5 of V = {s5:.1e}  (sigma_6 = {floor:.1e})  rank {'OK' if rank_ok else 'DEFICIENT: need >= 3 views with different orientations'}",
            46, (0, 255, 0) if rank_ok else (0, 140, 255))
        if res["K_zhang"] is not None:
            put(show, "Zhang linear   " + fmt_K(res["K_zhang"]) + (f"   rms {res['rms_zhang']:.2f} px" if "rms_zhang" in res else ""), 70)
        if "K_cv" in res:
            put(show, "OpenCV refined " + fmt_K(res["K_cv"]) + f"   rms {res['rms_cv']:.2f} px", 94)
            d = res["dist"]
            put(show, f"distortion k1={d[0]:+.3f} k2={d[1]:+.3f} p1={d[2]:+.4f} p2={d[3]:+.4f} k3={d[4]:+.3f}", 118)
            put(show, "board tilts (deg): " + " ".join(f"{t:.0f}" for t in res["tilts"]), 142)
    return show


# --------------------------------------------------------------------------
# main loop, live or replayed
# --------------------------------------------------------------------------

def frames_from_camera(index, width, height):
    cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)           # a changing focal length is a changing K; ignored if unsupported
    if not cap.isOpened():
        raise SystemExit(f"cannot open camera {index}")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        yield frame
    cap.release()


def check_gui():
    """Fail before the class is watching, not after: opencv-python-headless has no imshow."""
    try:
        cv2.namedWindow("L14 calibration", cv2.WINDOW_AUTOSIZE)
    except cv2.error:
        raise SystemExit("this cv2 build has no GUI (opencv-python-headless is shadowing opencv-python); "
                         "run: pip uninstall -y opencv-python-headless && pip install --force-reinstall opencv-python")


def main():
    check_gui()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cols", type=int, default=9, help="inner corners across (default 9)")
    ap.add_argument("--rows", type=int, default=6, help="inner corners down (default 6)")
    ap.add_argument("--square", type=float, default=25.0, help="measured square size in mm (default 25)")
    ap.add_argument("--camera", type=int, default=0)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--images", help="directory of saved frames to replay instead of the camera")
    ap.add_argument("--k3", action="store_true",
                    help="also fit k3 (fixed at 0 by default: it is not determinable from a dozen webcam views)")
    args = ap.parse_args()
    pattern = (args.cols, args.rows)
    flags = 0 if args.k3 else cv2.CALIB_FIX_K3

    if args.images:
        paths = sorted(glob.glob(os.path.join(args.images, "*.png")) + glob.glob(os.path.join(args.images, "*.jpg")))
        if not paths:
            raise SystemExit(f"no images in {args.images}")
        print(f"replaying {len(paths)} images; SPACE steps to the next one and captures it")
        first = cv2.imread(paths[0])
        h, w = first.shape[:2]
        sess = Session(pattern, args.square, (w, h), flags)
        for p in paths:
            frame = cv2.imread(p)
            ok, corners = detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), pattern)
            if ok:
                sess.add(corners)
                if len(sess.views) >= 3:
                    sess.calibrate()
            else:
                print("no board in", p)
            cv2.imshow("L14 calibration", overlay(frame.copy(), sess, ok, corners, False))
            k = cv2.waitKey(0) & 0xFF
            if k in (ord("q"), 27):
                break
        if sess.result and "K_cv" in sess.result:
            sess.save()
        cv2.destroyAllWindows()
        return

    os.makedirs(CAPTURES, exist_ok=True)
    sess = None
    undistort = False
    last_capture = 0.0
    for frame in frames_from_camera(args.camera, args.width, args.height):
        if sess is None:
            h, w = frame.shape[:2]
            sess = Session(pattern, args.square, (w, h), flags)
            print(f"camera {args.camera} at {w}x{h}; looking for {pattern[0]}x{pattern[1]} inner corners of {args.square:g} mm squares")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ok, corners = detect(gray, pattern)

        show = overlay(frame.copy(), sess, ok, corners, undistort)
        if time.time() - last_capture < 0.4:         # a brief flash so the capture is visible from the back row
            cv2.rectangle(show, (0, 0), (show.shape[1] - 1, show.shape[0] - 1), (255, 255, 255), 12)
        cv2.imshow("L14 calibration", show)

        k = cv2.waitKey(1) & 0xFF
        if k in (ord("q"), 27):
            break
        elif k == ord(" ") and ok:
            sess.add(corners)
            last_capture = time.time()
            cv2.imwrite(os.path.join(CAPTURES, f"view_{len(sess.views):02d}.png"), frame)
            sess.calibrate()
        elif k == ord(" "):
            print("board not detected; hold it flat, fully in frame, and away from glare")
        elif k == ord("d"):
            sess.drop()
            if sess.views:
                sess.calibrate()
            print(f"dropped last view, {len(sess.views)} remain")
        elif k == ord("c") and sess.views:
            sess.calibrate()
        elif k == ord("u"):
            undistort = not undistort
        elif k == ord("s"):
            sess.save()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
