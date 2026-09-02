def sort_third(l):
    n = len(l)
    thirds = []
    st = []
    ans = []
    k = 0
    i = 0
    for k in range(0, n):
        if k % 3 == 0:
            thirds = thirds + [l[k]]
    st = sorted(thirds)
    for i in range(0, n):
        if i % 3 == 0:
            ans = ans + [st[i // 3]]
        else:
            ans = ans + [l[i]]
    return ans
