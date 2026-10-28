"""Talinah walkthrough v4: new animated intro and outro on top of the v3 edit (render.py).

Usage: same flags as render.py, e.g.
  python3 v4.py out.mp4 --to 9          # intro clip with VO
  python3 v4.py out.mp4 --from 80 --to 91.9
  python3 v4.py prev_dir --preview 5 --to 9
"""
import subprocess

import cv2
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFilter

import pii
import render as R
from render import CH, CW, FPS, GREEN, H, W, blend_rgba, ease, ease_out, font

LIGHT_GREEN = (118, 214, 140)
INK = (24, 52, 33)

# On-screen type now carries these lines, so they no longer get a caption.
R.CAPS = [c for c in R.CAPS if c[2] not in (
    'Meet Talinah.', 'Hiring, powered by AI.', 'Hire smarter with Talinah.', 'Book your demo at talinah.com.')]
R.APP_IN = (4.2, 7.6)
R.APP_OUT = (81.1, 85.8)
R.END = 93.9  # end card held 2 s longer so the QR code can be scanned


# ---------------------------------------------------------------- helpers
def clean_content(part, src_t):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{src_t:.3f}', '-i', R.SRC[part], '-frames:v', '1',
                        '-vf', f'crop={CW}:{CH}:0:10', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
                       stdout=subprocess.PIPE, check=True)
    fr = np.frombuffer(p.stdout, np.uint8).reshape(CH, CW, 3).copy()
    return pii.blur(fr, pii.detect(fr, part, src_t))


def window_image(content):
    rgb, alpha, shadow, pad = R.LAYERS
    win = rgb.copy()
    win[R.BAR:] = content
    return win, alpha, shadow, pad


def comp_window(out, content, sc, dx, dy, shadow=1.0):
    """Composite the browser window holding `content` at window->frame scale sc, offset dx,dy."""
    win, alpha, sh, pad = window_image(content)
    if sc < 0.7:  # pre-shrink with area filtering so small UI doesn't shimmer
        ww, hh = max(2, round(R.WIN_W * sc)), max(2, round(R.WIN_H * sc))
        win = cv2.resize(win, (ww, hh), interpolation=cv2.INTER_AREA)
        alpha = cv2.resize(alpha, (ww, hh), interpolation=cv2.INTER_AREA)
        sh = cv2.resize(sh, (round(sh.shape[1] * sc), round(sh.shape[0] * sc)), interpolation=cv2.INTER_AREA)
        s_win = sc / (ww / R.WIN_W)  # residual scale, ~1
    else:
        s_win = sc
    s = R.warp_rgba(sh, s_win, dx - pad * sc, dy - pad * sc) * shadow
    out *= (1 - s[..., None])
    a = R.warp_rgba(alpha, s_win, dx, dy)[..., None]
    w = R.warp_rgba(win, s_win, dx, dy).astype(np.float32)
    return out * (1 - a) + w * a


def rounded_card(img_bgr, radius=18):
    """White-bordered rounded card: returns BGR uint8 + alpha float (same size)."""
    h, w = img_bgr.shape[:2]
    m = Image.new('L', (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), radius * 2, fill=255)
    alpha = np.array(m.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
    out = img_bgr.copy()
    edge = Image.new('L', (w * 2, h * 2), 0)
    ImageDraw.Draw(edge).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), radius * 2, outline=255, width=4)
    e = np.array(edge.resize((w, h), Image.LANCZOS)).astype(np.float32)[..., None] / 255
    out = (out * (1 - e) + np.array([226, 233, 227], np.float32) * e).astype(np.uint8)
    return out, alpha


