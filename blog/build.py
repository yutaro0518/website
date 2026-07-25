#!/usr/bin/env python3
"""
上野裕太郎 Blog ビルドスクリプト

使い方:
    python3 build.py

posts/ 内の *.md を読み込み、記事ページと index.html を生成する。
記事の追加は「posts/ に .md を1枚置いて、このスクリプトを実行する」だけ。
"""

import re
import html
from pathlib import Path
import markdown

ROOT = Path(__file__).parent          # blog/ ディレクトリ
POSTS_DIR = ROOT / "posts"
SITE_ROOT = ROOT.parent               # リポジトリのルート

# 一覧上部のカテゴリナビ（表示順）
CATEGORIES = [
    "All", "論考", "研究ノート", "読書", "日常",
]

# ---- 共通パーツ -------------------------------------------------------------

def head(title):
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+JP:wght@300;400;500;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="style.css" />
</head>
<body>"""


def header_html():
    return """  <header class="blog-header">
    <div class="blog-header__inner">
      <a href="../index.html" class="blog-home">← 上野裕太郎</a>
      <a href="index.html" class="blog-logo">Blog</a>
      <span class="blog-logo__sub">Yutaro UENO</span>
    </div>
  </header>"""


def footer_html():
    return """  <footer class="blog-footer">
    <p class="blog-footer__left">Tokyo, Japan　<span>© 2026 Yutaro UENO</span></p>
    <div class="blog-footer__social">
      <a href="https://x.com/yutaro_0518" target="_blank" rel="noopener" aria-label="X (Twitter)">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
      </a>
      <a href="https://www.linkedin.com/in/yutaro0518/" target="_blank" rel="noopener" aria-label="LinkedIn">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
      </a>
    </div>
  </footer>"""


def nav_html():
    items = []
    for i, c in enumerate(CATEGORIES):
        cls = ' class="is-active"' if i == 0 else ""
        cat_val = "all" if i == 0 else html.escape(c)
        items.append(
            f'    <a href="#"{cls} data-cat="{cat_val}">{html.escape(c)}</a>')
    return '  <nav class="category-nav">\n' + "\n".join(items) + "\n  </nav>"


def page(title, body):
    return f"""{head(title)}
{header_html()}
{body}
{footer_html()}
</body>
</html>
"""

# ---- frontmatter パーサ -----------------------------------------------------

def parse_post(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if not m:
        raise ValueError(f"frontmatter がありません: {path.name}")
    meta_block, body_md = m.group(1), m.group(2)

    meta = {}
    for line in meta_block.splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, val = line.split(":", 1)
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        meta[key.strip()] = val

    for req in ("title", "date", "category"):
        if req not in meta:
            raise ValueError(f"{path.name}: '{req}' が frontmatter にありません")

    meta["slug"] = path.stem
    meta["body_html"] = markdown.markdown(
        body_md, extensions=["extra", "sane_lists"]
    )
    meta.setdefault("excerpt", "")
    meta.setdefault("thumbnail", "")
    return meta


def date_ja(iso):
    y, mth, d = iso.split("-")
    return f"{int(y)}年{int(mth)}月{int(d)}日"

# ---- 記事ページ生成 ---------------------------------------------------------

def render_article(p):
    thumb = ""
    if p["thumbnail"]:
        thumb = (f'    <div class="article__hero">'
                 f'<img src="{html.escape(p["thumbnail"])}" alt="" /></div>\n')
    body = f"""  <article class="article">
    <a href="index.html" class="article__back">← ブログ一覧へ戻る</a>
    <h1 class="article__title">{html.escape(p["title"])}</h1>
    <div class="article__meta">{html.escape(p["category"])} ・ {date_ja(p["date"])}</div>
{thumb}    <div class="article__body">
{p["body_html"]}
    </div>
  </article>"""
    out = ROOT / f'{p["slug"]}.html'
    out.write_text(page(f'{p["title"]} | 上野裕太郎 Blog', body), encoding="utf-8")
    return out.name

# ---- 一覧ページ生成 ---------------------------------------------------------

def render_index(posts):
    cards = []
    for p in posts:
        link = f'{p["slug"]}.html'
        thumb = ""
        if p["thumbnail"]:
            thumb = (f'      <a href="{link}" class="post__thumb">'
                     f'<img src="{html.escape(p["thumbnail"])}" alt="" /></a>\n')
        excerpt = ""
        if p["excerpt"]:
            excerpt = f'      <p class="post__excerpt">{html.escape(p["excerpt"])}</p>\n'
        cards.append(f"""    <article class="post" data-category="{html.escape(p["category"])}">
      <a href="{link}"><h2 class="post__title">{html.escape(p["title"])}</h2></a>
      <div class="post__meta">
        <span class="post__cat">{html.escape(p["category"])}</span>
        <span>{date_ja(p["date"])}</span>
      </div>
{thumb}{excerpt}      <a href="{link}" class="post__more">read more</a>
    </article>""")

    empty = '    <p class="post-empty" hidden>このカテゴリの記事はまだありません。</p>'
    body = ('  <div class="blog-intro"><h1>Blog</h1>'
            '<p>理論社会学・AIガバナンス・気候変動をめぐって考えたことのログ。</p></div>\n\n'
            + nav_html()
            + '\n\n  <main class="post-list">\n'
            + "\n\n".join(cards) + "\n" + empty + "\n  </main>\n" + FILTER_JS)
    (ROOT / "index.html").write_text(
        page("上野裕太郎 Blog", body), encoding="utf-8")

# 一覧のカテゴリ絞り込み（クリックで表示/非表示を切り替え）
FILTER_JS = """  <script>
  (function () {
    var nav = document.querySelector(".category-nav");
    var posts = Array.prototype.slice.call(document.querySelectorAll(".post"));
    var empty = document.querySelector(".post-empty");
    if (!nav) return;

    function apply(cat) {
      var shown = 0;
      posts.forEach(function (el) {
        var match = cat === "all" || el.getAttribute("data-category") === cat;
        el.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
    }

    nav.addEventListener("click", function (e) {
      var a = e.target.closest("a[data-cat]");
      if (!a) return;
      e.preventDefault();
      nav.querySelectorAll("a").forEach(function (x) {
        x.classList.remove("is-active");
      });
      a.classList.add("is-active");
      apply(a.getAttribute("data-cat"));
    });
  })();
  </script>"""

# ---- トップページに最新記事を差し込む（任意：テンプレートがある場合のみ） -----

def render_top(posts, n=3):
    template = SITE_ROOT / "index.template.html"
    if not template.exists():
        return
    cards = []
    for p in posts[:n]:
        link = f'blog/{p["slug"]}.html'
        cards.append(f"""      <article class="home-card">
        <div class="home-card__body">
          <div class="home-card__meta"><span class="home-card__cat">{html.escape(p["category"])}</span><span>{date_ja(p["date"])}</span></div>
          <a href="{link}"><h3 class="home-card__title">{html.escape(p["title"])}</h3></a>
        </div>
      </article>""")
    html_out = template.read_text(encoding="utf-8").replace(
        "<!--LATEST_POSTS-->", "\n".join(cards))
    (SITE_ROOT / "index.html").write_text(html_out, encoding="utf-8")
    print(f"  トップページ最新記事を更新（{min(n, len(posts))}件）")

# ---- main -------------------------------------------------------------------

def main():
    md_files = sorted(POSTS_DIR.glob("*.md"))
    if not md_files:
        print("posts/ に .md がありません。")
        return
    posts = [parse_post(f) for f in md_files]
    posts.sort(key=lambda p: p["date"], reverse=True)   # 新しい順

    for p in posts:
        name = render_article(p)
        print(f"  記事生成: {name}")
    render_index(posts)
    render_top(posts)
    print(f"\n✅ 完了: {len(posts)}件の記事 + 一覧を生成しました。")


if __name__ == "__main__":
    main()
