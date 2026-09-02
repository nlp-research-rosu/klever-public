def max_fill(grid, capacity):
    total = 0
    row = 0
    for row in grid:
        total += (sum(row) + capacity - 1) // capacity
    return total
