#!/usr/bin/env python3
"""
メインページ（About / Bio / Research）を content/*.md から生成する。

使い方:
    python3 build.py

編集は content/*.md だけ。実行すると about.html / bio.html / research.html を再生成する。
（index.html と activities.html は手書きのまま。ブログは blog/build.py）
"""

import re
import html
import hashlib
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"

PAGES = ["about", "bio", "research"]

X_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 '
         '8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 '
         '6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>')
LINKEDIN_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569'
                'c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414'
                'v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337'
                ' 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9'
                'h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24'
                'h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>')


def asset_v(name):
    """style.css / script.js の内容ハッシュ（キャッシュ更新用）。"""
    p = ROOT / name
    return hashlib.md5(p.read_bytes()).hexdigest()[:8] if p.exists() else "1"


def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if not m:
        raise ValueError(f"frontmatter がありません: {path.name}")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"\'')
    body = markdown.markdown(m.group(2), extensions=["extra", "sane_lists"])
    return meta, body


def nav(slug):
    def a(active):
        return ' class="active"' if active else ''
    in_about = slug in PAGES
    return f'''      <nav class="nav-links">
        <div class="nav-item has-dropdown">
          <a href="about.html"{a(in_about)}>About me <span class="caret" aria-hidden="true">▾</span></a>
          <div class="dropdown"><div class="dropdown-inner">
            <a href="about.html"{a(slug == "about")}>About</a>
            <a href="bio.html"{a(slug == "bio")}>Bio</a>
            <a href="research.html"{a(slug == "research")}>Research</a>
          </div></div>
        </div>
        <a href="blog/?cat=Essay">Thought</a>
        <div class="nav-item has-dropdown">
          <a href="activities.html">Activities <span class="caret" aria-hidden="true">▾</span></a>
          <div class="dropdown"><div class="dropdown-inner">
            <a href="https://humanresearchcollective.substack.com/" target="_blank" rel="noopener">Human Research Collective<span class="ext">↗</span></a>
          </div></div>
        </div>
        <a href="blog/">Blog</a>
      </nav>'''


def render(slug, meta, body, css_v, js_v):
    title = meta.get("title", slug)
    desc = meta.get("desc", "")
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}｜上野裕太郎</title>
  <meta name="description" content="{html.escape(desc)}" />
  <script>(function(){{try{{var t=localStorage.getItem('theme');if(!t){{t=window.matchMedia&&window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';}}document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+JP:wght@300;400;500;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="style.css?v={css_v}" />
</head>
<body>

  <header class="site-header scrolled" id="top">
    <div class="nav-inner">
      <a href="index.html" class="brand">
        <span class="brand-jp">上野裕太郎</span>
        <span class="brand-en">Yutaro&nbsp;UENO</span>
      </a>
      <button class="nav-toggle" aria-label="メニュー" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <button class="theme-toggle" type="button" aria-label="テーマ切り替え（ライト / ダーク）">
        <span class="tt-opt tt-l">L</span>
        <span class="tt-opt tt-d">D</span>
      </button>
{nav(slug)}
    </div>
  </header>

  <main class="page">
    <div class="page-head">
      <h1>{html.escape(title)}</h1>
    </div>
    <div class="page-prose">
{body}
    </div>
  </main>

  <footer class="site-footer">
    <p class="hf-left">Tokyo, Japan　<span>© <span class="year"></span> Yutaro UENO</span></p>
    <div class="hf-social">
      <a href="https://x.com/yutaro_0518" target="_blank" rel="noopener" aria-label="X (Twitter)">{X_SVG}</a>
      <a href="https://www.linkedin.com/in/yutaro0518/" target="_blank" rel="noopener" aria-label="LinkedIn">{LINKEDIN_SVG}</a>
    </div>
  </footer>

  <script src="script.js?v={js_v}"></script>
</body>
</html>
'''


def main():
    css_v, js_v = asset_v("style.css"), asset_v("script.js")
    for slug in PAGES:
        meta, body = parse(CONTENT / f"{slug}.md")
        (ROOT / f"{slug}.html").write_text(
            render(slug, meta, body, css_v, js_v), encoding="utf-8")
        print(f"  生成: {slug}.html")
    print(f"\n✅ 完了: {len(PAGES)}ページを content/*.md から生成しました。")


if __name__ == "__main__":
    main()
