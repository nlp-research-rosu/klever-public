def count_ones(n):
    return n.bit_count()


def comes_before(a, b):
    return count_ones(a) < count_ones(b) or (
        count_ones(a) == count_ones(b) and a <= b
    )


def insert_sorted(x, values):
    if values == []:
        return [x]
    if comes_before(x, values[0]):
        return [x] + values
    return [values[0]] + insert_sorted(x, values[1:])


def sort_array(arr):
    if arr == []:
        return []
    return insert_sorted(arr[0], sort_array(arr[1:]))
