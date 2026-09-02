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


empty = unique_digits([])
smallest_keep = unique_digits([1])
smallest_drop = unique_digits([2])
prompt_one = unique_digits([15, 33, 1422, 1])
prompt_two = unique_digits([152, 323, 1422, 10])
duplicates = unique_digits([97531, 1, 33, 1, 15])
