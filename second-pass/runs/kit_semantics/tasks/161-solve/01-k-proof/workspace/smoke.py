def solve(s):
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


example_digits = solve("1234")
example_letters = solve("ab")
example_mixed = solve("#a@C")
empty = solve("")
