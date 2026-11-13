---
title: Loops
summary: Repeat code for every item in a collection or while a condition holds.
category: Control Flow
order: 2
difficulty: Beginner
updated: 2026-11-13
---

## What it is

A `for` loop goes through the items of a collection one by one. A `while` loop repeats as long as its condition stays true. `range(n)` produces the numbers `0` to `n - 1`.

## Syntax

```python
for item in collection:
    ...

for i in range(5):            # 0, 1, 2, 3, 4
    ...

while condition:
    ...

break       # leave the loop now
continue    # skip to the next round
```

## Example

```python
total = 0
for n in range(1, 6):
    total += n
print("sum 1..5 =", total)

fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)

countdown = 3
while countdown > 0:
    print(countdown)
    countdown -= 1
print("go!")

for n in range(10):
    if n % 2 == 0:
        continue
    if n > 7:
        break
    print("odd:", n)
```

The first loop prints `sum 1..5 = 15`, and the last loop prints the odd numbers `1`, `3`, `5` and `7` before `break` stops it.

## Common mistakes

- **Infinite `while` loops.** Make sure something inside the loop eventually makes the condition false.
- **Forgetting that `range` stops early.** `range(5)` ends at `4`; use `range(1, 6)` for `1` to `5`.
- **Looping with `range(len(x))`.** Looping directly (`for item in x`) is simpler, and `enumerate` gives you the index too.
- **Changing a list while looping over it.** Build a new list instead.

## Related sheets

- [Lists](lists.md)
- [Conditionals](conditionals.md)
