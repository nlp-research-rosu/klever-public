def sort_array(arr):
    return sorted(
        sorted(arr),
        key=lambda value: (
            0
            if value < 0
            else bin(value).count("1")
        ),
    )
