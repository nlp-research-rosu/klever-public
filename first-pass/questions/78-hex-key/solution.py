def hex_key(num):
    count = 0
    c = ""
    code = 0
    for c in num:
        code = ord(c)
        if code == 50 or code == 51 or code == 53 or code == 55 or code == 66 or code == 68:
            count = count + 1
    return count
