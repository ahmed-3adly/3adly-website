"""Animated backdrops for the v4 intro/outro. Each returns a BGR float32 frame for VO time t."""
import os

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
W, H = 1920, 1080
_rng = np.random.default_rng(11)
_GRAIN = [_rng.normal(0, 1, (H, W, 1)).astype(np.float32) for _ in range(4)]


def _grain(t, amp):
    return _GRAIN[int(t * 12) % 4] * amp


def _blobs(t, blobs, base, sw=240, sh=135):
    """Sum of drifting soft gaussian colour fields, computed small and upscaled (they are smooth)."""
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    img = np.ones((sh, sw, 3), np.float32) * np.array(base, np.float32)
    for (cx, cy, r, col, ax, ay, sp, ph) in blobs:
        x = (cx + ax * np.sin(t * sp + ph)) * sw
        y = (cy + ay * np.cos(t * sp * 0.8 + ph)) * sh
        g = np.exp(-(((xx - x) / (r * sw)) ** 2 + ((yy - y) / (r * sw)) ** 2))[..., None]
        img = img * (1 - g * 0.85) + np.array(col, np.float32) * g * 0.85
    return cv2.resize(img, (W, H), interpolation=cv2.INTER_CUBIC)


# ---------------------------------------------------------------- A: aurora mesh (dark, rich, moving colour)
_AURORA = [  # cx, cy, radius, BGR colour, drift x, drift y, speed, phase
    (0.18, 0.25, 0.30, (78, 168, 38), 0.10, 0.08, 0.35, 0.0),     # emerald
    (0.82, 0.30, 0.28, (110, 150, 20), 0.08, 0.10, 0.28, 1.7),    # teal
    (0.55, 0.85, 0.32, (60, 120, 24), 0.12, 0.06, 0.31, 3.1),     # deep green
    (0.70, 0.62, 0.18, (120, 222, 150), 0.10, 0.10, 0.42, 4.4),   # lime highlight
    (0.30, 0.70, 0.20, (96, 190, 70), 0.09, 0.07, 0.38, 2.2),
]


def aurora(t):
    img = _blobs(t, _AURORA, (16, 40, 12))
    yy = np.linspace(-1, 1, H, dtype=np.float32)[:, None]
    xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
    vign = 1 - 0.45 * np.clip(xx ** 2 * 0.6 + yy ** 2, 0, 1)
    return img * vign[..., None] + _grain(t, 3.0)


# ---------------------------------------------------------------- B: talent network (dark + connected nodes)
_N = 64
_P = _rng.uniform([-0.05, -0.05], [1.05, 1.05], (_N, 2)).astype(np.float32)
_V = _rng.normal(0, 0.012, (_N, 2)).astype(np.float32)
_Z = _rng.uniform(0.35, 1.0, _N).astype(np.float32)  # depth: brightness and size
_HUB = _rng.choice(_N, 7, replace=False)
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_NET_BASE = None


def _net_base():
    global _NET_BASE
    if _NET_BASE is None:
        r = np.sqrt(((_xx - 960) / 1100) ** 2 + ((_yy - 520) / 700) ** 2)
        t = np.clip(r, 0, 1)
        t = t * t * (3 - 2 * t)
        c0, c1 = np.array([34, 70, 18], np.float32), np.array([10, 22, 7], np.float32)
        img = c0 + (c1 - c0) * t[..., None]
        for x in range(0, W, 48):  # faint dot grid
            for y in range(0, H, 48):
                img[y:y + 2, x:x + 2] += 10
        _NET_BASE = img
    return _NET_BASE


