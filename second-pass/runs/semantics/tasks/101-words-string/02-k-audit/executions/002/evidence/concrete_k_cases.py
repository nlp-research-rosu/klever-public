def words_string(s):
    return s.replace(",", " ").split()


assert words_string("Hi, my name is John") == [
    "Hi", "my", "name", "is", "John"
]
assert words_string("") == []
assert words_string(",,,") == []
assert words_string(" a,,b \t c\n") == ["a", "b", "c"]
assert words_string("alpha\u00a0beta") == ["alpha", "beta"]
