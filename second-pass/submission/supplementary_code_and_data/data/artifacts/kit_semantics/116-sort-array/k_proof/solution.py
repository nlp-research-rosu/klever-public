def sort_array(arr):
    return sorted(
        sorted(arr),
        key=lambda value: bin(value).count("1"),
    )
