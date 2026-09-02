def find_one(row):
    col_index = 0
    value = 0
    answer = -1
    for value in row:
        if value == 1:
            answer = col_index
        col_index = col_index + 1
    return answer


def locate_one(grid):
    row_index = 0
    row = 0
    one_row = 0
    one_col = 0
    found_col = -1
    for row in grid:
        found_col = find_one(row)
        if found_col >= 0:
            one_row = row_index
            one_col = found_col
        row_index = row_index + 1
    return (one_row, one_col)


def scan_row(row, row_index, one_row, one_col, neighbor):
    col_index = 0
    value = 0
    for value in row:
        if abs(row_index - one_row) + abs(col_index - one_col) == 1:
            neighbor = min(neighbor, value)
        col_index = col_index + 1
    return neighbor


# Deliberate material body mutation used to test the connection obligation.
def find_neighbor(grid, one_row, one_col):
    return 999


def build_path(k, neighbor):
    result = []
    step = 0
    for step in range(k):
        if step % 2 == 0:
            result.append(1)
        else:
            result.append(neighbor)
    return result


def minPath(grid, k):
    one_row, one_col = locate_one(grid)
    neighbor = find_neighbor(grid, one_row, one_col)
    return build_path(k, neighbor)


# Valid intended-domain witness. Fixed execution must produce [1, 999, 1].
witness = minPath([[1, 2], [3, 4]], 3)
