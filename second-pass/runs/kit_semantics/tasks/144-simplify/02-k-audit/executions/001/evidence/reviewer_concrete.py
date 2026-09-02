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


assert simplify("1/5", "5/1")
assert not simplify("1/6", "2/1")
assert not simplify("7/10", "10/2")
assert simplify("1/1", "1/1")
assert simplify("00012/00003", "00010/00004")
assert not simplify("9007199254740993/9007199254740992", "1/1")
