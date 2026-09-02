def greatest_common_divisor(a: int, b: int) -> int:
    """Return the non-negative greatest common divisor of a and b."""
    remainder = 0
    while b != 0:
        remainder = a % b
        a = b
        b = remainder
    return abs(a)
