def eat(number, need, remaining):
    if need <= remaining:
        return [number + need + 1, remaining - need]
    return [number + remaining, 0]
