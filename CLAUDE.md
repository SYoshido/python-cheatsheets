# CLAUDE.md — Python Cheat-Sheets

> Read this file completely before changing anything in this repository.
> It is the single source of truth for the project's purpose, structure, and rules.
> `AGENTS.md` points here, so every AI coding tool follows the same rules.

---

## 1. Project purpose

**Python Cheat-Sheets** is a small static website of one-page references for people learning Python.

- **Audience:** absolute beginners (school students, career changers). They know what a computer is, but not what a "list comprehension" is.
- **Goal of each page ("sheet"):** one concept, explained so a reader can understand it and copy a working example in under three minutes.
- **Promise to the reader:** *every code example on the site runs without errors.* This is checked by a script (see §4, §8).
- **Goal of the repository:** adding a new sheet is a *content-only* task. The AI writes one Markdown file, runs two commands, and the site updates itself. No HTML or CSS is hand-edited to add a normal sheet.

Live site: `https://<github-username>.github.io/python-cheatsheets/`
(Replace `<github-username>` with the repository owner. Served from the `docs/` folder on `main`.)

---

## 2. How the project works (mental model)

```
content/*.md  ──►  check_examples.py  ──►  build.py  ──►  docs/*.html  ──►  GitHub Pages
 (you edit)        (runs every example)   (stdlib only)    (generated)       (public website)
```

- **Source of truth = `content/`, `templates/`, `assets/`.** Humans and AI edit these.
- **`docs/` is generated output.** It is committed (GitHub Pages serves it) but is **never edited by hand**.
  Always regenerate it with `python3 build.py`.
- `build.py` and all scripts use **only the Python standard library**. Do not add dependencies, a `requirements.txt`,
  npm packages, or a framework. Do not add external CDN links, web fonts, or tracking scripts.
- Examples on the sheets target **Python 3.9+** and use only the standard library.

---

## 3. Directory structure

```
python-cheatsheets/
├── CLAUDE.md              ← this file (rules for AI)
├── AGENTS.md              ← short pointer to CLAUDE.md
├── README.md              ← short human-facing intro
├── build.py               ← static site generator + content validator (stdlib only)
├── content/
│   ├── about.md           ← standalone page  → docs/about.html
│   ├── _template.md       ← blueprint for a new sheet (files starting with _ are ignored)
│   └── sheets/            ← ONE FILE PER SHEET → docs/sheets/<slug>.html
├── templates/
│   ├── base.html          ← page shell: <head>, header, nav, footer
│   ├── home.html          ← homepage body (hero + card grid)
│   ├── page.html          ← standalone page body (e.g. About)
│   └── sheet.html         ← sheet page body (meta, TOC, content, prev/next)
├── assets/
│   └── style.css          ← the only stylesheet; copied to docs/assets/
├── scripts/
│   ├── new_sheet.py       ← scaffolds a new sheet from the template
│   └── check_examples.py  ← runs every Python example under "## Example"
└── docs/                  ← GENERATED. Do not edit by hand.
```

---

## 4. Commands

| Task | Command |
|------|---------|
| Create a new sheet file | `python3 scripts/new_sheet.py "Sheet Title" --category "Data Structures" --difficulty Beginner` |
| Run every code example | `python3 scripts/check_examples.py` |
| Validate content only (writes nothing) | `python3 build.py --check` |
| Build the site into `docs/` | `python3 build.py` |
| Preview locally | `python3 -m http.server 8000 --directory docs` then open `http://localhost:8000` |

Both `build.py` and `check_examples.py` exit with a non-zero status and a clear message when a rule is broken.
**A run that prints errors is not finished work.**

---

## 5. Content rules for sheets

### 5.1 File naming and location

- Every sheet is exactly one file: `content/sheets/<slug>.md`.
- `<slug>` is **kebab-case**: lowercase letters, digits and single hyphens only
  (`reading-files`, not `Reading_Files`). Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`.
- The slug becomes the URL, so choose it once and do not rename it later (links would break).
- Name the slug after the concept, in the plural if the concept is a type (`lists`, `strings`, `dictionaries`).
- Never put sheets anywhere except `content/sheets/`.

### 5.2 Front matter (required, at the very top of the file)

```
---
title: Lists
summary: Keep an ordered, changeable collection of values in one variable.
category: Data Structures
order: 1
difficulty: Beginner
updated: 2026-11-13
---
```

| Field | Rule |
|-------|------|
| `title` | Title Case, 1–4 words, unique across the site. |
| `summary` | One sentence, ≤ 110 characters, starts with a verb, ends with a period. Shown on homepage cards. |
| `category` | Exactly one of: `Basics`, `Data Structures`, `Control Flow`, `Functions and Files`. (The list is `CATEGORIES` in `build.py`.) |
| `order` | Integer ≥ 1. Position **within its category**; a learner should be able to read a category top to bottom. Do not reuse a number inside one category. |
| `difficulty` | `Beginner` or `Intermediate`. Use `Beginner` unless the sheet needs another sheet's concept (e.g. `try/except`). |
| `updated` | ISO date `YYYY-MM-DD`. Set to today's date whenever you edit the sheet. |

Do **not** write a `# H1` in the body — the page title comes from `title`.

