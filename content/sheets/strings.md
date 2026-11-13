---
title: Strings
summary: Work with text using indexing, slicing, methods and f-strings.
category: Basics
order: 2
difficulty: Beginner
updated: 2026-11-13
---

## What it is

A **string** is a piece of text in quotes. Strings are **immutable**: methods such as `upper()` return a new string and never change the original.

## Syntax

```python
s = "hello"
s[0]               # first character
s[-1]              # last character
s[1:4]             # slice: characters 1 up to (not including) 4
len(s)             # number of characters
s.upper()          # also lower(), strip(), title()
s.replace("l", "L")
s.split(",")       # text to list
",".join(items)    # list to text
f"Hi {name}"       # f-string: put values inside text
```

## Example

```python
word = "  Python is fun  "
clean = word.strip()

print(clean)
print(clean.upper())
print(clean[0], clean[-1], clean[0:6])
print(len(clean))
print(clean.replace("fun", "great"))

parts = "red,green,blue".split(",")
print(parts)
print(" and ".join(parts))

price = 4.5
print(f"Total: {price * 2:.2f} dollars")
```

The slice `clean[0:6]` gives `Python`, and the f-string format `:.2f` rounds to two decimal places, so the last line prints `Total: 9.00 dollars`.

## Common mistakes

- **Expecting a method to change the string.** `s.upper()` on its own does nothing useful; write `s = s.upper()`.
- **Off-by-one slices.** The end index is not included, so `s[0:3]` has three characters.
- **Changing a character directly.** `s[0] = "J"` raises a `TypeError`. Build a new string instead.
- **Forgetting the `f`.** Without it, `"Hi {name}"` prints the braces literally.

## Related sheets

- [Variables and Types](variables-and-types.md)
- [Lists](lists.md)
