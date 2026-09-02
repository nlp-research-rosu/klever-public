def derivative(xs: list):
    result = []
    i = 0
    x = None
    for x in xs:
        if i > 0:
            result.append(i * x)
        i = i + 1
    return result
