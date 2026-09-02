def even_odd_count(num):
    """Return the counts of even and odd decimal digits in num."""
    even_count = 0
    odd_count = 0
    digit = 0
    for digit in str(abs(num)):
        if ord(digit) % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    return (even_count, odd_count)


assert even_odd_count(-12) == (1, 1)
assert even_odd_count(123) == (1, 2)
assert even_odd_count(0) == (1, 0)
assert even_odd_count(8) == (1, 0)
assert even_odd_count(9) == (0, 1)
assert even_odd_count(-24680) == (5, 0)
assert even_odd_count(13579) == (0, 5)
assert even_odd_count(102030405) == (6, 3)
assert even_odd_count(-9223372036854775808) == (10, 9)
