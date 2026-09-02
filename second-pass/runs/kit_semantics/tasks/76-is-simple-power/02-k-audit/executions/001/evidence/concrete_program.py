def is_simple_power(x, n):
    if x == 1:
        return True
    if n == 0:
        return x == 0
    if n == 1:
        return False
    if n == -1:
        return x == -1
    if x == 0:
        return False
    while x % n == 0:
        x = x // n
    return x == 1


# Documented examples.
assert is_simple_power(1, 4)
assert is_simple_power(2, 2)
assert is_simple_power(8, 2)
assert not is_simple_power(3, 2)
assert not is_simple_power(3, 1)
assert not is_simple_power(5, 3)

# Branch, loop, sign, and magnitude boundaries.
assert is_simple_power(0, 0)
assert not is_simple_power(0, 2)
assert is_simple_power(-1, -1)
assert is_simple_power(-8, -2)
assert is_simple_power(16, -2)
assert not is_simple_power(8, -2)
assert not is_simple_power(-8, 2)
assert is_simple_power(1048576, 2)
assert not is_simple_power(1048575, 2)
