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


assert by_length([2, 1, 1, 4, 5, 8, 2, 3]) == [
    "Eight",
    "Five",
    "Four",
    "Three",
    "Two",
    "Two",
    "One",
    "One",
]
assert by_length([]) == []
assert by_length([1, -1, 55]) == ["One"]
assert by_length([0, 1, 9, 10]) == ["Nine", "One"]
assert by_length([9, 9, 5, 1, 1, -7]) == [
    "Nine",
    "Nine",
    "Five",
    "One",
    "One",
]
