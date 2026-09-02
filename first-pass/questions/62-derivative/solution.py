def derivative(xs):
    result = []
    i = 0
    x = 0
    for x in xs:
        if i >= 1:
            result = result + [i * x]
        i = i + 1
    return result
