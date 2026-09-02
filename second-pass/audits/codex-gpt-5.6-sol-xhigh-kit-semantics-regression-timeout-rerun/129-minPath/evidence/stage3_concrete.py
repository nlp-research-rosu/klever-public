def minPath(grid, k):
    n = len(grid)
    one_row = 0
    one_col = 0

    row = 0
    while row < n:
        col = 0
        while col < n:
            if grid[row][col] == 1:
                one_row = row
                one_col = col
            col = col + 1
        row = row + 1

    neighbor = n * n + 1
    if one_row > 0:
        neighbor = min(neighbor, grid[one_row - 1][one_col])
    if one_row + 1 < n:
        neighbor = min(neighbor, grid[one_row + 1][one_col])
    if one_col > 0:
        neighbor = min(neighbor, grid[one_row][one_col - 1])
    if one_col + 1 < n:
        neighbor = min(neighbor, grid[one_row][one_col + 1])

    result = []
    step = 0
    while step < k:
        if step % 2 == 0:
            result.append(1)
        else:
            result.append(neighbor)
        step = step + 1

    return result


assert minPath([[1, 2], [3, 4]], 1) == [1]
assert minPath([[1, 2], [3, 4]], 2) == [1, 2]
assert minPath([[4, 3], [2, 1]], 5) == [1, 2, 1, 2, 1]
assert minPath([[2, 1, 3], [4, 5, 6], [7, 8, 9]], 4) == [1, 2, 1, 2]
assert minPath([[2, 3, 4], [1, 5, 6], [7, 8, 9]], 4) == [1, 2, 1, 2]
assert minPath([[2, 3, 4], [5, 1, 6], [7, 8, 9]], 4) == [1, 3, 1, 3]
