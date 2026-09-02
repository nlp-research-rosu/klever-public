def get_row(lst, x):
    result = []
    row = 0
    for values in lst:
        col = len(values) - 1
        while col >= 0:
            if values[col] == x:
                result = result + [(row, col)]
            col = col - 1
        row = row + 1
    return result
