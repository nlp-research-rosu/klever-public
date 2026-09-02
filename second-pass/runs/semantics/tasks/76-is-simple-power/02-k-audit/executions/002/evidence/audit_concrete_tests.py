def is_simple_power(x, n):
    if x == 1:
        return True
    if x < 1:
        return False
    if n <= 1:
        return False
    while x % n == 0:
        x = x // n
    return x == 1


# Prompt examples.
assert is_simple_power(1, 4)
assert is_simple_power(2, 2)
assert is_simple_power(8, 2)
assert not is_simple_power(3, 2)
assert not is_simple_power(3, 1)
assert not is_simple_power(5, 3)

# Every branch boundary and both loop exits.
assert not is_simple_power(-1, 2)
assert not is_simple_power(0, 2)
assert is_simple_power(1, -1)
assert not is_simple_power(2, -1)
assert not is_simple_power(2, 0)
assert not is_simple_power(2, 1)
assert is_simple_power(16, 2)
assert is_simple_power(16, 4)
assert not is_simple_power(24, 2)
assert not is_simple_power(128, 4)
