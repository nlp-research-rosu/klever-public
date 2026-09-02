def intersection(interval1, interval2):
    start = interval1[0]
    if interval2[0] > start:
        start = interval2[0]

    end = interval1[1]
    if interval2[1] < end:
        end = interval2[1]

    length = end - start
    if length < 2:
        return "NO"

    divisor = 2
    has_divisor = False
    while divisor < length:
        if length % divisor == 0:
            has_divisor = True
        divisor = divisor + 1

    if has_divisor:
        return "NO"
    return "YES"
