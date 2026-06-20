#!/usr/bin/env bash
# Tải toàn bộ asset (Three.js + texture) về local để chạy OFFLINE.
# Chạy 1 lần sau khi clone:  bash download-assets.sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
VENDOR="$DIR/assets/vendor"
TEX="$DIR/assets/textures"
mkdir -p "$VENDOR" "$TEX"

THREE_URL="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
TEX_BASE="https://cdn.jsdelivr.net/gh/KyleGough/solar-system@master/static/textures"

TEXTURES=(
  sun.jpg mercury.jpg venus.jpg earth.jpg moon.jpg mars.jpg
  jupiter.jpg io.jpg europa.jpg ganymede.jpg callisto.jpg
  saturn.jpg saturn-ring.png titan.webp uranus.jpg neptune.jpg triton.jpg
)

dl() { # url dest
  if command -v curl >/dev/null 2>&1; then curl -fL --retry 3 -o "$2" "$1";
  else wget -O "$2" "$1"; fi
}

echo "→ Three.js r128…"
dl "$THREE_URL" "$VENDOR/three.min.js"

echo "→ Textures (${#TEXTURES[@]} files)…"
for f in "${TEXTURES[@]}"; do
  echo "   $f"
  dl "$TEX_BASE/$f" "$TEX/$f"
done

echo "✓ Xong. Mở index.html là chạy offline được rồi."
