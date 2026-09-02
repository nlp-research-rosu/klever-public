def after_slice(s):
    tail = s[1:]
    marker = "after"
    return tail + marker


# Each case observes the continuation after the bridged slice through both a
# state update and the returned value.
assert after_slice("") == "after"
assert after_slice("a") == "after"
assert after_slice("ab") == "bafter"
assert after_slice("abcd") == "bcdafter"
