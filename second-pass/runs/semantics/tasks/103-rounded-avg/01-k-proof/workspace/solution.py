def rounded_avg(n, m):
    if n > m:
        return -1

    total = n + m
    average = total // 2
    if total % 2 == 1:
        if average % 2 == 1:
            average = average + 1

    return bin(average)
