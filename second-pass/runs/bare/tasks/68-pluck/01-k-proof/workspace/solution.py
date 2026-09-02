def pluck(arr):
    return min(
        [[value, index] for index, value in enumerate(arr) if value % 2 == 0],
        default=[],
    )
