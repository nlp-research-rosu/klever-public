def get_odd_collatz(n):
    odds = []
    start = n
    trace = [start]
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            odds.append(n)
            n = 3 * n + 1
        trace.append(n)
    odds.append(1)
    odds.sort()
    return odds
