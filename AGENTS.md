# AGENTS.md

This repository's complete rules for AI agents live in **[CLAUDE.md](CLAUDE.md)**.

Read `CLAUDE.md` in full before making any change. In short:

- Edit content in `content/`, never the generated `docs/` folder.
- Add a sheet with `python3 scripts/new_sheet.py ...`, then run `python3 scripts/check_examples.py` and `python3 build.py`.
- Every code example must run on its own; standard library only; no JavaScript; follow the front-matter and section rules in `CLAUDE.md` §5.
