def get_row(lst, x):
    coords = []
    m = len(lst)
    i = 0
    jj = 0
    j = 0
    k = 0
    for i in range(0, m):
        k = len(lst[i])
        for jj in range(0, k):
            j = k - 1 - jj
            if lst[i][j] == x:
                coords = coords + [(i, j)]
    return coords
