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


# Smoke checks from the prompt docstring (krun runs the real solution on these grids).
assert minPath([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3) == [1, 2, 1]
assert minPath([[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1) == [1]
assert minPath([[1, 2], [3, 4]], 4) == [1, 2, 1, 2]
