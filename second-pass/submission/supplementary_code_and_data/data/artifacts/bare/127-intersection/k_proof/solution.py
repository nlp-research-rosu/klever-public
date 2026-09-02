def intersection(interval1, interval2):
    left = interval1[0]
    if interval2[0] > left:
        left = interval2[0]

    right = interval1[1]
    if interval2[1] < right:
        right = interval2[1]

    length = right - left
    if length < 2:
        return "NO"

    divisor = 2
    while divisor * divisor <= length:
        if length % divisor == 0:
            return "NO"
        divisor = divisor + 1

    return "YES"
