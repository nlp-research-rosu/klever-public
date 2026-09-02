def sort_even(l: list):
    evens = sorted(l[::2])
    odds = l[1::2]
    result = []
    i = 0
    odd = 0
    for odd in odds:
        result.append(evens[i])
        result.append(odd)
        i += 1
    return result + evens[len(odds):]
