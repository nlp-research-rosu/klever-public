def sum_to_n(n):
    return sum(range(n + 1))


# Smoke checks from the prompt docstring (NOT hidden tests).
assert sum_to_n(30) == 465
assert sum_to_n(100) == 5050
assert sum_to_n(5) == 15
assert sum_to_n(10) == 55
assert sum_to_n(1) == 1
