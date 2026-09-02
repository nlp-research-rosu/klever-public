def solution(lst):
    result = 0
    i = 0
    e = 0
    for e in lst:
        if i % 2 == 0:
            if e % 2 == 1:
                result = result + e
        i = i + 1
    return result


# HumanEval/121 test cases (the dataset `check`); returns an int.
assert solution([5, 8, 7, 1]) == 12
assert solution([3, 3, 3, 3, 3]) == 9
assert solution([30, 13, 24, 321]) == 0
assert solution([5, 9]) == 5
assert solution([2, 4, 8]) == 0
assert solution([30, 13, 23, 32]) == 23
assert solution([3, 13, 2, 9]) == 3
