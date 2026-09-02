def modp(n: int, p: int):
    """Return 2^n modulo p."""
    return (2 ** n) % p


assert modp(0, 1) == 0
assert modp(0, 101) == 1
assert modp(1, 1) == 0
assert modp(3, 5) == 3
assert modp(1101, 101) == 2
