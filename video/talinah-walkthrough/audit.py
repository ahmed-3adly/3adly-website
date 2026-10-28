import json, os, re, subprocess, sys
import numpy as np, cv2
from rapidocr_onnxruntime import RapidOCR
V = sys.argv[1]; part = int(sys.argv[2]); parts = int(sys.argv[3])
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
_P = json.load(open(HERE + 'private/subs.json'))
_COMMON = {'gmail', 'hotmail', 'outlook', 'example', 'com', 'co', 'uk'}
BAD = sorted({w for real, _ in _P['subs'] for w in re.split(r'[^a-z0-9]+', real.lower())
              if len(w) >= 4 and w not in _COMMON} | set(_P.get('audit_extra', [])))
FS = 1080 * 1920 * 3
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', V, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
e = RapidOCR()
hits, i, checked = [], 0, 0
while True:
    b = p.stdout.read(FS)
    if len(b) < FS:
        break
    if i % parts == part:
        fr = np.frombuffer(b, np.uint8).reshape(1080, 1920, 3)
        r, _ = e(fr)
        checked += 1
        for box, txt, s in (r or []):
            if any(k in txt.lower().replace(' ', '') for k in BAD):
                hits.append((round(i / 30, 3), txt, [int(v) for v in box[0]]))
                cv2.imwrite(HERE + f'audit_{i / 30:.2f}.png', fr)
    i += 1
print(json.dumps({'checked': checked, 'hits': hits}))
