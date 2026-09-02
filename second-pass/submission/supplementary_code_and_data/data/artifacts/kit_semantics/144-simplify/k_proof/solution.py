def simplify(x, n):
    part = 0
    a = 0
    b = 0
    c = 0
    d = 0
    ch = ""
    for ch in x + "/" + n:
        if ch == "/":
            part = part + 1
        elif part == 0:
            a = a * 10 + (ord(ch) - 48)
        elif part == 1:
            b = b * 10 + (ord(ch) - 48)
        elif part == 2:
            c = c * 10 + (ord(ch) - 48)
        else:
            d = d * 10 + (ord(ch) - 48)
    return (a * c) % (b * d) == 0
