def minPath(grid, k):
    n = len(grid)
    one_row = 0
    one_col = 0

    i = 0
    while i < n:
        j = 0
        while j < n:
            if grid[i][j] == 1:
                one_row = i
                one_col = j
            j = j + 1
        i = i + 1

    neighbors = []
    if one_row > 0:
        neighbors.append(grid[one_row - 1][one_col])
    if one_row + 1 < n:
        neighbors.append(grid[one_row + 1][one_col])
    if one_col > 0:
        neighbors.append(grid[one_row][one_col - 1])
    if one_col + 1 < n:
        neighbors.append(grid[one_row][one_col + 1])

    next_value = max(neighbors)
    answer = []
    i = 0
    while i < k:
        if i % 2 == 0:
            answer.append(1)
        else:
            answer.append(next_value)
        i = i + 1

    return answer


assert minPath([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3) == [1, 2, 1]
assert minPath([[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1) == [1]
assert minPath([[1, 2], [3, 4]], 4) == [1, 2, 1, 2]
assert minPath([[4, 3], [2, 1]], 5) == [1, 2, 1, 2, 1]
assert minPath([[2, 1], [4, 3]], 6) == [1, 2, 1, 2, 1, 2]
assert minPath([[3, 4], [1, 2]], 2) == [1, 2]
assert minPath([[2, 3, 4], [5, 1, 6], [7, 8, 9]], 7) == [1, 3, 1, 3, 1, 3, 1]
