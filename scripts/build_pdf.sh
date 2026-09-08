#!/usr/bin/env bash
# draft/p*.md を結合し、A4・図表中心のPDFを Chromium で生成する。
# 使い方: bash scripts/build_pdf.sh [出力名]   (既定: dist/kijo-dx-plan.pdf)
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-dist/kijo-dx-plan.pdf}"
mkdir -p dist
HTML="dist/_build.html"

python3 scripts/md2html.py "$HTML"

CHROME="$(ls -d /opt/pw-browsers/chromium*/chrome-linux/chrome 2>/dev/null | head -1 || true)"
[[ -z "$CHROME" ]] && CHROME="$(command -v chromium || command -v chromium-browser || true)"
if [[ -z "$CHROME" ]]; then
  echo "Chromium が見つかりません。/opt/pw-browsers を確認してください。" >&2
  exit 1
fi

"$CHROME" --headless --no-sandbox --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$OUT" "file://$(pwd)/$HTML" 2>/dev/null

echo "生成: $OUT"
