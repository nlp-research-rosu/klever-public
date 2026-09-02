def unique(l):
    out = []
    for x in l:
        if x not in out:
            out = out + [x]
    return sorted(out)
assert unique([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [0, 2, 3, 5, 9, 123]
assert unique([1, 1, 1]) == [1]
assert unique([]) == []
