"""Reviewer-authored concrete execution cases for the supplied MPY semantics."""


def circular_shift(x, shift):
    s = str(x)
    return (
        s[::-1]
        if shift > len(s)
        else (
            s
            if shift < 0
            else (s + s)[len(s) - shift : 2 * len(s) - shift]
        )
    )


assert circular_shift(0, 0) == "0"
assert circular_shift(0, 1) == "0"
assert circular_shift(0, 2) == "0"
assert circular_shift(12, 1) == "21"
assert circular_shift(12, 2) == "12"
assert circular_shift(12, 3) == "21"
assert circular_shift(100, 1) == "010"
assert circular_shift(12345, 4) == "23451"
assert circular_shift(12345, 5) == "12345"
assert circular_shift(12345, -1) == "12345"
assert circular_shift(-120, 1) == "0-12"
assert circular_shift(-120, 2) == "20-1"
assert circular_shift(-120, 4) == "-120"
assert circular_shift(-120, 5) == "021-"
assert circular_shift(12345678901234567890, 3) == "89012345678901234567"
