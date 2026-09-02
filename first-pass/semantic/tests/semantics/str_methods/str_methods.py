# pure string methods
assert "ABC".isupper()
assert not "ABc".isupper()
assert not "123".isupper()
assert not "".isupper()
assert "abc".islower()
assert not "aBc".islower()
assert "abc".isalpha()
assert not "ab1".isalpha()
assert not "".isalpha()
assert "123".isdigit()
assert not "12a".isdigit()
assert "AbC".lower() == "abc"
assert "AbC".upper() == "ABC"
assert "AbC".swapcase() == "aBc"
assert "abcdef".startswith("abc")
assert not "abcdef".startswith("xyz")
assert "abc".startswith("")
assert not "ab".startswith("abc")
# per-char in a loop (the common usage)
u = 0
for c in "aB3cD":
    if c.isupper():
        u = u + 1
assert u == 2
