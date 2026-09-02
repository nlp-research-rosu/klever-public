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
assert solution([-5, 2, -7]) == -12
assert solution([2]) == 0
