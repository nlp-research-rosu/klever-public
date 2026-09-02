def sort_array(array):
    if not array:
        return sorted(array)
    return sorted(
        array,
        reverse=(array[0] + array[-1]) % 2 == 0,
    )


assert sort_array([]) == []
assert sort_array([5]) == [5]
assert sort_array([2, 4, 3, 0, 1, 5]) == [0, 1, 2, 3, 4, 5]
assert sort_array([2, 4, 3, 0, 1, 5, 6]) == [6, 5, 4, 3, 2, 1, 0]
assert sort_array([0, 1]) == [0, 1]
assert sort_array([1, 1]) == [1, 1]
assert sort_array([3, 1, 2, 1]) == [3, 2, 1, 1]

original = [2, 4, 3, 0, 1, 5, 6]
result = sort_array(original)
assert original == [2, 4, 3, 0, 1, 5, 6]
assert result == [6, 5, 4, 3, 2, 1, 0]
