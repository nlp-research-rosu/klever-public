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