def draw_quad(out, img, alpha, quad, opacity=1.0, shadow=0.32):
    """Perspective-warp a card onto the frame. quad: 4 dst points (tl, tr, br, bl)."""
    h, w = img.shape[:2]
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    M = cv2.getPerspectiveTransform(src, np.float32(quad))
    if shadow:
        sq = np.float32(quad) + np.float32([0, 22])
        Ms = cv2.getPerspectiveTransform(src, sq)
        sa = cv2.warpPerspective(alpha, Ms, (W, H), borderValue=0)
        sa = cv2.GaussianBlur(cv2.resize(sa, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 7)
        sa = cv2.resize(sa, (W, H), interpolation=cv2.INTER_LINEAR) * shadow * opacity
        out *= (1 - sa[..., None])
    a = cv2.warpPerspective(alpha, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)[..., None] * opacity
    c = cv2.warpPerspective(img, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0).astype(np.float32)
    return out * (1 - a) + c * a


def tilt_quad(cx, cy, w, h, tilt):
    """Card rotated about its vertical axis; tilt>0 pushes the left edge away."""
    k = 1 - abs(tilt)
    ww = w * (1 - abs(tilt) * 0.35)
    far, near = h * k, h
    lh, rh = (far, near) if tilt > 0 else (near, far)
    x0, x1 = cx - ww / 2, cx + ww / 2
    return [(x0, cy - lh / 2), (x1, cy - rh / 2), (x1, cy + rh / 2), (x0, cy + lh / 2)]


def words_layer(words, f, colors):
    """Render each word on its own transparent strip, with x offsets from the full-line layout."""
    d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    line = ' '.join(words)
    total = d.textlength(line, font=f)
    hgt = int(f.size * 1.45)
    out, pos = [], 0
    for wd, col in zip(words, colors):
        x = d.textlength(line[:pos], font=f)
        wdt = int(d.textlength(wd, font=f)) + 8
        im = Image.new('RGBA', (wdt, hgt), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((2, 0), wd, font=f, fill=col + (255,))
        out.append((np.array(im), x))
        pos += len(wd) + 1
    return out, total, hgt


def letters_layer(text, f, col=(255, 255, 255)):
    d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    total = d.textlength(text, font=f)
    hgt = int(f.size * 1.4)
    out = []
    for i, ch in enumerate(text):
        x = d.textlength(text[:i], font=f)
        im = Image.new('RGBA', (int(d.textlength(ch, font=f)) + 40, hgt), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20, 0), ch, font=f, fill=col + (255,))
        out.append((np.array(im), x - 20))
    return out, total, hgt


def scale_rgba(img, s):
    if abs(s - 1) < 1e-3:
        return img
    h, w = img.shape[:2]
    return cv2.resize(img, (max(1, round(w * s)), max(1, round(h * s))),
                      interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)


# ---------------------------------------------------------------- background light
_yy, _xx = np.mgrid[0:H * 2:4, 0:W * 2:4].astype(np.float32)
_BLOB = np.exp(-(((_xx - W) / 620) ** 2 + ((_yy - H) / 420) ** 2))
_BLOB = cv2.resize(_BLOB, (W * 2, H * 2))[..., None] * np.array([46, 92, 40], np.float32)  # BGR, green-ish


def dark_live(t):
    """Dark-green backdrop with a slow light sweep drifting across it."""
    cx = int(330 + 1250 * ease((t + 0.4) / 9.0)) if t < 20 else int(1500 - 1100 * ease((t - 85.0) / 7.0))
    cy = 400
    ox, oy = W - cx, H - cy
    return R.DARK + _BLOB[oy:oy + H, ox:ox + W] * 0.55


# ---------------------------------------------------------------- intro assets
WM_FONT = font(600, 156)
WM_LETTERS, WM_W, WM_H = letters_layer('Talinah', WM_FONT)
WM_FULL = np.array(R.text_rgba([('Talinah', WM_FONT, (255, 255, 255, 255), 0)]))
TAG_WORDS, TAG_W, TAG_H = words_layer(['Hiring,', 'powered', 'by', 'AI.'], font(500, 56),
                                      [(255, 255, 255)] * 3 + [LIGHT_GREEN])
TAG_T = [4.95, 5.72, 6.18, 6.42]

_snap = clean_content(1, 41.5)
CARD_L = rounded_card(_snap[190:576, 370:1312])
_score = clean_content(1, 109.0)
CARD_R = rounded_card(_score[0:720, 1452:1888])

MID_W = 760
MID_SC = MID_W / R.WIN_W
MID_CX, MID_CY = W / 2, 712


def mid_affine(t):
    sc = MID_SC
    dy = MID_CY - R.WIN_H * sc / 2 + 4 * np.sin(t * 1.3)
    return sc, MID_CX - R.WIN_W * sc / 2, dy


def intro(t, readers, state):
    push = ease((t - 6.9) / 0.7)
    out = BG(t)
    if push > 0:
        out = out * (1 - push) + R.MINT * push

    # wordmark: letters build on the first "Talinah", glow on the second, then it moves up
    move = ease((t - 4.1) / 0.8)
    s = (1 + 0.04 * ease((t - 0.6) / 3.5)) * (1 - 0.42 * move)  # slow push while the VO pauses
    cy = 470 - 236 * move - 50 * push
    fade_out = 1 - ease((t - 6.95) / 0.45)
    line_u = ease_out((t + 0.3) / 0.55) * (1 - ease((t - 4.0) / 0.5))
    if line_u > 0:
        half = 300 * line_u
        cv2.line(out, (int(W / 2 - half), 588), (int(W / 2 + half), 588), (90, 181, 60), 3, cv2.LINE_AA)
    wm = np.zeros((WM_H, int(WM_W) + 80, 4), np.uint8)
    for i, (img, x) in enumerate(WM_LETTERS):
        u = ease_out((t - 0.02 - i * 0.075) / 0.4)
        if u <= 0:
            continue
        y = int(18 * (1 - u))
        x0 = int(x) + 40
        reg = wm[y:y + img.shape[0], x0:x0 + img.shape[1]]
        src = img[:reg.shape[0], :reg.shape[1]].astype(np.float32)
        a = src[..., 3:4] / 255 * u
        reg[..., :3] = (reg[..., :3] * (1 - a) + src[..., :3] * a).astype(np.uint8)
        reg[..., 3] = np.maximum(reg[..., 3], (src[..., 3] * u).astype(np.uint8))
    sweep = (t - 3.35) / 0.8
    if 0 < sweep < 1:
        xs = np.arange(wm.shape[1], dtype=np.float32)
        pos = -120 + (wm.shape[1] + 240) * ease(sweep)
        band = np.exp(-((xs - pos) / 70) ** 2)[None, :]
        glow = wm[..., 3].astype(np.float32) / 255 * band
        wm = wm.copy()
        wm[..., :3] = np.clip(wm[..., :3] * (1 - glow[..., None] * 0.35)
                              + np.array([200, 255, 215]) * glow[..., None] * 0.6, 0, 255).astype(np.uint8)
        halo = cv2.GaussianBlur(glow, (0, 0), 14) * 0.8
        hrgba = np.dstack([np.full(halo.shape + (3,), GLOW_COL, np.uint8), (halo * 255).astype(np.uint8)])
        hs = scale_rgba(hrgba, s)
        blend_rgba(out, hs, int(W / 2 - hs.shape[1] / 2), int(cy - hs.shape[0] / 2), fade_out)
    ws = scale_rgba(wm, s)
    blend_rgba(out, ws, int(W / 2 - ws.shape[1] / 2), int(cy - ws.shape[0] / 2), fade_out)

    # tagline, word by word, AI in green
    ty = 352 - 50 * push
    for (img, x), ts in zip(TAG_WORDS, TAG_T):
        u = ease_out((t - ts) / 0.35)
        if u > 0:
            blend_rgba(out, img, int(W / 2 - TAG_W / 2 + x), int(ty - TAG_H / 2 + 14 * (1 - u)), u * fade_out)

    # product cards
    for side, card, start, cx in ((-1, CARD_L, 4.3, 352), (1, CARD_R, 4.6, 1588)):
        u = ease_out((t - start) / 0.65)
        if u <= 0:
            continue
        img, al = card
        cw = 520 if side < 0 else 262
        ch = cw * img.shape[0] / img.shape[1]
        drift = 6 * np.sin(t * 1.1 + side)
        x = cx + side * 520 * push
        q = tilt_quad(x, 712 + 60 * (1 - u) + drift, cw, ch, 0.16 * -side)
        out = draw_quad(out, img, al, q, u * (1 - push))

    u = ease_out((t - 4.45) / 0.65)
    if u > 0:
        content = R.app_content(t, readers, state)  # holds the first dashboard frame until 7.1
        sc, dx, dy = mid_affine(t)
        dy += 60 * (1 - u)
        if push > 0:
            sc2, dx2, dy2 = R.cam_affine(*R.camera(7.6))
            sc, dx, dy = sc + (sc2 - sc) * push, dx + (dx2 - dx) * push, dy + (dy2 - dy) * push
        tmp = comp_window(out.copy(), content, sc, dx, dy)
        out = out * (1 - u) + tmp * u
    return out


# ---------------------------------------------------------------- outro assets
SLOT_W, GAP = 340, 18
SLOT_SC = SLOT_W / R.WIN_W
SLOT_H = R.WIN_H * SLOT_SC
SLOT_X0 = (W - (5 * SLOT_W + 4 * GAP)) / 2
SLOT_Y = 372
LABELS = ['Dashboard', 'AI Insights', 'Scheduling', 'Scorecard', 'Offer']
TRACK_Y = int(SLOT_Y + SLOT_H + 58)
REACH = [82.05, 82.75, 83.45, 84.15, 84.85]

SLOT_CONTENT = [clean_content(1, 2.4), _snap, clean_content(1, 89.5), clean_content(1, 161.0)]
LABEL_IMG = {(lab, on): np.array(R.text_rgba([(lab, font(600 if on else 500, 27),
                                               (INK if on else (125, 150, 132)) + (255,), 0)]))
             for lab in LABELS for on in (False, True)}


def _ring():
    pad = 8
    im = Image.new('RGBA', ((SLOT_W + 2 * pad) * 2, (int(SLOT_H) + 2 * pad) * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((2, 2, im.width - 3, im.height - 3), 26, outline=GREEN + (255,), width=7)
    return np.array(im.resize((im.width // 2, im.height // 2), Image.LANCZOS)), pad


RING, RING_PAD = _ring()
HEAD_WORDS, HEAD_W, HEAD_H = words_layer(['Hire', 'smarter', 'with', 'Talinah'], font(600, 92),
                                         [(255, 255, 255)] * 3 + [LIGHT_GREEN])
HEAD_T = [85.82, 86.12, 86.48, 86.7]


def _qr():
    q = qrcode.QRCode(border=1, box_size=11, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data('https://talinah.com')
    q.make(fit=True)
    img = q.make_image(fill_color=(20, 56, 32), back_color=(255, 255, 255)).convert('RGB')  # whole-pixel modules
    qs = img.width
    tw, th = qs + 60, qs + 100
    tile = Image.new('RGBA', (tw + 24, th + 32), (0, 0, 0, 0))
    sh = Image.new('L', tile.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((12, 20, 12 + tw, 20 + th), 26, fill=110)
    tile.paste((0, 20, 8, 255), mask=sh.filter(ImageFilter.GaussianBlur(11)))
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle((12, 8, 12 + tw, 8 + th), 26, fill=(255, 255, 255, 255))
    tile.paste(img, (42, 38))
    d.text((12 + tw // 2, 8 + th - 34), 'Scan to book a demo', font=font(600, 26), fill=INK + (255,), anchor='mm')
    return np.array(tile)


QR = _qr()


def _button():
    img = Image.new('RGBA', (520, 160), (0, 0, 0, 0))
    sh = Image.new('L', img.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((40, 36, 480, 140), 52, fill=110)
    img.paste((0, 30, 10, 255), mask=sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((40, 24, 480, 128), 52, fill=GREEN + (255,))
    d.text((260, 76), 'Book a demo', font=font(600, 42), fill=(255, 255, 255, 255), anchor='mm')
    return np.array(img)


BTN = _button()
URL = np.array(R.text_rgba([('talinah.com', font(500, 42), (218, 238, 223, 255), 0)]))


def slot_affine(i):
    return SLOT_SC, SLOT_X0 + i * (SLOT_W + GAP), SLOT_Y


def outro_row(t, readers, state):
    out = BG(t)
    # track under the row
    show = ease_out((t - 81.6) / 0.5)
    x_first = SLOT_X0 + SLOT_W / 2
    x_last = SLOT_X0 + 4 * (SLOT_W + GAP) + SLOT_W / 2
    if show > 0:
        cv2.line(out, (int(x_first), TRACK_Y), (int(x_last), TRACK_Y),
                 tuple(float(c) for c in (205, 228, 210)), 4, cv2.LINE_AA)
        prog = np.interp(t, [REACH[0], REACH[-1]], [x_first, x_last])
        if t >= REACH[0]:
            cv2.line(out, (int(x_first), TRACK_Y), (int(prog), TRACK_Y), (90, 181, 60), 5, cv2.LINE_AA)
    for i in range(5):
        u = 1.0 if i == 4 else ease_out((t - 81.3 - 0.13 * i) / 0.55)
        sc, dx, dy = slot_affine(i)
        if i == 4:
            k = ease((t - 81.1) / 0.95)
            sc0, dx0, dy0 = R.cam_affine(*R.camera(min(t, 81.1)))
            sc, dx, dy = sc0 + (sc - sc0) * k, dx0 + (dx - dx0) * k, dy0 + (dy - dy0) * k
            content = R.app_content(t, readers, state)
        else:
            content = SLOT_CONTENT[i]
            dy += 40 * (1 - u)
        if u <= 0:
            continue
        on = t >= REACH[i]
        if on:
            pop = ease_out((t - REACH[i]) / 0.3)
            blend_rgba(out, RING, int(dx - RING_PAD), int(dy - RING_PAD), pop)
        tmp = comp_window(out.copy(), content, sc, dx, dy, shadow=0.8)
        out = out * (1 - u) + tmp * u if u < 1 else tmp
        if show > 0:
            cx = int(SLOT_X0 + i * (SLOT_W + GAP) + SLOT_W / 2)
            r = 9 + (3 * (1 - ease((t - REACH[i]) / 0.35)) if on else 0)
            col = (90, 181, 60) if on else (205, 228, 210)
            cv2.circle(out, (cx, TRACK_Y), int(r), col, -1, cv2.LINE_AA)
            if on:
                cv2.circle(out, (cx, TRACK_Y), 4, (255, 255, 255), -1, cv2.LINE_AA)
            lab = LABEL_IMG[(LABELS[i], on)]
            blend_rgba(out, lab, cx - lab.shape[1] // 2, TRACK_Y + 22, show)
    return out


def outro(t, readers, state):
    if t < 85.0:
        return outro_row(t, readers, state)
    u = ease((t - 85.0) / 0.8)
    out = BG(t)
    if u < 1:
        row = outro_row(t, readers, state)
        row = np.roll(row, int(110 * u), axis=0)
        sig = 1 + 14 * u
        small = cv2.resize(row, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        blurred = cv2.resize(cv2.GaussianBlur(small, (0, 0), sig / 4), (W, H))
        row = row * (1 - min(1, u * 2.5)) + blurred * min(1, u * 2.5)
        out = row * (1 - u) + out * u
    hy = 405
    for (img, x), ts in zip(HEAD_WORDS, HEAD_T):
        w = ease_out((t - ts) / 0.38)
        if w > 0:
            blend_rgba(out, img, int(W / 2 - HEAD_W / 2 + x), int(hy - HEAD_H / 2 + 16 * (1 - w)), w)
    b = ease_out((t - 87.78) / 0.4)
    if b > 0:
        pulse = 1 + 0.05 * np.sin(np.pi * min(1, max(0, (t - 88.5) / 0.5)))
        s = (0.86 + 0.14 * b) * pulse
        btn = scale_rgba(BTN, s)
        ring = (t - 88.5) / 0.7
        if 0 < ring < 1:
            rr = Image.new('RGBA', (620, 240), (0, 0, 0, 0))
            e = 26 * ease_out(ring)
            ImageDraw.Draw(rr).rounded_rectangle((90 - e, 66 - e, 530 + e, 170 + e), 52 + e,
                                                 outline=LIGHT_GREEN + (int(200 * (1 - ring)),), width=3)
            blend_rgba(out, np.array(rr), W // 2 - 310, 556 - 118)
        blend_rgba(out, btn, int(W / 2 - btn.shape[1] / 2), int(556 - btn.shape[0] / 2 + 6), b)
    u = ease_out((t - 89.05) / 0.45)
    if u > 0:
        url = URL
        blend_rgba(out, url, W // 2 - url.shape[1] // 2, int(650 + 12 * (1 - u)), u)
    q = ease_out((t - 88.3) / 0.6)
    if q > 0:
        blend_rgba(out, QR, W - 64 - QR.shape[1], int(H - 48 - QR.shape[0] + 20 * (1 - q)), q)
    return out


# ---------------------------------------------------------------- background styles
import backgrounds  # noqa: E402

BG = dark_live
GLOW_COL = (170, 255, 190)


def set_style(name):
    """Swap the backdrop and re-colour the on-screen type to suit it."""
    global BG, WM_LETTERS, TAG_WORDS, HEAD_WORDS, URL, GLOW_COL
    light = name in ('studio', 'ghost', 'wordmark', 'ribbons', 'gradient')
    text = (22, 94, 48) if light else (255, 255, 255)
    body = (24, 52, 33) if light else (255, 255, 255)
    accent = GREEN if light else LIGHT_GREEN
    backgrounds.GHOST_SOURCES = [SLOT_CONTENT[0], _snap, SLOT_CONTENT[3], SLOT_CONTENT[2]]
    backgrounds.WORDMARK_FONT = font(600, 520)
    BG = {'dark': dark_live, 'aurora': backgrounds.aurora, 'network': backgrounds.network,
          'studio': backgrounds.studio_illustrated, 'ghost': backgrounds.ghost,
          'wordmark': backgrounds.wordmark_bg, 'ribbons': backgrounds.ribbons,
          'gradient': backgrounds.gradient_plate}[name]
    GLOW_COL = (120, 220, 150) if light else (170, 255, 190)
    WM_LETTERS = letters_layer('Talinah', WM_FONT, text)[0]
    TAG_WORDS = words_layer(['Hiring,', 'powered', 'by', 'AI.'], font(500, 56), [body] * 3 + [accent])[0]
    HEAD_WORDS = words_layer(['Hire', 'smarter', 'with', 'Talinah'], font(600, 92), [body] * 3 + [accent])[0]
    URL = np.array(R.text_rgba([('talinah.com', font(500, 42), (body if light else (218, 238, 223)) + (255,), 0)]))


def frame_at(t, readers, state):
    if t < 7.6:
        out = intro(t, readers, state)
    elif t < 81.1:
        out = R.app_frame(t, readers, state)
    else:
        out = outro(t, readers, state)
    out = R.overlays(out, t)
    return np.clip(out, 0, 255).astype(np.uint8)


R.frame_at = frame_at

if __name__ == '__main__':
    import sys
    if '--style' in sys.argv:
        i = sys.argv.index('--style')
        set_style(sys.argv[i + 1])
        del sys.argv[i:i + 2]
    R.main()
