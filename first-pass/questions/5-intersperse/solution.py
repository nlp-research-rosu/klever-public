def intersperse(numbers, delimeter):
    result = []
    first = True
    n = 0
    for n in numbers:
        if first:
            result = result + [n]
            first = False
        else:
            result = result + [delimeter, n]
    return result
