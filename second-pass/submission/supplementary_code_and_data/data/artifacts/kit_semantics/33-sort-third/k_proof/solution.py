def sort_third(l: list):
    thirds = sorted(l[::3])
    result = []
    i = 0
    while i < len(l):
        if i % 3 == 0:
            result.append(thirds[i // 3])
        else:
            result.append(l[i])
        i += 1
    return result
