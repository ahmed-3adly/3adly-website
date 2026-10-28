import json, os, subprocess, sys
import cv2, numpy as np
from rapidocr_onnxruntime import RapidOCR
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
SRC = HERE + 'inputs/raw_part1.webm'
CW, CH = 1890, 900
times = [float(x) for x in sys.argv[1:]]
e = RapidOCR()
res = {}
for t in times:
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', SRC, '-frames:v', '1', '-vf', f'crop={CW}:{CH}:0:10',
                        '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE, check=True)
    fr = np.frombuffer(p.stdout, np.uint8).reshape(CH, CW, 3)
    cv2.imwrite(HERE + f'kf/{t:.2f}.png', fr)
    r, _ = e(fr)
    res[f'{t:.2f}'] = [[[int(v) for v in b[0]], [int(v) for v in b[2]], txt, float(s)] for b, txt, s in (r or [])]
json.dump(res, open(HERE + f'kf/ocr_{times[0]:.2f}.json', 'w'))
