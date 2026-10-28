#!/bin/bash
# Build everything derived from the private inputs (all git-ignored): reference frames, OCR keyframes,
# fake-data templates and the music. Needs inputs/raw_part1.webm, inputs/raw_part2.webm, inputs/voiceover.mp3
# and private/subs.json.
set -e
cd "$(dirname "$0")"
for f in inputs/raw_part1.webm inputs/raw_part2.webm inputs/voiceover.mp3 private/subs.json; do
  [ -f "$f" ] || { echo "missing $f (see HANDOFF.md)"; exit 1; }
done
mkdir -p raw kf
for t in 1 23.5 29; do ffmpeg -v error -y -ss $t -i inputs/raw_part1.webm -frames:v 1 raw/r_$t.png; done
ffmpeg -v error -y -ss 17.3 -i inputs/raw_part2.webm -frames:v 1 raw/q_17.3.png
python3 ocr_kf.py 0.2 2.6 4 6 8 10 12 14 16 &
python3 ocr_kf.py 22.8 23.3 25 26.5 27.9 28.7 28.9 29 29.1 33 &
python3 ocr_kf.py 37 38.5 40 41.5 43 44.5 &
python3 ocr_kf.py 46 47.5 49 50.2 &
wait
python3 fakedata.py | tail -3
python3 music.py showcase_music.wav
echo "prepare done"
