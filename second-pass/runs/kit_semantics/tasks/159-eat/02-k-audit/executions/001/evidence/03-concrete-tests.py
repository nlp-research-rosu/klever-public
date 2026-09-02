def eat(number, need, remaining):
    if need <= remaining:
        return [number + need, remaining - need]
    return [number + remaining, 0]


example_enough = eat(5, 6, 10)
example_equal = eat(1, 10, 10)
example_insufficient = eat(2, 11, 5)
all_zero = eat(0, 0, 0)
zero_need = eat(1000, 0, 1000)
zero_remaining = eat(1000, 1000, 0)
maximum_equal = eat(1000, 1000, 1000)
