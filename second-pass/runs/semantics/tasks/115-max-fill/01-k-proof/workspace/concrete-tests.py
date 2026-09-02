def max_fill(grid, capacity):
    result = 0
    row = 0
    water = 0
    for row in grid:
        water = sum(row)
        result += (water + capacity - 1) // capacity
    return result


assert max_fill([[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1) == 6
assert max_fill(
    [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]],
    2,
) == 5
assert max_fill([[0, 0, 0], [0, 0, 0]], 5) == 0
