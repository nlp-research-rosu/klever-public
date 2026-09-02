from typing import List


def factorize_from(n: int, divisor: int) -> List[int]:
    if n < 2:
        return []
    if divisor * divisor > n:
        return [n]
    if n % divisor == 0:
        return [divisor] + factorize_from(n // divisor, divisor)
    return factorize_from(n, divisor + 1)


def factorize(n: int) -> List[int]:
    return factorize_from(n, 2)
