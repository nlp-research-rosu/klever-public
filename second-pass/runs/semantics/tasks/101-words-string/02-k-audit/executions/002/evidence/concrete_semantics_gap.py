def words_string(s):
    return s.replace(",", " ").split()


# Python str.split() treats vertical tab (U+000B) as whitespace.
assert words_string("a\vb") == ["a", "b"]
