---
title: Variables and Types
summary: Store values under names and know which type each value has.
category: Basics
order: 1
difficulty: Beginner
updated: 2026-11-13
---

## What it is

A **variable** is a name that points to a value. Every value has a **type**, such as whole number (`int`), decimal number (`float`), text (`str`) or true/false (`bool`). Python works out the type for you.

## Syntax

```python
name = value          # create or change a variable
type(name)            # ask for its type
int("42")             # convert text to a whole number
float("3.5")          # convert text to a decimal number
str(42)               # convert a number to text
```

## Example

```python
age = 17
height = 1.68
name = "Mina"
is_student = True

print(name, age, height, is_student)
print(type(age), type(height), type(name), type(is_student))

age = age + 1
print(f"{name} will be {age} next year")

total = int("40") + 2
print(total)
```

The first `print` shows the four values, the second shows their types, and the last two show `Mina will be 18 next year` and `42`.

## Common mistakes

- **Mixing text and numbers.** `"age: " + 17` raises a `TypeError`. Use `str(17)` or an f-string instead.
- **Using `=` to compare.** `=` stores a value; `==` compares two values.
- **Bad names.** Names cannot start with a digit or contain spaces. Use `snake_case` such as `total_price`.
- **Forgetting to convert input.** `input()` always returns text, so wrap it with `int()` or `float()` before doing math.

## Related sheets

- [Strings](strings.md)
