def same_chars(s0: str, s1: str):
    return set(s0) == set(s1)


assert same_chars("eabcdzzzz", "dddzzzzzzzddeddabc")
assert same_chars("abcd", "dddddddabc")
assert same_chars("dddddddabc", "abcd")
assert not same_chars("eabcd", "dddddddabc")
assert not same_chars("abcd", "dddddddabce")
assert not same_chars("eabcdzzzz", "dddzzzzzzzddddabc")
