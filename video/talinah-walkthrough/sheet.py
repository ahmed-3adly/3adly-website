import sys, glob, cv2, numpy as np
d = sys.argv[1]; per = int(sys.argv[2]) if len(sys.argv) > 2 else 20
fs = sorted(glob.glob(d + '/f_*.jpg'))
for k in range(0, len(fs), per):
    tiles = []
    for f in fs[k:k + per]:
        im = cv2.resize(cv2.imread(f), (480, 270))
        n = int(f.split('_')[-1][:5]); t = n / 30 - 0.35
        cv2.putText(im, f'{t:.1f}', (6, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        tiles.append(im)
    while len(tiles) % 4: tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]
    cv2.imwrite(f'{d}/sheet_{k // per:02d}.png', np.vstack(rows))
