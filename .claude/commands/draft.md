---
description: 指定ページを執筆する（例: /draft 7）。research/ を基に summary-editor が清書
---

`draft/outline.md` の第 **$ARGUMENTS** ページを執筆する。手順:

1. `draft/outline.md` で該当ページの「ページ内容」「主担当エージェント」を確認する。
2. そのページに必要な立案が research/ に未整備なら、対応する立案エージェントを先に走らせる:
   - 中核戦略（アプリ/チャネル）→ **app-strategy**（必要に応じ channel-audit）
   - 内部業務/標準化 → **internal-ops**
   - セキュリティ/基盤 → **infra-security**
   立案結果は `research/strategy-*.md` に保存させる。
3. 必要な research/ 文書を **summary-editor** に渡し、`draft/pNN_*.md` を1ページとして執筆させる。
   - 本文300字以内・図表中心・出典必須・施策は担当課/概算費用/初年度工数を明記。
4. できたページを表示し、`draft/outline.md` の状態列を 🔵査読待ち に更新する。
5. 「次は `/review $ARGUMENTS` で査読し、その後 `/clear` してください」と案内する。

必ず research/ の中間生成物を根拠にする。生資料（inputs/）を直接読まないこと。
