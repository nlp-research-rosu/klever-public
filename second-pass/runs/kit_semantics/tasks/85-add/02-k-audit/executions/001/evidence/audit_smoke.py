def add(lst):
    result = 0
    odd = False
    value = 0
    for value in lst:
        if odd:
            if value % 2 == 0:
                result += value
        odd = not odd
    return result


documented = add([4, 2, 6, 7])
empty_boundary = add([])
singleton = add([10])
odd_value_at_odd_index = add([8, 3])
zero_at_odd_index = add([9, 0])
negative_even_at_odd_indices = add([1, -2, 3, -4])
mixed_branches = add([2, 4, 6, 7, 8, -10])
