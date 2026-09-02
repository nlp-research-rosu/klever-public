def generate_integers(a, b):
    lower = max(2, min(a, b))
    upper = min(8, max(a, b))
    return [i for i in range(lower, upper + 1) if i % 2 == 0]


# Smoke checks from the prompt docstring (NOT hidden tests).
assert generate_integers(2, 8) == [2, 4, 6, 8]
assert generate_integers(8, 2) == [2, 4, 6, 8]
assert generate_integers(10, 14) == []
