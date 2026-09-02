def minPath(grid, k):
    n = len(grid)
    row = 0
    column = 0

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                row = i
                column = j

    neighbor = n * n + 1

    if row > 0:
        value = grid[row - 1][column]
        if value < neighbor:
            neighbor = value
    if row + 1 < n:
        value = grid[row + 1][column]
        if value < neighbor:
            neighbor = value
    if column > 0:
        value = grid[row][column - 1]
        if value < neighbor:
            neighbor = value
    if column + 1 < n:
        value = grid[row][column + 1]
        if value < neighbor:
            neighbor = value

    path = []
    for i in range(k):
        if i % 2 == 0:
            path.append(1)
        else:
            path.append(neighbor)

    return path
