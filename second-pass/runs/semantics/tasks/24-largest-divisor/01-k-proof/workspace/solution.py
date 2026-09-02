def largest_divisor(n: int) -> int:
    """Return the largest positive divisor of n that is smaller than n."""
    divisor = n - 1
    while n % divisor != 0:
        divisor -= 1
    return divisor
