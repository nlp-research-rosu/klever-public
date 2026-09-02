# solution.py — canonical verbatim minus the docstring (one function; real
# str(x), len, and slices).


def circular_shift(x, shift):
    s = str(x)
    if shift > len(s):
        return s[::-1]
    else:
        return s[len(s) - shift:] + s[:len(s) - shift]
