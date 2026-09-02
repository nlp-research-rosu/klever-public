def pluck(arr):
    smallest = -1
    smallest_index = -1
    index = 0
    value = 0
    for value in arr:
        if value % 2 == 0:
            if smallest == -1:
                smallest = value
                smallest_index = index
            else:
                if value < smallest:
                    smallest = value
                    smallest_index = index
        index += 1
    if smallest == -1:
        return []
    return [smallest, smallest_index]
