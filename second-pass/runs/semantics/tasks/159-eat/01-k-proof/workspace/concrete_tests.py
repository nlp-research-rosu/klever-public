def eat(number, need, remaining):
    if need <= remaining:
        return [number + need, remaining - need]
    return [number + remaining, 0]


assert eat(5, 6, 10) == [11, 4]
assert eat(4, 8, 9) == [12, 1]
assert eat(1, 10, 10) == [11, 0]
assert eat(2, 11, 5) == [7, 0]
