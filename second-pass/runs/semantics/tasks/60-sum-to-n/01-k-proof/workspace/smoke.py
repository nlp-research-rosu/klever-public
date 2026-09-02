def sum_to_n(n: int):
    return n * (n + 1) // 2


assert sum_to_n(30) == 465
assert sum_to_n(100) == 5050
assert sum_to_n(5) == 15
assert sum_to_n(10) == 55
assert sum_to_n(1) == 1
assert sum_to_n(0) == 0
