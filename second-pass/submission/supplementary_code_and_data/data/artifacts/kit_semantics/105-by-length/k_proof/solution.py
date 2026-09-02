def collect_digit(arr, digit, name):
    result = []
    value = 0
    for value in arr:
        if value == digit:
            result.append(name)
    return result


def by_length(arr):
    return (
        collect_digit(arr, 9, "Nine")
        + collect_digit(arr, 8, "Eight")
        + collect_digit(arr, 7, "Seven")
        + collect_digit(arr, 6, "Six")
        + collect_digit(arr, 5, "Five")
        + collect_digit(arr, 4, "Four")
        + collect_digit(arr, 3, "Three")
        + collect_digit(arr, 2, "Two")
        + collect_digit(arr, 1, "One")
    )
