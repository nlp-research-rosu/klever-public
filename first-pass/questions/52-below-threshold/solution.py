def below_threshold(l, t):
    for e in l:
        if e >= t:
            return False
    return True
