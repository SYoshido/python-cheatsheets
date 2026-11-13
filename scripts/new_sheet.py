#!/usr/bin/env python3
"""Scaffold a new sheet page from content/_template.md.

    python3 scripts/new_sheet.py "Lists" --category "Data Structures" --difficulty Beginner

Creates content/sheets/<slug>.md with the next free `order` in that category.
Fill in every TODO, then run `python3 build.py`.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (reuses CATEGORIES, DIFFICULTIES, SLUG_RE so rules live in one place)


def next_order(category: str) -> int:
    used = [0]
    for path in build.SHEET_DIR.glob("*.md"):
        if path.name.startswith("_"):
            continue
        try:
            meta, _ = build.split_front_matter(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if meta.get("category") == category and meta.get("order", "").isdigit():
            used.append(int(meta["order"]))
    return max(used) + 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("title", help='Title Case name, e.g. "Few-shot Examples"')
    ap.add_argument("--category", required=True, choices=list(build.CATEGORIES))
    ap.add_argument("--difficulty", default="Beginner", choices=list(build.DIFFICULTIES))
    args = ap.parse_args()

    slug = re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-")
    if not build.SLUG_RE.match(slug):
        print(f"Cannot make a valid slug from {args.title!r}", file=sys.stderr)
        return 1
    target = build.SHEET_DIR / f"{slug}.md"
    if target.exists():
        print(f"{target.relative_to(ROOT)} already exists; choose another title.", file=sys.stderr)
        return 1

    text = (build.CONTENT / "_template.md").read_text(encoding="utf-8")
    text = (
        text.replace("__TITLE__", args.title)
        .replace("__CATEGORY__", args.category)
        .replace("__ORDER__", str(next_order(args.category)))
        .replace("__DIFFICULTY__", args.difficulty)
        .replace("__DATE__", date.today().isoformat())
    )
    target.write_text(text, encoding="utf-8")
    print(f"Created {target.relative_to(ROOT)}")
    print("Next: fill in every TODO, then run `python3 build.py`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
