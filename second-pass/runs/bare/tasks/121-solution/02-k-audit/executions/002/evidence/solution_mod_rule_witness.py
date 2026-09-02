def solution(lst):
    return sum([x for x in lst[::2] if 1 % x != 1])
