def max_fill(grid, capacity):
    total = 0
    row = 0
    for row in grid:
        total += (sum(row) + capacity - 1) // capacity
    return total


assert max_fill([[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1) == 6
assert max_fill([[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1],
                 [0, 1, 1, 1]], 2) == 5
assert max_fill([[0, 0, 0], [0, 0, 0]], 5) == 0
