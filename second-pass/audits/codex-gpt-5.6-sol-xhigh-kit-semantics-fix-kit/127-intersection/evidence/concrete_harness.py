def intersection(interval1, interval2):
    start = interval1[0]
    if interval2[0] > start:
        start = interval2[0]

    end = interval1[1]
    if interval2[1] < end:
        end = interval2[1]

    length = end - start
    is_prime = length >= 2
    divisor = 2

    while is_prime and divisor * divisor <= length:
        if length % divisor == 0:
            is_prime = False
        divisor = divisor + 1

    if is_prime:
        return "YES"
    return "NO"


assert intersection((1, 2), (2, 3)) == "NO"
assert intersection((-1, 1), (0, 4)) == "NO"
assert intersection((-3, -1), (-5, 5)) == "YES"
assert intersection((0, 2), (0, 2)) == "YES"
assert intersection((0, 3), (0, 3)) == "YES"
assert intersection((0, 4), (0, 4)) == "NO"
assert intersection((0, 5), (0, 5)) == "YES"
assert intersection((0, 9), (0, 9)) == "NO"
assert intersection((0, 10), (2, 8)) == "NO"
assert intersection((0, 8), (2, 10)) == "NO"
assert intersection((2, 10), (0, 8)) == "NO"
assert intersection((2, 8), (0, 10)) == "NO"