### 5.3 Required body sections (in this order, as `##` headings)

1. `## What it is` — 1–3 plain sentences. Define each new term in **bold** the first time it appears.
2. `## Syntax` — a fenced ```` ```python ```` block showing the smallest useful template. Short `#` comments explain each line.
3. `## Example` — **a complete, runnable program** in a ```` ```python ```` block that prints its results (see §5.4),
   followed by one sentence saying what it prints or shows.
4. `## Common mistakes` — 3–4 bullets. Each starts with a **bold** label of the mistake, then how to avoid it.

An optional `## Related sheets` section may follow, listing 1–3 links.
`build.py` fails the build if a required section is missing or out of order.

### 5.4 Rules for code examples (most important)

- The `## Example` section contains one or more ```` ```python ```` blocks. `scripts/check_examples.py` runs each block
  **separately, in a fresh Python process, in an empty temporary folder**, so each block must be self-contained
  (its own variables, imports and any files it needs).
- An example that needs a file must create that file first (see `reading-files.md`). Never rely on files in the repo,
  the network, user input (`input()`), randomness, the current date, or third-party packages.
- Every example must print something visible. Prefer `print(...)` over a bare expression.
- Examples are 5–20 lines. Use realistic, friendly names (`scores`, `student`, `fruits`) instead of `foo`/`bar`.
- When you describe what an example prints, **verify it by running the example**. Never write expected output from memory.
- Code under `## Syntax` is *not* executed. It may contain placeholders (`name`, `collection`, `...`).
  Use `python` as the fence language there too so it is highlighted consistently.
- Code style: PEP 8, 4-space indentation, double quotes, `snake_case` names, f-strings instead of `%` or `.format()`.

### 5.5 Supported Markdown (and nothing more)

