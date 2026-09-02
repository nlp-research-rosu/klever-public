def insert_sorted(x, xs):
    if xs == []:
        return [x]
    else:
        if x <= xs[0]:
            return [x] + xs
        else:
            return [xs[0]] + insert_sorted(x, xs[1:])


def sort_values(xs):
    if xs == []:
        return []
    else:
        return insert_sorted(xs[0], sort_values(xs[1:]))


def even_values(l):
    if l == []:
        return []
    else:
        return [l[0]] + even_values(l[2:])


def rebuild(l, evens):
    if l == []:
        return []
    else:
        if l[1:] == []:
            return [evens[0]]
        else:
            return [evens[0], l[1]] + rebuild(l[2:], evens[1:])


def sort_even(l: list):
    # Sensitivity mutation: bypass the three program-defined helpers.
    return l
