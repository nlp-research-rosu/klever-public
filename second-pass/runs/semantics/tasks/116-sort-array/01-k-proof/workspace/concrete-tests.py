def sort_array(arr):
    return sorted(
        sorted(arr),
        key=lambda value: (
            0
            if value < 0
            else bin(value).count("1")
        ),
    )


assert sort_array([]) == []
assert sort_array([0]) == [0]
assert sort_array([1, 5, 2, 3, 4]) == [1, 2, 4, 3, 5]
assert sort_array([1, 0, 2, 3, 4]) == [0, 1, 2, 4, 3]
assert sort_array([7, 3, 5, 6, 9, 8]) == [8, 3, 5, 6, 9, 7]
assert sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
