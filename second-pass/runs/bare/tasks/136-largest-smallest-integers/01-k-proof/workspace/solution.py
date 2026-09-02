def largest_smallest_integers(lst):
    largest_negative = None
    smallest_positive = None

    for value in lst:
        if value < 0:
            if largest_negative is None:
                largest_negative = value
            else:
                if value > largest_negative:
                    largest_negative = value

        if value > 0:
            if smallest_positive is None:
                smallest_positive = value
            else:
                if value < smallest_positive:
                    smallest_positive = value

    return (largest_negative, smallest_positive)
