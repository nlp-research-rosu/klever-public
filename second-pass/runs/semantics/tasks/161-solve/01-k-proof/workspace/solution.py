def solve(s):
    result = s.swapcase()
    if result == s:
        return s[::-1]
    return result
