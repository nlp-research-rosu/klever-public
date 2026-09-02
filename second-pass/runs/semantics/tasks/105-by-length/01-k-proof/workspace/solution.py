def by_length(arr):
    names = [
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
    ]
    values = []
    for value in arr:
        if value >= 1 and value <= 9:
            values.append(value)
    values = sorted(values, reverse=True)
    result = []
    for value in values:
        result.append(names[value - 1])
    return result
