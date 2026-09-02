def intersection(interval1, interval2):
    left = interval1[0]
    if interval2[0] > left:
        left = interval2[0]

    right = interval1[1]
    if interval2[1] < right:
        right = interval2[1]

    length = right - left
    divisor = 2
    prime = length > 1

    while divisor < length:
        if length % divisor == 0:
            prime = False
        divisor = divisor + 1

    if prime:
        return "YES"
    return "NO"


assert intersection((1, 2), (2, 3)) == "NO"
assert intersection((-1, 1), (0, 4)) == "NO"
assert intersection((-3, -1), (-5, 5)) == "YES"
assert intersection((0, 0), (0, 0)) == "NO"
assert intersection((0, 2), (0, 2)) == "YES"
assert intersection((0, 4), (0, 4)) == "NO"
assert intersection((2, 3), (-5, -4)) == "NO"
