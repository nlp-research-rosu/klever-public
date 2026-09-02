# List comprehensions: [ELT for T in ITER (if COND ...) (for T2 in ITER2 ...)]

# basic map / filter over a list (incl. empty)
assert [e for e in [1, 2, 3]] == [1, 2, 3]
assert [e + 1 for e in [1, 2, 3]] == [2, 3, 4]
assert [e for e in [1, -2, 3, -4] if e > 0] == [1, 3]
assert [e for e in []] == []

# over the other iterables: str / range / tuple
assert [c for c in "abc"] == ["a", "b", "c"]
assert [i for i in range(5)] == [0, 1, 2, 3, 4]
assert [i * i for i in range(4)] == [0, 1, 4, 9]
assert [x for x in (1, 2, 3, 4) if x > 2] == [3, 4]

# multiple filters (if ... if ...) behave as AND
assert [x for x in [5, -1, 12, 3] if x > 0 if x < 10] == [5, 3]

# nested for (one shared scope; row-major order); a later iterable can see an earlier target
assert [i * 10 + j for i in range(3) for j in range(2)] == [0, 1, 10, 11, 20, 21]
assert [a + b for a in [1, 2] for b in [10, 20] if a + b > 11] == [21, 12, 22]
assert [j for row in [[1, 2], [3, 4]] for j in row] == [1, 2, 3, 4]

# Python-3 comprehension scope: the target does not leak or clobber an enclosing var
a = 5
r = [a for a in [1, 2, 3]]
assert a == 5 and r == [1, 2, 3]
base = 10
assert [e + base for e in [1, 2]] == [11, 12]                 # free var resolves to enclosing
xs = [7, 8, 9]
assert [xs for xs in xs] == [7, 8, 9] and xs == [7, 8, 9]     # target shadows iterable, no clobber

# comprehension inside a comprehension (the reserved accumulator must not clash)
assert [y for y in [x for x in [1, 2, 3]]] == [1, 2, 3]
assert [y * 10 for y in [x + 1 for x in [1, 2, 3]]] == [20, 30, 40]
assert [[y for y in row] for row in [[1, 2], [3, 4]]] == [[1, 2], [3, 4]]
assert [x for x in [x for x in [1, 2, 3]]] == [1, 2, 3]
