def modp(n: int, p: int):
    return (2 ** n) % p


assert modp(0, 1) == 0
assert modp(1, 1) == 0
assert modp(0, 2) == 1
assert modp(1, 2) == 0
assert modp(2, 3) == 1
assert modp(32, 7) == 4
