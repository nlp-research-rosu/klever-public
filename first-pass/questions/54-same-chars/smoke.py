def same_chars(s0, s1):
    return set(s0) == set(s1)


# Smoke checks from the prompt docstring (NOT hidden tests).
assert same_chars('eabcdzzzz', 'dddzzzzzzzddeddabc') == True
assert same_chars('abcd', 'dddddddabc') == True
assert same_chars('dddddddabc', 'abcd') == True
assert same_chars('eabcd', 'dddddddabc') == False
assert same_chars('abcd', 'dddddddabce') == False
assert same_chars('eabcdzzzz', 'dddzzzzzzzddddabc') == False
