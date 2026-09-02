def starts_one_ends(n):
    return 1 if n == 1 else 18 * 10 ** (n - 2)


assert starts_one_ends(1) == 1
assert starts_one_ends(2) == 18
assert starts_one_ends(3) == 180
assert starts_one_ends(6) == 180000