def network(t):
    img = _net_base().copy()
    p = (_P + _V * t) % 1.1 - 0.05
    pts = np.stack([p[:, 0] * W, p[:, 1] * H], 1)
    lay = np.zeros((H, W, 3), np.float32)
    for i in range(_N):
        d = np.linalg.norm(pts[i + 1:] - pts[i], axis=1)
        for j in np.where(d < 260)[0]:
            k = i + 1 + j
            a = float((1 - d[j] / 260) * min(_Z[i], _Z[k]) * 70)
            cv2.line(lay, tuple(int(v) for v in pts[i]), tuple(int(v) for v in pts[k]), (a * 0.55, a, a * 0.5), 1, cv2.LINE_AA)
    for i in range(_N):
        x, y = (int(v) for v in pts[i])
        hub = i in _HUB
        pulse = 0.5 + 0.5 * np.sin(t * 2.2 + i) if hub else 0
        r = int(2 + 3 * _Z[i] + (3 if hub else 0))
        c = float(120 + 120 * _Z[i] + 60 * pulse)
        cv2.circle(lay, (x, y), r, (c * 0.55, c, c * 0.5), -1, cv2.LINE_AA)
        if hub:
            cv2.circle(lay, (x, y), int(r + 8 + 10 * pulse), (40, 90, 40), 1, cv2.LINE_AA)
    glow = cv2.GaussianBlur(cv2.resize(lay, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 4)
    lay += cv2.resize(glow, (W, H)) * 1.6
    return img + lay + _grain(t, 2.0)


# ---------------------------------------------------------------- C: light studio (mint, matches the app)
_STUDIO = [
    (0.12, 0.18, 0.30, (186, 236, 196), 0.06, 0.05, 0.30, 0.0),
    (0.88, 0.22, 0.26, (200, 240, 214), 0.06, 0.06, 0.26, 1.3),
    (0.78, 0.86, 0.34, (150, 222, 168), 0.08, 0.05, 0.28, 2.6),
    (0.22, 0.82, 0.24, (214, 246, 226), 0.07, 0.05, 0.33, 3.9),
]
_STUDIO_GRID = None


def studio(t):
    global _STUDIO_GRID
    img = _blobs(t, _STUDIO, (242, 251, 244))
    if _STUDIO_GRID is None:
        g = np.zeros((H, W, 1), np.float32)
        for x in range(24, W, 40):
            for y in range(24, H, 40):
                g[y:y + 2, x:x + 2] = 1
        fade = np.exp(-(((_xx - 960) / 900) ** 2 + ((_yy - 540) / 520) ** 2))[..., None]
        _STUDIO_GRID = g * (1 - fade * 0.8)
    return img - _STUDIO_GRID * np.array([40, 26, 38], np.float32) + _grain(t, 1.2)


# ---------------------------------------------------------------- C+: light studio with faded hiring illustration
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

_INK = (34, 120, 62)  # RGB line colour for the icons


def _icon(kind, s=64, sw=4):
    """Line-art icon drawn at 4x and downsampled for clean strokes."""
    k = 4
    im = Image.new('RGBA', (s * k, s * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = sw * k
    c = _INK + (255,)

    def P(*v):
        return [x * k for x in v]

    if kind == 'person':
        d.ellipse(P(22, 10, 42, 30), outline=c, width=w)
        d.arc(P(12, 34, 52, 74), 200, 340, fill=c, width=w)
    elif kind == 'calendar':
        d.rounded_rectangle(P(10, 14, 54, 54), 6 * k, outline=c, width=w)
        d.line(P(10, 26, 54, 26), fill=c, width=w)
        d.line(P(22, 8, 22, 18), fill=c, width=w)
        d.line(P(42, 8, 42, 18), fill=c, width=w)
        for x in (21, 32, 43):
            for y in (36, 45):
                d.ellipse(P(x - 2, y - 2, x + 2, y + 2), fill=c)
    elif kind == 'doc':
        d.line(P(16, 8, 38, 8, 50, 20, 50, 56, 16, 56, 16, 8), fill=c, width=w, joint='curve')
        d.line(P(38, 8, 38, 20, 50, 20), fill=c, width=w, joint='curve')
        for y in (30, 38, 46):
            d.line(P(23, y, 43, y), fill=c, width=w)
    elif kind == 'check':
        d.ellipse(P(8, 8, 56, 56), outline=c, width=w)
        d.line(P(20, 33, 29, 42, 45, 24), fill=c, width=w, joint='curve')
    elif kind == 'chat':
        d.rounded_rectangle(P(8, 12, 56, 44), 10 * k, outline=c, width=w)
        d.line(P(18, 44, 16, 56, 30, 44), fill=c, width=w, joint='curve')
        for x in (22, 32, 42):
            d.ellipse(P(x - 2.5, 26.5, x + 2.5, 31.5), fill=c)
    elif kind == 'spark':
        pts = []
        for i in range(8):
            a = np.pi / 4 * i - np.pi / 2
            r = 24 if i % 2 == 0 else 7
            pts += [32 + r * np.cos(a), 32 + r * np.sin(a)]
        d.polygon(P(*pts), outline=c, width=w)
        d.ellipse(P(48, 8, 54, 14), fill=c)
    elif kind == 'search':
        d.ellipse(P(10, 10, 40, 40), outline=c, width=w)
        d.line(P(36, 36, 54, 54), fill=c, width=w + 2 * k)
    elif kind == 'case':
        d.rounded_rectangle(P(8, 20, 56, 52), 6 * k, outline=c, width=w)
        d.rounded_rectangle(P(24, 10, 40, 20), 3 * k, outline=c, width=w)
        d.line(P(8, 34, 56, 34), fill=c, width=w)
    return im.resize((s, s), Image.LANCZOS)


_LUCIDE = {'person': 'user-round', 'calendar': 'calendar-check', 'doc': 'file-text', 'check': 'clipboard-check',
           'chat': 'message-square-text', 'spark': 'sparkles', 'search': 'search', 'case': 'briefcase-business'}
_ICON_DIR = HERE + 'icons/'


def _badge(kind, r=44):
    """Soft-green circular badge holding a white Lucide icon, optically centred on its drawn pixels. Built at 4x."""
    k = 4
    size = (r * 2 + 40) * k
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    c = size // 2
    sh = Image.new('L', im.size, 0)
    ImageDraw.Draw(sh).ellipse((c - r * k, c - r * k + 6 * k, c + r * k, c + r * k + 6 * k), fill=60)
    im.paste((20, 70, 30, 255), mask=sh.filter(ImageFilter.GaussianBlur(10 * k)))
    d = ImageDraw.Draw(im)
    d.ellipse((c - r * k, c - r * k, c + r * k, c + r * k), fill=(96, 190, 120, 255),
              outline=(140, 210, 158, 255), width=2 * k)
    ic = Image.open(_ICON_DIR + _LUCIDE[kind] + '.png').convert('RGBA')
    ic = ic.crop(ic.getbbox())
    ic = Image.merge('RGBA', (*Image.new('RGB', ic.size, (255, 255, 255)).split(), ic.getchannel('A')))  # white icon
    side = r * k * 0.92  # icon box fills ~46% of the badge diameter
    sc = side / max(ic.size)
    ic = ic.resize((max(1, round(ic.width * sc)), max(1, round(ic.height * sc))), Image.LANCZOS)
    im.alpha_composite(ic, (c - ic.width // 2, c - ic.height // 2))
    im = im.resize((size // k, size // k), Image.LANCZOS)
    return np.array(im).astype(np.float32)


_CX, _CY = 960, 500
_RINGS = [(470, 250), (700, 380), (960, 520)]
# ring index, start angle, angular speed (rad/s), icon, badge radius
_BADGES = [
    (0, 0.30, 0.060, 'spark', 38), (0, 3.60, 0.060, 'person', 36),
    (1, 1.15, -0.045, 'calendar', 44), (1, 2.45, -0.045, 'chat', 40),
    (1, 4.30, -0.045, 'check', 42), (1, 5.55, -0.045, 'search', 40),
    (2, 0.75, 0.032, 'doc', 48), (2, 2.20, 0.032, 'case', 46),
    (2, 3.95, 0.032, 'person', 46), (2, 5.20, 0.032, 'spark', 42),
]
_SPRITES = {}
_RING_LAYER = None
_TEXT_MASK = None


def _ring_layer():
    """Dashed orbit ellipses as a float alpha mask."""
    m = Image.new('L', (W * 2, H * 2), 0)
    d = ImageDraw.Draw(m)
    for rx, ry in _RINGS:
        n = int((rx + ry) / 9)
        for i in range(n):
            a0, a1 = 360 * i / n, 360 * (i + 0.55) / n
            d.arc((2 * (_CX - rx), 2 * (_CY - ry), 2 * (_CX + rx), 2 * (_CY + ry)), a0, a1, fill=255, width=3)
    return np.array(m.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255


def _text_mask():
    """1 at the edges, falling to ~0.15 behind the centred titles so the art never fights the type."""
    r = ((_xx - 960) / 780) ** 2 + ((_yy - 450) / 300) ** 2
    return (0.1 + 0.9 * np.clip((r - 0.45) / 0.9, 0, 1))[..., None]


_QR_ZONE = np.clip(np.minimum((_xx - 1380) / 80, (_yy - 560) / 80), 0, 1)[..., None]


def studio_illustrated(t):
    global _RING_LAYER, _TEXT_MASK
    img = studio(t)
    if _RING_LAYER is None:
        _RING_LAYER = _ring_layer()
        _TEXT_MASK = _text_mask()
    lay = np.zeros((H, W, 3), np.float32)
    alpha = np.zeros((H, W, 1), np.float32)
    ring_a = _RING_LAYER[..., None] * 0.22
    lay += np.array([110, 175, 120], np.float32) * ring_a
    alpha += ring_a
    for ring, a0, w, kind, r in _BADGES:
        key = (kind, r)
        if key not in _SPRITES:
            _SPRITES[key] = _badge(kind, r)
        sp = _SPRITES[key]
        rx, ry = _RINGS[ring]
        a = a0 + w * t
        x = int(_CX + rx * np.cos(a) - sp.shape[1] / 2)
        y = int(_CY + ry * np.sin(a) - sp.shape[0] / 2 + 6 * np.sin(t * 0.9 + a0))
        x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + sp.shape[1]), min(H, y + sp.shape[0])
        if x1 <= x0 or y1 <= y0:
            continue
        s = sp[y0 - y:y1 - y, x0 - x:x1 - x]
        sa = s[..., 3:4] / 255
        lay[y0:y1, x0:x1] = lay[y0:y1, x0:x1] * (1 - sa) + s[..., 2::-1] * sa
        alpha[y0:y1, x0:x1] = alpha[y0:y1, x0:x1] * (1 - sa) + sa
    mask = _TEXT_MASK
    if t > 85.0:  # keep the orbiting badges clear of the QR code on the end card
        mask = mask * (1 - _QR_ZONE * min(1.0, (t - 85.0) / 1.5))
    a = np.clip(alpha, 0, 1) * mask * 0.55  # the whole illustration sits faded behind everything
    col = lay / np.maximum(alpha, 1e-3)
    return img * (1 - a) + col * a


# ---------------------------------------------------------------- D: ghost product (blurred UI at depth)
GHOST_SOURCES = []  # BGR screenshots, set by v4.py
_GHOSTS = None
# source index, width, centre x, centre y, blur sigma, opacity, drift x, drift y, tilt
_GHOST_LAYOUT = [
    (0, 860, 250, 200, 3.0, 0.62, 14, 8, 0.10),
    (1, 720, 1690, 210, 2.5, 0.66, -12, 10, -0.12),
    (2, 780, 330, 900, 4.0, 0.58, 12, -8, 0.08),
    (3, 820, 1640, 910, 5.0, 0.55, -10, -10, -0.10),
]


def _ghost_panels():
    out = []
    for src, w, cx, cy, sig, op, ddx, ddy, tilt in _GHOST_LAYOUT:
        img = GHOST_SOURCES[src]
        h = int(w * img.shape[0] / img.shape[1])
        im = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32)
        im = im * 0.78 + np.array([200, 236, 208], np.float32) * 0.22  # light wash toward mint
        m = Image.new('L', (w * 2, h * 2), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), 40, fill=255)
        a = np.array(m.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
        pad = 60
        im = cv2.copyMakeBorder(im, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        a = cv2.copyMakeBorder(a, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        hh, ww = a.shape
        k = abs(tilt)
        srcq = np.float32([[0, 0], [ww, 0], [ww, hh], [0, hh]])
        dq = np.float32([[0, hh * k / 2 if tilt > 0 else 0], [ww, 0 if tilt > 0 else hh * k / 2],
                         [ww, hh if tilt > 0 else hh * (1 - k / 2)], [0, hh * (1 - k / 2) if tilt > 0 else hh]])
        M = cv2.getPerspectiveTransform(srcq, dq)
        im = cv2.warpPerspective(im, M, (ww, hh))
        a = cv2.warpPerspective(a, M, (ww, hh))
        im = cv2.GaussianBlur(im * a[..., None], (0, 0), sig)
        a = cv2.GaussianBlur(a, (0, 0), sig)
        im = im / np.maximum(a[..., None], 1e-3)
        out.append((im, a * op, cx, cy, ddx, ddy))
    return out


_HALO = (np.exp(-(((_xx - 960) / 720) ** 2 + ((_yy - 440) / 300) ** 2)) * 0.85)[..., None]


def ghost(t):
    global _GHOSTS
    img = studio(t)
    if _GHOSTS is None:
        _GHOSTS = _ghost_panels()
    for im, a, cx, cy, ddx, ddy in _GHOSTS:
        hh, ww = a.shape
        x = int(cx - ww / 2 + ddx * np.sin(t * 0.25))
        y = int(cy - hh / 2 + ddy * np.cos(t * 0.21))
        x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + ww), min(H, y + hh)
        if x1 <= x0 or y1 <= y0:
            continue
        aa = a[y0 - y:y1 - y, x0 - x:x1 - x][..., None]
        img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - aa) + im[y0 - y:y1 - y, x0 - x:x1 - x] * aa
    return img * (1 - _HALO) + np.array([244, 252, 246], np.float32) * _HALO  # clean pool of light behind the type


# ---------------------------------------------------------------- E: giant outlined wordmark drifting
WORDMARK_FONT = None  # PIL font, set by v4.py
_WM_STRIP = None


def _wm_strip():
    f = WORDMARK_FONT
    word = 'Talinah  '
    d = ImageDraw.Draw(Image.new('L', (8, 8)))
    tw = int(d.textlength(word, font=f))
    h = int(f.size * 1.3)
    m = Image.new('L', (tw * 2, h), 0)
    dd = ImageDraw.Draw(m)
    dd.text((0, 0), word, font=f, fill=255)
    dd.text((tw, 0), word, font=f, fill=255)
    return np.array(m).astype(np.float32) / 255, tw


def wordmark_bg(t):
    """Giant tone-on-tone 'Talinah' sliding slowly along the bottom, cropped by the frame edge."""
    global _WM_STRIP
    img = studio(t)
    if _WM_STRIP is None:
        _WM_STRIP = _wm_strip()
    strip, tw = _WM_STRIP
    off = int((t * 26 + 260) % tw)
    seg = np.roll(strip, -off, axis=1)[:, :W]
    row_y = H - int(seg.shape[0] * 0.78)
    a = seg[:H - row_y][..., None] * 0.55
    col = np.array([196, 232, 205], np.float32)
    img[row_y:] = img[row_y:] * (1 - a) + col * a
    return img


# ---------------------------------------------------------------- F: flowing line ribbons
_XS = np.linspace(-80, W + 80, 220).astype(np.float32)


def ribbons(t):
    img = studio(t)
    lay = np.zeros((H, W), np.float32)
    for band, (base, amp, freq, sp, n, th) in enumerate((
            (800, 130, 0.0021, 0.35, 30, 2), (250, 90, 0.0027, -0.28, 22, 1))):
        for i in range(n):
            ph = t * sp + i * 0.05
            y = (base + (i - n / 2) * 8 + amp * np.sin(_XS * freq + ph)
                 + 0.4 * amp * np.sin(_XS * freq * 2.3 - ph * 1.7) - (_XS - W / 2) * 0.16 * (1 if band == 0 else -1))
            pts = np.stack([_XS, y], 1).astype(np.int32).reshape(-1, 1, 2)
            fade = 1 - abs(i - n / 2) / (n / 2)
            cv2.polylines(lay, [pts], False, float(0.3 + 0.7 * fade), th, cv2.LINE_AA)
    a = np.clip(lay, 0, 1)[..., None] * 0.6 * _ribbon_mask()
    col = np.array([92, 178, 74], np.float32)  # brand green (BGR)
    return img * (1 - a) + col * a


_RMASK = None


def _ribbon_mask():
    global _RMASK
    if _RMASK is None:
        r = ((_xx - 960) / 700) ** 2 + ((_yy - 450) / 260) ** 2
        _RMASK = (0.35 + 0.65 * np.clip((r - 0.4) / 0.8, 0, 1))[..., None]
    return _RMASK


# ---------------------------------------------------------------- G: Higgsfield gradient plate, animated here
_PLATE = None
_PLATE_PATH = HERE + 'hfbg/gradient.webp'  # generated with Higgsfield


def gradient_plate(t):
    """The generated gradient with a slow push-in, a gentle drift and the corner glows softly breathing."""
    global _PLATE
    if _PLATE is None:
        im = np.array(Image.open(_PLATE_PATH).convert('RGB'))[..., ::-1].astype(np.float32)
        _PLATE = cv2.resize(im, (int(W * 1.05), int(H * 1.05)), interpolation=cv2.INTER_AREA)
    ph, pw = _PLATE.shape[:2]
    local = t if t < 40 else t - 79.5  # each scene starts its own slow move
    z = 1.0 + 0.035 * np.sin(min(local, 14) / 14 * np.pi / 2)
    cx = pw / 2 + 18 * np.sin(local * 0.17)
    cy = ph / 2 + 10 * np.cos(local * 0.13)
    M = np.float32([[z, 0, W / 2 - cx * z], [0, z, H / 2 - cy * z]])
    img = cv2.warpAffine(_PLATE, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    # breathe the green: push saturation of the coloured corners up and down slightly
    grey = img.mean(axis=2, keepdims=True)
    k = 1.0 + 0.18 * np.sin(local * 0.6)
    return grey + (img - grey) * k + _grain(t, 1.0)
