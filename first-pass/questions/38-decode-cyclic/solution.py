def decode_cyclic(s):
    result = ""
    c0 = ""
    c1 = ""
    buf = ""
    count = 0
    ch = ""
    for ch in s:
        if count == 0:
            c0 = ch
        elif count == 1:
            c1 = ch
        buf = buf + ch
        count = count + 1
        if count == 3:
            result = result + ch + c0 + c1
            buf = ""
            count = 0
    result = result + buf
    return result
