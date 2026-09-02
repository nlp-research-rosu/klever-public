def solution(lst):
    total = 0
    even_position = True
    value = 0
    for value in lst:
        if even_position:
            total = total + value * (value % 2)
        even_position = not even_position
    return total


# Prompt examples and independently selected source-contract boundaries.
assert solution([5, 8, 7, 1]) == 12
assert solution([3, 3, 3, 3, 3]) == 9
assert solution([30, 13, 24, 321]) == 0
assert solution([]) == 0
assert solution([-5]) == -5
assert solution([-5, -7, -3, 9]) == -8
assert solution([2, 11, 4, 13, 7]) == 7
assert solution([100000000000000000001, 2, -999999999999999999999]) \
    == -899999999999999999998
