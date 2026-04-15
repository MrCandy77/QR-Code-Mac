#!/bin/bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
DIST_PATH="$PROJECT_ROOT/release"
WORK_PATH="$PROJECT_ROOT/pyinstaller-work"

cd "$PROJECT_ROOT"

python3 -m pip install -r requirements.txt

python3 -m PyInstaller \
  --noconfirm \
  --windowed \
  --clean \
  --name "QRGenerator" \
  --distpath "$DIST_PATH" \
  --workpath "$WORK_PATH" \
  --osx-bundle-identifier "com.local.qrgenerator" \
  "qr_generator_app.py"

echo
echo "Build complete. Your macOS app is here:"
echo "release/QRGenerator.app"
