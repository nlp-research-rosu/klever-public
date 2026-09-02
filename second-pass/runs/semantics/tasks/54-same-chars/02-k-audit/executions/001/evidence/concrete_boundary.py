"""Reviewer-authored concrete MPY harness for same_chars."""


def same_chars(s0: str, s1: str):
    return set(s0) == set(s1)


# Empty, one-sided membership failures, duplicate/order invariance, and case.
assert same_chars("", "")
assert not same_chars("", "a")
assert not same_chars("a", "")
assert same_chars("a", "aaaa")
assert same_chars("ab", "bbaa")
assert not same_chars("ab", "a")
assert not same_chars("a", "ab")
assert not same_chars("Aa", "aa")
