def is_sorted(lst):
    result = True
    previous = 0
    repeats = 0
    for number in lst:
        if number < previous:
            result = False
        if number == previous:
            repeats += 1
        else:
            repeats = 1
        if repeats > 2:
            result = False
        previous = number
    return result
