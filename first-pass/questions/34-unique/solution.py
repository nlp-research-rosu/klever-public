def unique(l):
    out = []
    for x in l:
        if x not in out:
            out = out + [x]
    return sorted(out)
