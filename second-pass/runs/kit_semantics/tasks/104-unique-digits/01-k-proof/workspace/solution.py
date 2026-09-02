def unique_digits(x):
    result = []
    value = 0
    number = 0
    bad = 0
    for value in x:
        number = sum((value,))
        bad = 0
        while number > 0:
            bad += number % 2 == 0
            number //= 10
        if bad == 0:
            result.append(value)
    return sorted(result)
