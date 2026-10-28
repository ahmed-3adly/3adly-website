#!/bin/bash
# usage: mixmusic.sh in.mp4 music.wav out.mp4  — duck the music under the VO, then master to -14 LUFS
ffmpeg -v error -y -i "$1" -i "$2" -filter_complex \
 "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][key];\
  [1:a]volume=0.8[m];\
  [m][key]sidechaincompress=threshold=0.015:ratio=6:attack=20:release=400:knee=4[md];\
  [vo][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$3"
