def median(l: list):
    values = sorted(l)
    middle = len(values) // 2
    if len(values) % 2 == 1:
        return values[middle]
    return (values[middle] + values[middle + 1]) / 2.0
