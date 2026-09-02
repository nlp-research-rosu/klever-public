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


assert is_simple_power(1, 4)
assert is_simple_power(2, 2)
assert is_simple_power(8, 2)
assert not is_simple_power(3, 2)
assert not is_simple_power(3, 1)
assert not is_simple_power(5, 3)
