#!/usr/bin/env python3
"""Python Cheat-Sheets - static site builder (Python standard library only).

    content/*.md + content/sheets/*.md  ->  docs/*.html

Usage:
    python3 build.py            validate content and build the site into docs/
    python3 build.py --check    validate content only, write nothing

The rules enforced here are documented in CLAUDE.md. Do not loosen a rule to make
a build pass; fix the content instead.
"""
from __future__ import annotations

import html
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
SHEET_DIR = CONTENT / "sheets"
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "assets"
OUT = ROOT / "docs"

# ---- Site configuration (see CLAUDE.md sections 5 and 7) --------------------
SITE_NAME = "Python Cheat-Sheets"

# Display order of categories. Value = one-line blurb shown on the homepage.
CATEGORIES = {
    "Basics": "The building blocks: values, names and text.",
    "Data Structures": "Containers for holding many values at once.",
    "Control Flow": "Make decisions and repeat work.",
    "Functions and Files": "Package code for reuse and work with files.",
}
DIFFICULTIES = ("Beginner", "Intermediate")
REQUIRED_SECTIONS = ["What it is", "Syntax", "Example", "Common mistakes"]
# Standalone pages shown in the header: (file name without .md, nav label)
NAV_PAGES = [("about", "About")]

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LIST_RE = re.compile(r"^([-*]|\d+\.)\s+(.*)$")
NESTED_RE = re.compile(r"^\s{2,}([-*]|\d+\.)\s")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")

errors: list[str] = []


def err(src: Path | str, msg: str) -> None:
    try:
        name = str(Path(src).relative_to(ROOT))
    except ValueError:
        name = str(src)
    errors.append(f"{name}: {msg}")


# ---- Front matter -----------------------------------------------------------
def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    text = text.replace("\r\n", "\n")
    m = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", text, re.S)
    if not m:
        raise ValueError("missing front matter block (--- ... ---) at the top of the file")
    meta: dict[str, str] = {}
    for n, raw in enumerate(m.group(1).split("\n"), start=2):
        if not raw.strip():
            continue
        if ":" not in raw:
            raise ValueError(f"front matter line {n} is not 'key: value': {raw!r}")
        key, _, value = raw.partition(":")
        meta[key.strip()] = value.strip()
    return meta, m.group(2)


# ---- Markdown (small, strict subset) ---------------------------------------
def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def inline(s: str, src: Path) -> str:
    codes: list[str] = []

    def stash(m: re.Match) -> str:
        codes.append("<code>%s</code>" % html.escape(m.group(1), quote=False))
        return "\x00%d\x00" % (len(codes) - 1)

    s = re.sub(r"`([^`]+)`", stash, s)
    if "![" in s:
        err(src, "images are not supported (see CLAUDE.md 5.4)")
    s = html.escape(s, quote=False)

    def link(m: re.Match) -> str:
        text, href = m.group(1), m.group(2)
        extra = ""
        path, sep, frag = href.partition("#")
        if re.match(r"^https?://", href):
            extra = ' rel="noopener"'
        elif path.endswith(".md"):
            if not (src.parent / path).resolve().is_file():
                err(src, f"broken link: {href}")
            href = path[:-3] + ".html" + sep + frag
        href = href.replace('"', "%22")
        return f'<a href="{href}"{extra}>{text}</a>'

    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])", r"<em>\1</em>", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], s)


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render_markdown(text: str, src: Path) -> tuple[str, list[tuple[str, str]], list[str]]:
    """Return (html, [(h2 id, h2 text)], [h2 raw titles])."""
    lines = text.split("\n")
    out: list[str] = []
    toc: list[tuple[str, str]] = []
    h2_titles: list[str] = []
    para: list[str] = []
    i = 0

    def flush() -> None:
        if para:
            out.append("<p>%s</p>" % inline(" ".join(p.strip() for p in para), src))
            para.clear()

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            flush()
            lang = line[3:].strip()
            buf: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            if i >= len(lines):
                err(src, "unclosed code fence")
            i += 1
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(buf), quote=False)}</code></pre>")
            continue

        if not line.strip():
            flush()
            i += 1
            continue

        h = HEADING_RE.match(line)
        if h:
            flush()
            level, title = len(h.group(1)), h.group(2)
            if level == 1:
                err(src, "do not write a '# H1' in the body; the title comes from front matter")
            elif level >= 4:
                err(src, f"heading too deep ('{line}'); use ## or ###")
            else:
                hid = slugify(title)
                if level == 2:
                    toc.append((hid, title))
                    h2_titles.append(title)
                out.append(f'<h{level} id="{hid}">{inline(title, src)}</h{level}>')
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,})\s*$", line):
            flush()
            out.append("<hr>")
            i += 1
            continue

        if line.startswith(">"):
            flush()
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            paras = [p.strip() for p in "\n".join(buf).split("\n\n") if p.strip()]
            cls = ""
            if paras and paras[0].startswith("**Tip:**"):
                cls = ' class="callout tip"'
            elif paras and paras[0].startswith("**Warning:**"):
                cls = ' class="callout warn"'
            body = "".join("<p>%s</p>" % inline(" ".join(p.split("\n")), src) for p in paras)
            out.append(f"<blockquote{cls}>{body}</blockquote>")
            continue

        m = LIST_RE.match(line)
        if m:
            flush()
            ordered = m.group(1)[0].isdigit()
            items: list[str] = []
            while i < len(lines):
                cur = lines[i]
                lm = LIST_RE.match(cur)
                if lm and lm.group(1)[0].isdigit() == ordered:
                    items.append(lm.group(2))
                    i += 1
                elif NESTED_RE.match(cur):
                    err(src, f"nested lists are not supported: '{cur.strip()}'")
                    i += 1
                elif cur.startswith("  ") and cur.strip() and items:
                    items[-1] += " " + cur.strip()
                    i += 1
                else:
                    break
            tag = "ol" if ordered else "ul"
            lis = "".join(f"<li>{inline(it, src)}</li>" for it in items)
            out.append(f"<{tag}>{lis}</{tag}>")
            continue

        if line.lstrip().startswith("|") and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
            flush()
            head = split_row(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            th = "".join(f"<th>{inline(c, src)}</th>" for c in head)
            trs = "".join(
                "<tr>" + "".join(f"<td>{inline(c, src)}</td>" for c in r) + "</tr>" for r in rows
            )
            out.append(
                f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'
            )
            continue

        if line.lstrip().startswith("<"):
            err(src, f"raw HTML is not allowed in Markdown: '{line.strip()[:40]}'")
        para.append(line)
        i += 1

    flush()
    return "\n".join(out), toc, h2_titles


# ---- Loading and validating content ----------------------------------------
def read_source(path: Path) -> tuple[dict[str, str], str] | None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"\bTODO\b", text):
        err(path, "contains a TODO marker; finish the content first")
    try:
        return split_front_matter(text)
    except ValueError as e:
        err(path, str(e))
        return None


