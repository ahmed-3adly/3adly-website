"""Original background score for the Talinah showcase, synthesised from scratch (royalty-free).

Timeline is the OUTPUT clock (VO time + 0.35 s). 96 BPM, D major: I - vi - IV - V (Dmaj9, Bm7add11, Gmaj7, A).
Intro: soft pad, bell on the logo reveal, riser into the product. Groove: sub, soft kick, snap, shaker, plucked
arpeggio with ping-pong delay. Whooshes on chapter changes, ticks on click ripples, ring-out on the closing card.
"""
import sys
import wave

import numpy as np

SR = 48000
DUR = 38.95
N = int(SR * DUR)
OFF = 0.35
rng = np.random.default_rng(7)

BEAT = 60 / 96
BAR = BEAT * 4
GROOVE = 7.6 + OFF            # product appears
END = 36.1 + OFF              # closing card
CHAPTERS = [17.5 + OFF, 25.2 + OFF]
CLICKS = [23.70 + OFF, 27.16 + OFF]
LOGO = 3.32 + OFF

CH = {  # pad voicing, pluck tones, bass root (MIDI)
    'D': ([50, 57, 61, 64, 66], [74, 78, 81, 76], 38),
    'Bm': ([47, 54, 57, 62, 64], [71, 74, 78, 76], 35),
    'G': ([43, 50, 54, 59, 62], [67, 71, 74, 78], 31),
    'A': ([45, 52, 57, 59, 64], [69, 73, 76, 78], 33),
}
PROG = ['D', 'Bm', 'G', 'A']

L = np.zeros(N)
Rt = np.zeros(N)
REV = np.zeros((2, N))  # send to reverb


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def add(sig, t0, gain=1.0, pan=0.0, rev=0.0):
    i0 = int(t0 * SR)
    if i0 >= N:
        return
    if i0 < 0:
        sig = sig[-i0:]
        i0 = 0
    sig = sig[:N - i0]
    gl, gr = gain * np.sqrt(0.5 * (1 - pan)), gain * np.sqrt(0.5 * (1 + pan))
    L[i0:i0 + len(sig)] += sig * gl
    Rt[i0:i0 + len(sig)] += sig * gr
    if rev:
        REV[0, i0:i0 + len(sig)] += sig * gl * rev
        REV[1, i0:i0 + len(sig)] += sig * gr * rev


def env(n, a, r, hold=None):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    if hold is not None:
        e *= np.where(t > hold, np.exp(-(t - hold) / r), 1)
    return e


# ---------------------------------------------------------------- instruments
def pad_note(m, dur, a=0.9, r=1.4):
    n = int((dur + r * 3) * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for det in (-0.004, 0.0, 0.0045):
        f = hz(m) * (1 + det)
        for k in range(1, 9):
            s += np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6.28)) / k * np.exp(-k / 3.2)
    lfo = 1 + 0.08 * np.sin(2 * np.pi * 0.23 * t)
    return s * lfo * env(n, a, r, hold=dur) / 6


def pluck(m, vel=1.0):
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = hz(m)
    s = np.zeros(n)
    for k in range(1, 7):
        s += np.sin(2 * np.pi * f * k * t) / k ** 1.3 * np.exp(-t * (3.5 + 2.2 * k))
    s *= np.minimum(1, t / 0.004)
    return s * vel


def bell(m, dur=3.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for ratio, amp, dec in ((1, 1, 1.6), (2.76, 0.45, 3.5), (5.4, 0.25, 6), (8.93, 0.12, 9)):
        s += amp * np.sin(2 * np.pi * hz(m) * ratio * t) * np.exp(-t * dec)
    return s * np.minimum(1, t / 0.003)


def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 46 + 70 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9) + 0.04 * rng.normal(0, 1, n) * np.exp(-t * 300)


def noise_hit(dur, decay, bright=True):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = rng.normal(0, 1, n)
    if bright:
        x = np.diff(x, prepend=0)
    return x * np.exp(-t * decay)


def bass(m, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
    return s * np.minimum(1, t / 0.02) * np.exp(-t * 1.8)


def whoosh(dur, rise=True):
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    y = np.zeros(n)
    acc = 0.0
    for i in range(n):  # one-pole lowpass with a sweeping cutoff
        u = i / n if rise else 1 - i / n
        a = 0.01 + 0.25 * u ** 2
        acc += a * (x[i] - acc)
        y[i] = acc
    shape = np.sin(np.pi * np.linspace(0, 1, n) ** (0.7 if rise else 1.3))
    return y * shape * 4


def tick():
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1850 * t) * np.exp(-t * 60) + 0.3 * rng.normal(0, 1, n) * np.exp(-t * 400))


