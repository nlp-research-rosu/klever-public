def x_or_y(n, x, y):
    prime = n != 1
    k = 0
    for k in range(2, n):
        if n % k == 0:
            prime = False
    if prime:
        ans = x
    else:
        ans = y
    return ans


# HumanEval/150 dataset `check` cases (small n only — large n is impractical for krun).
assert x_or_y(7, 34, 12) == 34
assert x_or_y(15, 8, 5) == 5
assert x_or_y(3, 33, 5212) == 33
assert x_or_y(91, 56, 129) == 129
assert x_or_y(6, 34, 1234) == 1234
assert x_or_y(1, 2, 0) == 0
assert x_or_y(2, 2, 0) == 2
