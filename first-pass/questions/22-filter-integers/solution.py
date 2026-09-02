def filter_integers(values):
    result = []
    i = 0
    int_type = int
    for i in range(len(values)):
        if isinstance(values[i], int_type):
            result = result + [values[i]]
    return result
