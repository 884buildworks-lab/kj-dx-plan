#!/usr/bin/env python3
"""draft/p*.md を順に結合し、A4印刷用HTMLを書き出す。build_pdf.sh から呼ばれる。

各 pNN_*.md を1ページ（改ページ区切り）として扱う。図表中心・本文300字以内の
概要版レイアウトを想定した最小限の印刷CSSを付与する。
"""
import glob
import os
import sys

import markdown  # pip install markdown

CSS = """
@page { size: A4; margin: 16mm 15mm; }
* { box-sizing: border-box; }
body {
  font-family: "IPAGothic", "IPAPGothic", sans-serif;
  color: #1a1a1a; line-height: 1.7; font-size: 10.5pt; margin: 0;
}
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 20pt; color: #0b4f6c; border-bottom: 3px solid #0b4f6c;
     padding-bottom: 6px; margin: 0 0 14px; }
h2 { font-size: 14pt; color: #0b4f6c; margin: 18px 0 8px;
     border-left: 6px solid #35a7b5; padding-left: 8px; }
h3 { font-size: 11.5pt; color: #333; margin: 12px 0 4px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9.5pt; }
th, td { border: 1px solid #b9c6cc; padding: 5px 8px; text-align: left;
         vertical-align: top; }
th { background: #e8f2f4; color: #0b4f6c; }
blockquote { background: #fff7e6; border-left: 4px solid #f0a500;
             margin: 8px 0; padding: 6px 12px; font-size: 9.5pt; }
code { background: #eef2f4; padding: 1px 4px; border-radius: 3px; }
ul, ol { margin: 6px 0 6px 1.2em; padding: 0; }
li { margin: 2px 0; }
.src { font-size: 8pt; color: #777; }
"""


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "dist/_build.html"
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
    pages = []
    for path in sorted(glob.glob("draft/p*.md")):
        with open(path, encoding="utf-8") as f:
            html = md.convert(f.read())
        md.reset()
        pages.append(f'<section class="page">\n{html}\n</section>')
    if not pages:
        print("draft/p*.md がありません。", file=sys.stderr)
        sys.exit(1)
    doc = (
        "<!doctype html><html lang='ja'><head><meta charset='utf-8'>"
        f"<style>{CSS}</style></head><body>\n" + "\n".join(pages) + "\n</body></html>"
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"{len(pages)} ページ -> {out}")


if __name__ == "__main__":
    main()
