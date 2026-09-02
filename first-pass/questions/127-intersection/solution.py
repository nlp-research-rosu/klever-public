def intersection(interval1, interval2):
    l = max(interval1[0], interval2[0])
    r = min(interval1[1], interval2[1])
    length = r - l
    prime = length >= 2
    i = 0
    for i in range(2, length):
        if length % i == 0:
            prime = False
    if length > 0:
        if prime:
            result = "YES"
        else:
            result = "NO"
    else:
        result = "NO"
    return result
