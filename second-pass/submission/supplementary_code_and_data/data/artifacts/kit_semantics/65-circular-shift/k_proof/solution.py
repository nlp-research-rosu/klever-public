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
