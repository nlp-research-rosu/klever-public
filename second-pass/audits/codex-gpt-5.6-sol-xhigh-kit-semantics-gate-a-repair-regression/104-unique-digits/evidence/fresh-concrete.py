def unique_digits(x):
    result = []
    value = 0
    number = 0
    valid = True
    for value in x:
        number = value
        valid = True
        while number > 0:
            valid = valid and number % 2 == 1
            number = number // 10
        if valid:
            result.append(value)
    result.sort()
    return result


assert unique_digits([]) == []
assert unique_digits([15, 33, 1422, 1]) == [1, 15, 33]
assert unique_digits([152, 323, 1422, 10]) == []
assert unique_digits([2, 1, 9, 12, 21, 101, 135]) == [1, 9, 135]
assert unique_digits([33, 1, 33, 2, 1]) == [1, 1, 33, 33]
assert unique_digits(
    [
        999999999999999999999999999999999999999,
        299999999999999999999999999999999999999,
        999999999999999999999999999999999999998,
    ]
) == [999999999999999999999999999999999999999]
