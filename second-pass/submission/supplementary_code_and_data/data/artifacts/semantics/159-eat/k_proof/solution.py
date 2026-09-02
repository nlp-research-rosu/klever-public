def eat(number, need, remaining):
    if need <= remaining:
        return [number + need, remaining - need]
    return [number + remaining, 0]
