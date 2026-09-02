def is_happy(s):
    if len(s) < 3:
        return False
    i = 0
    while i + 2 < len(s):
        if s[i] == s[i + 1]:
            return False
        if s[i] == s[i + 2]:
            return False
        if s[i + 1] == s[i + 2]:
            return False
        i += 1
    return True


assert not is_happy("")
assert not is_happy("a")
assert not is_happy("aa")
assert not is_happy("aaa")
assert not is_happy("aab")
assert not is_happy("aba")
assert not is_happy("abb")
assert is_happy("abc")
assert is_happy("abcd")
assert not is_happy("aabb")
assert is_happy("adb")
assert not is_happy("xyy")
assert is_happy("abcabc")
assert not is_happy("abac")
assert not is_happy("abcc")
assert is_happy("abcad")
assert is_happy("abcdefgh")
assert not is_happy("abcdefghh")
