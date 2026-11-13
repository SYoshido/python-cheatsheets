---
title: Dictionaries
summary: Look up values by a key, such as a name, instead of by position.
category: Data Structures
order: 2
difficulty: Beginner
updated: 2026-11-13
---

## What it is

A **dictionary** stores pairs of **key: value**. You find a value by asking for its key, which is much clearer than remembering a position number.

## Syntax

```python
d = {"name": "Mina", "age": 17}
d["name"]              # get a value (error if missing)
d.get("city", "n/a")   # get a value with a default
d["city"] = "Taipei"   # add or change a pair
del d["age"]           # remove a pair
"name" in d            # is this key present?
d.keys()  d.values()  d.items()
```

## Example

```python
student = {"name": "Mina", "age": 17}
student["city"] = "Taipei"
student["age"] = 18

print(student)
print(student["name"])
print(student.get("phone", "no phone"))
print("city" in student)

for key, value in student.items():
    print(key, "->", value)

counts = {}
for letter in "banana":
    counts[letter] = counts.get(letter, 0) + 1
print(counts)
```

The loop at the end counts letters and prints `{'b': 1, 'a': 3, 'n': 2}`.

## Common mistakes

- **Asking for a missing key.** `d["phone"]` raises a `KeyError`. Use `d.get("phone")` or check with `in` first.
- **Using a list as a key.** Keys must be unchangeable, such as strings, numbers or tuples.
- **Expecting duplicates.** Each key appears once; assigning to an existing key replaces its value.
- **Confusing `[]` and `{}`.** Square brackets make a list; curly braces make a dictionary.

## Related sheets

- [Lists](lists.md)
- [Loops](loops.md)
