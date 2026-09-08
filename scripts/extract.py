#!/usr/bin/env python3
"""inputs/*.txt からキーワードに合致する段落だけを抜き出し research/ に書く。

LLMを使わない前処理。生資料をメイン会話のコンテキストに載せないための土台。
ヒット率（抽出行数 / 全行数）が10%を超えたら KEYWORDS が広すぎる。

使い方:
    python3 scripts/extract.py            # 既定キーワードで inputs/*.txt を処理
    python3 scripts/extract.py 標準化 予算 # キーワードを引数で上書き
出力:
    research/extract_<元ファイル名>.md    # ヒットした段落＋行番号
"""
import glob
import os
import re
import sys

# DXの概要版で拾いたい語。CLAUDE.md の論点に対応。広げすぎないこと。
KEYWORDS = [
    "DX", "デジタル", "アプリ", "LINE", "情報発信", "到達", "住民サービス",
    "標準化", "基幹", "セキュリティ", "個人情報", "マイナ",
    "行財政", "職員", "工数", "予算", "費用", "委託",
    "総合計画", "未来宣言", "推進体制", "KPI", "高齢", "防災",
]


def main():
    kws = sys.argv[1:] if len(sys.argv) > 1 else KEYWORDS
    pat = re.compile("|".join(re.escape(k) for k in kws))
    os.makedirs("research", exist_ok=True)

    files = sorted(glob.glob("inputs/*.txt"))
    if not files:
        print("inputs/*.txt がありません。先に scripts/fetch.sh を実行してください。")
        return

    for path in files:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        hits = [(n, ln.rstrip()) for n, ln in enumerate(lines, 1)
                if pat.search(ln) and ln.strip()]
        rate = (len(hits) / len(lines) * 100) if lines else 0
        name = os.path.splitext(os.path.basename(path))[0]
        out = f"research/extract_{name}.md"
        with open(out, "w", encoding="utf-8") as f:
            f.write(f"# 抽出: {path}\n\n")
            f.write(f"- 全行 {len(lines)} / ヒット {len(hits)} / ヒット率 {rate:.1f}%\n")
            f.write(f"- キーワード: {' '.join(kws)}\n\n")
            if rate > 10:
                f.write("> ⚠ ヒット率が10%超。KEYWORDS が広すぎます。絞ってください。\n\n")
            for n, ln in hits:
                f.write(f"- L{n}: {ln}\n")
        print(f"{path}: {len(hits)}/{len(lines)} 行 ({rate:.1f}%) -> {out}")


if __name__ == "__main__":
    main()
