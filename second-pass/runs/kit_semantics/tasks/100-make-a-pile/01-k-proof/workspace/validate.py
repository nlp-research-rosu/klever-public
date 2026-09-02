from solution import make_a_pile


def oracle(n):
    return list(range(n, 3 * n, 2))


checked = 0
for value in range(1, 1001):
    actual = make_a_pile(value)
    expected = oracle(value)
    if actual != expected:
        raise AssertionError(
            f"n={value}: actual={actual!r}, expected={expected!r}"
        )
    checked += 1

print(f"CPython differential validation: {checked} inputs, 0 mismatches")
