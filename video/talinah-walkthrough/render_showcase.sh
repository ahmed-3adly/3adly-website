#!/bin/bash
# Full-quality showcase render (4 parallel chunks), voice-over, music mix and a full-frame privacy audit.
cd "$(dirname "$0")"
VO=${VO:-inputs/voiceover.mp3}
rm -f s?.mp4 audit_*.png audit_?.json
python3 showcase.py s1.mp4 --noaudio --to 9.6 > s1.log 2>&1 &
python3 showcase.py s2.mp4 --noaudio --from 9.6 --to 19.2 > s2.log 2>&1 &
python3 showcase.py s3.mp4 --noaudio --from 19.2 --to 28.8 > s3.log 2>&1 &
python3 showcase.py s4.mp4 --noaudio --from 28.8 --to 38.6 > s4.log 2>&1 &
wait
printf "file s1.mp4\nfile s2.mp4\nfile s3.mp4\nfile s4.mp4\n" > slist.txt
ffmpeg -v error -y -f concat -safe 0 -i slist.txt -i "$VO" -filter_complex \
  "[1:a]atrim=0:36.6,afade=t=out:st=36.2:d=0.4,adelay=350:all=1,apad[a]" -map 0:v -map "[a]" \
  -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart talinah_showcase.mp4
./mixmusic.sh talinah_showcase.mp4 showcase_music.wav talinah_showcase_music.mp4
for i in 0 1 2 3; do python3 audit.py talinah_showcase.mp4 $i 4 > audit_$i.json 2>/dev/null & done
wait
cat audit_?.json   # every frame OCR'd; any hit is a real name that slipped through