# ---------------------------------------------------------------- arrangement
# intro pads: Bm (hook) -> D with bell on the logo -> G -> A, riser into the product
for name, t0, t1 in (('Bm', 0.0, LOGO), ('D', LOGO, 5.55), ('G', 5.55, 6.75), ('A', 6.75, GROOVE)):
    for m in CH[name][0]:
        add(pad_note(m, t1 - t0, a=1.2 if t0 == 0 else 0.5), t0, gain=0.10, pan=rng.uniform(-0.4, 0.4), rev=0.5)
for m, g, p in ((86, 0.07, -0.3), (81, 0.05, 0.3), (90, 0.035, 0.0)):
    add(bell(m, 3.5), LOGO, gain=g, pan=p, rev=0.8)
add(whoosh(0.75), GROOVE - 0.72, gain=0.05, rev=0.3)
add(bell(74, 2.0), GROOVE, gain=0.05, rev=0.6)

# groove
bar = 0
t = GROOVE
while t < END - 1e-6:
    name = PROG[bar % 4]
    pads, tones, root = CH[name]
    bar_len = min(BAR, END - t)
    for m in pads:
        add(pad_note(m, bar_len, a=0.35, r=0.9), t, gain=0.038, pan=rng.uniform(-0.5, 0.5), rev=0.45)
    lift = 0.65 if bar < 2 else 1.0  # chapter 01 starts lighter
    for b in range(4):
        tb = t + b * BEAT
        if tb >= END:
            break
        add(bass(root + 12, BEAT * 0.95), tb, gain=0.16 * lift)
        if b in (0, 2):
            add(kick(), tb, gain=0.20 * lift)
        if b in (1, 3) and bar >= 1:
            add(noise_hit(0.15, 38), tb, gain=0.035, pan=0.1, rev=0.35)
        for h in range(2):
            add(noise_hit(0.05, 120), tb + h * BEAT / 2, gain=0.012 * (1.3 if h else 0.8), pan=0.35)
    pattern = [0, 2, 1, 3, 2, 1, 3, 2]
    for e, ix in enumerate(pattern):
        te = t + e * BEAT / 2
        if te >= END:
            break
        vel = (0.9 if e % 2 == 0 else 0.6) * lift * rng.uniform(0.85, 1.0)
        p = pluck(tones[ix], vel)
        pan = -0.35 if e % 2 == 0 else 0.35
        add(p, te, gain=0.06, pan=pan, rev=0.3)
        for k, (dl, g) in enumerate(((0.75 * BEAT, 0.35), (1.5 * BEAT, 0.16))):  # ping-pong delay
            add(p, te + dl, gain=0.06 * g, pan=-pan if k == 0 else pan, rev=0.4)
    t += BAR
    bar += 1

for tc in CHAPTERS:
    add(whoosh(0.6), tc - 0.55, gain=0.045, pan=-0.2, rev=0.3)
for tc in CLICKS:
    add(tick(), tc, gain=0.05, pan=0.15)

# closing card: resolve to D, bell, ring out
for m in CH['D'][0] + [69]:
    add(pad_note(m, DUR - END - 0.6, a=0.25, r=1.0), END, gain=0.05, pan=rng.uniform(-0.5, 0.5), rev=0.6)
for m, g, p in ((86, 0.09, -0.25), (81, 0.06, 0.25)):
    add(bell(m, 3.0), END, gain=g, pan=p, rev=0.8)
add(bass(38 + 12, 1.6), END, gain=0.14)
add(kick(), END, gain=0.16)

# ---------------------------------------------------------------- reverb (FFT convolution) + master
ir_n = int(2.4 * SR)
tt = np.arange(ir_n) / SR
nfft = 1 << int(np.ceil(np.log2(N + ir_n)))
for c in range(2):
    ir = rng.normal(0, 1, ir_n) * np.exp(-tt * 2.6)
    ir = np.convolve(ir, np.ones(6) / 6, mode='same')  # darken
    wet = np.fft.irfft(np.fft.rfft(REV[c], nfft) * np.fft.rfft(ir, nfft), nfft)[:N]
    wet *= 0.018
    if c == 0:
        L += wet
    else:
        Rt += wet

mix = np.stack([L, Rt], 1)
fade_in = np.minimum(1, np.arange(N) / (0.8 * SR))
fade_out = np.clip((DUR - np.arange(N) / SR) / 1.6, 0, 1)
mix *= (fade_in * fade_out)[:, None]
mix = np.tanh(mix * 1.2) / 1.2  # gentle soft clip
mix *= 0.5 / np.max(np.abs(mix))

out = sys.argv[1] if len(sys.argv) > 1 else 'showcase_music.wav'
with wave.open(out, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('wrote', out, round(N / SR, 2), 's')
