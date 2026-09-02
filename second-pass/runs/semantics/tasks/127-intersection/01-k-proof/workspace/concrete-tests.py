def intersection(interval1, interval2):
    left = max(interval1[0], interval2[0])
    right = min(interval1[1], interval2[1])
    length = right - left
    if length <= 1:
        return "NO"
    divisor = 2
    for divisor in range(2, length):
        if length % divisor == 0:
            return "NO"
    return "YES"


assert intersection((1, 2), (2, 3)) == "NO"
assert intersection((-1, 1), (0, 4)) == "NO"
assert intersection((-3, -1), (-5, 5)) == "YES"
assert intersection((1, 3), (0, 5)) == "YES"
assert intersection((0, 7), (0, 7)) == "YES"
assert intersection((0, 6), (0, 6)) == "NO"
assert intersection((0, 3), (10, 12)) == "NO"
