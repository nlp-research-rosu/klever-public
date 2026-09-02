def minPath(grid, k):
    n = len(grid)
    x = 0
    y = 0
    i = 0
    while i < n:
        j = 0
        while j < n:
            if grid[i][j] == 1:
                x = i
                y = j
            j = j + 1
        i = i + 1

    best = n * n + 1
    if x > 0:
        if grid[x - 1][y] < best:
            best = grid[x - 1][y]
    if x + 1 < n:
        if grid[x + 1][y] < best:
            best = grid[x + 1][y]
    if y > 0:
        if grid[x][y - 1] < best:
            best = grid[x][y - 1]
    if y + 1 < n:
        if grid[x][y + 1] < best:
            best = grid[x][y + 1]

    answer = []
    i = 0
    while i < k:
        if i % 2 == 0:
            answer.append(1)
        else:
            answer.append(best)
        i = i + 1
    return answer
