---
description: 前処理→構造化→調査。inputs/urls から research/ のエビデンス群を作る
---

会議録・公開資料を機械前処理し、調査エージェントで research/ のエビデンスを整える。
メイン会話に生資料を載せないこと。手順:

1. `scripts/urls.txt` にURLがあれば `bash scripts/fetch.sh` を実行して inputs/ に取得。
   続いて `python3 scripts/extract.py` でキーワード抽出（ヒット率>10%なら KEYWORDS を絞る）。
2. `inputs/*.txt` / `research/extract_*.md` があれば **minutes-structurer** に構造化を委譲し
   `research/struct_*.md` を作らせる。（メイン会話は生テキストを読まない）
3. 不足している基盤エビデンスを、対応する調査エージェントに並行で作らせる:
   - **evidence-miner** → `research/facts.md`（未作成なら）
   - **policy-tracker** → `research/policy.md`（未作成なら）
   - **channel-audit** → `research/channels.md`（未作成なら）
4. 生成された research/ の各ファイルの要点を3〜5行で要約し、`draft/outline.md` の
   どのページに使えるかを対応づけて報告する。research/ 本文の全文はメイン会話に展開しない。

引数 `$ARGUMENTS` があれば、その論点（例: セキュリティ, 標準化）に絞って調査する。
