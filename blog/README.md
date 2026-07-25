# 上野裕太郎 Blog

Markdownで記事を書き、`build.py` を実行するとHTMLが生成される静的ブログです。
（PMI ThinkTank のブログと同じ仕組み）

## 構成

```
yutaro0518/                    ← サイトのルート
├─ index.html ほか *.html      ← 個人サイト本体（About / Bio / Research / Activities）
├─ requirements.txt
├─ .github/workflows/deploy.yml← push で自動ビルド＆公開（GitHub Actions）
└─ blog/                       ← ブログ（/blog/ で公開）
   ├─ posts/                   ← 記事の本体（.md）。ここだけ触ればOK
   ├─ images/                  ← サムネイル・図版
   ├─ build.py                 ← 実行するとブログを生成
   ├─ style.css                ← ブログのデザイン
   ├─ index.html               ← 一覧（自動生成）
   └─ *.html                   ← 各記事ページ（自動生成）
```

## 記事を追加する手順

1. `posts/` に Markdown ファイルを1枚作る（例: `2026-08-01-my-post.md`）
2. 先頭に frontmatter を書く：

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

3. ビルドを実行：

   ```bash
   python3 build.py
   ```

これで記事ページが作られ、`index.html` の一覧に **日付の新しい順** で並びます。
あとは `git push` すると GitHub Actions が自動でビルド＆公開します。

## カテゴリを変えたいとき

`build.py` 冒頭の `CATEGORIES` リストを編集してください。

## 記事を消したいとき

`posts/` から該当の `.md` を削除して `build.py` を再実行。
（生成済みの `*.html` が残る場合は手動で削除）
