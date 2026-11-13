---
title: About
summary: Learn why these cheat-sheets exist and how every page is built.
---

## What this is

Python Cheat-Sheets is a small collection of one-page references for people learning Python.
Each sheet has the same four parts: **what it is**, the **syntax**, a **runnable example** and the **common mistakes**.

New to Python? Start with [Variables and Types](sheets/variables-and-types.md), then [Strings](sheets/strings.md).

## Every example is tested

Before the site is built, a script runs every code example on every sheet.
If an example fails, the project is not finished, so you can copy any snippet and trust that it works.

## How the site is built

Every page is a Markdown file in the `content/` folder. A single script, `build.py`, turns those files into the HTML you are reading.
There is no framework, no JavaScript and nothing to install beyond Python.

| Part | Where it lives | Who edits it |
|------|----------------|--------------|
| Sheet text and code | `content/` | You or an AI assistant |
| Layout | `templates/` | Rarely |
| Look and feel | `assets/style.css` | Rarely |
| Finished website | `docs/` | Nobody; it is generated |

## Adding a sheet

The project includes a `CLAUDE.md` file that tells AI assistants the purpose, structure, naming rules and writing style of this site.
To add a sheet, an assistant creates one Markdown file, runs the example checker and the build, and verifies the result.
