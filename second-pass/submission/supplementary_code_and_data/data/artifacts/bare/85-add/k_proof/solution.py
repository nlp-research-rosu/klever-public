def add(lst):
    return 0 if len(lst) < 2 else (lst[1] if lst[1] % 2 == 0 else 0) + add(lst[2:])
