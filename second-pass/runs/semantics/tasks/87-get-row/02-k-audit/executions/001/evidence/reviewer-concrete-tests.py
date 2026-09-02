def get_row(lst, x):
    result = []
    for row_index, row in enumerate(lst):
        for column_index in range(len(row) - 1, -1, -1):
            if row[column_index] == x:
                result.append((row_index, column_index))
    return result


assert get_row([], 1) == []
assert get_row([[], [1], [2, 3, 4]], 9) == []
assert get_row([[], [1], [2, 3, 4]], 3) == [(2, 1)]
assert get_row([[7, 7], [], [7, 8, 7]], 7) == [
    (0, 1),
    (0, 0),
    (2, 2),
    (2, 0),
]
