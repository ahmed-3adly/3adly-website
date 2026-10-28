"""Talinah sales walkthrough v3: re-edit of the raw capture to the new voice-over.

Usage: python3 render.py [out.mp4] [--preview N] [--from T] [--to T]
  --preview N  render every Nth frame at half size into a contact-sheet folder instead of a video
"""
import math
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pii  # noqa: E402

HERE = pii.HERE
# inputs/ is git-ignored: put the raw screen recordings and the voice-over there (see HANDOFF.md)
SRC = {1: HERE + 'inputs/raw_part1.webm', 2: HERE + 'inputs/raw_part2.webm'}
VO = HERE + 'inputs/voiceover.mp3'

FPS = 30
W, H = 1920, 1080
OFF = 0.35            # voice-over starts this late in the video
END = 91.9            # video length (VO clock)
CW, CH = 1890, 900    # raw capture minus the 10px strip at the top
BAR = 46              # browser chrome height in raw-capture pixels
WIN_W, WIN_H = CW, CH + BAR
S0 = 1580 / CW        # window scale in the wide shot
WX, WY = (W - WIN_W * S0) / 2, 112

GREEN = (60, 181, 90)


def font(w, s):
    return ImageFont.truetype(HERE + f'fonts/package/files/poppins-latin-{w}-normal.woff2', s)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


# ---------------------------------------------------------------- timeline (VO clock)
# (t0, t1, part, src0, src1, crossfade_frames)
SEGS = [
    (7.10, 11.00, 1, 0.00, 2.45, 0),     # dashboard top
    (11.00, 14.40, 1, 2.45, 12.00, 0),   # scroll: stats, pipeline
    (14.40, 17.50, 1, 12.00, 16.50, 0),  # upcoming interviews
    (17.50, 18.30, 1, 23.30, 23.30, 9),  # candidates list (hold)
    (18.30, 23.90, 1, 23.30, 26.60, 0),  # hover, open the candidate
    (23.90, 25.20, 1, 27.90, 29.20, 6),  # candidate details
    (25.20, 27.00, 1, 37.00, 38.80, 6),  # click AI Insights
    (27.00, 29.40, 1, 38.80, 43.00, 0),  # recruiter snapshot
    (29.40, 31.60, 1, 43.00, 46.00, 0),  # why it may work
    (31.60, 33.40, 1, 46.00, 47.50, 0),  # why to be careful
    (33.40, 36.10, 1, 47.50, 50.20, 0),  # interview focus
    (36.10, 38.90, 1, 62.00, 67.00, 9),  # interviews tab -> schedule
    (38.90, 40.10, 1, 67.00, 69.60, 0),  # date
    (40.10, 41.10, 1, 72.00, 74.40, 5),  # duration
    (41.10, 42.20, 1, 76.00, 79.00, 5),  # interview type
    (42.20, 43.40, 1, 79.60, 82.60, 5),  # location
    (43.40, 46.10, 1, 83.50, 89.00, 0),  # schedule -> success
    (46.10, 47.60, 1, 94.50, 97.30, 9),  # mark completed
    (47.60, 50.30, 1, 97.30, 101.00, 0),  # confirm -> scorecard
    (50.30, 51.90, 1, 101.00, 103.50, 0),  # overall recommendation
    (51.90, 53.40, 1, 104.50, 110.00, 5),  # skill ratings
    (53.40, 54.20, 1, 113.50, 117.00, 5),  # strengths
    (54.20, 54.70, 1, 129.50, 131.00, 4),
    (54.70, 55.50, 1, 134.00, 137.50, 4),  # areas to improve
    (55.50, 56.40, 1, 147.00, 150.50, 4),
    (56.40, 57.60, 1, 153.50, 156.60, 4),  # submit
    (57.60, 61.00, 1, 156.60, 162.85, 0),  # feedback on record
    (61.00, 65.80, 2, 2.60, 9.00, 9),    # status -> next step, auto-assign
    (65.80, 67.40, 2, 10.00, 13.60, 5),  # 2nd interview scheduled + notification
    (67.40, 69.00, 2, 16.40, 20.00, 5),  # assign interviewer
    (69.00, 70.00, 2, 21.20, 23.60, 5),  # schedule next round
    (70.00, 71.00, 2, 31.40, 33.80, 5),
    (71.00, 72.00, 2, 37.80, 40.80, 5),
    (72.00, 73.40, 2, 56.50, 59.50, 9),  # notes tab
    (73.40, 74.60, 2, 61.50, 65.50, 5),  # typing
    (74.60, 75.40, 2, 81.50, 84.00, 4),
    (75.40, 77.00, 2, 84.00, 87.50, 0),  # saved automatically
    (77.00, 78.80, 2, 96.50, 100.60, 9),  # status -> Offer Sent
    (78.80, 80.40, 2, 100.60, 102.40, 0),  # upload offer dialog
    (80.40, 81.60, 2, 136.70, 138.60, 6),  # file chosen, upload
    (81.60, 86.00, 2, 138.60, 143.70, 0),  # offer sent
]
APP_IN = (7.05, 7.65)    # intro -> app dissolve
APP_OUT = (85.45, 86.0)  # app -> outro dissolve

