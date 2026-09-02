def solution(lst):
    return 1 + sum([x for x in lst[::2] if x % 2 != 0])
