def sort_third(l: list):
    result = l[:]
    result[::3] = sorted(result[::3])
    return result
