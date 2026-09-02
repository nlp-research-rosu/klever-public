def same_chars(s0: str, s1: str):
    return set(s0) == set(s1)


example_1 = same_chars("eabcdzzzz", "dddzzzzzzzddeddabc")
example_2 = same_chars("abcd", "dddddddabc")
example_3 = same_chars("dddddddabc", "abcd")
example_4 = same_chars("eabcd", "dddddddabc")
example_5 = same_chars("abcd", "dddddddabce")
example_6 = same_chars("eabcdzzzz", "dddzzzzzzzddddabc")
