def iscube(a):
    if a < 0:
        a = -a

    candidate = 0
    while candidate * candidate * candidate < a:
        candidate += 1

    return candidate * candidate * candidate == a
