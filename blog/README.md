# 上野裕太郎 Blog

Markdownで記事を書くだけの静的ブログです。**HTMLは書きません。**
`.md` を main に入れると、GitHub Actions が `build.py` を実行してHTMLを自動生成・公開します。
（PMI ThinkTank のブログと同じ仕組み）

> **md-only 運用**：生成される `blog/*.html` は `.gitignore` 済みで、リポジトリには入りません。
> **ソースは `blog/posts/*.md` だけ**。ローカルで `python3 build.py` を実行するのは、公開前に見た目を確認したいとき（任意）です。

## 構成

```
website/                       ← サイトのルート
├─ index.html ほか *.html      ← 個人サイト本体（About / Bio / Research / Activities）
├─ requirements.txt
├─ .github/workflows/deploy.yml← main への push で自動ビルド＆公開（GitHub Actions）
└─ blog/                       ← ブログ（/blog/ で公開）
   ├─ posts/                   ← 記事の本体（.md）。★ここだけ触ればOK★
   ├─ images/                  ← サムネイル・図版
   ├─ build.py                 ← ブログ生成スクリプト（CIが実行。手動実行は任意）
   ├─ style.css                ← ブログのデザイン
   └─ *.html                   ← 一覧・各記事（自動生成・Git管理外）
```

## 記事を追加する手順（python 実行なし）

1. ブランチを切る
2. `posts/` に Markdown ファイルを1枚作る（例: `2026-08-01-my-post.md`）。画像を使うなら `images/` にも置く
3. 先頭に frontmatter を書く：

   ```markdown
   ---
   title: 記事タイトル
   date: 2026-08-01
   category: 論考
   thumbnail: images/xxx.png   （任意）
   excerpt: 一覧に表示される要約。
   ---

   ここから本文をMarkdownで書く。

   ## 見出し

   - 箇条書き
   - **強調** や [リンク](https://example.com) も使える
   ```

4. PR を作成して **main に merge**

これだけで、GitHub Actions が記事ページと一覧（**日付の新しい順**）を生成し、
1分ほどで `yutaro0518.com/blog/` に公開されます。

### ローカルで先に確認したいとき（任意）

```bash
pip install -r ../requirements.txt   # 初回のみ
python3 build.py                     # blog/*.html が生成される（コミット不要）
```

## カテゴリを変えたいとき

`build.py` 冒頭の `CATEGORIES` リストを編集してください。

## 記事を消したいとき

`posts/` から該当の `.md` を削除して merge するだけ（HTMLは自動で作り直されます）。
