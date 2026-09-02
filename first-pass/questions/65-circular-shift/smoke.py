# solution.py — canonical verbatim minus the docstring (one function; real
# str(x), len, and slices).


def circular_shift(x, shift):
    s = str(x)
    if shift > len(s):
        return s[::-1]
    else:
        return s[len(s) - shift:] + s[:len(s) - shift]


assert circular_shift(12, 1) == "21"
assert circular_shift(12, 2) == "12"
assert circular_shift(100, 5) == "001"
