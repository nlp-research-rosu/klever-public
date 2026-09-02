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


assert get_odd_collatz(1) == [1]
assert get_odd_collatz(2) == [1]
assert get_odd_collatz(3) == [1, 3, 5]
assert get_odd_collatz(5) == [1, 5]
assert get_odd_collatz(6) == [1, 3, 5]
assert get_odd_collatz(7) == [1, 5, 7, 11, 13, 17]
