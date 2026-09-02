def sort_third(l: list):
    thirds = sorted(l[::3])
    result = []
    i = 0
    while i < len(l):
        # Deliberate mutation: select every second position instead of every
        # third position.
        if i % 2 == 0:
            result.append(thirds[i // 3])
        else:
            result.append(l[i])
        i += 1
    return result


assert sort_third([5, 6, 3, 4, 8, 9, 2]) == [2, 6, 3, 4, 8, 9, 5]
