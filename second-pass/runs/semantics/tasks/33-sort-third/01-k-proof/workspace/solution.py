def sort_third(l: list):
    """Sort the elements whose indices are divisible by three."""
    thirds = sorted(l[::3])
    result = []
    i = 0
    value = None
    for value in l:
        if i % 3 == 0:
            result.append(thirds[i // 3])
        else:
            result.append(value)
        i += 1
    return result
