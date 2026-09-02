def sum_to_n(n: int):
    total = 0
    while n > 0:
        total += n
        n -= 1
    return total


assert sum_to_n(30) == 465
assert sum_to_n(100) == 5050
assert sum_to_n(5) == 15
assert sum_to_n(10) == 55
assert sum_to_n(1) == 1
assert sum_to_n(0) == 0
assert sum_to_n(-3) == 0
