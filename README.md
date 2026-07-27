# 上野裕太郎｜Yutaro UENO — Personal Site

理論社会学／AIガバナンスをテーマとする個人サイト＋ブログ。

- **構成:** GitHub Pages 標準の **Jekyll** サイト。`.md` を置くだけで自動的にHTML化・公開されます（ビルドスクリプト不要）
- **公開:** `main` への push を GitHub Pages が自動でビルド＆デプロイ
- **URL:** 独自ドメイン `https://yutaro0518.com`（`.html` なしのクリーンURL）

## 構成

```
├─ _config.yml          サイト設定（タイトル / カテゴリ など）
├─ _layouts/            ページの雛形（default / home / page / activities / blog / post）
├─ _includes/           共通パーツ（head / nav / social / scripts）
├─ index.html           トップ（名前だけのランディング。layout: home）
├─ about.md             About me（本文だけ編集すればOK）
├─ bio.md               Bio
├─ research.md          Research
├─ activities.html      Activities（カード）
├─ blog/
│   ├─ index.html       ブログ一覧（記事は自動で並ぶ）
│   ├─ *.md             記事（★ここに .md を置くだけ★）
│   └─ images/          記事のサムネイル・画像
├─ style.css            デザイン（全ページ共通）
└─ CNAME                独自ドメイン設定
```

## ブログ記事を追加する

`blog/` に frontmatter 付きの `.md` を1枚置いて push するだけ。

```markdown
---
title: "記事タイトル"
date: 2026-08-01
category: "Essay"          # Essay / Book / Log（未指定は Log）
excerpt: "一覧に出る要約。"
thumbnail: images/xxx.jpeg  # blog/images/ に置いた画像（任意）
---

本文を Markdown で。
```

> **ポイント**
> - 見出しは `## 見出し` のように `#` の後に**半角スペース**（kramdown 仕様）
> - `thumbnail` は `blog/images/` 内の実ファイル名と拡張子まで一致させる
> - ファイル名がそのまま URL になります（例: `2026-08-01-my-post.md` → `/blog/2026-08-01-my-post/`）

## ページ本文を直す

- About / Bio / Research → `about.md` / `bio.md` / `research.md` の本文を Markdown で編集
- Activities → `activities.html` のカードを編集
- カテゴリの追加・並び順 → `_config.yml` の `categories_list`
- デザイン → `style.css`

いずれも編集して push すれば自動で反映されます。
