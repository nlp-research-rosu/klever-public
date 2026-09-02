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
