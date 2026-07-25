# 上野裕太郎｜Yutaro UENO — Personal Site

理論社会学／AIガバナンスをテーマとする個人サイト。トップページは名前のみのランディングで、上部の固定ナビから各ページへ遷移します（sakana.ai 風構成）。

## ページ構成

| ナビ | ページ | 内容 |
|---|---|---|
| （トップ） | `index.html` | 名前だけのランディング |
| About me | `about.html` | 自己紹介 |
| Bio | `bio.html` | 経歴 |
| Research | `research.html` | 研究テーマ |
| Thought | [外部](https://yutaro0518.substack.com/t/log) | Substack |
| Activities | `activities.html` | 所属・活動 |
| Human Research Collective | [外部](https://humanresearchcollective.substack.com/) | Substack |

## ファイル

| ファイル | 役割 |
|---|---|
| `index.html` ほか `*.html` | 各ページ |
| `style.css` | 共通デザイン |
| `script.js` | モバイルメニュー・年号・ブランド表示制御 |
| `assets/` | 画像等 |

## ローカルで確認

`index.html` をブラウザで開く、または簡易サーバーで：

```bash
python3 -m http.server 8000
# http://localhost:8000
```
