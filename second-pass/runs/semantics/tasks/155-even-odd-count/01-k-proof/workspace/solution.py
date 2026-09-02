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
