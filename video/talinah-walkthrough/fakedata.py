"""Replace real personal data in the raw capture with consistent fake data, typeset in the app's own font (DM Sans).

Build step (once): OCR keyframes, find every text box holding a real name / email / phone / org ID, fit DM Sans size and
weight to it, and store a template of the original pixels plus how to draw the replacement.
Per frame: template-match each entry (tracked near its last position), paint the original out with the local
background and draw the fake text at the same baseline, size, weight and colour.
"""
import glob
import json
import os
import pickle
import re

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
DM = HERE + 'fonts/fontsource-dm-sans/package/files/dm-sans-latin-{w}-normal.woff2'
WEIGHTS = (400, 500, 600, 700)

def _load_subs():
    """Real -> fake pairs (longest first). They name real people, so they live in private/subs.json, which is
    git-ignored and never committed. See HANDOFF.md."""
    p = HERE + 'private/subs.json'
    if not os.path.exists(p):
        raise SystemExit('private/subs.json is missing: upload it (see HANDOFF.md)')
    return [tuple(x) for x in json.load(open(p))['subs']]


SUBS = _load_subs()


def _norm(s):
    return re.sub(r'\s+', '', s).lower()


def font(w, size):
    return ImageFont.truetype(DM.format(w=w), max(6, int(round(size))))


def _ink_amount(gray, bgv, fgv):
    span = fgv - bgv
    if abs(span) < 1:
        return np.zeros_like(gray, np.float32)
    return np.clip((gray.astype(np.float32) - bgv) / span, 0, 1)


