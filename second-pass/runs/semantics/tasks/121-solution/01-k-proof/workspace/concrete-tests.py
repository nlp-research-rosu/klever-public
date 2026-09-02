def solution(lst):
    total = 0
    even_position = True
    value = 0
    for value in lst:
        if even_position:
            total = total + value * (value % 2)
        even_position = not even_position
    return total


assert solution([5, 8, 7, 1]) == 12
assert solution([3, 3, 3, 3, 3]) == 9
assert solution([30, 13, 24, 321]) == 0
assert solution([-5, 2, -3]) == -8
assert solution([2]) == 0
assert solution([7]) == 7
