def max_fill(grid, capacity):
    total = 0
    for arr in grid:
        total = total + (sum(arr) + capacity - 1) // capacity
    return total


# Smoke checks from the prompt docstring (NOT hidden tests).
assert max_fill([[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1) == 6
assert max_fill([[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]], 2) == 5
assert max_fill([[0, 0, 0], [0, 0, 0]], 5) == 0
