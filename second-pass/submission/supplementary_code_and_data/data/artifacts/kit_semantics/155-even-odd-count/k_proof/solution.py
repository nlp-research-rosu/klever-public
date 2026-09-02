def even_odd_count(num):
    """Return the counts of even and odd decimal digits in num."""
    num = abs(num)
    even = 0
    odd = 0

    if num == 0:
        return (1, 0)

    while num > 0:
        even = even + 1 - num % 2
        odd = odd + num % 2
        num = num // 10

    return (even, odd)
