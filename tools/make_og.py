#!/usr/bin/env python3
"""
ブログ記事の OGP 画像を生成する（「Yutaro's Blog」＋記事タイトルを焼き込む）。

使い方:
    pip install Pillow          # 初回のみ
    python3 tools/make_og.py

blog/*.md をすべて読み、blog/og/<ファイル名>.png（1200x630）を生成する。
記事を追加したら再実行してコミットするだけ。
"""
import re
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
OUT = BLOG / "og"
OUT.mkdir(exist_ok=True)

W, H = 1200, 630
BG = (20, 20, 18)
INK = (242, 241, 236)
ACCENT = (224, 113, 92)
LINE = (56, 55, 50)
PAD = 84

FONT_JP = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_LAT = "/System/Library/Fonts/Helvetica.ttc"


def load(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if draw.textlength(cur + ch, font=font) <= maxw:
            cur += ch
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines


def read_title(md):
    raw = md.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", raw, re.DOTALL)
    fm = m.group(1) if m else ""
    for line in fm.splitlines():
        mm = re.match(r"^\s*title\s*:\s*(.*)$", line)
        if mm:
            return mm.group(1).strip().strip("\"'")
    return md.stem


def render(title, out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    try:
        label = load(FONT_LAT, 36, index=1)   # Helvetica Bold
    except Exception:
        label = load(FONT_LAT, 36)
    d.text((PAD, 74), "Yutaro's Blog", font=label, fill=ACCENT)
    d.line([(PAD, 138), (W - PAD, 138)], fill=LINE, width=1)

    title_font = load(FONT_JP, 62)
    lines = wrap(d, title, title_font, W - 2 * PAD)
    if len(lines) > 5:
        lines = lines[:5]
        lines[-1] = lines[-1][:-1] + "…"
    lh = 88
    total = lh * len(lines)
    y = 138 + (H - 138 - total) / 2 - 10
    for ln in lines:
        d.text((PAD, y), ln, font=title_font, fill=INK)
        y += lh
    img.save(out, "PNG")


def main():
    # 一覧ページ用（タイトル無しの「Yutaro's Blog」）
    render("ブログ", OUT / "list.png")
    n = 0
    for md in sorted(BLOG.glob("*.md")):
        render(read_title(md), OUT / f"{md.stem}.png")
        n += 1
        print("  og:", md.stem)
    print(f"\n✅ {n}記事 + 一覧の OGP 画像を生成しました（blog/og/）。")


if __name__ == "__main__":
    main()
