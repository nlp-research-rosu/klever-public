def make_a_pile(n):
    return [n + 2 * i for i in range(n)]


# Smoke checks from the prompt docstring (NOT hidden tests).
assert make_a_pile(3) == [3, 5, 7]
