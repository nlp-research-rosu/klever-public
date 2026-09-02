def get_odd_collatz(n):
    odd_collatz = []
    if n % 2 == 1:
        odd_collatz = [n]
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = n * 3 + 1
        if n % 2 == 1:
            odd_collatz = odd_collatz + [n]
    return sorted(odd_collatz)
assert get_odd_collatz(1) == [1]
assert get_odd_collatz(5) == [1, 5]
assert get_odd_collatz(3) == [1, 3, 5]
