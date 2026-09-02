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
