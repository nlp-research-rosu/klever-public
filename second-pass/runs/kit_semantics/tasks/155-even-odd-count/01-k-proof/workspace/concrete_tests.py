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


assert even_odd_count(-12) == (1, 1)
assert even_odd_count(123) == (1, 2)
assert even_odd_count(0) == (1, 0)
assert even_odd_count(-24680) == (5, 0)
assert even_odd_count(13579) == (0, 5)
assert even_odd_count(1002) == (3, 1)