# camera keyframes: (t, zoom, focus_x, focus_y) in capture coords; zoom 1 = wide window
CAM = [
    (7.0, 1.00, 945, 450), (9.6, 1.00, 945, 450), (11.4, 1.32, 1110, 520), (14.2, 1.30, 1110, 480),
    (17.3, 1.30, 1110, 480),
    (17.55, 1.06, 1110, 450), (19.4, 1.22, 1100, 470), (21.4, 1.40, 1110, 500), (23.6, 1.40, 1110, 500),
    (24.2, 1.18, 960, 420), (25.4, 1.25, 900, 600), (26.9, 1.35, 860, 560), (29.0, 1.42, 880, 520),
    (31.0, 1.48, 760, 560), (32.4, 1.55, 1080, 560), (33.6, 1.50, 1080, 560), (35.0, 1.45, 860, 520),
    (36.1, 1.45, 860, 520),
    (36.4, 1.12, 900, 450), (38.4, 1.12, 900, 450), (39.2, 1.42, 860, 420), (43.2, 1.42, 860, 470),
    (44.4, 1.15, 900, 450), (46.0, 1.15, 900, 450),
    (46.3, 1.25, 820, 560), (47.6, 1.25, 820, 560), (49.0, 1.62, 1650, 470), (56.4, 1.62, 1650, 470),
    (57.4, 1.62, 1650, 470), (58.4, 1.30, 880, 520), (60.9, 1.30, 880, 520),
    (61.1, 1.30, 1150, 330), (64.6, 1.38, 1250, 340), (65.8, 1.30, 1100, 420), (67.3, 1.30, 1000, 470),
    (68.8, 1.32, 900, 520), (69.2, 1.32, 960, 450), (71.8, 1.25, 960, 450),
    (72.1, 1.25, 960, 520), (73.3, 1.45, 900, 600), (77.0, 1.45, 900, 600),
    (77.2, 1.30, 1200, 360), (78.9, 1.42, 960, 460), (81.5, 1.42, 960, 460), (83.2, 1.15, 1000, 420),
    (86.0, 1.0, 945, 450),
]

