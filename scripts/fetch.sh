#!/usr/bin/env bash
# scripts/urls.txt のURLを inputs/ にダウンロードし、PDFはテキスト化する。
# LLMを使わない前処理。ダウンロード物は inputs/ に置き、メイン会話は直接読まない。
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p inputs

i=0
while IFS= read -r url; do
  # 空行・コメント行スキップ
  [[ -z "${url// }" ]] && continue
  [[ "$url" =~ ^[[:space:]]*# ]] && continue
  i=$((i+1))
  base=$(printf '%03d' "$i")
  ext="${url##*.}"
  case "$ext" in
    pdf|PDF) out="inputs/${base}.pdf" ;;
    *)       out="inputs/${base}.html" ;;
  esac
  echo "[$i] fetching: $url -> $out"
  curl -sSL --retry 3 -o "$out" "$url" || { echo "  ! failed"; continue; }
  if [[ "$out" == *.pdf ]]; then
    pdftotext -layout "$out" "inputs/${base}.txt" && echo "  -> inputs/${base}.txt"
  fi
done < scripts/urls.txt

echo "done. $i 件処理。inputs/*.txt を scripts/extract.py にかけてください。"
