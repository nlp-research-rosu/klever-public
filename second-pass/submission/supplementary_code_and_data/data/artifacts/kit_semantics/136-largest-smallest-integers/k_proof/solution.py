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

    return (
        None if largest_negative == 0 else largest_negative,
        None if smallest_positive == 0 else smallest_positive,
    )
