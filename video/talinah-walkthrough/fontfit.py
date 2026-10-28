import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
F = os.path.dirname(os.path.abspath(__file__)) + '/fonts/'
FAMS = {'dm': F + 'fontsource-dm-sans/package/files/dm-sans-latin-{w}-normal.woff2',
        'jak': F + 'fontsource-plus-jakarta-sans/package/files/plus-jakarta-sans-latin-{w}-normal.woff2',
        'man': F + 'fontsource-manrope/package/files/manrope-latin-{w}-normal.woff2',
        'inter': None}


def ink(gray, bgv):
    return (np.abs(gray.astype(np.float32) - bgv) > 40)


def render_mask(text, path, size):
    f = ImageFont.truetype(path, size)
    im = Image.new('L', (int(f.getlength(text)) + 40, int(size * 2)), 0)
    ImageDraw.Draw(im).text((10, int(size * 0.3)), text, font=f, fill=255)
    a = np.array(im) > 100
    ys, xs = np.where(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def fit(crop_gray, text, fams=('dm', 'jak', 'man'), weights=(400, 500, 600, 700)):
    bgv = np.median(np.concatenate([crop_gray[0], crop_gray[-1], crop_gray[:, 0], crop_gray[:, -1]]))
    m = ink(crop_gray, bgv)
    ys, xs = np.where(m)
    m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = None
    for fam in fams:
        for w in weights:
            path = FAMS[fam].format(w=w)
            lo, hi = 8.0, 80.0
            for _ in range(18):
                mid = (lo + hi) / 2
                r = render_mask(text, path, mid)
                if r.shape[1] < m.shape[1]:
                    lo = mid
                else:
                    hi = mid
            r = render_mask(text, path, (lo + hi) / 2)
            rr = cv2.resize(r.astype(np.uint8), (m.shape[1], m.shape[0]), interpolation=cv2.INTER_AREA).astype(np.float32)
            score = np.corrcoef(rr.ravel(), m.astype(np.float32).ravel())[0, 1]
            hs = r.shape[0] / m.shape[0]
            if best is None or score > best[0]:
                best = (score, fam, w, round((lo + hi) / 2, 2), round(hs, 3))
    return best
