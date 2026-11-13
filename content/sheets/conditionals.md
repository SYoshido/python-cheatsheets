---
title: Conditionals
summary: Run different code depending on whether a condition is true.
category: Control Flow
order: 1
difficulty: Beginner
updated: 2026-11-13
---

## What it is

An `if` statement runs a block of code only when a condition is true. Add `elif` for more conditions and `else` for everything else. The block is marked by **indentation**, usually four spaces.

## Syntax

```python
if condition:
    ...
elif other_condition:
    ...
else:
    ...

# comparison: ==  !=  <  >  <=  >=
# combine:    and  or  not
```

## Example

```python
def grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"

for s in [95, 83, 61, 40]:
    print(s, grade(s))

age = 20
has_ticket = True
if age >= 18 and has_ticket:
    print("Welcome in")
```

The loop prints the grades `A`, `B`, `C`, `F` for the four scores, and the last block prints `Welcome in`.

## Common mistakes

- **Missing colon.** Every `if`, `elif` and `else` line ends with `:`.
- **Inconsistent indentation.** Mixing tabs and spaces raises an `IndentationError`.
- **Wrong order of conditions.** Python takes the first true branch, so test the strictest condition (`>= 90`) first.
- **Writing `if x = 5`.** Use `==` to compare.

## Related sheets

- [Loops](loops.md)
- [Functions](functions.md)
