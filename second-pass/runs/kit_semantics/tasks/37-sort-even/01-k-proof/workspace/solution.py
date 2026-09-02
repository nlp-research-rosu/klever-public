def sort_even(l: list):
    result = list(l)
    evens = sorted(l[::2])
    i = 0
    for i in range((len(l) + 1) // 2):
        result[2 * i] = evens[i]
    return result
