def solve(s):
    result = s.swapcase()
    if result == s:
        return s[::-1]
    return result


# Documented examples and both control-flow branches.
assert solve("1234") == "4321"
assert solve("ab") == "AB"
assert solve("#a@C") == "#A@c"
assert solve("") == ""
assert solve("#") == "#"
assert solve("a1B!") == "A1b!"
assert solve("@AZ[\\`az{") == "@az[\\`AZ{"
