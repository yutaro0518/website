# Posting Notes from iPhone

Tap an icon on the Home Screen, type a thought, send — it appears on `/notes/`.

No server involved. The shortcut calls the GitHub API directly and creates one
file in `_notes/`. Action names below are the English ones shown in the
Shortcuts app; if your iPhone is set to another language, look for the
equivalent action.

---

## 1. Create an access token

Create a [fine-grained personal access token](https://github.com/settings/personal-access-tokens/new) on GitHub.

| Field | Value |
|---|---|
| Token name | `notes-shortcut` |
| Expiration | Your choice — set one, don't pick "No expiration" |
| Repository access | **Only select repositories** → `yutaro0518/website` |
| Permissions | **Contents** → **Read and write**. Leave everything else alone |

The token is shown only once. Copy it now; you'll paste it in step 2⑤.

> This token can write files to the repository. Don't put it in screenshots,
> don't paste it into chats, don't share it. If it ever leaks, open the token
> settings on GitHub and click **Revoke** — that kills it immediately.

---

## 2. Get the shortcut

Two ways. Try the ready-made file first; fall back to building it by hand if the
import fails.

### Option A — import the ready-made file

`docs/Post to Notes.shortcut` in this repo is the finished shortcut, **signed**
so iOS will open it directly. No settings to change.

1. Get the file onto the phone — AirDrop from the Mac is easiest.
2. Open it. Shortcuts will ask **"Paste your GitHub token"** during import —
   paste the token from step 1 there.
3. Skip to section 3.

> **iOS only opens signed shortcut files.** If you ever regenerate this file, or
> edit it on a Mac, sign it again before sending it to a phone:
>
> ```bash
> shortcuts sign --mode anyone --input unsigned.shortcut --output signed.shortcut
> ```
>
> An unsigned file fails with *"Shortcut cannot be opened"*. A signed file
> starts with the bytes `AEA1`; an unsigned one starts with `bplist` or `<?xml`.

If the file still refuses to import, build it by hand with Option B — the result
is identical.

### Option B — build it by hand

Open the **Shortcuts** app, create a new shortcut, and add these actions in order.

### ① Ask for Input

**Ask for Input**

| Setting | Value |
|---|---|
| Input Type | `Text` |
| Prompt | `What's on your mind?` |

### ② Prepare the date

Add **Date** once (it defaults to the current date).

Then add **Format Date** twice. **In each one, set the input explicitly to the
`Current Date` variable from the Date action** — don't rely on it picking up the
previous action automatically. Leaving it implicit is what produced empty dates
and a file literally named `.md`.

| | Date Format | Format String | Used for |
|---|---|---|---|
| A | `Custom` | `yyyy-MM-dd HH:mm` | the `date:` line in the file |
| B | `Custom` | `yyyy-MM-dd-HHmmss` | the filename |

> Tip: rename these two actions (long-press → Rename) to `Date A` and `Date B`
> so you don't mix them up when inserting variables later.

### ③ Build the file contents

Add a **Text** action containing exactly these four lines:

```
---
date: [Formatted Date A]
---
[Provided Input]
```

Insert `Formatted Date A` (from ②A) and `Provided Input` (from ①) as variables —
type the text, then tap the variable bar above the keyboard to insert them.

### ④ Base64 Encode

**Base64 Encode**

| Setting | Value |
|---|---|
| Input | the **Text** from ③ |
| Line Breaks | **None** |

> **Line Breaks must be None.** If it's set to every 64 or 76 characters, the
> encoded string gets newlines in it and GitHub rejects the request or stores a
> broken file. This is the single most common thing to get wrong here.

### ⑤ Send it to GitHub

**Get Contents of URL**

**URL** — insert `Formatted Date B` (from ②B) where shown:

```
https://api.github.com/repos/yutaro0518/website/contents/_notes/note-[Formatted Date B].md
```

**Method:** `PUT`

**Headers:**

| Key | Value |
|---|---|
| `Authorization` | `Bearer YOUR_TOKEN_FROM_STEP_1` |
| `Accept` | `application/vnd.github+json` |
| `X-GitHub-Api-Version` | `2022-11-28` |

**Request Body:** `JSON`

| Key | Type | Value |
|---|---|---|
| `message` | Text | `note` |
| `content` | Text | the **Base64 Encoded** result from ④ |

> Don't add a `sha` field. It's only needed when replacing an existing file, and
> every note creates a new one.

### ⑥ Confirm (optional)

**Show Notification** with something like `Posted`.

---

## 3. Put it on the Home Screen

Open the shortcut's detail view → Share → **Add to Home Screen**.

Now one tap opens the prompt and posts.

---

## Checking that it works

1. Run the shortcut and send a test line
2. Check that a new file appeared in `_notes/` on GitHub
3. Wait a few minutes, then open <https://yutaro0518.com/notes/>

If nothing shows up, look at `_notes/` first — that tells you which half failed.

| Symptom | Cause |
|---|---|
| File is named `.md` and the note never appears | The date variables resolved to empty — set the input of each **Format Date** explicitly to `Current Date` |
| No file in `_notes/` | Token permissions (needs Contents: Read and write), or the repo name in the URL |
| File exists but the page doesn't show it | Pages is still building, or the `date:` format is wrong |
| Text is garbled or cut off | Line Breaks in ④ isn't set to None |
| `401` / `403` response | Token expired, revoked, or missing the `Bearer ` prefix |
| `404` response | Wrong repo path in the URL, or the token can't see the repo |

---

## Notes on the setup

- **This commits straight to `main`.** No pull request. Opening a PR for every
  one-line thought isn't practical, so this is deliberate. Blog posts still go
  through the normal PR flow.
- To delete a note, delete its file on GitHub. It stays in the git history.
- The body is Markdown, so links and emphasis work.
- Filenames only need to be unique — ordering comes from the `date:` field in
  the file, not the filename.
