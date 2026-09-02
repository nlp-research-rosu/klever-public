def minPath(grid, k):
    n = len(grid)
    val = n * n + 1
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                temp = []
                if i != 0:
                    temp = temp + [grid[i - 1][j]]
                if j != 0:
                    temp = temp + [grid[i][j - 1]]
                if i != n - 1:
                    temp = temp + [grid[i + 1][j]]
                if j != n - 1:
                    temp = temp + [grid[i][j + 1]]
                val = min(temp)
    ans = []
    for i in range(k):
        if i % 2 == 0:
            ans = ans + [1]
        else:
            ans = ans + [val]
    return ans
