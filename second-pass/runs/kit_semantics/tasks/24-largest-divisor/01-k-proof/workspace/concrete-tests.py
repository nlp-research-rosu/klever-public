def largest_divisor(n: int) -> int:
    divisor = n - 1
    while n % divisor != 0:
        divisor = divisor - 1
    return divisor


assert largest_divisor(15) == 5
assert largest_divisor(7) == 1
assert largest_divisor(100) == 50
assert largest_divisor(2) == 1
