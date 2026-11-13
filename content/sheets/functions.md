---
title: Functions
summary: Name a block of code so you can reuse it with different inputs.
category: Functions and Files
order: 1
difficulty: Beginner
updated: 2026-11-13
---

## What it is

A **function** is a named block of code. It takes **parameters** (inputs), does some work and can **return** a result. Functions stop you from copying and pasting the same code.

## Syntax

```python
def name(parameter, other="default"):
    """One-line description."""
    ...
    return result

name(value)                 # call it
name(value, other="x")      # use a keyword argument
```

## Example

```python
def area(width, height=1):
    """Return the area of a rectangle."""
    return width * height

def describe(name, age):
    return f"{name} is {age} years old"

print(area(3, 4))
print(area(5))
print(area(height=2, width=6))
print(describe("Mina", 17))

result = area(2, 2)
print(result + 1)
```

The calls print `12`, `5`, `12` and `Mina is 17 years old`, and the last line prints `5`.

## Common mistakes

- **Forgetting `return`.** Without it the function gives back `None`, so `print(f())` shows `None`.
- **Calling without parentheses.** `area` is the function itself; `area(3, 4)` runs it.
- **Using a list as a default value.** `def f(x=[])` shares one list between all calls. Use `x=None` and create the list inside.
- **Expecting changes to variables outside.** Variables created inside a function exist only inside it.

## Related sheets

- [Conditionals](conditionals.md)
- [Reading Files](reading-files.md)
