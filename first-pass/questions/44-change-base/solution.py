def change_base(x, base):
    ret = ''
    while x > 0:
        ret = str(x % base) + ret
        x //= base
    return ret
