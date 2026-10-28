"""Find and blur personal data (emails, phone numbers, org ID, file names) in raw capture frames.

Frames are the raw capture cropped by CROP_Y rows at the top; templates are cut
from full raw frames, so only their pixels matter, not their coordinates.
"""
import os

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
CROP_Y = 10


def _tight(img, x0, x1, y0, y1, thr=200):
    c = img[y0:y1, x0:x1]
    ys = np.where((c < thr).any(1))[0]
    return img[y0 + ys[0] - 1:y0 + ys[-1] + 2, x0 - 1:x1 + 1].copy()


_list = cv2.imread(HERE + 'raw/r_23.5.png', 0)
_det = cv2.imread(HERE + 'raw/r_29.png', 0)
_dd = cv2.imread(HERE + 'raw/q_17.3.png', 0)
_dash = cv2.imread(HERE + 'raw/r_1.png', 0)

AT_TPLS = [
    _tight(_list, 534, 547, 422, 446),      # gray list email
    _tight(_det, 628, 643, 180, 204),       # header / green link email
    _tight(_dd, 630, 645, 472, 498, 150),   # interviewer dropdown (larger)
]
PHONE_TPL = _det[575:603, 412:436].copy()
ORG_TPL = _dash[214:238, 1543:1655].copy()


def _peaks(res, thr):
    if res.max() < thr:
        return []
    dil = cv2.dilate(res, np.ones((9, 9), np.uint8))
    ys, xs = np.where((res >= thr) & (res == dil))
    return list(zip(xs.tolist(), ys.tolist()))


def _extent(gray, x0, x1, y0, y1, gap=5, maxw=400, maxl=290):
    """Grow [x0,x1) left/right across a text line until a run of `gap` empty columns."""
    hgt, wid = gray.shape
    y0, y1 = max(0, y0), min(hgt, y1)
    lo, hi = max(0, x0 - 320), min(wid, x1 + 720)
    band = gray[y0:y1, lo:hi].astype(np.int16)
    med = np.median(band)
    ink = (np.abs(band - med) > 38).any(0)
    a = x0 - lo
    b = x1 - lo
    run = 0
    i = a
    while i > 0 and run < gap and a - i < maxl:
        i -= 1
        run = 0 if ink[i] else run + 1
    left = i + run
    run = 0
    j = b
    while j < len(ink) - 1 and run < gap and j - a < maxw:
        j += 1
        run = 0 if ink[j] else run + 1
    right = j - run + 1
    return lo + left, lo + right


def detect(frame_bgr, part, src_t):
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    rects = []
    for tpl in AT_TPLS:
        th, tw = tpl.shape
        res = cv2.matchTemplate(gray, tpl, cv2.TM_CCOEFF_NORMED)
        for x, y in _peaks(res, 0.78):
            l, r = _extent(gray, x, x + tw, y - 2, y + th + 2)
            rects.append((l - 5, y - 6, r + 5, y + th + 6))
    th, tw = PHONE_TPL.shape
    res = cv2.matchTemplate(gray, PHONE_TPL, cv2.TM_CCOEFF_NORMED)
    for x, y in _peaks(res, 0.8):
        l, r = _extent(gray, x + tw + 8, x + tw + 20, y, y + th, gap=14, maxw=300)
        rects.append((x + tw + 4, y - 3, max(r + 6, x + tw + 150), y + th + 3))
    th, tw = ORG_TPL.shape
    res = cv2.matchTemplate(gray, ORG_TPL, cv2.TM_CCOEFF_NORMED)
    for x, y in _peaks(res, 0.8):
        rects.append((x + tw - 2, y - 3, x + tw + 225, y + th + 3))
    if part == 2 and 135.0 <= src_t <= 142.5:
        # offer upload dialog: chosen file name (someone else's CV) in the input and file row
        rects.append((800, 400 - CROP_Y, 1205, 474 - CROP_Y))
        rects.append((720, 505 - CROP_Y, 1180, 575 - CROP_Y))
        if src_t >= 138.3:  # dialog shrinks and fades while closing
            rects.append((700, 380 - CROP_Y, 1250, 600 - CROP_Y))
    return rects


def blur(frame, rects):
    h, w = frame.shape[:2]
    for x0, y0, x1, y1 in rects:
        x0, y0, x1, y1 = max(0, int(x0)), max(0, int(y0)), min(w, int(x1)), min(h, int(y1))
        if x1 - x0 < 4 or y1 - y0 < 4:
            continue
        roi = frame[y0:y1, x0:x1]
        small = cv2.resize(roi, (max(1, (x1 - x0) // 7), max(1, (y1 - y0) // 7)), interpolation=cv2.INTER_AREA)
        soft = cv2.resize(small, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR)
        frame[y0:y1, x0:x1] = cv2.GaussianBlur(soft, (0, 0), 4)
    return frame
