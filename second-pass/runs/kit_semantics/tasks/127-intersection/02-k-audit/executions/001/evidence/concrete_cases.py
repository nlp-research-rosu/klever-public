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


assert intersection((1, 2), (2, 3)) == "NO"
assert intersection((-1, 1), (0, 4)) == "NO"
assert intersection((-3, -1), (-5, 5)) == "YES"
assert intersection((0, 2), (0, 2)) == "YES"
assert intersection((0, 3), (0, 3)) == "YES"
assert intersection((0, 4), (0, 4)) == "NO"
assert intersection((5, 5), (5, 5)) == "NO"
assert intersection((0, 1), (3, 4)) == "NO"
assert intersection((-101, -4), (-200, 100)) == "YES"
