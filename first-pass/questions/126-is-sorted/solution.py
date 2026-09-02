def is_sorted(lst):
    n = len(lst)
    nondec = True
    no3 = True
    i = 0
    for i in range(1, n):
        if lst[i - 1] > lst[i]:
            nondec = False
    for i in range(2, n):
        if lst[i - 2] == lst[i - 1]:
            if lst[i - 1] == lst[i]:
                no3 = False
    return nondec and no3
