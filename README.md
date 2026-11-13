# Python Cheat-Sheets

A small static website of one-page Python cheat-sheets for beginners.
Every page is a Markdown file; `build.py` turns them into HTML in `docs/`, which GitHub Pages serves.
Every code example on the site is executed by `scripts/check_examples.py`, so none of them is broken.

## Quick start

```bash
python3 scripts/new_sheet.py "Sets" --category "Data Structures" --difficulty Beginner
# edit content/sheets/sets.md
python3 scripts/check_examples.py   # run every example
python3 build.py
python3 -m http.server 8000 --directory docs   # open http://localhost:8000
```

Needs only Python 3.9+.

## For AI assistants

Read [`CLAUDE.md`](CLAUDE.md) first. It defines the purpose, structure, content format, design rules and workflows.

## Publishing

Settings → Pages → Deploy from a branch → `main` / `/docs`.
