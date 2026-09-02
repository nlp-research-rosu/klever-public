def solve(s):
    result = s.swapcase()
    if result == s:
        return s[::-1]
    return result


assert solve("1234") == "4321"
assert solve("ab") == "AB"
assert solve("#a@C") == "#A@c"
assert solve("") == ""
assert solve("a1B!") == "A1b!"
