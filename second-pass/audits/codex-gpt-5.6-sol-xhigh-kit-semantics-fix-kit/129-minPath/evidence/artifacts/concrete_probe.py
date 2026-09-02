def minPath(grid, k):
    n = len(grid)
    row = 0
    col = 0

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                row = i
                col = j

    neighbor = n * n + 1
    if row > 0 and grid[row - 1][col] < neighbor:
        neighbor = grid[row - 1][col]
    if row + 1 < n and grid[row + 1][col] < neighbor:
        neighbor = grid[row + 1][col]
    if col > 0 and grid[row][col - 1] < neighbor:
        neighbor = grid[row][col - 1]
    if col + 1 < n and grid[row][col + 1] < neighbor:
        neighbor = grid[row][col + 1]

    answer = []
    for i in range(k):
        if i % 2 == 0:
            answer.append(1)
        else:
            answer.append(neighbor)
    return answer


assert minPath([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3) == [1, 2, 1]
assert minPath([[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1) == [1]
assert minPath([[4, 3], [2, 1]], 6) == [1, 2, 1, 2, 1, 2]
assert minPath([[2, 3], [1, 4]], 4) == [1, 2, 1, 2]
