"""Concrete ASCII witnesses for both formal entry-claim preconditions."""


def solve(s):
    result = s.swapcase()
    if result == s:
        return s[::-1]
    return result


# Letter branch: mapSwap([97]) = [65] != [97].
assert solve("a") == "A"
assert solve("a1B!") == "A1b!"

# No-letter branch: mapSwap is identity, so reversal is required.
assert solve("") == ""
assert solve("0") == "0"
assert solve("12!?") == "?!21"
