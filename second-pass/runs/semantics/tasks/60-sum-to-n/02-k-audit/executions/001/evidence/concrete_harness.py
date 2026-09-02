def sum_to_n(n: int):
    return n * (n + 1) // 2


# Formal-domain boundary and representative satisfying inputs.
assert sum_to_n(0) == 0
assert sum_to_n(1) == 1
assert sum_to_n(2) == 3
assert sum_to_n(30) == 465
assert sum_to_n(100) == 5050

# Outside the formal precondition: confirms that the K execution follows the
# submitted body here too (this value intentionally differs from canonical.py).
assert sum_to_n(-2) == 1
