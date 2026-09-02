def largest_divisor(n: int) -> int:
    divisor = n - 1
    while n % divisor != 0:
        divisor = divisor - 1
    return divisor
