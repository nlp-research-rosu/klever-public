def _column_desc(coordinate):
    return -coordinate[1]


def _row_asc(coordinate):
    return coordinate[0]


def get_row(lst, x):
    coordinates = []
    row_index = 0
    row = None
    column_index = 0
    value = 0
    for row in lst:
        column_index = 0
        value = 0
        for value in row:
            if value in (x,):
                coordinates.append((row_index, column_index))
            column_index += 1
        row_index += 1

    coordinates = sorted(coordinates, key=_column_desc)
    return sorted(coordinates, key=_row_asc)


assert get_row([], 1) == []
assert get_row([[]], 0) == []
assert get_row([[0]], 0) == [(0, 0)]
assert get_row([[0]], 1) == []
assert get_row([[1, 1, 1]], 1) == [(0, 2), (0, 1), (0, 0)]
assert get_row([[2, 1, 2], [2], [1, 2, 1, 2]], 2) == [
    (0, 2),
    (0, 0),
    (1, 0),
    (2, 3),
    (2, 1),
]
