def max_element(l: list):
    return max(l)


assert max_element([1, 2, 3]) == 3
assert max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]) == 123
assert max_element([-7]) == -7
assert max_element([3, 2, 1]) == 3
assert max_element([1, 2, 3]) == 3
assert max_element([4, 4, 4]) == 4
assert max_element([2, -1, 9, 9, 0]) == 9
assert max_element([-9223372036854775808, 9223372036854775807]) == 9223372036854775807
