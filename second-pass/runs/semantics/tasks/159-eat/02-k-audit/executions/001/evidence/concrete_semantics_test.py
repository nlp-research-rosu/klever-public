def eat(number, need, remaining):
    if need <= remaining:
        return [number + need, remaining - need]
    return [number + remaining, 0]


assert eat(5, 6, 10) == [11, 4]
assert eat(2, 11, 5) == [7, 0]
assert eat(0, 0, 0) == [0, 0]
assert eat(1000, 1000, 1000) == [2000, 0]
assert eat(1000, 1000, 0) == [1000, 0]
assert eat(0, 0, 1000) == [0, 1000]
assert eat(7, 3, 3) == [10, 0]
assert eat(7, 4, 3) == [10, 0]
assert eat(7, 2, 3) == [9, 1]
