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
assert sort_array([7, 7, 0, 3, 3, 8, 8, 1]) == [0, 1, 8, 8, 3, 3, 7, 7]
assert sort_array([12, 10, 9, 6, 5, 3]) == [3, 5, 6, 9, 10, 12]
assert sort_array(
    [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 63, 64]
) == [0, 1, 2, 4, 8, 16, 32, 64, 3, 7, 15, 31, 63]
assert sort_array(
    [18446744073709551615, 18446744073709551616, 3]
) == [18446744073709551616, 3, 18446744073709551615]
assert sort_array([-1, 0, 1]) == [-1, 0, 1]
