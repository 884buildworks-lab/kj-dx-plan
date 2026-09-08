# 木城町 DX推進計画（概要版）策定リポジトリ

公開情報のみで作る**仮説版**。Claude Code 単独のマルチエージェント構成で運用する。

## 実行環境

このリポジトリは **Claude Code Web版（claude.ai/code）** で運用する前提。
ローカル（`claude` CLI）でも動くが、その場合は poppler と日本語フォントを各自で用意する。

Web版では初回セッションで以下が自動的に使える状態になっている（未導入なら下記を実行）：

```bash
apt-get update && apt-get install -y --no-install-recommends poppler-utils   # pdftotext
pip install fpdf2 markdown                                                     # 補助
# 日本語フォント: IPAゴシック（同梱）／ PDF化: Chromium（同梱）
```

## 運用ループ（1ページごとに /clear を挟む）

```
1. 調査対象（会議録・公開資料）のURLを scripts/urls.txt に貼る
2. /mine          … 前処理（PDF→テキスト→キーワード抽出）→ 構造化 → エビデンス表
3. /draft 2       … 2ページ目を執筆
4. /review 2      … 3体で査読（feasibility / alignment / hypothesis）
5. /clear         … コンテキストを捨てて次のページへ
```

13ページを1セッションで書こうとすると自動コンパクションで前半の判断が失われる。
`/draft` と `/review` は1ページごとに `/clear` を挟むこと。

## ディレクトリ

```
inputs/     元資料（読み取り専用扱い。メイン会話は直接読まない）
research/   中間生成物。メイン会話が読むのはここだけ
draft/      成果物。1ページ1ファイル。outline.md に割付
scripts/    LLMを使わない前処理・PDFビルド
```

## エージェント12体

| 層 | エージェント | モデル |
|---|---|---|
| 前処理 | minutes-structurer | haiku |
| 調査 | policy-tracker / channel-audit / evidence-miner | opus |
| 立案 | app-strategy / internal-ops / infra-security | opus |
| 検証 | hypothesis-keeper / feasibility-critic / alignment-checker | opus |
| 編集 | summary-editor / interview-designer | opus |

feasibility-critic と alignment-checker は書き込み権限なし。指摘のみ返す。

## トークン節約の考え方

| 段階 | 手段 | 消費 |
|---|---|---|
| PDF → テキスト → キーワード抽出 | pdftotext + Python | ゼロ |
| 抽出結果 → 構造化表 | minutes-structurer (haiku) | 小 |
| 構造化表 → 判断・執筆 | メイン会話 + opus エージェント | 最小限 |

`inputs/` の生資料をメイン会話のコンテキストに載せないことが最大の節約になる。
`extract.py` のヒット率が10%を超えたら KEYWORDS が広すぎる。

## PDF出力

```bash
bash scripts/build_pdf.sh    # draft/ の各ページを結合し A4 PDF を生成
```

## 進捗

`draft/outline.md` の状態列を更新していく。
