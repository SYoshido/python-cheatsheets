#!/usr/bin/env python3
"""Run every ```python block found under '## Example' in content/sheets/*.md.

    python3 scripts/check_examples.py

Each block runs on its own in a fresh Python process inside a temporary folder,
so examples must be self-contained. Exit status is 1 if any example fails.
Blocks outside the '## Example' section (e.g. under '## Syntax') are not run.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHEETS = ROOT / "content" / "sheets"


def example_blocks(text: str) -> list[str]:
    m = re.search(r"^## Example\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return []
    return re.findall(r"^```python\n(.*?)^```", m.group(1), re.S | re.M)


def main() -> int:
    failures = 0
    total = 0
    for path in sorted(SHEETS.glob("*.md")):
        if path.name.startswith("_"):
            continue
        for n, code in enumerate(example_blocks(path.read_text(encoding="utf-8")), start=1):
            total += 1
            with tempfile.TemporaryDirectory() as tmp:
                run = subprocess.run(
                    [sys.executable, "-I", "-c", code], cwd=tmp, capture_output=True, text=True, timeout=20
                )
            if run.returncode != 0:
                failures += 1
                print(f"FAIL {path.name} (example block {n})\n{run.stderr.strip()}\n", file=sys.stderr)
            else:
                print(f"ok   {path.name} (example block {n})")
    print(f"{total - failures}/{total} examples ran successfully")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
