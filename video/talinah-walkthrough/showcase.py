"""Talinah feature showcase (~39 s): v6 intro + dashboard -> AI ranking -> AI Insights, in the reference's editorial
style. Fake demo data replaces real people (no blur), chapter splits (headline left, product right), anchor-tracked
spotlights with callouts, click ripples, light captions, header with step pills and a closing card.

Usage:
  python3 showcase.py out.mp4 --from T --to T     # video only (chunks), see render_showcase.sh
  python3 showcase.py --stills 8.0 12.0 ...         # contact sheet of single frames
"""
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import fakedata
import intro6 as I
import render as R
import v4
from render import CH, CW, H, W, blend_rgba, ease, ease_out

END_T = 38.6          # showcase length on the VO clock
FREEZE_T = 36.09      # product footage holds its last frame after the Interview Focus beat
HERE = R.HERE

# ---------------------------------------------------------------- fake demo data instead of blur
FAKER = fakedata.Faker()


def _at(self, src_t):
    want = max(0, int(round((src_t - self.s0) * 60)))
    while self.idx < want:
        if not self._read():
            break
    if self.dirty:
        fr = np.frombuffer(self.raw, np.uint8).reshape(CH, CW, 3).copy()
        if self.part == 1 and self.s0 + self.idx / 60 < 2.5:
            fr[818:900, 1430:1890] = R.BAR_PATCH  # hide the recorder's control bar
        self.cur = edge_fade(FAKER.apply(fr))
        self.dirty = False
    return self.cur


def edge_fade(fr, x0=340, solid=14, ramp=20):
    """Fade the bottom edge of the page view to its own background, so lines cut off mid-scroll (half a name)
    are never readable. The sidebar (x < x0) does not scroll and is left alone."""
    n = solid + ramp
    band = fr[CH - 64:CH, x0:].astype(np.float32)
    bgcol = np.median(band, axis=0)
    a = np.concatenate([np.linspace(0, 1, ramp), np.ones(solid)])[:, None, None]
    fr[CH - n:, x0:] = (fr[CH - n:, x0:] * (1 - a) + bgcol[None] * a).astype(np.uint8)
    return fr


R.Reader.at = _at

# dashboard beats re-timed so each element is on screen while the VO names it
R.SEGS[0:3] = [
    (7.10, 11.00, 1, 0.00, 2.45, 0),
    (11.00, 11.70, 1, 2.45, 3.40, 0),
    (11.70, 12.95, 1, 3.40, 3.95, 0),    # "applicants"
    (12.95, 14.55, 1, 3.95, 7.40, 0),    # "pipeline stages"
    (14.55, 17.50, 1, 12.30, 15.80, 7),  # "upcoming interviews"
]
for _i, _s in enumerate(R.SEGS):  # longer hold on the candidate page so STEP 03 can be read before the click
    if _s[0] == 25.20:
        R.SEGS[_i] = (25.20, 27.40, 1, 36.95, 38.80, 6)
    elif _s[0] == 27.00:
        R.SEGS[_i] = (27.40, 29.40, 1, 38.80, 43.00, 0)
R.CAM = [k for k in R.CAM if not 14.0 < k[0] < 17.4] + [(14.4, 1.30, 1110, 480), (15.1, 1.30, 1110, 650),
                                                         (17.3, 1.30, 1110, 650)]
R.CAM.sort(key=lambda k: k[0])

# ---------------------------------------------------------------- layout: split (headline left, product right)
SPLIT_W = 1120
SPLIT_SC = SPLIT_W / R.WIN_W
SPLIT_CX, SPLIT_CY = 1310, 560


def split_aff():
    return SPLIT_SC, SPLIT_CX - R.WIN_W * SPLIT_SC / 2, SPLIT_CY - R.WIN_H * SPLIT_SC / 2


def split_quad(_t=None):
    sc, dx, dy = split_aff()
    return [(dx, dy), (dx + R.WIN_W * sc, dy), (dx + R.WIN_W * sc, dy + R.WIN_H * sc), (dx, dy + R.WIN_H * sc)]


# (collapse start, collapsed, expand start, expanded)
LAYOUT = [(7.0, 7.0, 10.5, 11.3), (17.5, 18.2, 19.0, 19.8), (25.2, 25.85, 26.6, 27.3), (36.1, 36.8, 99, 99)]


