from typing import List


def factorize(n: int) -> List[int]:
    factors = []
    divisor = 2
    while n > 1:
        if n % divisor == 0:
            factors.append(divisor)
            n = n // divisor
        else:
            divisor += 1
    return factors


# Independently chosen normal, loop-boundary, branch, multiplicity, and prime cases.
assert factorize(1) == []
assert factorize(2) == [2]
assert factorize(3) == [3]
assert factorize(4) == [2, 2]
assert factorize(8) == [2, 2, 2]
assert factorize(25) == [5, 5]
assert factorize(70) == [2, 5, 7]
assert factorize(97) == [97]
assert factorize(360) == [2, 2, 2, 3, 3, 5]
