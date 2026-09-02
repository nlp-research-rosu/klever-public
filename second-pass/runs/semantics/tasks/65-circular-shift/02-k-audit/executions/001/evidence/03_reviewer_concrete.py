def circular_shift(x, shift):
    s = str(x)
    if shift > len(s):
        return s[::-1]
    return s[-shift:] + s[:-shift]


assert circular_shift(12, 1) == "21"
assert circular_shift(12, 2) == "12"
assert circular_shift(12, 3) == "21"
assert circular_shift(12345, 0) == "12345"
assert circular_shift(12345, 4) == "23451"
assert circular_shift(12345, 5) == "12345"
assert circular_shift(12345, 6) == "54321"
assert circular_shift(0, 0) == "0"
assert circular_shift(0, 1) == "0"
assert circular_shift(0, 2) == "0"
assert circular_shift(-123, 1) == "3-12"
assert circular_shift(-123, 5) == "321-"
