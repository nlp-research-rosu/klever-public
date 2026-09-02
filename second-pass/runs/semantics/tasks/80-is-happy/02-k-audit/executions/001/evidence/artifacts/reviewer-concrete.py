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
assert is_happy("abc")
assert not is_happy("aab")
assert not is_happy("aba")
assert not is_happy("abb")
assert is_happy("abcd")
assert not is_happy("abcaab")
assert not is_happy("abcaba")
assert not is_happy("abcabb")
assert is_happy("abcabc")
assert not is_happy("abcabcaa")
