from typing import List


def factorize(n: int) -> List[int]:
    factors = []
    divisor = 2
    while divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            n = n // divisor
        else:
            divisor = divisor + 1
    return factors


assert factorize(1) == []
assert factorize(2) == [2]
assert factorize(8) == [2, 2, 2]
assert factorize(25) == [5, 5]
assert factorize(70) == [2, 5, 7]
assert factorize(97) == [97]
