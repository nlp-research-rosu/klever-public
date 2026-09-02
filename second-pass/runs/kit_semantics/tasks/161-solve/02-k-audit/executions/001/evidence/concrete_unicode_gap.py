def solve(s):
    """Toggle letter case, or reverse a string containing no letters."""
    swapped = ""
    reversed_s = ""
    has_letter = False
    c = ""
    for c in s:
        reversed_s = c + reversed_s
        if c.isalpha():
            swapped += c.swapcase()
            has_letter = True
        else:
            swapped += c
    if has_letter:
        return swapped
    return reversed_s


unicode_gap = solve("é1")
