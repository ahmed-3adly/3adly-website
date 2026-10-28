"""Talinah intro v6: closer to the reference's editorial style.

Neutral grotesk headlines (Inter Display Medium) with a muted italic-serif accent, a cool grey-white backdrop with
mint and pale-blue glows and a dot grid, mask-wipe line reveals, a header with step pills, and one large, crisp,
live AI Insights card rebuilt from Talinah's real data before pushing into the walkthrough.

Usage: python3 intro6.py out.mp4 --to 9.0
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import backgrounds
import render as R
import v4
from render import H, W, blend_rgba, ease, ease_out

v4.set_style('gradient')

HERE = R.HERE
SERIF = HERE + 'fonts/serif/package/files/instrument-serif-latin-400-italic.woff2'
INTER = '/usr/share/fonts/opentype/inter/'

INK = (31, 47, 40)        # soft green-grey ink (RGB)
SLATE = (108, 120, 136)   # muted slate for the "problem" line
SAGE = (70, 128, 94)      # muted green for the serif accent
BODY = (110, 122, 116)
LOGO = (28, 96, 54)
EYEBROW = (84, 132, 104)


def disp(weight, size):
    return ImageFont.truetype(INTER + f'InterDisplay-{weight}.otf', size)


def text(weight, size):
    return ImageFont.truetype(INTER + f'Inter-{weight}.otf', size)


def serif(size):
    return ImageFont.truetype(SERIF, size)


# ---------------------------------------------------------------- type helpers
def rich_line(segs, gap=0.26):
    """segs: [(word, font, RGB)] -> word sprites [(rgba, x)], width, height (sprites share one baseline)."""
    d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    asc = max(f.getmetrics()[0] for _, f, _ in segs)
    desc = max(f.getmetrics()[1] for _, f, _ in segs)
    hgt = asc + desc + 16
    base = asc + 4
    out, x = [], 0.0
    for i, (wd, f, col) in enumerate(segs):
        wdt = int(d.textlength(wd, font=f)) + 50
        im = Image.new('RGBA', (wdt, hgt), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((12, base), wd, font=f, fill=col + (255,), anchor='ls')
        out.append((np.array(im), x - 12))
        x += d.textlength(wd, font=f) + segs[0][1].size * gap
    return out, x, base


def tracked(s, f, col, track):
    d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    wdt = int(sum(d.textlength(c, font=f) + track for c in s)) + 20
    im = Image.new('RGBA', (wdt, int(f.size * 1.5)), (0, 0, 0, 0))
    dd, x = ImageDraw.Draw(im), 4
    for c in s:
        dd.text((x, 2), c, font=f, fill=col + (255,))
        x += d.textlength(c, font=f) + track
    return np.array(im)


def wipe(out, img, x, y, u, rise=None, opacity=1.0):
    """Mask-wipe reveal: the sprite slides up into place from behind an invisible edge at its own bottom."""
    if u <= 0:
        return
    h = img.shape[0]
    rise = h * 0.9 if rise is None else rise
    off = int(round(rise * (1 - u)))
    vis = img[:h - off] if off > 0 else img
    if vis.shape[0] <= 0:
        return
    blend_rgba(out, vis, int(x), int(y + off), opacity * min(1.0, u * 1.6))


def line_reveal(out, words, x0, y, starts, dur=0.55, opacity=1.0):
    for (img, x), ts in zip(words, starts):
        wipe(out, img, x0 + x, y, ease_out((T[0] - ts) / dur), opacity=opacity)


T = [0.0]
KEEP_HEADER = False     # showcase keeps the docked logo + pills on screen after the intro
DRAW_PROGRESS = True

# ---------------------------------------------------------------- assets
H1 = 142
HOOK1, _, HOOK1_B = rich_line([('Less', disp('Medium', H1), SLATE), ('guesswork.', disp('Medium', H1), SLATE)])
HOOK2, _, HOOK2_B = rich_line([('Better', disp('Medium', H1), INK), ('hires.', serif(176), SAGE)])
_d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
_gx = HOOK1[1][1] + 12
STRIKE = (_gx - 4, _gx + _d.textlength('guesswork.', font=disp('Medium', H1)) + 10)
STRIKE_Y = disp('Medium', H1).getmetrics()[0] + 4 - int(H1 * 0.30)

H2 = 112
MAIN1, _, MAIN1_B = rich_line([('Hiring,', disp('Medium', H2), INK)])
MAIN2, _, MAIN2_B = rich_line([('powered', disp('Medium', H2), INK), ('by', disp('Medium', H2), INK),
                         ('AI.', serif(140), SAGE)])
BODY1, _, BODY_B = rich_line([(w, text('Regular', 31), BODY) for w in 'Screen, interview and hire,'.split()])
BODY2, _, _ = rich_line([(w, text('Regular', 31), BODY) for w in 'all in one workspace.'.split()])
EYE_LOGO = tracked('THE AI HIRING COPILOT', text('SemiBold', 25), EYEBROW, 9)
EYE_MAIN = tracked('STEP 01  ·  SCREEN', text('SemiBold', 21), EYEBROW, 6)
WORDMARK = np.array(R.text_rgba([('Talinah', R.font(600, 210), LOGO + (255,), 0)]))
LEFT = 150


def _pills(active):
    f = text('Medium', 20)
    labels = ['01 Screen', '02 Interview', '03 Hire']
    d = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    ws = [int(d.textlength(s, font=f)) + 36 for s in labels]
    im = Image.new('RGBA', (sum(ws) + 10 * len(ws) + 4, 50), (0, 0, 0, 0))
    dd, x = ImageDraw.Draw(im), 2
    for i, (s, w) in enumerate(zip(labels, ws)):
        on = i == active
        dd.rounded_rectangle((x, 4, x + w, 44), 20, fill=(52, 110, 78, 255) if on else (255, 255, 255, 235),
                             outline=None if on else (226, 232, 228, 255), width=2)
        dd.text((x + w / 2, 24), s, font=f, fill=(255, 255, 255, 255) if on else (70, 84, 77, 255), anchor='mm')
        x += w + 10
    return np.array(im)


PILLS = _pills(0)


# ---------------------------------------------------------------- live AI Insights card (rebuilt UI)
CW_, CH_ = 860, 560
_SPARK = Image.open(HERE + 'icons/sparkles.png').convert('RGBA')
_SPARK = _SPARK.crop(_SPARK.getbbox()).resize((30, 30), Image.LANCZOS)


def ai_card(score_u, chip1, chip2):
    """The real AI Insights snapshot for this candidate, drawn crisp at 2x: Borderline, Hold, 69% match."""
    k = 2
    im = Image.new('RGB', (CW_ * k, CH_ * k), (255, 255, 255))
    d = ImageDraw.Draw(im)

    def P(*v):
        return [int(a * k) for a in v]

    def F(fn, w, s):
        return fn(w, s * k)

    im.paste(_SPARK.resize((30 * k, 30 * k), Image.LANCZOS), P(40, 38), _SPARK.resize((30 * k, 30 * k), Image.LANCZOS))
    d.text(P(82, 53), 'AI Insights', font=F(text, 'SemiBold', 24), fill=INK, anchor='lm')
    live = score_u < 1
    d.ellipse(P(CW_ - 214, 47, CW_ - 202, 59), fill=(230, 160, 40) if live else (60, 170, 90))
    d.text(P(CW_ - 194, 53), 'Analyzing CV' if live else 'Analysis ready', font=F(text, 'Medium', 19),
           fill=(110, 122, 116), anchor='lm')
    d.text(P(40, 112), 'Recruiter decision snapshot', font=F(disp, 'SemiBold', 36), fill=INK, anchor='lm')
    d.text(P(40, 152), 'Accountant Specialist  ·  applied Oct 21', font=F(text, 'Regular', 20), fill=BODY, anchor='lm')
    for x in range(40, CW_ - 40, 9):  # dotted divider like the reference
        d.ellipse(P(x, 186, x + 3, 189), fill=(214, 222, 217))

    # recommended action
    d.text(P(40, 228), 'RECOMMENDED ACTION', font=F(text, 'SemiBold', 15), fill=(130, 140, 135), anchor='lm')
    d.text(P(40, 282), 'Hold', font=F(disp, 'SemiBold', 58), fill=INK, anchor='lm')
    d.rounded_rectangle(P(40, 330, 178, 364), 17 * k, fill=(254, 243, 224))
    d.text(P(109, 347), 'Borderline', font=F(text, 'SemiBold', 18), fill=(176, 110, 20), anchor='mm')

    # match score with counting number and filling bar
    sx = 470
    d.text(P(sx, 228), 'MATCH SCORE', font=F(text, 'SemiBold', 15), fill=(130, 140, 135), anchor='lm')
    val = int(round(69 * score_u))
    d.text(P(sx, 285), f'{val}%', font=F(disp, 'SemiBold', 70), fill=INK, anchor='lm')
    d.text(P(sx + 150, 296), 'role fit', font=F(text, 'Regular', 20), fill=BODY, anchor='lm')
    d.rounded_rectangle(P(sx, 336, CW_ - 40, 348), 6 * k, fill=(238, 241, 239))
    fx = sx + (CW_ - 40 - sx) * 0.69 * score_u
    if fx > sx + 12:
        d.rounded_rectangle(P(sx, 336, fx, 348), 6 * k, fill=(232, 168, 44))

    # signals
    d.text(P(40, 410), 'SIGNALS', font=F(text, 'SemiBold', 15), fill=(130, 140, 135), anchor='lm')
    chips = [((40, 436, 368, 486), (229, 245, 234), (36, 120, 70), '✓  3 reasons it may work', chip1),
             ((384, 436, 700, 486), (253, 236, 236), (184, 52, 52), '!  3 things to validate', chip2)]
    for (x0, y0, x1, y1), bgc, fg, label, u in chips:
        if u <= 0:
            continue
        a = min(1.0, u)
        bgm = tuple(int(255 + (c - 255) * a) for c in bgc)
        fgm = tuple(int(255 + (c - 255) * a) for c in fg)
        d.rounded_rectangle(P(x0, y0, x1, y1), 25 * k, fill=bgm)
        d.text(P((x0 + x1) / 2, (y0 + y1) / 2), label, font=F(text, 'SemiBold', 20), fill=fgm, anchor='mm')
    d.text(P(40, 524), 'Suggested focus: hands-on QuickBooks / NetSuite experience', font=F(text, 'Regular', 19),
           fill=(120, 132, 126) if chip2 >= 1 else (255, 255, 255), anchor='lm')
    small = im.resize((CW_, CH_), Image.LANCZOS)
    return np.array(small)[..., ::-1].copy()


_m = Image.new('L', (CW_ * 2, CH_ * 2), 0)
ImageDraw.Draw(_m).rounded_rectangle((0, 0, CW_ * 2 - 1, CH_ * 2 - 1), 44, fill=255)
CARD_ALPHA = np.array(_m.resize((CW_, CH_), Image.LANCZOS)).astype(np.float32) / 255


def card_border(img):
    e = Image.new('L', (CW_ * 2, CH_ * 2), 0)
    ImageDraw.Draw(e).rounded_rectangle((0, 0, CW_ * 2 - 1, CH_ * 2 - 1), 44, outline=255, width=3)
    e = np.array(e.resize((CW_, CH_), Image.LANCZOS)).astype(np.float32)[..., None] / 255
    return (img * (1 - e) + np.array([224, 231, 227], np.float32) * e).astype(np.uint8)


_BORDER_CACHE = {}


# ---------------------------------------------------------------- backdrop: cool grey-white, mint + pale blue, dots
_GLOWS = [  # cx, cy, r, BGR, dx, dy, speed, phase
    (0.80, 0.08, 0.34, (214, 240, 220), 0.04, 0.03, 0.25, 0.0),   # mint, top right
    (0.10, 0.95, 0.32, (246, 232, 220), 0.04, 0.03, 0.22, 1.5),   # pale blue, bottom left
    (0.98, 0.85, 0.22, (222, 242, 228), 0.03, 0.03, 0.28, 2.7),   # soft mint, bottom right
]
_yy, _xx = np.mgrid[0:H, 0:W]
_DOTS = (((_xx % 34) < 2) & ((_yy % 34) < 2)).astype(np.float32)[..., None]


def bg(t):
    img = backgrounds._blobs(t, _GLOWS, (246, 248, 247))
    return img - _DOTS * np.array([16, 13, 14], np.float32) + backgrounds._grain(t, 1.0)


def flat_rect_at(t):
    sc, dx, dy = R.cam_affine(*R.camera(t))
    return [(dx, dy), (dx + R.WIN_W * sc, dy), (dx + R.WIN_W * sc, dy + R.WIN_H * sc), (dx, dy + R.WIN_H * sc)]


def rect(cx, cy, w, h):
    return [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]


# ---------------------------------------------------------------- the intro
def intro(t, readers, state):
    T[0] = t
    push = ease((t - 6.9) / 0.7)
    out = bg(t)
    if push > 0:
        out = out * (1 - push) + R.MINT * push

    # 1) hook
    if t < 3.45:
        exit_u = ease((t - 2.95) / 0.45)
        op = 1 - exit_u
        y1 = 300 - 50 * exit_u
        line_reveal(out, HOOK1, LEFT, y1 + 150 - HOOK1_B, [0.0, 0.12], opacity=op)
        s = ease((t - 0.85) / 0.42)
        if s > 0:
            layer = out.copy()
            yb = int(y1 + 150 - HOOK1_B + STRIKE_Y)
            x0 = int(LEFT + STRIKE[0])
            cv2.line(layer, (x0, yb), (int(x0 + (STRIKE[1] - STRIKE[0]) * s), yb),
                     tuple(float(c) for c in INK[::-1]), 8, cv2.LINE_AA)
            out = out * (1 - op) + layer * op
        line_reveal(out, HOOK2, LEFT, y1 + 322 - HOOK2_B, [1.35, 1.55], opacity=op)

    # 2) logo reveal, then dock into the header
    header_op = 1.0 if KEEP_HEADER else 1 - ease((t - 6.9) / 0.3)
    if t >= 3.3:
        dock = ease((t - 4.35) / 0.55)
        s = 1 - 0.8 * dock
        wm = v4.scale_rgba(WORDMARK, s)
        cx = W / 2 + (64 + wm.shape[1] / 2 - W / 2) * dock
        cy = 560 + (58 - 560) * dock
        u = ease_out((t - 3.32) / 0.6) if dock == 0 else 1.0
        wipe(out, wm, cx - wm.shape[1] / 2, cy - wm.shape[0] / 2, u, opacity=header_op)
        eu = ease_out((t - 3.6) / 0.5) * (1 - ease((t - 4.2) / 0.3))
        if eu > 0:
            blend_rgba(out, EYE_LOGO, W // 2 - EYE_LOGO.shape[1] // 2, int(418 + 10 * (1 - eu)), eu)
        pu = ease_out((t - 4.75) / 0.45) * header_op
        if pu > 0:
            blend_rgba(out, PILLS, W - 64 - PILLS.shape[1], int(36 + 10 * (1 - pu)), pu)

    # 3) headline left
    text_op = 1 - ease((t - 6.9) / 0.3)
    if t >= 4.8 and text_op > 0:
        eu = ease_out((t - 4.85) / 0.45)
        blend_rgba(out, EYE_MAIN, LEFT, int(332 + 10 * (1 - eu)), eu * text_op)
        line_reveal(out, MAIN1, LEFT, 468 - MAIN1_B, v4.TAG_T[:1], opacity=text_op)
        line_reveal(out, MAIN2, LEFT, 592 - MAIN2_B, v4.TAG_T[1:], opacity=text_op)
        line_reveal(out, BODY1, LEFT, 676 - BODY_B, [6.0 + 0.04 * i for i in range(len(BODY1))], dur=0.5, opacity=text_op)
        line_reveal(out, BODY2, LEFT, 720 - BODY_B, [6.12 + 0.04 * i for i in range(len(BODY2))], dur=0.5, opacity=text_op)

    # 4) live AI Insights card, then push into the real dashboard
    cu = ease_out((t - 4.7) / 0.7)
    ccx, ccy = 1410 + 160 * (1 - cu), 560 + 5 * np.sin(t * 1.1)
    if cu > 0:
        if push > 0:
            content = R.app_content(t, readers, state)
            start = rect(ccx, ccy, CW_, CW_ * R.WIN_H / R.WIN_W)
            flat = flat_rect_at(7.6)
            q = [(a[0] + (b[0] - a[0]) * push, a[1] + (b[1] - a[1]) * push) for a, b in zip(start, flat)]
            win, alpha, _, _ = v4.window_image(content)
            out = v4.draw_quad(out, win, alpha, np.float32(q), min(1.0, push * 2.2), 0.3)
        card_op = cu * (1 - ease((t - 6.9) / 0.35))
        if card_op > 0:
            score = ease((t - 5.45) / 0.9)
            img = card_border(ai_card(score, ease_out((t - 6.15) / 0.3), ease_out((t - 6.35) / 0.3)))
            sc = 1 + 0.25 * push
            out = v4.draw_quad(out, img, CARD_ALPHA, np.float32(rect(ccx, ccy, CW_ * sc, CH_ * sc)), card_op, 0.22)
    elif t >= 4.0:
        R.app_content(t, readers, state)  # keep the reader warm

    prog = min(1.0, (t + 0.35) / 7.25) * text_op
    if prog > 0 and DRAW_PROGRESS:
        cv2.line(out, (0, H - 3), (int(W * prog), H - 3), (98.0, 140.0, 72.0), 4, cv2.LINE_AA)
    return out


def frame_at(t, readers, state):
    if t < 7.6:
        out = intro(t, readers, state)
    elif t < 81.1:
        out = R.app_frame(t, readers, state)
    else:
        out = v4.outro(t, readers, state)
    out = R.overlays(out, t)
    return np.clip(out, 0, 255).astype(np.uint8)


R.frame_at = frame_at

if __name__ == '__main__':
    R.main()