Headings `##` `###`, paragraphs, `**bold**`, `*italic*`, `` `inline code` ``, fenced code blocks
(```` ``` ````), single-level bullet (`-`) and numbered (`1.`) lists, `>` blockquotes, pipe tables, `---` rules, and links.

- **No nested lists, no raw HTML, no images** (unless the owner asks; then put files in `assets/img/`).
- Callouts: start a blockquote with `> **Tip:**` or `> **Warning:**` — these get special styling.
- Link to another page with a relative `.md` path; `build.py` rewrites it to `.html` and verifies the target exists:
  - from a sheet to a sheet: `[Lists](lists.md)`
  - from `about.md` to a sheet: `[Lists](sheets/lists.md)`
- External links use full `https://` URLs.

### 5.6 Writing style

- English, second person ("you"), active voice, present tense.
- Plain words. No jargon without a definition. Say "list", not "mutable sequence", unless you explain it.
- A whole sheet is roughly 150–300 words of prose plus code.
- Be factually careful. If you are not sure Python behaves a certain way, run it and look.
  Do not invent version numbers, benchmarks, or quotes.

---

## 6. Design rules

The site should feel like a **clean notebook page**: pale blue-grey paper, dark ink text, one blue accent,
serif headings, generous spacing, dark code blocks.

- All colors, spacing and fonts are CSS custom properties at the top of `assets/style.css`
  (`--paper`, `--ink`, `--accent`, …). Change a token there; **never hard-code a color elsewhere**.
- Fonts: system stacks only (serif for headings, sans for body, monospace for code).
- Dark mode is automatic via `prefers-color-scheme`; any new color token needs a dark value too.
- Layout must work at 360 px width (phone) up to 1200 px (desktop). Keep the text column ≤ 70 characters wide.
- Accessibility: one `<h1>` per page, visible focus outlines, text contrast ≥ 4.5:1, meaningful link text (not "click here").
- Do not add JavaScript unless the owner explicitly asks. The site works with zero JS.

---

## 7. Playbooks (step-by-step recipes for common requests)

### 7.1 "Add a new sheet" (e.g. "add a sheet about sets")

1. Read two existing sheets in `content/sheets/` to match tone, length and example style.
2. Run `python3 scripts/new_sheet.py "Sets" --category "Data Structures" --difficulty Beginner`.
   It creates `content/sheets/sets.md` with the front matter and section skeleton, and picks the next free `order`.
3. Fill in every section following §5. Remove every `TODO` marker.
4. Write the example, **run it** with `python3 scripts/check_examples.py`, then write the sentence describing its output
   from what it really printed.
5. Add `## Related sheets` links, and add a link back to the new sheet from one existing related sheet.
6. Run `python3 build.py`. Fix every error it reports.
7. Preview (§4) and look at `docs/sheets/<slug>.html`.
8. Complete the checklist in §9, then commit.

### 7.2 "Add a standalone page" (e.g. Glossary, Setup guide)

1. Create `content/<name>.md` with front matter containing only `title` and `summary`.
2. Add `("<name>", "Label")` to `NAV_PAGES` in `build.py` so it appears in the header.
3. Build, verify, commit. No template change is needed.

### 7.3 "Add a new category" (e.g. Error Handling)

1. Add `"Name": "one-line blurb"` to the `CATEGORIES` dictionary in `build.py` (dictionary order is the display order).
2. Add the name to the table in §5.2 of this file.
3. Create at least one sheet in it (empty categories are not displayed).

### 7.4 "Change the look"

Edit design tokens in `assets/style.css` first. Edit `templates/*.html` only if the *structure* must change.
Rebuild and check light mode, dark mode and a narrow window.

### 7.5 "Fix a mistake in an existing sheet"

Edit the Markdown, update the `updated` date, run `check_examples.py` and `build.py`, commit.
Never edit `docs/*.html` directly — your change would be overwritten by the next build.

### 7.6 "Change a rule" (e.g. require a new section)

Change `build.py` **and** this file in the same commit, then fix every existing sheet so the build passes.
A rule that is documented but not enforced (or the reverse) is a bug.

---

## 8. Hard rules (never do these)

1. Never edit files in `docs/` by hand.
2. Never add dependencies, build tools, frameworks, CDNs, analytics, or JavaScript without being asked.
3. Never publish an example you have not run. Never delete or weaken `check_examples.py` to make an example pass — fix the example.
4. Never rename or delete a published slug without also fixing every link to it (run `python3 build.py --check`).
5. Never put raw HTML in Markdown files.
6. Never skip a required section or front-matter field to "save time".
7. Never loosen a validation rule in `build.py` just to make a build pass — fix the content instead.
8. Never commit secrets, personal data, or files outside the structure in §3.
9. Never claim a task is done without a successful `python3 scripts/check_examples.py` **and** `python3 build.py`.

If a request conflicts with these rules, **stop and ask the owner** before proceeding.

---

## 9. Definition of done (check every item)

- [ ] `python3 scripts/check_examples.py` reports all examples ran successfully.
- [ ] `python3 build.py` finishes with `Build OK` and no warnings.
- [ ] New or edited file follows §5 (front matter, 4 sections in order, code and style rules).
- [ ] Any output described in prose was copied from a real run, not guessed.
- [ ] The sheet appears on the homepage in the right category and is reachable through prev/next links.
- [ ] No file inside `docs/` was edited manually; `docs/` was regenerated.
- [ ] Layout checked at narrow width; no horizontal scrolling.
- [ ] `git status` shows only intended files.

---

## 10. Git and deployment

- Branch: `main`. Small, focused commits.
- Commit message format: `type: short description`
  with `type` ∈ `content` (new/edited sheet), `design` (CSS/templates), `build` (build.py/scripts), `docs` (this file/README).
  Examples: `content: add sets sheet`, `design: increase body line height`.
- Always commit regenerated `docs/` together with the source change that caused it.
- Deployment: GitHub repository → **Settings → Pages → Build and deployment → Source: "Deploy from a branch" →
  Branch `main`, folder `/docs`**. Pushing to `main` updates the live site within a minute or two.

---

## 11. Quick reference for the AI

If you only remember five things:

1. Content goes in `content/`, never in `docs/`.
2. One sheet = one kebab-case Markdown file with complete front matter and four fixed sections.
3. Use `scripts/new_sheet.py`, then `check_examples.py`, then `build.py`.
4. Every example must run on its own and print something; describe only output you have seen.
5. Standard library only, no JavaScript, tokens in `style.css`. When rules and a request disagree, ask the owner.
