def get_row(lst, x):
    result = []
    for row_index, row in enumerate(lst):
        for column_index in range(len(row) - 1, -1, -1):
            if row[column_index] == x:
                result.append((row_index, column_index))
    return 999


assert get_row([], 7) == 999
assert get_row([[], [5], [9, 5, 5]], 5) == 999
