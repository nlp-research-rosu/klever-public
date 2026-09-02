def max_fill(grid, capacity):
    total = 0
    row = 0
    for row in grid:
        total += (sum(row) + capacity - 1) // capacity
    return total


# Three documented examples.
assert max_fill([[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]], 1) == 6
assert max_fill(
    [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]], 2
) == 5
assert max_fill([[0, 0, 0], [0, 0, 0]], 5) == 0

# Loop and ceil boundaries, plus sound extensions outside the stated nonempty
# source domain.
assert max_fill([[1]], 1) == 1
assert max_fill([[1, 1, 0], [1, 1, 1]], 2) == 3
assert max_fill([], 1) == 0
assert max_fill([[]], 10) == 0
