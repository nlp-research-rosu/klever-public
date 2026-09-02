def all_prefixes(string):
    prefixes = []
    prefix = ""
    char = ""
    for char in string:
        prefix = prefix + char
        prefixes.append(prefix)
    return prefixes


assert all_prefixes("") == []
assert all_prefixes("a") == ["a"]
assert all_prefixes("abc") == ["a", "ab", "abc"]
assert all_prefixes("xy") == ["x", "xy"]
assert all_prefixes("a a") == ["a", "a ", "a a"]
assert all_prefixes("!?") == ["!", "!?"]
