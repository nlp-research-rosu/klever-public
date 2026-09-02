def can_arrange(arr):
    result = -1
    index = 0
    previous = 0
    for current in arr:
        if index > 0:
            if current < previous:
                result = index
        previous = current
        index = index + 1
    return result
