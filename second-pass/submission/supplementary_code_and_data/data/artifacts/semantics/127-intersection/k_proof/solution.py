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
