def circular_shift(x, shift):
    s = str(x)
    return (
        s[::-1]
        if shift > len(s)
        else (
            s
            if shift < 0
            else (s + s)[len(s) - shift:2 * len(s) - shift]
        )
    )


assert circular_shift(12, 1) == "21"
assert circular_shift(12, 2) == "12"
assert circular_shift(12, 3) == "21"
assert circular_shift(100, 1) == "010"
assert circular_shift(1234, 0) == "1234"
assert circular_shift(1234, 4) == "1234"
assert circular_shift(1234, -3) == "1234"
assert circular_shift(-120, 2) == "20-1"
