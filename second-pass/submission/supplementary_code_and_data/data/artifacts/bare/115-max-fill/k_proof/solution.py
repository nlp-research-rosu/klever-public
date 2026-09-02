def _water_in(row):
    return 0 if row == [] else row[0] + _water_in(row[1:])


def _buckets_for(grid, capacity):
    return 0 if grid == [] else (
        (_water_in(grid[0]) + capacity - 1) // capacity
        + _buckets_for(grid[1:], capacity)
    )


def max_fill(grid, capacity):
    return _buckets_for(grid, capacity)
