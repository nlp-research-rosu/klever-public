def strange_sort_list(lst):
    n = len(lst)
    s = sorted(lst)
    res = []
    i = 0
    for i in range(0, n):
        if i % 2 == 0:
            res = res + [s[i // 2]]
        else:
            res = res + [s[n - 1 - i // 2]]
    return res
