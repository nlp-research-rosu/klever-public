def circular_shift(x, shift):
    s = str(x)
    if shift > len(s):
        return s[::-1]
    return s[-shift:] + s[:-shift]
