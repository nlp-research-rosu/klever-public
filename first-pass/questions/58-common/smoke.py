def common(l1, l2):
    out = []
    for e1 in l1:
        if e1 in l2:
            if e1 not in out:
                out = out + [e1]
    return sorted(out)
assert common([1,4,3,34,653,2,5],[5,7,1,5,9,653,121]) == [1,5,653]
assert common([5,3,2,8],[3,2]) == [2,3]
assert common([1,2],[3,4]) == []
