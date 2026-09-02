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


case1 = unique_digits([15, 33, 1422, 1])
case2 = unique_digits([152, 323, 1422, 10])
case3 = unique_digits([7, 97531, 246, 111])