CAPS = [
    (0.0, 4.35, 'Meet Talinah.'),
    (4.75, 7.2, 'Hiring, powered by AI.'),
    (7.5, 11.3, 'Your dashboard shows the whole hiring picture at a glance:'),
    (11.55, 16.25, 'applicants, pipeline stages, and upcoming interviews.'),
    (17.55, 20.45, 'Every candidate gets an AI match score,'),
    (20.6, 23.9, 'so you know exactly where to focus first.'),
    (25.25, 28.75, 'Open AI Insights for a clear recommendation.'),
    (29.2, 31.7, 'Talinah shows why a candidate may work,'),
    (31.85, 33.3, 'what to be careful about,'),
    (33.45, 36.1, 'and which questions to ask in the interview.'),
    (36.65, 39.15, 'Schedule interviews in a few clicks.'),
    (39.25, 43.5, 'Pick the date, duration, interview type, and location,'),
    (43.6, 45.95, 'and Talinah handles the rest.'),
    (46.7, 50.35, 'After each interview, fill in a structured scorecard:'),
    (50.5, 53.55, 'an overall recommendation, skill ratings,'),
    (53.65, 56.4, 'strengths, and areas to improve.'),
    (56.75, 60.85, 'Every hiring decision is backed by consistent evidence.'),
    (60.98, 65.6, 'Move a candidate forward, and Talinah takes care of the next step:'),
    (65.85, 68.95, 'updating the status, assigning the recruiter,'),
    (69.05, 71.25, 'and lining up the next round.'),
    (71.65, 76.4, 'Keep the whole team aligned with shared notes that save automatically.'),
    (76.85, 80.85, "When you're ready, send the offer straight from the candidate's profile."),
    (80.95, 85.4, 'From first look to final offer, it all happens in Talinah.'),
    (85.6, 87.45, 'Hire smarter with Talinah.'),
    (87.5, END, 'Book your demo at talinah.com.'),
]

CHAPTERS = [
    (7.7, 11.3, '01', 'Your hiring at a glance', 'Pipeline, applicants and interviews in one dashboard'),
    (17.7, 21.3, '02', 'Every candidate, ranked', 'AI recommendations right in the list'),
    (25.4, 29.0, '03', 'AI insights', 'Clear recommendation, evidence and risks, per candidate'),
    (36.3, 39.9, '04', 'Schedule in seconds', 'Book interviews with the right people and format'),
    (46.3, 49.9, '05', 'Structured feedback', 'Consistent scorecards after every interview'),
    (61.2, 64.8, '06', 'Pipeline on autopilot', 'Status updates auto-assign the next step'),
    (72.2, 75.8, '07', 'Shared notes', 'Context that saves automatically'),
    (77.2, 80.8, '08', 'From interview to offer', 'Send the offer without leaving Talinah'),
]


# ---------------------------------------------------------------- static layers
def noise(h, w, amp=1.5, seed=3):
    return np.random.default_rng(seed).normal(0, amp, (h, w, 1)).astype(np.float32)


def mint_bg():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = (x / W * 0.55 + y / H * 0.45)
    a = np.array([228, 245, 231], np.float32)
    b = np.array([188, 230, 200], np.float32)
    img = a + (b - a) * d[..., None] ** 1.6
    r = np.sqrt(((x - 560) / 1300) ** 2 + ((y - 260) / 900) ** 2)
    img += (1 - np.clip(r, 0, 1))[..., None] * np.array([10, 6, 9], np.float32)
    return np.clip(img + noise(H, W), 0, 255)[..., ::-1].copy()  # BGR float


def dark_bg():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - 960) / 1150) ** 2 + ((y - 560) / 760) ** 2)
    t = np.clip(r, 0, 1)
    t = t * t * (3 - 2 * t)
    c0 = np.array([40, 118, 58], np.float32)
    c1 = np.array([8, 29, 15], np.float32)
    img = c0 + (c1 - c0) * t[..., None]
    return np.clip(img + noise(H, W, 1.2, 5), 0, 255)[..., ::-1].copy()


