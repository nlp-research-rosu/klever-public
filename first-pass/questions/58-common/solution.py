def common(l1, l2):
    out = []
    for e1 in l1:
        if e1 in l2:
            if e1 not in out:
                out = out + [e1]
    return sorted(out)
