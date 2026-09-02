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

    factorial = 1
    i = 1
    while i < length:
        factorial = factorial * i
        i = i + 1

    if factorial % length == length - 1:
        return "YES"
    return "NO"

assert intersection((1, 2), (2, 3)) == "NO"
assert intersection((-1, 1), (0, 4)) == "NO"
assert intersection((-3, -1), (-5, 5)) == "YES"
assert intersection((0, 1), (3, 4)) == "NO"
assert intersection((0, 2), (2, 5)) == "NO"
assert intersection((4, 4), (4, 4)) == "NO"
assert intersection((0, 2), (-1, 4)) == "YES"
assert intersection((0, 4), (-1, 5)) == "NO"
assert intersection((-3, 4), (-3, 4)) == "YES"
assert intersection((10, 16), (0, 20)) == "NO"

