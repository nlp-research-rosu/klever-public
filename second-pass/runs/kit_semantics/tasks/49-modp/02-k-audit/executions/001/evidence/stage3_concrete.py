def modp(n: int, p: int):
    return 2 ** n % p


assert modp(3, 5) == 3
assert modp(1101, 101) == 2
assert modp(0, 101) == 1
assert modp(0, 1) == 0
assert modp(0, -5) == -4
assert modp(1, -5) == -3
assert modp(100, 101) == 1
