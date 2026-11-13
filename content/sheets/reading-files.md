---
title: Reading Files
summary: Open a text file, read its lines and close it safely with a with-block.
category: Functions and Files
order: 2
difficulty: Intermediate
updated: 2026-11-13
---

## What it is

To read a file, open it, read the text and close it. The `with` statement closes the file for you, even if an error happens. Always pass `encoding="utf-8"` so text in any language reads correctly.

## Syntax

```python
with open("notes.txt", encoding="utf-8") as f:
    text = f.read()          # the whole file as one string

with open("notes.txt", encoding="utf-8") as f:
    for line in f:           # one line at a time
        ...

with open("out.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")       # "w" replaces the file; "a" appends
```

## Example

```python
with open("fruits.txt", "w", encoding="utf-8") as f:
    f.write("apple\nbanana\ncherry\n")

with open("fruits.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f]

print(lines)
print(len(lines), "lines")

try:
    open("missing.txt", encoding="utf-8")
except FileNotFoundError:
    print("missing.txt does not exist")
```

The example first creates `fruits.txt`, so it runs anywhere. It prints `['apple', 'banana', 'cherry']`, `3 lines` and the not-found message.

## Common mistakes

- **Wrong path.** A relative path like `"notes.txt"` is looked up from where you run the program, not where the script is saved.
- **Forgetting `strip()`.** Each line keeps its newline character `\n` at the end.
- **Opening with `"w"` by accident.** It erases the existing file. Use `"a"` to add to the end.
- **Not closing the file.** Use a `with` block so Python closes it for you.

## Related sheets

- [Functions](functions.md)
- [Strings](strings.md)
