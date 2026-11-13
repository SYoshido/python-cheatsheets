---
title: Lists
summary: Keep an ordered, changeable collection of values in one variable.
category: Data Structures
order: 1
difficulty: Beginner
updated: 2026-11-13
---

## What it is

A **list** holds several values in order. You can add, remove and change items, and items can be of different types. Positions are numbered from `0`.

## Syntax

```python
items = [10, 20, 30]
items[0]               # first item
items.append(40)       # add to the end
items.remove(20)       # remove the first matching value
items.pop()            # remove and return the last item
len(items)             # how many items
sorted(items)          # new sorted list
[x * 2 for x in items] # list comprehension
```

## Example

```python
scores = [72, 95, 88]
scores.append(60)
scores[0] = 75

print(scores)
print(len(scores), max(scores), min(scores))
print(sorted(scores))
print(sorted(scores, reverse=True)[:2])

doubled = [s * 2 for s in scores]
passed = [s for s in scores if s >= 70]
print(doubled)
print(passed)
```

The last line prints `[75, 95, 88]` because the `if` part of the comprehension drops the score `60`.

## Common mistakes

- **Index out of range.** A list with 3 items has indexes `0`, `1`, `2`; asking for `items[3]` raises an `IndexError`.
- **Expecting `append` to return a list.** `append` changes the list and returns `None`, so `x = items.append(5)` makes `x` empty.
- **Copying with `=`.** `b = a` makes two names for one list. Use `b = a.copy()` for a real copy.
- **Changing a list while looping over it.** Loop over a copy or build a new list instead.

## Related sheets

- [Dictionaries](dictionaries.md)
- [Loops](loops.md)
