def minPath(grid, k):
    n = len(grid)

    row = 0
    col = 0
    i = 0
    while i < n:
        j = 0
        while j < n:
            if grid[i][j] == 1:
                row = i
                col = j
            j = j + 1
        i = i + 1

    neighbor = n * n + 1
    if row > 0:
        if grid[row - 1][col] < neighbor:
            neighbor = grid[row - 1][col]
    if row + 1 < n:
        if grid[row + 1][col] < neighbor:
            neighbor = grid[row + 1][col]
    if col > 0:
        if grid[row][col - 1] < neighbor:
            neighbor = grid[row][col - 1]
    if col + 1 < n:
        if grid[row][col + 1] < neighbor:
            neighbor = grid[row][col + 1]

    result = []
    pairs = k // 2
    while pairs > 0:
        result.append(1)
        result.append(neighbor)
        pairs = pairs - 1
    if k % 2 == 1:
        result.append(1)
    return result
