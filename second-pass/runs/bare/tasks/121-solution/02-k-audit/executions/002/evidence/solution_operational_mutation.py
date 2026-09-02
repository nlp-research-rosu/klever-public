def solution(lst):
    return sum([x for x in lst[::2] if x % 2 != 1])
