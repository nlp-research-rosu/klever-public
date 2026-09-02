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


# CPython constructs U+00E9 and returns "É1"; the supplied K chr rule is
# intentionally restricted to code points below 128 and therefore gets stuck.
unicode_result = solve(chr(233) + "1")
