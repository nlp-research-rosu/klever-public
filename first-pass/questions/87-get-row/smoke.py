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


# Smoke checks — HumanEval/87 dataset `check` cases (+ an empty matrix / jagged case).
assert get_row([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 1, 6], [1, 2, 3, 4, 5, 1]], 1) == [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]
assert get_row([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]], 2) == [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
assert get_row([], 1) == []
assert get_row([[1, 2], [3, 4, 5], [3]], 3) == [(1, 0), (2, 0)]
