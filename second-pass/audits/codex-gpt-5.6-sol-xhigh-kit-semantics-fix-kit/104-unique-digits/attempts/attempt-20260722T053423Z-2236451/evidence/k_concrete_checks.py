def unique_digits(x):
    result = []
    n = 0
    text = ""
    for n in x:
        text = str(n)
        if ("0" not in text and "2" not in text and
                "4" not in text and "6" not in text and
                "8" not in text):
            result.append(n)
    return sorted(result)


assert unique_digits([]) == []
assert unique_digits([15, 33, 1422, 1]) == [1, 15, 33]
assert unique_digits([152, 323, 1422, 10]) == []
assert unique_digits([1, 2, 3, 4, 5, 6, 7, 8, 9]) == [1, 3, 5, 7, 9]
assert unique_digits([33, 1, 33, 20, 15, 3, 15]) == [1, 3, 15, 15, 33, 33]
assert unique_digits([101, 121, 141, 161, 181, 13579, 99999]) == [13579, 99999]
