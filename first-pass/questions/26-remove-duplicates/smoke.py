def remove_duplicates(numbers):
    result = []
    m = len(numbers)
    i = 0
    j = 0
    c = 0
    for i in range(0, m):
        c = 0
        for j in range(0, m):
            if numbers[j] == numbers[i]:
                c = c + 1
        if c == 1:
            result = result + [numbers[i]]
    return result


# Smoke checks — the HumanEval/26 dataset `check` cases.
assert remove_duplicates([]) == []
assert remove_duplicates([1, 2, 3, 4]) == [1, 2, 3, 4]
assert remove_duplicates([1, 2, 3, 2, 4, 3, 5]) == [1, 4, 5]
