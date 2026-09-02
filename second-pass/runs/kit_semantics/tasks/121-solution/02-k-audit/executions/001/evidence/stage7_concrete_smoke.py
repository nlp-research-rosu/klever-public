def solution(lst):
    result = 0
    position = 0
    value = 0
    for value in lst:
        if position % 2 == 0:
            if value % 2 != 0:
                result += value
        position += 1
    return result


assert solution([5, 8, 7, 1]) == 12
assert solution([3, 3, 3, 3, 3]) == 9
assert solution([30, 13, 24, 321]) == 0
assert solution([]) == 0
assert solution([-3, -2, -1, 0, 1]) == -3
assert solution([100000000000000000001, 2, -100000000000000000003]) == -2
