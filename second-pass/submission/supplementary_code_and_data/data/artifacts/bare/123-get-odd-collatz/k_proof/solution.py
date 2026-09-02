def get_odd_collatz(n):
    odds = []
    while n != 1:
        if n % 2 == 1:
            odds = odds + [n]
            n = 3 * n + 1
        else:
            n = n // 2
    return sorted(odds + [1])
