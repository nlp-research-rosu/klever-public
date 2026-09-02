def solve(s):
    result = s.swapcase()
    if result == s:
        return s[::-1]
    return result


# This is the submitted algorithm's result in the supplied ASCII case model.
# It is intentionally not the trusted canonical result ("1中").
assert solve("1中") == "中1"
