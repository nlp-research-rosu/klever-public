def words_string(s):
    return s.replace(",", " ").split()


assert words_string("Hi, my name is John") == [
    "Hi", "my", "name", "is", "John"
]
assert words_string("") == []
assert words_string(",") == []
assert words_string("a,,b") == ["a", "b"]
assert words_string("  alpha,,beta\tgamma\n") == ["alpha", "beta", "gamma"]
assert words_string(",a,") == ["a"]
