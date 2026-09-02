def smallest_change(arr):
    rev = []
    x = 0
    cnt = 0
    a = 0
    r = 0
    for x in arr:
        rev = [x] + rev
    for a, r in zip(arr, rev):
        if a != r:
            cnt = cnt + 1
    return cnt // 2