def window_layers():
    """Browser window at capture scale: chrome RGB, alpha mask, and a soft shadow (padded)."""
    ss = 2
    img = Image.new('RGBA', (WIN_W * ss, WIN_H * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rad = int(20 / S0) * ss
    d.rounded_rectangle((0, 0, WIN_W * ss - 1, WIN_H * ss - 1), rad, fill=(252, 253, 251, 255))
    d.rectangle((0, BAR * ss - 2, WIN_W * ss, BAR * ss), fill=(226, 233, 227, 255))
    cy = BAR * ss // 2
    for i, col in enumerate([(249, 92, 84), (255, 190, 39), (36, 199, 60)]):
        cx = int((24 + i * 22) / S0) * ss
        rr = int(6.5 / S0) * ss
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col + (255,))
    pw, ph = 560 * ss, 30 * ss
    px = WIN_W * ss // 2 - pw // 2
    d.rounded_rectangle((px, cy - ph // 2, px + pw, cy + ph // 2), ph // 2, fill=(237, 243, 238, 255))
    f = font(400, 19 * ss)
    txt = 'app.talinah.com'
    tw = d.textlength(txt, font=f)
    tx = WIN_W * ss // 2 - tw / 2 + 10 * ss
    d.text((tx, cy), txt, font=f, fill=(70, 82, 74, 255), anchor='lm')
    lx, ly = tx - 22 * ss, cy
    d.rounded_rectangle((lx - 6 * ss, ly - 2 * ss, lx + 6 * ss, ly + 7 * ss), 2 * ss, fill=(90, 100, 94, 255))
    d.arc((lx - 4 * ss, ly - 9 * ss, lx + 4 * ss, ly + 2 * ss), 180, 360, fill=(90, 100, 94, 255), width=2 * ss)
    img = img.resize((WIN_W, WIN_H), Image.LANCZOS)
    arr = np.array(img)
    rgb = arr[..., :3][..., ::-1].astype(np.uint8).copy()
    alpha = arr[..., 3].astype(np.float32) / 255
    pad = 120
    sh = Image.new('L', (WIN_W + 2 * pad, WIN_H + 2 * pad), 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 26, pad + WIN_W, pad + WIN_H + 26), rad // ss, fill=255)
    sh = sh.filter(ImageFilter.GaussianBlur(42))
    shadow = np.array(sh).astype(np.float32) / 255 * 0.30
    return rgb, alpha, shadow, pad


def text_rgba(lines, pad=(0, 0)):
    """lines: list of (text, font, rgba, dy). Returns tight RGBA image."""
    d0 = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    wmax = max(d0.textlength(t, font=f) for t, f, _, _ in lines)
    hgt = max(dy + f.size * 1.4 for t, f, _, dy in lines)
    img = Image.new('RGBA', (int(wmax + 2 * pad[0] + 4), int(hgt + 2 * pad[1])), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for t, f, col, dy in lines:
        tw = d.textlength(t, font=f)
        d.text(((img.width - tw) / 2, pad[1] + dy), t, font=f, fill=col)
    return img


def caption_img(text):
    f = font(500, 37)
    d0 = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    tw = d0.textlength(text, font=f)
    bw, bh = int(tw + 64), 80
    pad = 30
    img = Image.new('RGBA', (bw + 2 * pad, bh + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('L', img.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 8, pad + bw, pad + bh + 8), 16, fill=90)
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    base = Image.new('RGBA', img.size, (0, 0, 0, 0))
    base.paste((0, 0, 0, 255), mask=sh)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((pad, pad, pad + bw, pad + bh), 16, fill=(21, 38, 27, 238))
    d.text((pad + bw / 2, pad + bh / 2 + 1), text, font=f, fill=(255, 255, 255, 255), anchor='mm')
    return np.array(base)


def pill_img(num, title, sub):
    ft, fs, fn = font(600, 36), font(400, 24), font(600, 28)
    d0 = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    tw = max(d0.textlength(title, font=ft), d0.textlength(sub, font=fs))
    hgt = 100
    wid = int(hgt + 22 + tw + 38)
    pad = 26
    img = Image.new('RGBA', (wid + 2 * pad, hgt + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('L', img.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 8, pad + wid, pad + hgt + 8), hgt // 2, fill=80)
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    img.paste((0, 0, 0, 255), mask=sh)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((pad, pad, pad + wid, pad + hgt), hgt // 2, fill=(26, 44, 32, 245))
    c = pad + hgt // 2
    d.ellipse((pad + 18, pad + 18, pad + hgt - 18, pad + hgt - 18), fill=GREEN + (255,))
    d.text((pad + hgt // 2, c + 1), num, font=fn, fill=(255, 255, 255, 255), anchor='mm')
    x = pad + hgt + 4
    d.text((x, pad + 14), title, font=ft, fill=(255, 255, 255, 255))
    d.text((x, pad + 60), sub, font=fs, fill=(176, 205, 184, 255))
    return np.array(img), pad, hgt


def blend_rgba(dst, rgba, x, y, opacity=1.0, clip_w=None):
    """Alpha-composite an RGB(A) numpy image (RGB order) onto BGR float dst at integer x,y."""
    h, w = rgba.shape[:2]
    if clip_w is not None:
        w = max(0, min(w, int(clip_w)))
        rgba = rgba[:, :w]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0 or opacity <= 0:
        return
    src = rgba[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    a = src[..., 3:4] / 255 * opacity
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + src[..., 2::-1] * a


def warp_rgba(rgba, scale, dx, dy):
    M = np.float32([[scale, 0, dx], [0, scale, dy]])
    return cv2.warpAffine(rgba, M, (W, H), flags=cv2.INTER_CUBIC if scale > 1 else cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=0)


# ---------------------------------------------------------------- source decoding
class Reader:
    """Sequential 60fps reader for one segment's source range, with blur applied."""

    def __init__(self, part, s0, s1):
        self.part, self.s0 = part, s0
        dur = max(0.2, s1 - s0 + 0.2)
        self.p = subprocess.Popen(
            ['ffmpeg', '-v', 'error', '-ss', f'{s0:.3f}', '-i', SRC[part], '-t', f'{dur:.3f}',
             '-vf', f'fps=60,crop={CW}:{CH}:0:10', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
            stdout=subprocess.PIPE)
        self.idx = -1
        self.cur = None
        self.hold = []  # (rect, ttl)
        self.raw = None
        self.dirty = False

    def _read(self):
        b = self.p.stdout.read(CW * CH * 3)
        if len(b) < CW * CH * 3:
            return False
        self.idx += 1
        self.raw = b
        self.dirty = True
        return True

    def at(self, src_t):
        want = max(0, int(round((src_t - self.s0) * 60)))
        while self.idx < want:
            if not self._read():
                break
        if self.dirty:
            # only frames that make it into the edit get scanned and blurred
            fr = np.frombuffer(self.raw, np.uint8).reshape(CH, CW, 3).copy()
            src_t = self.s0 + self.idx / 60
            if self.part == 1 and src_t < 2.5:
                fr[818:900, 1430:1890] = BAR_PATCH  # hide the recorder's control bar
            rects = pii.detect(fr, self.part, src_t)
            self.hold = [(r, ttl - 1) for r, ttl in self.hold if ttl > 1] + [(r, 3) for r in rects]
            self.cur = pii.blur(fr, [r for r, _ in self.hold])
            self.dirty = False
        return self.cur

    def close(self):
        self.p.kill()


def _bar_patch():
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '19.3', '-i', SRC[1], '-frames:v', '1',
                        '-vf', f'crop={CW}:{CH}:0:10', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
                       stdout=subprocess.PIPE, check=True)
    fr = np.frombuffer(p.stdout, np.uint8).reshape(CH, CW, 3)
    return fr[818:900, 1430:1890].copy()


BAR_PATCH = _bar_patch()


# ---------------------------------------------------------------- scene renderers
def camera(t):
    if t <= CAM[0][0]:
        k = CAM[0]
        return k[1], k[2], k[3]
    for a, b in zip(CAM, CAM[1:]):
        if a[0] <= t <= b[0]:
            u = ease((t - a[0]) / max(1e-6, b[0] - a[0]))
            return tuple(a[i] + (b[i] - a[i]) * u for i in (1, 2, 3))
    k = CAM[-1]
    return k[1], k[2], k[3]


def cam_affine(z, fx, fy):
    """Window-pixel -> frame affine (scale, dx, dy); the view stays inside the window where it can."""
    px, py = WX + fx * S0, WY + (fy + BAR) * S0
    hw, hh = W / 2 / z, H / 2 / z
    wl, wr, wt, wb = WX, WX + WIN_W * S0, WY, WY + WIN_H * S0
    lo_x, hi_x = wl + hw - 30 / z, wr - hw + 30 / z
    lo_y, hi_y = wt + hh - 20 / z, wb - hh + 120 / z
    cx = min(max(px, lo_x), hi_x) if lo_x <= hi_x else (lo_x + hi_x) / 2
    cy = min(max(py, lo_y), hi_y) if lo_y <= hi_y else (lo_y + hi_y) / 2
    return S0 * z, (WX - cx) * z + W / 2, (WY - cy) * z + H / 2


def app_content(t, readers, state):
    seg_i = 0
    for i, s in enumerate(SEGS):
        if t >= s[0]:
            seg_i = i
    t0, t1, part, s0, s1, xf = SEGS[seg_i]
    tt = min(max(t, t0), t1)
    src_t = s0 + (tt - t0) * (s1 - s0) / max(1e-6, t1 - t0)
    if seg_i not in readers:
        for k in list(readers):
            if k < seg_i - 1:
                readers.pop(k).close()
        readers[seg_i] = Reader(part, s0, s1)
    if state.get('seg') != seg_i:
        state['last_prev'] = state.get('last')
        state['seg'] = seg_i
    content = readers[seg_i].at(src_t)
    state['last'] = content
    nf = (t - t0) * FPS
    if xf and nf < xf and state.get('last_prev') is not None:
        u = ease(nf / xf)
        content = cv2.addWeighted(state['last_prev'], 1 - u, content, u, 0)
    return content


def app_frame(t, readers, state):
    content = app_content(t, readers, state)
    rgb, alpha, shadow, pad = LAYERS
    win = rgb.copy()
    win[BAR:] = content
    z, fx, fy = camera(t)
    sc, dx, dy = cam_affine(z, fx, fy)
    out = MINT.copy()
    sh = warp_rgba(shadow, sc, dx - pad * sc, dy - pad * sc)
    out *= (1 - sh[..., None])
    a = warp_rgba(alpha, sc, dx, dy)[..., None]
    w = warp_rgba(win, sc, dx, dy).astype(np.float32)
    out = out * (1 - a) + w * a
    return out


def title_scene(t, outro):
    out = DARK.copy()
    if not outro:
        # 'Talinah' in Poppins SemiBold, no dot
        for img, y, start in ((INTRO_TITLE, 412, 0.15), (INTRO_SUB, 606, 0.75)):
            u = ease_out((t - start) / 0.9)
            blend_rgba(out, img, (W - img.shape[1]) // 2, int(y + 26 * (1 - u)), u)
    else:
        lt = t - APP_OUT[0]
        items = ((OUT_TITLE, 380, 0.25), (OUT_SUB, 508, 0.6), (OUT_BTN, 606, 0.9), (OUT_URL, 728, 1.15))
        for img, y, start in items:
            u = ease_out((lt - start) / 0.85)
            blend_rgba(out, img, (W - img.shape[1]) // 2, int(y + 24 * (1 - u)), u)
    return out


def overlays(out, t):
    for a, b, num, title, sub in CHAPTERS:
        if a - 0.1 <= t <= b + 0.6:
            img, pad, hgt = PILLS[num]
            open_u = ease_out((t - a) / 0.55)
            close_u = ease((t - b) / 0.5)
            reveal = pad + hgt + (img.shape[1] - pad - hgt) * open_u * (1 - close_u)
            op = min(1.0, (t - a + 0.1) / 0.25) * (1 - ease((t - b - 0.25) / 0.35))
            blend_rgba(out, img, 48 - pad, 40 - pad, op, clip_w=reveal)
    for a, b, text in CAPS:
        if a <= t <= b:
            img = CAPTIONS[text]
            u_in = ease_out((t - a) / 0.22)
            u_out = ease((t - (b - 0.18)) / 0.18)
            op = u_in * (1 - u_out)
            y = 990 - img.shape[0] // 2 + int(10 * (1 - u_in))
            blend_rgba(out, img, (W - img.shape[1]) // 2, y, op)
    return out


def frame_at(t, readers, state):
    if t < APP_IN[0]:
        out = title_scene(t, False)
    elif t < APP_IN[1]:
        u = ease((t - APP_IN[0]) / (APP_IN[1] - APP_IN[0]))
        out = title_scene(t, False) * (1 - u) + app_frame(t, readers, state) * u
    elif t < APP_OUT[0]:
        out = app_frame(t, readers, state)
    elif t < APP_OUT[1]:
        u = ease((t - APP_OUT[0]) / (APP_OUT[1] - APP_OUT[0]))
        out = app_frame(t, readers, state) * (1 - u) + title_scene(t, True) * u
    else:
        out = title_scene(t, True)
    out = overlays(out, t)
    return np.clip(out, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- assets
MINT = mint_bg()
DARK = dark_bg()
LAYERS = window_layers()
INTRO_TITLE = np.array(text_rgba([('Talinah', font(600, 156), (255, 255, 255, 255), 0)]))
INTRO_SUB = np.array(text_rgba([('AI-powered hiring, from first look to final offer', font(400, 40),
                                 (170, 218, 182, 255), 0)]))
OUT_TITLE = np.array(text_rgba([('Hire smarter with Talinah', font(600, 86), (255, 255, 255, 255), 0)]))
OUT_SUB = np.array(text_rgba([('Find, assess and hire the right people faster', font(400, 36),
                               (170, 218, 182, 255), 0)]))


def _button():
    f = font(500, 34)
    img = Image.new('RGBA', (400, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    sh = Image.new('L', img.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((30, 28, 370, 108), 40, fill=110)
    img.paste((0, 30, 10, 255), mask=sh.filter(ImageFilter.GaussianBlur(10)))
    d.rounded_rectangle((30, 18, 370, 98), 40, fill=GREEN + (255,))
    d.text((200, 59), 'Book a demo', font=f, fill=(255, 255, 255, 255), anchor='mm')
    return np.array(img)


OUT_BTN = _button()
OUT_URL = np.array(text_rgba([('talinah.com', font(500, 34), (218, 238, 223, 255), 0)]))
CAPTIONS = {c[2]: caption_img(c[2]) for c in CAPS}
PILLS = {c[2]: pill_img(c[2], c[3], c[4]) for c in CHAPTERS}


def main():
    args = sys.argv[1:]
    out_path = args[0] if args and not args[0].startswith('--') else HERE + 'talinah_walkthrough_sales_v3.mp4'
    preview = int(args[args.index('--preview') + 1]) if '--preview' in args else 0
    t_from = float(args[args.index('--from') + 1]) if '--from' in args else -OFF
    t_to = float(args[args.index('--to') + 1]) if '--to' in args else END
    n0 = int(round((t_from + OFF) * FPS))
    n1 = int(round((t_to + OFF) * FPS))
    readers, state = {}, {}
    enc = None
    if '--noaudio' in args:
        enc = subprocess.Popen(
            ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS),
             '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', out_path],
            stdin=subprocess.PIPE)
    elif not preview:
        enc = subprocess.Popen(
            ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS),
             '-i', '-', '-ss', f'{max(0, t_from):.3f}', '-i', VO,
             '-filter_complex', f'[1:a]adelay={int(OFF * 1000) if t_from <= 0 else 0}:all=1,apad,'
                                f'afade=t=out:st={t_to + OFF - 0.6 - max(0, t_from + OFF):.2f}:d=0.6[a]',
             '-map', '0:v', '-map', '[a]', '-shortest',
             '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
             '-c:a', 'aac', '-b:a', '192k', out_path], stdin=subprocess.PIPE)
    for n in range(n0, n1):
        t = n / FPS - OFF
        if preview and (n - n0) % preview:
            # keep readers in sync cheaply by still advancing app time
            if APP_IN[0] <= t < APP_OUT[1]:
                app_content(t, readers, state)
            continue
        fr = frame_at(t, readers, state)
        if preview:
            cv2.imwrite(f'{out_path}/f_{n:05d}.jpg', cv2.resize(fr, (W // 2, H // 2)), [cv2.IMWRITE_JPEG_QUALITY, 85])
        else:
            enc.stdin.write(fr.tobytes())
        if n % 150 == 0:
            print(f'{t:6.2f}s', flush=True)
    if enc:
        enc.stdin.close()
        enc.wait()
    for r in readers.values():
        r.close()


if __name__ == '__main__':
    main()