def layout_weight(t):
    w = 0.0
    for a, b, c, d in LAYOUT:
        if a <= t <= d:
            up = 1.0 if b <= a else ease((t - a) / (b - a))
            down = 1.0 if d >= 99 else 1 - ease((t - c) / (d - c))
            w = max(w, min(up, down))
    return w


def lerp_aff(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def to_screen(aff, x, y):
    sc, dx, dy = aff
    return dx + x * sc, dy + (y + R.BAR) * sc


# ---------------------------------------------------------------- intro hooks
I.KEEP_HEADER = True
I.DRAW_PROGRESS = False
I.flat_rect_at = split_quad            # the intro's push now lands in the chapter-01 split
I.EYE_MAIN = I.tracked('AI-POWERED HIRING', I.text('SemiBold', 21), I.EYEBROW, 6)
R.MINT = I.bg(7.3)                     # intro push blends into the walkthrough backdrop


def pills(active):
    f = I.text('Medium', 20)
    labels = ['01 Overview', '02 Rank', '03 Decide']
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


PILLS = {k: pills(k) for k in (None, 0, 1, 2)}
I.PILLS = PILLS[0]
LOGO_SMALL = v4.scale_rgba(I.WORDMARK, 0.2)


def header(out, op, active):
    if op <= 0:
        return
    blend_rgba(out, LOGO_SMALL, 64, int(58 - LOGO_SMALL.shape[0] / 2), op)
    p = PILLS[active]
    blend_rgba(out, p, W - 64 - p.shape[1], 36, op)


# ---------------------------------------------------------------- chapter headlines
D, S = 'd', 's'
LEFT = 120
MAXW = SPLIT_CX - SPLIT_W / 2 - LEFT - 50


def _line(words, size):
    segs = [(w, I.disp('Medium', size) if k == D else I.serif(int(size * 1.24)),
             I.INK if k == D else I.SAGE) for w, k in words]
    return I.rich_line(segs)


def _fit(l1, l2):
    for size in range(84, 50, -2):
        a, b = _line(l1, size), _line(l2, size)
        if max(a[1], b[1]) <= MAXW:
            return a, b, size
    return a, b, size


CHAPS = []
for t_in, t_out, eyebrow, l1, l2, body, pill in [
        (7.45, 10.5, 'STEP 01  ·  OVERVIEW', [('Your', D), ('hiring,', D)], [('at', D), ('a', D), ('glance.', S)],
         'Applicants, pipeline and interviews in one view.', 0),
        (17.65, 19.0, 'STEP 02  ·  RANK', [('Every', D), ('candidate,', D)], [('ranked', D), ('by', D), ('AI.', S)],
         'A match score on every application.', 1),
        (25.35, 26.6, 'STEP 03  ·  DECIDE', [('A', D), ('clear', D)], [('recommendation.', S)],
         'Reasons, risks and the questions to ask.', 2),
        (36.3, 99, 'TALINAH', [('Hire', D), ('smarter', D)], [('with', D), ('Talinah.', S)],
         'Book your demo at talinah.com', None)]:
    a, b, size = _fit(l1, l2)
    body_words = I.rich_line([(w, I.text('Regular', 28), I.BODY) for w in body.split()])
    CHAPS.append(dict(t_in=t_in, t_out=t_out, eye=I.tracked(eyebrow, I.text('SemiBold', 20), I.EYEBROW, 6),
                      l1=a, l2=b, size=size, body=body_words, pill=pill))
BTN = v4.scale_rgba(v4.BTN, 0.72)


def chapter_text(out, t):
    I.T[0] = t
    for c in CHAPS:
        if not (c['t_in'] - 0.05 <= t <= c['t_out'] + 0.5):
            continue
        op = 1 - ease((t - c['t_out']) / 0.4)
        lh = c['size'] * 1.2
        top = 560 - (lh * 2 + 120) / 2
        eu = ease_out((t - c['t_in']) / 0.45)
        blend_rgba(out, c['eye'], LEFT, int(top - 34 + 10 * (1 - eu)), eu * op)
        b1 = top + c['size'] * 0.95
        b2 = b1 + lh
        words, _, base = c['l1']
        I.line_reveal(out, words, LEFT, b1 - base, [c['t_in'] + 0.1 + 0.08 * i for i in range(len(words))], opacity=op)
        words, _, base = c['l2']
        I.line_reveal(out, words, LEFT, b2 - base, [c['t_in'] + 0.32 + 0.08 * i for i in range(len(words))],
                      opacity=op)
        words, _, base = c['body']
        I.line_reveal(out, words, LEFT, b2 + 64 - base, [c['t_in'] + 0.6 + 0.03 * i for i in range(len(words))],
                      dur=0.5, opacity=op)
        if c['pill'] is None:  # closing card: CTA button
            bu = ease_out((t - c['t_in'] - 0.9) / 0.45)
            if bu > 0:
                blend_rgba(out, BTN, LEFT - 26, int(b2 + 104 + 14 * (1 - bu)), bu)


# ---------------------------------------------------------------- spotlights + callouts
def _anchor(kf, box, rect):
    g = cv2.cvtColor(cv2.imread(HERE + f'kf/{kf}.png'), cv2.COLOR_BGR2GRAY)
    x0, y0, x1, y1 = box
    p = 4
    return dict(tpl=g[y0 - p:y1 + p, x0 - p:x1 + p].copy(), kx=x0, pad=p, rect=rect)


ANCH = {
    'stats': _anchor('2.60', (399, 482, 537, 505), (-29, -27, 1463, 168)),
    'pipeline': _anchor('2.60', (402, 717, 663, 742), (-32, -27, 698, 720)),
    'upcoming': _anchor('14.00', (402, 652, 813, 678), (-32, -34, 1460, 300)),
    'aicol': _anchor('25.00', (1442, 342, 1621, 362), (-14, -14, 180, 560)),
    'tab': _anchor('38.50', (649, 607, 773, 631), (-35, -11, 207, 35)),
    'decision': _anchor('41.50', (400, 255, 789, 284), (-6, 100, 914, 322)),
    'why': _anchor('41.50', (421, 683, 596, 704), (-15, -22, 425, 440)),
    'careful': _anchor('41.50', (888, 682, 1071, 705), (-18, -22, 422, 440)),
    'focus': _anchor('47.50', (399, 611, 554, 631), (-29, -22, 945, 300)),
}

SPOTS = [  # VO start, VO end, anchor, callout
    (11.55, 13.25, 'stats', '1,397 applicants in the pipeline'),
    (12.95, 14.85, 'pipeline', 'Every hiring stage, live'),
    (14.75, 17.25, 'upcoming', 'Interviews for the next 7 days'),
    (19.55, 23.80, 'aicol', 'AI match score on every applicant'),
    (26.95, 27.90, 'tab', 'One click to AI Insights'),
    (27.85, 29.50, 'decision', 'Recommended: Hold  ·  69% role fit'),
    (29.40, 31.80, 'why', '3 reasons they may work'),
    (31.70, 33.55, 'careful', '3 risks to validate'),
    (33.50, 36.10, 'focus', 'Interview questions, ready to use'),
]
RIPPLES = [(23.70, None, (790, 420)), (27.16, 'tab', (86, 20))]


def find_anchor(content, name, state, t):
    a = ANCH[name]
    key = 'anc_' + name
    if state.get(key + '_t') == t:
        return state.get(key)
    g = cv2.cvtColor(content, cv2.COLOR_BGR2GRAY)
    th, tw = a['tpl'].shape
    x0, x1 = max(0, a['kx'] - 90), min(CW, a['kx'] + tw + 90)
    r = cv2.matchTemplate(g[:, x0:x1], a['tpl'], cv2.TM_CCOEFF_NORMED)
    _, mx, _, ml = cv2.minMaxLoc(r)
    if mx >= 0.72:
        state[key] = (ml[0] + x0 + a['pad'], ml[1] + a['pad'])
    state[key + '_t'] = t
    return state.get(key)


def _chip(text):
    f = I.text('SemiBold', 25)
    tw = int(f.getlength(text))
    w, h, pad = tw + 74, 56, 22
    im = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('L', im.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 6, pad + w, pad + h + 6), 16, fill=70)
    im.paste((16, 40, 26, 255), mask=sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((pad, pad, pad + w, pad + h), 16, fill=(255, 255, 255, 250), outline=(214, 230, 220, 255),
                        width=2)
    d.ellipse((pad + 22, pad + h / 2 - 7, pad + 36, pad + h / 2 + 7), fill=(60, 170, 90, 255))
    d.text((pad + 50, pad + h / 2), text, font=f, fill=I.INK + (255,), anchor='lm')
    return np.array(im), pad


CHIPS = {s[3]: _chip(s[3]) for s in SPOTS}


def _ring(w, h):
    w, h = int(w), int(h)
    m = 24
    k = 2
    im = Image.new('RGBA', ((w + 2 * m) * k, (h + 2 * m) * k), (0, 0, 0, 0))
    glow = Image.new('L', im.size, 0)
    ImageDraw.Draw(glow).rounded_rectangle((m * k, m * k, (m + w) * k, (m + h) * k), 16 * k, outline=255, width=8 * k)
    im.paste((90, 200, 120, 110), mask=glow.filter(ImageFilter.GaussianBlur(8 * k)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((m * k, m * k, (m + w) * k, (m + h) * k), 16 * k, outline=(52, 168, 86, 255), width=3 * k)
    return np.array(im.resize((w + 2 * m, h + 2 * m), Image.LANCZOS)), m


def spotlights(out, t, content, aff, state, active):
    shots = []
    for t0, t1, name, label in SPOTS:
        if not (t0 <= t <= t1):
            continue
        k = min(ease((t - t0) / 0.35), 1 - ease((t - (t1 - 0.3)) / 0.3)) * active
        if k <= 0.01:
            continue
        anc = find_anchor(content, name, state, t)
        if anc is None:
            continue
        rx0, ry0, rx1, ry1 = ANCH[name]['rect']
        cx0, cy0 = max(0, anc[0] + rx0), max(0, anc[1] + ry0)
        cx1, cy1 = min(CW, anc[0] + rx1), min(CH, anc[1] + ry1)
        if cx1 - cx0 < 10 or cy1 - cy0 < 10:
            continue
        X0, Y0 = to_screen(aff, cx0, cy0)
        X1, Y1 = to_screen(aff, cx1, cy1)
        X0, Y0, X1, Y1 = max(-40, X0), max(-40, Y0), min(W + 40, X1), min(H + 40, Y1)
        shots.append((k, (X0, Y0, X1, Y1), label, t0))
    if not shots:
        return out
    # dim everything outside the union of active spots
    q = 4
    inside = np.zeros((H // q, W // q), np.float32)
    kmax = max(s[0] for s in shots)
    for k, (X0, Y0, X1, Y1), _, _ in shots:
        m = np.zeros_like(inside)
        cv2.rectangle(m, (int(X0 / q), int(Y0 / q)), (int(X1 / q), int(Y1 / q)), 1.0, -1)
        inside = np.maximum(inside, m * k / kmax)
    inside = cv2.GaussianBlur(inside, (0, 0), 2.5)
    inside = cv2.resize(inside, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    out = out * (1 - 0.40 * kmax * (1 - inside)) + np.array([236, 240, 238], np.float32) * 0.0
    for k, (X0, Y0, X1, Y1), label, t0 in shots:
        ring, m = _ring(X1 - X0, Y1 - Y0)
        blend_rgba(out, ring, int(X0 - m), int(Y0 - m), k)
        chip, pad = CHIPS[label]
        cu = ease_out((t - t0 - 0.15) / 0.4)
        if cu <= 0:
            continue
        cw, chh = chip.shape[1] - 2 * pad, chip.shape[0] - 2 * pad
        x = min(max(40, X0), W - 40 - cw)
        y = Y0 - chh - 18
        if y < 110:
            y = Y1 + 18 if Y1 + 18 + chh < 930 else Y0 + 18
        blend_rgba(out, chip, int(x - pad), int(y - pad + 12 * (1 - cu)), min(k, cu))
    return out


def ripples(out, t, content, aff, state):
    for tr, anc_name, (ox, oy) in RIPPLES:
        u = (t - tr) / 0.6
        if not (0 <= u <= 1):
            continue
        if anc_name:
            anc = find_anchor(content, anc_name, state, t)
            if anc is None:
                continue
            x, y = anc[0] + ox, anc[1] + oy
        else:
            x, y = ox, oy
        X, Y = to_screen(aff, x, y)
        layer = out.copy()
        r = 12 + 44 * ease_out(u)
        cv2.circle(layer, (int(X), int(Y)), int(r), (86.0, 170.0, 52.0), 3, cv2.LINE_AA)
        cv2.circle(layer, (int(X), int(Y)), int(10 * (1 - u) + 4), (86.0, 170.0, 52.0), -1, cv2.LINE_AA)
        a = (1 - u) * 0.85
        out = out * (1 - a) + layer * a
    return out


# ---------------------------------------------------------------- light captions + progress
def caption_img(text):
    f = I.text('Medium', 30)
    tw = f.getlength(text)
    bw, bh, pad = int(tw + 56), 62, 24
    im = Image.new('RGBA', (bw + 2 * pad, bh + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('L', im.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 6, pad + bw, pad + bh + 6), 18, fill=60)
    im.paste((16, 40, 26, 255), mask=sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((pad, pad, pad + bw, pad + bh), 18, fill=(255, 255, 255, 242), outline=(222, 230, 225, 255),
                        width=2)
    d.text((pad + bw / 2, pad + bh / 2 + 1), text, font=f, fill=I.INK + (255,), anchor='mm')
    return np.array(im)


CAPS = [c for c in R.CAPS if c[0] < FREEZE_T]
CAP_IMG = {c[2]: caption_img(c[2]) for c in CAPS}


def overlays(out, t):
    for a, b, text in CAPS:
        if a <= t <= b:
            img = CAP_IMG[text]
            u_in = ease_out((t - a) / 0.22)
            op = u_in * (1 - ease((t - (b - 0.18)) / 0.18))
            blend_rgba(out, img, (W - img.shape[1]) // 2, int(1010 - img.shape[0] / 2 + 10 * (1 - u_in)), op)
    prog = min(1.0, (t + 0.35) / (END_T + 0.35))
    cv2.line(out, (0, H - 3), (int(W * prog), H - 3), (98.0, 140.0, 72.0), 4, cv2.LINE_AA)
    return out


# ---------------------------------------------------------------- frames
def walk(t, readers, state):
    out = I.bg(t)
    tc = min(t, FREEZE_T)
    content = R.app_content(tc, readers, state)
    L = layout_weight(t)
    aff = lerp_aff(R.cam_affine(*R.camera(tc)), split_aff(), L)
    out = v4.comp_window(out, content, *aff)
    out = spotlights(out, t, content, aff, state, 1 - L)
    out = ripples(out, t, content, aff, state)
    active = 0 if t < 17.5 else 1 if t < 25.2 else 2 if t < 36.1 else None
    header(out, L, active)  # header only lives in the split layouts; it would cover the zoomed UI
    chapter_text(out, t)
    return out


def frame_at(t, readers, state):
    if t < 7.6:
        out = I.intro(t, readers, state)
    else:
        out = walk(t, readers, state)
    out = overlays(out, t)
    return np.clip(out, 0, 255).astype(np.uint8)


R.frame_at = frame_at
R.END = END_T


def stills(times, path):
    readers, state = {}, {}
    tiles = []
    for t in sorted(times):
        f = frame_at(t, readers, state)
        tile = cv2.resize(f, (960, 540), interpolation=cv2.INTER_AREA)
        cv2.putText(tile, f'{t:.1f}', (10, 34), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 220), 2)
        tiles.append(tile)
        cv2.imwrite(HERE + f'sc_full_{t:.2f}.png', f)
    while len(tiles) % 2:
        tiles.append(np.zeros_like(tiles[0]))
    cv2.imwrite(path, np.vstack([np.hstack(tiles[i:i + 2]) for i in range(0, len(tiles), 2)]),
                [cv2.IMWRITE_JPEG_QUALITY, 88])


if __name__ == '__main__':
    if '--stills' in sys.argv:
        i = sys.argv.index('--stills')
        out_path = sys.argv[i + 1]
        stills([float(x) for x in sys.argv[i + 2:]], out_path)
    else:
        R.main()
