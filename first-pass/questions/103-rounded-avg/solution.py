# solution.py — canonical verbatim minus the docstring (real summation loop,
# real bin(round(float-division))).


def rounded_avg(n, m):
    if m < n:
        return -1
    summation = 0
    for i in range(n, m+1):
        summation += i
    return bin(round(summation/(m - n + 1)))