def check_common(path: Path, meta: dict[str, str], fields: list[str]) -> None:
    for f in fields:
        if not meta.get(f):
            err(path, f"front matter is missing required field '{f}'")
    summary = meta.get("summary", "")
    if len(summary) > 110:
        err(path, f"summary is {len(summary)} characters; the limit is 110")
    if summary and not summary.endswith("."):
        err(path, "summary must end with a period")


def load_sheets() -> list[dict]:
    sheets: list[dict] = []
    titles: dict[str, Path] = {}
    orders: dict[tuple[str, int], Path] = {}
    for path in sorted(SHEET_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        slug = path.stem
        if not SLUG_RE.match(slug):
            err(path, f"file name '{slug}' is not kebab-case (lowercase letters, digits, hyphens)")
        parsed = read_source(path)
        if not parsed:
            continue
        meta, body = parsed
        check_common(path, meta, ["title", "summary", "category", "order", "difficulty", "updated"])
        cat = meta.get("category", "")
        if cat and cat not in CATEGORIES:
            err(path, f"category '{cat}' must be one of: {', '.join(CATEGORIES)}")
        if meta.get("difficulty") and meta["difficulty"] not in DIFFICULTIES:
            err(path, f"difficulty must be one of: {', '.join(DIFFICULTIES)}")
        order = 0
        try:
            order = int(meta.get("order", ""))
            if order < 1:
                raise ValueError
        except ValueError:
            err(path, "order must be an integer >= 1")
        try:
            date.fromisoformat(meta.get("updated", ""))
        except ValueError:
            err(path, "updated must be an ISO date like 2026-11-12")
        title = meta.get("title", "")
        if title in titles:
            err(path, f"duplicate title (also used by {titles[title].name})")
        titles[title] = path
        if (cat, order) in orders:
            err(path, f"order {order} is already used in category {cat} by {orders[(cat, order)].name}")
        orders[(cat, order)] = path

        body_html, toc, h2s = render_markdown(body, path)
        if h2s[: len(REQUIRED_SECTIONS)] != REQUIRED_SECTIONS:
            err(path, "the first four '##' sections must be exactly, in order: " + ", ".join(REQUIRED_SECTIONS))
        sheets.append({"slug": slug, "meta": meta, "order": order, "html": body_html, "toc": toc})

    cat_index = {c: n for n, c in enumerate(CATEGORIES)}
    sheets.sort(key=lambda p: (cat_index.get(p["meta"].get("category", ""), 99), p["order"]))
    return sheets


def load_pages() -> list[dict]:
    pages: list[dict] = []
    for path in sorted(CONTENT.glob("*.md")):
        if path.name.startswith("_"):
            continue
        if not SLUG_RE.match(path.stem):
            err(path, "file name is not kebab-case")
        parsed = read_source(path)
        if not parsed:
            continue
        meta, body = parsed
        check_common(path, meta, ["title", "summary"])
        body_html, _, _ = render_markdown(body, path)
        pages.append({"slug": path.stem, "meta": meta, "html": body_html})
    for name, _label in NAV_PAGES:
        if not (CONTENT / f"{name}.md").is_file():
            err(ROOT / "build.py", f"NAV_PAGES lists '{name}' but content/{name}.md does not exist")
    return pages


# ---- Templates and output ---------------------------------------------------
def fill(template_name: str, values: dict[str, str]) -> str:
    """Single-pass {{key}} substitution; inserted values are never re-scanned."""
    tpl = (TEMPLATES / template_name).read_text(encoding="utf-8")

    def sub(m: re.Match) -> str:
        key = m.group(1)
        if key not in values:
            err(TEMPLATES / template_name, f"unknown placeholder {{{{{key}}}}}")
            return ""
        return values[key]

    return re.sub(r"\{\{(\w+)\}\}", sub, tpl)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def nav_html(root: str, current: str) -> str:
    items = [("home", "Home", f"{root}index.html"), ("sheets", "Sheets", f"{root}index.html#sheets")]
    items += [(name, label, f"{root}{name}.html") for name, label in NAV_PAGES]
    parts = []
    for key, label, href in items:
        cur = ' aria-current="page"' if key == current else ""
        parts.append(f'<a href="{href}"{cur}>{label}</a>')
    return "\n".join(parts)


def wrap(root: str, current: str, title: str, description: str, body: str) -> str:
    page_title = SITE_NAME if current == "home" else f"{title} | {SITE_NAME}"
    return fill(
        "base.html",
        {
            "root": root,
            "page_title": esc(page_title),
            "description": esc(description),
            "nav": nav_html(root, current),
            "content": body,
            "site_name": esc(SITE_NAME),
        },
    )


def build_home(sheets: list[dict]) -> str:
    groups = []
    for cat, blurb in CATEGORIES.items():
        mine = [p for p in sheets if p["meta"].get("category") == cat]
        if not mine:
            continue
        cards = "\n".join(
            f'<li class="card"><a href="sheets/{p["slug"]}.html">'
            f'<span class="tag">{esc(p["meta"]["difficulty"])}</span>'
            f'<h3>{esc(p["meta"]["title"])}</h3>'
            f'<p>{esc(p["meta"]["summary"])}</p></a></li>'
            for p in mine
        )
        groups.append(
            f'<section class="category"><h2>{esc(cat)}</h2>'
            f'<p class="cat-blurb">{esc(blurb)}</p><ul class="cards">{cards}</ul></section>'
        )
    body = fill("home.html", {"count": str(len(sheets)), "groups": "\n".join(groups)})
    return wrap("", "home", SITE_NAME, "Short, runnable Python cheat-sheets for beginners.", body)


def build_sheet(p: dict, prev: dict | None, nxt: dict | None) -> str:
    m = p["meta"]
    toc = "".join(f'<li><a href="#{hid}">{esc(t)}</a></li>' for hid, t in p["toc"])
    prev_html = (
        f'<a class="prev" href="{prev["slug"]}.html"><span>&larr; Previous</span>{esc(prev["meta"]["title"])}</a>'
        if prev
        else "<span></span>"
    )
    next_html = (
        f'<a class="next" href="{nxt["slug"]}.html"><span>Next &rarr;</span>{esc(nxt["meta"]["title"])}</a>'
        if nxt
        else "<span></span>"
    )
    body = fill(
        "sheet.html",
        {
            "category": esc(m["category"]),
            "title": esc(m["title"]),
            "summary": esc(m["summary"]),
            "difficulty": esc(m["difficulty"]),
            "updated": esc(m["updated"]),
            "toc": toc,
            "body": p["html"],
            "prev": prev_html,
            "next": next_html,
        },
    )
    return wrap("../", "sheets", m["title"], m["summary"], body)


def build_page(pg: dict) -> str:
    m = pg["meta"]
    body = fill("page.html", {"title": esc(m["title"]), "summary": esc(m["summary"]), "body": pg["html"]})
    return wrap("", pg["slug"], m["title"], m["summary"], body)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    sheets = load_sheets()
    pages = load_pages()
    if not sheets:
        err(SHEET_DIR, "no sheet files found")

    outputs: dict[Path, str] = {}
    if not errors:
        outputs[OUT / "index.html"] = build_home(sheets)
        for n, p in enumerate(sheets):
            prev = sheets[n - 1] if n > 0 else None
            nxt = sheets[n + 1] if n < len(sheets) - 1 else None
            outputs[OUT / "sheets" / f"{p['slug']}.html"] = build_sheet(p, prev, nxt)
        for pg in pages:
            outputs[OUT / f"{pg['slug']}.html"] = build_page(pg)

    if errors:
        print(f"Build FAILED with {len(errors)} problem(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if check_only:
        print(f"Check OK: {len(sheets)} sheets, {len(pages)} pages")
        return 0

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for path, text in outputs.items():
        write(path, text)
    shutil.copytree(ASSETS, OUT / "assets")
    write(OUT / ".nojekyll", "")
    print(f"Build OK: {len(sheets)} sheets, {len(pages)} pages -> {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
