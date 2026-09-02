def largest_smallest_integers(lst):
    largest_negative = 0
    smallest_positive = 0
    value = 0

    for value in lst:
        if value < 0:
            if largest_negative == 0 or value > largest_negative:
                largest_negative = value
        if value > 0:
            if smallest_positive == 0 or value < smallest_positive:
                smallest_positive = value

    if largest_negative == 0:
        largest_negative = None
    if smallest_positive == 0:
        smallest_positive = None

    return (largest_negative, smallest_positive)


assert largest_smallest_integers([2, 4, 1, 3, 5, 7]) == (None, 1)
assert largest_smallest_integers([]) == (None, None)
assert largest_smallest_integers([0]) == (None, None)
assert largest_smallest_integers([-5, -2, -9]) == (-2, None)
assert largest_smallest_integers([-1, 8, -3, 2, 0]) == (-1, 2)