def _render_amount(text, w, size):
    f = font(w, size)
    pad = int(size)
    im = Image.new('L', (int(f.getlength(text)) + 2 * pad, int(size * 2.2)), 0)
    ImageDraw.Draw(im).text((pad, pad // 2), text, font=f, fill=255, anchor='lt')
    a = np.array(im).astype(np.float32) / 255
    return a, pad, pad // 2


def _bbox(a, thr=0.5):
    ys, xs = np.where(a > thr)
    if len(xs) == 0:
        return None
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def fit_text(crop_bgr, text):
    """Return (weight, size, ink bbox in crop, bg BGR, fg BGR) for `text` drawn in DM Sans inside crop."""
    g = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    border = np.concatenate([g[0], g[-1], g[:, 0], g[:, -1]])
    bgv = float(np.median(border))
    diff = np.abs(g - bgv)
    fg_mask = diff > max(40, diff.max() * 0.6)
    if fg_mask.sum() < 5:
        return None
    fgv = float(np.median(g[fg_mask]))
    amt = _ink_amount(g, bgv, fgv)
    rows = amt.sum(1) > 0.6
    runs, start = [], None
    for i, r in enumerate(list(rows) + [False]):
        if r and start is None:
            start = i
        if not r and start is not None:
            runs.append((start, i))
            start = None
    if not runs:
        return None
    # merge runs split by a 1-row gap, keep the band with the most ink
    merged = [list(runs[0])]
    for a, b in runs[1:]:
        if a - merged[-1][1] <= 1:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    by0, by1 = max(merged, key=lambda r: amt[r[0]:r[1]].sum())
    band = np.zeros_like(amt)
    band[by0:by1] = amt[by0:by1]
    amt = band
    bb = _bbox(amt)
    if bb is None:
        return None
    x0, y0, x1, y1 = bb
    real_w = x1 - x0
    real_mass = amt[y0:y1, x0:x1].sum()
    best = None
    for w in WEIGHTS:
        lo, hi = 6.0, 90.0
        for _ in range(16):
            mid = (lo + hi) / 2
            a, _, _ = _render_amount(text, w, mid)
            b = _bbox(a)
            if b is None or (b[2] - b[0]) < real_w:
                lo = mid
            else:
                hi = mid
        size = (lo + hi) / 2
        a, _, _ = _render_amount(text, w, size)
        b = _bbox(a)
        mass = a[b[1]:b[3], b[0]:b[2]].sum()
        # at a fixed width a wrong weight changes the height, so height is the main test; ink mass breaks ties
        err = 3 * abs((b[3] - b[1]) / max(y1 - y0, 1) - 1) + abs(mass / max(real_mass, 1) - 1)
        if best is None or err < best[0]:
            best = (err, w, size)
    bgr_bg = np.median(np.concatenate([crop_bgr[0], crop_bgr[-1], crop_bgr[:, 0], crop_bgr[:, -1]]), axis=0)
    fg_px = crop_bgr[fg_mask]
    bgr_fg = np.median(fg_px, axis=0)
    return best[1], best[2], (x0, y0, x1, y1), bgr_bg, bgr_fg


def _render_line(text, w, size, col_bgr):
    """RGBA-like (BGR + alpha) sprite of `text` with its ink bbox top-left reported."""
    f = font(w, size)
    pad = int(size)
    im = Image.new('L', (int(f.getlength(text)) + 2 * pad, int(size * 2.2)), 0)
    ImageDraw.Draw(im).text((pad, pad // 2), text, font=f, fill=255, anchor='lt')
    a = np.array(im).astype(np.float32) / 255
    return a, pad, pad // 2


# ---------------------------------------------------------------- build
def build(out_path=HERE + 'fake_templates.pkl'):
    ocr = {}
    for f in glob.glob(HERE + 'kf/ocr_*.json'):
        ocr.update(json.load(open(f)))
    entries, seen = [], set()
    for t in sorted(ocr, key=float):
        frame = cv2.imread(HERE + f'kf/{t}.png')
        for (a, b, txt, score) in ocr[t]:
            raw = txt.strip()
            n = _norm(raw)
            for real, fake in SUBS:
                rn = _norm(real)
                if rn not in n:
                    continue
                if '@' not in real and not real[0].isdigit() and '@' in raw:
                    continue
                x0, y0 = a
                x1, y1 = b
                m = 6
                cx0, cy0, cx1, cy1 = max(0, x0 - m), max(0, y0 - m), min(frame.shape[1], x1 + m), min(frame.shape[0], y1 + m)
                crop = frame[cy0:cy1, cx0:cx1]
                # the full box text, cleaned of OCR icon junk at the start
                full = re.sub(r'^[^A-Za-z0-9]+', '', raw)
                fit = fit_text(crop, full)
                if fit is None:
                    continue
                w, size, (ix0, iy0, ix1, iy1), bg, fg = fit
                fnt = font(w, size)
                # locate the real substring inside the full string by layout widths
                idx = _norm(full).find(rn)
                # map normalised index back to the raw string
                pos, k = 0, 0
                while k < idx and pos < len(full):
                    if not full[pos].isspace():
                        k += 1
                    pos += 1
                while pos < len(full) and full[pos].isspace():
                    pos += 1
                end, k = pos, 0
                while k < len(rn) and end < len(full):
                    if not full[end].isspace():
                        k += 1
                    end += 1
                while end < len(full) and full[end] in '!.,:)':
                    fake = fake + full[end] if not fake.endswith(full[end]) else fake
                    end += 1
                prefix, sub = full[:pos], full[pos:end]
                a_full, px, py = _render_amount(full, w, size)
                bf = _bbox(a_full)
                xoff = fnt.getlength(prefix) if prefix else 0.0
                subw = fnt.getlength(sub)
                # x of the substring's left edge in crop coords (align rendered ink bbox to measured ink bbox)
                sx0 = ix0 + (px + xoff) - bf[0]
                sx1 = sx0 + subw
                # baseline-free placement: top of rendered layout box relative to ink top
                lay_top = iy0 - (bf[1] - py)
                tx0, tx1 = int(max(0, sx0 - 3)), int(min(crop.shape[1], sx1 + 4))
                if not full[end:].strip():
                    tx1 = int(min(crop.shape[1], max(tx1, ix1 + 4)))
                ty0, ty1 = int(max(0, iy0 - 3)), int(min(crop.shape[0], iy1 + 4))
                tpl = cv2.cvtColor(crop[ty0:ty1, tx0:tx1], cv2.COLOR_BGR2GRAY)
                if tpl.shape[1] < 8:
                    continue
                # skip near-duplicates, but keep visually different states of the same text (hover, underline, cursor)
                dup = False
                for o in entries:
                    if o.get('real') == real and o['tpl'].shape == tpl.shape:
                        if cv2.matchTemplate(tpl, o['tpl'], cv2.TM_CCOEFF_NORMED)[0, 0] > 0.93:
                            dup = True
                            break
                if dup:
                    continue
                entries.append(dict(
                    real=real, fake=fake, weight=w, size=size, tpl=tpl,
                    text_dx=sx0 - tx0, text_top=lay_top - ty0,   # where the layout box of the fake starts, in tpl coords
                    fg=fg.astype(np.float32), src=f'{t}', box=(cx0 + tx0, cy0 + ty0)))
                break
    # the HR user's photo in the sidebar -> initials avatar
    f0 = cv2.imread(HERE + 'kf/0.20.png')
    av = f0[846:896, 16:68]
    entries.append(dict(real='avatar', fake='NH', avatar=True, tpl=cv2.cvtColor(av, cv2.COLOR_BGR2GRAY),
                        src='0.20', box=(16, 846)))
    # initials bubble on the candidate page ("RE")
    f1 = cv2.imread(HERE + 'kf/29.00.png')
    ocr29 = ocr['29.00']
    for (a, b, txt, s) in ocr29:
        if txt.strip() == 'RE':
            cx, cy = (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
            r = 26
            bub = f1[cy - r:cy + r, cx - r:cx + r]
            entries.append(dict(real='RE', fake='MA', bubble=True, tpl=cv2.cvtColor(bub, cv2.COLOR_BGR2GRAY),
                                fg=np.array([60, 60, 60], np.float32), src='29.00', box=(cx - r, cy - r)))
    pickle.dump(entries, open(out_path, 'wb'))
    return entries


# ---------------------------------------------------------------- apply
class Faker:
    def __init__(self, path=HERE + 'fake_templates.pkl', thr=0.86):
        self.entries = pickle.load(open(path, 'rb'))
        self.thr = thr
        self.last = {}
        self.sprites = {}

    def _find(self, gray, i, e):
        tpl = e['tpl']
        # long strings stay distinctive when the cursor covers part of them (0.74 under cover vs <0.5 on other text)
        thr = self.thr if tpl.shape[1] < 200 else 0.66
        r = cv2.matchTemplate(gray, tpl, cv2.TM_CCOEFF_NORMED)
        if r.max() < thr:
            return []
        hits = []
        if r.max() >= thr:
            dil = cv2.dilate(r, np.ones((15, 15), np.uint8))
            ys, xs = np.where((r >= thr) & (r == dil))
            hits = [(int(x), int(y), float(r[y, x])) for x, y in zip(xs, ys)]
        hits += self._edge_hits(gray, tpl)
        return hits

    @staticmethod
    def _edge_hits(gray, tpl, thr=0.8):
        """Text half-hidden where it scrolls out of view: match the visible part of the template in the bands at the
        viewport bottom and just under the sticky page header, and return the full template's position."""
        th, tw = tpl.shape
        hits = []
        H_ = gray.shape[0]
        for part, y0, y1, shift in ((tpl[:int(th * 0.6)], H_ - th, H_, 0),             # entering at the bottom
                                    (tpl[th - int(th * 0.6):], 0, 150, th - int(th * 0.6))):  # under the top bar
            ph = part.shape[0]
            band = gray[max(0, y0):y1]
            if band.shape[0] < ph or ph < 6:
                continue
            r = cv2.matchTemplate(band, part, cv2.TM_CCOEFF_NORMED)
            if r.max() < thr:
                continue
            dil = cv2.dilate(r, np.ones((15, 15), np.uint8))
            ys, xs = np.where((r >= thr) & (r == dil))
            hits += [(int(x), int(y) + max(0, y0) - shift, float(r[y, x]) - 0.05) for x, y in zip(xs, ys)]
        return hits

    def _sprite(self, e):
        key = id(e)
        if key not in self.sprites:
            a, px, py = _render_amount(e['fake'], e['weight'], e['size'])
            self.sprites[key] = (a, px, py)
        return self.sprites[key]

    def apply(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hits = []
        for i, e in enumerate(self.entries):
            for (x, y, sc) in self._find(gray, i, e):
                th, tw = e['tpl'].shape
                hits.append((sc, e, x, y, x + tw, y + th))
        hits.sort(key=lambda h: -h[0])
        jobs, kept = [], []
        for sc, e, x0, y0, x1, y1 in hits:  # one replacement per spot: best-matching template wins
            clash = False
            for (a0, b0, a1, b1) in kept:
                iw = min(x1, a1) - max(x0, a0)
                ih = min(y1, b1) - max(y0, b0)
                if iw > 0 and ih > 0 and iw * ih > 0.3 * min((x1 - x0) * (y1 - y0), (a1 - a0) * (b1 - b0)):
                    clash = True
                    break
            if not clash:
                kept.append((x0, y0, x1, y1))
                jobs.append((e, x0, y0))
        out = frame.astype(np.float32)
        for e, x, y in jobs:
            th, tw = e['tpl'].shape
            if e.get('avatar'):
                self._avatar(out, x, y, tw, th, e['fake'])
                continue
            if e.get('bubble'):
                self._bubble(out, frame, x, y, tw, th, e['fake'])
                continue
            # paint out with the local background (median of the region's border, so hover tints survive)
            y0c, y1c = max(0, y), min(frame.shape[0], y + th)
            if y1c - y0c < 3:
                continue
            reg = frame[y0c:y1c, x:x + tw]
            bg = np.median(np.concatenate([reg[0], reg[-1], reg[:, 0], reg[:, -1]]), axis=0).astype(np.float32)
            out[y0c:y1c, x:x + tw] = bg
            a, px, py = self._sprite(e)
            gx = int(round(x + e['text_dx'] - px))
            gy = int(round(y + e['text_top'] - py))
            h, w = a.shape
            X0, Y0, X1, Y1 = max(0, gx), max(0, gy), min(out.shape[1], gx + w), min(out.shape[0], gy + h)
            if X1 <= X0 or Y1 <= Y0:
                continue
            aa = a[Y0 - gy:Y1 - gy, X0 - gx:X1 - gx][..., None]
            out[Y0:Y1, X0:X1] = out[Y0:Y1, X0:X1] * (1 - aa) + e['fg'] * aa
        return np.clip(out, 0, 255).astype(np.uint8)

    @staticmethod
    def _avatar(out, x, y, w, h, initials):
        cx, cy, r = x + w / 2, y + h / 2, min(w, h) / 2 - 2
        k = 4
        im = Image.new('RGBA', (int(w * k), int(h * k)), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse(((w / 2 - r) * k, (h / 2 - r) * k, (w / 2 + r) * k, (h / 2 + r) * k), fill=(46, 140, 80, 255))
        d.text((w / 2 * k, h / 2 * k), initials, font=font(600, r * 0.9 * k), fill=(255, 255, 255, 255), anchor='mm')
        im = np.array(im.resize((w, h), Image.LANCZOS)).astype(np.float32)
        a = im[..., 3:4] / 255
        out[y:y + h, x:x + w] = out[y:y + h, x:x + w] * (1 - a) + im[..., 2::-1] * a

    @staticmethod
    def _bubble(out, frame, x, y, w, h, initials):
        reg = frame[y:y + h, x:x + w].astype(np.float32)
        cy, cx = h // 2, w // 2
        fill = np.median(reg[cy - 6:cy + 6, cx - 14:cx - 8].reshape(-1, 3), axis=0)
        ink = reg.reshape(-1, 3)[np.argmin(reg.reshape(-1, 3).sum(1))]
        k = 4
        im = Image.new('L', (w * k, h * k), 0)
        ImageDraw.Draw(im).ellipse(((cx - 18) * k, (cy - 11) * k, (cx + 18) * k, (cy + 11) * k), fill=255)
        m = np.array(im.resize((w, h), Image.LANCZOS)).astype(np.float32)[..., None] / 255
        out[y:y + h, x:x + w] = out[y:y + h, x:x + w] * (1 - m) + fill * m
        t = Image.new('L', (w * k, h * k), 0)
        ImageDraw.Draw(t).text((cx * k, cy * k), initials, font=font(500, 17 * k), fill=255, anchor='mm')
        a = np.array(t.resize((w, h), Image.LANCZOS)).astype(np.float32)[..., None] / 255
        out[y:y + h, x:x + w] = out[y:y + h, x:x + w] * (1 - a) + ink * a


if __name__ == '__main__':
    es = build()
    for e in es:
        print(e['src'], e['real'][:30], '->', e['fake'], e.get('weight'), round(e.get('size', 0), 1), e['tpl'].shape)
