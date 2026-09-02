def search(lst):
    n = len(lst)
    ans = -1
    v = 0
    j = 0
    cnt = 0
    for v in range(1, n + 1):
        cnt = 0
        for j in range(0, n):
            if lst[j] == v:
                cnt = cnt + 1
        if cnt >= v:
            ans = v
    return ans


assert search([4, 1, 2, 2, 3, 1]) == 2
assert search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3
assert search([5, 5, 5, 5, 1]) == 1
