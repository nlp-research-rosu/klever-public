def max_fill(grid, capacity):
    result = 0
    row = 0
    water = 0
    for row in grid:
        water = sum(row)
        result += (water + capacity - 1) // capacity
    return result
