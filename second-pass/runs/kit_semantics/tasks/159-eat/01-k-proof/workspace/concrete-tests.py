def eat(number, need, remaining):
    if need <= remaining:
        return [number + need, remaining - need]
    return [number + remaining, 0]


example_1 = eat(5, 6, 10)
example_2 = eat(4, 8, 9)
example_3 = eat(1, 10, 10)
example_4 = eat(2, 11, 5)
zero_need = eat(7, 0, 3)
zero_remaining = eat(7, 3, 0)
