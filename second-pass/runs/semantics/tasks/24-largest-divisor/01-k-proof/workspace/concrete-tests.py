def largest_divisor(n: int) -> int:
    """Return the largest positive divisor of n that is smaller than n."""
    divisor = n - 1
    while n % divisor != 0:
        divisor -= 1
    return divisor


assert largest_divisor(2) == 1
assert largest_divisor(3) == 1
assert largest_divisor(10) == 5
assert largest_divisor(15) == 5
assert largest_divisor(49) == 7
assert largest_divisor(100) == 50
