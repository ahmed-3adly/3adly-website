#!/bin/bash
# One-time environment setup: Python deps + fonts (fontsource packages from npm, same folder layout the scripts expect).
set -e
cd "$(dirname "$0")"
pip install -q opencv-python-headless numpy pillow qrcode rapidocr_onnxruntime
mkdir -p fonts && cd fonts
npm pack -q @fontsource/poppins@5.0.8 >/dev/null && tar xzf fontsource-poppins-5.0.8.tgz            # -> fonts/package
mkdir -p serif && npm pack -q @fontsource/instrument-serif@5.0.19 >/dev/null && tar xzf fontsource-instrument-serif-5.0.19.tgz -C serif
for p in dm-sans@5.0.18 plus-jakarta-sans@5.0.20 manrope@5.0.21; do
  n=${p%@*}; mkdir -p fontsource-$n; npm pack -q @fontsource/$p >/dev/null; tar xzf fontsource-$n-*.tgz -C fontsource-$n
done
cd ..
# Inter / Inter Display are read from the system (/usr/share/fonts/opentype/inter); check they exist
ls /usr/share/fonts/opentype/inter/InterDisplay-Medium.otf >/dev/null || echo "WARNING: Inter Display not found, see HANDOFF.md"
echo "setup done"
